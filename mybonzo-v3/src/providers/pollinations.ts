import { ChatMessage, ChatOptions, ProviderResult } from './types';

export const POLLINATIONS_MODELS = [
  { id: 'openai', name: 'GPT-4o Mini (Pollinations 🆓)' },
  { id: 'mistral', name: 'Mistral Nemo (Pollinations 🆓)' },
  { id: 'deepseek', name: 'DeepSeek V3 (Pollinations 🆓)' },
  { id: 'qwen', name: 'Qwen 2.5 72B (Pollinations 🆓)' }
];

export async function callPollinationsAI(
  messages: ChatMessage[],
  options: ChatOptions = {}
): Promise<ProviderResult> {
  const start = Date.now();
  const model = options.model || 'openai';

  const fullPrompt = messages
    .map(m => `${m.role.toUpperCase()}: ${m.content}`)
    .join('\n\n') + '\n\nASSISTANT:';

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 20000);

  try {
    const encodedPrompt = encodeURIComponent(fullPrompt);
    const url = `https://text.pollinations.ai/${encodedPrompt}?model=${encodeURIComponent(model)}&seed=${Math.floor(Math.random() * 100000)}`;

    const res = await fetch(url, {
      method: 'GET',
      signal: controller.signal
    });

    if (!res.ok) {
      throw new Error(`Pollinations HTTP ${res.status}: ${res.statusText}`);
    }

    const content = await res.text();
    const latency = Date.now() - start;

    const promptTokens = Math.ceil(fullPrompt.length / 4);
    const completionTokens = Math.ceil((content || '').length / 4);
    const totalTokens = promptTokens + completionTokens;
    const savedUsd = (totalTokens / 1_000_000) * 5.0;

    return {
      content,
      provider: 'pollinations',
      model: `pollinations/${model}`,
      latency_ms: latency,
      prompt_tokens: promptTokens,
      completion_tokens: completionTokens,
      total_tokens: totalTokens,
      saved_usd: Number(savedUsd.toFixed(6)),
      free: true
    };
  } finally {
    clearTimeout(timeoutId);
  }
}
