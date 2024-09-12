from fastapi import APIRouter, UploadFile, File, HTTPException
import aiofiles
import uuid
from backend.models.schemas import DocumentProcessResponse
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

router = APIRouter()

def generate_asset_id():
    return str(uuid.uuid4())

def create_embeddings(file_path: str, embedder):
    try:
        # Read the content of the file
        with open(file_path, 'r') as f:
            text = f.read()
        # Generate embeddings for the text
        embeddings = embedder.embed_documents([text])
        return text, embeddings  # Return both text and embeddings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating embeddings: {e}")

def store_embeddings(text, embeddings, metadata):
    try:
        # Initialize the embedding instance
        embedder = HuggingFaceEmbeddings()
        
        # Initialize Chroma with the embedding instance
        chroma_client = Chroma(embedding_function=embedder, collection_name="document_embeddings")
        
        # Wrap the embedding and metadata into a Document object
        document = Document(page_content=text, metadata=metadata)
        
        # Store the document
        chroma_client.add_documents(documents=[document])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing embeddings: {e}")

@router.post("/api/documents/process", response_model=DocumentProcessResponse)
async def process_document(file: UploadFile = File(...)):
    try:
        # Define the file path
        file_path = f'./{file.filename}'
        
        # Save the uploaded file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Create embeddings
        embedder = HuggingFaceEmbeddings()
        text, embeddings = create_embeddings(file_path, embedder)
        asset_id = generate_asset_id()
        metadata = {"filename": file.filename}
        
        # Store embeddings
        store_embeddings(text, embeddings, metadata)

        return {"asset_id": asset_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
