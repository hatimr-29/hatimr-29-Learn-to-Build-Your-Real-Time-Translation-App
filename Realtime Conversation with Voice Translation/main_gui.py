# main_gui.py
import tkinter as tk
from tkinter import messagebox

from translator_model import NearestNeighborTranslator
from speech_utils import listen, speak
from trainning_data import spanish_sentences, english_sentences

# Build ML models
es_to_en = NearestNeighborTranslator(spanish_sentences, english_sentences)
en_to_es = NearestNeighborTranslator(english_sentences, spanish_sentences)


def translate_from_spanish():
    text = listen("es-ES")
    if text:
        output = es_to_en.translate(text)
        spanish_input_var.set(text)
        english_output_var.set(output)
        speak(output, "en")
    else:
        messagebox.showerror("Error", "Could not recognize Spanish speech.")


def translate_from_english():
    text = listen("en-US")
    if text:
        output = en_to_es.translate(text)
        english_input_var.set(text)
        spanish_output_var.set(output)
        speak(output, "es")
    else:
        messagebox.showerror("Error", "Could not recognize English speech.")


root = tk.Tk()
root.title("Real-Time English ↔ Spanish Voice Translator")
root.geometry("600x450")
root.configure(bg="#f2f2f2")

# Variables for labels
spanish_input_var = tk.StringVar()
english_output_var = tk.StringVar()
english_input_var = tk.StringVar()
spanish_output_var = tk.StringVar()

title = tk.Label(root, text="Real-Time English ↔ Spanish Translator",
                 font=("Arial", 18, "bold"), bg="#f2f2f2")
title.pack(pady=20)

# Spanish to English
tk.Label(root, text="Spanish → English", font=("Arial", 14), bg="#f2f2f2").pack()
tk.Button(root, text="Speak Spanish", font=("Arial", 12),
          command=translate_from_spanish).pack(pady=5)
tk.Label(root, textvariable=spanish_input_var,
         font=("Arial", 12), bg="#f2f2f2").pack(pady=2)
tk.Label(root, textvariable=english_output_var,
         font=("Arial", 14, "bold"), fg="blue", bg="#f2f2f2").pack(pady=5)

# English to Spanish
tk.Label(root, text="English → Spanish", font=("Arial", 14), bg="#f2f2f2").pack(pady=15)
tk.Button(root, text="Speak English", font=("Arial", 12),
          command=translate_from_english).pack(pady=5)
tk.Label(root, textvariable=english_input_var,
         font=("Arial", 12), bg="#f2f2f2").pack(pady=2)
tk.Label(root, textvariable=spanish_output_var,
         font=("Arial", 14, "bold"), fg="green", bg="#f2f2f2").pack(pady=5)

root.mainloop()
