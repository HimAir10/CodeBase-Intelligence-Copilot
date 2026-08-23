import json

from app.llm_client.exceptions import StructuredOutputError
from app.llm_client.streaming import StreamingResponse
from app.llm_client.retry import RetryHandler
from app.llm_client.token_counter import TikTokenCounter
from app.llm_client.structured import StructuredOutputParser
from app.llm_client.providers.openrouter import OpenRouterProvider

class LLMClient:

    def __init__(
        self,
        provider,
        model,
        retry_handler,
        token_counter,
        structured_parser,
        timeout,
        structured_repair_attempts,
    ):
        self.provider = provider
        self.model = model
        self.retry_handler = retry_handler
        self.token_counter = token_counter
        self.structured_parser = structured_parser
        self.timeout = timeout
        self.structured_repair_attempts = structured_repair_attempts

    def complete(self, messages, **kwargs):

        return self.retry_handler.execute(
            lambda: self.provider.complete(
                messages,
                **kwargs
            )
        )

    def stream(self, messages, **kwargs):
        provider_stream = self.retry_handler.execute(
            lambda: self.provider.stream(messages, **kwargs)
        )
        return StreamingResponse().process(provider_stream)

    def structured(self, messages, response_model, **kwargs):
        response = self.complete(messages, **kwargs)

        for attempt in range(self.structured_repair_attempts + 1):
            try:
                return self.structured_parser.parse(
                    response.content,
                    response_model,
                )
            except StructuredOutputError:
                if attempt == self.structured_repair_attempts:
                    raise

                response = self.complete(
                    self._repair_messages(response.content, response_model),
                    **kwargs,
                )

    @staticmethod
    def _repair_messages(invalid_content, response_model):
        schema = json.dumps(response_model.model_json_schema(), indent=2)
        return [
            {
                "role": "system",
                "content": (
                    "Repair the supplied LLM output. Return only valid JSON that "
                    "conforms exactly to the supplied JSON Schema. Do not include "
                    "Markdown, commentary, or code fences."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"JSON Schema:\n{schema}\n\n"
                    f"Output to repair:\n{invalid_content}"
                ),
            },
        ]



def create_llm_client(config):

    provider  = OpenRouterProvider(
        api_key=config.api_key,
        model=config.model,
        timeout=config.timeout,
    )

    

    retry_handler = RetryHandler(config.retry_policy)

    token_counter = TikTokenCounter(config.model)

    parser = StructuredOutputParser()

    return LLMClient(
        provider=provider,
        model = config.model,
        retry_handler=retry_handler,
        token_counter=token_counter,
        structured_parser=parser,
        timeout=config.timeout,
        structured_repair_attempts=config.structured_repair_attempts,
    )
