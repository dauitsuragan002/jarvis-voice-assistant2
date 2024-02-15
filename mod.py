# Module functions
import re
import pydub
from pydub import playback
import speech_recognition as sr
from gtts import gTTS
from elevenlabs import generate, play

JARVIS_WAKE_WORDS = ["Джарвис", "Ты здесь"]

def get_wake_word(phrase):
    for wake_word in JARVIS_WAKE_WORDS:
        if wake_word.lower() in phrase.lower():
            return wake_word
    return None

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

async def recognize_speech(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

# Text-To-Speach with GoogleTTS
async def tts_goog(text, output_file, active_assistant):
    text = re.sub(r"[\U0001F3A8\U0001F60A\U0001F44B\U0001F64F]+", "", text)
    if text.strip():
        tts = gTTS(text=text, lang="ru")
        tts.save(output_file)

# Text-To-Speach with elevenlabs
def tts_elevenlabs(text):
    # Call generate with streaming enabled
    audio_stream = generate(
        text=text, 
        voice="Michael",
        model='eleven_multilingual_v2',)
    
    # Stream the generated audio
    
    play(audio_stream)