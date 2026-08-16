class LLMError(Exception):
    """Base class for all LLM-related exceptions."""
    
class LLMTimeoutError(LLMError):
    """LLM request timed out."""

class LLMRateLimitError(LLMError):
    """Provider rate limit exceeded."""

class LLMProviderError(LLMError):
    """Provider returned an error."""

class StructuredOutputError(LLMError):
    """Structured output could not be parsed."""