# Islamic Finance Accounting Assistant

This project was developed as part of Challenge 1 – Use Case Scenarios of the IsDBI Islamic Finance AI Hackathon.
It features a Streamlit interface powered by Ubility AI and OpenAI GPT models, designed to analyze Islamic finance cases and generate journal entries in compliance with AAOIFI accounting standards.

## Features

- **Case Analysis**: Process Islamic finance case descriptions
- **Contract Type Identification**: Determine the specific Islamic financial contract type
- **AAOIFI Standard Reference**: Provide the relevant AAOIFI Financial Accounting Standard
- **Journal Entry Generation**: Calculate and format proper accounting journal entries
- **Step-by-Step Explanation**: Show detailed reasoning for calculations

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Start the Streamlit application:

```bash
python -m streamlit run islamic_finance_text_output.py
```

2. Access the application in your web browser (typically at http://localhost:8501)
3. Enter your Islamic finance case in the text area
4. Click "Analyze Case" to process
5. Review the structured results

## Files in this Repository

- `islamic_finance_direct_openai.py` - Enhanced application with environment variable support
- `requirements.txt` - Required Python packages
- `.env` - Environment variables file (you need to add your API key)
- `README.md` - This documentation file

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection

## Project Structure

```
islamic-finance-app/
├── islamic_finance_text_output.py
├── islamic_finance_direct_openai.py
├── requirements.txt
├── .env
└── README.md
```

## How It Works

1. The application takes a textual description of an Islamic finance case
2. It processes this text using OpenAI's GPT model via the Ubility SDK
3. The model analyzes the case and returns a structured output with:
   - Contract type identification
   - Applicable AAOIFI standard
   - Journal entry calculations
   - Step-by-step explanation
4. The results are displayed in an organized, user-friendly interface

## Customization

You can customize the application by:

- Modifying the prompt template in the `LANGCHAIN_BASIC_LLM_CONTENT_JSON` variable
- Adjusting the model parameters in the `LANGCHAIN_BASIC_LLM_MODEL` variable
- Enhancing the UI by editing the Streamlit components

## Limitations

- Requires a valid OpenAI API key
- Internet connection needed for API calls
- Analysis quality depends on the clarity and completeness of the case description

## Troubleshooting

If you encounter issues:

1. Verify your OpenAI API key is correctly set in the `.env` file
2. Check that all dependencies are installed
3. Ensure you have a stable internet connection
4. Verify the Ubility SDK is properly installed and configured

