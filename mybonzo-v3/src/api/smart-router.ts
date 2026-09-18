import { Hono } from 'hono';
import { SmartRouterEngine } from '../providers/router';
import { ChatMessage, RoutingRequirement } from '../providers/types';
import { fetchOmniRouteModels, checkOmniRouteHealth, OMNIROUTE_DEFAULT_URL, OMNIROUTE_DEFAULT_KEY } from '../providers/omniroute';

const api = new Hono<{
  Bindings: {
    DB: D1Database;
    AI: any;
    OMNIROUTE_URL?: string;
    OMNIROUTE_API_KEY?: string;
    GROQ_API_KEY?: string;
    GOOGLE_API_KEY?: string;
    OPENROUTER_API_KEY?: string;
    CEREBRAS_API_KEY?: string;
  };
}>();

// Główny endpoint inteligentnego czatu z automatycznym fallbackiem
api.post('/chat', async (c) => {
  try {
    const body = await c.req.json();
    const message = body.message || body.prompt;
    const requirement: RoutingRequirement = body.requirement || 'free_unlimited';
    const systemPrompt = body.systemPrompt || 'You are an elite AI assistant on the MyBonzo mesh.';

    if (!message && (!body.messages || body.messages.length === 0)) {
      return c.json({ error: 'Message or messages array is required' }, 400);
    }

    const messages: ChatMessage[] = body.messages || [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: message }
    ];

    const engine = new SmartRouterEngine({
      DB: c.env.DB,
      AI: c.env.AI,
      OMNIROUTE_URL: c.env.OMNIROUTE_URL,
      OMNIROUTE_API_KEY: c.env.OMNIROUTE_API_KEY,
      GROQ_API_KEY: c.env.GROQ_API_KEY,
      GOOGLE_API_KEY: c.env.GOOGLE_API_KEY,
      OPENROUTER_API_KEY: c.env.OPENROUTER_API_KEY,
      CEREBRAS_API_KEY: c.env.CEREBRAS_API_KEY
    });

    const result = await engine.executeWithFallback(messages, {
      requirement,
      model: body.model,
      temperature: body.temperature,
      max_tokens: body.max_tokens
    });

    return c.json({
      success: true,
      data: result,
      routing: {
        served_by: result.provider,
        model: result.model,
        latency_ms: result.latency_ms,
        saved_usd: result.saved_usd,
        free_tier: true
      }
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// Zwraca listę wszystkich połączonych darmowych modeli ze wszystkich providerów + OmniRoute
api.get('/models', async (c) => {
  const engine = new SmartRouterEngine({
    DB: c.env.DB,
    AI: c.env.AI,
    OMNIROUTE_URL: c.env.OMNIROUTE_URL
  });

  const baseCatalog = await engine.getCatalog();

  // Pobranie modeli z bazy D1 model_catalog
  let d1Models: any[] = [];
  try {
    const rows = await c.env.DB.prepare('SELECT id, display_name, provider_id, is_free, priority FROM model_catalog WHERE is_free = 1').all();
    d1Models = rows.results || [];
  } catch {}

  // Sprawdzenie i dołączenie modeli z OmniRoute (jeśli dostępny)
  const omniUrl = c.env.OMNIROUTE_URL || OMNIROUTE_DEFAULT_URL;
  const omniKey = c.env.OMNIROUTE_API_KEY || OMNIROUTE_DEFAULT_KEY;
  const omniModels = await fetchOmniRouteModels(omniUrl, omniKey);

  return c.json({
    total_models: baseCatalog.length + d1Models.length + omniModels.length,
    base_free_models: baseCatalog,
    d1_registered_models: d1Models,
    omniroute_models: omniModels.slice(0, 50),
    omniroute_connected: omniModels.length > 0
  });
});

// Status połączeń z dostawcami
api.get('/providers', async (c) => {
  const omniUrl = c.env.OMNIROUTE_URL || OMNIROUTE_DEFAULT_URL;
  const isOmniAlive = await checkOmniRouteHealth(omniUrl);

  return c.json({
    providers: [
      {
        id: 'cloudflare',
        name: 'Cloudflare Workers AI',
        status: 'online',
        type: 'edge_native',
        cost: 'FREE (10k neurons/day)',
        models: ['Llama 3.1 8B', 'Llama 3.3 70B', 'DeepSeek R1 Distill 32B', 'Mistral 7B', 'Qwen 2.5 Coder']
      },
      {
        id: 'pollinations',
        name: 'Pollinations.ai',
        status: 'online',
        type: 'keyless_public',
        cost: '100% FREE (no key required)',
        models: ['GPT-4o Mini', 'Mistral Nemo', 'DeepSeek V3', 'Qwen 2.5 72B']
      },
      {
        id: 'airforce',
        name: 'Airforce Free Gateway',
        status: 'online',
        type: 'keyless_public',
        cost: '100% FREE',
        models: ['Llama 3.1 70B', 'DeepSeek V3', 'ChatGPT 4o']
      },
      {
        id: 'omniroute',
        name: 'OmniRoute Local Aggregator',
        status: isOmniAlive ? 'online' : 'reachable_via_host',
        port: 20128,
        type: 'multi_provider_gateway',
        cost: 'Aggregated Free Tiers',
        models: ['auto/best-free', 'auto/coding:free', 'auto/reasoning', 'auto/fast', 'tllm/*', 'veo-free/*']
      },
      {
        id: 'openrouter',
        name: 'OpenRouter Free Tier',
        status: 'supported',
        type: 'cloud_api',
        cost: 'FREE (:free models)',
        models: ['google/gemini-2.0-flash-lite:free', 'meta-llama/llama-3.3-70b-instruct:free']
      },
      {
        id: 'groq',
        name: 'Groq Cloud LPU',
        status: 'supported',
        type: 'cloud_api',
        cost: 'FREE Tier (rate-limited)',
        models: ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant']
      },
      {
        id: 'google',
        name: 'Google Gemini Studio',
        status: 'supported',
        type: 'cloud_api',
        cost: 'FREE Tier (15 RPM / 1M TPM)',
        models: ['gemini-2.0-flash', 'gemini-1.5-flash']
      }
    ]
  });
});

export default api;