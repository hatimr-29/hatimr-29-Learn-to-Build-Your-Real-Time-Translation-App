import tkinter as tk
from tkinter import messagebox

# Simple French → Tamil mini-dictionary (5-letter words only)
translation_dict = {
    "chien": "நாய்",
    "plage": "கடற்கரை",
    "pomme": "ஆப்பிள்",
    "fleur": "மலர்",
    "livre": "புத்தகம்",
    "arbre": "மரம்",
    "rouge": "சிவப்பு"
}

def translate_word():
    french_word = entry.get().strip().lower()

    # Check length condition
    if len(french_word) != 5:
        output_label.config(text="❗ Only 5-letter French words allowed.")
        return

    # Translate if available
    tamil_word = translation_dict.get(french_word)

    if tamil_word:
        output_label.config(text=f"தமிழ்: {tamil_word}")
    else:
        output_label.config(text="❗ Translation not found.")

# GUI window
root = tk.Tk()
root.title("French → Tamil Translator (5-letter only)")
root.geometry("400x250")
root.config(bg="#f0f0f0")

# Heading
heading = tk.Label(root, text="French → Tamil Translator", font=("Arial", 16), bg="#f0f0f0")
heading.pack(pady=10)

# Input section
input_label = tk.Label(root, text="Enter French word:", font=("Arial", 12), bg="#f0f0f0")
input_label.pack()

entry = tk.Entry(root, font=("Arial", 14), justify="center")
entry.pack(pady=5)

# Translate button
translate_btn = tk.Button(root, text="Translate", font=("Arial", 12), command=translate_word)
translate_btn.pack(pady=10)

# Output section
output_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0", fg="blue")
output_label.pack(pady=10)

root.mainloop()
