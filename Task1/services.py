import os
import json
import whisper
import google.generativeai as genai

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using OpenAI's Whisper model.
    """
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Whisper model loaded.")

    print(f"Starting transcription for {file_path}...")
    try:
        result = model.transcribe(file_path)
        print("Transcription complete.")
        return result["text"]
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""


def extract_emr_data(transcript: str) -> dict:
    """
    Sends a transcript to the Gemini API to extract structured EMR data.
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not found.")
            return {}
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return {}

    print("Sending transcript to Gemini for analysis...")
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are a highly trained medical assistant specializing in parsing doctor-patient conversations. Your task is to analyze the following transcript and extract structured clinical information.

    The required JSON output must contain these four fields exactly:
    - "chief_complaint": The primary reason the patient is visiting the doctor.
    - "history": A brief history of the present illness, including duration and context.
    - "diagnosis": The doctor's clinical assessment or diagnosis.
    - "plan": The proposed treatment plan, including medications, therapies, or follow-ups.

    Analyze the transcript below. If you cannot find information for a specific field, you MUST use an empty string "" as the value for that field.

    Provide your output *only* in a valid JSON object format. Do not include any introductory text, explanations, or markdown code fences.

    --- TRANSCRIPT ---
    {transcript}
    --- END TRANSCRIPT ---

    JSON Output:
    """

    try:
        response = model.generate_content(prompt)
        
        print("--- Raw Gemini Response ---")
        print(response.text)
        print("--------------------------")

        cleaned_response = response.text.strip().lstrip("```json").rstrip("```")
        
        print("Gemini analysis complete. Parsing JSON...")
        return json.loads(cleaned_response)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from Gemini response: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while contacting Gemini: {e}")
        return {}


if __name__ == '__main__':
    from dotenv import load_dotenv
    from pprint import pprint

 
    load_dotenv()

    sample_transcript = transcribe_audio("sample_audio/Basic Requests 2-Jane Wightwick & Mahmoud Gaafar.mp3")

    emr_data = extract_emr_data(sample_transcript)

    if emr_data:
        pprint(emr_data)
        print("\nTest successful!")
    else:
        print("\nTest failed or returned no data.")