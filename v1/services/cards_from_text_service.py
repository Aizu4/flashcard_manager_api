from v1.models import Card, Deck
from v1.services import SentenceService
from v1.services.openai import TranslationService


class CardsFromTextService:
    def __init__(self, deck_id: str, generate_translations=False, generate_sentences=False):
        self.deck_id = deck_id
        self.generate_translations = generate_translations
        self.generate_sentences = generate_sentences

    def from_bulk(self, text: str) -> list[Card]:
        return [self.from_line(line) for line in text.splitlines()]

    def from_line(self, line: str) -> Card:
        if '>' in line:
            front, back = line.split('>', maxsplit=1)
            card = Card(front=front.strip(), back=back.strip(), deck_id=self.deck_id)
        else:
            card = Card(front=line.strip(), deck_id=self.deck_id)

        if self.generate_sentences or self.generate_translations:
            self._generate_content(card)

        return card

    def _generate_content(self, card: Card) -> None:
        deck = Deck.objects.get(id=self.deck_id)
        language_params = {
            'front_language_code': deck.front_language_code,
            'back_language_code': deck.back_language_code,
        }

        if self.generate_translations:
            back = TranslationService(**language_params).generate(front_word=card.front)
            card.back = back[0] if back else None

        if self.generate_sentences:
            card.example_front, card.example_back = \
                SentenceService(**language_params).generate(front_word=card.front, back_word=card.back)
