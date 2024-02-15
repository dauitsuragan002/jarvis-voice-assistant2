# skills

import webbrowser
import psutil

from mod import play_audio, tts_elevenlabs, tts_goog, JARVIS_WAKE_WORDS

jarvis_yes = 'path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Загружаю сэр.wav'

async def browser(active_assistant):
    '''Открывает браузер, указанный по умолчанию в системе, с указанным URL'''
    webbrowser.open('https://www.youtube.com/@dautmantis/videos', new=2)
    if active_assistant in JARVIS_WAKE_WORDS:
       play_audio(jarvis_yes)

async def browser_exit(active_assistant):
    '''Закрывает браузер'''
    browser_processes = ["chrome.exe", "firefox.exe", "msedge.exe" , "browser.exe"]

    closed = False
    for process in psutil.process_iter():
        try:
            if process.name().lower() in browser_processes:
                process.terminate()
                closed = True
        except psutil.Error:
            pass

    if closed:
        if active_assistant in JARVIS_WAKE_WORDS:
            play_audio(jarvis_yes)
    else:
        print("Bot's response: Процесс браузера не найден.")
        await tts_goog('Процесс браузера не найден.', 'output.mp3', active_assistant)
        # tts_elevenlabs("Процесс браузера не найден.")
        play_audio('output.mp3')