import csv
from datetime import datetime

from django.http import HttpResponse


class CSVService:
    def __init__(self, separator: str, quotechar: str, with_images: bool = False, with_tags: bool = False):
        self.separator = separator
        self.quotechar = quotechar
        self.rows = ('front', 'back', 'example_front', 'example_back', 'notes')

        if with_tags:
            self.rows += ('tags',)

        if with_images:
            self.rows += ('image_name',)

    def export_deck(self, deck):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{deck.name}_{datetime.now()}.csv"'},
        )

        writer = csv.writer(response, delimiter=self.separator, quotechar=self.quotechar, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(self.rows)

        for card in deck.card_set.prefetch_related('tags'):
            writer.writerow(self.get_attribute_wrapper(card, row) for row in self.rows)

        return response

    @staticmethod
    def get_attribute_wrapper(card, attribute):
        if attribute == 'tags':
            return '; '.join(tag.name for tag in card.tags.all())
        else:
            return getattr(card, attribute)
