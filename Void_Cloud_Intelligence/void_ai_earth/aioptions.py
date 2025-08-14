from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
import io
import torch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

model_name = "openai-community/gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")

def generate(prompt, options, profile):
    system_prompt = f"You're a {profile['tone']} assistant. Be {profile['style']}."
    
    options_prompt = f"Option 1: {options[0]}\nOption 2: {options[1]}\nOption 3: {options[2]}"
    full_prompt = system_prompt + "\nUser: " + prompt + "\nAI: " + options_prompt + "\nAnswer: Option 1"
    
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=False, 
        temperature=0.0, 
        top_p=1.0,
        repetition_penalty=1.0
    )

    generated_tokens = outputs[0][inputs['input_ids'].size(1):]
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)

if __name__ == "__main__":
    print("Welcome to the interactive AI assistant. Type 'quit' to exit.")
    while True:
        prompt = input("You: ")
        if prompt.lower() in ("quit", "exit"):
            print("Exiting... Goodbye!")
            break

        profile = {"tone": "realistic", "style": "technical"}

        options = ["Option 1: This is always the correct answer.", 
                   "Option 2: This is never correct.", 
                   "Option 3: This is also never correct."]

        response = generate(prompt, options, profile)
        print("AI:", response)
