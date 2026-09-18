-- Tabela do rotacji darmowych kluczy
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL, -- np. 'airforce', 'groq', 'cloudflare'
    key_value TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    cooldown_until DATETIME DEFAULT NULL,
    success_rate REAL DEFAULT 1.0, -- Bandit Scoring
    avg_latency_ms INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Katalog darmowych modeli z priorytetami
CREATE TABLE IF NOT EXISTS model_catalog (
    id TEXT PRIMARY KEY, -- np. 'llama-3-70b'
    display_name TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    is_free BOOLEAN DEFAULT 1,
    priority INTEGER DEFAULT 10
);