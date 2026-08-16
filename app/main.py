from fastapi import FastAPI, UploadFile, File, HTTPException
from routes.ingest import ingest_document
app = FastAPI()


@app.post("/upload")
async def upload_markdown(file: UploadFile = File(...)):
    result = ingest_document(file)
    return result
    