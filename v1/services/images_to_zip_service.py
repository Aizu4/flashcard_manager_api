import zipfile
from datetime import datetime

from django.http import HttpResponse

from v1.models import Deck


class ImagesToZipService:
    def __init__(self, compression=zipfile.ZIP_STORED, compression_level: int = 0):
        self.compression = compression
        self.compression_level = compression_level

    def export_images(self, deck: Deck):
        response = HttpResponse(
            content_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{deck.name}_{datetime.now()}.zip"'},
        )

        with zipfile.ZipFile(response, 'w', compression=self.compression, compresslevel=self.compression_level) as file:  # noqa
            for card_id, img in deck.card_set.all().values_list('id', 'image'):
                if img: file.write(img, img.removeprefix('static/cards/images/'))

        return response
