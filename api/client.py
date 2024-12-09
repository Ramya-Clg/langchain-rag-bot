import requests
import streamlit as st

def get_gemini_response(prompt):
    response = requests.post("http://localhost:8000/gemini/essay/invoke", json={'input': {'topic':prompt}})

    return response.json()['output']['content']

def get_qwen_response(prompt):
    response = requests.post("http://localhost:8000/qwen/poem/invoke", json={'input': {'topic':prompt}})

    return response.json()['output']['content']


st.title("Langchain API Client")
input_text1 = st.text_input("Essay Topic: ")
input_text2 = st.text_input("Poem Topic: ")

if input_text1:
    st.write(get_gemini_response(input_text1))

if input_text2:
    st.write(get_qwen_response(input_text2))