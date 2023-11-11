from ninja import Router
from ninja_jwt.authentication import JWTAuth

from v1.models import Card
from v1.schemas.card import CardSchema, CardPostSchema, CardPatchSchema

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


def cards(request):
    if request.auth.is_superuser:
        return Card.objects.all()
    return Card.objects.filter(user=request.auth).all()
