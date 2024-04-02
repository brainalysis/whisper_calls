from fastapi import FastAPI
import requests
import io
from pydantic import BaseModel

from call_analyzer import main

app_test = FastAPI()


class Args(BaseModel):
    file_url: str
    key: str


# for admin purposes
@app_test.get("/")
async def read_root():
    return {"Hello": "World"}


# post request to demystify the calls
@app_test.post("/demystify")
async def do_the_magic(file_url: Args):
    res = main(file_url.file_url, file_url.key)
    return {"response": res}
