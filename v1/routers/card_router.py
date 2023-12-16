from ninja import Router
from ninja import Router
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth

from v1.models import Card, Deck
from v1.schemas.card_schemas import CardSchema, CardPostSchema, CardPatchSchema
from v1.services import ImageService, SentenceService

router = Router(auth=JWTAuth())


@router.get('/', response=list[CardSchema])
def get_cards(request):
    return Card.visible_by(request.auth).all()


@router.get('/{int:id}', response=CardSchema)
def get_card(request, id: str):
    return Card.visible_by(request.auth).get(id=id)


@router.post('/', response=CardSchema)
def post_card(request, deck_id: str, card: CardPostSchema):
    if not Deck.objects.get(id=deck_id).is_editable_by(request.auth):
        return

    return Card.objects.create(deck_id=deck_id, **card.dict(exclude_defaults=True))


@router.patch('/{uuid:id}', response=CardSchema)
def patch_card(request, id: str, card_patch: CardPatchSchema):
    card = Card.ediable_by(request.auth).get(id=id)
    card.update(**card_patch.dict(exclude_defaults=True))
    card.save()
    return card


@router.delete('/{uuid:id}')
def delete_card(request, id: str):
    Card.ediable_by(request.auth).get(id=id).delete()


@router.get('/{uuid:id}/image')
def get_image(request, id: str):
    return ImageService().get_image(Card.visible_by(request.auth).get(id=id))


@router.post('/{uuid:id}/image')
def upload_image(request, id: str, image: UploadedFile):
    card = Card.ediable_by(request.auth).get(id=id)
    return ImageService().save_image(card, image)


@router.delete('/{uuid:id}/image')
def delete_image(request, id: str):
    card = Card.ediable_by(request.auth).get(id=id)
    card.image.delete()
    card.save()


@router.post('/{uuid:id}/generate_sentences', response=CardSchema)
def patch_and_generate_sentences(request, id: str, card_patch: CardPatchSchema):
    card = Card.ediable_by(request.auth).get(id=id)
    card.update(**card_patch.dict(exclude_defaults=True))
    front, back = SentenceService(
        language_from=card.deck.front_language_code,
        language_to=card.deck.back_language_code,
        retries=3
    ).generate_sentences(card.front, card.back)

    if front and back:
        card.example_front = front
        card.example_back = back
        card.save()

    return card
