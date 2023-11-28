from ninja import Router
from ninja_jwt.authentication import JWTAuth

from v1.models import Deck
from v1.schemas.deck_schemas import DeckSchema, DeckPostSchema, DeckPatchSchema, DeckSimpleSchema
from v1.services.csv_service import CSVService

router = Router(auth=JWTAuth())


@router.get('/', response=list[DeckSimpleSchema])
def get_decks(request):
    return decks(request).all()


@router.get('/{uuid:id}', response=DeckSchema)
def get_deck(request, id: str):
    return decks(request).get(id=id)


@router.post('/', response=DeckSchema)
def post_deck(request, deck: DeckPostSchema):
    return Deck.objects.create(user=request.auth, **deck.dict(exclude_defaults=True))


@router.patch('/{uuid:id}', response=DeckSchema)
def patch_deck(request, id: str, deck_patch: DeckPatchSchema):
    deck = decks(request).get(id=id)
    deck.update(**deck_patch.dict(exclude_defaults=True))
    deck.save()
    return deck


@router.delete('/{uuid:id}')
def get_deck(request, id: str):
    decks(request).get(id=id).delete()


@router.post('/{uuid:id}/export')
def export_deck(request, id: str):
    deck = decks(request).get(id=id)
    return CSVService().export_deck(deck)


def decks(request):
    if request.auth.is_superuser:
        return Deck.objects.all()
    return Deck.objects.filter(user=request.auth).all()
