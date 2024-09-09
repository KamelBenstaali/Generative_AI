import os
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv
import time

#This feature fropm assembly.Ai is only available in paid-only and requires you to add a credit card.

# Load environment variables
load_dotenv(find_dotenv())
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Set up AssemblyAI API key
aai.settings.api_key = ASSEMBLYAI_API_KEY


def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)


def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")


def on_error(error: aai.RealtimeError):
    print("An error occured:", error)


def on_close():
    print("Closing Session")


transcriber = aai.RealtimeTranscriber(
    sample_rate=16_000,
    on_data=on_data,
    on_error=on_error,
    on_open=on_open,
    on_close=on_close,
)

transcriber.connect()

microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
transcriber.stream(microphone_stream)

transcriber.close()