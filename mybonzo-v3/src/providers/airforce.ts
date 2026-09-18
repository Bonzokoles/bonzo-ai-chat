import { ChatMessage, ChatOptions, ProviderResult } from './types';

export const AIRFORCE_MODELS = [
  { id: 'llama-3.1-70b-chat', name: 'Llama 3.1 70B (Airforce 🆓)' },
  { id: 'deepseek-v3', name: 'DeepSeek V3 (Airforce 🆓)' },
  { id: 'chatgpt-4o-latest', name: 'GPT-4o (Airforce 🆓)' }
];

export async function callAirforceAI(
  messages: ChatMessage[],
  options: ChatOptions = {}
): Promise<ProviderResult> {
  const start = Date.now();
  const model = options.model || 'llama-3.1-70b-chat';

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 25000);

  try {
    const res = await fetch('https://api.airforce/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer missing'
      },
      body: JSON.stringify({
        messages,
        model,
        temperature: options.temperature ?? 0.7,
        max_tokens: options.max_tokens || 1024
      }),
      signal: controller.signal
    });

    if (!res.ok) {
      throw new Error(`Airforce HTTP ${res.status}: ${res.statusText}`);
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
      provider: 'airforce',
      model: `airforce/${model}`,
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
