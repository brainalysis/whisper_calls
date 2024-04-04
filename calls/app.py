from fastapi import FastAPI, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from uuid import uuid4
import httpx
import logging

from call_analyzer import main

logging.basicConfig(level=logging.INFO)

app_test = FastAPI()


class Args(BaseModel):
    file_url: str
    key: str


async def process_request_in_background(
    request_id: str, callback_url: str, file_url: str, key: str
):
    logging.info(f"Starting background task for request_id: {request_id}")
    try:
        # Execute the long-running process in the thread pool
        main_result = await run_in_threadpool(main, file_url, key)

        payload = {
            "request_id": request_id,
            "status": "Completed",
            "data": main_result,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(callback_url, json=payload)
            logging.info(
                f"Notification sent for request_id: {request_id}, response status: {response.status_code}"
            )
    except Exception as e:
        logging.error(f"Error processing request {request_id}: {str(e)}")


@app_test.get("/")
async def read_root():
    return {"Hello": "World"}


@app_test.post("/demystify")
async def do_the_magic(background_tasks: BackgroundTasks, args: Args):
    request_id = str(uuid4())
    cb_url = "https://eojwjg4ll31ln5n.m.pipedream.net"
    logging.info(f"Process started for request_id: {request_id}")

    # Add the background task for processing
    background_tasks.add_task(
        process_request_in_background,
        request_id,
        cb_url,
        args.file_url,
        args.key,
    )

    # Immediately return the request_id to the client
    return {"status": "Processing", "request_id": request_id}
