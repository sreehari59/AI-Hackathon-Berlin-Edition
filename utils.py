import whisper
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream
import os
load_dotenv()


def transcribe(path):

    model = whisper.load_model("base")
    result = model.transcribe()
    transcribed_text = result["text"]
    print("Transcribed:", transcribed_text)


def stt(ai_text):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    audio = client.text_to_speech.convert(
        text=ai_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)