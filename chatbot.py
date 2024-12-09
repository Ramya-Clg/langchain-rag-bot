from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant.Please respond to the queries"),
    ("user", "Question: {question}"),
])

st.title("Chatbot")
input_text = st.text_input("Enter your question")
llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    temperature=0.5
)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))