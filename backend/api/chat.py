from fastapi import APIRouter, Query
from pydantic import BaseModel
import uuid
from typing import List, Dict
from backend.models.schemas import ChatStartResponse, ChatMessageResponse

router = APIRouter()

chat_history_store: Dict[str, List[Dict[str, str]]] = {}

def generate_chat_id():
    return str(uuid.uuid4())

async def get_rag_response(chat_thread_id: str, message: str):
    # Simulate RAG-based response here
    return f"Response from RAG for message: {message}"

class MessageRequest(BaseModel):
    message: str


class ChatHistoryResponse(BaseModel):
    chat_thread_id: str
    history: List[Dict[str, str]]

@router.post("/api/chat/start", response_model=ChatStartResponse)
def start_chat(asset_id: str):
    chat_id = generate_chat_id()
    # Initialize an empty history for the new chat thread
    chat_history_store[chat_id] = []
    return {"chat_thread_id": chat_id}

@router.post("/api/chat/message", response_model=ChatMessageResponse)
async def send_message(chat_thread_id: str, request: MessageRequest):
    message = request.message
    response = await get_rag_response(chat_thread_id, message)
     # Store the message in chat history
    if chat_thread_id not in chat_history_store:
        chat_history_store[chat_thread_id] = []
    
    chat_history_store[chat_thread_id].append({"message": message, "response": response})
    
    return {"response": response}


@router.get("/api/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(chat_thread_id: str):
    history = chat_history_store.get(chat_thread_id, [])
    return {"chat_thread_id": chat_thread_id, "history": history}