import { Hono } from 'hono';
import { SmartRouterEngine } from '../providers/router';
import { generateBonzoKey } from './hotspot';

type Bindings = {
  DB: D1Database;
  AI: any;
  OMNIROUTE_URL?: string;
  OMNIROUTE_API_KEY?: string;
  GROQ_API_KEY?: string;
  GOOGLE_API_KEY?: string;
  OPENROUTER_API_KEY?: string;
  CEREBRAS_API_KEY?: string;
  SAMBANOVA_API_KEY?: string;
  MISTRAL_API_KEY?: string;
};

const mcp = new Hono<{ Bindings: Bindings }>();

// List of available MCP tools exposed by MyBonzo Edge Mesh
const MCP_TOOLS = [
  {
    name: 'execute_powershell_bridge',
    description: 'Executes a PowerShell command on the host machine via the secure Cloudflare-to-PC D1 Bridge.',
    inputSchema: {
      type: 'object',
      properties: {
        command: {
          type: 'string',
          description: 'The PowerShell command line to execute on the local workstation.'
        }
      },
      required: ['command']
    }
  },
  {
    name: 'query_ai_mesh',
    description: 'Routes an AI query through the failover cascade of free AI mesh providers (Cloudflare, Cerebras, SambaNova, Groq, Google).',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: {
          type: 'string',
          description: 'The user prompt or instruction for the AI.'
        },
        model: {
          type: 'string',
          description: 'Optional target model ID (defaults to auto-router).'
        }
      },
      required: ['prompt']
    }
  },
  {
    name: 'generate_license_key',
    description: 'Generates a K.R.A.F.T. Base32 license access key (format BNZ-XXXX-YYYY-ZZZZ-WWWW) for the MyBonzo Hotspot.',
    inputSchema: {
      type: 'object',
      properties: {
        client_name: {
          type: 'string',
          description: 'The name or label of the client receiving the license key.'
        },
        token_limit: {
          type: 'number',
          description: 'Max tokens allowed for this license (default 50,000, -1 for unlimited).'
        },
        tier: {
          type: 'string',
          description: 'License tier (starter, pro, dev, enterprise).'
        }
      },
      required: ['client_name']
    }
  },
  {
    name: 'get_bridge_telemetry',
    description: 'Fetches recent task execution logs and status from the local PowerShell bridge.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Number of recent tasks to retrieve (max 20).'
        }
      }
    }
  }
];

// MCP JSON-RPC 2.0 Handler
mcp.post('/', async (c) => {
  let body: any;
  try {
    body = await c.req.json();
  } catch {
    return c.json({ jsonrpc: '2.0', error: { code: -32700, message: 'Parse error' }, id: null }, 400);
  }

  const { jsonrpc, id, method, params } = body;

  if (jsonrpc !== '2.0') {
    return c.json({ jsonrpc: '2.0', error: { code: -32600, message: 'Invalid Request: jsonrpc must be 2.0' }, id: id || null }, 400);
  }

  switch (method) {
    case 'initialize': {
      return c.json({
        jsonrpc: '2.0',
        id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: {
            tools: {}
          },
          serverInfo: {
            name: 'mybonzo-edge-mcp-mesh',
            version: '1.0.0-KRAFT'
          }
        }
      });
    }

    case 'notifications/initialized': {
      return new Response(null, { status: 204 });
    }

    case 'tools/list': {
      return c.json({
        jsonrpc: '2.0',
        id,
        result: {
          tools: MCP_TOOLS
        }
      });
    }

    case 'tools/call': {
      const toolName = params?.name;
      const args = params?.arguments || {};

      try {
        if (toolName === 'execute_powershell_bridge') {
          const command = args.command;
          if (!command) {
            return c.json({ jsonrpc: '2.0', id, error: { code: -32602, message: 'Missing command parameter' } });
          }

          const taskId = 'task-mcp-' + Date.now() + '-' + Math.random().toString(36).substring(2, 6);
          await c.env.DB.prepare(
            "INSERT INTO tasks (id, instruction, status, actor) VALUES (?, ?, 'pending', 'MCP_CLIENT')"
          ).bind(taskId, command).run();

          return c.json({
            jsonrpc: '2.0',
            id,
            result: {
              content: [
                {
                  type: 'text',
                  text: `Task #${taskId} successfully queued to local PowerShell bridge. Command: ${command}`
                }
              ]
            }
          });
        }

        if (toolName === 'query_ai_mesh') {
          const prompt = args.prompt;
          const model = args.model;
          const engine = new SmartRouterEngine({
            DB: c.env.DB,
            AI: c.env.AI,
            OMNIROUTE_URL: c.env.OMNIROUTE_URL,
            OMNIROUTE_API_KEY: c.env.OMNIROUTE_API_KEY,
            GROQ_API_KEY: c.env.GROQ_API_KEY,
            GOOGLE_API_KEY: c.env.GOOGLE_API_KEY,
            OPENROUTER_API_KEY: c.env.OPENROUTER_API_KEY,
            CEREBRAS_API_KEY: c.env.CEREBRAS_API_KEY,
            SAMBANOVA_API_KEY: c.env.SAMBANOVA_API_KEY,
            MISTRAL_API_KEY: c.env.MISTRAL_API_KEY
          });

          const result = await engine.executeWithFallback(
            [{ role: 'user', content: prompt }],
            { model }
          );

          return c.json({
            jsonrpc: '2.0',
            id,
            result: {
              content: [
                {
                  type: 'text',
                  text: result.content
                }
              ],
              _meta: {
                provider: result.provider,
                model: result.model,
                latency_ms: result.latency_ms
              }
            }
          });
        }

        if (toolName === 'generate_license_key') {
          const clientName = args.client_name || 'MCP Client';
          const tokenLimit = args.token_limit || 50000;
          const tier = args.tier || 'pro';
          const key = generateBonzoKey();

          await c.env.DB.prepare(
            'INSERT INTO hotspot_tokens (token, name, tier, allowed_providers, allowed_models, token_limit, rate_limit_rpm) VALUES (?, ?, ?, ?, ?, ?, ?)'
          ).bind(key, clientName, tier, '*', '*', tokenLimit, 60).run();

          return c.json({
            jsonrpc: '2.0',
            id,
            result: {
              content: [
                {
                  type: 'text',
                  text: `Generated K.R.A.F.T. License Key: ${key} (Tier: ${tier}, Token Limit: ${tokenLimit})`
                }
              ]
            }
          });
        }

        if (toolName === 'get_bridge_telemetry') {
          const limit = Math.min(20, Math.max(1, args.limit || 5));
          const { results: tasks } = await c.env.DB.prepare(
            'SELECT id, instruction, status, result, created_at, updated_at FROM tasks ORDER BY created_at DESC LIMIT ?'
          ).bind(limit).all();

          return c.json({
            jsonrpc: '2.0',
            id,
            result: {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(tasks, null, 2)
                }
              ]
            }
          });
        }

        return c.json({ jsonrpc: '2.0', id, error: { code: -32601, message: `Tool not found: ${toolName}` } });
      } catch (err: any) {
        return c.json({
          jsonrpc: '2.0',
          id,
          result: {
            content: [
              {
                type: 'text',
                text: `[ERROR EXECUTING TOOL]: ${err.message}`
              }
            ],
            isError: true
          }
        });
      }
    }

    default:
      return c.json({ jsonrpc: '2.0', id, error: { code: -32601, message: `Method not found: ${method}` } }, 404);
  }
});

export default mcp;
