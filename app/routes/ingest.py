# ingest.py

def ingest_document(file):
    # Read the uploaded file
    content = file.file.read().decode("utf-8")


    # Your ingestion logic
    result = {
        "filename": file.filename,
        "length": len(content),
        "content": content
    }

    return result