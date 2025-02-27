import os, getpass
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import time

# Set page configuration
st.set_page_config(
    page_title="Smart Document Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .css-18e3th9 {
        padding-top: 0;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .result-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
        border-left: 5px solid #4b6cb7;
    }
    .title-container {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .search-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
        padding: 10px 15px;
    }
    .loader {
        border: 5px solid #f3f3f3;
        border-top: 5px solid #4b6cb7;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Set environment variables
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# Initialize environment
if 'initialized' not in st.session_state:
    _set_env("GOOGLE_API_KEY")
    st.session_state.initialized = True

# Define sample documents
documents = [
    "LangChain is a framework for building AI applications using large language models (LLMs). It offers modular tools for prompt management, chaining, and agent-based workflows, streamlining the integration of complex AI tasks.",
    "Retrieval-Augmented Generation (RAG) enhances generative models by combining them with document retrieval methods. This hybrid approach leverages external knowledge bases to provide more contextually accurate and informed responses.",
    "FAISS, developed by Facebook, is a library designed for efficient similarity search in dense vector spaces. It plays a crucial role in rapidly retrieving relevant documents from large corpora in RAG systems.",
    "Streamlit is a Python library that enables developers to build interactive, data-driven web applications with minimal code. It is ideal for quickly prototyping and deploying machine learning and AI-powered dashboards.",
    "Generative AI (GenAI) involves algorithms that can create new content—such as text, images, or music—by learning from vast datasets. It is transforming creative fields and automating content generation.",
    "Large Language Models (LLMs) are neural networks trained on extensive text datasets, capable of understanding, generating, and summarizing human language with impressive accuracy.",
    "Agentic AI refers to systems that operate autonomously by making decisions based on predefined objectives and learned behaviors, pushing the boundaries of automated problem solving.",
    "Prompt Engineering is the process of designing effective input prompts to guide language models. By refining prompts, developers can control the output quality and relevance of generated content.",
    "Chain-of-Thought prompting encourages language models to reason through tasks step-by-step, resulting in more coherent and logically structured outputs, which is vital for complex problem-solving.",
    "Reinforcement Learning from Human Feedback (RLHF) is a training paradigm where models learn from human evaluations, aligning AI behavior with human values and expectations.",
    "Few-shot and Zero-shot Learning enable models to perform tasks with little to no task-specific data, demonstrating the flexibility of modern LLMs in adapting to new challenges.",
    "Fine-tuning pre-trained models on domain-specific data can significantly improve performance on specialized tasks, bridging the gap between general-purpose and targeted applications.",
    "Neural Search leverages deep learning to understand semantic relationships in text, enhancing traditional keyword-based search methods for improved relevance in document retrieval.",
    "AI Safety and Alignment research focuses on ensuring that AI systems are both reliable and ethical, addressing potential risks and aligning AI decisions with human intentions.",
    "Transformers, the architecture underpinning most state-of-the-art LLMs, utilize self-attention mechanisms to process sequences in parallel, facilitating efficient and scalable model training.",
    "Memory-augmented Neural Networks incorporate external memory components to maintain context over longer sequences, thereby improving the consistency and coherence of generated outputs.",
    "Multimodal AI systems integrate text, images, and other data types to produce richer, more context-aware responses, broadening the scope of traditional language models.",
    "Ethical AI development emphasizes transparency, fairness, and accountability, ensuring that AI systems are developed and deployed in ways that benefit society while mitigating bias.",
    "Scalable AI infrastructure involves the use of distributed computing and optimized algorithms, which is essential for processing large-scale data and supporting enterprise-level AI applications.",
    "Explainable AI (XAI) techniques aim to make the decision-making processes of complex models more transparent, helping stakeholders understand and trust AI-driven insights."
]

# Initialize the RAG components
@st.cache_resource
def initialize_rag():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    faiss_store = FAISS.from_texts(documents, embeddings)
    retriever = faiss_store.as_retriever()
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.3,
        max_tokens=800
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff",
        retriever=retriever,
    )
    return qa_chain

# Function to get answer
def get_answer(query, qa_chain):
    response = qa_chain.run(query)
    return response

# Sidebar with app information - Using native Streamlit components instead of HTML
with st.sidebar:
    st.title("🤖 About This App")
    
    # Using a container to style the about section
    with st.container():
        st.write("This intelligent assistant uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on a knowledge base of AI concepts.")
        
        st.subheader("Key Features:")
        
        # Use native Streamlit components to avoid HTML rendering issues
        features = [
            "Semantic search using Google's embedding models",
            "Powered by Gemini 1.5 Pro",
            "Contextual responses based on document retrieval"
        ]
        
        for feature in features:
            st.write(f"• {feature}")
        
        st.write("*Built with LangChain, Streamlit, and Google Generative AI*")
    
    st.subheader("Sample Questions")
    
    # Sample questions
    sample_questions = [
        "What is LangChain and how does it help in building AI applications?",
        "How does RAG enhance generative models?",
        "Explain the concept of Reinforcement Learning from Human Feedback",
        "What are the key ethical considerations in AI development?",
        "How can Chain-of-Thought prompting improve AI responses?"
    ]
    
    # Create buttons for sample questions
    for question in sample_questions:
        if st.button(f"📝 {question}", key=question):
            st.session_state.query = question

# Main content
st.markdown("<div class='title-container'><h1>Smart Document Assistant</h1><p>Powered by RAG & Gemini 1.5 Pro</p></div>", unsafe_allow_html=True)

# Search container
st.markdown("<div class='search-container'>", unsafe_allow_html=True)
query = st.text_input("What would you like to know about AI technologies?", value=st.session_state.get('query', ''))

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    search_button = st.button("🔍 Search", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Initialize the RAG system
qa_chain = initialize_rag()

# Process query
if search_button or (query and st.session_state.get('query') != query):
    st.session_state.query = query
    if query:
        with st.spinner("Searching knowledge base..."):
            # Add a slight delay and animation for better UX
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            answer = get_answer(query, qa_chain)
            
            # Display the result in a card
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("### 💡 Answer")
            st.markdown(answer)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Show a success message
            st.success("Response generated successfully!")
            
            # Offer follow-up suggestions
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔄 Follow-up Questions")
            
            # Dynamically generate follow-up questions based on the query
            follow_ups = [
                f"Can you explain more about how {query.split()[0:3]} relates to LLMs?",
                f"What are practical applications of {query.split()[0:2]}?",
                f"What are the limitations of {query.split()[0:3]}?"
            ]
            
            cols = st.columns(3)
            for i, follow_up in enumerate(follow_ups):
                with cols[i]:
                    if st.button(follow_up, key=f"follow_{i}"):
                        st.session_state.query = follow_up
                        st.experimental_rerun()
