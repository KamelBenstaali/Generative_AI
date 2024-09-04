# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.
import os
import assemblyai as aai

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Replace with your API key
aai.settings.api_key = ASSEMBLYAI_API_KEY

# URL of the file to transcribe
FILE_URL = "./data/Getting Started with LangChain and OpenAI.mp4"
# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

config = aai.TranscriptionConfig(
    language_code="fr",
    speech_model=aai.SpeechModel.nano,
    speaker_labels=True,
)

transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
    #print(transcript.text)
