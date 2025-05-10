import streamlit as st
import json
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client
if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    st.error("⚠️ OpenAI API key not found! Please add your API key to the .env file.")
    st.stop()

# Set page title and configure layout
st.set_page_config(
    page_title="Islamic Finance Accounting Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a header with styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
<div class="main-header">Islamic Finance Accounting Assistant</div>
<div class="subheader">AAOIFI Standards & Journal Entry Analysis</div>
""", unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2 = st.tabs(["Case Analysis", "About"])

with tab1:
    # Create a text area for user input with a default example
    default_question = 'On 1 January 2019, Alpha Islamic Bank entered into an Ijarah MBT with Super Generators for a generator costing $450,000. Import tax was $12,000 and freight was $30,000. Lease term: 2 years with annual rental of $300,000. Purchase option: $3,000.'
    user_question = st.text_area("Enter your Islamic finance case:", value=default_question, height=150)

    # Create a button to trigger the analysis
    if st.button("Analyze Case", type="primary"):
        if user_question.strip():
            # Display a spinner while processing
            with st.spinner("Analyzing the case..."):
                try:
                    # Define the prompt for the OpenAI API
                    prompt = f"""You are an expert Islamic finance accountant specializing in AAOIFI standards.
Your task is to analyze the case below and return a raw JSON object with:
- "contract_type": Islamic finance contract type
- "standard": AAOIFI FAS number
- "journal_entry": Accounting entry (journal lines with amounts)
- "explanation": Step-by-step reasoning including how the Right-of-Use (ROU) asset and Deferred Ijarah Cost are calculated
Use the following method for ROU:
1. ROU = (purchase cost + installation + other pre-delivery costs) − expected purchase price (if ownership is transferred).
2. Total rentals = rental per year × lease years.
3. Deferred Ijarah Cost = Total rentals − ROU (if positive).
❗Return ONLY the raw JSON object. Do not include triple backticks, markdown, or any extra text.
---
Case:
{user_question}"""

                    # Make API call to OpenAI
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        response_format={"type": "json_object"},
                        temperature=0.7,
                        messages=[
                            {"role": "system", "content": "You are an expert Islamic finance accountant."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # Parse the JSON response
                    result_text = response.choices[0].message.content
                    result = json.loads(result_text)
                    
                    # Display results - just show the JSON itself
                    st.success("Analysis complete! Here's the JSON output:")
                    
                    # Display JSON output in a code block with highlighting
                    st.json(result)
                    
                    # Add option to view in alternate formats if needed
                    view_mode = st.radio(
                        "View options:",
                        ["JSON Only", "Formatted Display"],
                        horizontal=True
                    )
                    
                    if view_mode == "Formatted Display":
                        st.markdown("### 📊 Formatted Results")
                        
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.markdown("#### Contract Information")
                            st.info(f"**Contract Type:** {result['contract_type']}")
                            st.info(f"**AAOIFI Standard:** {result['standard']}")
                        
                        st.markdown("#### Journal Entry")
                        st.code(result['journal_entry'], language="text")
                        
                        st.markdown("#### Explanation")
                        st.write(result['explanation'])
                    
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
                    st.info("Check your API key configuration and ensure all dependencies are installed.")
        else:
            st.warning("Please enter a case to analyze.")

with tab2:
    st.markdown("""
    ## About This Application
    
    This application helps users analyze Islamic finance cases according to AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) standards.
    
    ### Features
    - **Contract Type Identification**: Determine the specific Islamic financial contract type from case details
    - **AAOIFI Standard Reference**: Provide the relevant AAOIFI Financial Accounting Standard
    - **Journal Entry Generation**: Calculate and format proper accounting journal entries
    - **Step-by-Step Explanation**: Show detailed reasoning for calculations
    
    ### How It Works
    The application uses natural language processing powered by OpenAI's GPT-4o model to analyze financial cases and generate structured analysis.
    
    ### Credits
    Built with:
    - Streamlit
    - OpenAI API
    """)

# Display instructions in the sidebar
with st.sidebar:
    st.image("https://placehold.co/600x200?text=Islamic+Finance", use_column_width=True)
    
    st.subheader("Instructions")
    st.write("""
    1. Enter your Islamic finance case in the text area
    2. Click "Analyze Case" to process
    3. Review the structured results
    """)
    
    st.subheader("Required Setup")
    st.write("""
    Before running this app:
    1. Install required packages:
       ```
       pip install -r requirements.txt
       ```
    2. Create a `.env` file with your OpenAI API key:
       ```
       OPENAI_API_KEY=your_key_here
       ```
    """)

    st.caption("© 2025 Islamic Finance AI Assistant")