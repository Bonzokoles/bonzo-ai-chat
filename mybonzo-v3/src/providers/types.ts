export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export type RoutingRequirement = 'speed' | 'stability' | 'reasoning' | 'free_unlimited' | 'omniroute';

export interface ChatOptions {
  model?: string;
  requirement?: RoutingRequirement;
  temperature?: number;
  max_tokens?: number;
  systemPrompt?: string;
}

export interface ProviderResult {
  content: string;
  provider: string;
  model: string;
  latency_ms: number;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  saved_usd: number;
  free: boolean;
  raw?: any;
}

export interface ModelCatalogEntry {
  id: string;
  display_name: string;
  provider_id: string;
  is_free: boolean;
  priority: number;
  context_window?: number;
  description?: string;
}

export interface ProviderStatus {
  id: string;
  name: string;
  type: 'edge' | 'keyless' | 'cloud_free_tier' | 'local_omniroute';
  status: 'online' | 'degraded' | 'offline';
  requires_key: boolean;
  models_count: number;
  notes: string;
}
