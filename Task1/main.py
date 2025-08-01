import os
import shutil
import tempfile
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError

from services import transcribe_audio, extract_emr_data
from models import EMRData

load_dotenv()

app = FastAPI()

@app.get("/")
async def read_root():
    """
    Serve the main HTML page.
    """
    return FileResponse('templates/index.html')

@app.post("/process")
async def process_audio_file(file: UploadFile = File(...)):
    """
    Endpoint to upload an audio file, process it, and return structured EMR data.
    """

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
    finally:
        file.file.close()

    try:
        transcript = transcribe_audio(tmp_path)
        if not transcript:
            raise HTTPException(status_code=400, detail="Audio transcription failed or produced no text.")

        emr_data_dict = extract_emr_data(transcript)
        if not emr_data_dict:
            raise HTTPException(status_code=500, detail="Failed to extract EMR data from the transcript.")

        try:
            validated_data = EMRData(**emr_data_dict)
            return validated_data
        except ValidationError as e:
            print(f"Validation Error: {e}")
            raise HTTPException(status_code=500, detail=f"Data validation failed: {e}")

    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    import uvicorn
    print("Starting server... Go to http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)