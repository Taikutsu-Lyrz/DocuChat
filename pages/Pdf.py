import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader  
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from HtmlTemplates import css, bot_template, user_template
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from PIL import Image


# Initialize OpenAI Chat model
openai = ChatOpenAI(model_name="gpt-3.5-turbo")

# Function to extract text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector store from text chunks
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
    
    st.set_page_config(page_title="Chat with multiple PDFs",page_icon=im)
    
    st.write(css, unsafe_allow_html=True)


    # Session ststate (to keep conversation from reloading)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        

   

    

    # Sidebar at left
    with st.sidebar:
        
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        
        #To check file
        if pdf_docs:
            if st.button("Process"):
                with st.spinner("Processing"):
                    # Get PDF text
                    raw_text = get_pdf_text(pdf_docs)

                    # Get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # Create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # Create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)

                    st.success("Processing complete!")
                    
                    
    
    
                    
    if not pdf_docs:
        st.error("Please provide PDF documents first.")
    elif st.session_state.conversation:
        user_question = st.text_input("Ask a question about your Pdfs:")
        if user_question:
            handle_userinput(user_question)
    else:
        st.error("Please process your Pdf.")
       
  


    

if __name__ == '__main__':
    main()
