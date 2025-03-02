import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import io
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page layout and title with improved styling
st.set_page_config(
    page_title="Data Analysis Agent",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Custom CSS for a more professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 0.8rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #1E3A8A;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #F0F2F6;
    }
    .card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #EFF6FF;
        border-radius: 8px;
        padding: 1.2rem;
        height: 100%;
        border-left: 4px solid #3B82F6;
    }
    .feature-title {
        color: #1E40AF;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .highlight {
        background-color: #DBEAFE;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    .sidebar-content {
        padding: 1.5rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #F1F5F9;
    }
    .stTabs [aria-selected="true"] {
        background-color: #DBEAFE !important;
        border-bottom: 2px solid #3B82F6;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
    }
    .recommendation-card {
        border-left: 4px solid #3B82F6;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    /* Custom styling for buttons */
    div.stButton > button {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    div.stButton > button:hover {
        background-color: #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# Custom headers
st.markdown('<div class="main-header">📊 Data Analysis Agent</div>', unsafe_allow_html=True)
st.markdown(
    """<p style="font-size: 1.1rem; margin-bottom: 2rem;">
    Upload your data file and ask questions to get AI-powered insights and visualizations.
    </p>""", 
    unsafe_allow_html=True
)

# Set up Gemini API using environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Add fallback for manual input of API key if not found in environment
if not GOOGLE_API_KEY:
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.markdown('<h3>⚙️ Configuration</h3>', unsafe_allow_html=True)
    st.sidebar.info("API key not found in environment variables. Please enter it below.")
    GOOGLE_API_KEY = st.sidebar.text_input("Enter your Gemini API Key", type="password")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Configure API when key is available
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # Show a subtle success message when API key is configured
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = True
        st.sidebar.success("API key configured successfully!", icon="✅")
else:
    st.sidebar.warning("Please add your Gemini API Key to the .env file or enter it in the sidebar to continue.")

# Initialize session state to store data and history
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_description' not in st.session_state:
    st.session_state.data_description = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'columns_info' not in st.session_state:
    st.session_state.columns_info = None

# File uploader section with improved styling
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
st.sidebar.markdown('<h3>📁 Data Upload</h3>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx'])

# Add sample data option
if not uploaded_file:
    if st.sidebar.button("Use Sample Data"):
        # Create a sample dataset path
        sample_data_path = "sample_sales_data.csv"
        
        # Check if sample data exists, if not create it
        if not os.path.exists(sample_data_path):
            # Create sample data from the data in your document
            sample_data = pd.DataFrame({
                "TransactionDate": ["3/22/2024", "6/18/2024", "5/3/2024", "8/12/2024", "11/29/2024", 
                                   "4/17/2024", "7/31/2024", "9/25/2024", "2/14/2024", "10/3/2024"],
                "TransactionID": ["TRX-10000", "TRX-10001", "TRX-10002", "TRX-10003", "TRX-10004",
                                 "TRX-10005", "TRX-10006", "TRX-10007", "TRX-10008", "TRX-10009"],
                "StoreLocation": ["Chicago", "Miami", "New York", "Los Angeles", "Seattle",
                                 "Chicago", "New York", "Miami", "Seattle", "Los Angeles"],
                "ProductCategory": ["Electronics", "Clothing", "Home Goods", "Groceries", "Beauty",
                                   "Electronics", "Clothing", "Home Goods", "Groceries", "Beauty"],
                "Quantity": [3, 2, 1, 4, 3, 2, 5, 1, 2, 4],
                "UnitPrice": [823.45, 118.33, 327.89, 52.77, 88.65, 452.30, 49.99, 198.55, 87.22, 37.99],
                "DiscountAmount": [0.00, 47.33, 0.00, 0.00, 35.46, 180.92, 0.00, 0.00, 34.89, 0.00],
                "TotalSale": [2470.35, 189.33, 327.89, 211.08, 230.49, 723.68, 249.95, 198.55, 139.55, 151.96],
                "PaymentMethod": ["Credit Card", "Mobile Payment", "Cash", "Debit Card", "Credit Card",
                                 "Gift Card", "Cash", "Mobile Payment", "Credit Card", "Debit Card"],
                "CustomerAge": [42, 35, 29, 53, 61, 24, 38, 47, 59, 31],
                "CustomerRating": [3, 5, 2, 4, 5, 5, 1, 3, 5, 2],
                "PromotionApplied": ["", "1", "", "", "1", "1", "", "", "1", ""],
                "WeatherCondition": ["Sunny", "Cloudy", "Rainy", "Sunny", "Snowy", "Windy", "Rainy", "Cloudy", "Snowy", "Sunny"]
            })
            sample_data.to_csv(sample_data_path, index=False)
        
        # Use the sample data as if it was uploaded
        uploaded_file = open(sample_data_path, "rb")
        st.sidebar.success("Sample data loaded successfully!")

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Helper functions for data processing and analysis
def load_data(file):
    """Load data from uploaded file into pandas DataFrame"""
    # Determine file type and read accordingly
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:  # Excel file
        df = pd.read_excel(file)
    return df

def get_data_description(df):
    """Generate a comprehensive description of the dataframe"""
    # Create a string buffer to capture dataframe info
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    
    # Get basic statistics and shape information
    stats = df.describe().to_string()
    shape = f"Shape: {df.shape[0]} rows x {df.shape[1]} columns"
    
    # Get information about column types and missing values
    column_types = df.dtypes.to_string()
    missing_values = df.isnull().sum().to_string()
    
    # Compile all information into a comprehensive description
    description = f"{shape}\n\nColumn Information:\n{column_types}\n\nMissing Values:\n{missing_values}\n\nSummary Statistics:\n{stats}\n\nInfo:\n{info_str}"
    
    return description

def analyze_with_gemini(prompt, df_description=None, max_tokens=8192):
    """Use Gemini to analyze data based on a prompt"""
    if not GOOGLE_API_KEY:
        return "Please provide a valid API key to continue."
    
    try:
        # Construct a prompt that includes data context
        if df_description:
            system_prompt = f"""You are a data analysis assistant. Analyze the following dataset:
            
            {df_description}
            
            User question: {prompt}
            
            Provide a clear, insightful analysis. If appropriate for the question, include code for visualizations in Python using Plotly or Matplotlib."""
        else:
            system_prompt = prompt
        
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"Error in generating analysis: {str(e)}"

def generate_visualizations(df, query):
    """Generate visualizations based on user query using Gemini's suggestions"""
    if not GOOGLE_API_KEY:
        return "Please provide a valid API key to continue."
    
    try:
        # Create a prompt to ask for visualization code
        system_prompt = f"""You are a data visualization expert. Based on this dataset and query, generate Python code for a visualization.
        
        Dataset columns: {', '.join(df.columns.tolist())}
        Sample data: {df.head(3).to_string()}
        
        Query: {query}
        
        Return ONLY runnable Python code that uses Plotly or Matplotlib for the visualization. The code should be suitable for execution in a Streamlit app.
        Use 'fig' as the figure variable name. 
        
        IMPORTANT: DO NOT include any display commands like plt.show(), st.plotly_chart(), or st.pyplot() in your code. 
        ONLY create the figure and assign it to the variable 'fig'.
        
        Do not include markdown code blocks or explanations, just the Python code that I can execute directly."""
        
        response = model.generate_content(system_prompt)
        code = response.text.strip()
        
        # Remove markdown code block indicators if present
        if code.startswith("```python"):
            code = code[len("```python"):].strip()
        if code.endswith("```"):
            code = code[:-3].strip()
        
        # Make the code available for inspection and create a local context with the dataframe
        with st.expander("View Visualization Code"):
            st.code(code, language="python")
        
        # Execute the code in a controlled environment to avoid duplicate displays
        local_vars = {"df": df, "px": px, "go": go, "plt": plt, "np": np, "sns": sns, "pd": pd}
        
        # Clear any existing matplotlib figures to prevent leakage
        plt.close('all')
        
        # Execute the code
        exec(code, globals(), local_vars)
        
        # Get the figure and return it
        if 'fig' in local_vars:
            return local_vars['fig']
        else:
            return "No visualization was generated by the code."
    except Exception as e:
        return f"Error generating visualization: {str(e)}"

def get_recommendations(df):
    """Get recommendations for further analysis based on the dataset"""
    if not GOOGLE_API_KEY:
        return "Please provide a valid API key to continue."
    
    prompt = f"""You are a data science expert. Based on this dataset:
    
    Column Information:
    {df.dtypes.to_string()}
    
    Data Sample:
    {df.head(5).to_string()}
    
    Missing Values:
    {df.isnull().sum().to_string()}
    
    Please provide 5 specific recommendations for additional analyses or visualizations that would yield valuable insights from this data.
    Format your response as JSON with the structure:
    [
        {{"recommendation": "Brief description of recommendation", "reason": "Why this would be useful"}},
        ...
    ]
    Limit your response to ONLY the JSON array."""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Extract JSON if it's wrapped in markdown code blocks or other text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
        
        # Parse the JSON response
        recommendations = json.loads(text)
        return recommendations
    except Exception as e:
        return [{"recommendation": f"Error getting recommendations: {str(e)}", "reason": "API or parsing error"}]

# Main application logic
if uploaded_file is not None:
    # Display loading message
    with st.spinner("Loading and analyzing your data..."):
        # Check if this is a new file
        if st.session_state.file_name != uploaded_file.name:
            # Load the data
            df = load_data(uploaded_file)
            
            # Store in session state
            st.session_state.data = df
            st.session_state.file_name = uploaded_file.name
            
            # Generate and store data description
            st.session_state.data_description = get_data_description(df)
            
            # Analyze column info for better understanding
            column_analysis_prompt = f"""
            Analyze these dataset columns:
            {df.dtypes.to_string()}
            
            For each column, provide a short description of what it likely represents based on the name, data type, 
            and these sample values:
            {df.head(3).to_string()}
            
            Return a JSON object where keys are column names and values are descriptions.
            """
            column_info_response = analyze_with_gemini(column_analysis_prompt)
            
            # Extract JSON if response contains explanatory text
            try:
                if "```json" in column_info_response:
                    json_str = column_info_response.split("```json")[1].split("```")[0].strip()
                elif "```" in column_info_response:
                    json_str = column_info_response.split("```")[1].strip() 
                else:
                    json_str = column_info_response
                    
                st.session_state.columns_info = json.loads(json_str)
            except:
                st.session_state.columns_info = {"error": "Could not parse column information"}
            
            # Clear history when loading a new file
            st.session_state.history = []
        
        df = st.session_state.data

    # Display dataset information in the main area
    st.markdown('<div class="sub-header">Dataset Overview</div>', unsafe_allow_html=True)
    
    # Create a card for the dataset overview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Create two columns for the overview section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display a sample of the data
        st.markdown('<h4>Data Sample</h4>', unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)
        
        # Display data shape and summary metrics in a cleaner way
        metrics_cols = st.columns(4)
        with metrics_cols[0]:
            st.metric(label="Rows", value=f"{df.shape[0]:,}")
        with metrics_cols[1]:
            st.metric(label="Columns", value=df.shape[1])
        with metrics_cols[2]:
            missing_percent = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
            st.metric(label="Missing Data", value=f"{missing_percent:.1f}%")
        with metrics_cols[3]:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.metric(label="Numeric Columns", value=len(numeric_cols))
            else:
                st.metric(label="Numeric Columns", value="0")
    
    with col2:
        # Display column information with improved styling
        st.markdown('<h4>Column Information</h4>', unsafe_allow_html=True)
        
        if st.session_state.columns_info and "error" not in st.session_state.columns_info:
            for col in df.columns:
                if col in st.session_state.columns_info:
                    with st.expander(f"{col} ({df[col].dtype})"):
                        st.markdown(f"**Description**: {st.session_state.columns_info[col]}")
                        st.markdown(f"**Missing**: {df[col].isnull().sum()} values ({df[col].isnull().sum() / len(df) * 100:.1f}%)")
                        if pd.api.types.is_numeric_dtype(df[col]):
                            st.markdown(f"**Range**: {df[col].min()} to {df[col].max()}")
                            st.markdown(f"**Mean**: {df[col].mean():.2f}")
        else:
            for col in df.columns:
                st.text(f"• {col} ({df[col].dtype})")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display actions available to the user
    st.markdown('<div class="sub-header">Ask Questions About Your Data</div>', unsafe_allow_html=True)
    
    # Create tabs for different types of analysis with improved styling
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📈 Visualization", "💡 Recommendations"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### What would you like to know about this data?")
        analysis_query = st.text_area(
            "Enter your question",
            placeholder="Example: Summarize the key findings from this dataset",
            label_visibility="collapsed"
        )
        
        # Add example questions for better UX
        example_questions = [
            "What is the average sale amount by product category?",
            "Is there a correlation between customer age and total sales?",
            "Which store location has the highest average customer rating?",
            "How does the weather condition affect sales?"
        ]
        
        cols = st.columns(4)
        for i, question in enumerate(example_questions):
            if cols[i].button(f"Example {i+1}", key=f"example_{i+1}", help=question):
                analysis_query = question
                st.rerun()
        
        if st.button("Analyze", key="analyze_btn", use_container_width=True):
            if not analysis_query:
                st.warning("Please enter a question to analyze.")
            else:
                with st.spinner("Generating analysis..."):
                    analysis = analyze_with_gemini(analysis_query, st.session_state.data_description)
                    st.session_state.history.append({"query": analysis_query, "type": "analysis", "result": analysis})
                    st.markdown("### Analysis Results")
                    st.markdown(analysis)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### What visualization would you like to create?")
        viz_query = st.text_area(
            "Enter visualization request", 
            placeholder="Example: Show the relationship between store location and total sales",
            label_visibility="collapsed"
        )
        
        # # Add example visualization requests
        # viz_examples = [
        #     "Plot total sales by product category",
        #     "Create a scatter plot of customer age vs. total sale",
        #     "Show the distribution of payment methods",
        #     "Visualize the relationship between promotion and customer rating"
        # ]
        
        # cols = st.columns(4)
        # for i, viz in enumerate(viz_examples):
        #     if cols[i].button(f"Example {i+1}", key=f"viz_example_{i+1}", help=viz):
        #         viz_query = viz
        #         st.rerun()
        
        if st.button("Generate Visualization", key="viz_btn", use_container_width=True):
            if not viz_query:
                st.warning("Please enter a visualization request.")
            else:
                with st.spinner("Creating visualization..."):
                    # Clear previous matplotlib figures to prevent duplication
                    plt.close('all')
                    
                    viz_result = generate_visualizations(df, viz_query)
                    
                    if isinstance(viz_result, str):
                        st.error(viz_result)
                    else:
                        try:
                            # For Plotly figures with improved appearance
                            fig = viz_result
                            # Update layout for better appearance
                            if hasattr(fig, 'update_layout'):
                                fig.update_layout(
                                    title_font=dict(size=20),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    margin=dict(l=40, r=40, t=40, b=40),
                                    legend=dict(
                                        bordercolor="LightGrey",
                                        borderwidth=1
                                    )
                                )
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            try:
                                # For Matplotlib figures
                                st.pyplot(fig)
                            except:
                                st.error(f"Could not display the visualization: {str(e)}")
                    
                    st.session_state.history.append({"query": viz_query, "type": "visualization"})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Get AI-Powered Recommendations for Analysis")
        st.markdown("Let our AI suggest interesting insights and visualizations based on your data.")
        
        if st.button("Generate Recommendations", key="rec_btn", use_container_width=True):
            with st.spinner("Generating recommendations..."):
                recommendations = get_recommendations(df)
                st.session_state.history.append({"type": "recommendations", "result": recommendations})
                
                # Display recommendations with improved styling
                st.markdown("### Recommended Analyses")
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"Recommendation {i}: {rec.get('recommendation', 'No recommendation')}"):
                        st.markdown(f"**Why this matters**: {rec.get('reason', 'No reason provided')}")
                        # Add a "Try This" button that populates the analysis or visualization tab
                        col1, col2 = st.columns([1, 3])
                        if col1.button("Try as Analysis", key=f"try_analysis_{i}"):
                            # Set up for analysis tab
                            st.session_state.last_recommendation = {
                                "tab": "analysis",
                                "query": rec.get('recommendation')
                            }
                            st.rerun()
                        if col2.button("Try as Visualization", key=f"try_viz_{i}"):
                            # Set up for visualization tab
                            st.session_state.last_recommendation = {
                                "tab": "visualization",
                                "query": rec.get('recommendation')
                            }
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if a recommendation should populate a tab
    if 'last_recommendation' in st.session_state:
        if st.session_state.last_recommendation["tab"] == "analysis":
            # Switch to analysis tab and populate with recommendation
            st.session_state.analysis_query = st.session_state.last_recommendation["query"]
            del st.session_state.last_recommendation
            st.rerun()
        elif st.session_state.last_recommendation["tab"] == "visualization":
            # Switch to visualization tab and populate with recommendation
            st.session_state.viz_query = st.session_state.last_recommendation["query"]
            del st.session_state.last_recommendation
            st.rerun()
    
    # History section with improved styling
    if st.session_state.history:
        st.markdown('<div class="sub-header">Analysis History</div>', unsafe_allow_html=True)
        
        # Add export history functionality
        cols = st.columns([3, 1])
        with cols[1]:
            if st.button("Export Analysis History", key="export_history"):
                history_data = []
                for item in st.session_state.history:
                    history_item = {
                        "type": item["type"],
                        "query": item.get("query", "Auto-generated")
                    }
                    if "result" in item and isinstance(item["result"], str):
                        history_item["result"] = item["result"]
                    history_data.append(history_item)
                
                history_df = pd.DataFrame(history_data)
                csv = history_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="analysis_history.csv",
                    mime="text/csv",
                )
        
        for i, item in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"{i}. {item['type'].capitalize()}: {item.get('query', 'Auto-generated')}"):
                if item['type'] == 'analysis' or 'result' in item:
                    if isinstance(item.get('result'), str):
                        st.markdown(item.get('result', 'No result stored'))
                    else:
                        st.write(item.get('result', 'No result stored'))
                elif item['type'] == 'visualization':
                    st.info("Visualization was generated (not stored in history)")
                elif item['type'] == 'recommendations' and 'result' in item:
                    for rec in item['result']:
                        st.markdown(f'<div class="recommendation-card"><b>{rec.get("recommendation", "No recommendation")}</b>: {rec.get("reason", "No reason provided")}</div>', unsafe_allow_html=True)
else:
    # Display a more professional landing page when no file is uploaded
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 👋 Welcome to the Data Analysis Agent")
    st.markdown("""
    This intelligent assistant helps you analyze your data and discover insights through natural language. 
    To get started, upload a CSV or Excel file using the sidebar, or try our sample dataset.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display features in an attractive grid
    st.markdown('<div class="sub-header">Features</div>', unsafe_allow_html=True)
    
    features = [
        {
            "title": "Natural Language Analysis", 
            "description": "Ask questions about your data in plain English", 
            "icon": "💬"
        },
        {
            "title": "Smart Visualizations", 
            "description": "Generate beautiful charts with a simple request",
            "icon": "📈"
        },
        {
            "title": "AI Recommendations", 
            "description": "Get intelligent suggestions for deeper insights",
            "icon": "💡"
        },
        {
            "title": "Export & Share", 
            "description": "Save your findings for presentations and reports",
            "icon": "📊"
        }
    ]
    
    # Create a 2x2 grid of feature cards
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="feature-card">
                <h3>{feature["icon"]} {feature["title"]}</h3>
                <p>{feature["description"]}</p>
            </div>
            ''', unsafe_allow_html=True) 