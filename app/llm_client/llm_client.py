from app.llm_client.providers.base import LLMProvider
from app.llm_client.retry import RetryHandler
from app.llm_client.token_counter import TokenCounter
from app.llm_client.structured import StructuredOutputParser

class LLMClient:

    def __init__(
        self,
        provider,
        retry_handler,
        token_counter,
        structured_parser,
        timeout,
    ):
        self.provider = provider
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

        return self.provider.stream(
            messages,
            **kwargs
        )

    def structured(
        self,
        messages,
        response_model,
        **kwargs
    ):

        response = self.complete(
            messages,
            **kwargs
        )

        return self.structured_parser.parse(
            response,
            response_model
        )



def create_llm_client(config):

    provider = LLMProvider.create(config)

    retry_handler = RetryHandler(config.retry_policy)

    token_counter = TokenCounter.create(config.model)

    parser = StructuredOutputParser()

    return LLMClient(
        provider=provider,
        retry_handler=retry_handler,
        token_counter=token_counter,
        structured_parser=parser,
        timeout=config.timeout,
    )