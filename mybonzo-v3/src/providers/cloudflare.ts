import { ChatMessage, ChatOptions, ProviderResult } from './types';

export const CLOUDFLARE_FREE_MODELS = [
  { id: '@cf/meta/llama-3.3-70b-instruct-fp8-fast', name: 'Llama 3.3 70B Fast (Workers AI)' },
  { id: '@cf/meta/llama-3.2-3b-instruct', name: 'Llama 3.2 3B (Workers AI Fast)' },
  { id: '@cf/meta/llama-3.2-1b-instruct', name: 'Llama 3.2 1B (Workers AI Micro)' }
];

export async function callCloudflareAI(
  ai: any,
  messages: ChatMessage[],
  options: ChatOptions = {}
): Promise<ProviderResult> {
  const start = Date.now();
  const model = options.model || '@cf/meta/llama-3.3-70b-instruct-fp8-fast';

  const formattedMessages = messages.map(m => ({
    role: m.role.toLowerCase() === 'developer' ? 'system' : m.role.toLowerCase(),
    content: typeof m.content === 'string' ? m.content : (m.content ? JSON.stringify(m.content) : '')
  }));

  const runPayload: any = {
    messages: formattedMessages,
    max_tokens: options.max_tokens || 4096,
    temperature: options.temperature ?? 0.7,
    rejectIfBusy: true
  };

  const res = await ai.run(model, runPayload);

  const latency = Date.now() - start;
  const content = res.response || res.answer || (typeof res === 'string' ? res : JSON.stringify(res));

  const promptTokens = Math.ceil(formattedMessages.reduce((acc, m) => acc + m.content.length, 0) / 4);
  const completionTokens = Math.ceil((content || '').length / 4);
  const totalTokens = promptTokens + completionTokens;
  const savedUsd = (totalTokens / 1_000_000) * 5.0;

  return {
    content,
    provider: 'cloudflare',
    model,
    latency_ms: latency,
    prompt_tokens: promptTokens,
    completion_tokens: completionTokens,
    total_tokens: totalTokens,
    saved_usd: Number(savedUsd.toFixed(6)),
    free: true,
    raw: res
  };
}
