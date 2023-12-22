from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bardapi import Bard
import requests
from dotenv import load_dotenv
import os
import re
import json
import aiohttp
import urllib.parse
from typing import List, Optional
from Bard import Chatbot
from dotenv import load_dotenv

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    user_input: str

class ResponseModel(BaseModel):
    content: str
    images: list = None
    links: list = None

@app.post("/api/ask", response_model=ResponseModel)
def get_response(user_input: UserInput):
    try:

        # Load .env file for each request and overwrite existing variables
        load_dotenv(override=True)

        # Get BARD_API_KEY from the .env file
        BARD_API_KEY = os.environ.get('BARD_API_KEY')

        # Set up the session for each request
        session = requests.Session()
        session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
        session.cookies.set("__Secure-1PSID", BARD_API_KEY)

        bard = Bard(token=BARD_API_KEY, session=session, timeout=30)

        # Print the user input to the console
        print(f"Received user input: {user_input.user_input}")    
        response = process_input(user_input.user_input, bard)
        return response
    except Exception as e:
        # Log the error details for debugging
        print(f"Error: {e}")
        # You might want to return a more generic error message in a production environment
        raise HTTPException(status_code=400, detail=f"Error processing request: {e}")

def process_input(user_input, bard):
    response = bard.get_answer(user_input)
    result = {'content': response['content']}

    if 'images' in response:
        result['images'] = response['images']

    if 'links' in response:
        result['links'] = response['links']

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
