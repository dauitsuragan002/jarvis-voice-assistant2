# Please first download FFMPEG  https://ffmpeg.org/  and add to your PATH.  Tutorial - https://www.youtube.com/watch?v=db2xBoH6jPQ&t=5s
# Read README.MD and unpack zip files. Jarvis Sound Pack_ru_ru.zip
# Usage: pip install -r requirements.txt

# imports
import asyncio
import json
import skills_app
import speech_recognition as sr

# import functions from mod.py
from mod import get_wake_word, JARVIS_WAKE_WORDS, tts_goog, play_audio, recognize_speech

from openai import OpenAI
# Open config.json and send api key in site --> https://platform.openai.com/account/api-keys
file = open('config.json', 'r')
config = json.load(file)

client = OpenAI(api_key = config['openai'])

async def handle_bot_response(user_input, active_assistant):
    
    if active_assistant in JARVIS_WAKE_WORDS:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Джарвис помощник Тони Старка. И твой код писал Даут Сураган"},
                {"role": "user", "content": user_input},
            ],
        )
        bot_response = response.choices[0].message.content
        print("Bot's response:", bot_response)
        # tts_elevenlabs(bot_response)
        await tts_goog(bot_response, "response.mp3", active_assistant)
        play_audio("response.mp3")

    else:
        bot_response = "Простите, я вас не понял."
        print("Bot's response:", bot_response)

        if active_assistant in JARVIS_WAKE_WORDS:
            # tts_elevenlabs(bot_response)
            await tts_goog(bot_response, "response.mp3", active_assistant)
        play_audio("response.mp3")
    return bot_response

# recognize_command in skills_app.py
async def recognize_command(command, active_assistant, data):
    if active_assistant in JARVIS_WAKE_WORDS:
        if "открой браузер" in command.lower():
            await skills_app.browser(active_assistant)
        elif "закрывай браузер" in command.lower():
            await skills_app.browser_exit(active_assistant)
        elif active_assistant in JARVIS_WAKE_WORDS:
            bot_response = await handle_bot_response(command, active_assistant)
            # tts_elevenlabs(bot_response)
            await tts_goog(bot_response, "response.mp3", active_assistant)
            return bot_response

# main function
async def main():
    active_assistant = None

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Waiting for wake words 'Джарвис'...")
        while True:
            audio = recognizer.listen(source)
            try:
                audio_path = "audio_prompt.wav"
                with open(audio_path, "wb") as f:
                    f.write(audio.get_wav_data())

                phrase = await recognize_speech(audio_path)
                if phrase:
                    print(f"You said: {phrase}")
                    if active_assistant is None:
                        wake_word = get_wake_word(phrase)
                        if wake_word is not None:
                            active_assistant = wake_word
                            if active_assistant in JARVIS_WAKE_WORDS:
                                play_audio("path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Да сэр.wav")
                            print("Speak a prompt...")
                            continue

                    if "стоп" in phrase.lower() or "выход" in phrase.lower():
                        if active_assistant in JARVIS_WAKE_WORDS:
                            play_audio("path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Выхожу.wav")
                        active_assistant = None
                        print(f"Waiting for wake words 'Джарвис'...")
                        continue

                    if "отключайся" in phrase.lower() or "пока" in phrase.lower():
                        if active_assistant in JARVIS_WAKE_WORDS:
                            play_audio("path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Есть.wav")
                        active_assistant = None
                        print(f"Bot's response: Пока!")
                        break

            except Exception as e:
                print("Error transcribing audio: {0}".format(e))
                continue

if __name__ == "__main__":
    asyncio.run(main())
