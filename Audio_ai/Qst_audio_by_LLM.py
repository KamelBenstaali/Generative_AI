import os
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv



# Load environment variables
load_dotenv(find_dotenv())
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Set up AssemblyAI API key
aai.settings.api_key = ASSEMBLYAI_API_KEY

transcriber = aai.Transcriber()

audio_url = "https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3"

transcript = transcriber.transcribe(audio_url)

prompt = "Provide a brief summary of the transcript."

result = transcript.lemur.task(
    prompt, final_model=aai.LemurModel.claude3_5_sonnet
)

print(result.response)