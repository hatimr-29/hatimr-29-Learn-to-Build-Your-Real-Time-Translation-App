DualTranslator - Template Project
=================================

What this contains:
- main_gui.py           : GUI application that supports English↔French and English↔Hindi translations.
- save_models.py        : helper to download and save models automatically (requires internet) - optional.
- train_model.py        : minimal placeholder for training/fine-tuning (not functional here).
- README.txt            : this file.
- dual_model_fr/        : folder where you must place the en-fr model files downloaded from HuggingFace.
- dual_model_hi/        : folder where you must place the en-hi model files downloaded from HuggingFace.

IMPORTANT - Download model files manually:
1) Go to https://huggingface.co/Helsinki-NLP/opus-mt-en-fr and download these files into 'dual_model_fr':
   - config.json
   - pytorch_model.bin
   - tokenizer_config.json
   - source.spm
   - target.spm
   - vocab.json (if present)
   - special_tokens_map.json (if present)

2) Go to https://huggingface.co/Helsinki-NLP/opus-mt-en-hi and download these files into 'dual_model_hi':
   - config.json
   - pytorch_model.bin
   - tokenizer_config.json
   - source.spm
   - target.spm
   - vocab.json (if present)

Place the downloaded files in the specified folders (copied exactly as downloaded).

How to run:
- Ensure Python 3.8+ is installed.
- Install required packages:
    pip install transformers sentencepiece torch

- Run:
    python main_gui.py

Notes:
- The GUI will try to load local folders 'dual_model_fr' and 'dual_model_hi'. If models are missing, the GUI will show an error.
- This template does NOT include the heavy model weight files to avoid large downloads inside this archive.
