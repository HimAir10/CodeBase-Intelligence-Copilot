import os

from app.llm_client.providers.base import LLMProvider
from app.llm_client.streaming import StreamingResponse
from app.llm_client.retry import RetryHandler
from app.llm_client.token_counter import TikTokenCounter
from app.llm_client.structured import StructuredOutputParser
from app.llm_client.providers.openrouter import OpenRouterProvider
from dotenv import load_dotenv
load_dotenv()

class LLMClient:

    def __init__(
        self,
        provider,
        model,
        retry_handler,
        token_counter,
        structured_parser,
        timeout,
    ):
        self.provider = provider
        self.model = model
        self.retry_handler = retry_handler
        self.token_counter = token_counter
        self.structured_parser = structured_parser
        self.timeout = timeout

    def complete(self, messages, **kwargs):

        return self.retry_handler.execute(
            lambda: self.provider.complete(
                messages,
                **kwargs
            )
        )

    def stream(self, messages, **kwargs):
        provider_stream = self.provider.stream(messages, **kwargs)
        return StreamingResponse().process(provider_stream)

    def structured(self, messages, response_model, **kwargs):
        response = self.complete(messages, **kwargs)

        return self.structured_parser.parse(
            response.content,
            response_model,
        )



def create_llm_client(config):

    provider  = OpenRouterProvider(
        api_key = os.getenv("OPENROUTER_API_KEY"),
        model = config.model
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
    )