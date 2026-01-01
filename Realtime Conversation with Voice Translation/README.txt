VoiceTranslator - Real-Time English ↔ Spanish Speech Translator
---------------------------------------------------------------

Description:
This project allows two people (one Spanish-speaking, one English-speaking)
to talk using real-time voice translation.

Model:
A custom ML-style Nearest-Neighbor translator is implemented.
It uses a small training dataset and bag-of-words vector similarity.

Flow:
1. Spanish speaker talks → speech to text → ML translation → English TTS
2. English speaker talks → speech to text → ML translation → Spanish TTS

Files:
- main.py               : Main conversation loop
- translator_model.py   : Nearest-neighbor ML model
- speech_utils.py       : Speech recognition + TTS
- training_data.py      : Parallel EN–ES training corpus
- README.txt            : Documentation

Dependencies:
pip install SpeechRecognition pyttsx3 pyaudio

Run:
python main.py

Notes:
- Accuracy does not matter (task requirement).
- Effort + real ML pipeline + real-time voice matters.
- You can expand training_data.py to improve model behavior.
