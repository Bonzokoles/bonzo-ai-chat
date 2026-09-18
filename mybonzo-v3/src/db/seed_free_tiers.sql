-- Rejestracja darmowych dostawców i bram API
INSERT OR IGNORE INTO api_keys (provider, key_value, success_rate) VALUES 
('openrouter', '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', 1.0),
('opencode', 'sk-YolSFGkgX04ni4qwJHW6Mv7xrCnCc94jnBTN4pUGGvINRTMAP5ywCRYHWT5EMniM', 1.0),
('cloudflare', 'cfut_pOEjYqDt9O8YVUNVpDaYTG608A5YxSAHj6eEL5hj6b45e85b', 1.0),
('omniroute', 'oma_live_sGrlekYFf0gd7wE7qRn1tTq4yq8b698fHdA0JLuLl-A', 1.0),
('pollinations', 'keyless_public', 1.0),
('airforce', 'keyless_public', 1.0);

-- Katalog darmowych modeli AI (2026 Fleet)
INSERT OR REPLACE INTO model_catalog (id, display_name, provider_id, is_free, priority) VALUES 
-- 1. OmniRoute (Local Multi-Provider Router & Combos)
('auto/best-free', 'OmniRoute Best Free (Auto-Rotation)', 'omniroute', 1, 1),
('auto/coding:free', 'OmniRoute Coding Free (Specialized)', 'omniroute', 1, 2),
('auto/reasoning', 'OmniRoute Reasoning Engine', 'omniroute', 1, 3),
('auto/fast', 'OmniRoute Fast Low-Latency', 'omniroute', 1, 4),
('auto/smart', 'OmniRoute Smart Hybrid', 'omniroute', 1, 5),

-- 2. Cloudflare Workers AI (Edge Native)
('@cf/meta/llama-3.1-8b-instruct', 'Llama 3.1 8B (Workers AI)', 'cloudflare', 1, 1),
('@cf/meta/llama-3.3-70b-instruct-fp8-fast', 'Llama 3.3 70B Fast (Workers AI)', 'cloudflare', 1, 2),
('@cf/deepseek-ai/deepseek-r1-distill-qwen-32b', 'DeepSeek R1 Distill 32B (Workers AI)', 'cloudflare', 1, 3),
('@cf/mistral/mistral-7b-instruct-v0.2', 'Mistral 7B Instruct (Workers AI)', 'cloudflare', 1, 4),
('@cf/qwen/qwen2.5-coder-7b-instruct', 'Qwen 2.5 Coder 7B (Workers AI)', 'cloudflare', 1, 5),

-- 3. Pollinations.ai (100% Free / Keyless)
('pollinations/openai', 'GPT-4o Mini (Pollinations 🆓)', 'pollinations', 1, 1),
('pollinations/mistral', 'Mistral Nemo (Pollinations 🆓)', 'pollinations', 1, 2),
('pollinations/deepseek', 'DeepSeek V3 (Pollinations 🆓)', 'pollinations', 1, 3),
('pollinations/qwen', 'Qwen 2.5 72B (Pollinations 🆓)', 'pollinations', 1, 4),

-- 4. Airforce (Keyless Free)
('airforce/llama-3.1-70b-chat', 'Llama 3.1 70B (Airforce 🆓)', 'airforce', 1, 1),
('airforce/deepseek-v3', 'DeepSeek V3 (Airforce 🆓)', 'airforce', 1, 2),
('airforce/chatgpt-4o-latest', 'ChatGPT 4o (Airforce 🆓)', 'airforce', 1, 3),

-- 5. OpenRouter (:free Tier)
('google/gemini-2.0-flash-lite:free', 'Gemini 2.0 Flash Lite (OpenRouter 🆓)', 'openrouter', 1, 1),
('meta-llama/llama-3.3-70b-instruct:free', 'Llama 3.3 70B Instruct (OpenRouter 🆓)', 'openrouter', 1, 2),
('deepseek/deepseek-chat:free', 'DeepSeek V3 (OpenRouter 🆓)', 'openrouter', 1, 3),
('qwen/qwen-2.5-coder-32b:free', 'Qwen 2.5 Coder 32B (OpenRouter 🆓)', 'openrouter', 1, 4),

-- 6. OpenCode Zen
('deepseek/deepseek-chat', 'DeepSeek V3 (OpenCode)', 'opencode', 1, 1),
('qwen/qwen-2.5-coder-32b', 'Qwen 2.5 Coder (OpenCode)', 'opencode', 1, 2);