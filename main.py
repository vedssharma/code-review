from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

client = OpenAI()

class CodeInput(BaseModel):
    code: str

def provide_feedback(code_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": "You are an AI code reviewer specializing in analyzing code for best practices, readability, performance, and security. You provide structured feedback based on industry standards and best practices."
            },
            {
                "role": "user", 
                "content": f"Provide me feedback on the following code: {code_input}"
            }
        ]
    )

    return response.choices[0].message


@app.get("/")
def index():
    return "Hello World"


@app.post("/code")
def review_code(code_input: CodeInput):
    feedback = provide_feedback(code_input.code)
    return {"feedback": feedback}