# Imports
from dotenv import load_dotenv
import streamlit as st
import os
from docx import Document
import google.generativeai as genai
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Streamlit App
st.set_page_config(page_title="Gemini File Demo")
st.header("Gemini Application")

# User Input
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose a file...", type=["pdf", "docx"])

document_content = ""

# Process Uploaded File
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Handle PDF content extraction
        pdf_reader = PdfReader(uploaded_file)
        document_content = " ".join([pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Handle DOCX content extraction
        doc = Document(uploaded_file)
        document_content = " ".join([paragraph.text for paragraph in doc.paragraphs])

    # Display File Contents
    st.write("Document Contents:")
    st.write(document_content)

# Generate Response Button
submit = st.button("Generate Summary")

# Handle Response Generation and Display Summary
if submit:
    if document_content:
        try:
            response = get_gemini_response(document_content)
            st.subheader("The Summary is")
            st.write(response)
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")
    else:
        st.warning("Please upload a document before generating the summary.")
