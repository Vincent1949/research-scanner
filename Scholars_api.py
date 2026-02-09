"""
Scholar's Terminal - Backend API
Bridges React frontend with ChromaDB knowledge base, Ollama, and Research Scanner
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager
import chromadb
from chromadb.config import Settings
import httpx
import asyncio
import sys
import os
from pathlib import Path

# Add research_scanner to Python path
sys.path.insert(0, str(Path(__file__).parent / "research_scanner"))

# Import Research Scanner
from research_scanner.api_routes import create_research_router
from research_scanner.review_routes import create_review_router
from research_scanner.scheduler import start_scheduler

# Configuration
CHROMA_DB_PATH = r"D:\Claude\Projects\scholars-terminal\data\vector_db"
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"

# ============================================================
# Lifespan Event Handler
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=" * 60)
    print("Scholar's Terminal API v2.0 Starting...")
    print("=" * 60)
    print(f"Ollama: {OLLAMA_URL}")
    print(f"ChromaDB: {CHROMA_DB_PATH}")
    print(f"Research Scanner: Enabled")
    print("=" * 60)
    
    yield
    
    # Shutdown
    print("\nShutting down Scholar's Terminal API...")

# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(title="Scholar's Terminal API", version="2.0.0", lifespan=lifespan)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB client
try:
    chroma_client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH,
        settings=Settings(anonymized_telemetry=False)
    )
    print(f"[OK] Connected to ChromaDB at {CHROMA_DB_PATH}")
    
    # List available collections
    collections = chroma_client.list_collections()
    print(f"[INFO] Available collections: {[c.name for c in collections]}")
except Exception as e:
    print(f"[ERROR] Failed to connect to ChromaDB: {e}")
    chroma_client = None


# ============================================================
# Request/Response Models
# ============================================================

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = DEFAULT_MODEL
    messages: List[ChatMessage]
    use_knowledge_base: bool = True
    num_results: int = 5
    source_filter: Optional[str] = None  # "books", "github", "research", or None for all

class Citation(BaseModel):
    title: str
    author: Optional[str] = "Unknown"
    source: str  # "books", "github", or "research"
    page: Optional[str] = None
    relevance: float
    content: str

class ChatResponse(BaseModel):
    message: ChatMessage
    citations: Optional[List[Citation]] = None
    model: str


# ============================================================
# Collection Management
# ============================================================

def get_collection(collection_name: Optional[str] = None):
    """Get the knowledge base collection"""
    if not chroma_client:
        return None
    
    # If specific collection requested
    if collection_name:
        try:
            collection = chroma_client.get_collection(name=collection_name)
            print(f"[INFO] Using collection: {collection_name} ({collection.count()} documents)")
            return collection
        except Exception as e:
            print(f"[WARN] Collection '{collection_name}' not found: {e}")
            return None
    
    # Try common collection names
    collection_names = ["knowledge_base", "books", "documents", "default"]
    
    for name in collection_names:
        try:
            collection = chroma_client.get_collection(name=name)
            print(f"[INFO] Using collection: {name} ({collection.count()} documents)")
            return collection
        except:
            continue
    
    # If no named collection, try to get the first available
    collections = chroma_client.list_collections()
    if collections:
        collection = collections[0]
        print(f"[INFO] Using first available collection: {collection.name}")
        return collection
    
    return None


def search_knowledge_base(
    query: str, 
    n_results: int = 5,
    source_filter: Optional[str] = None
) -> List[Citation]:
    """Search ChromaDB for relevant documents with optional source filtering"""
    collection = get_collection()
    if not collection:
        return []
    
    try:
        # Build where filter for source type
        where_filter = None
        if source_filter:
            where_filter = {"source_type": source_filter}
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        citations = []
        if results and results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                distance = results['distances'][0][i] if results['distances'] else 0.5
                
                # Determine source type
                source = metadata.get('source_type', 'unknown')
                if not source or source == 'unknown':
                    # Fallback: guess from metadata
                    if metadata.get('file_path', '').startswith('D:\\Books'):
                        source = 'books'
                    elif metadata.get('file_path', '').startswith('D:\\GitHub'):
                        source = 'github'
                    else:
                        source = 'documents'
                
                citations.append(Citation(
                    title=metadata.get('title', metadata.get('filename', 'Untitled')),
                    author=metadata.get('author', metadata.get('authors', 'Unknown')),
                    source=source,
                    page=metadata.get('page'),
                    relevance=1.0 - distance,  # Convert distance to similarity
                    content=doc[:300] + "..." if len(doc) > 300 else doc
                ))
        
        return citations
    except Exception as e:
        print(f"[ERROR] Search error: {e}")
        return []


async def chat_with_ollama(messages: List[dict], model: str) -> str:
    """Send messages to Ollama and get response"""
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()['message']['content']
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")


# ============================================================
# API Routes
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "Scholar's Terminal API",
        "version": "2.0.0",
        "status": "running",
        "features": ["chat", "knowledge_base", "research_scanner"],
        "collections": [c.name for c in (chroma_client.list_collections() if chroma_client else [])]
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with RAG support"""
    
    # Get citations if knowledge base is enabled
    citations = None
    if request.use_knowledge_base:
        user_message = next((m.content for m in request.messages if m.role == "user"), None)
        if user_message:
            citations = search_knowledge_base(
                user_message, 
                n_results=request.num_results,
                source_filter=request.source_filter
            )
    
    # Build context from citations
    context = ""
    if citations:
        context = "\n\nRelevant context from knowledge base:\n"
        for i, cite in enumerate(citations, 1):
            context += f"\n[{i}] From {cite.source}: {cite.title}\n{cite.content}\n"
    
    # Prepare messages for Ollama
    messages = []
    for msg in request.messages:
        content = msg.content
        # Add context to the last user message
        if msg.role == "user" and msg == request.messages[-1] and context:
            content = content + context
        
        messages.append({
            "role": msg.role,
            "content": content
        })
    
    # Get response from Ollama
    response_text = await chat_with_ollama(messages, request.model)
    
    return ChatResponse(
        message=ChatMessage(role="assistant", content=response_text),
        citations=citations,
        model=request.model
    )


@app.get("/api/collections")
async def list_collections():
    """List all available ChromaDB collections"""
    if not chroma_client:
        return {"collections": []}
    
    collections = chroma_client.list_collections()
    return {
        "collections": [
            {
                "name": c.name,
                "count": c.count()
            }
            for c in collections
        ]
    }


@app.get("/api/models")
async def list_models():
    """List available Ollama models"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    ollama_status = "unknown"
    chromadb_status = "unknown"
    
    # Check Ollama
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.get(f"{OLLAMA_URL}/api/tags")
            ollama_status = "healthy"
    except:
        ollama_status = "unhealthy"
    
    # Check ChromaDB
    try:
        if chroma_client:
            chroma_client.list_collections()
            chromadb_status = "healthy"
        else:
            chromadb_status = "not connected"
    except:
        chromadb_status = "unhealthy"
    
    return {
        "status": "healthy" if ollama_status == "healthy" and chromadb_status == "healthy" else "degraded",
        "ollama": ollama_status,
        "chromadb": chromadb_status
    }


# ============================================================
# Research Scanner Integration
# ============================================================

# Mount Research Scanner routes
app.include_router(create_research_router(), prefix="/api/research", tags=["research"])

# Mount Review System routes
app.include_router(create_review_router(), prefix="/api/review", tags=["review"])

# Optionally start the background scheduler
# Uncomment to enable automatic daily scans at 3 AM
# scheduler = start_scheduler()


# ============================================================
# Port Management - Find Available Port
# ============================================================

def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            # Try to bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            # Port is in use, try next one
            continue
    
    # No available port found
    raise RuntimeError(f"No available ports found in range {start_port}-{start_port + max_attempts - 1}")


# ============================================================
# Main Entry Point
# ============================================================

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Scholar's Terminal API Server")
    parser.add_argument("--port", type=int, default=None, help="Port to run on (default: auto-detect starting from 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    args = parser.parse_args()
    
    # Determine port
    if args.port:
        # User specified a port
        port = args.port
        print(f"\n[PORT] Using user-specified port: {port}", flush=True)
    else:
        # Auto-detect available port
        try:
            port = find_available_port(start_port=8000, max_attempts=10)
            if port != 8000:
                print(f"\n[WARNING] Port 8000 is in use", flush=True)
                print(f"[OK] Found available port: {port}", flush=True)
            else:
                print(f"\n[OK] Using default port: {port}", flush=True)
        except RuntimeError as e:
            print(f"\n[ERROR] {e}", flush=True)
            print("[TIP] Try specifying a custom port: python Scholars_api.py --port 8080", flush=True)
            sys.exit(1)
    
    # Print startup info
    print("\n" + "=" * 60, flush=True)
    print("Scholar's Terminal API Starting...", flush=True)
    print("=" * 60, flush=True)
    print(f"Server: http://localhost:{port}", flush=True)
    print(f"API Docs: http://localhost:{port}/docs", flush=True)
    print(f"Health Check: http://localhost:{port}/health", flush=True)
    print("=" * 60, flush=True)
    print("\nPress Ctrl+C to stop the server\n", flush=True)
    
    try:
        uvicorn.run(app, host=args.host, port=port)
    except Exception as e:
        print(f"\n[ERROR] Server failed to start: {e}")
        print("[TIP] Common issues:")
        print(f"      - Port {port} might still be in use")
        print("      - Try: python Scholars_api.py --port 8080")
        sys.exit(1)
