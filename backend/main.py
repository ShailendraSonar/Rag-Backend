from fastapi import FastAPI
from backend.api import document, chat

app = FastAPI()

# Include routers for document processing and chat APIs
app.include_router(document.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Processing and RAG Chatbot Service! Shailendra Sonar"}
