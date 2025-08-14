import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from fastapi import FastAPI, Request
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from typing import Optional
from prompts import void_general_prompt
#from noises import run_noises
import sys
from retrievememory import store_memory, retrieve_similar
from flask import Flask, request, jsonify

load_dotenv() 

SUPABASE_URL= os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.ai/v1/chat/completions"
LOG_FILE = "token_log.jsonl"

SCOMATON_PASSWORD = os.getenv("SCOMATON_PASSWORD")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",  # Dev server
],  # Or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, OPTIONS, etc.
    allow_headers=["*"],
    
)



class ChatInput(BaseModel):
    prompt: str
    max_tokens: int = 1000
    tag: str = "default"
    user_id: Optional[str] = None
    




#Implementing Supabase message fetching and saving

def save_message(tag: str, role: str, content: str, user_id: str = None):
    
    #assert user_id, "user_id must not be None or empty"
    
    timestamp = "now()"
    
    # Insert into conversations
    convo_data = {
        "tag": tag,
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "user_id": user_id,
    }
    if user_id:
        convo_data["user_id"] = user_id
    convo_response = supabase.table("conversations").insert(convo_data).execute()
    if convo_response.data is None:
        print(f"Failed to save to conversations: {convo_response}")

    # Insert into intelligence_entries
    entry_data = {
        "tags": [tag],
        "content_type": role,
        "content_text": content,
        "created_at": timestamp,
        "user_id": user_id,
    }
    if user_id:
        entry_data["user_id"] = user_id
    entry_response = supabase.table("intelligence_entries").insert(entry_data).execute()
    if entry_response.data is None:
        print(f"Failed to save to intelligence_entries: {entry_response}")

    return convo_response.data



def get_recent_messages(tag: str, user_id: str = None, limit: int = 10):
    query = supabase.table("conversations").select("*").eq("tag", tag).order("timestamp", desc=True).limit(limit)
    #query = supabase.table("intelligence_entries").select("*").eq("tags", tag).order("created_at", desc=True).limit(limit)
    if user_id:
        query = query.eq("user_id", user_id)

    response = query.execute()

    if response.data is None:
        print(f"Failed to fetch history: {response}")
        return []
    
    #print(list(reversed(response.data)))
    return list(reversed(response.data))  # oldest first



def handle_message(user_input):
    store_memory(user_input, user="user")
    relevant = retrieve_similar(user_input)
    print("Relevant past memories:", relevant)
    return "Void AGI has made a decision."




def summarize_messages(messages):
    summary = "Earlier: "
    for msg in messages:
        if msg["role"] == "user":
            summary += f"User asked about '{msg['content'][:30]}...', "
        elif msg["role"] == "assistant":
            summary += f"Assistant replied with '{msg['content'][:30]}...', "
    return {"role": "system", "content": summary.strip(", ")}



def core_ai_route(prompt: str, tag: str) -> str:
    if tag=='void_general':
        return 'void_general'
    else:
        return "void_general"


def call_void_general(prompt: str, max_tokens: int, user_id: str):
    return call_chat_model(void_general_prompt, prompt, max_tokens, "void_general", user_id)



# pass tag, user id
def call_chat_model(system_prompt: str, prompt: str, max_tokens: int, tag: str, user_id: str):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    history = get_recent_messages(tag, user_id, limit=10)  # get last 10 messages

    conversation_history = [{"role": "system", "content": system_prompt}]
    for msg in history:
        conversation_history.append({"role": msg["role"], "content": msg["content"]})
        #conversation_history.append({"content_type": msg["role"], "content_text": msg["content"]})
    
    # Add current user prompt
    conversation_history.append({"role": "user", "content": prompt})

    data = {
        "model": "meta-llama/Llama-3-70b-chat-hf",
        "messages": conversation_history,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    print("Sending to TogetherAI:", data)
    response = requests.post(TOGETHER_API_URL, headers=headers, json=data)

    if not response.ok:
        print("TogetherAI error:", response.status_code, response.text)
        raise HTTPException(status_code=500, detail=response.text)

    res_json = response.json()
    ai_response = res_json["choices"][0]["message"]["content"].strip()
    
    # Save current prompt and response
    save_message(tag, "user", prompt, user_id)
    save_message(tag, "assistant", ai_response, user_id)

    return ai_response, res_json.get("usage", {})






@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    # Store and retrieve memory
    store_memory(user_input)
    similar = retrieve_similar(user_input)

    return jsonify({
        "response": f"Void AGI has made a decision.",
        "memory": similar
    })

if __name__ == "__main__":
    app.run(port=5000)







@app.post("/oldchat")
def chat(input: ChatInput):
    print("💬 CHAT RECEIVED:", input)
    print("Prompt:", input.prompt)
    print("Max Tokens:", input.max_tokens)
    
    route = core_ai_route(input.prompt, input.tag)
    print(f"Routing decision: {route}")
    
    if route == "void_general":
        ai_response, usage = call_void_general(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")

        # Return response with usage data as before
        today_total = 1000
        daily_limit = 33000
        warning = None
        total_tokens = usage.get("total_tokens", 0)
        if today_total > daily_limit:
            warning = f"⚠️ You’ve used {today_total} tokens today — over your soft daily limit of {daily_limit}."

        return {
            "response": ai_response,
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": total_tokens,
                "daily_total": today_total,
                "warning": warning
            }
        }

    # Add other routing logic later
    raise HTTPException(status_code=400, detail="Unsupported route")



def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        # Just echo back for now
        print(f"Void AGI stub response to: {user_input}")
    else:
        print("No input provided.")

if __name__ == "__main__":
    main()





@app.get('/noisesauto')
def noises_auto():
   #run_noises()
    return {"status": "Selenium script executed"}








