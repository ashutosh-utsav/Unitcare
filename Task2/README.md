# Patient Data Processor & Lab Trend Analyzer


## Live - [Live-link](https://unitcare-csijj5os2rxzuw7m5ryimd.streamlit.app/)

This project is an interactive web application built with Streamlit that provides a comprehensive toolkit for processing and visualizing patient medical data. It leverages the Google Gemini Pro AI model to intelligently parse and summarize unstructured data from various file formats.

FeaturesThe application is divided into two main parts:

### Part 1: 
1. EMR Visit Summarizer

    * AI-Powered Summarization: Upload one or more patient EMR visit files in any JSON format.
    
    * Narrative Generation: The application uses the Gemini API to analyze the combined data and generate a concise, human-readable narrative summary, highlighting recurrent complaints, chronic diagnoses, and consolidated medication lists.

### Part 2: 
1. Lab Trend Analyzer
    
    * PDF Lab Report Parsing: Upload one or more patient lab reports in PDF format, even from different labs with varying layouts.
    
    * Intelligent Data Extraction: The Gemini API reads the PDFs to extract key test results (CBC, Lipid Panel, Glucose, etc.), their values, units, and the sample collection date. 

    * Unit Conversion & Normalization: Automatically converts common units (e.g., Glucose from mmol/L to mg/dL) to a standard for consistent analysis and includes the original values in the final output.

    * Trend Visualization: Interactively displays the extracted lab data as a line chart, allowing users to visualize trends for specific tests over time.


```bash
Task2/
│
├── main.py                  # The main Streamlit application file
├── processor.py            # Handles EMR JSON summarization using Gemini
├── pdf_parser.py           # Handles PDF lab report parsing and trend generation using Gemini
│
├── .env                    # Stores the secret Google API key (must be created manually)
└── README.md               # This file
```




## Setup and Installation

### 1. Prerequisites
```bash
Python
UV(for package management. You can install uv by following the official instructions.)
```
### 2. 
```bash
git clone the REPO 

# Create the environment
uv venv

# Activate it (on macOS/Linux)
source .venv/bin/activate

# Activate it (on Windows)
.venv\Scripts\activate
```

### 3. Install The dependencies
```bash
uv pip install -e .
#OR
uv sync
```

### 4. 
```bash
cd Task2

# Configure API Key
touch .env

# Add the following in .env
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### 5. Run the app 
```bash
streamlit run main.py
```


## How to Use the Application
Once the application is running in your browser, follow these steps:

#### 1. To Generate an EMR Summary (Part 1)

- On the left side of the screen, under "Part 1: EMR Visit Summarizer", click the "Browse files" button.
- Select one or more patient EMR JSON files from your computer.
- Click the "Generate Summary" button.
- Wait for the spinner to finish processing. The generated narrative summary will appear on the right side of the screen.

#### 2. To Analyze Lab Trends (Part 2):

- On the left side of the screen, under "Part 2: Lab Trend Analyzer", click the "Browse files" button.
- Select one or more patient lab report PDF files.
- Click the "Analyze Trends" button.
- Wait for the AI analysis to complete. This may take a moment.
- The results will appear on the right side. You can now:
- Use the dropdown menu to select a specific lab test.
- View the trend for the selected test in the line chart.


