import os
import json
from typing import List
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in your .env file.")
genai.configure(api_key=API_KEY)

def summarize_json_with_gemini(files: List) -> str:
    if not files:
        return "No files were provided for summarization."

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    combined_content = ""
    for file in files:
        content = file.read()
        try:
            parsed_json = json.loads(content)
            combined_content += json.dumps(parsed_json, indent=2) + "\n\n"
        except json.JSONDecodeError:
            combined_content += content.decode('utf-8') + "\n\n"

    prompt = f"""
    Based on the following patient EMR data from one or more JSON files, please generate a concise, well-formatted narrative summary.
    Consolidate information across all visits. Note any recurrent complaints, chronic diagnoses, and create a single consolidated list of all medications.
    Format the output using Markdown.

    EMR Data:
    {combined_content}
    """

    try:
        response = model.generate_content(prompt, request_options={"timeout": 600})
        return response.text
    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        return "Error: Could not generate summary from the AI model."