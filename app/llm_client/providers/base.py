from abc import ABC, abstractmethod

class LLMProvider(ABC):

    @abstractmethod
    def complete(self,messages, **kwargs):
        pass

    @abstractmethod
    def stream(self, messages, **kwargs):
        pass