import { SmartRouterEngine } from '../providers/router';
import { ChatMessage } from '../providers/types';

export interface MoaResult {
  output: string;
  chain: string[];
  stages: {
    stage: string;
    provider: string;
    model: string;
    latency_ms: number;
    tokens: number;
  }[];
  total_saved_usd: number;
  errors: string[];
}

export class FreeMoaEngine {
  private router: SmartRouterEngine;

  constructor(private db: any, private ai: any, private extraEnv: any = {}) {
    this.router = new SmartRouterEngine({
      DB: db,
      AI: ai,
      ...extraEnv
    });
  }

  async runTask(instruction: string): Promise<MoaResult> {
    const stages: MoaResult['stages'] = [];
    const chain: string[] = [];
    const errors: string[] = [];
    let totalSavedUsd = 0;

    // ETAP 1: Szybki szkic / Draft (Speed/Worker tier)
    let draft = '';
    try {
      const draftMessages: ChatMessage[] = [
        { role: 'system', content: 'You are a high-speed analytical assistant. Provide an initial concise technical draft answering the user instruction.' },
        { role: 'user', content: instruction }
      ];
      const draftRes = await this.router.executeWithFallback(draftMessages, {
        requirement: 'speed'
      });
      draft = draftRes.content;
      chain.push(draftRes.provider);
      totalSavedUsd += draftRes.saved_usd;
      stages.push({
        stage: '1_DRAFT',
        provider: draftRes.provider,
        model: draftRes.model,
        latency_ms: draftRes.latency_ms,
        tokens: draftRes.total_tokens
      });
    } catch (e: any) {
      errors.push(`Stage 1 error: ${e.message}`);
      draft = instruction;
    }

    // ETAP 2: Krytyczna analiza i rozszerzenie (Reasoning tier)
    let review = '';
    try {
      const reviewMessages: ChatMessage[] = [
        { role: 'system', content: 'You are a Senior Technical Reviewer. Analyze the following initial draft. Identify missing edge cases, improve precision, and provide necessary corrections.' },
        { role: 'user', content: `Original Task: ${instruction}\n\nInitial Draft:\n${draft}` }
      ];
      const reviewRes = await this.router.executeWithFallback(reviewMessages, {
        requirement: 'reasoning'
      });
      review = reviewRes.content;
      chain.push(reviewRes.provider);
      totalSavedUsd += reviewRes.saved_usd;
      stages.push({
        stage: '2_CRITIQUE',
        provider: reviewRes.provider,
        model: reviewRes.model,
        latency_ms: reviewRes.latency_ms,
        tokens: reviewRes.total_tokens
      });
    } catch (e: any) {
      errors.push(`Stage 2 error: ${e.message}`);
      review = draft;
    }

    // ETAP 3: Końcowa synteza (Synthesis / Golden Standard tier)
    let finalOutput = '';
    try {
      const synthMessages: ChatMessage[] = [
        { role: 'system', content: 'You are the Lead Solutions Architect. Synthesize the initial draft and the critical review into the final, polished, authoritative response. Output clean, ready-to-use information without conversational filler.' },
        { role: 'user', content: `Task: ${instruction}\n\nDraft:\n${draft}\n\nReview & Corrections:\n${review}` }
      ];
      const synthRes = await this.router.executeWithFallback(synthMessages, {
        requirement: 'stability'
      });
      finalOutput = synthRes.content;
      chain.push(synthRes.provider);
      totalSavedUsd += synthRes.saved_usd;
      stages.push({
        stage: '3_SYNTHESIS',
        provider: synthRes.provider,
        model: synthRes.model,
        latency_ms: synthRes.latency_ms,
        tokens: synthRes.total_tokens
      });
    } catch (e: any) {
      errors.push(`Stage 3 error: ${e.message}`);
      finalOutput = review || draft;
    }

    // Zapis do tabeli moa_logs w D1
    try {
      for (const stage of stages) {
        await this.db.prepare(
          "INSERT INTO moa_logs (model_id, provider, latency, status) VALUES (?, ?, ?, 'completed')"
        ).bind(stage.model, stage.provider, stage.latency_ms).run();
      }
      await this.db.prepare(
        "INSERT INTO logs (agent_id, provider, model, tokens_used, cost_usd, action_type, timestamp) VALUES ('moa-chain', 'moa_hybrid', 'multi-stage-synthesis', ?, 0.0, 'moa_synthesis', CURRENT_TIMESTAMP)"
      ).bind(stages.reduce((acc, s) => acc + s.tokens, 0)).run();
    } catch {}

    return {
      output: finalOutput,
      chain,
      stages,
      total_saved_usd: Number(totalSavedUsd.toFixed(6)),
      errors
    };
  }
}