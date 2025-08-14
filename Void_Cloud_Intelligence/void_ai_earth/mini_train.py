# mini_train.py

from transformers import AutoTokenizer
from mini_dataset import dataset

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")
tokenizer.pad_token = tokenizer.eos_token  # Ensure compatibility

# Format + tokenize
def tokenize(example):
    prompt = f"Prompt: {example['input']}\nAnswer:"
    full_text = prompt + " " + example['label']
    encoding = tokenizer(full_text, truncation=True, padding="max_length", max_length=64)
    encoding["labels"] = encoding["input_ids"].copy()  # For causal LM training
    return encoding

# Tokenize dataset
tokenized_dataset = dataset.map(tokenize)
tokenized_dataset = tokenized_dataset.remove_columns(["input", "label"])

# Save for training
tokenized_dataset.save_to_disk("tokenized_dataset")
