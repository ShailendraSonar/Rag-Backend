from pydantic import BaseModel

class DocumentProcessResponse(BaseModel):
    asset_id: str

class ChatStartResponse(BaseModel):
    chat_thread_id: str

class ChatMessageResponse(BaseModel):
    response: str
