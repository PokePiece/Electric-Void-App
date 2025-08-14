from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch
import sys
import io
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv('HF_TOKEN')




# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Hugging Face login
login(token=hf_token)

# Model setup
model_name = "EleutherAI/pythia-160m"
try:
    print("Loading model with bfloat16 to save memory...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="cpu",
        torch_dtype=torch.bfloat16
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred during model loading: {e}")
    sys.exit(1)

# FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pythia Chat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    prompt: str
    tone: str = "realistic"
    style: str = "technical"

class ChatResponse(BaseModel):
    response: str

def generate(prompt: str, profile: dict) -> str:
    system_prompt = f"You're a {profile['tone']} assistant. Be {profile['style']}."
    full_prompt = system_prompt + "\nUser: " + prompt + "\nAI:"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,
        top_p=0.9,
        temperature=0.2,
        repetition_penalty=1.2,
    )
    generated_tokens = outputs[0][inputs['input_ids'].size(1):]
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        profile = {"tone": request.tone, "style": request.style}
        reply = generate(request.prompt, profile)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 