from fastapi import FastAPI, UploadFile, File, HTTPException
# from routes.ingest import ingest_document
from app.llm_client.llm_client import create_llm_client
from app.llm_client.config import LLM_config, ResponseModel
# app = FastAPI()


# @app.post("/upload")
# async def upload_markdown(file: UploadFile = File(...)):
#     result = ingest_document(file)
#     return result


llm_client = create_llm_client(LLM_config)

response = llm_client.complete(
    messages=[
        {
            "role": "system",
            "content": 'Return only JSON: {"explanation": "..."}',
        },
        {
            "role": "user",
            "content": "Explain FastAPI in one paragraph.",
        },
    ],
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

print(result.explanation)
# for text in llm_client.stream([
#     {"role": "user", "content": "Explain FastAPI in one paragraph."}
# ], max_tokens=5000  ):
#     print(text, end="", flush=True)

