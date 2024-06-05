import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader  
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from HtmlTemplates import css, bot_template, user_template
from langchain.chat_models import ChatOpenAI
openai = ChatOpenAI(model_name = "gpt-3.5-turbo")
from langchain.embeddings import OpenAIEmbeddings
from PIL import Image


# Chunk Function
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter (
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks


# Vector Function
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
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


def main():
    load_dotenv()
    im = Image.open("icon.png")
    st.set_page_config(page_title="Chat with your very own Texts",
                       page_icon=im)
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Initialize chat_history as an empty list

    

    with st.sidebar:
        st.subheader("Your Text")
        

        user_source =  st.text_area("Provide text here")
        
        if st.button("Process"):
            with st.spinner("Processing"):
                
                
                raw_text = user_source

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

                st.success("Processing complete!")
    st.header("Chat with your Text")            
    if not user_source:
        st.error("Please provide your Text and click 'Process'.")
    elif st.session_state.conversation:
        user_question = st.text_input("Ask a question about your text:")
        if user_question:
            handle_userinput(user_question)
              

if __name__ == '__main__':
    main()
