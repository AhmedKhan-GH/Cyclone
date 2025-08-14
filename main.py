# main.py
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Root endpoint to avoid 404 on "/"
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI file upload server!"}

# File upload endpoint
@app.post("/upload-test")
async def upload_test(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File received!"
    }
