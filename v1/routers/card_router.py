from ninja import Router
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth

from v1.models import Card, Deck
from v1.schemas.card_schemas import CardSchema, CardPostSchema, CardPatchSchema, CardsFromTextPostSchema
from v1.services import ImageService, SentenceService
from v1.services.cards_from_text_service import CardsFromTextService
from v1.services.openai import TranslationService

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


@router.post('/bulk', response=list[CardSchema])
def post_bulk_cards(request, deck_id: str, text: CardsFromTextPostSchema):
    if not Deck.objects.get(id=deck_id).is_editable_by(request.auth):
        return

    return Card.objects.bulk_create(
        CardsFromTextService(
            deck_id, generate_translations=text.generate_translations, generate_sentences=text.generate_sentences
        ).from_bulk(text.content)
    )


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


@router.post('/{uuid:id}/generate_translations', response=CardSchema)
def patch_and_generate_translations(request, id: str, card_patch: CardPatchSchema):
    card = Card.ediable_by(request.auth).get(id=id)
    card.update(**card_patch.dict(exclude_defaults=True))
    translations = TranslationService(
        language_from=card.deck.front_language_code,
        language_to=card.deck.back_language_code,
        retries=3
    ).generate(card.front)

    if translations:
        card.back = '; '.join(translations)
        card.save()

    return card


@router.post('/{uuid:id}/generate_sentences', response=CardSchema)
def patch_and_generate_sentences(request, id: str, card_patch: CardPatchSchema):
    card = Card.ediable_by(request.auth).get(id=id)
    card.update(**card_patch.dict(exclude_defaults=True))
    sentence_pair = SentenceService(
        language_from=card.deck.front_language_code,
        language_to=card.deck.back_language_code,
        retries=3
    ).generate(card.front, card.back)

    if sentence_pair:
        card.example_front, card.example_back = sentence_pair
        card.save()

    return card
