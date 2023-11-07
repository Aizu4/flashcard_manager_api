from django.contrib import admin
from django.urls import path

from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

from v1.routers import deck_router, card_router, user_router

api = NinjaExtraAPI()
api.add_router('/decks/', deck_router)
api.add_router('/cards/', card_router)
api.add_router('/users/', user_router)

api.register_controllers(NinjaJWTSlidingController)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', api.urls)
]
