---
id: chunk_11
title: "KRYTYCZNE: regulacje WhatsApp/Meta 2026"
tags: [regulacje, ryzyko, whatsapp, compliance, "2026"]
target_workers: [orchestrator, Polaczek_Bohdan_01, Polaczek_cwaniaczek_01]
source: PRYWATNA_BAZA_RAG_AGENCI_HANDLOWI.md
priority: critical
---

Od stycznia 2026 Meta zakazuje generycznych/niecertyfikowanych botów AI w oficjalnym WhatsApp Business API. Sklep używający nieoficjalnego bota ryzykuje zablokowanie numeru telefonu. Zasada twarda: integracje wyłącznie z platformami certyfikowanymi przez Meta — żadnych "szybkich" obejść przez nieoficjalne API.

ZASTOSOWANIE: przy projektowaniu KAŻDEGO nowego bota komunikującego się przez WhatsApp — to PIERWSZY punkt audytu, przed wyborem stacka technicznego. Orchestrator powinien blokować/flagować każdy plan integracji WhatsApp, który nie przeszedł tej weryfikacji.
