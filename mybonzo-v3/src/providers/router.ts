import { ChatMessage, ChatOptions, ProviderResult, RoutingRequirement } from './types';
import { callCloudflareAI, CLOUDFLARE_FREE_MODELS } from './cloudflare';
import { callPollinationsAI, POLLINATIONS_MODELS } from './pollinations';
import { callAirforceAI, AIRFORCE_MODELS } from './airforce';
import { callOpenAICompat } from './openai-compat';
import { callOmniRoute, checkOmniRouteHealth, OMNIROUTE_DEFAULT_KEY, OMNIROUTE_DEFAULT_URL, OMNIROUTE_FREE_COMBOS } from './omniroute';

export interface RouterEnv {
  DB: any;
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
  GITHUB_TOKEN?: string;
}

export class SmartRouterEngine {
  constructor(private env: RouterEnv) {}

  private async getKeyFromDb(provider: string): Promise<string | null> {
    try {
      const row: any = await this.env.DB.prepare(
        "SELECT key_value FROM api_keys WHERE provider = ? AND is_active = 1 AND (cooldown_until IS NULL OR cooldown_until < CURRENT_TIMESTAMP) ORDER BY success_rate DESC LIMIT 1"
      ).bind(provider).first();
      return row?.key_value || null;
    } catch {
      return null;
    }
  }

  private async recordProviderSuccess(provider: string, latencyMs: number) {
    try {
      await this.env.DB.prepare(
        "UPDATE api_keys SET success_rate = MIN(1.0, success_rate + 0.05), avg_latency_ms = ? WHERE provider = ?"
      ).bind(latencyMs, provider).run();
    } catch {}
  }

  private async recordProviderFailure(provider: string) {
    try {
      await this.env.DB.prepare(
        "UPDATE api_keys SET success_rate = MAX(0.1, success_rate - 0.2), cooldown_until = datetime('now', '+5 minutes') WHERE provider = ?"
      ).bind(provider).run();
    } catch {}
  }

  private async logOperation(result: ProviderResult, agentId: string = 'op-01') {
    try {
      await this.env.DB.prepare(
        "INSERT INTO logs (agent_id, provider, model, tokens_used, cost_usd, action_type, timestamp) VALUES (?, ?, ?, ?, ?, 'free_tier_inference', CURRENT_TIMESTAMP)"
      ).bind(agentId, result.provider, result.model, result.total_tokens, 0.0).run();
    } catch {}
  }

  async executeWithFallback(
    messages: ChatMessage[],
    options: ChatOptions = {}
  ): Promise<ProviderResult> {
    const req: RoutingRequirement = options.requirement || 'free_unlimited';
    const errors: string[] = [];

    // Kolejność łańcucha fallback w zależności od profilu
    const executionChain: string[] = [];

    if (req === 'omniroute') {
      executionChain.push('omniroute', 'cloudflare_70b', 'cerebras', 'sambanova', 'pollinations', 'cloudflare_fast');
    } else if (req === 'speed') {
      executionChain.push('cerebras', 'cloudflare_fast', 'groq', 'sambanova', 'pollinations', 'cloudflare_70b');
    } else if (req === 'stability') {
      executionChain.push('cloudflare_70b', 'sambanova', 'google', 'groq', 'pollinations', 'omniroute');
    } else if (req === 'reasoning') {
      executionChain.push('cloudflare_70b', 'sambanova', 'pollinations_deepseek', 'google', 'omniroute');
    } else {
      // free_unlimited domyślnie: Cloudflare (z rejectIfBusy) -> Cerebras (1800 t/s) -> SambaNova -> Groq -> Google -> OpenRouter -> Fast -> Pollinations
      executionChain.push('cloudflare_70b', 'cerebras', 'sambanova', 'groq', 'google', 'openrouter', 'cloudflare_fast', 'pollinations', 'omniroute', 'airforce');
    }

    for (const step of executionChain) {
      try {
        let result: ProviderResult | null = null;

        if (step === 'cloudflare_70b') {
          result = await callCloudflareAI(this.env.AI, messages, {
            ...options,
            model: '@cf/meta/llama-3.3-70b-instruct-fp8-fast'
          });
        } else if (step === 'cloudflare_fast') {
          result = await callCloudflareAI(this.env.AI, messages, {
            ...options,
            model: '@cf/meta/llama-3.2-3b-instruct'
          });
        } else if (step === 'pollinations') {
          result = await callPollinationsAI(messages, {
            ...options,
            model: 'openai'
          });
        } else if (step === 'pollinations_deepseek') {
          result = await callPollinationsAI(messages, {
            ...options,
            model: 'deepseek'
          });
        } else if (step === 'omniroute') {
          const url = this.env.OMNIROUTE_URL || OMNIROUTE_DEFAULT_URL;
          const key = this.env.OMNIROUTE_API_KEY || (await this.getKeyFromDb('omniroute')) || OMNIROUTE_DEFAULT_KEY;
          const isHealthy = await checkOmniRouteHealth(url);
          if (isHealthy) {
            result = await callOmniRoute(url, key, messages, options);
          } else {
            throw new Error('OmniRoute endpoint not reachable from worker');
          }
        } else if (step === 'airforce') {
          result = await callAirforceAI(messages, options);
        } else if (step === 'groq') {
          const key = this.env.GROQ_API_KEY || (await this.getKeyFromDb('groq'));
          if (key) {
            result = await callOpenAICompat(
              {
                provider: 'groq',
                baseUrl: 'https://api.groq.com/openai/v1',
                apiKey: key,
                defaultModel: 'llama-3.3-70b-versatile'
              },
              messages,
              options
            );
          } else {
            throw new Error('Groq key not configured');
          }
        } else if (step === 'google') {
          const key = this.env.GOOGLE_API_KEY || (await this.getKeyFromDb('google'));
          if (key) {
            result = await callOpenAICompat(
              {
                provider: 'google',
                baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai',
                apiKey: key,
                defaultModel: 'gemini-2.0-flash'
              },
              messages,
              options
            );
          } else {
            throw new Error('Google Gemini key not configured');
          }
        } else if (step === 'cerebras') {
          const key = this.env.CEREBRAS_API_KEY || (await this.getKeyFromDb('cerebras'));
          if (key) {
            result = await callOpenAICompat(
              {
                provider: 'cerebras',
                baseUrl: 'https://api.cerebras.ai/v1',
                apiKey: key,
                defaultModel: 'llama-3.3-70b'
              },
              messages,
              options
            );
          } else {
            throw new Error('Cerebras key not configured');
          }
        } else if (step === 'sambanova') {
          const key = this.env.SAMBANOVA_API_KEY || (await this.getKeyFromDb('sambanova'));
          if (key) {
            result = await callOpenAICompat(
              {
                provider: 'sambanova',
                baseUrl: 'https://api.sambanova.ai/v1',
                apiKey: key,
                defaultModel: 'Meta-Llama-3.3-70B-Instruct'
              },
              messages,
              options
            );
          } else {
            throw new Error('SambaNova key not configured');
          }
        } else if (step === 'openrouter') {
          const key = this.env.OPENROUTER_API_KEY || (await this.getKeyFromDb('openrouter'));
          result = await callOpenAICompat(
            {
              provider: 'openrouter',
              baseUrl: 'https://openrouter.ai/api/v1',
              apiKey: key || 'free_anon',
              defaultModel: 'meta-llama/llama-3.3-70b-instruct:free',
              extraHeaders: {
                'HTTP-Referer': 'https://mybonzo.com',
                'X-Title': 'Bonzo Mesh'
              }
            },
            messages,
            options
          );
        } else if (step === 'mistral') {
          const key = this.env.MISTRAL_API_KEY || (await this.getKeyFromDb('mistral'));
          if (key) {
            result = await callOpenAICompat(
              {
                provider: 'mistral',
                baseUrl: 'https://api.mistral.ai/v1',
                apiKey: key,
                defaultModel: 'mistral-small-latest'
              },
              messages,
              options
            );
          } else {
            throw new Error('Mistral key not configured');
          }
        }

        if (result && result.content) {
          await this.recordProviderSuccess(result.provider, result.latency_ms);
          await this.logOperation(result);
          return result;
        }
      } catch (err: any) {
        errors.push(`[${step}] ${err.message}`);
        await this.recordProviderFailure(step);
      }
    }

    // Ostateczny fallback na Pollinations (zawsze bezkluczykowy)
    try {
      const fallback = await callPollinationsAI(messages, { model: 'openai' });
      await this.logOperation(fallback);
      return fallback;
    } catch (e: any) {
      throw new Error(`All free tier providers exhausted. Details: ${errors.join('; ')}`);
    }
  }

  async getCatalog(): Promise<any[]> {
    const catalog = [
      ...CLOUDFLARE_FREE_MODELS.map(m => ({ ...m, provider: 'cloudflare', is_free: true })),
      ...POLLINATIONS_MODELS.map(m => ({ ...m, provider: 'pollinations', is_free: true })),
      ...AIRFORCE_MODELS.map(m => ({ ...m, provider: 'airforce', is_free: true })),
      ...OMNIROUTE_FREE_COMBOS.map(m => ({ ...m, provider: 'omniroute', is_free: true }))
    ];
    return catalog;
  }
}
