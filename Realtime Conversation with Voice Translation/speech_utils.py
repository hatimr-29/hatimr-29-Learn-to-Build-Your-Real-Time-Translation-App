# speech_utils.py
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")


def speak(text, lang="en"):
    lang = lang.lower()
    chosen_voice = None

    for v in voices:
        name = v.name.lower()
        vid = v.id.lower()
        if lang == "es" and ("spanish" in name or "es_" in vid):
            chosen_voice = v.id
            break
        if lang == "en" and ("english" in name or "en_" in vid):
            chosen_voice = v.id
            break

    if chosen_voice:
        engine.setProperty("voice", chosen_voice)

    engine.setProperty("rate", 160)
    engine.say(text)
    engine.runAndWait()


def listen(lang_code):
    with sr.Microphone() as source:
        print(f"[Listening for {lang_code}]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio, language=lang_code)
    except:
        return ""
