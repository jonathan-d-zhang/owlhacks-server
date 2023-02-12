from fastapi import FastAPI, UploadFile, Response
from dotenv import load_dotenv
import re
import aiohttp
import asyncio
import aiohttp
import aioredis
import random
import os
from pathlib import Path
import time

load_dotenv()

PARENT = Path(__file__).parent
TRANSCRIPTS = PARENT / "transcripts"
TRANSCRIPTS.mkdir(exist_ok=True)

STT_ENDPOINT = "https://api.assemblyai.com/v2/"
STT_HEADERS = {"authorization": os.environ["STT_KEY"]}
HTTP_SESSION = aiohttp.ClientSession()
REDIS_SESSION = aioredis.from_url("redis://redis")

app = FastAPI()


@app.post("/open", status_code=201)
async def open_room():
    while await REDIS_SESSION.sismember(
        "keys", key := random.randrange(10**6, 10**7)
    ):
        pass
    await REDIS_SESSION.sadd("keys", key)

    return key


PAT = re.compile(r"(\d+)")


@app.post("/stt/{key}")
async def convert_speech(key: int, file: UploadFile, response: Response):
    file.filename = file.filename or "1000000000000000000"
    order = int(PAT.findall(file.filename)[0])

    if not await REDIS_SESSION.sismember("keys", key):
        response.status_code = 403
        return {"message": "Invalid key"}

    async with HTTP_SESSION.post(
        STT_ENDPOINT + "upload", headers=STT_HEADERS, data=await file.read()
    ) as r:
        url = (await r.json())["upload_url"]

    async with HTTP_SESSION.post(
        STT_ENDPOINT + "transcript", json={"audio_url": url}, headers=STT_HEADERS
    ) as r:
        data = await r.json()
        transcript_id = data["id"]

    start = time.perf_counter()
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

    tdir = TRANSCRIPTS / str(key)
    tdir.mkdir(exist_ok=True)
    with open(tdir / transcript_id, "w") as f:
        f.write(str(data))

    for w in data["words"]:
        await REDIS_SESSION.xadd(str(key), {"order": order, "word": w["text"]})

    response.status_code = 201
    end = time.perf_counter()
    print(f"elapsed {end - start}")


@app.get("/text/{key}")
async def get_text(key: int, response: Response, start: str = "-"):
    if not await REDIS_SESSION.sismember("keys", key):
        response.status_code = 403
        return

    data = await REDIS_SESSION.xrange(str(key), min=start)
    print(data)

    out = []
    for start, d in data:
        out.append(dict(start=start, word=d[b"word"]))

    return out


async def read_file(data: UploadFile):
    while chunk := await data.read(1 << 15):
        yield chunk

