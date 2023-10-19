from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI
from ninja.security import django_auth
from ninja_auth.api import router as auth_router

from v1.routers import deck_router

api = NinjaAPI(auth=django_auth, csrf=True)
api.add_router('/decks/', deck_router)
api.add_router('/auth/', auth_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', api.urls)
]
