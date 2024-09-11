import os
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv


# Load environment variables
load_dotenv(find_dotenv())

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Replace with your API key
aai.settings.api_key = ASSEMBLYAI_API_KEY

# URL of the file to transcribe
FILE_URL = "./data/fontaine.mp3"
# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

# Set transcription configuration
config = aai.TranscriptionConfig(
    language_code="fr",
    speech_model=aai.SpeechModel.nano,
    speaker_labels=True,
)

# Start transcription using the web URL
transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(FILE_URL)

# Check if transcription is complete or if there's an error
if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    # Save the transcription to a file
    with open("data/transcription.txt", "w", encoding="utf-8") as file:
        for utterance in transcript.utterances:
            file.write(f"Speaker {utterance.speaker}: {utterance.text}\n")
    print("Transcription saved to transcription.txt")
