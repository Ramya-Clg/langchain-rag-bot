from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(image,input="explain"): 
    response= model.generate_content([input,image]) 
    return response.text

st.set_page_config(page_title="Gemini", page_icon="🦏")
st.header("Gemini llm app")
input = st.text_input("Write Prompt for you image(optional)",key="input")
upload_image = st.file_uploader("Upload your image",key="image",type=["jpg","png","jpeg"])
image=  ""
if upload_image:
    image = Image.open(upload_image)
    st.image(image,caption="Your image",use_container_width=True)
submit = st.button("Submit")

if submit:
    response = get_gemini_response(input,image)
    st.subheader("The response from Gemini:")
    st.write(response)