from transformers import MarianMTModel, MarianTokenizer

def save_model(model_name, out_dir):
    print(f"Downloading {model_name} ...")
    tokenizer = MarianTokenizer.from_pretrained(model_name, use_fast=False)
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer.save_pretrained(out_dir)
    model.save_pretrained(out_dir)
    print(f"Saved {out_dir}")

if __name__ == '__main__':
    save_model('Helsinki-NLP/opus-mt-en-fr', 'dual_model_fr')
    save_model('Helsinki-NLP/opus-mt-en-hi', 'dual_model_hi')
