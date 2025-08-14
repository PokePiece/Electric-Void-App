from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import torch.nn as nn
from torch.nn import Transformer
from datasets import load_dataset
from torch.optim import AdamW
from torch.utils.data import DataLoader

dataset = load_dataset("wikitext", "wikitext-2-raw-v1")


# Load GPT-2
model_name = "gpt2"  # "gpt2-medium", "gpt2-large", "gpt2-xl"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


class SimpleTransformer(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_layers):
        super(SimpleTransformer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer = Transformer(d_model=d_model, nhead=nhead, num_layers=num_layers)
        self.fc_out = nn.Linear(d_model, vocab_size)

    def forward(self, src, tgt):
        src = self.embedding(src)
        tgt = self.embedding(tgt)
        output = self.transformer(src, tgt)
        output = self.fc_out(output)
        return output

def tokenize_function(examples):
    return tokenizer(examples["text"], return_tensors="pt", truncation=True, padding="max_length", max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Hyperparameters
batch_size = 4
learning_rate = 5e-5
epochs = 3

optimizer = AdamW(model.parameters(), lr=learning_rate)

# DataLoader for training
train_dataloader = DataLoader(tokenized_datasets["train"], batch_size=batch_size, shuffle=True)

model.train()
for epoch in range(epochs):
    for batch in train_dataloader:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(model.device)
        attention_mask = batch["attention_mask"].to(model.device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")
        
def generate_text(prompt, model, tokenizer, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(input_ids=inputs["input_ids"], max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

prompt = "Once upon a time, in a distant land,"
print(generate_text(prompt, model, tokenizer))
