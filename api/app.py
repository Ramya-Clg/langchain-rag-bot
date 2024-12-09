from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    task="text-generation"
)

model_gemini = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    temperature=0.5
)

model_qwen = ChatHuggingFace(llm=llm)

app = FastAPI(
    title="Langchain server",
    version="1.0",
    description="Langchain API server",
)


prompt_essay = ChatPromptTemplate.from_template("Write me an essay about {topic} in 100 words")
prompt_poem = ChatPromptTemplate.from_template("Write me an poem about {topic} in 100 words")

add_routes(app, model_gemini, path="/gemini")
add_routes(app, prompt_essay|model_gemini, path="/gemini/essay")
add_routes(app, prompt_poem|model_qwen, path="/qwen/poem")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)