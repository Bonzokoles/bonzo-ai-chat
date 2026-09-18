import { SmartRouterEngine } from '../providers/router';
import { RoutingRequirement } from '../providers/types';

export class OperationalCore {
  private router: SmartRouterEngine;

  constructor(private db: any, private ai?: any, private extraEnv: any = {}) {
    this.router = new SmartRouterEngine({
      DB: db,
      AI: ai,
      ...extraEnv
    });
  }

  async getMeshStatus() {
    const stats = await this.db.prepare(
      'SELECT SUM(cost_usd) as total_cost, SUM(tokens_used) as total_tokens FROM logs'
    ).first();

    const activeKeys = await this.db.prepare(
      'SELECT COUNT(*) as count FROM api_keys WHERE is_active = 1 AND (cooldown_until IS NULL OR cooldown_until < CURRENT_TIMESTAMP)'
    ).first();

    const modelsCount = await this.db.prepare(
      'SELECT COUNT(*) as count FROM model_catalog WHERE is_free = 1'
    ).first();

    return {
      system: 'OperationalCore V4 (Surgical Multi-Provider Mesh)',
      status: 'active',
      stats: stats || { total_cost: 0, total_tokens: 0 },
      active_free_slots: (activeKeys?.count || 0) + 3, // D1 keys + native Cloudflare + Pollinations + Airforce
      catalog_free_models: modelsCount?.count || 0,
      providers: [
        { id: 'cloudflare', name: 'Cloudflare Workers AI (Edge Native)', status: 'online', keyless: true },
        { id: 'pollinations', name: 'Pollinations AI (Keyless Free)', status: 'online', keyless: true },
        { id: 'airforce', name: 'Airforce Free Gateway', status: 'online', keyless: true },
        { id: 'omniroute', name: 'OmniRoute Gateway (Local/Tunnel)', status: 'connected', port: 20128 },
        { id: 'groq', name: 'Groq Cloud (Ultra-Fast LPUs)', status: 'configured', keyless: false },
        { id: 'google', name: 'Google Gemini Studio (1M Context)', status: 'configured', keyless: false },
        { id: 'openrouter', name: 'OpenRouter Free Tier (:free)', status: 'configured', keyless: false },
        { id: 'cerebras', name: 'Cerebras Inference (WSE-3)', status: 'configured', keyless: false }
      ]
    };
  }

  async selectBestFreeModel(taskType: RoutingRequirement = 'free_unlimited') {
    let targetProvider = 'cloudflare';
    let targetModel = '@cf/meta/llama-3.1-8b-instruct';
    let reasoning = 'Edge-native inference with lowest TTFB latency';

    if (taskType === 'omniroute') {
      targetProvider = 'omniroute';
      targetModel = 'auto/best-free';
      reasoning = 'Local OmniRoute combo with 115+ provider fallback rotation';
    } else if (taskType === 'speed') {
      targetProvider = 'groq';
      targetModel = 'llama-3.3-70b-versatile';
      reasoning = 'Ultra-low latency hardware acceleration via Groq LPU';
    } else if (taskType === 'stability') {
      targetProvider = 'google';
      targetModel = 'gemini-2.0-flash';
      reasoning = 'High reliability and large context window via Google Gemini';
    } else if (taskType === 'reasoning') {
      targetProvider = 'cloudflare';
      targetModel = '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b';
      reasoning = 'Distilled reasoning model running on edge GPU infrastructure';
    }

    const key = await this.db.prepare(
      "SELECT id, provider, key_value FROM api_keys WHERE provider = ? AND is_active = 1 AND (cooldown_until IS NULL OR cooldown_until < CURRENT_TIMESTAMP) ORDER BY success_rate DESC LIMIT 1"
    ).bind(targetProvider).first();

    return {
      requirement: taskType,
      provider: targetProvider,
      model: targetModel,
      reasoning,
      has_direct_key: !!key,
      fallback_available: true
    };
  }

  async logAction(agentId: string, provider: string, model: string, tokens: number, costUsd: number, actionType: string = 'api_call') {
    try {
      await this.db.prepare(
        "INSERT INTO logs (agent_id, provider, model, tokens_used, cost_usd, action_type, timestamp) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)"
      ).bind(agentId, provider, model, tokens, costUsd, actionType).run();
    } catch {}
  }
}