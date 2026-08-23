from openai import OpenAI

from app.llm_client.providers.base import LLMProvider
from app.llm_client.types import LLMResponse, TokenUsage


class OpenRouterProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, timeout : float):
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.timeout = timeout

    def complete(self, messages, **kwargs) -> LLMResponse:
        kwargs.setdefault("timeout", self.timeout)
        raw = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )

        return LLMResponse(
            content=raw.choices[0].message.content,
            model=raw.model,
            usage=TokenUsage(
                prompt_tokens=raw.usage.prompt_tokens,
                completion_tokens=raw.usage.completion_tokens,
                total_tokens=raw.usage.total_tokens,
            ) if raw.usage else None,
        )

    def stream(self, messages, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **kwargs,
        )
