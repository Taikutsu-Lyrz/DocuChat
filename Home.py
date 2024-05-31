from PIL import Image
import streamlit as st
import time
import numpy as np



texts = " **DocuChat** is an innovative web application that allows you to upload and interact with the contents of multiple PDF documents and text files through a conversational interface. Extract, analyze, and ask questions about your documents effortlessly. Whether you're a student, researcher, or professional, DocuChat is designed to make navigating and understanding your documents easier and more efficient. Upload your PDFs and text files, process them, and start chatting to get the information you need quickly and accurately."
   


def stream_data():
        for word in texts.split(" "):
            yield word + " "
            time.sleep(0.1)
    

        


def main():
    

       
    im = Image.open("icon.png")
    st.set_page_config(page_title="Chat with your documennts",
                       page_icon=im,
                       initial_sidebar_state="collapsed"
                       )

        
    
    



    st.header("Hey! Welcome to DocuChat")
    
    st.write_stream(stream_data)


    
      

                
                
    st.write("It's easy to start just select your method ")
    st.page_link("pages/Pdf.py", label="Import Pdf 📕")
    st.page_link("pages/Text.py", label="Import Text 📄")
    
    


    
if __name__ == '__main__':
    main()