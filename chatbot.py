from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = model.generate_content(question,stream=True)
    return response

st.set_page_config(page_title="Chatbot", page_icon="🦏")
st.header("Gemini llm app")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
input = st.text_input("Ask a question to Gemini",key="input")
submit = st.button("Submit")
if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The response from Gemini:")
    for chunk in response:
        st.markdown(chunk.text + "",unsafe_allow_html=True)
    st.session_state['chat_history'].append(("Gemini",response.text))
st.subheader("Chat History")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}") 