import os
import tempfile

import pandas as pd
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from PyPDF2 import PdfReader

load_dotenv(find_dotenv())
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

llm = ChatOpenAI(model_name='gpt-4', temperature=0.5, max_tokens=1024)
embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)
doc_db = Pinecone.from_documents([], embeddings, index_name='kameltrainvectors')

def train_selected_pdf(file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.getbuffer())
        tmp_file_path = tmp_file.name

    loader = PyPDFLoader(tmp_file_path)
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20
    )
    doc_file = loader.load()
    doc_file_split = text_splitter.split_documents(doc_file)
    updated_index = Pinecone.from_documents(doc_file_split, embeddings, index_name='kameltrainvectors', namespace='synthese')
    return updated_index



def train_selected_txt(file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(file.getbuffer())
        tmp_file_path = tmp_file.name

    loader = TextLoader(tmp_file_path)
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20
    )
    doc_file = loader.load()
    doc_file_split = text_splitter.split_documents(doc_file)
    updated_index = Pinecone.from_documents(doc_file_split, embeddings, index_name='kameltrainvectors',namespace='synthese_txt')
    return updated_index

def train_selected_csv(file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(file.getbuffer())
        tmp_file_path = tmp_file.name
    loader = CSVLoader(file_path=tmp_file_path)
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20
    )
    doc_file = loader.load()
    doc_file_split = text_splitter.split_documents(doc_file)
    updated_index = Pinecone.from_documents(doc_file_split, embeddings, index_name='kameltrainvectors', namespace='synthese_sheet')
    return updated_index

def train_selected_excel(file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        tmp_file.write(file.getbuffer())
        tmp_file_path = tmp_file.name

    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20
    )
    loader = UnstructuredExcelLoader(tmp_file_path)
    doc_file = loader.load()
    doc_file_split = text_splitter.split_documents(doc_file)
    updated_index = Pinecone.from_documents(doc_file_split, embeddings, index_name='kameltrainvectors', namespace='synthese_xlsx')
    return updated_index

def retrieval_answer(query):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=doc_db.as_retriever(),
    )
    query = query
    result = qa.run(query)
    return result

def chatbot_response(input_text):
    # Simple echo response for demonstration purposes
    return "BABot: " + input_text

# Define the Streamlit app
def main():
    st.title("Bienvenu chez BABot")

    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'uploaded_file_content' not in st.session_state:
        st.session_state.uploaded_file_content = ""

    # Load existing conversation history from file if available
    conversation_file_path = "conversation_history_pdf.txt"
    try:
        with open(conversation_file_path, "r") as file:
            st.session_state.conversation_history = file.readlines()
    except FileNotFoundError:
        pass

    # Display conversation history
    for item in st.session_state.conversation_history:
        if "user" in item:
            item_display = item.replace("user: ", "")
            st.info(item_display)
        elif "BABot" in item:
            item_answer_display = item.replace("BABot:", "")
            st.success(item_answer_display)

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF, TXT, CSV, or Excel file", type=["pdf", "txt", "csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            train_selected_pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            train_selected_txt(uploaded_file)
        elif uploaded_file.type == "text/csv":
            train_selected_csv(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            train_selected_excel(uploaded_file)
            # print(uploaded_file.name)
            # print('/n hihi')
        st.success("File uploaded and processed successfully.")

    # User input box
    user_input = st.chat_input("Posez votre question")

    # Check if user input is not empty and Enter key is pressed
    if user_input:
        # Get chatbot response
        bot_response = chatbot_response(retrieval_answer(user_input))

        # Add user's message to the conversation history
        st.session_state.conversation_history.append("user: " + user_input)

        # Add chatbot's response to the conversation history
        st.session_state.conversation_history.append(bot_response)

        # Display the latest user input and chatbot response above the input field
        st.info(user_input)
        st.success(bot_response)

        # Update conversation history file
        with open(conversation_file_path, "a") as file:
            file.write("user: " + user_input + "\n")
            file.write("BABot: " + bot_response + "\n")

# Run the Streamlit app
if __name__ == "__main__":
    main()
