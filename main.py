from fastapi import FastAPI, UploadFile, Response
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import aiohttp
import aioredis
import random

load_dotenv()

STT_ENDPOINT = "https://api.assemblyai.com/v2/"
STT_HEADERS = {"authorization": os.environ["STT_KEY"]}
HTTP_SESSION = aiohttp.ClientSession()
REDIS_SESSION = aioredis.from_url("redis://redis")

app = FastAPI()


@app.post("/open", status_code=201)
async def open_room():
    #while await REDIS_SESSION.sismember("keys", key := random.randrange(10**6, 10**7)):
    #    pass
    key = 10
    await REDIS_SESSION.sadd("keys", key)

    return key


@app.post("/stt/{key}")
async def convert_speech(key: int, file: UploadFile):
    async with HTTP_SESSION.post(
        STT_ENDPOINT + "upload", headers=STT_HEADERS, data=read_file(file)
    ) as r:
        url = (await r.json())["upload_url"]

    async with HTTP_SESSION.post(
        STT_ENDPOINT + "transcript", json={"audio_url": url}, headers=STT_HEADERS
    ) as r:
        data = await r.json()
        transcript_id = data["id"]

    c = 3
    while True:
        async with HTTP_SESSION.get(
            STT_ENDPOINT + f"transcript/{transcript_id}", headers=STT_HEADERS
        ) as r:
            data = await r.json()

        if data["status"] == "error":
            return {}
        if data["status"] == "completed":
            break

        await asyncio.sleep(c)
        c += 3

    await REDIS_SESSION.xadd(str(key), {"data": str(data)})

@app.get("/text/{key}")
async def get_text(key: int, response: Response):
    if not await REDIS_SESSION.sismember("keys", key):
        response.status_code = 403
        return

    data = await REDIS_SESSION.xrange(str(key))

    return data

async def read_file(data: UploadFile):
    while chunk := await data.read(1 << 10):
        yield chunk
