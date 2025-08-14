from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
import io
import torch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load fine-tuned model from local directory
model_path = "./fine_tuned_model"  # <- model name

try:
    print("Loading fine-tuned model...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cpu", torch_dtype=torch.bfloat16)
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred during model loading: {e}")
    sys.exit(1)

def generate(prompt, profile):
    system_prompt = f"You're a {profile['tone']} assistant. Be {profile['style']}."
    full_prompt = system_prompt + "\nUser: " + prompt + "\nAI:"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,  # It's a classifier, so don't need as many tokens anymore
        do_sample=False,    # Make output deterministic
        temperature=0.0,    # Lock it down for predictable responses
        top_p=1.0,
        repetition_penalty=1.0,
    )
    generated_tokens = outputs[0][inputs['input_ids'].size(1):]
    return tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

if __name__ == "__main__":
    print("Welcome to the AI classifier. Type 'quit' to exit.")
    while True:
        prompt = input("You: ")
        if prompt.lower() in ("quit", "exit"):
            print("Exiting... Goodbye!")
            break
        profile = {"tone": "realistic", "style": "technical"}
        response = generate(prompt, profile)
        print("AI:", response)
