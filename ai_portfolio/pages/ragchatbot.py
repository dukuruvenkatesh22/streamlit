import streamlit as st
import numpy as np
import fitz  # PyMuPDF for PDF extraction
import faiss
from sentence_transformers import SentenceTransformer
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Global variables to store documents and FAISS index
documents = []
index = None

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file)
    text = ""
    for page in document:
        text += page.get_text()
    return text

# Function to create FAISS index
def create_faiss_index(documents):
    global index
    document_embeddings = model.encode(documents)
    dimension = document_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(document_embeddings).astype('float32'))

# Document retrieval function
def retrieve_documents(query, k=3):
    if index is None:
        raise Exception("No documents indexed.")
    query_vector = model.encode([query]).astype('float32')
    distances, indices = index.search(query_vector, k)
    return [(documents[i], distances[0][j]) for j, i in enumerate(indices[0])]

# Response generation function
def get_response(user_query):
    retrieved_docs = retrieve_documents(user_query)
    context = "\n".join([f"{doc} (distance: {dist:.2f})" for doc, dist in retrieved_docs])
    augmented_input = f"{user_query}\nContext:\n{context}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": augmented_input}]
    )

    return response['choices'][0]['message']['content']

# Streamlit app layout
st.title("PDF Chatbot")

# File upload section
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    documents = pdf_text.split('\n\n')  # Split into paragraphs or adjust as needed

    # Create FAISS index with new documents
    create_faiss_index(documents)
    st.success("PDF uploaded and indexed successfully.")

# User query section
user_query = st.text_input("Ask a question about the uploaded PDF:")

if st.button("Send"):
    if user_query:
        try:
            # Get the response from OpenAI
            response = get_response(user_query)
            st.write("Chatbot Response:", response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a query.")
