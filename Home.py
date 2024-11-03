from PIL import Image
import streamlit as st
import time
import numpy as np



texts = " **DocuChat** is an innovative web application that lets you interact with the contents of PDFs, text files, and even YouTube videos through a conversational interface. With its new AI image generation feature, students and teachers can create custom images to enhance their projects and presentations. Extract, analyze, and ask questions about your documents with ease, while generating visual aids to enrich your work. Whether you're a student, researcher, or professional, DocuChat is here to make navigating, understanding, and visualizing your documents faster and more efficient. Just upload your PDFs, text files, or videos, process them, and start chatting to quickly access the information and images you need."
   


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
    st.page_link("pages/Youtube.py", label="Import Youtube ▶️")
    st.page_link("pages/Image.py", label="Generate Photo 📷")
    
    

    

    
if __name__ == '__main__':
    main()