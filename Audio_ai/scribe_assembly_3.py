import os
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv
import time

# Load environment variables
load_dotenv(find_dotenv())
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Set up AssemblyAI API key
aai.settings.api_key = ASSEMBLYAI_API_KEY

# URL of the video or audio file on the web
FILE_URL = "https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3"

# Set transcription configuration
config = aai.TranscriptionConfig(
    language_code="en",  # Set the language code for transcription
    speech_model=aai.SpeechModel.nano,  # Optional: Choose speech model (can be left out for default)
    speaker_labels=True,  # Speaker diarization
)

# Start transcription using the web URL
transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(FILE_URL)

# Poll for transcription completion
while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
    time.sleep(5)  # Wait for 5 seconds before checking status again
    transcript = transcriber.get_transcription(transcript.id)

# Check if transcription is complete or if there's an error
if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription error: {transcript.error}")
else:
    # Save the transcription to a file
    with open("data/transcription.txt", "w", encoding="utf-8") as file:
        for utterance in transcript.utterances:
            file.write(f"Speaker {utterance.speaker}: {utterance.text}\n")
    print("Transcription saved to data/transcription.txt")
