from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(question):
    response= model.generate_content(question)
    return response.text

st.set_page_config(page_title="Gemini", page_icon="🦏")
st.header("Gemini llm app")
input = st.text_input("Ask a question to Gemini",key="input")
submit = st.button("Submit")
if submit:
    response = get_gemini_response(input)
    st.subheader("The response from Gemini:")
    st.write(response)