import React, { useState, useEffect, useRef } from "react";

/**
 * Minimalny Reactowy widget czatu do użycia w Astro.
 * Komunikuje się z backendem FastAPI (endpoint /api/chat or /api/stream).
 * Nie używa żadnych zewnętrznych API.
 */

export default function ChatWidget({ apiBaseUrl = "/api" }) {
  const [messages, setMessages] = useState([
    { id: 0, role: "system", text: "Witaj! Jestem lokalnym chatbotem z MCP tools." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState("unknown"); // unknown, connected, error
  const controllerRef = useRef(null);

  // Sprawdź połączenie z backendem przy starcie
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const res = await fetch(`${apiBaseUrl}/health`, { method: "GET" });
        if (res.ok) {
          setConnectionStatus("connected");
        } else {
          setConnectionStatus("error");
        }
      } catch (err) {
        setConnectionStatus("error");
        console.error("Backend connection error:", err);
      }
    };
    checkConnection();
  }, [apiBaseUrl]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { id: Date.now(), role: "user", text: input.trim() };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${apiBaseUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: [...messages, userMsg] }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Backend error (${res.status}): ${errorText}`);
      }

      const data = await res.json();

      // Obsługa odpowiedzi z tool calls (MCP)
      if (data.tool_calls && data.tool_calls.length > 0) {
        const toolMsg = {
          id: Date.now() + 1,
          role: "tool",
          text: "🔧 Użyte narzędzia:\n" + data.tool_calls.map(tc => `- ${tc.tool}: ${tc.result}`).join("\n")
        };
        setMessages((m) => [...m, toolMsg]);
      }

      const botMsg = { id: Date.now() + 2, role: "assistant", text: data.text };
      setMessages((m) => [...m, botMsg]);
      setConnectionStatus("connected");
    } catch (err) {
      setConnectionStatus("error");
      const errMsg = {
        id: Date.now(),
        role: "error",
        text: `❌ Błąd połączenia:\n${err.message}\n\nSprawdź czy backend działa na: ${apiBaseUrl}`
      };
      setMessages((m) => [...m, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Opcjonalnie: obsługa klawisza Enter
  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Status connection indicator colors
  const statusColors = {
    connected: "#4CAF50",
    error: "#f44336",
    unknown: "#FF9800"
  };

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, width: 400, maxWidth: "100%" }}>
      {/* Connection Status */}
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: 8,
        marginBottom: 8,
        padding: 6,
        background: "#f9f9f9",
        borderRadius: 4
      }}>
        <div style={{
          width: 10,
          height: 10,
          borderRadius: "50%",
          background: statusColors[connectionStatus]
        }} />
        <span style={{ fontSize: 12, color: "#666" }}>
          {connectionStatus === "connected" && "✓ Połączono z backendem"}
          {connectionStatus === "error" && "✗ Brak połączenia"}
          {connectionStatus === "unknown" && "⟳ Sprawdzanie..."}
        </span>
      </div>

      {/* Messages */}
      <div style={{ maxHeight: 400, overflowY: "auto", marginBottom: 8 }}>
        {messages.map((m) => (
          <div key={m.id} style={{ marginBottom: 8 }}>
            <div style={{ fontSize: 12, color: "#666", fontWeight: "bold" }}>
              {m.role === "user" && "👤 Ty"}
              {m.role === "assistant" && "🤖 AI"}
              {m.role === "system" && "ℹ️ System"}
              {m.role === "tool" && "🔧 Narzędzia"}
              {m.role === "error" && "❌ Błąd"}
            </div>
            <div style={{
              background: m.role === "user" ? "#e3f2fd" : m.role === "error" ? "#ffebee" : m.role === "tool" ? "#fff3e0" : "#f3f3f3",
              padding: 8,
              borderRadius: 6,
              whiteSpace: "pre-wrap"
            }}>
              {m.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={onKeyDown}
        rows={3}
        style={{
          width: "100%",
          marginBottom: 8,
          padding: 8,
          borderRadius: 4,
          border: "1px solid #ddd",
          fontFamily: "inherit"
        }}
        placeholder="Napisz wiadomość... (Enter = wyślij, Shift+Enter = nowa linia)"
        disabled={loading || connectionStatus === "error"}
      />

      {/* Send Button */}
      <div style={{ display: "flex", gap: 8 }}>
        <button
          onClick={sendMessage}
          disabled={loading || connectionStatus === "error"}
          style={{
            flex: 1,
            padding: 10,
            borderRadius: 4,
            border: "none",
            background: loading ? "#ccc" : "#2196F3",
            color: "white",
            fontWeight: "bold",
            cursor: loading || connectionStatus === "error" ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "⏳ Wysyłanie..." : "📤 Wyślij"}
        </button>
      </div>
    </div>
  );
}