from iso639 import Lang, exceptions
from openai.types.chat import ChatCompletion

from . import openAIClient


class BaseOpenAIService:
    def __init__(self, language_from: str, language_to: str, retries: int = 3):
        self.client = openAIClient
        self.language_from = self._language_from_code(language_from)
        self.language_to = self._language_from_code(language_to)
        self.retries = retries

    def generate(self, *args, **kwargs) -> any:
        for _ in range(self.retries):
            if result := self._generate(*args, **kwargs):
                return result
        return None

    def _response(self, prompt: str, user_input: str, model: str = "gpt-3.5-turbo", **params) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
            ], **(self._DEFAULT_PARAMS | params)
        )

    def _generate(self, *args, **kwargs) -> any:
        raise NotImplementedError

    @staticmethod
    def _language_from_code(language_code: str) -> str:
        try:
            return Lang(language_code).name
        except exceptions.InvalidLanguageValue:
            return str(language_code)

    _DEFAULT_PARAMS = dict(
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
