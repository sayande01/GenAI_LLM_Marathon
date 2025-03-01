import streamlit as st
import os
import tempfile
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI (Gemini)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page config
st.set_page_config(
    page_title="PDF Chatbot with RAG",
    page_icon="📚",
    layout="wide"
)

# Initialize session state variables
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_pdfs" not in st.session_state:
    st.session_state.processed_pdfs = []

# Function to process PDF and create vector store
def process_pdf(uploaded_file):
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Load and split the PDF
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    document_chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and store in vector database
    embeddings = VertexAIEmbeddings()
    vectorstore = FAISS.from_documents(document_chunks, embeddings)
    
    # Clean up the temporary file
    os.unlink(tmp_path)
    
    return vectorstore

# Function to setup the conversational chain
def setup_conversation_chain(vectorstore):
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create memory for conversation
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create the conversation chain
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        memory=memory
    )
    
    return conversation

# Main app UI
st.title("📚 Smart PDF Chatbot with RAG")
st.write("Upload PDF documents and ask questions about their content.")

# Sidebar for file upload and settings
with st.sidebar:
    st.header("Document Upload")
    uploaded_files = st.file_uploader(
        "Upload PDF documents", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="You can upload multiple PDF documents."
    )
    
    if uploaded_files:
        # Process each uploaded file if not already processed
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.processed_pdfs:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Create or update vector store
                    if not hasattr(st.session_state, 'vectorstore'):
                        st.session_state.vectorstore = process_pdf(uploaded_file)
                    else:
                        new_vectorstore = process_pdf(uploaded_file)
                        # Merge with existing vectorstore
                        st.session_state.vectorstore.merge_from(new_vectorstore)
                    
                    # Add to processed PDFs list
                    st.session_state.processed_pdfs.append(uploaded_file.name)
                    
                    # Setup or reset conversation chain
                    st.session_state.conversation = setup_conversation_chain(st.session_state.vectorstore)
                    
                    st.success(f"Processed {uploaded_file.name}")
    
    st.header("Processed Documents")
    if st.session_state.processed_pdfs:
        for pdf in st.session_state.processed_pdfs:
            st.write(f"- {pdf}")
    else:
        st.write("No documents processed yet.")
        
    st.header("Settings")
    st.caption("Gemini API Key is loaded from .env file")
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []

# Main chat area
st.divider()

# Display chat history
for i, message in enumerate(st.session_state.chat_history):
    if i % 2 == 0:  # User message
        with st.chat_message("user", avatar="👤"):
            st.write(message)
    else:  # AI message
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message)

# Chat input
if query := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.chat_history.append(query)
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.write(query)
    
    # Check if we can process the query
    if st.session_state.conversation is not None:
        with st.spinner("Thinking..."):
            # Get response from conversation chain
            response = st.session_state.conversation({"question": query})
            ai_response = response["answer"]
            
            # Add AI response to chat history
            st.session_state.chat_history.append(ai_response)
            
            # Display AI response
            with st.chat_message("assistant", avatar="🤖"):
                st.write(ai_response)
    else:
        # Display error message if no documents are uploaded
        with st.chat_message("assistant", avatar="🤖"):
            error_message = "Please upload at least one PDF document before asking questions."
            st.error(error_message)
            st.session_state.chat_history.append(error_message)

# Add some information at the bottom
st.divider()
st.caption("This app uses Google's Gemini API and LangChain for Retrieval-Augmented Generation (RAG).")
