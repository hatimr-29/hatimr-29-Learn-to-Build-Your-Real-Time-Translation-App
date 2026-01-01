TranslatorProject - English to Hindi Translator (Logic + ML Model)

Description:
This project translates English words into Hindi using a custom
machine-learning-style dictionary model and special logic rules.

Rules:
1. Outside 9 PM – 10 PM:
   - If the word starts with a vowel → show error
   - If the word starts with a consonant → translate normally

2. Between 9 PM – 10 PM:
   - Only vowel-starting words are allowed
   - Consonant words show an error

Files:
1. main_gui.py  → Tkinter GUI
2. model.py     → Custom ML model and rule logic
3. utils.py     → Helper functions
4. README.txt   → Documentation

How to Run:
1. Open terminal/cmd.
2. Navigate to the project folder:
       cd TranslatorProject
3. Run the GUI:
       python main_gui.py

Requirements:
- Python 3.x
- Tkinter (comes pre-installed in Python)

You can expand the dictionary inside model.py anytime.
