from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
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
async def chat(req: ChatRequest):
    """
    Główny endpoint czatu z obsługą MCP tools

    Jeśli use_tools=True, model może wywoływać narzędzia używając składni:
    [TOOL:nazwa_narzędzia]argumenty[/TOOL]
    """
    try:
        db = SessionLocal()
        conv = Conversation()
        db.add(conv)
        db.commit()
        db.refresh(conv)

        # Zapisz wiadomości użytkownika
        for m in req.messages:
            db.add(Message(conversation_id=conv.id, role=m.get("role"), content=m.get("text")))
        db.commit()

        # Przygotuj prompt - jeśli tools enabled, dodaj instrukcję
        if req.use_tools:
            system_prompt = f"""Jesteś pomocnym AI asystentem z dostępem do narzędzi MCP.

Dostępne narzędzia:
{chr(10).join([f"- {t}: {mcp_registry.get_tool(t)['description']}" for t in mcp_registry.list_tools()])}

Aby użyć narzędzia, użyj składni: [TOOL:nazwa]argumenty[/TOOL]
Przykład: [TOOL:calculator]2+2[/TOOL]

Zawsze wyjaśnij użytkownikowi co robisz przed użyciem narzędzia."""

            prompt = f"{system_prompt}\n\n" + "\n".join([f"{m['role']}: {m['text']}" for m in req.messages])
        else:
            prompt = "\n".join([f"{m['role']}: {m['text']}" for m in req.messages])

        # Generuj odpowiedź
        out = model.generate(prompt, max_tokens=req.max_tokens)

        # Sprawdź czy są wywołania narzędzi
        tool_calls = []
        if req.use_tools:
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
            "tool_calls": tool_calls if tool_calls else []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)