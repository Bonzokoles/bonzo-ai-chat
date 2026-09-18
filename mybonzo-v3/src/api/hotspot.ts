import { Hono } from 'hono';

type Bindings = {
  DB: D1Database;
  AI: any;
  OMNIROUTE_URL?: string;
  OMNIROUTE_API_KEY?: string;
  GROQ_API_KEY?: string;
  GOOGLE_API_KEY?: string;
  OPENROUTER_API_KEY?: string;
  CEREBRAS_API_KEY?: string;
};

interface HotspotToken {
  token: string;
  name: string;
  tier: string;
  allowed_providers: string;
  allowed_models: string;
  token_limit: number;
  tokens_used: number;
  requests_count: number;
  rate_limit_rpm: number;
  is_active: number;
  expires_at: string | null;
  created_at: string;
}

interface HotspotProvider {
  id: string;
  label: string;
  base_url: string;
  api_key: string;
  models_json: string;
  cost_per_mtok_usd: number;
  is_active: number;
  priority: number;
}

export function generateBonzoKey(): string {
  const chars = 'ABCDEFGHJKMNPQRSTVWXYZ23456789';
  const block = () => {
    let s = '';
    const bytes = new Uint8Array(4);
    crypto.getRandomValues(bytes);
    for (let i = 0; i < 4; i++) {
      s += chars[bytes[i] % chars.length];
    }
    return s;
  };
  return `BNZ-${block()}-${block()}-${block()}-${block()}`;
}

const hotspot = new Hono<{ Bindings: Bindings }>();

// Helper: Resolve active token and check quotas
async function authenticateToken(c: any): Promise<{ tokenRecord: HotspotToken | null; error?: string; status?: number }> {
  const headerToken = c.req.header('X-Hotspot-Token') || c.req.header('X-Bonzo-Key');
  const authHeader = c.req.header('Authorization');
  const bearerToken = authHeader?.startsWith('Bearer ') ? authHeader.substring(7).trim() : null;
  const queryToken = c.req.query('token') || c.req.query('key');

  const tokenValue = headerToken || bearerToken || queryToken || 'hb_guest_public';

  const tokenRecord = await c.env.DB.prepare(
    'SELECT * FROM hotspot_tokens WHERE token = ?'
  ).bind(tokenValue).first() as HotspotToken | null;

  if (!tokenRecord) {
    return { tokenRecord: null, error: 'INVALID_HOTSPOT_TOKEN', status: 401 };
  }

  if (tokenRecord.is_active !== 1) {
    return { tokenRecord: null, error: 'TOKEN_SUSPENDED_OR_REVOKED', status: 403 };
  }

  if (tokenRecord.expires_at && new Date(tokenRecord.expires_at).getTime() < Date.now()) {
    return { tokenRecord: null, error: 'TOKEN_EXPIRED', status: 403 };
  }

  if (tokenRecord.token_limit !== -1 && tokenRecord.tokens_used >= tokenRecord.token_limit) {
    return { tokenRecord: null, error: 'TOKEN_QUOTA_EXCEEDED', status: 429 };
  }

  return { tokenRecord };
}

// ─────────────────────────────────────────────────────────────────────────────
// 1. Catalog & Status Endpoint
// ─────────────────────────────────────────────────────────────────────────────
hotspot.get('/catalog', async (c) => {
  try {
    const { tokenRecord, error, status } = await authenticateToken(c);
    if (!tokenRecord) {
      return c.json({ error }, (status || 401) as any);
    }

    const { results: providers } = await c.env.DB.prepare(
      'SELECT id, label, models_json, cost_per_mtok_usd, priority FROM hotspot_providers WHERE is_active = 1 ORDER BY priority ASC'
    ).all() as { results: HotspotProvider[] };

    const allowedProvidersList = tokenRecord.allowed_providers === '*' 
      ? null 
      : tokenRecord.allowed_providers.split(',').map(s => s.trim().toLowerCase());

    const allowedModelsList = tokenRecord.allowed_models === '*' 
      ? null 
      : tokenRecord.allowed_models.split(',').map(s => s.trim().toLowerCase());

    const catalog: any[] = [];
    for (const p of providers) {
      if (allowedProvidersList && !allowedProvidersList.includes(p.id.toLowerCase())) {
        continue;
      }
      let models: string[] = [];
      try {
        models = JSON.parse(p.models_json);
      } catch {
        models = [];
      }
      if (allowedModelsList) {
        models = models.filter(m => allowedModelsList.includes(m.toLowerCase()));
      }
      if (models.length > 0) {
        catalog.push({
          id: p.id,
          label: p.label,
          models,
          cost_per_mtok_usd: p.cost_per_mtok_usd
        });
      }
    }

    return c.json({
      ok: true,
      token: tokenRecord.token,
      name: tokenRecord.name,
      tier: tokenRecord.tier,
      quota: {
        limit: tokenRecord.token_limit,
        used: tokenRecord.tokens_used,
        remaining: tokenRecord.token_limit === -1 ? 'unlimited' : Math.max(0, tokenRecord.token_limit - tokenRecord.tokens_used),
        requests_count: tokenRecord.requests_count
      },
      providers: catalog
    });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// 2. Chat Completions Gateway (OpenAI Compatible)
// ─────────────────────────────────────────────────────────────────────────────
hotspot.post('/chat', async (c) => {
  const startTime = Date.now();
  const clientIp = c.req.header('cf-connecting-ip') || c.req.header('x-forwarded-for') || 'unknown';

  const { tokenRecord, error, status } = await authenticateToken(c);
  if (!tokenRecord) {
    return c.json({ error }, (status || 401) as any);
  }

  let body: any;
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: 'INVALID_JSON_PAYLOAD' }, 400);
  }

  const { model, messages, temperature = 0.7, max_tokens, stream = false } = body;
  if (!model || !messages || !Array.isArray(messages)) {
    return c.json({ error: 'MODEL_AND_MESSAGES_REQUIRED' }, 400);
  }

  // Extract prompt preview for telemetry
  const lastUserMsg = messages.slice().reverse().find((m: any) => m.role === 'user');
  const promptPreview = typeof lastUserMsg?.content === 'string' 
    ? lastUserMsg.content.substring(0, 240) 
    : '[Multimodal/Array]';

  // Find matching active provider from DB
  const { results: providers } = await c.env.DB.prepare(
    'SELECT * FROM hotspot_providers WHERE is_active = 1 ORDER BY priority ASC'
  ).all() as { results: HotspotProvider[] };

  let targetProvider: HotspotProvider | null = null;
  for (const p of providers) {
    try {
      const models = JSON.parse(p.models_json) as string[];
      if (models.includes(model)) {
        targetProvider = p;
        break;
      }
    } catch {}
  }

  // Fallback match: if model contains '/', default to OpenRouter or Together
  if (!targetProvider) {
    if (model.includes('/')) {
      targetProvider = providers.find(p => p.id === 'openrouter' || p.id === 'together') || null;
    } else if (model.toLowerCase().includes('deepseek')) {
      targetProvider = providers.find(p => p.id === 'deepseek') || null;
    } else if (model.startsWith('@cf/')) {
      targetProvider = providers.find(p => p.id === 'cloudflare-ai') || null;
    } else if (model.toLowerCase().includes('gpt')) {
      targetProvider = providers.find(p => p.id === 'openai') || null;
    } else if (model.toLowerCase().includes('gemini')) {
      targetProvider = providers.find(p => p.id === 'gemini') || null;
    }
  }

  // If still not matched, check if model is @cf/
  if (!targetProvider && model.startsWith('@cf/')) {
    targetProvider = {
      id: 'cloudflare-ai',
      label: 'Cloudflare Workers AI',
      base_url: 'internal',
      api_key: '',
      models_json: '["@cf/meta/llama-3.3-70b-instruct-fp8-fast", "@cf/meta/llama-3.2-3b-instruct", "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b"]',
      cost_per_mtok_usd: 0,
      is_active: 1,
      priority: 0
    };
  }

  if (!targetProvider) {
    targetProvider = providers[0] || null;
  }

  if (!targetProvider) {
    return c.json({ error: 'NO_ACTIVE_AI_PROVIDER_AVAILABLE' }, 503);
  }

  // Handle Native Cloudflare Workers AI
  if (targetProvider.id === 'cloudflare-ai' || model.startsWith('@cf/')) {
    try {
      const cfRes: any = await c.env.AI.run(model as any, { messages });
      const content = cfRes?.response || cfRes?.text || (typeof cfRes === 'string' ? cfRes : JSON.stringify(cfRes));
      const durationMs = Date.now() - startTime;
      const totalTokens = Math.max(20, Math.ceil((content.length + promptPreview.length) / 4));

      c.executionCtx.waitUntil(
        (async () => {
          await c.env.DB.prepare(
            'INSERT INTO hotspot_telemetry (token_id, client_ip, provider, model, prompt_tokens, completion_tokens, total_tokens, cost_usd, prompt_preview, status, duration_ms) VALUES (?, ?, "cloudflare-ai", ?, ?, ?, ?, 0.0, ?, "ok", ?)'
          ).bind(tokenRecord.token, clientIp, model, Math.ceil(promptPreview.length / 4), Math.ceil(content.length / 4), totalTokens, promptPreview, durationMs).run();

          await c.env.DB.prepare(
            'UPDATE hotspot_tokens SET tokens_used = tokens_used + ?, requests_count = requests_count + 1 WHERE token = ?'
          ).bind(totalTokens, tokenRecord.token).run();
        })()
      );

      return c.json({
        id: `chatcmpl-${Date.now()}`,
        object: 'chat.completion',
        created: Math.floor(Date.now() / 1000),
        model,
        choices: [
          {
            index: 0,
            message: { role: 'assistant', content },
            finish_reason: 'stop'
          }
        ],
        usage: {
          prompt_tokens: Math.ceil(promptPreview.length / 4),
          completion_tokens: Math.ceil(content.length / 4),
          total_tokens: totalTokens
        }
      });
    } catch (cfErr: any) {
      return c.json({ error: `CLOUDFLARE_AI_ERROR: ${cfErr.message}` }, 500);
    }
  }

  // Verify model permissions for this token
  if (tokenRecord.allowed_providers !== '*') {
    const allowed = tokenRecord.allowed_providers.split(',').map(s => s.trim().toLowerCase());
    if (!allowed.includes(targetProvider.id.toLowerCase())) {
      return c.json({ error: `PROVIDER_NOT_ALLOWED: ${targetProvider.id}` }, 403);
    }
  }

  // Build upstream request
  const upstreamUrl = `${targetProvider.base_url.replace(/\/+$/, '')}/chat/completions`;
  const upstreamHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${targetProvider.api_key}`,
  };

  if (targetProvider.id === 'gemini') {
    upstreamHeaders['x-goog-api-key'] = targetProvider.api_key;
  }

  if (targetProvider.id === 'openrouter') {
    upstreamHeaders['HTTP-Referer'] = 'https://ai.mybonzoaiblog.com';
    upstreamHeaders['X-Title'] = 'EastWood Ops Hotspot Gateway';
  }

  try {
    const upstreamRes = await fetch(upstreamUrl, {
      method: 'POST',
      headers: upstreamHeaders,
      body: JSON.stringify({
        model,
        messages,
        temperature,
        ...(max_tokens ? { max_tokens } : {}),
      })
    });

    if (!upstreamRes.ok) {
      const errText = await upstreamRes.text();
      const durationMs = Date.now() - startTime;
      // Record failure telemetry
      c.executionCtx.waitUntil(
        c.env.DB.prepare(
          'INSERT INTO hotspot_telemetry (token_id, client_ip, provider, model, prompt_preview, status, error_message, duration_ms) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        ).bind(tokenRecord.token, clientIp, targetProvider.id, model, promptPreview, 'upstream_error', errText.substring(0, 300), durationMs).run()
      );
      return c.text(errText, upstreamRes.status as any);
    }

    // Handle Streaming Response
    if (stream) {
      const durationMs = Date.now() - startTime;
      c.executionCtx.waitUntil(
        (async () => {
          await c.env.DB.prepare(
            'INSERT INTO hotspot_telemetry (token_id, client_ip, provider, model, prompt_tokens, completion_tokens, total_tokens, prompt_preview, status, duration_ms) VALUES (?, ?, ?, ?, 100, 150, 250, ?, "streaming", ?)'
          ).bind(tokenRecord.token, clientIp, targetProvider.id, model, promptPreview, durationMs).run();

          await c.env.DB.prepare(
            'UPDATE hotspot_tokens SET tokens_used = tokens_used + 250, requests_count = requests_count + 1 WHERE token = ?'
          ).bind(tokenRecord.token).run();
        })()
      );

      return new Response(upstreamRes.body, {
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // Handle JSON Response
    const data: any = await upstreamRes.json();
    const durationMs = Date.now() - startTime;
    const promptTokens = data.usage?.prompt_tokens || 0;
    const completionTokens = data.usage?.completion_tokens || 0;
    const totalTokens = data.usage?.total_tokens || (promptTokens + completionTokens) || 100;
    const costUsd = (totalTokens / 1_000_000) * (targetProvider.cost_per_mtok_usd || 0.001);

    // Asynchronous Telemetry & Quota Update
    c.executionCtx.waitUntil(
      (async () => {
        await c.env.DB.prepare(
          'INSERT INTO hotspot_telemetry (token_id, client_ip, provider, model, prompt_tokens, completion_tokens, total_tokens, cost_usd, prompt_preview, status, duration_ms) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, "ok", ?)'
        ).bind(tokenRecord.token, clientIp, targetProvider.id, model, promptTokens, completionTokens, totalTokens, costUsd, promptPreview, durationMs).run();

        await c.env.DB.prepare(
          'UPDATE hotspot_tokens SET tokens_used = tokens_used + ?, requests_count = requests_count + 1 WHERE token = ?'
        ).bind(totalTokens, tokenRecord.token).run();
      })()
    );

    return c.json(data);
  } catch (err: any) {
    const durationMs = Date.now() - startTime;
    c.executionCtx.waitUntil(
      c.env.DB.prepare(
        'INSERT INTO hotspot_telemetry (token_id, client_ip, provider, model, prompt_preview, status, error_message, duration_ms) VALUES (?, ?, ?, ?, ?, "gateway_exception", ?, ?)'
      ).bind(tokenRecord.token, clientIp, targetProvider.id, model, promptPreview, err.message, durationMs).run()
    );
    return c.json({ error: err.message }, 500);
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// 3. Admin: Real-Time Telemetry & Monitoring
// ─────────────────────────────────────────────────────────────────────────────
hotspot.get('/admin/telemetry', async (c) => {
  const { tokenRecord } = await authenticateToken(c);
  if (!tokenRecord || tokenRecord.tier !== 'admin') {
    return c.json({ error: 'ADMIN_ACCESS_REQUIRED' }, 403);
  }

  const limit = Math.min(100, parseInt(c.req.query('limit') || '30'));
  const { results: logs } = await c.env.DB.prepare(
    'SELECT * FROM hotspot_telemetry ORDER BY id DESC LIMIT ?'
  ).bind(limit).all();

  const stats = await c.env.DB.prepare(`
    SELECT 
      COUNT(*) as total_requests,
      COALESCE(SUM(total_tokens), 0) as total_tokens_used,
      COALESCE(SUM(cost_usd), 0.0) as total_cost_usd,
      COUNT(DISTINCT token_id) as active_tokens_count,
      COUNT(DISTINCT client_ip) as unique_ips_count
    FROM hotspot_telemetry
  `).first();

  return c.json({ ok: true, stats, logs });
});

// ─────────────────────────────────────────────────────────────────────────────
// 4. Admin: Virtual Tokens List & Bulk Generator ("Modyfikuj w ilości")
// ─────────────────────────────────────────────────────────────────────────────
hotspot.get('/admin/tokens', async (c) => {
  const { tokenRecord } = await authenticateToken(c);
  if (!tokenRecord || tokenRecord.tier !== 'admin') {
    return c.json({ error: 'ADMIN_ACCESS_REQUIRED' }, 403);
  }

  const { results: tokens } = await c.env.DB.prepare(
    'SELECT * FROM hotspot_tokens ORDER BY created_at DESC'
  ).all();

  return c.json({ ok: true, tokens });
});

hotspot.post('/admin/tokens', async (c) => {
  const { tokenRecord } = await authenticateToken(c);
  if (!tokenRecord || tokenRecord.tier !== 'admin') {
    return c.json({ error: 'ADMIN_ACCESS_REQUIRED' }, 403);
  }

  const body = await c.req.json();
  const {
    name = 'Batch Client Token',
    tier = 'starter',
    token_limit = 50000,
    allowed_providers = '*',
    allowed_models = '*',
    rate_limit_rpm = 30,
    count = 1,
    format = 'kraft',
    prefix = 'BNZ'
  } = body;

  const generatedTokens: string[] = [];
  const stmt = c.env.DB.prepare(
    'INSERT INTO hotspot_tokens (token, name, tier, allowed_providers, allowed_models, token_limit, rate_limit_rpm) VALUES (?, ?, ?, ?, ?, ?, ?)'
  );

  const batchQueries = [];
  for (let i = 0; i < Math.min(100, Math.max(1, count)); i++) {
    const tokenStr = (format === 'kraft' || prefix.toUpperCase() === 'BNZ')
      ? generateBonzoKey()
      : `${prefix}_${tier}_${Math.random().toString(36).substring(2, 10)}${Math.random().toString(36).substring(2, 6)}`;
    const tokenName = count > 1 ? `${name} #${i + 1}` : name;
    generatedTokens.push(tokenStr);
    batchQueries.push(stmt.bind(tokenStr, tokenName, tier, allowed_providers, allowed_models, token_limit, rate_limit_rpm));
  }

  await c.env.DB.batch(batchQueries);

  return c.json({
    ok: true,
    created_count: generatedTokens.length,
    tokens: generatedTokens
  });
});

hotspot.post('/admin/tokens/toggle', async (c) => {
  const { tokenRecord } = await authenticateToken(c);
  if (!tokenRecord || tokenRecord.tier !== 'admin') {
    return c.json({ error: 'ADMIN_ACCESS_REQUIRED' }, 403);
  }

  const { token, is_active } = await c.req.json();
  if (!token) return c.json({ error: 'TOKEN_REQUIRED' }, 400);

  await c.env.DB.prepare(
    'UPDATE hotspot_tokens SET is_active = ? WHERE token = ?'
  ).bind(is_active ? 1 : 0, token).run();

  return c.json({ ok: true, token, is_active: is_active ? 1 : 0 });
});

// ─────────────────────────────────────────────────────────────────────────────
// 5. Admin: Providers & Kill-Switch
// ─────────────────────────────────────────────────────────────────────────────
hotspot.get('/admin/providers', async (c) => {
  const { tokenRecord } = await authenticateToken(c);
  if (!tokenRecord || tokenRecord.tier !== 'admin') {
    return c.json({ error: 'ADMIN_ACCESS_REQUIRED' }, 403);
  }

  const { results: providers } = await c.env.DB.prepare(
    'SELECT id, label, base_url, models_json, cost_per_mtok_usd, is_active, priority FROM hotspot_providers ORDER BY priority ASC'
  ).all();

  return c.json({ ok: true, providers });
});

hotspot.post('/admin/providers/toggle', async (c) => {
  const { tokenRecord } = await authenticateToken(c);
  if (!tokenRecord || tokenRecord.tier !== 'admin') {
    return c.json({ error: 'ADMIN_ACCESS_REQUIRED' }, 403);
  }

  const { provider_id, is_active } = await c.req.json();
  if (!provider_id) return c.json({ error: 'PROVIDER_ID_REQUIRED' }, 400);

  await c.env.DB.prepare(
    'UPDATE hotspot_providers SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
  ).bind(is_active ? 1 : 0, provider_id).run();

  return c.json({ ok: true, provider_id, is_active: is_active ? 1 : 0 });
});

export default hotspot;
