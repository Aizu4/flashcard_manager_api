from http import HTTPStatus

from PIL import Image
from django.http import HttpResponse
from ninja import UploadedFile

from v1.models import Card


class ImageService:
    def __init__(self, max_size_mb: float = 1.0):
        self.max_size = self._megabytes_to_bytes(max_size_mb)

    def save_image(self, card: Card, image_file: UploadedFile):
        if len(image_file.read()) > self.max_size:
            return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE)

        if card.image:
            card.image.delete()

        image_file.name = f"{card.id}__{image_file.name}"
        card.image = image_file
        card.save()

        with card.image.open() as image:
            return self._create_response(image)

    def get_image(self, card: Card):
        if not card.image:
            return HttpResponse(status=HTTPStatus.NO_CONTENT)

        with card.image.open() as image:
            return self._create_response(image)

    @staticmethod
    def _create_response(image: UploadedFile):
        extension = image.name.split('.')[-1]

        response = HttpResponse(
            content_type=f"image/{extension}",
            headers={"Content-Disposition": f'attachment'}
        )
        response.write(image.read())
        return response

    @staticmethod
    def _megabytes_to_bytes(megabytes: float) -> int:
        return int(megabytes * 1024 * 1024)
