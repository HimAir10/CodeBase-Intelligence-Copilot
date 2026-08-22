from pydantic import BaseModel, Field
from app.llm_client.retry import RetryPolicy

class LLMConfig(BaseModel): 
    provider : str
    model : str
    temperature : float = Field(default = 0.3, ge = 0.0, le = 2.0)
    timeout : float = Field(default = 60, gt = 0)
    retry_policy : RetryPolicy = Field(default = RetryPolicy())