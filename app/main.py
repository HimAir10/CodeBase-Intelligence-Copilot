from email import message

from fastapi import FastAPI, UploadFile, File, HTTPException
# from routes.ingest import ingest_document
from app.llm_client.llm_client import create_llm_client
from app.llm_client.config import LLM_config, ResponseModel
from app.llm_client.prompt_registry import PromptRegistry
# app = FastAPI()


# @app.post("/upload")
# async def upload_markdown(file: UploadFile = File(...)):
#     result = ingest_document(file)
#     return result


llm_client = create_llm_client(LLM_config)
prompt_registry = PromptRegistry(prompt_dir="/Users/himanshujha/Downloads/ResolveIQ/backend /app/prompts/")
# prompt = prompt_registry.get(
#     prompt_id="fastapi_explanation",
#     version="v1"
# )
def render_message(prompt_id:str,version:str, **variables): 
    prompt = prompt_registry.get(prompt_id, version)
    return [
        {
            "role" : message.role,
            "content" : message.content.format(**variables)
        }
        for message in prompt.messages
    ]

response = llm_client.complete(
    messages=render_message("fastapi_explanation", "v1", topic="FastAPI"),
    max_tokens=300,
)

print("Model:", response.model)

if response.usage:
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Completion tokens:", response.usage.completion_tokens)
    print("Total tokens:", response.usage.total_tokens)

result = llm_client.structured_parser.parse(
    response.content,
    ResponseModel,
)
print("Structured output:", result)
print(result.explanation)
# for text in llm_client.stream([
#     {"role": "user", "content": "Explain FastAPI in one paragraph."}
# ], max_tokens=5000  ):
#     print(text, end="", flush=True)

