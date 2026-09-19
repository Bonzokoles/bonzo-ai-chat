/* ==========================================================================
   BONZO ADDONS SUITE — Frontend Client
   Integracja multimedialna i codzienne narzędzia dla EastWood Ops:
   - Bonzo Media Hub: Muzyka (28 utworów) i Kino (105 filmów)
   - Live Internet Radio (Synthwave, Lofi, Rock, Jazz, Ambient)
   - Narzędzia codzienne (Pogoda Open-Meteo, Generator Obrazów FLUX, Fakty)
   - Interaktywne widgety w oknie czatu
   ========================================================================== */

(function () {
  'use strict';

  console.log('[ADDONS] Inicjalizacja Bonzo Addons Suite...');

  // State
  const State = {
    apiBase: '',
    tracks: [],
    films: [],
    categories: [],
    radioPresets: [],
    currentTrackIndex: -1,
    isPlaying: false,
    currentMedia: null, // { type: 'music'|'radio', title, artist, url }
    audioEl: new Audio(),
    drawerOpen: false,
    activeTab: 'music',
  };

  // Resolve API Base
  function getApiBase() {
    const input = document.getElementById('api-url-input');
    if (input && input.value) return input.value.replace(/\/+$/, '');
    if (typeof window !== 'undefined' && window.location.origin) {
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:4149';
      }
      return 'https://mybonzo-v3.stolarnia-ams.workers.dev';
    }
    return 'http://localhost:4149';
  }

  // Format seconds to mm:ss
  function formatTime(sec) {
    if (isNaN(sec) || !isFinite(sec)) return '00:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
  }

  // 1. Inject DOM Elements (Drawer, Mini-Player, Trailer Modal)
  function injectDOMElements() {
    // Addon Button in Topbar
    const topActions = document.querySelector('.tb-actions') || document.getElementById('topbar');
    if (topActions && !document.getElementById('btn-hub-addon')) {
      const hubBtn = document.createElement('button');
      hubBtn.id = 'btn-hub-addon';
      hubBtn.title = 'Bonzo Media Hub & Addons';
      hubBtn.innerHTML = `<span>[HUB]</span>`;
      hubBtn.onclick = toggleDrawer;
      topActions.prepend(hubBtn);
    }

    // Mini Player HTML
    if (!document.getElementById('bonzo-mini-player')) {
      const player = document.createElement('div');
      player.id = 'bonzo-mini-player';
      player.className = 'hidden';
      player.innerHTML = `
        <div class="bmp-info">
          <div class="bmp-pulse" id="bmp-indicator"></div>
          <div style="min-width:0; overflow:hidden;">
            <div class="bmp-title" id="bmp-title">Brak odtwarzania</div>
            <div class="bmp-artist" id="bmp-artist">Wybierz utwór lub radio</div>
          </div>
        </div>
        <div class="bmp-controls">
          <button class="bmp-btn" id="bmp-prev" title="Poprzedni">[PREV]</button>
          <button class="bmp-btn bmp-btn-primary" id="bmp-play" title="Odtwórz / Pauza">[PLAY]</button>
          <button class="bmp-btn" id="bmp-next" title="Następny">[NEXT]</button>
        </div>
        <div class="bmp-progress-wrap">
          <span class="bmp-time" id="bmp-cur-time">00:00</span>
          <div class="bmp-progress-bar" id="bmp-progress">
            <div class="bmp-progress-fill" id="bmp-progress-fill"></div>
          </div>
          <span class="bmp-time" id="bmp-dur-time">00:00</span>
        </div>
        <div class="bmp-volume-wrap">
          <span style="font-size:10px; color:#64748b;">VOL</span>
          <input type="range" class="bmp-volume-slider" id="bmp-vol" min="0" max="1" step="0.05" value="0.8">
          <button class="bmp-btn" id="bmp-close-player" style="padding:2px 6px; font-size:9px; border-color:#d55a6f; color:#d55a6f;">X</button>
        </div>
      `;
      document.body.appendChild(player);
    }

    // Drawer HTML
    if (!document.getElementById('bonzo-addons-drawer')) {
      const drawer = document.createElement('aside');
      drawer.id = 'bonzo-addons-drawer';
      drawer.innerHTML = `
        <div class="bad-header">
          <div class="bad-title">BONZO MEDIA HUB & ADDONS</div>
          <button class="bmp-btn" id="bad-close-btn">[ZAMKNIJ]</button>
        </div>
        <div class="bad-nav">
          <button class="bad-tab-btn active" data-tab="music">MUZYKA (28)</button>
          <button class="bad-tab-btn" data-tab="films">KINO (105)</button>
          <button class="bad-tab-btn" data-tab="radio">RADIO LIVE</button>
          <button class="bad-tab-btn" data-tab="fun">DAILY & FUN</button>
        </div>
        <div class="bad-content">
          <!-- MUSIC PANE -->
          <div class="bad-tab-pane active" id="pane-music">
            <input type="text" class="bad-search-bar" id="bad-music-search" placeholder="Filtruj utwory (Depeche Mode, Nosowska, Bowie, Męskie Granie)...">
            <div id="bad-track-list">Ładowanie utworów...</div>
          </div>

          <!-- FILMS PANE -->
          <div class="bad-tab-pane" id="pane-films">
            <input type="text" class="bad-search-bar" id="bad-film-search" placeholder="Szukaj w 105 filmach (tytuł, reżyser, psychodela, miłość)...">
            <div id="bad-film-categories" style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;"></div>
            <div class="bad-film-grid" id="bad-film-grid">Ładowanie katalogu...</div>
          </div>

          <!-- RADIO PANE -->
          <div class="bad-tab-pane" id="pane-radio">
            <div style="font-size:11px; color:#94a3b8; margin-bottom:10px;">Strumienie audio na żywo w tle bez obciążania systemu:</div>
            <div class="bad-radio-grid" id="bad-radio-grid">Ładowanie stacji...</div>
          </div>

          <!-- FUN & DAILY PANE -->
          <div class="bad-tab-pane" id="pane-fun">
            <!-- Weather Card -->
            <div class="bad-widget-card" id="bad-weather-widget">
              <div class="bad-widget-title">
                <span>POGODA NA ŻYWO</span>
                <input type="text" id="bad-weather-city-input" value="Warszawa" style="width:110px; padding:2px 6px; font-size:10px; background:#181c26; border:1px solid #2d3748; color:#ffffff;">
              </div>
              <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <div class="bad-weather-temp" id="bww-temp">--°C</div>
                <div class="bad-weather-cond" id="bww-cond">Pobieranie danych...</div>
              </div>
              <div class="bad-weather-grid">
                <div>Odczuwalna: <span id="bww-app-temp">--°C</span></div>
                <div>Wilgotność: <span id="bww-hum">--%</span></div>
                <div>Wiatr: <span id="bww-wind">-- km/h</span></div>
                <div>Wschód/Zachód: <span id="bww-sun">-- / --</span></div>
              </div>
            </div>

            <!-- Image Generation Card -->
            <div class="bad-widget-card">
              <div class="bad-widget-title">GENERATOR OBRAZÓW AI (POLLINATIONS)</div>
              <div style="display:flex; gap:6px; margin-bottom:10px;">
                <input type="text" id="bad-img-prompt" placeholder="Wpisz opis (np. cyberpunk detective office in neon rain)..." style="flex:1; padding:6px; background:#11141c; border:1px solid #2d3748; font-size:11px; color:#fff;">
                <button class="bmp-btn bmp-btn-primary" id="bad-btn-generate-img">[GENERUJ]</button>
              </div>
              <div id="bad-img-preview" style="min-height:160px; background:#05070a; border:1px solid #1a202c; display:grid; place-items:center; overflow:hidden;">
                <span style="color:#64748b; font-size:11px;">Podgląd wygenerowanej grafiki</span>
              </div>
            </div>

            <!-- Daily Thought Card -->
            <div class="bad-widget-card">
              <div class="bad-widget-title">MYŚL DNIA / STOICKI SPARK</div>
              <div id="bad-thought-text" style="font-size:12px; color:#ffffff; font-style:italic; line-height:1.5;">Ładowanie...</div>
              <div id="bad-thought-author" style="text-align:right; font-size:10px; color:#d4a574; margin-top:8px; font-weight:700;">-</div>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(drawer);
    }

    // Trailer Modal HTML
    if (!document.getElementById('bonzo-trailer-modal')) {
      const modal = document.createElement('div');
      modal.id = 'bonzo-trailer-modal';
      modal.innerHTML = `
        <div class="btm-box">
          <div class="btm-header">
            <span id="btm-title">OFFICIAL TRAILER</span>
            <button class="bmp-btn" id="btm-close-btn">[ZAMKNIJ]</button>
          </div>
          <div class="btm-video-wrap">
            <iframe id="btm-iframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }

    bindEvents();
  }

  // 2. Bind DOM & Player Events
  function bindEvents() {
    // Drawer Tab Switching
    document.querySelectorAll('.bad-tab-btn').forEach(btn => {
      btn.onclick = () => {
        const tab = btn.dataset.tab;
        switchTab(tab);
      };
    });

    // Drawer Close
    const closeBtn = document.getElementById('bad-close-btn');
    if (closeBtn) closeBtn.onclick = toggleDrawer;

    // Trailer Modal Close
    const btmClose = document.getElementById('btm-close-btn');
    if (btmClose) btmClose.onclick = closeTrailerModal;
    const modal = document.getElementById('bonzo-trailer-modal');
    if (modal) {
      modal.onclick = (e) => {
        if (e.target === modal) closeTrailerModal();
      };
    }

    // Mini Player Controls
    const playBtn = document.getElementById('bmp-play');
    if (playBtn) playBtn.onclick = togglePlay;

    const prevBtn = document.getElementById('bmp-prev');
    if (prevBtn) prevBtn.onclick = playPrevTrack;

    const nextBtn = document.getElementById('bmp-next');
    if (nextBtn) nextBtn.onclick = playNextTrack;

    const volSlider = document.getElementById('bmp-vol');
    if (volSlider) {
      volSlider.oninput = (e) => {
        State.audioEl.volume = parseFloat(e.target.value);
      };
    }

    const closePlayerBtn = document.getElementById('bmp-close-player');
    if (closePlayerBtn) {
      closePlayerBtn.onclick = () => {
        State.audioEl.pause();
        State.isPlaying = false;
        document.getElementById('bonzo-mini-player').classList.add('hidden');
      };
    }

    // Audio Progress Scrubber
    const progressBar = document.getElementById('bmp-progress');
    if (progressBar) {
      progressBar.onclick = (e) => {
        if (!State.audioEl.duration) return;
        const rect = progressBar.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const pct = Math.max(0, Math.min(1, clickX / rect.width));
        State.audioEl.currentTime = pct * State.audioEl.duration;
      };
    }

    // Audio element native listeners
    State.audioEl.ontimeupdate = () => {
      const cur = State.audioEl.currentTime || 0;
      const dur = State.audioEl.duration || 0;
      const curEl = document.getElementById('bmp-cur-time');
      const durEl = document.getElementById('bmp-dur-time');
      const fillEl = document.getElementById('bmp-progress-fill');
      if (curEl) curEl.textContent = formatTime(cur);
      if (durEl) durEl.textContent = formatTime(dur);
      if (fillEl && dur > 0) fillEl.style.width = `${(cur / dur) * 100}%`;
    };

    State.audioEl.onended = () => {
      playNextTrack();
    };

    State.audioEl.onplay = () => {
      State.isPlaying = true;
      updatePlayerUI();
    };

    State.audioEl.onpause = () => {
      State.isPlaying = false;
      updatePlayerUI();
    };

    // Filter listeners
    const musicSearch = document.getElementById('bad-music-search');
    if (musicSearch) {
      musicSearch.oninput = (e) => renderTrackList(e.target.value);
    }

    const filmSearch = document.getElementById('bad-film-search');
    if (filmSearch) {
      filmSearch.oninput = (e) => renderFilmGrid(e.target.value);
    }

    // Weather City input
    const cityInput = document.getElementById('bad-weather-city-input');
    if (cityInput) {
      cityInput.onchange = () => loadWeather(cityInput.value);
    }

    // Image Generator
    const genBtn = document.getElementById('bad-btn-generate-img');
    const promptInput = document.getElementById('bad-img-prompt');
    if (genBtn && promptInput) {
      genBtn.onclick = () => {
        const p = promptInput.value.trim();
        if (!p) return;
        generateImage(p);
      };
    }
  }

  // 3. Audio Player Logic
  function playAudio(url, title, artist, trackIndex = -1) {
    State.currentMedia = { type: 'music', title, artist, url };
    State.currentTrackIndex = trackIndex;

    const fullUrl = url.startsWith('http') ? url : `${getApiBase()}${url}`;
    State.audioEl.src = fullUrl;
    State.audioEl.play().catch(err => console.warn('[ADDONS] Audio play blocked:', err));

    const playerEl = document.getElementById('bonzo-mini-player');
    if (playerEl) playerEl.classList.remove('hidden');

    updatePlayerUI();
    highlightCurrentTrack();
  }

  function playRadio(streamUrl, stationName, genre) {
    State.currentMedia = { type: 'radio', title: stationName, artist: `Live Radio [${genre}]`, url: streamUrl };
    State.currentTrackIndex = -1;

    State.audioEl.src = streamUrl;
    State.audioEl.play().catch(err => console.warn('[ADDONS] Radio play error:', err));

    const playerEl = document.getElementById('bonzo-mini-player');
    if (playerEl) playerEl.classList.remove('hidden');

    updatePlayerUI();
  }

  function togglePlay() {
    if (!State.audioEl.src) {
      if (State.tracks.length > 0) playTrackByIndex(0);
      return;
    }
    if (State.isPlaying) {
      State.audioEl.pause();
    } else {
      State.audioEl.play();
    }
  }

  function playPrevTrack() {
    if (State.tracks.length === 0) return;
    let idx = State.currentTrackIndex - 1;
    if (idx < 0) idx = State.tracks.length - 1;
    playTrackByIndex(idx);
  }

  function playNextTrack() {
    if (State.tracks.length === 0) return;
    let idx = State.currentTrackIndex + 1;
    if (idx >= State.tracks.length) idx = 0;
    playTrackByIndex(idx);
  }

  function playTrackByIndex(idx) {
    if (idx < 0 || idx >= State.tracks.length) return;
    const t = State.tracks[idx];
    playAudio(t.stream_url, t.title, t.artist, idx);
  }

  function updatePlayerUI() {
    const playBtn = document.getElementById('bmp-play');
    const titleEl = document.getElementById('bmp-title');
    const artistEl = document.getElementById('bmp-artist');
    const indicator = document.getElementById('bmp-indicator');

    if (playBtn) playBtn.textContent = State.isPlaying ? '[PAUSE]' : '[PLAY]';
    if (State.currentMedia) {
      if (titleEl) titleEl.textContent = State.currentMedia.title;
      if (artistEl) artistEl.textContent = State.currentMedia.artist;
    }
    if (indicator) {
      indicator.style.animationPlayState = State.isPlaying ? 'running' : 'paused';
      indicator.style.opacity = State.isPlaying ? '1' : '0.2';
    }
  }

  function highlightCurrentTrack() {
    document.querySelectorAll('.bad-track-item').forEach(item => {
      if (Number(item.dataset.idx) === State.currentTrackIndex) {
        item.classList.add('playing');
      } else {
        item.classList.remove('playing');
      }
    });
  }

  // 4. Data Fetching
  async function loadData() {
    State.apiBase = getApiBase();
    try {
      // 1. Music tracks
      const resTracks = await fetch(`${State.apiBase}/api/addons/media/tracks`);
      if (resTracks.ok) {
        const data = await resTracks.json();
        State.tracks = data.tracks || [];
        renderTrackList();
      }

      // 2. Film catalog
      const resFilms = await fetch(`${State.apiBase}/api/addons/media/films?limit=105`);
      if (resFilms.ok) {
        const data = await resFilms.json();
        State.films = data.films || [];
        renderFilmGrid();
      }

      // 3. Film categories
      const resCats = await fetch(`${State.apiBase}/api/addons/media/films/categories`);
      if (resCats.ok) {
        const data = await resCats.json();
        State.categories = data.categories || [];
        renderCategories();
      }

      // 4. Radio presets
      const resRadio = await fetch(`${State.apiBase}/api/addons/radio/presets`);
      if (resRadio.ok) {
        const data = await resRadio.json();
        State.radioPresets = data.stations || [];
        renderRadioGrid();
      }

      // 5. Daily fun & weather
      loadWeather('Warszawa');
      loadDailyThought();
    } catch (err) {
      console.warn('[ADDONS] Background fetch error:', err);
    }
  }

  // 5. Rendering Views
  function renderTrackList(filter = '') {
    const listEl = document.getElementById('bad-track-list');
    if (!listEl) return;

    const q = filter.toLowerCase();
    const matched = State.tracks.filter(t =>
      !q || t.title.toLowerCase().includes(q) || t.artist.toLowerCase().includes(q)
    );

    if (matched.length === 0) {
      listEl.innerHTML = `<div style="color:#64748b; font-size:11px; padding:10px;">Brak utworów pasujących do: "${filter}"</div>`;
      return;
    }

    listEl.innerHTML = matched.map((t) => `
      <div class="bad-track-item ${State.tracks.indexOf(t) === State.currentTrackIndex ? 'playing' : ''}" data-idx="${State.tracks.indexOf(t)}">
        <div class="bad-track-meta">
          <div class="bad-track-title">${t.title}</div>
          <div class="bad-track-artist">${t.artist} (${t.size_mb} MB)</div>
        </div>
        <button class="bmp-btn">[PLAY]</button>
      </div>
    `).join('');

    listEl.querySelectorAll('.bad-track-item').forEach(item => {
      item.onclick = () => {
        const idx = parseInt(item.dataset.idx, 10);
        playTrackByIndex(idx);
      };
    });
  }

  function renderCategories() {
    const catWrap = document.getElementById('bad-film-categories');
    if (!catWrap) return;

    let html = `<button class="bmp-btn" data-cat="" style="font-size:10px;">WSZYSTKIE (105)</button>`;
    State.categories.forEach(c => {
      html += `<button class="bmp-btn" data-cat="${c.category}" style="font-size:10px;">${c.category} (${c.count})</button>`;
    });
    catWrap.innerHTML = html;

    catWrap.querySelectorAll('button').forEach(btn => {
      btn.onclick = () => {
        const cat = btn.dataset.cat;
        renderFilmGrid('', cat);
      };
    });
  }

  function renderFilmGrid(filter = '', category = '') {
    const gridEl = document.getElementById('bad-film-grid');
    if (!gridEl) return;

    const q = filter.toLowerCase();
    const catFilter = category.toLowerCase();

    const matched = State.films.filter(f => {
      const matchQ = !q || f.title.toLowerCase().includes(q) || (f.director && f.director.toLowerCase().includes(q));
      const matchCat = !catFilter || (f.category && f.category.toLowerCase().includes(catFilter));
      return matchQ && matchCat;
    });

    if (matched.length === 0) {
      gridEl.innerHTML = `<div style="color:#64748b; font-size:11px; padding:10px;">Brak filmów dla podanych kryteriów.</div>`;
      return;
    }

    gridEl.innerHTML = matched.map(f => `
      <div class="bad-film-card">
        <div class="bad-film-poster-wrap">
          <img src="${f.poster}" class="bad-film-poster" alt="${f.title}" loading="lazy">
          <div class="bad-film-badge">TMDB ${f.rating || '-'}</div>
        </div>
        <div class="bad-film-body">
          <div>
            <div class="bad-film-title">${f.title}</div>
            <div class="bad-film-meta">${f.category} | reż. ${f.director || 'N/A'}</div>
            <div class="bad-film-desc">${f.overview || 'Brak opisu.'}</div>
          </div>
          <button class="bmp-btn bmp-btn-primary bad-btn-trailer" data-id="${f.tmdb_id}" data-title="${f.title}">[TRAILER]</button>
        </div>
      </div>
    `).join('');

    gridEl.querySelectorAll('.bad-btn-trailer').forEach(btn => {
      btn.onclick = async (e) => {
        e.stopPropagation();
        const tmdbId = btn.dataset.id;
        const title = btn.dataset.title;
        openTrailer(tmdbId, title);
      };
    });
  }

  function renderRadioGrid() {
    const gridEl = document.getElementById('bad-radio-grid');
    if (!gridEl) return;

    gridEl.innerHTML = State.radioPresets.map(s => `
      <div class="bad-radio-card" data-url="${s.stream_url}" data-name="${s.name}" data-genre="${s.genre}">
        <span class="bad-radio-tag">${s.tag}</span>
        <div class="bad-radio-name">${s.name}</div>
        <div style="font-size:10px; color:#64748b;">${s.bitrate} MP3/AAC Stream</div>
      </div>
    `).join('');

    gridEl.querySelectorAll('.bad-radio-card').forEach(card => {
      card.onclick = () => {
        playRadio(card.dataset.url, card.dataset.name, card.dataset.genre);
      };
    });
  }

  async function loadWeather(city) {
    try {
      const res = await fetch(`${State.apiBase}/api/addons/fun/weather?city=${encodeURIComponent(city)}`);
      if (res.ok) {
        const w = await res.json();
        if (w.error) return;
        document.getElementById('bww-temp').textContent = `${w.temperature}°C`;
        document.getElementById('bww-cond').textContent = `${w.condition} (${w.city})`;
        document.getElementById('bww-app-temp').textContent = `${w.apparent_temperature}°C`;
        document.getElementById('bww-hum').textContent = `${w.humidity}%`;
        document.getElementById('bww-wind').textContent = `${w.wind_speed} km/h`;
        document.getElementById('bww-sun').textContent = `${w.sunrise} / ${w.sunset}`;
      }
    } catch (e) {}
  }

  async function loadDailyThought() {
    try {
      const res = await fetch(`${State.apiBase}/api/addons/fun/thought`);
      if (res.ok) {
        const t = await res.json();
        document.getElementById('bad-thought-text').textContent = `"${t.quote}"`;
        document.getElementById('bad-thought-author').textContent = `— ${t.author} [${t.tag}]`;
      }
    } catch (e) {}
  }

  function generateImage(prompt) {
    const preview = document.getElementById('bad-img-preview');
    if (!preview) return;
    preview.innerHTML = `<span style="color:#00e5ff; font-size:11px;">Generowanie obrazu FLUX dla: "${prompt}"...</span>`;

    const clean = encodeURIComponent(prompt.trim());
    const seed = Math.floor(Math.random() * 900000) + 100000;
    const url = `https://image.pollinations.ai/prompt/${clean}?width=1024&height=768&nologo=true&seed=${seed}&model=flux`;

    const img = new Image();
    img.src = url;
    img.style.width = '100%';
    img.style.height = 'auto';
    img.style.display = 'block';
    img.onload = () => {
      preview.innerHTML = '';
      preview.appendChild(img);
    };
    img.onerror = () => {
      preview.innerHTML = `<span style="color:#d55a6f; font-size:11px;">Błąd ładowania obrazu.</span>`;
    };
  }

  // 6. Trailer Modal
  async function openTrailer(tmdbId, title) {
    const modal = document.getElementById('bonzo-trailer-modal');
    const iframe = document.getElementById('btm-iframe');
    const titleEl = document.getElementById('btm-title');

    if (titleEl) titleEl.textContent = `TRAILER: ${title.toUpperCase()}`;
    if (modal) modal.classList.add('open');

    try {
      const res = await fetch(`${State.apiBase}/api/addons/media/films/${tmdbId}/trailer?title=${encodeURIComponent(title)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.trailer_embed) {
          iframe.src = data.trailer_embed;
          return;
        }
      }
    } catch (e) {}

    // Fallback search
    iframe.src = `https://www.youtube.com/embed?listType=search&list=${encodeURIComponent(title + ' official trailer')}&autoplay=1`;
  }

  function closeTrailerModal() {
    const modal = document.getElementById('bonzo-trailer-modal');
    const iframe = document.getElementById('btm-iframe');
    if (iframe) iframe.src = '';
    if (modal) modal.classList.remove('open');
  }

  // 7. Drawer Navigation
  function openDrawer() {
    State.drawerOpen = true;
    const drawer = document.getElementById('bonzo-addons-drawer');
    const btn = document.getElementById('btn-hub-addon');
    if (drawer) drawer.classList.add('open');
    if (btn) btn.classList.add('active');
  }

  function toggleDrawer() {
    State.drawerOpen = !State.drawerOpen;
    const drawer = document.getElementById('bonzo-addons-drawer');
    const btn = document.getElementById('btn-hub-addon');
    if (drawer) {
      if (State.drawerOpen) drawer.classList.add('open');
      else drawer.classList.remove('open');
    }
    if (btn) {
      if (State.drawerOpen) btn.classList.add('active');
      else btn.classList.remove('active');
    }
  }

  function switchTab(tab) {
    State.activeTab = tab;
    document.querySelectorAll('.bad-tab-btn').forEach(b => {
      if (b.dataset.tab === tab) b.classList.add('active');
      else b.classList.remove('active');
    });
    document.querySelectorAll('.bad-tab-pane').forEach(p => {
      if (p.id === `pane-${tab}`) p.classList.add('active');
      else p.classList.remove('active');
    });
  }

  // 8. Chat Interceptor & Message Widget Hydrator
  function hydrateMessageWidgets() {
    const messages = document.querySelectorAll('.msg-body');
    messages.forEach(msg => {
      if (msg.dataset.hydrated) return;

      const text = msg.innerHTML;

      // Detect [AUDIO_PLAY: url | title | artist]
      const audioMatch = text.match(/\[AUDIO_PLAY:\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\]]+)\]/);
      if (audioMatch) {
        const url = audioMatch[1].trim();
        const title = audioMatch[2].trim();
        const artist = audioMatch[3].trim();
        const widget = document.createElement('div');
        widget.className = 'chat-audio-card';
        widget.innerHTML = `
          <div>
            <div style="font-weight:700; color:#00E6A8; font-size:11px;">[PLAYING AUDIO] ${title}</div>
            <div style="color:#94a3b8; font-size:10px;">${artist}</div>
          </div>
          <button class="bmp-btn bmp-btn-primary" style="font-size:10px;">[ODTWÓRZ TERAZ]</button>
        `;
        widget.querySelector('button').onclick = () => playAudio(url, title, artist);
        msg.prepend(widget);
      }

      // Detect [RADIO_PLAY: url | name]
      const radioMatch = text.match(/\[RADIO_PLAY:\s*([^\|]+)\s*\|\s*([^\]]+)\]/);
      if (radioMatch) {
        const url = radioMatch[1].trim();
        const name = radioMatch[2].trim();
        const widget = document.createElement('div');
        widget.className = 'chat-audio-card';
        widget.innerHTML = `
          <div>
            <div style="font-weight:700; color:#00e5ff; font-size:11px;">[RADIO LIVE] ${name}</div>
            <div style="color:#94a3b8; font-size:10px;">Strumień audio na żywo</div>
          </div>
          <button class="bmp-btn bmp-btn-primary" style="font-size:10px; border-color:#00e5ff; color:#00e5ff;">[WŁĄCZ RADIO]</button>
        `;
        widget.querySelector('button').onclick = () => playRadio(url, name, 'LIVE');
        msg.prepend(widget);
      }

      msg.dataset.hydrated = 'true';
    });
  }

  // 9. Quick Input Command Interceptor
  function setupCommandInterceptor() {
    const input = document.getElementById('msg-input');
    if (!input) return;

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        const val = input.value.trim();
        if (val.startsWith('/play ')) {
          e.preventDefault();
          e.stopPropagation();
          input.value = '';
          const q = val.replace('/play ', '').trim();
          playAudioByQuery(q);
        } else if (val.startsWith('/radio')) {
          e.preventDefault();
          e.stopPropagation();
          input.value = '';
          const g = val.replace('/radio', '').trim() || 'synthwave';
          playRadioByGenre(g);
        } else if (val.startsWith('/film ')) {
          e.preventDefault();
          e.stopPropagation();
          input.value = '';
          const f = val.replace('/film ', '').trim();
          openDrawer();
          switchTab('films');
          renderFilmGrid(f);
        } else if (val.startsWith('/pogoda')) {
          e.preventDefault();
          e.stopPropagation();
          input.value = '';
          const city = val.replace('/pogoda', '').trim() || 'Warszawa';
          openDrawer();
          switchTab('fun');
          loadWeather(city);
        } else if (val.startsWith('/obrazek ')) {
          e.preventDefault();
          e.stopPropagation();
          input.value = '';
          const p = val.replace('/obrazek ', '').trim();
          openDrawer();
          switchTab('fun');
          generateImage(p);
        }
      }
    }, true);
  }

  function playAudioByQuery(q) {
    const query = q.toLowerCase();
    const matched = State.tracks.find(t =>
      t.title.toLowerCase().includes(query) || t.artist.toLowerCase().includes(query)
    );
    if (matched) {
      playAudio(matched.stream_url, matched.title, matched.artist, State.tracks.indexOf(matched));
    } else {
      alert(`Nie znaleziono utworu dla: "${q}". Otwieram katalog.`);
      toggleDrawer();
      switchTab('music');
    }
  }

  function playRadioByGenre(g) {
    const genre = g.toLowerCase();
    const matched = State.radioPresets.find(s =>
      s.genre.toLowerCase().includes(genre) || s.id.toLowerCase().includes(genre) || s.name.toLowerCase().includes(genre)
    );
    if (matched) {
      playRadio(matched.stream_url, matched.name, matched.genre);
    } else if (State.radioPresets.length > 0) {
      playRadio(State.radioPresets[0].stream_url, State.radioPresets[0].name, State.radioPresets[0].genre);
    }
  }

  // 10. Startup
  function initAddons() {
    injectDOMElements();
    loadData();
    setupCommandInterceptor();

    // Observe messages for dynamic widgets
    const messagesWrap = document.getElementById('messages');
    if (messagesWrap) {
      const observer = new MutationObserver(hydrateMessageWidgets);
      observer.observe(messagesWrap, { childList: true, subtree: true });
    }

    // Expose Global API for sidebar quick buttons
    window.BonzoAddons = {
      toggleDrawer,
      switchTab,
      loadWeather,
      loadDailyThought,
      generateImage,
      playRadio,
      playAudio,
      playRadioByGenre,
      playAudioByQuery,
      openTrailer,
      State,
    };

    console.log('[ADDONS] Bonzo Addons Suite gotowy!');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAddons);
  } else {
    initAddons();
  }
})();
