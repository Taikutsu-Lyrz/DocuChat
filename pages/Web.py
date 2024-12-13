import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from HtmlTemplates import css, bot_template, user_template
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from PIL import Image
import requests
from bs4 import BeautifulSoup
openai = ChatOpenAI(model_name="gpt-3.5-turbo")

# Used Chatgpt btw

# Chunk Function
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,  # Reduce chunk size to ensure token limit is respected
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Vector Function
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a conversation chain from a vector store
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Function to handle user input and generate responses
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    
    # Update chat history
    st.session_state.chat_history.append({'type': 'bot', 'content': response['answer']})
    st.session_state.chat_history.append({'type': 'user', 'content': user_question})
   
    # Reverse display order to show the latest messages at the top
    for message in reversed(st.session_state.chat_history):
        if message['type'] == 'user':
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)

# Main function
def main():
    load_dotenv()
    im = Image.open("icon.png")
    st.set_page_config(page_title="Chat with your very own Texts", page_icon=im)
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Initialize chat_history as an empty list

    with st.sidebar:
        st.subheader("Your Text")

        # Get user input for URL
        user_source = st.text_input("Enter the URL of your text:")
        
        if not user_source:
            st.error("Please provide a link")
            
        else:    
            
            if st.button("Process"):
                if not user_source:
                    st.error("Please provide a valid URL.")
                else:
                    try:
                        with st.spinner("Processing..."):
                            # Fetch and parse the webpage
                            page = requests.get(user_source)
                            page.raise_for_status()  # Check for HTTP errors

                            soup = BeautifulSoup(page.content, "html.parser")
                            text_content = soup.get_text(strip=True)

                            # Limit or chunk text
                            if len(text_content) > 16000:
                                text_content = text_content[:16000]  # Limit to first 16,000 characters
                            
                            # Split into chunks
                            text_chunks = get_text_chunks(text_content)

                            # Create vector store
                            vectorstore = get_vectorstore(text_chunks)

                            # Create conversation chain
                            st.session_state.conversation = get_conversation_chain(vectorstore)

                            st.success("Processing complete!")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error fetching the URL: {e}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")

    st.header("Chat with your Text")            
    if st.session_state.conversation:
        user_question = st.text_input("Ask a question about your text:")
        if user_question:
            handle_userinput(user_question)
    else:
        st.info("Please provide a URL, click 'Process', and wait for it to complete.")

if __name__ == '__main__':
    main()