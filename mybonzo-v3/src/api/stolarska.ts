import { Hono } from 'hono';
import { SmartRouterEngine } from '../providers/router';
import { ChatMessage } from '../providers/types';

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
};

const stolarska = new Hono<{ Bindings: Bindings }>();

// GET /api/stolarska/projekty - Lista wszystkich projektów stolarskich z KPI
stolarska.get('/projekty', async (c) => {
  try {
    const { results } = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis ORDER BY id DESC`
    ).all();

    return c.json({
      success: true,
      data: results || []
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// GET /api/stolarska/projekty/:id - Szczegóły projektu, pozycje kosztów, czas pracy i AI insights
stolarska.get('/projekty/:id', async (c) => {
  try {
    const id = c.req.param('id');

    const projekt = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis WHERE id = ?`
    ).bind(id).first();

    if (!projekt) {
      return c.json({ success: false, error: `Projekt ${id} nie został znaleziony` }, 404);
    }

    const koszty = await c.env.DB.prepare(
      `SELECT * FROM stolar_koszty WHERE projekt_id = ? ORDER BY id ASC`
    ).bind(id).all();

    const czasPracy = await c.env.DB.prepare(
      `SELECT * FROM stolar_czas_pracy WHERE projekt_id = ? ORDER BY data DESC`
    ).bind(id).all();

    const faktury = await c.env.DB.prepare(
      `SELECT * FROM stolar_faktury_sprzedaz WHERE projekt_id = ? ORDER BY id ASC`
    ).bind(id).all();

    const latestInsight = await c.env.DB.prepare(
      `SELECT * FROM stolar_insights WHERE projekt_id = ? ORDER BY created_at DESC LIMIT 1`
    ).bind(id).first();

    return c.json({
      success: true,
      data: {
        ...projekt,
        pozycje_kosztow: koszty.results || [],
        rejestr_czasu: czasPracy.results || [],
        faktury_sprzedazy: faktury.results || [],
        ai_insight: latestInsight ? {
          ...latestInsight,
          insights: latestInsight.insights_json ? JSON.parse(latestInsight.insights_json as string) : [],
          recommendations: latestInsight.recommendations_json ? JSON.parse(latestInsight.recommendations_json as string) : [],
          dashboard_hints: latestInsight.dashboard_hints_json ? JSON.parse(latestInsight.dashboard_hints_json as string) : {}
        } : null
      }
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// POST /api/stolarska/kalkulacja - Szybka symulacja rentowności z parametrów
stolarska.post('/kalkulacja', async (c) => {
  try {
    const body = await c.req.json();
    const wycena = Number(body.wycena_klienta || body.cena_klienta || 0);
    const zaliczka = Number(body.zaliczka || 0);

    const koszty_materialow = Number(body.koszty_materialow || 0);
    const godziny_produkcja = Number(body.godziny_produkcja || 0);
    const godziny_montaz = Number(body.godziny_montaz || 0);
    const stawka_godz = Number(body.stawka_godz || 80);

    const koszty_robocizny = Number(body.koszty_robocizny || ((godziny_produkcja + godziny_montaz) * stawka_godz));
    const koszty_inne = Number(body.koszty_inne || 0);

    const koszty_total = Math.round((koszty_materialow + koszty_robocizny + koszty_inne) * 100) / 100;
    const zysk = Math.round((wycena - koszty_total) * 100) / 100;
    const marza_proc = wycena > 0 ? Math.round((zysk / wycena) * 1000) / 10 : 0;
    const do_zaplaty = Math.max(0, Math.round((wycena - zaliczka) * 100) / 100);

    const status_rentownosci = marza_proc >= 35 ? 'dobra' : marza_proc >= 20 ? 'ok' : marza_proc >= 0 ? 'niska' : 'strata';

    return c.json({
      success: true,
      data: {
        wycena_klienta: wycena,
        zaliczka,
        do_zaplaty,
        koszty_materialow,
        koszty_robocizny,
        koszty_inne,
        koszty_total,
        zysk_brutto: zysk,
        marza_proc,
        status_rentownosci,
        rekomendacja: marza_proc < 20
          ? 'Uwaga: Marża poniżej progu 20%. Zweryfikuj koszt okuć i nakład roboczogodzin.'
          : 'Parametry rentowności projektu w normie branżowej Stolarni AMS.'
      }
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 400);
  }
});

// POST /api/stolarska/projekty - Utworzenie nowego projektu stolarskiego
stolarska.post('/projekty', async (c) => {
  try {
    const body = await c.req.json();
    if (!body.nazwa) {
      return c.json({ success: false, error: 'Pole "nazwa" jest wymagane' }, 400);
    }

    const id = body.id || `PRJ-${Date.now().toString().slice(-4)}`;
    const nazwa = body.nazwa.trim();
    const klient = body.klient || '';
    const status = body.status || 'nowy';
    const data_utworzenia = body.data_utworzenia || new Date().toISOString().slice(0, 10);
    const termin_klienta = body.termin_klienta || null;
    const wycena_klienta = Number(body.wycena_klienta || 0);
    const zaliczka = Number(body.zaliczka || 0);
    const pro100_plik = body.pro100_plik || null;
    const notatki = body.notatki || '';

    await c.env.DB.prepare(
      `INSERT INTO stolar_projekty (id, nazwa, klient, status, data_utworzenia, termin_klienta, wycena_klienta, zaliczka, pro100_plik, notatki)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(id, nazwa, klient, status, data_utworzenia, termin_klienta, wycena_klienta, zaliczka, pro100_plik, notatki).run();

    // Opcjonalne dodanie pozycji kosztów
    if (Array.isArray(body.koszty) && body.koszty.length > 0) {
      for (const k of body.koszty) {
        if (k.nazwa) {
          await c.env.DB.prepare(
            `INSERT INTO stolar_koszty (projekt_id, kategoria, nazwa, jednostka, ilosc, cena_jedn, faktura_nr, notatki)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
          ).bind(
            id,
            k.kategoria || 'material',
            k.nazwa,
            k.jednostka || 'szt',
            Number(k.ilosc || 1),
            Number(k.cena_jedn || 0),
            k.faktura_nr || null,
            k.notatki || null
          ).run();
        }
      }
    }

    const created = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis WHERE id = ?`
    ).bind(id).first();

    return c.json({
      success: true,
      data: created
    }, 201);
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// PUT /api/stolarska/projekty/:id - Aktualizacja danych projektu
stolarska.put('/projekty/:id', async (c) => {
  try {
    const id = c.req.param('id');
    const body = await c.req.json();

    const existing = await c.env.DB.prepare(
      `SELECT id FROM stolar_projekty WHERE id = ?`
    ).bind(id).first();

    if (!existing) {
      return c.json({ success: false, error: `Projekt ${id} nie istnieje` }, 404);
    }

    await c.env.DB.prepare(
      `UPDATE stolar_projekty
       SET nazwa = COALESCE(?, nazwa),
           klient = COALESCE(?, klient),
           status = COALESCE(?, status),
           termin_klienta = COALESCE(?, termin_klienta),
           wycena_klienta = COALESCE(?, wycena_klienta),
           zaliczka = COALESCE(?, zaliczka),
           notatki = COALESCE(?, notatki),
           updated_at = datetime('now')
       WHERE id = ?`
    ).bind(
      body.nazwa || null,
      body.klient || null,
      body.status || null,
      body.termin_klienta || null,
      body.wycena_klienta !== undefined ? Number(body.wycena_klienta) : null,
      body.zaliczka !== undefined ? Number(body.zaliczka) : null,
      body.notatki || null,
      id
    ).run();

    const updated = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis WHERE id = ?`
    ).bind(id).first();

    return c.json({
      success: true,
      data: updated
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// POST /api/stolarska/projekty/:id/koszty - Dodanie pozycji kosztowej
stolarska.post('/projekty/:id/koszty', async (c) => {
  try {
    const id = c.req.param('id');
    const body = await c.req.json();

    if (!body.nazwa) {
      return c.json({ success: false, error: 'Pole "nazwa" pozycji kosztowej jest wymagane' }, 400);
    }

    await c.env.DB.prepare(
      `INSERT INTO stolar_koszty (projekt_id, kategoria, nazwa, jednostka, ilosc, cena_jedn, faktura_nr, data_kosztu, notatki)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      id,
      body.kategoria || 'material',
      body.nazwa,
      body.jednostka || 'szt',
      Number(body.ilosc || 1),
      Number(body.cena_jedn || 0),
      body.faktura_nr || null,
      body.data_kosztu || new Date().toISOString().slice(0, 10),
      body.notatki || null
    ).run();

    const updatedKpi = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis WHERE id = ?`
    ).bind(id).first();

    return c.json({
      success: true,
      data: updatedKpi
    }, 201);
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// POST /api/stolarska/projekty/:id/czas - Rejestracja roboczogodzin
stolarska.post('/projekty/:id/czas', async (c) => {
  try {
    const id = c.req.param('id');
    const body = await c.req.json();

    const godziny = Number(body.godziny || 0);
    if (godziny <= 0) {
      return c.json({ success: false, error: 'Liczba godzin musi być większa niż 0' }, 400);
    }

    await c.env.DB.prepare(
      `INSERT INTO stolar_czas_pracy (projekt_id, pracownik, data, godziny, stawka_godz, opis)
       VALUES (?, ?, ?, ?, ?, ?)`
    ).bind(
      id,
      body.pracownik || 'Stolarz',
      body.data || new Date().toISOString().slice(0, 10),
      godziny,
      Number(body.stawka_godz || 80),
      body.opis || ''
    ).run();

    const updatedKpi = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis WHERE id = ?`
    ).bind(id).first();

    return c.json({
      success: true,
      data: updatedKpi
    }, 201);
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

// POST /api/stolarska/projekty/:id/ai-analyze - Analiza rentowności i BOM przez AI Mesh
stolarska.post('/projekty/:id/ai-analyze', async (c) => {
  try {
    const id = c.req.param('id');

    const projekt: any = await c.env.DB.prepare(
      `SELECT * FROM v_stolar_projekt_kpis WHERE id = ?`
    ).bind(id).first();

    if (!projekt) {
      return c.json({ success: false, error: `Projekt ${id} nie istnieje` }, 404);
    }

    const { results: koszty } = await c.env.DB.prepare(
      `SELECT kategoria, nazwa, ilosc, cena_jedn, wartosc FROM stolar_koszty WHERE projekt_id = ?`
    ).bind(id).all();

    const prompt = `Analiza finansowo-techniczna projektu stolarskiego:
Projekt: ${projekt.nazwa} (ID: ${projekt.id})
Klient: ${projekt.klient || 'Niezdefiniowany'}
Status: ${projekt.status}
Wycena klienta: ${projekt.wycena_klienta} PLN
Zaliczka: ${projekt.zaliczka} PLN
Koszty materiałów i okuć: ${projekt.koszty_materialow} PLN
Koszty robocizny: ${projekt.koszty_robocizny} PLN
Zysk brutto: ${projekt.zysk_brutto} PLN
Marża: ${projekt.marza_proc}%

Zestawienie pozycji:
${(koszty || []).map((k: any) => `- [${k.kategoria}] ${k.nazwa}: ${k.ilosc} x ${k.cena_jedn} PLN = ${k.wartosc} PLN`).join('\n')}

Wygeneruj precyzyjną, profesjonalną analizę w formacie JSON (bez bloków markdown i bez wstępów):
{
  "confidence": 0.95,
  "insights": ["obserwacja 1", "obserwacja 2", "obserwacja 3"],
  "recommendations": ["rekomendacja 1 z kwotą lub optymalizacją", "rekomendacja 2"],
  "dashboard_hints": {
    "alert": "none|margin_low|cost_spike",
    "priority": "low|medium|high|critical"
  }
}`;

    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'Jesteś Senior Cost Estimator & Master Joiner w Stolarni AMS. Odpowiadasz wyłącznie surowym JSON.'
      },
      { role: 'user', content: prompt }
    ];

    const engine = new SmartRouterEngine({
      DB: c.env.DB,
      AI: c.env.AI,
      OMNIROUTE_URL: c.env.OMNIROUTE_URL,
      OMNIROUTE_API_KEY: c.env.OMNIROUTE_API_KEY,
      GROQ_API_KEY: c.env.GROQ_API_KEY,
      GOOGLE_API_KEY: c.env.GOOGLE_API_KEY,
      OPENROUTER_API_KEY: c.env.OPENROUTER_API_KEY,
      CEREBRAS_API_KEY: c.env.CEREBRAS_API_KEY
    });

    let aiResult: any;
    try {
      const response = await engine.executeWithFallback(messages, {
        requirement: 'free_unlimited',
        temperature: 0.2,
        max_tokens: 600
      });

      const cleanJson = response.content.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      aiResult = JSON.parse(cleanJson);
    } catch {
      aiResult = {
        confidence: 0.85,
        insights: [
          `Aktualna marża projektu wynosi ${projekt.marza_proc}%.`,
          `Łączne koszty bezpośrednie: ${projekt.koszty_materialow + projekt.koszty_robocizny} PLN.`
        ],
        recommendations: [
          projekt.marza_proc < 25 ? 'Zalecana rewizja cen materiałów i podniesienie wyceny.' : 'Rentowność w optymalnym przedziale.'
        ],
        dashboard_hints: {
          alert: projekt.marza_proc < 20 ? 'margin_low' : 'none',
          priority: projekt.marza_proc < 20 ? 'high' : 'low'
        }
      };
    }

    const taskId = `AI-STOLAR-${id}-${Date.now().toString().slice(-4)}`;

    await c.env.DB.prepare(
      `INSERT INTO stolar_insights (projekt_id, task_id, package_type, domain, confidence, insights_json, recommendations_json, dashboard_hints_json)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      id,
      taskId,
      '_04',
      'stolarska',
      aiResult.confidence || 0.9,
      JSON.stringify(aiResult.insights || []),
      JSON.stringify(aiResult.recommendations || []),
      JSON.stringify(aiResult.dashboard_hints || {})
    ).run();

    return c.json({
      success: true,
      taskId,
      data: aiResult
    });
  } catch (err: any) {
    return c.json({ success: false, error: err.message }, 500);
  }
});

export default stolarska;
