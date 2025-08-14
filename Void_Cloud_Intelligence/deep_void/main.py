import os
import json
import queue
import threading
import time
import asyncio
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from dotenv import load_dotenv

from core_intelligence import life, action, prime_directive
s
load_dotenv() 

life_output_queue = queue.Queue()
life_thread: Optional[threading.Thread] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the FastAPI application.
    This is where we'll start our long-running 'life' process.
    """
    global life_thread
    print("FastAPI server starting up...")

    life_thread = threading.Thread(target=life, kwargs={'output_queue': life_output_queue})
    life_thread.daemon = True 
    life_thread.start()
    
    print("Background 'life' thread started.")
    
    yield 

    print("FastAPI server shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "https://void.dilloncarey.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/life_stream")
async def life_stream():
    """
    An SSE endpoint that streams output from the background 'life' process.
    """
    async def event_generator():
        while True:
            try:
                item = life_output_queue.get(timeout=1)
                yield f"data: {json.dumps(item)}\n\n"
                
                if item.get("type") == "death":
                    print("Death message sent, closing SSE stream.")
                    break
            except queue.Empty:
                yield ":keep-alive\n\n"
            except Exception as e:
                print(f"Error in SSE event_generator: {e}")
                yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/interact")
async def interact_with_ai(prompt: dict):
    """
    Allows a client to send a command or prompt to the AI.
    """
    user_input = prompt.get("text")
    if not user_input:
        raise HTTPException(status_code=400, detail="Prompt text is required.")

    response = action(user_input)
    return {"response": response}