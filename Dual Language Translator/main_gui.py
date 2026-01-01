import tkinter as tk
from tkinter import messagebox
import threading

# Attempt to import transformers lazily (handle missing packages gracefully)
try:
    from transformers import MarianMTModel, MarianTokenizer
except Exception as e:
    MarianMTModel = None
    MarianTokenizer = None

MODEL_PATH_FR = "dual_model_fr"
MODEL_PATH_HI = "dual_model_hi"

models = {
    "en-fr": {"tokenizer": None, "model": None, "path": MODEL_PATH_FR},
    "fr-en": {"tokenizer": None, "model": None, "path": MODEL_PATH_FR},
    "en-hi": {"tokenizer": None, "model": None, "path": MODEL_PATH_HI},
    "hi-en": {"tokenizer": None, "model": None, "path": MODEL_PATH_HI},
}

def load_model(direction, use_fast=False):
    if MarianTokenizer is None:
        raise RuntimeError("transformers is not installed. Please install: pip install transformers sentencepiece")
    entry = models[direction]
    path = entry["path"]
    if entry["tokenizer"] is None or entry["model"] is None:
        # use use_fast=False for older Marian tokenizers
        tokenizer = MarianTokenizer.from_pretrained(path, use_fast=use_fast)
        model = MarianMTModel.from_pretrained(path)
        entry["tokenizer"] = tokenizer
        entry["model"] = model
    return entry["tokenizer"], entry["model"]

def translate_text(direction, text):
    # Simple length rule: translate only if length >= 10 letters (counting characters)
    if len(text) < 10:
        return None, "Upload Again"
    # For fr-en and hi-en we use same models but decoding will be symmetric (OPUS-MT en-fr is not identical reversed)
    if direction not in models:
        return None, "Direction not supported"
    try:
        tokenizer, model = load_model(direction)
    except Exception as e:
        return None, f"Model load error: {e}"
    # For fr-en and hi-en we still call generate on the model; OPUS-MT en-fr model expects English source -> French target.
    # If you need true reverse direction, you must download the reversed model (opus-mt-fr-en and opus-mt-hi-en).
    # Here, we assume the available folders contain the appropriate models for both directions (or that you added both).
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=256)
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated, None

# Threaded translation to avoid blocking UI
def do_translate():
    text = entry.get().strip()
    direction = direction_var.get()
    output_label.config(text="Translating...")
    def worker():
        translated, err = translate_text(direction, text)
        if err:
            output_label.config(text=err)
        else:
            output_label.config(text=f"Translated ({direction}):\n{translated}")
    threading.Thread(target=worker, daemon=True).start()

# Setup GUI
root = tk.Tk()
root.title("Dual Translator (en↔fr, en↔hi)")
root.geometry("600x400")

tk.Label(root, text="Enter English / French / Hindi text (minimum 10 characters to translate):", font=("Arial", 12)).pack(pady=8)
entry = tk.Entry(root, font=("Arial", 14), width=60)
entry.pack(pady=6)

direction_var = tk.StringVar(value="en-fr")
direction_frame = tk.Frame(root)
direction_frame.pack(pady=6)
tk.Radiobutton(direction_frame, text="en → fr", variable=direction_var, value="en-fr").pack(side="left", padx=6)
tk.Radiobutton(direction_frame, text="fr → en", variable=direction_var, value="fr-en").pack(side="left", padx=6)
tk.Radiobutton(direction_frame, text="en → hi", variable=direction_var, value="en-hi").pack(side="left", padx=6)
tk.Radiobutton(direction_frame, text="hi → en", variable=direction_var, value="hi-en").pack(side="left", padx=6)

translate_btn = tk.Button(root, text="Translate", command=do_translate, font=("Arial", 12))
translate_btn.pack(pady=10)

output_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", justify="left", wraplength=560)
output_label.pack(pady=10)

root.mainloop()
