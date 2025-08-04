import os
import tempfile
from dotenv import load_dotenv
import streamlit as st
from pydantic import ValidationError

from services import transcribe_audio, extract_emr_data
from models import EMRData

load_dotenv()

st.set_page_config(
    page_title="Ambient Listening EMR Prototype",
    layout="centered"
)

st.title("Ambient Listening EMR Prototype")
st.write("Upload a doctor-patient consultation audio file. The system will transcribe the conversation and extract a structured clinical summary.")


uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=['mp3', 'wav', 'm4a', 'flac']
)

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Process Audio File"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            
            with st.spinner("Transcribing audio... This may take a moment."):
                transcript = transcribe_audio(tmp_path)

            if transcript:
                st.subheader("Generated Transcript")
                st.text_area("", transcript, height=150)

                with st.spinner("Analyzing transcript and extracting data..."):
                    emr_data_dict = extract_emr_data(transcript)

                if emr_data_dict:
                  
                    try:
                        validated_data = EMRData(**emr_data_dict)
                        st.subheader("Extracted EMR Data")
                        st.json(validated_data.model_dump())
                    except ValidationError as e:
                        st.error("Data Validation Error: The AI model returned data in an unexpected format.")
                        st.json(emr_data_dict) 
                        st.error(e)
                else:
                    st.error("Failed to extract EMR data from the transcript. The model may not have found relevant information.")
            else:
                st.error("Transcription failed. The audio file might be silent or in an unsupported format.")

        finally:
            os.unlink(tmp_path)
