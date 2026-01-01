import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

import speech_recognition as sr 
from langdetect import detect, LangDetectException

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


# ========== 1. Simple ML Translator Model (Train Your Own) ==========

class SimpleKNNTranslator:
    """
    Very simple ML translation model:
    - Train on (English sentence -> Hindi sentence) examples.
    - Use TF-IDF + K-Nearest Neighbors to find the most similar
      English sentence in training data and return its Hindi translation.
    """

    def __init__(self):
        self.vectorizer = None
        self.nn_model = None
        self.hindi_sentences = None

    def fit(self, english_sentences, hindi_sentences):
        """Train the translator model."""
        if len(english_sentences) != len(hindi_sentences):
            raise ValueError("English and Hindi sentence lists must be same length.")

        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(english_sentences)

        self.nn_model = NearestNeighbors(n_neighbors=1, metric="cosine")
        self.nn_model.fit(X)

        self.hindi_sentences = hindi_sentences

    def translate(self, english_text):
        """Return the Hindi sentence closest to the given English text."""
        if self.vectorizer is None or self.nn_model is None:
            raise RuntimeError("Model not trained. Call fit() first.")

        X = self.vectorizer.transform([english_text])
        distances, indices = self.nn_model.kneighbors(X)
        idx = indices[0][0]
        return self.hindi_sentences[idx]


def build_and_train_translator():
    # --- Training data (you can expand this list or load from CSV) ---
    english_sentences = [
        "hello",
        "how are you",
        "what is your name",
        "good morning",
        "good night",
        "thank you",
        "where are you from",
        "what are you doing",
        "please help me",
        "i am fine",
        "good evening",
        "what time is it",
        "i am hungry",
        "i am thirsty",
        "see you tomorrow",
    ]

    hindi_sentences = [
        "नमस्ते",
        "आप कैसे हैं?",
        "आपका नाम क्या है?",
        "सुप्रभात",
        "शुभ रात्रि",
        "धन्यवाद",
        "आप कहाँ से हैं?",
        "आप क्या कर रहे हैं?",
        "कृपया मेरी मदद कीजिए",
        "मैं ठीक हूँ",
        "शुभ संध्या",
        "समय क्या हुआ है?",
        "मुझे भूख लगी है",
        "मुझे प्यास लगी है",
        "कल मिलते हैं",
    ]

    translator = SimpleKNNTranslator()
    translator.fit(english_sentences, hindi_sentences)
    return translator


# ========== 2. Time Window Logic ==========

ACTIVE_START = datetime.time(21, 30)  # 9:30 PM
ACTIVE_END = datetime.time(22, 0)     # 10:00 PM


def is_active_now():
    """Check if current local time is between 9:30 PM and 10:00 PM."""
    now = datetime.datetime.now().time()
    return ACTIVE_START <= now <= ACTIVE_END


# ========== 3. GUI Application ==========

class VoiceTranslatorApp:
    def __init__(self, root, translator_model):
        self.root = root
        self.root.title("Voice Translator: English Audio to Hindi Text")
        self.root.geometry("650x500")

        self.translator = translator_model

        # --- Title ---
        title_label = tk.Label(
            root,
            text="Voice Translator (English Audio → Hindi Text)",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        # --- Time Window Info ---
        self.time_label = tk.Label(
            root,
            text="Active time: 9:30 PM to 10:00 PM",
            font=("Arial", 10)
        )
        self.time_label.pack()

        # --- Status / Messages Label ---
        self.status_label = tk.Label(
            root,
            text="Click 'Start Listening' and speak in English.",
            font=("Arial", 10),
            fg="blue"
        )
        self.status_label.pack(pady=5)

        # --- Button to start listening ---
        self.listen_button = tk.Button(
            root,
            text="Start Listening",
            font=("Arial", 12, "bold"),
            command=self.start_listening
        )
        self.listen_button.pack(pady=10)

        # --- Recognized English text box ---
        eng_frame = tk.Frame(root)
        eng_frame.pack(fill="both", expand=True, padx=10, pady=5)

        eng_label = tk.Label(eng_frame, text="Recognized English:", font=("Arial", 10, "bold"))
        eng_label.pack(anchor="w")

        self.eng_text = scrolledtext.ScrolledText(eng_frame, height=5, wrap=tk.WORD, font=("Arial", 10))
        self.eng_text.pack(fill="both", expand=True)

        # --- Translated Hindi text box ---
        hin_frame = tk.Frame(root)
        hin_frame.pack(fill="both", expand=True, padx=10, pady=5)

        hin_label = tk.Label(hin_frame, text="Translated Hindi:", font=("Arial", 10, "bold"))
        hin_label.pack(anchor="w")

        self.hin_text = scrolledtext.ScrolledText(hin_frame, height=5, wrap=tk.WORD, font=("Arial", 10))
        self.hin_text.pack(fill="both", expand=True)

        # --- Footer / Note ---
        note_label = tk.Label(
            root,
            text="Note: Works only with English audio. If unclear, you will be asked to repeat.",
            font=("Arial", 9),
            fg="gray"
        )
        note_label.pack(pady=5)

    def start_listening(self):
        """Handle the button click: check time, then listen and translate."""
        # 1. Time window check
        if not is_active_now():
            self.status_label.config(
                text="Taking rest, see you tomorrow!",
                fg="red"
            )
            messagebox.showinfo("Info", "Taking rest, see you tomorrow!")
            return

        # 2. Clear previous texts
        self.eng_text.delete(1.0, tk.END)
        self.hin_text.delete(1.0, tk.END)

        self.status_label.config(text="Listening... Please speak in English.", fg="green")
        self.root.update_idletasks()

        # 3. Record audio using microphone
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=7)

            # 4. Recognize speech (English)
            try:
                english_text = recognizer.recognize_google(audio_data, language="en-IN")
            except sr.UnknownValueError:
                self.status_label.config(
                    text="I didn’t catch that. Please repeat clearly in English.",
                    fg="red"
                )
                messagebox.showwarning(
                    "Repeat",
                    "I didn’t catch that. Please repeat clearly in English."
                )
                return
            except sr.RequestError as e:
                self.status_label.config(
                    text="Speech recognition service error.",
                    fg="red"
                )
                messagebox.showerror(
                    "Error",
                    f"Speech recognition service error: {e}"
                )
                return

        except sr.WaitTimeoutError:
            self.status_label.config(
                text="No speech detected. Please try again.",
                fg="red"
            )
            messagebox.showwarning(
                "Timeout",
                "No speech detected. Please try again."
            )
            return
        except OSError as e:
            self.status_label.config(
                text="Microphone error.",
                fg="red"
            )
            messagebox.showerror(
                "Error",
                f"Microphone error: {e}"
            )
            return

        # 5. Show recognized English text
        english_text = english_text.strip()
        self.eng_text.insert(tk.END, english_text)

        # 6. Check language (only English allowed)
        try:
            # langdetect can fail on very short text
            if len(english_text.split()) >= 2:
                detected_lang = detect(english_text)
            else:
                detected_lang = "en"
        except LangDetectException:
            detected_lang = "unknown"

        if detected_lang != "en":
            self.status_label.config(
                text="Please speak in English. This translator works only with English audio.",
                fg="red"
            )
            messagebox.showwarning(
                "Language",
                "Please speak in English. This translator works only with English audio."
            )
            return

        # 7. Translate English -> Hindi using your ML model
        try:
            hindi_text = self.translator.translate(english_text)
        except Exception as e:
            self.status_label.config(
                text="Translation failed. Check model.",
                fg="red"
            )
            messagebox.showerror(
                "Translation Error",
                f"Translation failed: {e}"
            )
            return

        # 8. Display Hindi translation
        self.hin_text.insert(tk.END, hindi_text)
        self.status_label.config(
            text="Translation completed.",
            fg="blue"
        )


# ========== 4. Run the App ==========

if __name__ == "__main__":
    # Train your ML translation model once at startup
    translator_model = build_and_train_translator()

    root = tk.Tk()
    app = VoiceTranslatorApp(root, translator_model)
    root.mainloop()
