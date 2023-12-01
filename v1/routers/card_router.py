from ninja import Router
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth

from v1.models import Card
from v1.schemas.card_schemas import CardSchema, CardPostSchema, CardPatchSchema
from v1.services import ImageService

router = Router(auth=JWTAuth())


@router.get('/', response=list[CardSchema])
def get_cards(request):
    return cards(request).all()


@router.get('/{int:id}', response=CardSchema)
def get_card(request, id: str):
    return cards(request).get(id=id)


@router.post('/', response=CardSchema)
def post_card(request, deck_id: str, card: CardPostSchema):
    return Card.objects.create(user=request.auth, deck_id=deck_id, **card.dict(exclude_defaults=True))


@router.patch('/{uuid:id}', response=CardSchema)
def patch_card(request, id: str, card_patch: CardPatchSchema):
    card = cards(request).get(id=id)
    card.update(**card_patch.dict(exclude_defaults=True))
    card.save()
    return card


@router.delete('/{uuid:id}')
def delete_card(request, id: str):
    cards(request).get(id=id).delete()


@router.get('/{uuid:id}/image')
def get_image(request, id: str):
    return ImageService().get_image(cards(request).get(id=id))


@router.post('/{uuid:id}/image')
def upload_image(request, id: str, image: UploadedFile):
    card = cards(request).get(id=id)
    return ImageService().save_image(card, image)


@router.delete('/{uuid:id}/image')
def delete_image(request, id: str):
    card = cards(request).get(id=id)
    card.image.delete()
    card.save()


def cards(request):
    if request.auth.is_superuser:
        return Card.objects.all()
    return Card.objects.filter(deck__user=request.auth).all()
