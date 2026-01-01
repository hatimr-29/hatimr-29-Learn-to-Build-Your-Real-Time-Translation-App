# model.py
from datetime import datetime
from utils import starts_with_vowel

# --------------------------
# Custom Machine Learning Model (Dictionary-based)
# --------------------------
translation_model = {
    "cat": "बिल्ली",
    "dog": "कुत्ता",
    "house": "घर",
    "tree": "पेड़",
    "apple": "सेब",
    "elephant": "हाथी",
    "orange": "संतरा",
    "ink": "स्याही",
    "umbrella": "छाता"
}

def is_between_9_to_10_pm():
    return datetime.now().hour == 21   # 21 = 9 PM


# --------------------------
# Translation Logic (Core Model)
# --------------------------
def translate_word(word):
    word = word.lower().strip()
    
    # Validation
    if not word.isalpha():
        return "ERROR: Please enter a valid English word."

    vowel_word = starts_with_vowel(word)
    time_window = is_between_9_to_10_pm()

    # ---------- RULE 1: Outside 9 PM - 10 PM ----------
    if not time_window:
        if vowel_word:
            return "ERROR: This word starts with a vowel. Please provide another word."
        else:
            return translation_model.get(word, "Translation not found in ML model.")

    # ---------- RULE 2: Between 9 PM - 10 PM ----------
    else:
        if not vowel_word:
            return "ERROR: Word translation allowed only for vowel-starting words between 9 PM and 10 PM."
        else:
            return translation_model.get(word, "Translation not found in ML model.")
