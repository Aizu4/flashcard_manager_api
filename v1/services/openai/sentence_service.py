from .base_openai_service import BaseOpenAIService
from .prompts import SENTENCE_PROMPT


class SentenceService(BaseOpenAIService):
    def _generate(self, front_word: str, back_word: str) -> tuple[str, str] | None:
        response = self._response(
            prompt=SENTENCE_PROMPT.format(
                front_language=self.language_from,
                back_language=self.language_to
            ),
            user_input=f"{front_word}|{back_word}",
            temperature=1.05,
        )

        content = response.choices[0].message.content

        if response.choices[0].finish_reason != "stop":
            return None

        if '#' in content or content.count("|") != 1:
            return None

        front_word, back_word = content.split("|")
        return front_word.strip(), back_word.strip()
