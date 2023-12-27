from .base_openai_service import BaseOpenAIService
from .prompts import TRANSLATION_PROMPT


class TranslationService(BaseOpenAIService):
    def _generate(self, front_word: str) -> list[str]:
        response = self._response(
            prompt=TRANSLATION_PROMPT.format(
                front_language=self.language_from,
                back_language=self.language_to
            ),
            user_input=front_word,
        )

        if response.choices[0].finish_reason != "stop":
            return []

        content = response.choices[0].message.content
        return [word.strip() for word in content.split("|")]
