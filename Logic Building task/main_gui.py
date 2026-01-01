# main_gui.py
import tkinter as tk
from model import translate_word

# -------------------------
# GUI Function
# -------------------------
def handle_translation():
    word = entry.get().strip()
    result = translate_word(word)

    if result.startswith("ERROR"):
        output_label.config(text=result, fg="red")
    else:
        output_label.config(text=result, fg="green")


# -------------------------
# GUI Setup
# -------------------------
root = tk.Tk()
root.title("English → Hindi Translator (AI Logic Model)")
root.geometry("450x300")
root.config(bg="#F3F3F3")

title = tk.Label(root, text="English → Hindi Translator", font=("Arial", 18, "bold"), bg="#F3F3F3")
title.pack(pady=10)

input_label = tk.Label(root, text="Enter English Word:", font=("Arial", 12), bg="#F3F3F3")
input_label.pack()

entry = tk.Entry(root, font=("Arial", 14), width=25)
entry.pack(pady=5)

translate_btn = tk.Button(root, text="Translate", command=handle_translation,
                           font=("Arial", 12, "bold"), bg="#0066CC", fg="white", width=15)
translate_btn.pack(pady=15)

output_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#F3F3F3")
output_label.pack(pady=20)

root.mainloop()
