from http import HTTPStatus

from PIL import Image
from django.http import HttpResponse
from ninja import UploadedFile

from v1.models import Card


class ImageService:
    def __init__(self, max_dim: tuple[int, int] = (800, 600), image_format: str = 'PNG'):
        self.max_dim = max_dim
        self.format = image_format

    def save_image(self, card: Card, image_file: UploadedFile):
        if card.image:
            card.image.delete()

        image_file.name = f"{card.id}.{self.format.lower()}"
        card.image = image_file
        card.save()

        with card.image.open() as image:
            return self._create_response(card, image.read())

    def get_image(self, card: Card):
        if not card.image:
            return HttpResponse(status=HTTPStatus.NO_CONTENT)

        with card.image.open() as image:
            return self._create_response(card, image.read())

    def _create_response(self, card: Card, image: UploadedFile):
        response = HttpResponse(
            content_type=f"image/{self.format.lower()}",
            headers={"Content-Disposition": f'attachment; filename="{card.id}.{self.format.lower()}"'},
        )
        response.write(image)
        return response
