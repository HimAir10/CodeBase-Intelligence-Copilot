from abc import ABC, abstractmethod
import tiktoken
class TokenCounter(ABC):

    @abstractmethod
    def count_tokens(self, message : str) -> int: 
        pass

class TikTokenCounter(TokenCounter):

    def __init__(self, model_name : str): 
        self.model_name = model_name

    def count_tokens(self, message : str) -> int: 
        encoding = tiktoken.encoding_for_model(self.model_name)
        return len(encoding.encode(message))
