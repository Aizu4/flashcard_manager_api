from ninja import Router
from ninja_jwt.authentication import JWTAuth

from v1.models import Deck
from v1.schemas.deck_schemas import DeckSchema, DeckPostSchema, DeckPatchSchema, DeckSimpleSchema, DeckCSVSettingsSchema
from v1.services import ImagesToZipService
from v1.services.csv_service import CSVService

router = Router(auth=JWTAuth())


@router.get('/', response=list[DeckSimpleSchema])
def get_decks(request):
    return Deck.visible_by(request.auth).all()


@router.get('/{uuid:id}', response=DeckSchema)
def get_deck(request, id: str):
    return Deck.visible_by(request.auth).get(id=id)


@router.post('/', response=DeckSchema)
def post_deck(request, deck: DeckPostSchema):
    return Deck.objects.create(user=request.auth, **deck.dict(exclude_defaults=True))


@router.patch('/{uuid:id}', response=DeckSchema)
def patch_deck(request, id: str, deck_patch: DeckPatchSchema):
    deck = Deck.editable_by(request.auth).get(id=id)
    deck.update(**deck_patch.dict(exclude_defaults=True))
    deck.save()
    return deck


@router.delete('/{uuid:id}')
def delete_deck(request, id: str):
    Deck.editable_by(request.auth).get(id=id).delete()


@router.delete('/{uuid:id}/empty_cards')
def delete_empty_cards(request, id: str):
    Deck.editable_by(request.auth).get(id=id).card_set.filter(front='', back='').delete()


@router.post('/{uuid:id}/export')
def export_deck(request, id: str, settings: DeckCSVSettingsSchema):
    deck = Deck.visible_by(request.auth).get(id=id)
    return CSVService(**settings.dict(exclude_none=True)).export_deck(deck)


@router.get('/{uuid:id}/export_images')
def export_deck_images(request, id: str):
    deck = Deck.visible_by(request.auth).get(id=id)
    return ImagesToZipService().export_images(deck)
