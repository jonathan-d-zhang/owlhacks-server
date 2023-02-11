from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
import os
import aiohttp
import asyncio

load_dotenv()

STT_ENDPOINT = "https://api.assemblyai.com/v2/"
STT_HEADERS = {"authorization": os.environ["STT_KEY"]}
SESSION = aiohttp.ClientSession()

app = FastAPI()


@app.post("/open")
async def open_room():
    return {"message": "Hello World"}


@app.post("/stt")
async def convert_speech(file: UploadFile):
    async with SESSION.post(
        STT_ENDPOINT + "upload", headers=STT_HEADERS, data=read_file(file)
    ) as r:
        url = (await r.json())["upload_url"]

    async with SESSION.post(
        STT_ENDPOINT + "transcript", json={"audio_url": url}, headers=STT_HEADERS
    ) as r:
        data = await r.json()
        transcript_id = data["id"]

    c = 3
    while True:
        async with SESSION.get(
            STT_ENDPOINT + f"transcript/{transcript_id}", headers=STT_HEADERS
        ) as r:
            data = await r.json()

        if data["status"] == "error":
            return {}

        if data["status"] == "completed":
            break

        await asyncio.sleep(c)

        c += 3

    with open(transcript_id, "w") as f:
        f.write(await r.text())

    return data


async def read_file(data: UploadFile):
    while chunk := await data.read(1 << 10):
        yield chunk
