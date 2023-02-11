from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/open")
async def open_room():
    return {"message": "Hello World"}


@app.post("/stt")
async def convert_speech(data: UploadFile):
    return {"filename": data.filename}
