-- Tabela Agentów
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'worker', -- worker, orchestrator, operator
    provider_preference TEXT DEFAULT 'omniroute', -- domyślny dostawca
    status TEXT DEFAULT 'idle',
    last_active DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela uprawnień i połączeń funkcji
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    resource TEXT NOT NULL, -- np. 'shopify_api', 'r2_storage'
    action TEXT NOT NULL,   -- np. 'read', 'write', 'delete'
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(agent_id) REFERENCES agents(id)
);

-- Tabela wydatków i logów operacyjnych
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0.0,
    action_type TEXT, -- 'api_call', 'function_switch'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(agent_id) REFERENCES agents(id)
);

-- Inicjalizacja Agenta Operacyjnego
INSERT OR IGNORE INTO agents (id, name, role, provider_preference, status) 
VALUES ('op-01', 'OPERATIONAL_CORE', 'operator', 'omniroute', 'online');