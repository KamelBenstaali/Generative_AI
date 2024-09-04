import os
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

llm = ChatOpenAI(model_name='gpt-4o', temperature=0.5, max_tokens=1024)
embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)
doc_db = Pinecone.from_documents('', embeddings, index_name = 'kameltrain' , namespace='excel')


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

    # Load existing conversation history from file if available
    conversation_file_path = "conversation_history_excel.txt"
    try:
        with open(conversation_file_path, "r") as file:
            st.session_state.conversation_history = file.readlines()
    except FileNotFoundError:
        pass

    # Display conversation history
    for item in st.session_state.conversation_history:
        if "user" in item:
            item_display = item.replace("user: ","")
            st.info(item_display)
        elif "BABot" in item:
            item_answer_display = item.replace("BABot:", "")
            st.success(item_answer_display)

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








