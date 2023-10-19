from ninja import Router

from v1.models import Deck
from v1.schemas.deck import DeckSchema, DeckPostSchema, DeckPatchSchema

router = Router()


@router.get('/', response=list[DeckSchema])
def get_decks(_request):
    return Deck.objects.all()


@router.get('/{int:id}', response=DeckSchema)
def get_deck(_request, id: int):
    return Deck.objects.get(id=id)


@router.post('/', response=DeckSchema)
def post_deck(request, deck: DeckPostSchema):
    return Deck.objects.create(user=request.auth, **deck.dict(exclude_defaults=True))


@router.patch('/{int:id}', response=DeckSchema)
def patch_deck(_request, id: int, deck_patch: DeckPatchSchema):
    deck = Deck.objects.get(id=id)
    deck.update(**deck_patch.dict(exclude_defaults=True))
    deck.save()
    return deck
