# Ambient Listening EMR Prototype

### This project is a Python application that uses AI to transcribe doctor-patient audio consultations and automatically extracts structured clinical notes into a clean JSON format.

## Overview
The goal of this prototype is to demonstrate the power of "ambient listening" in a clinical setting. By capturing a natural conversation, the application can reduce the administrative burden on physicians, allowing them to focus more on the patient rather than on note-taking.

The backend pipeline consists of two main AI services: 
1. `OpenAI` `Whisper`: For highly accurate, speech-to-text transcription of audio files.`
2. `Google Gemini`: For natural language understanding to parse the transcript and extract key medical information.


The application is built with a user-friendly web interface using Streamlit, allowing users to easily upload an audio file and view the structured output.

### Features
* Audio Transcription: Converts audio files (.mp3, .wav, etc.) into written text.
* Structured Data Extraction: Parses the transcript to identify four key clinical fields:

    * chief_complaint
    * history
    * diagnosis
    * plan

* Web-Based UI: A simple and interactive interface built with Streamlit for file uploads and results display.
* Data Validation: Uses Pydantic to ensure the data extracted by the AI conforms to the required structure.


### Project Structure

```bash
Task1/
│
├── main.py                 # The Streamlit application script
├── services.py             # Core functions for transcription and AI analysis
├── models.py               # Pydantic data model for validation
│
├── .env                    # For storing the Google API Key (Must be created)
└── README.md               # Project documentation (this file)

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
cd Task1

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
1. Navigate to the URL provided by Streamlit 
2. Click the "Browse files" button or drag and drop an audio file into the uploader.
3. Once the file is uploaded, an audio player will appear.
4. Click the "Process Audio File" button.
5. Wait for the application to finish transcribing and analyzing the audio. The progress will be indicated by spinners.
6. The final, structured EMR data will be displayed on the page in JSON format.


### The AI model is trained to understand doctor-patient conversations. It will not produce meaningful results for random audio clips. A sample audio file is available in the `sample_audio/` folder for testing.


