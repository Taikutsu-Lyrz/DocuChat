# DocuChat

DocuChat is an innovative web application that lets you interact with the contents of PDFs, text files, and even YouTube videos through a conversational interface. With its new AI image generation feature, students and teachers can create custom images to enhance their projects and presentations. Extract, analyze, and ask questions about your documents with ease while generating visual aids to enrich your work.

## Features

- **Conversational Document Interaction**: Upload PDFs, text files, or import YouTube videos and chat with their contents.
- **AI-Powered Image Generation**: Create custom images to support projects and presentations.
- **Quick Access to Information**: Extract, analyze, and retrieve important details instantly.
- **Multiple Input Methods**:
  - 📕 Import PDF
  - 📄 Import Text File
  - 🌐 Import Website Link
  - ▶️ Import YouTube Video
  - 📷 Generate Photo

## How to Use

1. **Upload a Document**: Choose from PDF, text files, or enter a YouTube link.
2. **Process the Content**: DocuChat will analyze the document for easy interaction.
3. **Start Chatting**: Ask questions and get instant responses based on your document.
4. **Generate AI Images**: Create custom visuals to enhance your work.

## Who is it for?

- **Students**: Quickly summarize and extract key points from study materials.
- **Researchers**: Analyze large documents efficiently.
- **Professionals**: Interact with reports and presentations in an intuitive way.

Here’s the rewritten **Installation & Setup** guide for **DocuChat** using Python and **Streamlit** (instead of npm):

---

### Installation & Setup for DocuChat (Python + Streamlit)

To run **DocuChat** locally, follow these steps:

1. **Clone the repository:**
   Open your terminal and clone the project repository using Git:

   ```bash
   git clone https://github.com/Taikutsu-Lyrz/DocuChat.git
   ```

2. **Navigate into the project directory:**
   Change into the project directory:

   ```bash
   cd DocuChat
   ```

3. **Set up a virtual environment (recommended):**
   It’s a good practice to use a virtual environment for Python projects to manage dependencies. Run the following command to create one:

   - For **Windows**:
     ```bash
     python -m venv venv
     ```

   - For **macOS/Linux**:
     ```bash
     python3 -m venv venv
     ```

   Activate the virtual environment:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   Once your virtual environment is activated, install the required Python dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

   This will install the following packages:
   - `langchain==0.0.316`
   - `PyPDF2==3.0.1`
   - `python-dotenv==1.0.1`
   - `streamlit==1.34.0`
   - `openai==0.28.0`
   - `faiss-cpu==1.8.0`
   - `altair==5.3.0`
   - `tiktoken==0.7.0`
   - `youtube_transcript_api==0.6.2`
   - `pillow==10.3.0`
   - `beautifulsoup4==4.12.3`

5. **Run the app:**
   To start the **DocuChat** app using **Streamlit**, run:

   ```bash
   streamlit run app.py  # or whatever the main entry point is
   ```

   This will start the app, and you should be able to access it in your browser at `http://localhost:8501`.

---

### Additional Notes:
- **Make sure you have Python installed** on your system. You can download the latest version from [Python's official website](https://www.python.org/downloads/).
- **Set up environment variables:** If needed, create a `.env` file to store your sensitive keys (like OpenAI API keys) in the project directory.
- **Streamlit documentation:** For further customization and usage of Streamlit, you can check the [Streamlit documentation](https://docs.streamlit.io/).

With these steps, you’ll be able to run **DocuChat** locally using Python and **Streamlit**.
## Live Demo

Try DocuChat online:
👉 [DocuChat Web App](https://docuchatt.streamlit.app/)

## Contributing

We welcome contributions! Feel free to fork the repo and submit a pull request.

## License

This project is licensed under the MIT License.

---

### 🚀 Start using DocuChat today and revolutionize the way you interact with documents!

