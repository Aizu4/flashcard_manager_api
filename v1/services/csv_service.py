import csv
from datetime import datetime

from django.http import HttpResponse


class CSVService:
    def __init__(self, separator: str, quotechar: str, with_images: bool = False):
        self.separator = separator
        self.quotechar = quotechar

        if with_images:
            self.rows = ('front', 'back', 'example_front', 'example_back', 'notes', 'image_name')
        else:
            self.rows = ('front', 'back', 'example_front', 'example_back', 'notes')

    def export_deck(self, deck):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{deck.name}_{datetime.now()}.csv"'},
        )

        writer = csv.writer(response, delimiter=self.separator, quotechar=self.quotechar, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(self.rows)

        for card in deck.card_set.all():
            writer.writerow(getattr(card, row) for row in self.rows)

        return response
