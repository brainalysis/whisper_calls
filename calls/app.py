from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import requests
import logging

from call_analyzer import main

logging.basicConfig(level=logging.INFO)

app_test = FastAPI()


# pedantic model for request body
class Args(BaseModel):
    """Request body model"""

    file_url: str
    key: str


# wrapper function to process the request in the background
# save the result to bubble app
# we need this wrapper function to pass the background task to the endpoint
# because bubble API connector times out after 60 seconds
def process_request_in_background(
    file_url: str,
    key: str,
):
    """Background task to process the request"""

    logging.info("Starting background task")

    # run the function
    main_result = main(file_url, key)

    # now post the main result to bubble app's webhook / api workflow
    res = requests.post(
        url="https://test1-87232.bubbleapps.io/version-test/api/1.1/wf/api_workflow_for_all_analysis",
        json=main_result,
        timeout=60,
    )
    logging.info("Background task completed!")
    logging.info("Response from Bubble: %s", res.json())


# Just a simple root endpoint to check if the app is running
@app_test.get("/")
async def read_root():
    """Root endpoint"""
    return {"Hello": "World"}


# The main endpoint to analyze the audio file
@app_test.post("/demystify")
async def do_the_magic(background_tasks: BackgroundTasks, args: Args):
    """Endpoint to start the background task"""

    logging.info("+++ Front Process started")

    # Add the background task for processing
    background_tasks.add_task(
        process_request_in_background,
        args.file_url,
        args.key,
    )

    # Immediately return the request_id to the client
    return {"status": "Crafting clarity from complexity, just a moment please.. "}
