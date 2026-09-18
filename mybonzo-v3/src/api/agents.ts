import { Hono } from 'hono';
import { FreeMoaEngine } from '../agents/moa-engine';

const agents = new Hono<{
  Bindings: {
    DB: D1Database;
    AI: any;
    OMNIROUTE_URL?: string;
    OMNIROUTE_API_KEY?: string;
    GROQ_API_KEY?: string;
    GOOGLE_API_KEY?: string;
    OPENROUTER_API_KEY?: string;
    CEREBRAS_API_KEY?: string;
  };
}>();

// Uruchamianie darmowego łańcucha MOA (Mixture of Agents)
agents.post('/moa-run', async (c) => {
  try {
    const { instruction } = await c.req.json();
    if (!instruction) {
      return c.json({ error: 'Instruction is required' }, 400);
    }

    const engine = new FreeMoaEngine(c.env.DB, c.env.AI, {
      OMNIROUTE_URL: c.env.OMNIROUTE_URL,
      OMNIROUTE_API_KEY: c.env.OMNIROUTE_API_KEY,
      GROQ_API_KEY: c.env.GROQ_API_KEY,
      GOOGLE_API_KEY: c.env.GOOGLE_API_KEY,
      OPENROUTER_API_KEY: c.env.OPENROUTER_API_KEY,
      CEREBRAS_API_KEY: c.env.CEREBRAS_API_KEY
    });

    const result = await engine.runTask(instruction);

    const taskId = 'moa-' + Math.random().toString(36).substring(2, 6);
    try {
      await c.env.DB.prepare(
        'INSERT INTO tasks (id, agent_id, instruction, status, result) VALUES (?, "MOA_CHAIN", ?, "completed", ?)'
      ).bind(taskId, instruction, result.output).run();
    } catch {}

    return c.json({
      success: true,
      taskId,
      chain: result.chain,
      stages: result.stages,
      output: result.output,
      total_saved_usd: result.total_saved_usd,
      errors: result.errors
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

export default agents;