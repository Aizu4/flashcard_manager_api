from ninja import Router
from ninja_jwt.authentication import JWTAuth

from v1.models import Card
from v1.schemas.card import CardSchema, CardPostSchema, CardPatchSchema

router = Router(auth=JWTAuth())


@router.get('/', response=list[CardSchema])
def get_cards(_request):
    return Card.objects.all()


@router.get('/{int:id}', response=CardSchema)
def get_card(_request, id: int):
    return Card.objects.get(id=id)


@router.post('/', response=CardSchema)
def post_card(request, deck_id: str, card: CardPostSchema):
    return Card.objects.create(user=request.auth, deck_id=deck_id, **card.dict(exclude_defaults=True))


@router.patch('/{int:id}', response=CardSchema)
def patch_card(_request, id: int, Card_patch: CardPatchSchema):
    card = Card.objects.get(id=id)
    card.update(**Card_patch.dict(exclude_defaults=True))
    card.save()
    return Card
