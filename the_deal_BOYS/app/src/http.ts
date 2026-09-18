// Custom HTTP endpoints + statyczny web UI.
// VoltAgent używa hono pod spodem — registerCustomEndpoint dodaje route do istniejącego serwera.
import { registerCustomEndpoint } from "@voltagent/core";
import { dispatchToWorkers, pickWorkers } from "./dispatcher.js";
import { POLACZKI, type PolaczekName } from "./orchestrator.js";

const HTML_UI = `<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>Buch — Polaczki Workers</title>
<style>
  body { font: 14px/1.5 system-ui, sans-serif; max-width: 900px; margin: 30px auto; padding: 0 20px; color: #222; background: #fafafa; }
  h1 { color: #1a3a5c; }
  .box { background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 14px; margin: 10px 0; }
  textarea { width: 100%; min-height: 60px; font: inherit; box-sizing: border-box; padding: 8px; }
  button { background: #1a3a5c; color: #fff; border: 0; padding: 8px 16px; border-radius: 4px; cursor: pointer; font: inherit; }
  button:hover { background: #26527e; }
  .workers { font-size: 12px; color: #666; margin: 4px 0; }
  pre { background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }
  .worker-tag { display: inline-block; background: #e8f0f8; color: #1a3a5c; padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-right: 4px; }
  h2 { color: #444; font-size: 14px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
  .examples { font-size: 12px; color: #666; }
  .examples a { color: #1a3a5c; cursor: pointer; text-decoration: underline; margin-right: 12px; }
</style>
</head>
<body>
<h1>Buch — Polaczki Workers</h1>
<p>Supervisor + 5 Polaczków nad RAG <code>bonzo_private_strategy</code>. Wpisz pytanie — dispatcher (keyword router) wybiera 1+ workerów i scala odpowiedzi.</p>
<div class="examples">
  <strong>Przykłady:</strong>
  <a onclick="setExample('Mam wyciek w lejku B2C, gdzie szukać przyczyny?')">lejek B2C</a>
  <a onclick="setExample('Chcę sprzedawać produkt z Alibaba za 8$ na Amazon za 25$ — jaka realna marża?')">marża</a>
  <a onclick="setExample('Mogę użyć bota AI na WhatsApp do sprzedaży?')">WhatsApp + bohdah</a>
  <a onclick="setExample('Potrzebuję cennika progowego dla B2B, Net 30')">B2B</a>
</div>
<div class="box">
  <textarea id="q" placeholder="np. Chcę zbudować sklep od zera — co najpierw?"></textarea>
  <div style="margin-top: 8px">
    <button onclick="ask()">Wyślij</button>
    <button onclick="whoOnly()">Kto odpowie? (test routingu)</button>
  </div>
</div>
<div id="out"></div>
<script>
function setExample(t) { document.getElementById('q').value = t; }
async function ask() {
  const q = document.getElementById('q').value.trim();
  if (!q) return;
  document.getElementById('out').innerHTML = '<div class="box">Pytanie leci do 9router...</div>';
  try {
    const r = await fetch('/api/dispatch', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ prompt: q }) });
    const j = await r.json();
    const tags = (j.workers || []).map(w => '<span class="worker-tag">' + w + '</span>').join('');
    document.getElementById('out').innerHTML =
      '<div class="box">' +
        '<div class="workers">pracują: ' + tags + '</div>' +
        '<pre>' + escape(j.combined || j.error || 'brak odpowiedzi') + '</pre>' +
      '</div>';
  } catch (e) {
    document.getElementById('out').innerHTML = '<div class="box" style="color:red">błąd: ' + e.message + '</div>';
  }
}
async function whoOnly() {
  const q = document.getElementById('q').value.trim();
  if (!q) return;
  const r = await fetch('/api/who', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ prompt: q }) });
  const j = await r.json();
  const tags = (j.workers || []).map(w => '<span class="worker-tag">' + w + '</span>').join('');
  document.getElementById('out').innerHTML = '<div class="box"><div class="workers">' + tags + '</div></div>';
}
function escape(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
</script>
</body>
</html>`;

export function registerHttpEndpoints(): void {
	registerCustomEndpoint({
		path: "/",
		method: "get",
		handler: () =>
			new Response(HTML_UI, {
				headers: { "content-type": "text/html; charset=utf-8" },
			}),
	});

	registerCustomEndpoint({
		path: "/api/workers",
		method: "get",
		handler: () =>
			new Response(JSON.stringify(Object.keys(POLACZKI)), {
				headers: { "content-type": "application/json" },
			}),
	});

	registerCustomEndpoint({
		path: "/api/who",
		method: "post",
		handler: async (c) => {
			const body = (await c.req.json().catch(() => ({}))) as { prompt?: string };
			const workers = pickWorkers(body.prompt ?? "");
			return new Response(JSON.stringify({ workers }), {
				headers: { "content-type": "application/json" },
			});
		},
	});

	registerCustomEndpoint({
		path: "/api/dispatch",
		method: "post",
		handler: async (c) => {
			const body = (await c.req.json().catch(() => ({}))) as { prompt?: string };
			const prompt = body.prompt ?? "";
			if (!prompt) {
				return new Response(JSON.stringify({ error: "missing prompt" }), {
					status: 400,
					headers: { "content-type": "application/json" },
				});
			}
			try {
				const r = await dispatchToWorkers(prompt);
				return new Response(JSON.stringify(r), {
					headers: { "content-type": "application/json" },
				});
			} catch (err) {
				const msg = err instanceof Error ? err.message : String(err);
				return new Response(JSON.stringify({ error: msg }), {
					status: 500,
					headers: { "content-type": "application/json" },
				});
			}
		},
	});

	registerCustomEndpoint({
		path: "/api/health",
		method: "get",
		handler: () =>
			new Response(JSON.stringify({ status: "ok", workers: Object.keys(POLACZKI) }), {
				headers: { "content-type": "application/json" },
			}),
	});
}
