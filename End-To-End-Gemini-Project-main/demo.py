# Imports
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(prompt, document_content):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, document_content])
    return response.text

# Streamlit App
st.set_page_config(page_title="Gemini File Demo")
st.header("Gemini Application")

# User Input
input_prompt = st.text_input("Input Your Prompt for Gemini-pro: ", key="input")
uploaded_file = st.file_uploader("Choose a file...", type=["pdf", "docx", "txt"])

document_content = ""

# Process Uploaded File
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Handle PDF content extraction
        pdf_reader = PdfReader(uploaded_file)
        document_content = " ".join([page.extract_text() for page in pdf_reader.pages])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Handle DOCX content extraction
        doc = Document(uploaded_file)
        document_content = " ".join([paragraph.text for paragraph in doc.paragraphs])
    elif uploaded_file.type == "text/plain":
        # Handle plain text file
        document_content = uploaded_file.read().decode("utf-8")

    # Display File Contents
    st.write("Document Contents:")
    st.write(document_content)

# Generate Response Button
submit = st.button("Generate Result with Gemini-pro")

# Handle Response Generation and Display Result
if submit:
    if document_content:
        try:
            response = get_gemini_response(input_prompt, document_content)
            st.subheader("The Result from Gemini-pro is")
            st.write(response)
        except Exception as e:
            st.error(f"Error generating result with Gemini-pro: {str(e)}")
    else:
        st.warning("Please upload a document before generating the result with Gemini-pro.")
