import whisper

def transcribe_audio(file_path: str) ->str:
    model = whisper.load_model("base")

    result = model.transcribe(file_path)

    return result["text"]

if __name__ == '__main__':
    audiofile = "sample_audio/Basic Requests 1-Jane Wightwick & Mahmoud Gaafar.mp3"

    transcrib = transcribe_audio(audiofile)

    print(transcrib)