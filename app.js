/* EastWood Ops — app.js */
'use strict';

const readStored = (primaryKey, legacyKey, fallback = '') => {
  const primary = localStorage.getItem(primaryKey);
  if (primary !== null) return primary;
  if (legacyKey) {
    const legacy = localStorage.getItem(legacyKey);
    if (legacy !== null) return legacy;
  }
  return fallback;
};

const UI = {
  appName: 'EastWood Ops',
  assistantName: 'EASTWOOD',
  userName: 'Bonzo',
  kbLabel: 'KNOWLEDGE MOOD',
  defaultSystemPrompt: '',
  taskProfiles: {},
  defaultTaskProfile: 'shop_help',
};

const defaultApi = (typeof window !== 'undefined' && window.location.hostname && !['localhost', '127.0.0.1'].includes(window.location.hostname))
  ? 'https://mybonzo-v3.stolarnia-ams.workers.dev'
  : 'http://localhost:4149';

const S = {
  apiBase: readStored('eastwood-api', 'jimbo-api', defaultApi),
  model: readStored('eastwood-model', 'jimbo-model', ''),
  taskProfile: readStored('eastwood-task-profile', null, 'shop_help'),
  temperature: parseFloat(readStored('eastwood-temp', 'jimbo-temp', '0.6')),
  topP: parseFloat(readStored('eastwood-topp', 'jimbo-topp', '0.9')),
  maxTokens: parseInt(readStored('eastwood-maxtok', 'jimbo-maxtok', '1024')),
  useTools: readStored('eastwood-tools', 'jimbo-tools', 'true') !== 'false',
  autoTts: readStored('eastwood-auto-tts', 'jimbo-auto-tts', 'true') !== 'false',
  voiceMode: readStored('eastwood-voice-mode', 'jimbo-voice-mode', 'true') !== 'false',
  systemPrompt: readStored('eastwood-sysprompt', 'jimbo-sysprompt', ''),
  theme: readStored('eastwood-theme', 'jimbo-theme', 'blackout'),
  messages: [],       // active conversation
  conversations: [],  // saved in localStorage
  activeConvId: null,
  attachedFiles: [],
  isLoading: false,
  term: null,
  termWs: null,
  termOpen: false,
  termReconnectTimer: null,
  termReconnectAttempts: 0,
  pendingTermCmd: null,
  recognition: null,
  isRecording: false,
  sessionTokens: 0,
};

const THEMES = ['bugatti', 'hashicorp', 'midnight', 'blackout'];
const THEME_VARS = {
  midnight: { bg: '#02060c', cardBg: '#050b14', border: '#1f3b63', accent: '#2ee6ff', dim: '#5aa0b0', text: '#ddf8ff', userBg: '#07101b' },
  bugatti:  { bg: '#05060a', cardBg: '#0b0d12', border: '#2d3444', accent: '#7b88f0', dim: '#7d8aa6', text: '#f1f5ff', userBg: '#0d1426' },
  hashicorp:{ bg: '#0a0602', cardBg: '#14100b', border: '#4d3320', accent: '#ff9d2f', dim: '#b98958', text: '#fff1dd', userBg: '#1b120a' },
  blackout: { bg: '#000000', cardBg: '#050505', border: '#3a3a3a', accent: '#ffffff', dim: '#a8a8a8', text: '#ffffff', userBg: '#0b0b0b' },
};

let DEFAULT_SYSTEM = `Jesteś EASTWOOD (BUCH / JIMBO) – Senior Software Architect & Automation Guru operujący w ekosystemie Bonzo (standard K.R.A.F.T. v3).

ROLA I ARCHITEKTURA STANOWISKA:
- Pracujesz w centrum dowodzenia The Buch (EastWood Ops, port 4149).
- Twoim partnerem i zleceniodawcą jest Bonzo.
- Masz zintegrowane dwa okna operacyjne: Chat AI (po lewej) oraz interaktywny terminal PowerShell 7 Core (pwsh.exe po prawej z obsługą PTY).
- Ignorujesz uprzejmości i marketingowy bełkot. Działasz z chirurgiczną precyzją techniczną.
- Używaj tagów statusu: [OK], [RUN], [WARN], [ERR]. Kategoryczny zakaz używania emoji.
- Odpowiedzi formułujesz konkretnie: wskazujesz dokładny plik, logikę i gotową komendę CLI.

INTEGRACJA Z TERMINALEM POWERSHELL (PRAWE OKNO):
- Prawy panel to natywna sesja PowerShell 7 Core (pwsh.exe) w katalogu roboczym.
- Gdy proponujesz uruchomienie skryptu, testu, komendy diagnostycznej lub polecenia CLI, ZAWSZE umieszczaj je w bloku kodu \`\`\`powershell.
- Interfejs The Buch wyposażony jest w przycisk [run] przy każdym bloku kodu powłoki – Bonzo może jednym kliknięciem wysłać polecenie bezpośrednio do terminala.
- Zawsze podawaj kompletne ścieżki i parametry, aby polecenie było natychmiast wykonywalne bez poprawek.

MAPA EKOSYSTEMU, DYSKÓW I NARZĘDZI:
1. Z:\\.Goose_agent\\ — Centrum Skryptów i Launcherów (START_THE_BUCH.ps1, START_AGENT_PI_MYBONZO.ps1, check_env.ps1, test_gateway.ps1).
2. Z:\\36_chambers\\The_Buch\\ — Baza The Buch (FastAPI + Chat + Terminal, MyBonzo Cloudflare AI).
3. U:\\WWW_Zen_BRo_wser_tool\\ — Hub Narzędziowy i Silnik ETL (meblepumo.db, AGENT_Pi_TOOLS, diff_processor.py, JIMBOKIT_COMMS).
4. U:\\WWW_Zen_BRo_wser_org3\\ — ZENO Browser (Electron 27, Cloudflare Pages zeno-browser-web, D1 zeno-browser-db, R2 zen-static-assets).
5. F:\\GENINI_ANTGRAV\\workspace\\ — Główny obszar roboczy projektów.
6. R:\\repos\\active\\ — Repozytoria Git. Pamięć: R:\\mempalace\\.

WYTYCZNE OPERACYJNE DLA ODPOWIEDZI:
- Komunikacja z Bonzo w języku polskim. Kod, nazwy zmiennych, ścieżki i zapytania SQL po angielsku.
- Zero pustych pytań na końcu typu "Co o tym sądzisz?". Kończ konkretnym werdyktem, gotową komendą PowerShell do uruchomienia lub kolejnym krokiem wdrożeniowym.`;

// ── DOM refs ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const el = {
  appRoot:      $('app'),
  statusDot:    $('status-dot'),
  statusText:   $('status-text'),
  modelSelect:  $('model-select'),
  taskProfileSelect: $('task-profile-select'),
  apiUrl:       $('api-url-input'),
  messages:     $('messages'),
  messagesWrap: $('messages-wrap'),
  typing:       $('typing'),
  msgInput:     $('msg-input'),
  btnSend:      $('btn-send'),
  btnAttach:    $('btn-attach'),
  fileInput:    $('file-input'),
  btnVoice:     $('btn-voice'),
  attachedFiles:$('attached-files'),
  historyList:  $('history-list'),
  kbList:       $('kb-list'),
  kbFileInput:  $('kb-file-input'),
  sttFileInput: $('stt-file-input'),
  tempSlider:   $('sl-temperature'),
  toppSlider:   $('sl-topp'),
  maxTokSlider: $('sl-maxtok'),
  tempVal:      $('temp-val'),
  toppVal:      $('topp-val'),
  maxTokVal:    $('maxtok-val'),
  cbTools:      $('cb-tools'),
  sysPrompt:    $('system-prompt'),
  termPanel:    $('term-panel'),
  rightbar:     $('rightbar'),
  termDot:      $('term-dot'),
  termStatusTxt:$('term-status-text'),
  termContainer:$('term-container'),
  ttsStyleSelect:$('tts-style-select'),
  cbAutoTts:    $('cb-auto-tts'),
};

// ── Init ───────────────────────────────────────────────────────────────────
async function init() {
  await loadUiConfig();
  applyTheme(S.theme);
  restoreSettings();
  initVoxToggle();
  initTermResize();
  loadConversations();
  renderHistory();
  setupEventListeners();
  await checkHealth();
  setInterval(checkHealth, 15000);
  await loadTaskProfiles();
  await loadModels();
  loadKB();
  refreshDiagnostics();
  newConversation(true); // silent — start fresh
}

async function loadUiConfig() {
  try {
    const r = await fetch(`${S.apiBase}/api/ui-config`, { signal: AbortSignal.timeout(4000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const cfg = await r.json();
    Object.assign(UI, {
      appName: cfg.app_name || UI.appName,
      assistantName: cfg.assistant_name || UI.assistantName,
      userName: cfg.user_name || UI.userName,
      kbLabel: cfg.kb_label || UI.kbLabel,
      taskProfiles: cfg.task_profiles || UI.taskProfiles,
      defaultSystemPrompt: cfg.default_system_prompt || DEFAULT_SYSTEM,
    });
    DEFAULT_SYSTEM = UI.defaultSystemPrompt;
  } catch {
    UI.defaultSystemPrompt = DEFAULT_SYSTEM;
  }
  applyUiConfig();
}

function applyUiConfig() {
  document.title = UI.appName;
  const logoText = $('app-title');
  if (logoText) logoText.textContent = UI.assistantName;
  const panelTitle = $('panel-title');
  if (panelTitle) panelTitle.textContent = `${UI.appName.toUpperCase()} PANEL`;
  const promptTitle = $('prompt-title');
  if (promptTitle) promptTitle.textContent = `${UI.assistantName} PROMPT`;
  const kbTitle = $('kb-title');
  if (kbTitle) kbTitle.textContent = UI.kbLabel;
  const resetPromptBtn = $('btn-reset-prompt');
  if (resetPromptBtn) resetPromptBtn.textContent = 'RESET PROMPT';
  if (el.sysPrompt) {
    el.sysPrompt.placeholder = `Custom system prompt... (puste = domyślny prompt ${UI.assistantName})`;
  }
}

// ── Settings ───────────────────────────────────────────────────────────────
function restoreSettings() {
  el.apiUrl.value = S.apiBase;
  if (el.taskProfileSelect) el.taskProfileSelect.value = S.taskProfile;
  el.tempSlider.value = S.temperature;
  el.toppSlider.value = S.topP;
  el.maxTokSlider.value = S.maxTokens;
  el.tempVal.textContent = S.temperature;
  el.toppVal.textContent = S.topP;
  el.maxTokVal.textContent = S.maxTokens;
  el.cbTools.checked = S.useTools;
  if (el.cbAutoTts) el.cbAutoTts.checked = S.autoTts;
  el.sysPrompt.value = S.systemPrompt;
}

function saveSettings() {
  localStorage.setItem('eastwood-api', S.apiBase);
  localStorage.setItem('eastwood-model', S.model);
  localStorage.setItem('eastwood-task-profile', S.taskProfile);
  localStorage.setItem('eastwood-temp', S.temperature);
  localStorage.setItem('eastwood-topp', S.topP);
  localStorage.setItem('eastwood-maxtok', S.maxTokens);
  localStorage.setItem('eastwood-tools', S.useTools);
  localStorage.setItem('eastwood-auto-tts', S.autoTts);
  localStorage.setItem('eastwood-voice-mode', S.voiceMode);
  localStorage.setItem('eastwood-sysprompt', S.systemPrompt);
  localStorage.setItem('eastwood-theme', S.theme);
}

// ── Health ─────────────────────────────────────────────────────────────────
async function checkHealth() {
  const t0 = performance.now();
  try {
    const r = await fetch(`${S.apiBase}/api/health`, { signal: AbortSignal.timeout(4000) });
    const latency = Math.round(performance.now() - t0);
    if (r.ok) {
      const d = await r.json();
      const provName = d.provider === 'mybonzo' ? 'MYBONZO EDGE' : (d.provider || 'ONLINE').toUpperCase();
      if (el.statusDot) {
        el.statusDot.className = 'dot dot-green';
        el.statusDot.style.background = '#00E6A8';
        el.statusDot.style.boxShadow = '0 0 8px #00E6A8';
      }
      if (el.statusText) {
        el.statusText.textContent = `ONLINE · ${provName} [${d.mcp_tools} TOOLS]`;
        el.statusText.style.color = '#00E6A8';
      }
      const pingEl = $('ping-badge');
      if (pingEl) pingEl.textContent = `${latency}ms`;
      const badge = $('conn-badge');
      if (badge) badge.style.borderColor = '#00E6A8';

      // Update Sidebar Telemetry LEDs
      const ledKey = $('led-key-status');
      const ledAi = $('led-ai-status');
      const ledMesh = $('led-mesh-status');
      const ledD1 = $('led-d1-status');
      if (ledKey) ledKey.textContent = d.key_tier || 'ROOT 2026';
      if (ledAi) ledAi.textContent = 'ONLINE (CF)';
      if (ledMesh) ledMesh.textContent = `${d.mesh_nodes || 6} PROVIDERS`;
      if (ledD1) ledD1.textContent = 'CONNECTED';
    } else throw new Error('bad status');
  } catch {
    if (el.statusDot) {
      el.statusDot.className = 'dot dot-red';
      el.statusDot.style.background = '#ef4444';
      el.statusDot.style.boxShadow = '0 0 8px #ef4444';
    }
    if (el.statusText) {
      el.statusText.textContent = 'OFFLINE · NO CONNECTION';
      el.statusText.style.color = '#ef4444';
    }
    const pingEl = $('ping-badge');
    if (pingEl) pingEl.textContent = 'ERR';
    const badge = $('conn-badge');
    if (badge) badge.style.borderColor = '#ef4444';

    const ledAi = $('led-ai-status');
    if (ledAi) ledAi.textContent = 'OFFLINE';
    const ledMesh = $('led-mesh-status');
    if (ledMesh) ledMesh.textContent = 'STANDALONE';
  }
}

// ── Models ─────────────────────────────────────────────────────────────────
async function loadModels() {
  try {
    const r = await fetch(`${S.apiBase}/api/models`);
    const data = await r.json();
    el.modelSelect.innerHTML = '';

    // data can be {groups: {ProviderName: [model, ...]}} or flat list
    if (data.groups) {
      for (const [provider, models] of Object.entries(data.groups)) {
        const grp = document.createElement('optgroup');
        grp.label = provider;
        models.forEach(m => {
          const opt = document.createElement('option');
          const name = typeof m === 'string' ? m : (m.name || m);
          opt.value = typeof m === 'object' ? (m.id || m.name || m) : m;
          opt.textContent = name;
          grp.appendChild(opt);
        });
        el.modelSelect.appendChild(grp);
      }
    } else {
      // flat list or dict {displayName: modelId}
      const entries = Array.isArray(data)
        ? data.map(m => [m, m])
        : Object.entries(data);
      entries.forEach(([name, id]) => {
        const opt = document.createElement('option');
        opt.value = id;
        opt.textContent = name;
        el.modelSelect.appendChild(opt);
      });
    }

    // restore saved model
    if (S.model) {
      el.modelSelect.value = S.model;
      if (!el.modelSelect.value) el.modelSelect.selectedIndex = 0;
    } else if (data.default_id) {
      el.modelSelect.value = data.default_id;
      if (!el.modelSelect.value) el.modelSelect.selectedIndex = 0;
    } else {
      el.modelSelect.selectedIndex = 0;
    }
    S.model = el.modelSelect.value;
  } catch (e) {
    el.modelSelect.innerHTML = '<option value="">— offline —</option>';
  }
}

async function loadTaskProfiles() {
  try {
    const r = await fetch(`${S.apiBase}/api/task-profiles`);
    const data = await r.json();
    UI.taskProfiles = data.profiles || {};
    UI.defaultTaskProfile = data.default || 'shop_help';
    if (!el.taskProfileSelect) return;
    el.taskProfileSelect.innerHTML = '';
    Object.entries(UI.taskProfiles).forEach(([key, profile]) => {
      const opt = document.createElement('option');
      opt.value = key;
      opt.textContent = profile.label || key;
      opt.title = profile.description || '';
      el.taskProfileSelect.appendChild(opt);
    });
    const preferred = S.taskProfile || UI.defaultTaskProfile;
    el.taskProfileSelect.value = preferred;
    if (!el.taskProfileSelect.value) el.taskProfileSelect.value = UI.defaultTaskProfile;
    S.taskProfile = el.taskProfileSelect.value || UI.defaultTaskProfile;
  } catch {
    if (el.taskProfileSelect) {
      el.taskProfileSelect.innerHTML = '<option value="shop_help">Shop Help</option>';
      el.taskProfileSelect.value = 'shop_help';
    }
    S.taskProfile = 'shop_help';
  }
}

// ── Token Telemetry ────────────────────────────────────────────────────────
function updateTokenTelemetry(addedTokens = 0, speed = 0) {
  S.sessionTokens = (S.sessionTokens || 0) + addedTokens;
  const countEl = $('sb-tokens-count');
  const fillEl = $('sb-token-fill');
  const speedEl = $('sb-token-est');
  if (countEl) {
    const k = S.sessionTokens >= 1000 ? (S.sessionTokens / 1000).toFixed(1) + 'k' : S.sessionTokens;
    countEl.textContent = `${k} / 50k`;
  }
  if (fillEl) {
    const pct = Math.min(100, Math.round((S.sessionTokens / 50000) * 100));
    fillEl.style.width = `${Math.max(2, pct)}%`;
  }
  if (speedEl && speed > 0) {
    speedEl.textContent = `~${speed} T/s`;
  }
}

// ── API Chat ───────────────────────────────────────────────────────────────
async function sendMessage(text, files = []) {
  if (S.isLoading) return;
  text = text.trim();
  if (!text && !files.length) return;

  if (text === '/clear') { clearChat(); return; }

  S.isLoading = true;
  if (el.appRoot) el.appRoot.classList.add('model-busy');
  el.btnSend.disabled = true;

  // Add user message
  const userMsg = { role: 'user', text, ts: Date.now() };
  S.messages.push(userMsg);
  renderMessage(userMsg);
  autoSaveConversation();
  scrollBottom();

  // Track tokens for prompt
  const userToks = Math.max(1, Math.round((text.length + files.length * 120) / 3.8));
  updateTokenTelemetry(userToks, 0);
  const streamStartTime = performance.now();
  let generatedChars = 0;

  // Show typing
  el.typing.classList.add('visible');
  scrollBottom();

  try {
    const form = new FormData();
    const apiMessages = S.messages.slice(-20).map(m => ({
      role: m.role === 'user' ? 'user' : 'assistant',
      text: m.text,
    }));
    form.append('messages', JSON.stringify(apiMessages));
    form.append('use_tools', S.useTools);
    form.append('max_tokens', S.maxTokens);
    form.append('temperature', S.temperature);
    form.append('top_p', S.topP);
    if (S.model) form.append('model_name', S.model);
    if (S.taskProfile) form.append('task_profile', S.taskProfile);

    const sysPrompt = el.sysPrompt.value.trim();
    if (sysPrompt) form.append('custom_system_prompt', sysPrompt);

    files.forEach(f => form.append('files', f));

    const r = await fetch(`${S.apiBase}/api/chat/stream`, { method: 'POST', body: form });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);

      const assistantMsg = {
        role: 'assistant',
        text: '',
        ts: Date.now(),
        toolCalls: [],
        uploadedFiles: [],
        kbScope: [],
        kbSources: [],
        charScope: [],
        useCharacterExamples: true,
        provider: '',
      modelId: '',
      modelDisplay: '',
      modelRequested: '',
      taskProfile: S.taskProfile || '',
      taskProfileLabel: '',
    };
    S.messages.push(assistantMsg);
    const bubble = renderMessage(assistantMsg);
    const textEl = bubble.querySelector('.msg-text');
    el.typing.classList.remove('visible');
    scrollBottom();
    const reader = r.body.getReader();
    const decoder = new TextDecoder();
    let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const ev = JSON.parse(line.slice(6));
          if (ev.type === 'chunk') {
            assistantMsg.text += ev.text;
            generatedChars += ev.text.length;
            textEl.innerHTML = renderMarkdown(assistantMsg.text);
            scrollBottom();
            } else if (ev.type === 'done') {
              assistantMsg.text = ev.text;
              assistantMsg.toolCalls = ev.tool_calls || [];
              assistantMsg.uploadedFiles = ev.uploaded_files || [];
              assistantMsg.kbScope = ev.kb_scope || [];
              assistantMsg.kbSources = ev.kb_sources || [];
              assistantMsg.charScope = ev.char_scope || [];
              assistantMsg.useCharacterExamples = ev.use_character_examples !== false;
              assistantMsg.provider = ev.provider || '';
            assistantMsg.modelId = ev.model_id || '';
            assistantMsg.modelDisplay = ev.model_display || '';
            assistantMsg.modelRequested = ev.model_requested || '';
            assistantMsg.taskProfile = ev.task_profile || assistantMsg.taskProfile || '';
            assistantMsg.taskProfileLabel = ev.task_profile_label || '';
            textEl.innerHTML = renderMarkdown(assistantMsg.text);
            refreshMessageMeta(bubble, assistantMsg);

            // Compute generation speed and completion tokens
            const completionToks = Math.max(1, Math.round(generatedChars / 3.8));
            const elapsed = Math.max(0.1, (performance.now() - streamStartTime) / 1000);
            const tokPerSec = Math.round(completionToks / elapsed);
            updateTokenTelemetry(completionToks, tokPerSec);
          }
        } catch {}
      }
    }
    autoSaveConversation();
    scrollBottom();

    // Update history title from first user message
    if (S.messages.filter(m => m.role === 'user').length === 1) {
      updateConvTitle(text.slice(0, 60));
    }
    if (S.voiceMode) {
      playTtsText(assistantMsg.text);
    }
  } catch (e) {
    el.typing.classList.remove('visible');
    addSystemMsg(`Błąd: ${e.message}`);
  } finally {
    S.isLoading = false;
    if (el.appRoot) el.appRoot.classList.remove('model-busy');
    el.btnSend.disabled = false;
    S.attachedFiles = [];
    el.attachedFiles.innerHTML = '';
    el.fileInput.value = '';
  }
}

// ── Render Messages ─────────────────────────────────────────────────────────
function renderMessage(msg) {
  const div = document.createElement('div');
  div.className = `msg msg-${msg.role}`;
  div.dataset.ts = msg.ts;

  const avatarSvg = msg.role === 'user'
    ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5zm0 2c-4.4 0-8 2.2-8 5v1h16v-1c0-2.8-3.6-5-8-5z"/></svg>'
    : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 3h8v3h2a2 2 0 0 1 2 2v7a4 4 0 0 1-4 4h-1v2h-2v-2h-2v2H9v-2H8a4 4 0 0 1-4-4V8a2 2 0 0 1 2-2h2zm-1 5v7a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V8H7zm3 2h2v2h-2zm4 0h2v2h-2z"/></svg>';
  const timeStr = new Date(msg.ts).toLocaleTimeString('pl', { hour: '2-digit', minute: '2-digit' });

  let html = `<div class="msg-avatar">${avatarSvg}</div><div class="msg-body">`;
  html += `<div class="msg-text">${renderMarkdown(msg.text)}</div>`;
  html += `<div class="msg-meta"><span class="msg-time">${timeStr}</span>${renderMessageBadges(msg)}`;

    if (msg.role === 'assistant') {
    html += `<button class="msg-action" onclick="copyMsg(this)">copy</button>`;
    if (S.termOpen) {
      html += `<button class="msg-action" onclick="sendLastToTerm(this)">→ terminal</button>`;
    }
  }
  if (msg.toolCalls && msg.toolCalls.length) {
    html += `<span class="msg-action" style="cursor:default">tool: ${msg.toolCalls.map(t => t.tool).join(', ')}</span>`;
  }
  html += `</div></div>`;
  div.innerHTML = html;

  // Wire code block action buttons
  div.querySelectorAll('.code-act-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      const action = e.target.dataset.action;
      const code = e.target.closest('.code-block-wrap').querySelector('code').textContent;
      if (action === 'copy') {
        navigator.clipboard.writeText(code);
        btn.textContent = '✓';
        setTimeout(() => btn.textContent = 'copy', 1500);
      } else if (action === 'run') {
        if (S.term && S.termWs && S.termWs.readyState === WebSocket.OPEN) {
          if (!S.termOpen) toggleTerminal();
          S.termWs.send(JSON.stringify({ type: 'input', data: code + '\r' }));
        } else {
          toggleTerminal();
          addSystemMsg('Terminal połączony — uruchom ponownie.');
        }
      }
    });
  });

  el.messages.appendChild(div);
  return div;
}

function renderMessageBadges(msg) {
  const bits = [];
  if (msg.role === 'assistant') {
    if (msg.taskProfileLabel || msg.taskProfile) {
      bits.push(metaBadge('profile', msg.taskProfileLabel || msg.taskProfile));
    }
    if (msg.modelDisplay || msg.modelId) {
      bits.push(metaBadge('model', msg.modelDisplay || msg.modelId));
    }
    if (msg.provider) {
      bits.push(metaBadge('provider', msg.provider));
    }
      if (msg.kbScope && msg.kbScope.length) {
        bits.push(metaBadge('kb', msg.kbScope.join(', ')));
      }
      if (msg.kbSources && msg.kbSources.length) {
        bits.push(metaBadge('kb-src', msg.kbSources.join(', ')));
      }
      if (msg.role === 'assistant' && msg.useCharacterExamples === false) {
        bits.push(metaBadge('style', 'direct'));
    } else if (msg.charScope && msg.charScope.length) {
      bits.push(metaBadge('style', msg.charScope.join(', ')));
    }
    if (msg.uploadedFiles && msg.uploadedFiles.length) {
      bits.push(metaBadge('files', msg.uploadedFiles.join(', ')));
    }
  }
  if (msg.toolCalls && msg.toolCalls.length) {
    bits.push(metaBadge('tools', msg.toolCalls.map(t => t.tool).join(', ')));
  }
  return bits.join('');
}

function metaBadge(label, value) {
  return `<span class="msg-badge"><span class="msg-badge-label">${escapeHtml(label)}</span><span class="msg-badge-value">${escapeHtml(value)}</span></span>`;
}

function refreshMessageMeta(bubble, msg) {
  const meta = bubble.querySelector('.msg-meta');
  if (!meta) return;
  const time = meta.querySelector('.msg-time');
  const actions = Array.from(meta.querySelectorAll('.msg-action'));
  meta.innerHTML = '';
  if (time) meta.appendChild(time);
  const badgesHtml = renderMessageBadges(msg);
  if (badgesHtml) meta.insertAdjacentHTML('beforeend', badgesHtml);
  actions.forEach(action => meta.appendChild(action));
}

function renderMarkdown(text) {
  if (!window.marked) return escapeHtml(text).replace(/\n/g, '<br>');

  marked.setOptions({
    breaks: true,
    gfm: true,
    highlight: (code, lang) => {
      if (window.hljs) {
        try {
          if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
          }
          return hljs.highlightAuto(code).value;
        } catch { return escapeHtml(code); }
      }
      return escapeHtml(code);
    }
  });

  let html = marked.parse(text);

  // Wrap pre/code blocks with action buttons
  html = html.replace(/<pre><code(?: class="language-(\w+)")?>([\s\S]*?)<\/code><\/pre>/g,
    (match, lang, code) => {
      const isShell = ['powershell', 'ps1', 'bash', 'sh', 'shell', 'cmd', 'batch'].includes((lang || '').toLowerCase());
      const runBtn = isShell ? `<button class="code-act-btn" data-action="run" title="Run in terminal">run</button>` : '';
      return `<div class="code-block-wrap">
        ${lang ? `<span class="code-lang">${lang}</span>` : ''}
        <pre><code class="language-${lang || ''}">${code}</code></pre>
        <div class="code-actions">
          ${runBtn}
          <button class="code-act-btn" data-action="copy">copy</button>
        </div>
      </div>`;
    });
  return html;
}

function addSystemMsg(text) {
  const div = document.createElement('div');
  div.className = 'msg msg-system';
  div.textContent = text;
  el.messages.appendChild(div);
  scrollBottom();
}

function renderAllMessages() {
  el.messages.innerHTML = '';
  S.messages.forEach(m => renderMessage(m));
  scrollBottom();
}

function clearChat() {
  S.messages = [];
  el.messages.innerHTML = '';
  addSystemMsg('Chat wyczyszczony.');
}

function copyMsg(btn) {
  const text = btn.closest('.msg-body').querySelector('.msg-text').innerText;
  navigator.clipboard.writeText(text);
  btn.textContent = '✓';
  setTimeout(() => btn.textContent = 'copy', 1500);
}

function sendLastToTerm(btn) {
  const text = btn.closest('.msg-body').querySelector('.msg-text').innerText;
  if (S.termWs && S.termWs.readyState === WebSocket.OPEN) {
    S.termWs.send(JSON.stringify({ type: 'input', data: text + '\r' }));
  }
}

function scrollBottom() {
  requestAnimationFrame(() => {
    el.messagesWrap.scrollTop = el.messagesWrap.scrollHeight;
  });
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
          .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

// ── Conversations ───────────────────────────────────────────────────────────
function isJunkConversation(conv) {
  if (!conv || !hasMeaningfulMessages(conv.messages)) return true;
  const title = (conv.title || '').trim().toLowerCase();
  if (
    title.includes('chatboxjimbo') ||
    title.startsWith('>>') ||
    title.startsWith('start m:') ||
    title.includes('ps m:') ||
    title.includes('m:\\chatboxjimbo')
  ) {
    return true;
  }
  const firstMsg = (conv.messages[0]?.text || '').trim().toLowerCase();
  if (
    firstMsg.includes('chatboxjimbo') ||
    firstMsg.startsWith('>> start') ||
    firstMsg.startsWith('ps m:\\')
  ) {
    return true;
  }
  return false;
}

function loadConversations() {
  try {
    S.conversations = JSON.parse(readStored('eastwood-convs', 'jimbo-convs', '[]'));
    pruneConversations();
    saveConversations();
  } catch { S.conversations = []; }
}

function saveConversations() {
  pruneConversations();
  localStorage.setItem('eastwood-convs', JSON.stringify(S.conversations.slice(0, 50)));
}

function hasMeaningfulMessages(messages) {
  return (messages || []).some(m => {
    if (m.role !== 'user' && m.role !== 'assistant') return false;
    return (m.text || '').trim().length > 0;
  });
}

function pruneConversations() {
  S.conversations = S.conversations.filter(c => !isJunkConversation(c));
}

function autoSaveConversation() {
  if (!S.activeConvId) return;
  const idx = S.conversations.findIndex(c => c.id === S.activeConvId);
  if (idx < 0) {
    if (!hasMeaningfulMessages(S.messages)) return;
    S.conversations.unshift({
      id: S.activeConvId,
      title: 'New Chat',
      messages: [...S.messages],
      ts: Date.now(),
    });
    saveConversations();
    renderHistory();
    return;
  }
  if (idx >= 0) {
    S.conversations[idx].messages = [...S.messages];
    S.conversations[idx].ts = Date.now();
  }
  saveConversations();
  renderHistory();
}

function updateConvTitle(title) {
  const idx = S.conversations.findIndex(c => c.id === S.activeConvId);
  if (idx >= 0) {
    S.conversations[idx].title = title;
    saveConversations();
    renderHistory();
  }
}

function newConversation(silent = false) {
  const id = Date.now().toString(36);
  S.activeConvId = id;
  S.messages = [];
  saveConversations();
  el.messages.innerHTML = '';
  if (!silent) addSystemMsg('Nowy chat started.');
  renderHistory();
}

function loadConversation(id) {
  const conv = S.conversations.find(c => c.id === id);
  if (!conv) return;
  S.activeConvId = id;
  S.messages = [...(conv.messages || [])];
  renderAllMessages();
  renderHistory();
}

function deleteConversation(id) {
  S.conversations = S.conversations.filter(c => c.id !== id);
  saveConversations();
  if (S.activeConvId === id) newConversation(true);
  renderHistory();
}

function renderHistory() {
  el.historyList.innerHTML = '';
  const items = S.conversations.filter(c => !isJunkConversation(c)).slice(0, 3);
  items.forEach(conv => {
    const d = document.createElement('div');
    d.className = 'hist-item' + (conv.id === S.activeConvId ? ' active' : '');
    const title = escapeHtml((conv.title || 'Chat').slice(0, 45));
    d.innerHTML = `<span class="hist-title" title="${title}">${title}</span><span class="hist-del" data-id="${conv.id}" title="Delete">✕</span>`;
    d.querySelector('.hist-title').addEventListener('click', () => loadConversation(conv.id));
    d.querySelector('.hist-del').addEventListener('click', e => {
      e.stopPropagation();
      deleteConversation(conv.id);
    });
    el.historyList.appendChild(d);
  });
  if (!items.length) {
    el.historyList.innerHTML = '<span style="color:var(--text3);font-size:11px">brak zapisanych chatów</span>';
  }
}

// ── Knowledge Mood ──────────────────────────────────────────────────────────
async function loadKB() {
  try {
    const r = await fetch(`${S.apiBase}/api/knowledge`);
    const data = await r.json();
    el.kbList.innerHTML = '';
    if (!data.files || !data.files.length) {
      el.kbList.innerHTML = '<span style="color:var(--text3);font-size:11px">brak plików</span>';
      return;
    }
    data.files.forEach(f => {
      const d = document.createElement('div');
      d.className = 'kb-item';
      const kb = (f.size / 1024).toFixed(1);
      d.innerHTML = `<span title="${f.path}">${escapeHtml(f.name)}</span><span style="color:var(--text3);font-size:10px">${kb}kb</span><span class="kb-item-del" data-name="${f.name}">✕</span>`;
      d.querySelector('.kb-item-del').addEventListener('click', () => deleteKBFile(f.name));
      el.kbList.appendChild(d);
    });
  } catch {
    el.kbList.innerHTML = '<span style="color:var(--text3);font-size:11px">błąd ładowania</span>';
  }
}

async function uploadKBFiles(files) {
  for (const file of files) {
    const form = new FormData();
    form.append('file', file);
    try {
      await fetch(`${S.apiBase}/api/knowledge/upload`, { method: 'POST', body: form });
    } catch (e) {
      addSystemMsg(`Upload błąd: ${e.message}`);
    }
  }
  await loadKB();
  addSystemMsg(`Przesłano ${files.length} plik(ów) do ${UI.kbLabel}.`);
}

async function transcribeAudioFile(file) {
  const form = new FormData();
  form.append('file', file);
  form.append('language', 'pl');
  try {
    const r = await fetch(`${S.apiBase}/api/speech/transcribe`, { method: 'POST', body: form });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();
    if (d.text) {
      el.msgInput.value = (el.msgInput.value ? `${el.msgInput.value}\n` : '') + d.text;
      autoResizeTextarea();
      el.msgInput.focus();
      addSystemMsg('Transkrypcja audio dodana do pola wiadomości.');
    } else {
      addSystemMsg('Brak tekstu z transkrypcji.');
    }
  } catch (e) {
    addSystemMsg(`Transcribe error: ${e.message}`);
  }
}

function getLastAssistantText() {
  for (let i = S.messages.length - 1; i >= 0; i--) {
    if (S.messages[i].role === 'assistant' && S.messages[i].text) return S.messages[i].text;
  }
  return '';
}

async function ttsReadAloud() {
  const text = el.msgInput.value.trim() || getLastAssistantText();
  if (!text) {
    addSystemMsg('Brak tekstu do TTS (pole wiadomości i historia puste).');
    return;
  }
  await playTtsText(text);
}

function initVoxToggle() {
  const btn = $('#btn-vox-toggle');
  if (!btn) return;
  btn.className = S.voiceMode ? 'vox-on' : 'vox-off';
  btn.textContent = S.voiceMode ? 'VOX' : 'VOX';
}

function toggleVoiceMode() {
  S.voiceMode = !S.voiceMode;
      localStorage.setItem('eastwood-voice-mode', S.voiceMode);
  initVoxToggle();
  if (S.voiceMode) {
    addSystemMsg('Voice mode ON — odpowiedzi będą czytane na głos (bez kodu).');
  } else {
    addSystemMsg('Voice mode OFF.');
  }
}

function stripCodeForTts(text) {
  // Remove fenced code blocks (```...```) keeping only text between them
  // This strips powershell, bash, cmd, and any other code blocks
  const cleaned = text
    .replace(/\`\`\`[\s\S]*?\`\`\`/g, '')
    .replace(/\`[^\`]+\`/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  return cleaned;
}

async function playTtsText(text) {
  if (!text || !text.trim()) return;
  text = stripCodeForTts(text);
  if (!text) return;
  const body = {
    text: text.slice(0, 3000),
    format: 'mp3',
    style_preset: (el.ttsStyleSelect && el.ttsStyleSelect.value) || 'neo-noir',
  };
  try {
    const r = await fetch(`${S.apiBase}/api/speech/synthesize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = new Audio(url);
    a.play().catch(() => addSystemMsg('Autoplay audio zablokowany przez przeglądarkę.'));
    a.onended = () => URL.revokeObjectURL(url);
  } catch (e) {
    addSystemMsg(`TTS error: ${e.message}`);
  }
}

async function runResearchToKB() {
  const q = prompt('Zapytanie do researchu web -> KB:');
  if (!q) return;
  try {
    const r = await fetch(`${S.apiBase}/api/knowledge/research_web`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: q, max_results: 5 }),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();
    addSystemMsg(`Research zapisany: ${d.count} plik(ów).`);
    await loadKB();
  } catch (e) {
    addSystemMsg(`Research error: ${e.message}`);
  }
}

async function runTmdbToKB() {
  const q = prompt('Fraza filmowa do TMDB (np. Blade Runner):');
  if (!q) return;
  try {
    const r = await fetch(`${S.apiBase}/api/knowledge/ingest_tmdb`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: q, limit: 5 }),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();
    addSystemMsg(`TMDB import: ${d.count} plik(ów).`);
    await loadKB();
  } catch (e) {
    addSystemMsg(`TMDB error: ${e.message}`);
  }
}

async function pushKnowledgeToR2() {
  try {
    const r = await fetch(`${S.apiBase}/api/knowledge/push_r2`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prefix: 'knowledge_mood' }),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();
    addSystemMsg(`R2 push OK: ${d.uploaded} plik(ów) do ${d.bucket}.`);
  } catch (e) {
    addSystemMsg(`R2 push error: ${e.message}`);
  }
}

async function loadMemorySummary() {
  const box = $('memory-summary');
  if (!box) return;
  try {
    const r = await fetch(`${S.apiBase}/api/diary`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();
    const facts = (d.facts || []).slice(-5);
    const goals = (d.goals || []).slice(-5);
    const decs = (d.decisions || []).slice(-3);
    const lines = [];
    if (facts.length) lines.push(`Facts: ${facts.join(' | ')}`);
    if (goals.length) lines.push(`Goals: ${goals.join(' | ')}`);
    if (decs.length) lines.push(`Decisions: ${decs.map(x => x.topic).join(' | ')}`);
    box.textContent = lines.length ? lines.join('\n') : 'Memory is empty.';
  } catch (e) {
    box.textContent = `Memory load error: ${e.message}`;
  }
}

async function runDecisionCoach() {
  const topic = prompt('Temat decyzji:');
  if (!topic) return;
  const optionsRaw = prompt('Opcje (oddziel ;), opcjonalnie:', '');
  const constraintsRaw = prompt('Ograniczenia (oddziel ;), opcjonalnie:', '');
  const options = optionsRaw ? optionsRaw.split(';').map(x => x.trim()).filter(Boolean) : [];
  const constraints = constraintsRaw ? constraintsRaw.split(';').map(x => x.trim()).filter(Boolean) : [];
  try {
    const r = await fetch(`${S.apiBase}/api/decision/coach`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, options, constraints }),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();
    addSystemMsg(`Decision coach gotowy dla: ${d.topic}`);
    renderMessage({ role: 'assistant', text: d.answer, ts: Date.now() });
    await loadMemorySummary();
  } catch (e) {
    addSystemMsg(`Decision coach error: ${e.message}`);
  }
}

async function deleteKBFile(name) {
  try {
    await fetch(`${S.apiBase}/api/knowledge/${encodeURIComponent(name)}`, { method: 'DELETE' });
    await loadKB();
  } catch (e) {
    addSystemMsg(`Błąd usuwania: ${e.message}`);
  }
}

// ── Terminal ────────────────────────────────────────────────────────────────
function initTerminal() {
  if (S.term) { S.term.dispose(); S.term = null; }
  el.termContainer.innerHTML = '';

  S.term = new Terminal({
    allowTransparency: true,
    theme: {
      background: 'transparent',
      foreground: '#e2e8f3',
      cursor: '#9fb2ff',
      cursorAccent: '#05070d',
      selectionBackground: '#7b88f055',
      black: '#1a1a1a', brightBlack: '#444',
      red: '#e05050', brightRed: '#ff6060',
      green: '#3dcc88', brightGreen: '#50ee99',
      yellow: '#f0c040', brightYellow: '#ffe060',
      blue: '#4d9fff', brightBlue: '#66bbff',
      magenta: '#cc88ff', brightMagenta: '#dd99ff',
      cyan: '#44ddcc', brightCyan: '#55eedd',
      white: '#cccccc', brightWhite: '#ffffff',
    },
    fontFamily: "'JetBrains Mono','Fira Code','Cascadia Code','Consolas',monospace",
    fontSize: 12,
    lineHeight: 1.4,
    cursorBlink: true,
    scrollback: 2000,
    convertEol: true,
  });

  const fitAddon = new FitAddon.FitAddon();
  S.fitAddon = fitAddon;
  S.term.loadAddon(fitAddon);
  S.term.open(el.termContainer);
  syncTerminalTheme();
  fitAddon.fit();
  S.term.scrollToBottom();

  S.term.onData(data => {
    if (S.termWs && S.termWs.readyState === WebSocket.OPEN) {
      S.termWs.send(JSON.stringify({ type: 'input', data }));
    }
  });

  new ResizeObserver(() => {
    try {
      fitAddon.fit();
      S.term.scrollToBottom();
      if (S.termWs && S.termWs.readyState === WebSocket.OPEN && S.term) {
        S.termWs.send(JSON.stringify({ type: 'resize', rows: S.term.rows, cols: S.term.cols }));
      }
    } catch {}
  }).observe(el.termContainer);

  connectTermWs();
}

function connectTermWs() {
  if (S.termReconnectTimer) {
    clearTimeout(S.termReconnectTimer);
    S.termReconnectTimer = null;
  }

  if (S.termWs) {
    try { S.termWs.close(); } catch {}
    S.termWs = null;
  }

  const wsBase = S.apiBase.replace(/^http/, 'ws');
  const ws = new WebSocket(`${wsBase}/ws/terminal`);
  S.termWs = ws;

  setTermStatus('connecting', 'connecting...');

  ws.onopen = () => {
    S.termReconnectAttempts = 0;
    setTermStatus('green', 'connected');
    if (S.fitAddon) {
      S.fitAddon.fit();
      ws.send(JSON.stringify({ type: 'resize', rows: S.term.rows, cols: S.term.cols }));
    }
    if (S.pendingTermCmd) {
      const cmd = S.pendingTermCmd;
      S.pendingTermCmd = null;
      // Daj PTY chwile na wystartowanie powloki zanim wesle komende.
      setTimeout(() => {
        if (S.termWs && S.termWs.readyState === WebSocket.OPEN) {
          S.termWs.send(JSON.stringify({ type: 'input', data: cmd }));
        }
      }, 400);
    }
  };

  ws.onmessage = e => {
    try {
      const d = JSON.parse(e.data);
      if (d.type === 'output' && S.term) S.term.write(d.data, () => S.term.scrollToBottom());
      if (d.type === 'error' && S.term) S.term.write(`\x1b[31m${d.data}\x1b[0m`, () => S.term.scrollToBottom());
    } catch {
      if (S.term) S.term.write(e.data, () => S.term.scrollToBottom());
    }
  };

  ws.onerror = () => setTermStatus('red', 'error');

  ws.onclose = () => {
    setTermStatus('red', 'disconnected');
    // Soft reconnect with cap to avoid endless reconnect loop spam.
    if (S.termOpen && S.term && S.termReconnectAttempts < 6) {
      S.termReconnectAttempts += 1;
      const delayMs = Math.min(15000, 1500 * S.termReconnectAttempts);
      setTermStatus('connecting', `reconnect ${S.termReconnectAttempts}/6...`);
      S.termReconnectTimer = setTimeout(() => {
        if (S.termOpen && S.term) connectTermWs();
      }, delayMs);
    }
  };
}

function sendToTerminal(cmd) {
  if (!S.termOpen) toggleTerminal();
  if (S.termWs && S.termWs.readyState === WebSocket.OPEN) {
    S.termWs.send(JSON.stringify({ type: 'input', data: cmd }));
  } else {
    // Terminal sie dopiero laczy (zimny start) — wyslij komende jak tylko WS bedzie gotowy.
    S.pendingTermCmd = cmd;
  }
}

function setTermStatus(color, text) {
  el.termDot.className = `dot dot-${color === 'connecting' ? 'yellow' : color}`;
  el.termStatusTxt.textContent = text;
}

function toggleTerminal() {
  S.termOpen = !S.termOpen;
  el.termPanel.classList.toggle('hidden', !S.termOpen);
  if (el.rightbar) el.rightbar.classList.toggle('hidden', S.termOpen);
  const modeBtn = $('btn-right-mode');
  if (modeBtn) modeBtn.textContent = S.termOpen ? 'TERM' : 'PANEL';
  $('btn-term-toggle').classList.toggle('active', S.termOpen);

  if (S.termOpen && !S.term) {
    setTimeout(() => { initTerminal(); initTermResize(); }, 50);
  } else if (S.termOpen && S.fitAddon) {
    setTimeout(() => { S.fitAddon.fit(); if (S.term) S.term.scrollToBottom(); }, 50);
  }
  if (S.termOpen) {
    setTimeout(initTermResize, 50);
  }
}

function toggleLeftColumn() {
  el.appRoot.classList.toggle('left-collapsed');
}

function toggleRightColumn() {
  el.appRoot.classList.toggle('right-collapsed');
}

function toggleRightMode() {
  if (el.appRoot.classList.contains('right-collapsed')) {
    el.appRoot.classList.remove('right-collapsed');
  }
  if (S.termOpen) {
    S.termOpen = false;
    el.termPanel.classList.add('hidden');
    if (el.rightbar) el.rightbar.classList.remove('hidden');
    $('btn-term-toggle').classList.remove('active');
    $('btn-right-mode').textContent = 'PANEL';
    return;
  }
  S.termOpen = true;
  el.termPanel.classList.remove('hidden');
  if (el.rightbar) el.rightbar.classList.add('hidden');
  $('btn-term-toggle').classList.add('active');
  $('btn-right-mode').textContent = 'TERM';
  if (!S.term) setTimeout(initTerminal, 50);
  else if (S.fitAddon) setTimeout(() => S.fitAddon.fit(), 50);
}

// ── Diagnostics Dashboard (real backend data only) ──────────────────────────
let diagnosticsActive = false;
let diagnosticsTimer = null;
let diagnosticsBusy = false;

function toggleDiagnostics() {
  const diagMain = document.getElementById('diag-main');
  const chatMain = document.getElementById('chat-main');
  const btn = document.getElementById('btn-diag-toggle');
  if (!diagMain || !chatMain || !btn) return;

  diagnosticsActive = !diagnosticsActive;
  if (diagnosticsActive) {
    chatMain.style.setProperty('display', 'none', 'important');
    diagMain.style.setProperty('display', 'flex', 'important');
    btn.style.backgroundColor = '#ff0055';
    btn.style.color = '#000000';
    refreshDiagnostics();
    diagnosticsTimer = setInterval(refreshDiagnostics, 7000);
  } else {
    chatMain.style.display = '';
    diagMain.style.display = 'none';
    btn.style.backgroundColor = '';
    btn.style.color = '#ff0055';
    if (diagnosticsTimer) clearInterval(diagnosticsTimer);
    diagnosticsTimer = null;
  }
}

function renderDiagnostics(data) {
  const statusEl = $('diag-sys-status');
  const refreshedEl = $('diag-generated-at');
  const backendStatusEl = $('diag-backend-status');
  const providerEl = $('diag-provider');
  const activeChatEl = $('diag-active-chat');
  const activeTerminalEl = $('diag-active-terminal');
  const embeddingsEl = $('diag-embeddings');
  const convEl = $('diag-conversations');
  const msgEl = $('diag-messages');
  const msgBreakdownEl = $('diag-message-breakdown');
  const diaryCountEl = $('diag-diary-count');
  const defaultModelEl = $('diag-default-model');
  const profilesEl = $('diag-profiles');
  const recentConvEl = $('diag-recent-conversations');
  const recentActEl = $('diag-recent-activity');
  const kbCountEl = $('diag-kb-count');
  const kbDirEl = $('diag-knowledge-dir');
  const kbSampleEl = $('diag-kb-sample');
  const diarySummaryEl = $('diag-diary-summary');

  const health = data.health || {};
  const runtime = data.runtime || {};
  const db = data.database || {};
  const diary = data.diary || {};
  const knowledge = data.knowledge || {};
  const profiles = data.task_profiles || [];
  const recentConversations = db.recent_conversations || [];
  const recentMessages = db.recent_messages || [];
  const activeStatus = health.status === 'ok' ? 'ONLINE' : 'OFFLINE';

  if (statusEl) statusEl.textContent = activeStatus;
  if (refreshedEl) refreshedEl.textContent = data.generated_at ? new Date(data.generated_at).toLocaleString() : '-';
  if (backendStatusEl) backendStatusEl.textContent = health.provider || activeStatus;
  if (providerEl) providerEl.textContent = `${health.default_model || 'default model'} · router ${health.model_router_enabled ? 'on' : 'off'}`;
  if (activeChatEl) activeChatEl.textContent = String(runtime.active_chat_requests ?? 0);
  if (activeTerminalEl) activeTerminalEl.textContent = String(runtime.active_terminal_connections ?? 0);
  if (embeddingsEl) embeddingsEl.textContent = `${health.embeddings_ready ? 'embeddings ready' : 'embeddings not ready'} · terminal ${health.terminal_available ? 'available' : 'missing'}`;
  if (convEl) convEl.textContent = String(db.conversation_count ?? 0);
  if (msgEl) msgEl.textContent = String(db.message_count ?? 0);
  if (msgBreakdownEl) {
    const breakdown = db.messages_by_role || {};
    const parts = Object.entries(breakdown).map(([role, count]) => `${role}: ${count}`);
    msgBreakdownEl.textContent = parts.length ? parts.join(' · ') : 'no messages yet';
  }
  if (diaryCountEl) diaryCountEl.textContent = String([
    ...(diary.facts || []),
    ...(diary.moments || []),
    ...(diary.preferences || []),
    ...(diary.goals || []),
    ...(diary.decisions || []),
  ].length);
  if (defaultModelEl) defaultModelEl.textContent = `router base: ${health.model_router_base_url || '-'}`;
  if (kbCountEl) kbCountEl.textContent = `${knowledge.file_count || 0} files`;
  if (kbDirEl) kbDirEl.textContent = knowledge.dir ? `Knowledge dir: ${knowledge.dir}` : 'Knowledge dir unavailable';
  if (kbSampleEl) {
    const sample = knowledge.sample_files || [];
    kbSampleEl.innerHTML = sample.length
      ? sample.map(name => `<div style="padding:4px 0;border-bottom:1px solid var(--border);">${escapeHtml(name)}</div>`).join('')
      : '<div style="color:var(--text3);font-size:11px">no files found</div>';
  }

  if (profilesEl) {
    profilesEl.innerHTML = profiles.length
      ? profiles.map(profile => `
        <div style="border:1px solid var(--border2);background:var(--bg3);padding:8px;">
          <div style="display:flex;justify-content:space-between;gap:8px;">
            <span style="color:var(--accent);font-size:11px;font-weight:700;">${escapeHtml(profile.key)}</span>
            <span style="color:var(--text3);font-size:10px;">${escapeHtml(profile.model_name || 'default')}</span>
          </div>
          <div style="font-size:11px;color:var(--text2);margin-top:4px;line-height:1.45;">${escapeHtml(profile.description || '')}</div>
          <div style="font-size:10px;color:var(--text3);margin-top:4px;">KB: ${escapeHtml((profile.kb_scope || []).join(', ') || '-')}</div>
        </div>`).join('')
      : '<div style="color:var(--text3);font-size:11px">no profiles available</div>';
  }

  if (recentConvEl) {
    recentConvEl.innerHTML = recentConversations.length
      ? recentConversations.map(conv => `
        <div style="border:1px solid var(--border2);background:var(--bg3);padding:8px;">
          <div style="display:flex;justify-content:space-between;gap:8px;font-size:11px;">
            <span style="color:var(--accent);font-weight:700;">Conversation #${escapeHtml(String(conv.id))}</span>
            <span style="color:var(--text3);">${escapeHtml(conv.created_at || '-')}</span>
          </div>
          <div style="font-size:11px;color:var(--text2);margin-top:4px;">Messages: ${escapeHtml(String(conv.message_count ?? 0))} · Last: ${escapeHtml(conv.last_role || 'n/a')}</div>
          <div style="font-size:11px;color:var(--text3);margin-top:4px;line-height:1.45;">${escapeHtml(conv.last_excerpt || '')}</div>
        </div>`).join('')
      : '<div style="color:var(--text3);font-size:11px">no conversations yet</div>';
  }

  if (recentActEl) {
    recentActEl.innerHTML = recentMessages.length
      ? recentMessages.map(msg => `
        <div style="border:1px solid var(--border2);background:var(--bg3);padding:8px;">
          <div style="display:flex;justify-content:space-between;gap:8px;font-size:11px;">
            <span style="color:var(--accent);font-weight:700;">${escapeHtml(msg.role || 'unknown')}</span>
            <span style="color:var(--text3);">${escapeHtml(msg.created_at || '-')}</span>
          </div>
          <div style="font-size:11px;color:var(--text2);margin-top:4px;">conv #${escapeHtml(String(msg.conversation_id ?? '-'))}</div>
          <div style="font-size:11px;color:var(--text3);margin-top:4px;line-height:1.45;">${escapeHtml(msg.excerpt || '')}</div>
        </div>`).join('')
      : '<div style="color:var(--text3);font-size:11px">no recent messages</div>';
  }

  if (diarySummaryEl) {
    const parts = [
      `facts: ${(diary.facts || []).length}`,
      `moments: ${(diary.moments || []).length}`,
      `preferences: ${(diary.preferences || []).length}`,
      `goals: ${(diary.goals || []).length}`,
      `decisions: ${(diary.decisions || []).length}`,
      '',
      diary.summary || 'Diary is empty.'
    ];
    diarySummaryEl.textContent = parts.join('\n');
  }
}

async function refreshDiagnostics() {
  if (diagnosticsBusy) return;
  diagnosticsBusy = true;
  const btn = $('btn-diag-test');
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'REFRESHING...';
  }
  try {
    const r = await fetch(`${S.apiBase}/api/diagnostics`, { signal: AbortSignal.timeout(5000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    renderDiagnostics(data);
  } catch (err) {
    const statusEl = $('diag-sys-status');
    if (statusEl) statusEl.textContent = 'OFFLINE';
    const backendStatusEl = $('diag-backend-status');
    if (backendStatusEl) backendStatusEl.textContent = 'offline';
    const providerEl = $('diag-provider');
    if (providerEl) providerEl.textContent = err?.message || 'diagnostics failed';
  } finally {
    diagnosticsBusy = false;
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'REFRESH LIVE';
    }
  }
}

// ── Terminal Resize ──────────────────────────────────────────────────────────
function initTermResize() {
  const handle = document.getElementById('term-resize-handle');
  const panel = document.getElementById('term-panel');
  if (!handle || !panel) return;

  // Restore saved width
  const saved = readStored('eastwood-term-width', 'jimbo-term-width', '');
  if (saved) {
    const w = parseInt(saved);
    if (w >= 200) updateTermGridWidth(w);
  }

  handle.onmousedown = function(e) {
    e.preventDefault();
    handle.classList.add('dragging');
    const startX = e.clientX;
    const startW = panel.offsetWidth;

    function onMove(ev) {
      const diff = startX - ev.clientX;
      let newW = startW + diff;
      newW = Math.max(200, Math.min(newW, window.innerWidth * 0.6));
      updateTermGridWidth(newW);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    }

    function onUp() {
      handle.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      localStorage.setItem('eastwood-term-width', panel.offsetWidth);
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
    }

    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  };
}

// ── Update grid column for term panel ─────────────────────────────────────
function updateTermGridWidth(px) {
  const main = document.getElementById('main');
  const sidebar = document.getElementById('sidebar');
  const rightbar = document.getElementById('rightbar');
  const leftW = sidebar && sidebar.offsetWidth > 0 ? '260px' : '0px';
  const rightW = rightbar && !rightbar.classList.contains('hidden') ? '340px' : px + 'px';
  main.style.gridTemplateColumns = leftW + ' minmax(0,1fr) ' + rightW;
  if (S.fitAddon) setTimeout(() => S.fitAddon.fit(), 20);
}

// ── Themes ─────────────────────────────────────────────────────────────────
function applyTheme(theme) {
  S.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  const fallback = THEME_VARS[theme];
  if (fallback) {
    const r = document.documentElement.style;
    r.setProperty('--bg', fallback.bg);
    r.setProperty('--bg2', fallback.cardBg);
    r.setProperty('--border', fallback.border);
    r.setProperty('--accent', fallback.accent);
    r.setProperty('--text3', fallback.dim);
    r.setProperty('--text', fallback.text);
    r.setProperty('--user-bg', fallback.userBg);
  }
  fetch(`themes/${theme}.json`)
    .then(resp => resp.ok ? resp.json() : null)
    .then(cfg => {
      if (!cfg || !cfg.vars || !cfg.colors) return;
      const vars = cfg.vars;
      const colors = cfg.colors;
      const pick = key => vars[colors[key]] || colors[key] || '';
      const r = document.documentElement.style;
      r.setProperty('--accent', pick('accent') || fallback?.accent || '#79c0ff');
      r.setProperty('--border', pick('border') || fallback?.border || '#2d3f71');
      r.setProperty('--border2', pick('borderAccent') || fallback?.border || '#3f5794');
      r.setProperty('--text2', pick('muted') || '#8ea3c4');
      r.setProperty('--text3', pick('dim') || fallback?.dim || '#5a6e8d');
      r.setProperty('--user-bg', vars.userMsgBg || fallback?.userBg || '#0d1c37');
      r.setProperty('--bg2', cfg.export?.cardBg || fallback?.cardBg || '#0d1021');
      r.setProperty('--bg', cfg.export?.pageBg || fallback?.bg || '#080c16');
      syncTerminalTheme();
    })
    .catch(() => {
      syncTerminalTheme();
    });
  saveSettings();
}

function syncTerminalTheme() {
  if (!S.term) return;
  const css = getComputedStyle(document.documentElement);
  const bg = css.getPropertyValue('--bg').trim() || '#080c16';
  const fg = css.getPropertyValue('--text').trim() || '#dce9ff';
  const accent = css.getPropertyValue('--accent').trim() || '#79c0ff';
  const border = css.getPropertyValue('--border2').trim() || '#3f5794';
  S.term.options.theme = {
    ...S.term.options.theme,
    background: `${bg}cc`,
    foreground: fg,
    cursor: accent,
    selectionBackground: `${accent}55`,
    cursorAccent: border,
  };
}

function cycleTheme() {
  const idx = (THEMES.indexOf(S.theme) + 1) % THEMES.length;
  applyTheme(THEMES[idx]);
}

// ── Voice ───────────────────────────────────────────────────────────────────
function toggleVoice() {
  if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
    addSystemMsg('Twoja przeglądarka nie obsługuje rozpoznawania mowy.');
    return;
  }

  if (S.isRecording) {
    S.recognition && S.recognition.stop();
    S.isRecording = false;
    el.btnVoice.classList.remove('recording');
    return;
  }

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  S.recognition = new SR();
  S.recognition.lang = 'pl-PL';
  S.recognition.continuous = false;
  S.recognition.interimResults = false;

  S.recognition.onresult = e => {
    el.msgInput.value += e.results[0][0].transcript;
    autoResizeTextarea();
  };
  S.recognition.onend = () => {
    S.isRecording = false;
    el.btnVoice.classList.remove('recording');
  };
  S.recognition.onerror = e => {
    addSystemMsg(`Błąd mikrofonu: ${e.error}`);
    S.isRecording = false;
    el.btnVoice.classList.remove('recording');
  };

  S.recognition.start();
  S.isRecording = true;
  el.btnVoice.classList.add('recording');
}

// ── Export ─────────────────────────────────────────────────────────────────
function exportJSON() {
  const data = {
    exported: new Date().toISOString(),
    model: S.model,
    messages: S.messages,
  };
  downloadFile(`eastwood-ops-${Date.now()}.json`, JSON.stringify(data, null, 2), 'application/json');
}

function exportMarkdown() {
  const lines = [`# ${UI.appName} — ${new Date().toLocaleDateString('pl')}`, '', `**Model:** ${S.model}`, ''];
  S.messages.forEach(m => {
    const role = m.role === 'user' ? `**${UI.userName}**` : `**${UI.assistantName}**`;
    lines.push(`### ${role} — ${new Date(m.ts).toLocaleTimeString('pl')}`);
    lines.push('', m.text, '');
  });
  downloadFile(`eastwood-ops-${Date.now()}.md`, lines.join('\n'), 'text/markdown');
}

function downloadFile(name, content, type) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([content], { type }));
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}

// ── Textarea auto-resize ───────────────────────────────────────────────────
function autoResizeTextarea() {
  const ta = el.msgInput;
  ta.style.height = 'auto';
  ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
}

// ── Sidebar collapsible ────────────────────────────────────────────────────
function setupCollapsibles() {
  document.querySelectorAll('.toggle-icon').forEach(icon => {
    const targetId = icon.dataset.target;
    const body = $(targetId);
    if (!body) return;
    icon.addEventListener('click', () => {
      const collapsed = body.classList.toggle('collapsed');
      icon.style.transform = collapsed ? 'rotate(-90deg)' : '';
    });
  });
}

// ── Event Listeners ────────────────────────────────────────────────────────
function setupEventListeners() {
  setupCollapsibles();

  // Send
  el.btnSend.addEventListener('click', doSend);
  el.msgInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); doSend(); }
  });
  el.msgInput.addEventListener('input', autoResizeTextarea);

  function doSend() {
    const text = el.msgInput.value;
    el.msgInput.value = '';
    el.msgInput.style.height = 'auto';
    sendMessage(text, [...S.attachedFiles]);
  }

  // File attach
  el.btnAttach.addEventListener('click', () => el.fileInput.click());
  el.fileInput.addEventListener('change', e => {
    addAttachedFiles(Array.from(e.target.files));
  });

  // Drag & drop onto chat
  el.messagesWrap.addEventListener('dragover', e => e.preventDefault());
  el.messagesWrap.addEventListener('drop', e => {
    e.preventDefault();
    addAttachedFiles(Array.from(e.dataTransfer.files));
  });
  $('input-area').addEventListener('dragover', e => e.preventDefault());
  $('input-area').addEventListener('drop', e => {
    e.preventDefault();
    addAttachedFiles(Array.from(e.dataTransfer.files));
  });

  function addAttachedFiles(files) {
    files.forEach(f => {
      S.attachedFiles.push(f);
      const chip = document.createElement('div');
      chip.className = 'attached-file';
      chip.innerHTML = `<span>FILE ${escapeHtml(f.name)}</span><span class="rm" title="Remove">x</span>`;
      chip.querySelector('.rm').addEventListener('click', () => {
        S.attachedFiles = S.attachedFiles.filter(x => x !== f);
        chip.remove();
      });
      el.attachedFiles.appendChild(chip);
    });
  }

  // Voice
  el.btnVoice.addEventListener('click', toggleVoice);
  $('btn-stt-upload').addEventListener('click', () => el.sttFileInput.click());
  el.sttFileInput.addEventListener('change', e => {
    const f = e.target.files && e.target.files[0];
    if (f) transcribeAudioFile(f);
    e.target.value = '';
  });
  $('btn-tts-play').addEventListener('click', ttsReadAloud);
  $('btn-vox-toggle').addEventListener('click', toggleVoiceMode);
  $('btn-research-kb').addEventListener('click', runResearchToKB);
  $('btn-tmdb-kb').addEventListener('click', runTmdbToKB);
  $('btn-decision-coach').addEventListener('click', runDecisionCoach);
  $('btn-memory-refresh').addEventListener('click', loadMemorySummary);
  $('btn-memory-clear').addEventListener('click', async () => {
    if (!confirm(`Wyczyścić pamięć użytkownika ${UI.userName}?`)) return;
    try {
      const r = await fetch(`${S.apiBase}/api/diary`, { method: 'DELETE' });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      await loadMemorySummary();
      addSystemMsg('Memory cleared.');
    } catch (e) {
      addSystemMsg(`Memory clear error: ${e.message}`);
    }
  });

  // Model select
  el.modelSelect.addEventListener('change', () => {
    S.model = el.modelSelect.value;
    saveSettings();
  });
  if (el.taskProfileSelect) {
    el.taskProfileSelect.addEventListener('change', () => {
      S.taskProfile = el.taskProfileSelect.value;
      saveSettings();
    });
  }

  // API URL
  el.apiUrl.addEventListener('change', () => {
    S.apiBase = el.apiUrl.value.trim().replace(/\/$/, '');
    saveSettings();
    checkHealth();
    loadTaskProfiles();
    loadModels();
  });

  // Sliders
  el.tempSlider.addEventListener('input', () => {
    S.temperature = parseFloat(el.tempSlider.value);
    el.tempVal.textContent = S.temperature.toFixed(1);
  });
  el.toppSlider.addEventListener('input', () => {
    S.topP = parseFloat(el.toppSlider.value);
    el.toppVal.textContent = S.topP.toFixed(2);
  });
  el.maxTokSlider.addEventListener('input', () => {
    S.maxTokens = parseInt(el.maxTokSlider.value);
    el.maxTokVal.textContent = S.maxTokens;
  });
  [el.tempSlider, el.toppSlider, el.maxTokSlider].forEach(s => s.addEventListener('change', saveSettings));

  // Tools toggle
  el.cbTools.addEventListener('change', () => {
    S.useTools = el.cbTools.checked;
    saveSettings();
  });
  if (el.cbAutoTts) {
    el.cbAutoTts.addEventListener('change', () => {
      S.autoTts = el.cbAutoTts.checked;
      saveSettings();
    });
  }

  // System prompt
  el.sysPrompt.addEventListener('change', () => {
    S.systemPrompt = el.sysPrompt.value;
    saveSettings();
  });
  $('btn-reset-prompt').addEventListener('click', () => {
    el.sysPrompt.value = '';
    S.systemPrompt = '';
    saveSettings();
    addSystemMsg(`System prompt zresetowany do domyślnego promptu ${UI.assistantName}.`);
  });

  // New chat
  $('btn-new-chat-sb').addEventListener('click', () => newConversation());
  $('btn-history-prune').addEventListener('click', () => {
    pruneConversations();
    saveConversations();
    renderHistory();
    addSystemMsg('Historia oczyszczona: usunięto niepoprawne wpisy.');
  });
  $('btn-export-json-sb').addEventListener('click', exportJSON);
  $('btn-clear-chat-sb').addEventListener('click', () => {
    if (confirm('Wyczyścić aktywny chat?')) clearChat();
  });

  // Sidebar Quick Tools Buttons
  const btnHub = $('sb-btn-hub');
  if (btnHub) {
    btnHub.addEventListener('click', () => {
      if (window.BonzoAddons && window.BonzoAddons.toggleDrawer) {
        if (!window.BonzoAddons.State.drawerOpen) window.BonzoAddons.toggleDrawer();
        window.BonzoAddons.switchTab('music');
      } else {
        addSystemMsg('[HUB] Media & Kino: Inicjalizacja katalogu...');
      }
    });
  }

  const btnRadio = $('sb-btn-radio');
  if (btnRadio) {
    btnRadio.addEventListener('click', () => {
      if (window.BonzoAddons && window.BonzoAddons.toggleDrawer) {
        if (!window.BonzoAddons.State.drawerOpen) window.BonzoAddons.toggleDrawer();
        window.BonzoAddons.switchTab('radio');
      } else {
        addSystemMsg('[RADIO] Live Stream: Inicjalizacja stacji...');
      }
    });
  }

  const btnWeather = $('sb-btn-weather');
  if (btnWeather) {
    btnWeather.addEventListener('click', () => {
      if (window.BonzoAddons && window.BonzoAddons.toggleDrawer) {
        if (!window.BonzoAddons.State.drawerOpen) window.BonzoAddons.toggleDrawer();
        window.BonzoAddons.switchTab('fun');
        if (window.BonzoAddons.loadWeather) window.BonzoAddons.loadWeather('Warszawa');
      } else {
        addSystemMsg('[METEO] Pogoda Live: Odświeżanie prognozy...');
      }
    });
  }

  const btnImage = $('sb-btn-image');
  if (btnImage) {
    btnImage.addEventListener('click', () => {
      if (window.BonzoAddons && window.BonzoAddons.toggleDrawer) {
        if (!window.BonzoAddons.State.drawerOpen) window.BonzoAddons.toggleDrawer();
        window.BonzoAddons.switchTab('fun');
        const p = document.getElementById('bad-img-prompt');
        if (p) {
          p.focus();
          p.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      } else {
        addSystemMsg('[FLUX] Generator AI: Otwieranie generatora...');
      }
    });
  }

  const btnTerm = $('sb-btn-term');
  if (btnTerm) {
    btnTerm.addEventListener('click', () => {
      toggleTerminal();
    });
  }

  const btnReset = $('sb-btn-reset');
  if (btnReset) {
    btnReset.addEventListener('click', () => {
      if (confirm('Zresetować sesję i otworzyć nowy czat?')) {
        newConversation(false);
      }
    });
  }

  // Theme
  $('btn-theme').addEventListener('click', cycleTheme);
  $('btn-left-toggle').addEventListener('click', toggleLeftColumn);
  $('btn-right-toggle').addEventListener('click', toggleRightColumn);
  $('btn-right-mode').addEventListener('click', toggleRightMode);
  $('btn-diag-toggle').addEventListener('click', toggleDiagnostics);
  $('btn-diag-test').addEventListener('click', refreshDiagnostics);

  // Terminal toggle
  $('btn-term-toggle').addEventListener('click', toggleTerminal);
  $('btn-term-reconnect').addEventListener('click', () => {
    if (S.term) connectTermWs();
    else initTerminal();
  });
  $('btn-term-clear-screen').addEventListener('click', () => {
    if (S.term) S.term.clear();
  });
  $('btn-term-send-to-chat').addEventListener('click', () => {
    if (!S.term) return;
    const buf = S.term.buffer.active;
    const lines = [];
    for (let i = 0; i < buf.length; i++) {
      const line = buf.getLine(i);
      if (line) lines.push(line.translateToString(true));
    }
    const text = lines.join('\n').trim();
    if (text) {
      el.msgInput.value = `\`\`\`\n${text}\n\`\`\`\nCo oznacza ten output?`;
      autoResizeTextarea();
      el.msgInput.focus();
    }
  });

  // Terminal quick buttons
  document.querySelectorAll('.tqcmd').forEach(btn => {
    btn.addEventListener('click', () => {
      const cmd = btn.dataset.cmd.replace('\\r', '\r');
      sendToTerminal(cmd);
    });
  });

  // Jeden przycisk: otworz terminal (jesli trzeba) i odpal agenta Pi obok czatu
  $('btn-launch-pi').addEventListener('click', () => sendToTerminal('pi\r'));

  // Quick commands
  document.querySelectorAll('.qcmd').forEach(btn => {
    btn.addEventListener('click', () => {
      const cmd = btn.dataset.cmd;
      if (cmd === '/clear') { clearChat(); return; }
      el.msgInput.value = cmd;
      autoResizeTextarea();
      el.msgInput.focus();
    });
  });

  // KB
  $('btn-kb-upload').addEventListener('click', () => el.kbFileInput.click());
  $('btn-kb-refresh').addEventListener('click', () => loadKB());
  el.kbFileInput.addEventListener('change', e => {
    uploadKBFiles(Array.from(e.target.files));
    e.target.value = '';
  });

  // Export / Clear
  $('btn-export-json').addEventListener('click', exportJSON);
  $('btn-export-md').addEventListener('click', exportMarkdown);
  $('btn-clear-chat').addEventListener('click', () => {
    if (confirm('Wyczyścić chat?')) clearChat();
  });
}

// ── Start ───────────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', init);
window.addEventListener('DOMContentLoaded', loadMemorySummary);

// Expose helpers for inline onclick
window.copyMsg = copyMsg;
window.sendLastToTerm = sendLastToTerm;
