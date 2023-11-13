from ninja import Router
from ninja_jwt.authentication import JWTAuth

from v1.schemas.user_schemas import UserSchema

router = Router(auth=JWTAuth())


@router.get('/me', response=UserSchema)
def me(request):
    return request.auth
