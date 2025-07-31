import whisper
import os
import json
import google.generativeai as genai


def transcribe_audio(file_path: str) ->str:
    model = whisper.load_model("base")

    result = model.transcribe(file_path)

    return result["text"]


def extract_emr_data(transcript: str) -> dict:
    """
    Sends a transcript to the Gemini API to extract structured EMR data.
    """
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return {}

    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are a highly trained medical assistant specializing in parsing doctor-patient conversations. Your task is to analyze the following transcript and extract structured clinical information.

    The required JSON output must contain these four fields exactly:
    - "chief_complaint": The primary reason the patient is visiting the doctor.
    - "history": A brief history of the present illness, including duration and context.
    - "diagnosis": The doctor's clinical assessment or diagnosis.
    - "plan": The proposed treatment plan, including medications, therapies, or follow-ups.

    Analyze the transcript below. Provide your output *only* in a valid JSON object format. Do not include any introductory text, explanations, or markdown code fences.

    --- TRANSCRIPT ---
    {transcript}
    --- END TRANSCRIPT ---

    JSON Output:
    """

    response = model.generate_content(prompt)
    
    try:
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```")
        
        print("Gemini analysis complete. Parsing JSON...")
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing JSON from Gemini response: {e}")
        print("Raw response received:", response.text)
        return {}



# if __name__ == '__main__':
#     audiofile = "sample_audio/Basic Requests 1-Jane Wightwick & Mahmoud Gaafar.mp3"

#     transcrib = transcribe_audio(audiofile)

#     print(transcrib)


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