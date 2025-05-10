import streamlit as st
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
    page_title="Islamic Finance Text Output",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a header
st.title("Islamic Finance Analysis")
st.markdown("This application analyzes Islamic finance cases and returns results as text.")

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
Your task is to analyze the case below and provide the following information as text:

1. ISLAMIC CONTRACT TYPE:
   Identify the Islamic finance contract type in this case.

2. APPLICABLE AAOIFI STANDARD:
   State the applicable AAOIFI FAS number.

3. JOURNAL ENTRIES:
   Provide the accounting entries (journal lines with amounts) that should be recorded.

4. EXPLANATION:
   Give a step-by-step explanation including calculations for the Right-of-Use (ROU) asset 
   and Deferred Ijarah Cost, using this method:
   - ROU = (purchase cost + installation + other pre-delivery costs) − expected purchase price (if ownership is transferred)
   - Total rentals = rental per year × lease years
   - Deferred Ijarah Cost = Total rentals − ROU (if positive)

Case for analysis:
{user_question}"""

                # Make API call to OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o",
                    temperature=0.7,
                    messages=[
                        {"role": "system", "content": "You are an expert Islamic finance accountant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Get the text response
                result_text = response.choices[0].message.content
                
                # Display success message
                st.success("Analysis complete!")
                
                # Show the text output directly
                st.subheader("Analysis Results")
                st.write(result_text)
                
                # Add a download button for the text
                st.download_button(
                    label="Download Results",
                    data=result_text,
                    file_name="islamic_finance_analysis.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.info("Check your API key configuration and ensure all dependencies are installed.")
    else:
        st.warning("Please enter a case to analyze.")

# Display instructions in the sidebar
with st.sidebar:
    st.subheader("Instructions")
    st.write("""
    1. Enter your Islamic finance case in the text area
    2. Click "Analyze Case" to process
    3. View the text output
    4. Download the results if needed
    """)
    
    st.subheader("Output Format")
    st.write("""
    The analysis provides:
    1. Contract type identification
    2. Applicable AAOIFI standard
    3. Journal entries with amounts
    4. Step-by-step explanation
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