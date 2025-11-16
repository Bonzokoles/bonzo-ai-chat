from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import json
import shutil
from model import LocalModel
from db import SessionLocal, init_db, Conversation, Message
from mcp_tools import mcp_registry, parse_tool_call_from_text
from typing import List, Optional

# Inicjalizacja
app = FastAPI(title="Local AI Chat")

# CORS Configuration - umożliwia połączenia z frontendu
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # W produkcji ustaw konkretne domeny
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = LocalModel()  # ładuje model raz przy starcie
init_db()

class ChatRequest(BaseModel):
    messages: List[dict]  # [{role: "user"|'assistant'|'system', text: "..."}]
    max_tokens: int = 512
    use_tools: bool = True  # Czy używać MCP tools

@app.get("/api/health")
async def health_check():
    """Health check endpoint - sprawdza czy backend działa"""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "database": "connected",
        "mcp_tools": len(mcp_registry.list_tools()),
        "available_tools": mcp_registry.list_tools()
    }

@app.get("/api/tools")
async def list_tools():
    """Lista dostępnych narzędzi MCP"""
    tools_info = []
    for tool_name in mcp_registry.list_tools():
        tool = mcp_registry.get_tool(tool_name)
        tools_info.append({
            "name": tool["name"],
            "description": tool["description"]
        })
    return {"tools": tools_info}

@app.post("/api/chat")
async def chat(
    messages: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    req: Optional[ChatRequest] = None
):
    """
    Główny endpoint czatu z obsługą MCP tools i file uploads

    Obsługuje dwa formaty:
    1. JSON (bez plików): {"messages": [...], "use_tools": true}
    2. FormData (z plikami): messages (JSON string) + files (multipart)
    """
    db = None
    try:
        # Określ format requesta
        uploaded_files_info = []

        if messages is not None:
            # FormData format (z plikami)
            parsed_messages = json.loads(messages)
            use_tools = True
            max_tokens = 512

            # Przetwórz uploadowane pliki
            if files:
                upload_dir = os.getenv("MCP_SAFE_DIR", "./mcp_workspace") + "/uploads"
                os.makedirs(upload_dir, exist_ok=True)

                for file in files:
                    file_path = os.path.join(upload_dir, file.filename)
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    uploaded_files_info.append({
                        "filename": file.filename,
                        "path": file_path,
                        "size": os.path.getsize(file_path)
                    })

                # Dodaj info o plikach do prompt
                files_info_text = "\n\n📎 Załączone pliki:\n" + "\n".join([
                    f"- {f['filename']} ({f['size']} bytes) zapisany w {f['path']}"
                    for f in uploaded_files_info
                ])
                # Dodaj do ostatniej wiadomości
                if parsed_messages:
                    parsed_messages[-1]["text"] += files_info_text

            request_messages = parsed_messages
        else:
            # JSON format (bez plików)
            if req is None:
                raise HTTPException(status_code=400, detail="Missing request body")
            request_messages = req.messages
            use_tools = req.use_tools
            max_tokens = req.max_tokens

        db = SessionLocal()
        conv = Conversation()
        db.add(conv)
        db.commit()
        db.refresh(conv)

        # Zapisz wiadomości użytkownika
        for m in request_messages:
            db.add(Message(conversation_id=conv.id, role=m.get("role"), content=m.get("text")))
        db.commit()

        # Przygotuj prompt - jeśli tools enabled, dodaj instrukcję
        if use_tools:
            system_prompt = f"""Jesteś pomocnym AI asystentem z dostępem do narzędzi MCP.

Dostępne narzędzia:
{chr(10).join([f"- {t}: {mcp_registry.get_tool(t)['description']}" for t in mcp_registry.list_tools()])}

Aby użyć narzędzia, użyj składni: [TOOL:nazwa]argumenty[/TOOL]
Przykład: [TOOL:calculator]2+2[/TOOL]

Zawsze wyjaśnij użytkownikowi co robisz przed użyciem narzędzia."""

            prompt = f"{system_prompt}\n\n" + "\n".join([f"{m['role']}: {m['text']}" for m in request_messages])
        else:
            prompt = "\n".join([f"{m['role']}: {m['text']}" for m in request_messages])

        # Generuj odpowiedź
        out = model.generate(prompt, max_tokens=max_tokens)

        # Sprawdź czy są wywołania narzędzi
        tool_calls = []
        if use_tools:
            tool_calls_parsed = parse_tool_call_from_text(out)

            for tc in tool_calls_parsed:
                result = mcp_registry.execute_tool(tc["tool"], **tc["args"])
                tool_calls.append({
                    "tool": tc["tool"],
                    "args": tc["args"],
                    "result": result
                })

            # Jeśli były wywołania narzędzi, dodaj ich wyniki do odpowiedzi
            if tool_calls:
                tools_summary = "\n\n🔧 Użyte narzędzia:\n" + "\n".join([
                    f"- {tc['tool']}: {tc['result']}" for tc in tool_calls
                ])
                out = out + tools_summary

        # Zapisz odpowiedź asystenta
        db.add(Message(conversation_id=conv.id, role="assistant", content=out))
        db.commit()

        return {
            "text": out,
            "tool_calls": tool_calls if tool_calls else [],
            "uploaded_files": uploaded_files_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)