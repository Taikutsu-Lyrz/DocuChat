import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Function to generate an image
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,  # number of images to generate
        size="512x512",  # image size
        quality = "standard"
        
    )
    image_url = response['data'][0]['url']
    return image_url

def main():

    st.header("DALL·E Image Generator")

# Input for the prompt
    prompt = st.text_input("Enter a prompt for the image:")
    


    
    if prompt:
        if st.button("Generate Image"):
            with st.spinner("Generating image..."):
            
                image_url = generate_image(prompt)
                st.image(image_url, caption=prompt, use_column_width=True)
    else:
        st.error("Please enter a prompt!")
        
# Run the Streamlit app
if __name__ == '__main__':
    main()