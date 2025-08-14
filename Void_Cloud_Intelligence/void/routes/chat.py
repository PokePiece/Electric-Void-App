from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

chat_router = APIRouter()

class ChatInput(BaseModel):
    prompt: str
    max_tokens: int = 1000
    tag: str = "default"
    user_id: Optional[str] = None

@chat_router.post("/chat")
def chat(input: ChatInput):
    from main import os_ai_route, call_general_chatbot, call_webtrix_expert, call_webtrix_general, call_portfolio_general_chatbot, call_brain_interface, call_portfolio_accomplishments, call_portfolio_masterpiece, call_portfolio_skills, call_portfolio_reach, call_void_general
    print("💬 CHAT RECEIVED:", input)
    print("Prompt:", input.prompt)
    print("Max Tokens:", input.max_tokens)
    
    route = os_ai_route(input.prompt, input.tag)
    print(f"Routing decision: {route}")

    if route == "general_chatbot":
        ai_response = call_general_chatbot(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "portfolio_general_chatbot":
        ai_response = call_portfolio_general_chatbot(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "brain_interface":
        ai_response = call_brain_interface(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "portfolio_accomplishments":
        ai_response = call_portfolio_accomplishments(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "portfolio_masterpiece":
        ai_response = call_portfolio_masterpiece(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "portfolio_skills":
        ai_response = call_portfolio_skills(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "portfolio_reach":
        ai_response = call_portfolio_reach(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "void_general":
        ai_response = call_void_general(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "webtrix_general":
        ai_response = call_webtrix_general(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    elif route == "webtrix_expert":
        ai_response = call_webtrix_expert(input.prompt, input.max_tokens, input.user_id)
        print(f"INPUT USER_ID: {input.user_id!r}")
        return {"response": ai_response}
    else:
        return {"response": "Error: Unknown route."}

    raise HTTPException(status_code=400, detail="Unsupported route")