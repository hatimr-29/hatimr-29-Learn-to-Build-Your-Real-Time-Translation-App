# translator.py
from deep_translator import GoogleTranslator

def translate_to_english(text):
    if not text.strip():
        return "No English text detected."

    try:
        # English to English correction
        result = GoogleTranslator(source='auto', target='en').translate(text)
        return result
    except Exception as e:
        return f"Translation error: {e}"
