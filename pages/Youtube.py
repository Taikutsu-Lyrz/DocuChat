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
from youtube_transcript_api import YouTubeTranscriptApi
openai = ChatOpenAI(model_name = "gpt-3.5-turbo")


# Function to get YouTube transcript
def get_youtube_transcript(video_url):
    video_id = video_url.replace('https://www.youtube.com/watch?v=', '')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    output = ''.join([x['text'] + '\n' for x in transcript])
    return output

# Function to chunk text
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=70,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector store
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a conversation chain from a vector store
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
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
   
    st.session_state.chat_history.append({'type': 'bot', 'content': response['answer']})
    st.session_state.chat_history.append({'type': 'user', 'content': user_question})
    

    for message in reversed(st.session_state.chat_history):
        if message['type'] == 'user':
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)

def main():
    load_dotenv()
    im = Image.open("icon.png")
    st.set_page_config(page_title="Chat with Youtube Videos", page_icon=im)
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        st.subheader("Your Link")
        video_url = st.text_input("Enter YouTube Video URL")

        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_youtube_transcript(video_url)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success("Processing complete!")

    st.header("Chat with a YouTube Video")
    if not video_url:
        st.error("Please provide a YouTube Video URL and click on 'Process'.")
    elif st.session_state.conversation:
        user_question = st.text_input("Ask a question about your YouTube Video:")
        if user_question:
            handle_userinput(user_question)

if __name__ == '__main__':
    main()
