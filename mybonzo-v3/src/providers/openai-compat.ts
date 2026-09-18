import { ChatMessage, ChatOptions, ProviderResult } from './types';

export interface OpenAICompatConfig {
  provider: string;
  baseUrl: string;
  apiKey: string;
  defaultModel: string;
  extraHeaders?: Record<string, string>;
  timeoutMs?: number;
}

export async function callOpenAICompat(
  config: OpenAICompatConfig,
  messages: ChatMessage[],
  options: ChatOptions = {}
): Promise<ProviderResult> {
  const start = Date.now();
  const model = options.model || config.defaultModel;
  const timeoutMs = config.timeoutMs || 30000;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  const url = config.baseUrl.endsWith('/chat/completions')
    ? config.baseUrl
    : `${config.baseUrl.replace(/\/+$/, '')}/chat/completions`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${config.apiKey}`,
    ...(config.extraHeaders || {})
  };

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        model,
        messages,
        temperature: options.temperature ?? 0.7,
        max_tokens: options.max_tokens || 1024
      }),
      signal: controller.signal
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`${config.provider} HTTP ${res.status}: ${errText.substring(0, 300)}`);
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
      provider: config.provider,
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
