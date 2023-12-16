from . import openAIClient
from iso639 import Lang

from .prompts import SENTENCE_PROMPT


def _language_from_code(language_code: str):
    return Lang(language_code).name


class SentenceService:
    def __init__(self, language_from: str, language_to: str, retries: int = 3):
        self.client = openAIClient
        self.language_from = _language_from_code(language_from)
        self.language_to = _language_from_code(language_to)
        self.retries = retries

    def generate_sentences(self, front_word: str, back_word: str):
        for _ in range(self.retries):
            front, back = self._generate_sentences(front_word, back_word)
            if front and back:
                return front, back
        return None, None

    def _generate_sentences(self, front_word: str, back_word: str):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": SENTENCE_PROMPT.format(front_language=self.language_from, back_language=self.language_to)
                },
                {
                    "role": "user",
                    "content": f"{front_word} - {back_word}" if back_word else front_word
                }
            ], **PARAMS
        )

        content = response.choices[0].message.content

        if response.choices[0].finish_reason != "stop":
            print("Invalid response from OpenAI API for", front_word, back_word, content, sep='; ')
            return None, None

        if '#' in content or content.count("|") != 1:
            print("Invalid response from OpenAI API for", front_word, back_word, content, sep='; ')
            return None, None

        front_word, back_word = content.split("|")
        return front_word.strip(), back_word.strip()


PARAMS = dict(
    temperature=1,
    max_tokens=128,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)
