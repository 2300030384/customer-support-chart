
from fastapi import APIRouter, HTTPException
from app.services.chatbot_service import generate_chatbot_response

router = APIRouter(tags=["Chatbot"], prefix="/chatbot")

@router.post("/reply")
def chatbot_reply(payload: dict):
    # Accept both messages array and suggestion string
    messages = payload.get("messages", [])
    suggestion = payload.get("suggestion")
    try:
        if suggestion:
            # If suggestion is provided, use it as user message
            messages = messages + [{"role": "user", "content": suggestion}]
        if not messages:
            raise HTTPException(status_code=400, detail="No messages or suggestion provided")
        reply = generate_chatbot_response(messages)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
