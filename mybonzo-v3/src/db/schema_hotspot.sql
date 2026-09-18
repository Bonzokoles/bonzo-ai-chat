-- ==========================================================
-- THE BUCH / MYBONZO HOTSPOT GATEWAY & KEY PROVISIONING ENGINE
-- Cloudflare D1 Architecture
-- ==========================================================

CREATE TABLE IF NOT EXISTS hotspot_providers (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    base_url TEXT NOT NULL,
    api_key TEXT NOT NULL,
    models_json TEXT NOT NULL,
    cost_per_mtok_usd REAL DEFAULT 0.0,
    is_active INTEGER DEFAULT 1,
    priority INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hotspot_tokens (
    token TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tier TEXT DEFAULT 'starter',
    allowed_providers TEXT DEFAULT '*',
    allowed_models TEXT DEFAULT '*',
    token_limit INTEGER DEFAULT 50000,
    tokens_used INTEGER DEFAULT 0,
    requests_count INTEGER DEFAULT 0,
    rate_limit_rpm INTEGER DEFAULT 30,
    is_active INTEGER DEFAULT 1,
    expires_at DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hotspot_telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT,
    client_ip TEXT,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_tokens INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0.0,
    prompt_preview TEXT,
    status TEXT DEFAULT 'ok',
    error_message TEXT,
    duration_ms INTEGER DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hotspot_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Seed initial master settings
INSERT OR IGNORE INTO hotspot_config (key, value) VALUES ('global_killswitch', '0');
INSERT OR IGNORE INTO hotspot_config (key, value) VALUES ('guest_access_allowed', '1');
INSERT OR IGNORE INTO hotspot_config (key, value) VALUES ('default_guest_model', 'deepseek-chat');

-- Seed master admin token for Bonzo
INSERT OR REPLACE INTO hotspot_tokens (token, name, tier, allowed_providers, allowed_models, token_limit, is_active)
VALUES ('hb_bonzo_root_2026', 'Bonzo Root Master', 'admin', '*', '*', -1, 1);

-- Seed default public guest token
INSERT OR REPLACE INTO hotspot_tokens (token, name, tier, allowed_providers, allowed_models, token_limit, is_active)
VALUES ('hb_guest_public', 'Guest Web Public', 'guest', 'deepseek,openrouter,gemini', '*', 20000, 1);
