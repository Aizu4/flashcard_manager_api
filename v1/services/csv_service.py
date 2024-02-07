import csv
from datetime import datetime
from io import StringIO

from django.http import HttpResponse
from ninja import UploadedFile

from v1.models import Deck, Card


class CSVService:
    def __init__(self, separator: str, quotechar: str, with_images: bool = False, with_tags: bool = False):
        self.separator = separator
        self.quotechar = quotechar
        self.rows = ('front', 'back', 'example_front', 'example_back', 'notes')

        if with_tags:
            self.rows += ('tags',)

        if with_images:
            self.rows += ('image_name',)

    def export_deck(self, deck: Deck):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{deck.name}_{datetime.now()}.csv"'},
        )

        writer = csv.writer(response, delimiter=self.separator, quotechar=self.quotechar, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(self.rows)

        for card in deck.card_set.prefetch_related('tags'):
            writer.writerow(self.get_attribute_wrapper(card, row) for row in self.rows)

        return response

    def import_deck(self, deck: Deck, csv_file: str):
        reader = csv.DictReader(StringIO(csv_file), delimiter=self.separator, quotechar=self.quotechar)

        if not self.fields_valid(reader.fieldnames):
            raise ValueError(f"Invalid fields: {reader.fieldnames}")

        cards = [Card(deck=deck, **card_dict) for card_dict in reader]
        return Card.objects.bulk_create(cards)

    def fields_valid(self, fields):
        fields = fields.copy()
        if 'tags' in fields:
            fields.remove('tags')

        if 'image_name' in fields:
            fields.remove('image_name')

        return fields == [*self.rows]

    @staticmethod
    def get_attribute_wrapper(card, attribute):
        if attribute == 'tags':
            return '; '.join(tag.name for tag in card.tags.all())
        else:
            return getattr(card, attribute)
