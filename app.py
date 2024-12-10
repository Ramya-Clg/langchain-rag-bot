import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
load_dotenv()
from langchain_community.vectorstores import FAISS 

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

if "vector" not in st.session_state:
    st.session_state.embeddings = embeddings
    st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs = st.session_state.loader.load()
    st.session_state.chunk_documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(st.session_state.docs[:10])
    st.session_state.vector = FAISS.from_documents(st.session_state.chunk_documents, embedding=st.session_state.embeddings)
    
st.title("Groq Langchain")
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate answer.
    If the answer is not in the context, say "I don't know."
    <context>
    {context}
    <context>
    Question: {input}
    """
)

document_chain = create_stuff_documents_chain(llm, prompt=prompt)
retriever = st.session_state.vectors.as_retriever()
retrival_chain = create_retrieval_chain(retriever, document_chain)

prompt = st.text_input("Ask me anything about: ")

if prompt:
    response = retrival_chain.invoke({"input": prompt})
    st.write(response['answer'])
    
    with st.expander("More"):
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("____________________________________________________________")