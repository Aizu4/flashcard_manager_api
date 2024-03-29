from django.http import HttpResponse
from ninja import Router, UploadedFile, Form
from ninja_jwt.authentication import JWTAuth

from v1.models import Deck, Tag
from v1.schemas.deck_schemas import DeckSchema, DeckPostSchema, DeckPatchSchema, DeckSimpleSchema, \
    DeckCSVSettingsSchema, DeckQuizSchema, DeckCSVImportSchema
from v1.schemas.tag_schemas import TagPostSchema, TagSchema, TagPatchSchema
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


@router.post('/{uuid:id}/import')
def import_deck(request, id: str, data: DeckCSVImportSchema):
    deck = Deck.editable_by(request.auth).get(id=id)
    CSVService(separator=data.separator, quotechar=data.quotechar).import_deck(deck, data.file)
    return HttpResponse(status=201)


@router.post('/{uuid:id}/export')
def export_deck(request, id: str, settings: DeckCSVSettingsSchema):
    deck = Deck.visible_by(request.auth).get(id=id)
    return CSVService(**settings.dict(exclude_none=True)).export_deck(deck)


@router.get('/{uuid:id}/export_images')
def export_deck_images(request, id: str):
    deck = Deck.visible_by(request.auth).get(id=id)
    return ImagesToZipService().export_images(deck)


@router.get('/s/{str:slug}', response=DeckQuizSchema, auth=None)
def get_public_deck_by_slug(_request, slug: str):
    try:
        return Deck.visible_by(None).get(slug=slug)
    except Deck.DoesNotExist:
        return HttpResponse(status=404)


@router.patch('/{uuid:id}/s')
def patch_deck_slug(request, id: str, slug: str):
    if Deck.objects.filter(slug=slug, public=True).exists():
        return HttpResponse(status=409)  # Conflict
    deck = Deck.editable_by(request.auth).filter(public=True).get(id=id)
    deck.slug = slug
    deck.save()


# ================================ #
# ============= Tags ============= #
# ================================ #


@router.post('/{uuid:id}/tags', response=TagSchema)
def post_tag_to_deck(request, id: str, tag: TagPostSchema):
    deck = Deck.editable_by(request.auth).get(id=id)
    return Tag.objects.create(deck=deck, **tag.dict(exclude_defaults=True))


@router.patch('/{uuid:id}/tags/{uuid:tag_id}', response=TagSchema)
def patch_tag_from_deck(request, id: str, tag_id: str, tag_patch: TagPatchSchema):
    deck = Deck.editable_by(request.auth).get(id=id)
    tag = deck.tag_set.get(id=tag_id)
    tag.update(**tag_patch.dict(exclude_defaults=True))
    tag.save()
    return tag


@router.delete('/{uuid:id}/tags/{uuid:tag_id}')
def delete_tag_from_deck(request, id: str, tag_id: str):
    deck = Deck.editable_by(request.auth).get(id=id)
    deck.tag_set.get(id=tag_id).delete()
