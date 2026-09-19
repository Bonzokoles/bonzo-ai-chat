import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { OperationalCore } from './agents/operational';
import agents from './api/agents';
import terminal from './api/terminal';
import smartRouter from './api/smart-router';
import hotspot from './api/hotspot';
import mcp from './api/mcp';
import stolarska from './api/stolarska';
import { SmartRouterEngine } from './providers/router';
import { checkOmniRouteHealth, OMNIROUTE_DEFAULT_URL, OMNIROUTE_DEFAULT_KEY, fetchOmniRouteModels } from './providers/omniroute';

type Bindings = {
  DB: D1Database;
  AI: any;
  OMNIROUTE_URL?: string;
  OMNIROUTE_API_KEY?: string;
  GROQ_API_KEY?: string;
  GOOGLE_API_KEY?: string;
  OPENROUTER_API_KEY?: string;
  CEREBRAS_API_KEY?: string;
  SAMBANOVA_API_KEY?: string;
  MISTRAL_API_KEY?: string;
  DEEPSEEK_API_KEY?: string;
};

const app = new Hono<{ Bindings: Bindings }>();

// Enable CORS for all incoming client origins
app.use('*', cors({
  origin: '*',
  allowHeaders: ['*'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
}));

// Global Health Check
app.get('/api/health', (c) => {
  return c.json({
    status: 'ok',
    provider: 'mybonzo',
    service: 'MyBonzo Multi-Provider Mesh',
    version: '0.6.2-KRAFT-SURGICAL',
    cf_edge: true
  });
});

// Routery modułowe
app.route('/api/agents', agents);
app.route('/api/term', terminal);
app.route('/api/smart-router', smartRouter);
app.route('/api/router', smartRouter);
app.route('/api/hotspot', hotspot);
app.route('/api/mcp', mcp);
app.route('/mcp', mcp);
app.route('/api/stolarska', stolarska);

// Standardowy endpoint OpenAI-compatible dla listy modeli (wymagany przez Terax, Cursor, LibreChat, itp.)
app.get('/v1/models', (c) => {
  return c.json({
    object: 'list',
    data: [
      {
        id: '@cf/meta/llama-3.3-70b-instruct-fp8-fast',
        object: 'model',
        created: 1700000000,
        owned_by: 'cloudflare',
        name: 'Meta Llama 3.3 70B Instruct Fast'
      },
      {
        id: '@cf/meta/llama-3.2-3b-instruct',
        object: 'model',
        created: 1700000000,
        owned_by: 'cloudflare',
        name: 'Meta Llama 3.2 3B Instruct'
      },
      {
        id: '@cf/meta/llama-3.1-8b-instruct',
        object: 'model',
        created: 1700000000,
        owned_by: 'cloudflare',
        name: 'Meta Llama 3.1 8B Instruct'
      },
      {
        id: 'auto',
        object: 'model',
        created: 1700000000,
        owned_by: 'mybonzo',
        name: 'MyBonzo Smart Auto-Router'
      }
    ]
  });
});

// Standardowy endpoint OpenAI-compatible dla dowolnych narzędzi i agentów CLI (Aider, Claude Code, Goose, itp.)
app.post('/v1/chat/completions', async (c) => {
  try {
    const body = await c.req.json();
    const messages = body.messages || [{ role: 'user', content: body.prompt || '' }];
    const model = body.model;

    // Optional License / Hotspot Token Check
    const authHeader = c.req.header('Authorization');
    const bearer = authHeader?.startsWith('Bearer ') ? authHeader.substring(7).trim() : null;
    const clientKey = c.req.header('X-Bonzo-Key') || c.req.header('X-Hotspot-Token') || bearer;

    let licenseRecord: any = null;
    if (clientKey) {
      licenseRecord = await c.env.DB.prepare(
        'SELECT * FROM hotspot_tokens WHERE token = ? AND is_active = 1'
      ).bind(clientKey).first();

      if (licenseRecord) {
        if (licenseRecord.token_limit !== -1 && licenseRecord.tokens_used >= licenseRecord.token_limit) {
          return c.json({ error: { message: 'LICENSE_TOKEN_QUOTA_EXCEEDED', type: 'quota_error' } }, 429);
        }
      }
    }

    const engine = new SmartRouterEngine({
      DB: c.env.DB,
      AI: c.env.AI,
      OMNIROUTE_URL: c.env.OMNIROUTE_URL,
      OMNIROUTE_API_KEY: c.env.OMNIROUTE_API_KEY,
      GROQ_API_KEY: c.env.GROQ_API_KEY,
      GOOGLE_API_KEY: c.env.GOOGLE_API_KEY,
      OPENROUTER_API_KEY: c.env.OPENROUTER_API_KEY,
      CEREBRAS_API_KEY: c.env.CEREBRAS_API_KEY,
      SAMBANOVA_API_KEY: c.env.SAMBANOVA_API_KEY,
      MISTRAL_API_KEY: c.env.MISTRAL_API_KEY,
      DEEPSEEK_API_KEY: c.env.DEEPSEEK_API_KEY
    });

    const result = await engine.executeWithFallback(messages, {
      model,
      temperature: body.temperature,
      max_tokens: body.max_tokens
    });

    if (licenseRecord) {
      c.executionCtx.waitUntil(
        c.env.DB.prepare(
          'UPDATE hotspot_tokens SET tokens_used = tokens_used + ?, requests_count = requests_count + 1 WHERE token = ?'
        ).bind(result.total_tokens || 100, licenseRecord.token).run()
      );
    }

    const isStream = Boolean(body.stream);
    const id = 'chatcmpl-' + Math.random().toString(36).substring(2, 10);
    const created = Math.floor(Date.now() / 1000);

    if (isStream) {
      const chunk1 = {
        id,
        object: 'chat.completion.chunk',
        created,
        model: result.model,
        choices: [
          {
            index: 0,
            delta: { role: 'assistant', content: result.content },
            finish_reason: null
          }
        ]
      };
      const chunk2 = {
        id,
        object: 'chat.completion.chunk',
        created,
        model: result.model,
        choices: [
          {
            index: 0,
            delta: {},
            finish_reason: 'stop'
          }
        ]
      };

      const sseBody = `data: ${JSON.stringify(chunk1)}\n\ndata: ${JSON.stringify(chunk2)}\n\ndata: [DONE]\n\n`;
      return new Response(sseBody, {
        headers: {
          'Content-Type': 'text/event-stream; charset=utf-8',
          'Cache-Control': 'no-cache, no-transform',
          'Connection': 'keep-alive',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    return c.json({
      id,
      object: 'chat.completion',
      created,
      model: result.model,
      choices: [
        {
          index: 0,
          message: {
            role: 'assistant',
            content: result.content
          },
          finish_reason: 'stop'
        }
      ],
      usage: {
        prompt_tokens: result.prompt_tokens,
        completion_tokens: result.completion_tokens,
        total_tokens: result.total_tokens
      },
      _routing: {
        provider: result.provider,
        latency_ms: result.latency_ms,
        saved_usd: result.saved_usd,
        licensed_tier: licenseRecord ? licenseRecord.tier : 'public_free'
      }
    });
  } catch (err: any) {
    return c.json({ error: { message: err.message, type: 'router_error' } }, 500);
  }
});

// Zgodność wsteczna z /api/ai/run
app.post('/api/ai/run', async (c) => {
  const { prompt, model } = await c.req.json();
  const selectedModel = model || '@cf/meta/llama-3.1-8b-instruct';

  try {
    const answer = await c.env.AI.run(selectedModel, { prompt });
    const op = new OperationalCore(c.env.DB, c.env.AI);
    await op.logAction('op-01', 'cloudflare', selectedModel, 0, 0, 'cf_workers_ai');

    return c.json({ success: true, answer });
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

// Status OmniRoute Gateway
app.get('/api/omniroute/status', async (c) => {
  const url = c.env.OMNIROUTE_URL || OMNIROUTE_DEFAULT_URL;
  const key = c.env.OMNIROUTE_API_KEY || OMNIROUTE_DEFAULT_KEY;
  const isHealthy = await checkOmniRouteHealth(url);
  const models = isHealthy ? await fetchOmniRouteModels(url, key) : [];

  return c.json({
    status: isHealthy ? 'online' : 'unreachable_from_worker',
    target_url: url,
    models_count: models.length,
    models: models.slice(0, 20),
    note: isHealthy 
      ? 'Direct connection active' 
      : 'For Cloudflare edge to reach local OmniRoute, configure Cloudflare Tunnel or Goose Bridge'
  });
});

// Status siatki agentów
app.get('/api/mesh/status', async (c) => {
  const op = new OperationalCore(c.env.DB, c.env.AI, {
    OMNIROUTE_URL: c.env.OMNIROUTE_URL
  });
  const status = await op.getMeshStatus();
  return c.json({
    status: 'online',
    mesh_version: '0.6.0-SURGICAL',
    identity: 'Butch Multi-Provider AI Mesh',
    operational_data: status
  });
});

// --- POWERSHELL BRIDGE COMPATIBILITY ENDPOINTS ---
app.post('/api/bridge/task', async (c) => {
  try {
    const { instruction } = await c.req.json();
    if (!instruction || !instruction.trim()) {
      return c.json({ error: 'EMPTY_INSTRUCTION' }, 400);
    }
    const id = 'task-' + Date.now() + '-' + Math.random().toString(36).substring(2, 7);
    await c.env.DB.prepare(
      'INSERT INTO tasks (id, instruction, status, actor) VALUES (?, ?, ?, ?)'
    ).bind(id, instruction.trim(), 'pending', 'BONZO_UI').run();

    return c.json({ success: true, id, status: 'pending' });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

app.get('/api/bridge/poll', async (c) => {
  try {
    const task = await c.env.DB.prepare(
      "SELECT * FROM tasks WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
    ).first();

    if (task) {
      await c.env.DB.prepare("UPDATE tasks SET status = 'running', updated_at = CURRENT_TIMESTAMP WHERE id = ?")
        .bind(task.id).run();
    }

    return c.json(task || { message: 'NO_PENDING_TASKS' });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

app.post('/api/bridge/result', async (c) => {
  try {
    const { id, result, status } = await c.req.json();
    if (!id) return c.json({ error: 'MISSING_ID' }, 400);

    await c.env.DB.prepare(
      "UPDATE tasks SET result = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    ).bind(result || '', status || 'completed', id).run();

    return c.json({ ok: true, id });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

// ── The Buch / EastWood Ops Compatibility Endpoints ─────────────────────────
app.get('/api/models', async (c) => {
  try {
    const { results } = await c.env.DB.prepare(
      'SELECT id, label, models_json FROM hotspot_providers WHERE is_active = 1 ORDER BY priority ASC'
    ).all();

    const groups: Record<string, any[]> = {
      'Darmowe (Cloudflare Edge AI)': [
        { id: '@cf/meta/llama-3.3-70b-instruct-fp8-fast', name: 'Meta Llama 3.3 70B (Fast & Free)', provider: 'cloudflare-ai' },
        { id: '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b', name: 'DeepSeek R1 32B (Darmowy / Free)', provider: 'cloudflare-ai' },
        { id: '@cf/meta/llama-3.2-3b-instruct', name: 'Meta Llama 3.2 3B (Ultra Szybki)', provider: 'cloudflare-ai' }
      ]
    };

    const modelsList: any[] = [
      { id: '@cf/meta/llama-3.3-70b-instruct-fp8-fast', name: 'Meta Llama 3.3 70B (Fast & Free)', provider: 'cloudflare-ai' },
      { id: '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b', name: 'DeepSeek R1 32B (Darmowy / Free)', provider: 'cloudflare-ai' },
      { id: '@cf/meta/llama-3.2-3b-instruct', name: 'Meta Llama 3.2 3B (Ultra Szybki)', provider: 'cloudflare-ai' }
    ];

    for (const r of (results || [])) {
      try {
        const list = JSON.parse(r.models_json as string);
        const groupItems: any[] = [];
        const groupLabel = r.id === 'openai' 
          ? 'OpenAI Direct (GPT-4o)' 
          : (r.id === 'together' ? 'Together AI (Ultra Fast)' : (r.label || r.id));

        for (const m of list) {
          let displayName = `${r.label}: ${m}`;
          if (m === 'gpt-4o') displayName = 'OpenAI GPT-4o (Flagowy)';
          else if (m === 'gpt-4o-mini') displayName = 'OpenAI GPT-4o Mini (Szybki & Ekonomiczny)';
          else if (m === 'o3-mini') displayName = 'OpenAI o3-mini (Rozumowanie)';
          else if (m.includes('Llama-3.3-70B')) displayName = 'Together: Llama 3.3 70B Turbo';
          else if (m.includes('DeepSeek-R1')) displayName = 'Together: DeepSeek R1 Turbo';

          const item = { id: m, name: displayName, provider: r.id };
          groupItems.push(item);
          modelsList.push(item);
        }
        if (groupItems.length > 0) {
          groups[groupLabel] = groupItems;
        }
      } catch {}
    }

    return c.json({
      groups,
      models: modelsList,
      default_id: '@cf/meta/llama-3.3-70b-instruct-fp8-fast'
    });
  } catch (err: any) {
    return c.json({ groups: {}, models: [] });
  }
});

app.get('/api/task-profiles', (c) => {
  return c.json({
    profiles: {
      shop_help: { label: 'Store Operations', description: 'PINKY_one store ops & deal BOYS' },
      coding: { label: 'Coding & Architecture', description: 'Engineering rules and code synthesis' },
      creative: { label: 'Creative & Strategy', description: 'Content and brand automation' }
    }
  });
});

app.post('/api/chat/stream', async (c) => {
  try {
    let text = '';
    let modelName = '@cf/meta/llama-3.3-70b-instruct-fp8-fast';
    let sysPrompt = 'You are EASTWOOD, an autonomous AI operator for Bonzo.';
    let conversationHistory: Array<{ role: string; content: string }> = [];

    const contentType = c.req.header('content-type') || '';
    if (contentType.includes('multipart/form-data') || contentType.includes('application/x-www-form-urlencoded')) {
      const form = await c.req.parseBody();
      text = (form['text'] as string) || (form['message'] as string) || '';
      if (form['model_name'] || form['model']) {
        modelName = (form['model_name'] as string) || (form['model'] as string);
      }
      if (form['custom_system_prompt']) {
        sysPrompt = form['custom_system_prompt'] as string;
      }
      if (form['messages']) {
        try {
          const rawMsgs = typeof form['messages'] === 'string' ? JSON.parse(form['messages'] as string) : form['messages'];
          if (Array.isArray(rawMsgs)) {
            conversationHistory = rawMsgs.map((m: any) => ({
              role: m.role === 'user' ? 'user' : 'assistant',
              content: m.content || m.text || ''
            })).filter((m: any) => m.content.trim().length > 0);
            if (!text && conversationHistory.length > 0) {
              const lastUser = [...conversationHistory].reverse().find(m => m.role === 'user');
              if (lastUser) text = lastUser.content;
            }
          }
        } catch {}
      }
    } else {
      const json: any = await c.req.json().catch(() => ({}));
      text = json.text || json.message || '';
      if (json.model_name || json.model) modelName = json.model_name || json.model;
      if (json.custom_system_prompt) sysPrompt = json.custom_system_prompt;
      if (Array.isArray(json.messages)) {
        conversationHistory = json.messages.map((m: any) => ({
          role: m.role === 'user' ? 'user' : 'assistant',
          content: m.content || m.text || ''
        })).filter((m: any) => m.content.trim().length > 0);
        if (!text && conversationHistory.length > 0) {
          const lastUser = [...conversationHistory].reverse().find(m => m.role === 'user');
          if (lastUser) text = lastUser.content;
        }
      }
    }

    if (!text && conversationHistory.length === 0) {
      return c.text('data: {"type":"error","text":"Empty message"}\n\n', 400);
    }

    // Build outbound messages for Hotspot / AI provider
    const outboundMessages: Array<{ role: string; content: string }> = [
      { role: 'system', content: sysPrompt }
    ];
    if (conversationHistory.length > 0) {
      outboundMessages.push(...conversationHistory);
    } else {
      outboundMessages.push({ role: 'user', content: text });
    }

    // Call Hotspot Chat via Worker fetch
    const hotspotPayload = {
      model: modelName,
      messages: outboundMessages
    };

    const hotspotReq = new Request('http://localhost/api/hotspot/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Hotspot-Token': c.req.header('X-Hotspot-Token') || 'hb_guest_public'
      },
      body: JSON.stringify(hotspotPayload)
    });

    const hotspotRes = await app.fetch(hotspotReq, c.env, c.executionCtx);
    if (!hotspotRes.ok) {
      const err = await hotspotRes.text();
      return c.text(`data: {"type":"error","text":"Hotspot error: ${err.replace(/"/g, "'")}"}\n\n`, 500);
    }

    const data: any = await hotspotRes.json();
    const assistantText = data.choices?.[0]?.message?.content || 'No response generated.';

    const sseChunks = [
      `data: {"type":"chunk","text":${JSON.stringify(assistantText)}}\n\n`,
      `data: {"type":"done","text":${JSON.stringify(assistantText)},"model_id":"${modelName}","provider":"hotspot"}\n\n`
    ].join('');

    return new Response(sseChunks, {
      status: 200,
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*'
      }
    });
  } catch (err: any) {
    return c.text(`data: {"type":"error","text":"${err.message}"}\n\n`, 500);
  }
});

app.get('/api/bridge/tasks', async (c) => {
  try {
    const { results } = await c.env.DB.prepare(
      "SELECT id, instruction, status, result, actor, created_at, updated_at FROM tasks ORDER BY created_at DESC LIMIT 25"
    ).all();
    return c.json(results || []);
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

app.get('/api/knowledge', (c) => {
  return c.json({ files: [] });
});

app.post('/api/knowledge/upload', (c) => {
  return c.json({ success: true, count: 0 });
});

app.post('/api/tts', (c) => {
  return c.text('EDGE_TTS_OFFLINE', 204);
});

app.get('/api/memory', (c) => {
  return c.json({ memory: 'Cloudflare Edge AI Mesh Active. Modele gotowe do pracy.' });
});

export default app;