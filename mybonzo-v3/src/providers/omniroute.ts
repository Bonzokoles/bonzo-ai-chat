import { ChatMessage, ChatOptions, ProviderResult } from './types';

export const OMNIROUTE_DEFAULT_URL = 'http://127.0.0.1:20128/v1';
export const OMNIROUTE_DEFAULT_KEY = ''; // set via Cloudflare Secret (env.OMNIROUTE_API_KEY)

export const OMNIROUTE_FREE_COMBOS = [
  { id: 'auto/best-free', name: 'OmniRoute — Best Free Tier (Auto-Rotation)' },
  { id: 'auto/coding:free', name: 'OmniRoute — Coding Free (Specialized)' },
  { id: 'auto/reasoning', name: 'OmniRoute — Reasoning (Auto-Fallback)' },
  { id: 'auto/fast', name: 'OmniRoute — Fast Speed Priority' },
  { id: 'auto/smart', name: 'OmniRoute — Smart Exploration' }
];

export async function checkOmniRouteHealth(baseUrl: string = OMNIROUTE_DEFAULT_URL): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);
    const url = `${baseUrl.replace(/\/+$/, '')}/models`;
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchOmniRouteModels(
  baseUrl: string = OMNIROUTE_DEFAULT_URL,
  apiKey: string = OMNIROUTE_DEFAULT_KEY
): Promise<any[]> {
  try {
    const url = `${baseUrl.replace(/\/+$/, '')}/models`;
    const res = await fetch(url, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    });
    if (!res.ok) return [];
    const data: any = await res.json();
    return data.data || [];
  } catch {
    return [];
  }
}

export async function callOmniRoute(
  baseUrl: string,
  apiKey: string,
  messages: ChatMessage[],
  options: ChatOptions = {}
): Promise<ProviderResult> {
  const start = Date.now();
  const model = options.model || 'auto/best-free';
  const url = `${baseUrl.replace(/\/+$/, '')}/chat/completions`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 45000);

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'X-Client': 'mybonzo-surgical-mesh'
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: options.temperature ?? 0.7,
        max_tokens: options.max_tokens || 2048
      }),
      signal: controller.signal
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`OmniRoute HTTP ${res.status}: ${errText.substring(0, 300)}`);
    }

    const data: any = await res.json();
    const latency = Date.now() - start;
    const content = data.choices?.[0]?.message?.content || '';

    const promptTokens = data.usage?.prompt_tokens || Math.ceil(JSON.stringify(messages).length / 4);
    const completionTokens = data.usage?.completion_tokens || Math.ceil(content.length / 4);
    const totalTokens = promptTokens + completionTokens;
    const savedUsd = (totalTokens / 1_000_000) * 5.0;

    return {
      content,
      provider: 'omniroute',
      model,
      latency_ms: latency,
      prompt_tokens: promptTokens,
      completion_tokens: completionTokens,
      total_tokens: totalTokens,
      saved_usd: Number(savedUsd.toFixed(6)),
      free: true,
      raw: data
    };
  } finally {
    clearTimeout(timeoutId);
  }
}
