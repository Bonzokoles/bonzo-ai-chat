import { Hono } from 'hono';

const term = new Hono<{ Bindings: { DB: D1Database } }>();

term.post('/exec', async (c) => {
  try {
    const { command } = await c.req.json();
    if (!command || !command.trim()) {
      return c.json({ success: false, error: 'Command cannot be empty' }, 400);
    }
    const taskId = 'task-' + Date.now() + '-' + Math.random().toString(36).substring(2, 7);
    
    await c.env.DB.prepare(
      'INSERT INTO tasks (id, instruction, status, actor) VALUES (?, ?, "pending", "BONZO_UI")'
    ).bind(taskId, command.trim()).run();
    
    // Telemetry log
    try {
      await c.env.DB.prepare(
        'INSERT INTO audit_logs (action, actor, details) VALUES ("TERMINAL_EXEC", "BONZO_UI", ?)'
      ).bind(JSON.stringify({ taskId, command: command.trim() })).run();
    } catch (_) {}

    return c.json({ 
      success: true,
      taskId,
      status: "pending", 
      command: command.trim(),
      message: "Polecenie zsynchronizowane z mostkiem PowerShell."
    });
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

term.get('/status/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const task = await c.env.DB.prepare('SELECT * FROM tasks WHERE id = ?').bind(id).first();
    if (!task) {
      return c.json({ success: false, error: 'Task not found' }, 404);
    }
    return c.json({ success: true, task });
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

term.get('/tasks', async (c) => {
  try {
    const { results } = await c.env.DB.prepare(
      'SELECT id, instruction, status, result, actor, created_at, updated_at FROM tasks ORDER BY created_at DESC LIMIT 20'
    ).all();
    return c.json({ success: true, tasks: results || [] });
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

term.post('/launch-local', async (c) => {
  try {
    const taskId = 'task-launch-' + Date.now();
    const command = 'Start-Process -FilePath "M:\\CHATboxJIMBO\\start.bat"';
    
    await c.env.DB.prepare(
      'INSERT INTO tasks (id, instruction, status, actor) VALUES (?, ?, "pending", "BONZO_UI_LAUNCH")'
    ).bind(taskId, command).run();

    return c.json({
      success: true,
      taskId,
      targetUrl: 'http://localhost:4433',
      message: 'Zlecenie startu lokalnego JIMBO Chat zostalo wyslane do mostka.'
    });
  } catch (e: any) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

export default term;