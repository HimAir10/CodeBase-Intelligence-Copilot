from pydantic import BaseModel, Field
import os
from app.llm_client.retry import RetryPolicy
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

class ResponseModel(BaseModel):
    explanation: str


class LLMConfig(BaseModel): 
    model : str
    api_key : str
    max_tokens : int = Field(default = 5000, gt = 0)
    temperature : float = Field(default = 0.3, ge = 0.0, le = 2.0)
    timeout : float = Field(default = 60, gt = 0)
    retry_policy : RetryPolicy = Field(default = RetryPolicy())
    response_model : ResponseModel = Field(default = ResponseModel(explanation=""))

client = OpenAI(
    base_url = "https://api.openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

LLM_config = LLMConfig(
    model = "qwen/qwen3.8-27b",
    api_key = os.getenv("OPENROUTER_API_KEY"),
    max_tokens = 5000
)

model = "qwen/qwen3.8-27b"
