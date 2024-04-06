from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import logging
import time
import requests


logging.basicConfig(level=logging.INFO)

app_test = FastAPI()


async def main(file_url: str, key: str):
    # seleep for 10 seconds to simulate a long-running process
    print(f"=== Backend PROCESSING: {file_url} with key: {key}")
    logging.info(f"=== Back end PROCESSING: {file_url} with key: {key}")
    time.sleep(10)
    # print(f"PROCESSED: {file_url} with key: {key}")
    res = requests.post(
        url="https://test1-87232.bubbleapps.io/version-test/api/1.1/wf/test_workflow",
        json={
            "file_url": file_url,
            "key": key,
        },
    )

    logging.info(f"- ***** from bubble.i0 {res.json()}")

    print(f"^^^^ Backend Process completed")
    logging.info(f"^^^ Backend Process completed")

    return {"file_url": file_url, "key": key}


class Args(BaseModel):
    file_url: str
    key: str


@app_test.get("/")
async def read_root():
    return {"Hello": "World"}


@app_test.post("/demystify")
async def do_the_magic(background_tasks: BackgroundTasks, args: Args):
    # cb_url = "https://eojwjg4ll31ln5n.m.pipedream.net"
    print(f"+++ Front Process started")
    logging.info(f"+++ Front Process started")

    # Add the background task for processing
    background_tasks.add_task(
        main,
        args.file_url,
        args.key,
    )

    # Immediately return the request_id to the client
    return {"status": "Please wait, processing the request in the background"}
