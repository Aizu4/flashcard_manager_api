from ninja import Router
from ninja_jwt.authentication import JWTAuth

from v1.models import Deck
from v1.schemas.deck import DeckSchema, DeckPostSchema, DeckPatchSchema, DeckSimpleSchema

router = Router(auth=JWTAuth())


@router.get('/', response=list[DeckSimpleSchema])
def get_decks(_request):
    return Deck.objects.all()


@router.get('/{uuid:id}', response=DeckSchema)
def get_deck(_request, id: str):
    return Deck.objects.get(id=id)


@router.post('/', response=DeckSchema)
def post_deck(request, deck: DeckPostSchema):
    return Deck.objects.create(user=request.auth, **deck.dict(exclude_defaults=True))


@router.patch('/{uuid:id}', response=DeckSchema)
def patch_deck(_request, id: str, deck_patch: DeckPatchSchema):
    deck = Deck.objects.get(id=id)
    deck.update(**deck_patch.dict(exclude_defaults=True))
    deck.save()
    return deck


@router.delete('/{uuid:id}')
def get_deck(_request, id: str):
    Deck.objects.get(id=id).delete()
