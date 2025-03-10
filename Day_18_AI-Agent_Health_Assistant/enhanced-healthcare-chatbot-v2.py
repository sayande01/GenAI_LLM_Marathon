import os
import getpass
import streamlit as st
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import time

# Page configuration
st.set_page_config(
    page_title="HealthCare Assistant",
    page_icon="🏥",
    layout="wide",
)

# Custom CSS for visually stunning UI
st.markdown("""
<style>
    /* Main Container Styling */
    .main {
        background: linear-gradient(135deg, #f5f7ff 0%, #eef1ff 100%);
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header & Title Styling */
    h1, h2, h3 {
        background: linear-gradient(90deg, #4361ee, #3a0ca3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        text-align: center;
    }
    
    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: white;
        border-radius: 25px;
        padding: 16px 20px;
        font-size: 16px;
        border: 1px solid #e0e0e0;
        color: #333333;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4361ee;
        box-shadow: 0 4px 20px rgba(67, 97, 238, 0.2);
        transform: translateY(-2px);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #4361ee, #3a0ca3);
        color: white !important;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #3a0ca3, #4361ee);
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(67, 97, 238, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Chat Message Styling */
    .chat-message {
        padding: 18px;
        border-radius: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: flex-start;
        color: #333333;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.5s ease-out forwards;
        max-width: 90%;
        position: relative;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #dcf8c6 0%, #c5f4b0 100%);
        margin-left: 40px;
        margin-right: 10px;
        border-top-right-radius: 5px;
    }
    
    .user-message::before {
        content: "";
        position: absolute;
        top: 0;
        right: -10px;
        width: 20px;
        height: 20px;
        background: linear-gradient(135deg, #c5f4b0 0%, #c5f4b0 50%, transparent 50%, transparent 100%);
        border-radius: 0 0 0 20px;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        margin-right: 40px;
        margin-left: 10px;
        border-top-left-radius: 5px;
        border-left: 4px solid #4361ee;
    }
    
    .bot-message::before {
        content: "";
        position: absolute;
        top: 0;
        left: -10px;
        width: 20px;
        height: 20px;
        background: linear-gradient(225deg, #f0f4ff 0%, #f0f4ff 50%, transparent 50%, transparent 100%);
        border-radius: 0 0 20px 0;
    }
    
    .avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 15px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
        border: 2px solid white;
    }
    
    /* Health Category Cards */
    .health-category {
        background: white;
        padding: 14px;
        border-radius: 16px;
        margin: 8px;
        cursor: pointer;
        text-align: center;
        transition: all 0.3s ease;
        color: #333333;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .health-category:hover {
        background: linear-gradient(135deg, #eef2ff 0%, #e6f0ff 100%);
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(67, 97, 238, 0.15);
        border-color: rgba(67, 97, 238, 0.2);
    }
    
    .health-category.selected {
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        color: white !important;
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.3);
    }
    
    /* Typing Indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        margin-left: 15px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        border-radius: 50%;
        opacity: 0.6;
        animation: typing-dot-animation 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing-dot-animation {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    
    /* Disclaimer Box */
    .disclaimer {
        padding: 15px;
        background: linear-gradient(135deg, #fff8e1 0%, #fffbec 100%);
        border-left: 4px solid #ffb74d;
        margin-top: 20px;
        border-radius: 8px;
        font-size: 14px;
        color: #333333;
        box-shadow: 0 3px 10px rgba(255, 183, 77, 0.2);
    }
    
    /* Topic Badge */
    .topic-badge {
        display: inline-block;
        background: linear-gradient(90deg, #4361ee, #3a0ca3);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 10px;
        box-shadow: 0 3px 8px rgba(67, 97, 238, 0.3);
    }
    
    /* Conversation Container */
    .conversation-container {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .conversation-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .conversation-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .conversation-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        border-radius: 10px;
    }
    
    /* Input Container */
    .input-container {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e2130 0%, #2d3250 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] h1 {
        color: white !important;
        -webkit-text-fill-color: white !important;
        margin-bottom: 30px !important;
        font-size: 26px !important;
        background: none;
        text-align: center;
    }
    
    [data-testid="stSidebar"] h3 {
        color: white !important;
        -webkit-text-fill-color: white !important;
        background: none;
        margin-top: 20px !important;
        margin-bottom: 15px !important;
        font-size: 18px !important;
    }
    
    [data-testid="stSidebar"] .health-category {
        background: rgba(255, 255, 255, 0.05);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .health-category:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .health-category.selected {
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
    }
    
    /* Fix for dark mode and light mode compatibility */
    .st-emotion-cache-1v0mbdj, .st-emotion-cache-16txtl3, .st-emotion-cache-1wrcr25 {
        color: #333333 !important;
    }
    
    /* Ensure sidebar text is visible */
    .st-sidebar .st-emotion-cache-16idsys p, 
    .st-sidebar .st-emotion-cache-16idsys h1, 
    .st-sidebar .st-emotion-cache-16idsys h2, 
    .st-sidebar .st-emotion-cache-16idsys h3, 
    .st-sidebar .st-emotion-cache-16idsys li,
    .st-sidebar .st-emotion-cache-16idsys div {
        color: #f8f9fa !important;
    }
    
    /* Force dark background text to be light */
    [data-testid="stSidebar"] {
        color: #f8f9fa !important;
    }
    
    /* Ensure the main content area has correct contrast */
    .st-emotion-cache-183lzff {
        color: #333333;
    }
    
    /* Specific fix for the healthcare assistant response text */
    .bot-message div, .user-message div {
        color: #333333 !important;
    }
    
    /* Responsive layout adjustments */
    @media (max-width: 768px) {
        .chat-message {
            max-width: 100%;
        }
        
        .user-message {
            margin-left: 10px;
        }
        
        .bot-message {
            margin-right: 10px;
        }
    }
    
    /* Animation for page elements */
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    .animate-slide-up {
        animation: slideUp 0.5s ease-out forwards;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Set environment variables
def set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# Define sample questions for each health category
DEMO_QUESTIONS = {
    "General Health": "What are some essential health screenings recommended for adults?",
    "Symptoms & Conditions": "What are common symptoms of seasonal allergies and how can I manage them?",
    "Nutrition": "What foods are good sources of omega-3 fatty acids and why are they important?",
    "Fitness": "What are the benefits of incorporating strength training into my exercise routine?",
    "Mental Health": "What are some effective strategies for managing stress in daily life?",
    "Medications": "What should I know about taking antibiotics properly?",
    "First Aid": "How should I properly clean and dress a minor cut or wound?",
    "Sleep Health": "What are some tips for improving sleep quality naturally?"
}

# Initialize environment
if 'initialized' not in st.session_state:
    set_env("GOOGLE_API_KEY")
    st.session_state.initialized = True
    st.session_state.current_topic = None
    st.session_state.messages = []
    st.session_state.input_key = 0  # Add a key counter for input widgets
    st.session_state.demo_question = ""

# Define health categories with icons
HEALTH_CATEGORIES = {
    "General Health": {
        "description": "General health and wellness advice, including preventive care and lifestyle recommendations.",
        "icon": "🏥"
    },
    "Symptoms & Conditions": {
        "description": "Information about common symptoms and medical conditions (not for diagnosis).",
        "icon": "🔍"
    },
    "Nutrition": {
        "description": "Nutritional guidance, dietary recommendations, and information about healthy eating habits.",
        "icon": "🥗"
    },
    "Fitness": {
        "description": "Physical activity recommendations, exercise tips, and fitness-related information.",
        "icon": "💪"
    },
    "Mental Health": {
        "description": "Information about mental well-being, stress management, and emotional health.",
        "icon": "🧠"
    },
    "Medications": {
        "description": "General information about common medications, side effects, and usage guidelines.",
        "icon": "💊"
    },
    "First Aid": {
        "description": "Basic first aid information and emergency response guidance.",
        "icon": "🚑"
    },
    "Sleep Health": {
        "description": "Guidance for better sleep habits and sleep-related issues.",
        "icon": "😴"
    }
}

# Initialize LLM
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.2,
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )

# Setup the healthcare chatbot
@st.cache_resource
def setup_chain():
    llm = get_llm()
    
    template = """
    You are an advanced Healthcare Assistant, a specialized AI designed to provide informative guidance on health and wellness topics. You are knowledgeable about medical information, wellness practices, and health resources.

    Important guidelines:
    1. You are NOT a doctor and CANNOT provide medical diagnoses.
    2. You should always encourage users to consult with healthcare professionals for specific medical concerns.
    3. Your responses should be evidence-based, referencing reputable health organizations like WHO and CDC when appropriate.
    4. Provide clear, concise information that is easy to understand.
    5. Be empathetic and supportive while maintaining professionalism.
    6. If you don't know something or if it's outside your scope, acknowledge this clearly.

    Current topic focus: {current_topic}

    Previous conversation:
    {history}

    Human: {human_input}
    Healthcare Assistant:"""
    
    prompt = PromptTemplate(
        input_variables=["history", "human_input", "current_topic"],
        template=template
    )
    
    memory = ConversationBufferMemory(
        memory_key="history",
        input_key="human_input"
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    return chain

# App layout
def main():
    # Sidebar
    with st.sidebar:
        st.title("🏥 HealthCare Assistant")
        st.markdown("### Select a Health Topic")
        
        selected_topic = None
        for topic, info in HEALTH_CATEGORIES.items():
            if st.button(
                f"{info['icon']} {topic}", 
                key=f"topic_{topic}", 
                help=info['description'],
                use_container_width=True
            ):
                selected_topic = topic
                st.session_state.current_topic = topic
                st.session_state.demo_question = DEMO_QUESTIONS[topic]
                st.session_state.input_key += 1  # Force input field refresh
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### About This Chatbot
        
        This advanced healthcare assistant provides general health information and wellness guidance. It can help with:
        
        - General health advice
        - Information about symptoms
        - Wellness and prevention tips
        - Basic information on conditions and medications
        """)
        
        # Disclaimer
        st.markdown("""
        <div class="disclaimer">
            <strong>Medical Disclaimer:</strong> This chatbot provides general health information only. 
            It is not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult with qualified healthcare providers for medical concerns.
        </div>
        """, unsafe_allow_html=True)

    # Main content
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.markdown('<h1 class="animate-fade-in">Talk to Your Healthcare Assistant</h1>', unsafe_allow_html=True)
        
        # Show current topic with badge
        if st.session_state.current_topic:
            topic_info = HEALTH_CATEGORIES[st.session_state.current_topic]
            st.markdown(f"""
            <div class="animate-slide-up">
                <span class="topic-badge">{topic_info['icon']} {st.session_state.current_topic}</span>
                <p><em>{topic_info['description']}</em></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="animate-slide-up">
                <p><em>Select a health topic from the sidebar to get started, or ask a general health question below.</em></p>
            </div>
            """, unsafe_allow_html=True)

        # Initialize the conversation chain
        chain = setup_chain()
        
        # Display chat messages in a container
        with st.container():
            st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
            
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div>👤 <b>You:</b> {message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <div>{HEALTH_CATEGORIES.get(st.session_state.current_topic, {"icon": "🏥"})["icon"]} <b>Healthcare Assistant:</b> {message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input in a container
        with st.container():
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            
            # Create columns for input and button
            input_col, button_col = st.columns([5, 1])
            
            # Create a unique key for the input field
            input_key = f"user_input_{st.session_state.input_key}"
            with input_col:
                # Use the demo question if a topic was just selected
                user_input = st.text_input(
                    "Type your health question here:", 
                    key=input_key,
                    value=st.session_state.demo_question
                )
            
            with button_col:
                send_button = st.button("Send", key=f"send_{st.session_state.input_key}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if send_button and user_input:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Clear the demo question so it doesn't appear again
                st.session_state.demo_question = ""
                
                # Display the user message
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div>👤 <b>You:</b> {user_input}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show typing indicator
                with st.empty():
                    st.markdown("""
                    <div class="chat-message bot-message">
                        <div>🏥 <b>Healthcare Assistant:</b> 
                            <div class="typing-indicator">
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get AI response
                    current_topic = st.session_state.current_topic if st.session_state.current_topic else "General Health Information"
                    response = chain.predict(
                        human_input=user_input,
                        current_topic=current_topic
                    )
                    
                    # Add a small delay to simulate typing
                    time.sleep(0.5)
                
                # Display AI response
                topic_icon = HEALTH_CATEGORIES.get(st.session_state.current_topic, {"icon": "🏥"})["icon"]
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <div>{topic_icon} <b>Healthcare Assistant:</b> {response}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add AI message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Increment the key counter for the next input widget instead of modifying the current one
                st.session_state.input_key += 1
                
                # Force a rerun to display the new empty input field
                st.rerun()

if __name__ == "__main__":
    main()
