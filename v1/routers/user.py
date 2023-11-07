from ninja import Router
from ninja_jwt.authentication import JWTAuth

router = Router(auth=JWTAuth())


@router.get('/me')
def me(request):
    return request.auth
