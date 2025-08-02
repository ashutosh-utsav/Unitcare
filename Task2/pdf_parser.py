import pandas as pd
from pathlib import Path
import json
import os
import time
import tempfile
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in your .env file.")
genai.configure(api_key=API_KEY)

TEST_NAME_MAP = {
    "Hemoglobin": "Hemoglobin",
    "Platelets": "Platelet Count",
    "White Blood Cells (WBC)": "WBC",
    "TOTAL CHOLESTEROL": "Cholesterol",
    "TRIGLYCERIDES": "Triglycerides",
    "HDL-CHOLESTEROL": "HDL Cholesterol",
    "LDL-CHOLESTEROL": "LDL Cholesterol",
    "VLDL": "VLDL",
    "Glucose (Fasting)": "Fasting Glucose",
}

def normalize_and_convert_units(record: dict) -> dict:
    test_name = record.get("test_name", "")
    original_value = record.get("value")
    original_unit = record.get("unit", "").lower()

    record['original_value'] = original_value
    record['original_unit'] = record.get("unit", "")

    if 'glucose' in test_name.lower() and 'mmol/l' in original_unit:
        record['value'] = round(original_value * 18.0182, 2)
        record['unit'] = 'mg/dL'

    return record

def extract_data_with_gemini(pdf_path: Path) -> list:
    model = genai.GenerativeModel('gemini-2.5-flash')
    pdf_file = genai.upload_file(path=pdf_path)

    prompt = """
    Analyze the attached PDF lab report.
    1. Find the sample collection date (format as YYYY-MM-DD).
    2. Extract all major test results, especially for CBC, Lipid Panel, and Glucose.
    3. For each test, provide the test name, its numerical value, and its unit.
    4. Return the result ONLY as a valid JSON list of objects. Each object must have four keys: "test_name", "date", "value", and "unit".
    Example format:
    [
        {"test_name": "Hemoglobin", "date": "2025-06-30", "value": 15.6, "unit": "g/dl"}
    ]
    """
    
    try:
        response = model.generate_content([prompt, pdf_file], request_options={"timeout": 600})
        cleaned_json = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_json)
    except Exception as e:
        return []
    finally:
        genai.delete_file(pdf_file.name)

def create_trend_data(files: List) -> dict:
    all_results = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = file.read()
            tmp.write(content)
            tmp_path = tmp.name

        extracted_data = extract_data_with_gemini(Path(tmp_path))
        for item in extracted_data:
            normalized_item = normalize_and_convert_units(item)
            all_results.append(normalized_item)

        os.unlink(tmp_path)
        time.sleep(1)

    if not all_results:
        return {}

    df = pd.DataFrame(all_results)
    df['test_name'] = df['test_name'].apply(lambda x: TEST_NAME_MAP.get(x, x))
    
    trend_data = {}
    output_columns = ['date', 'value', 'unit', 'original_value', 'original_unit']
    
    for test_name, group in df.groupby('test_name'):
        valid_records = group.dropna(subset=['value'])
        trend_data[test_name] = valid_records[output_columns].to_dict('records')

    return trend_data