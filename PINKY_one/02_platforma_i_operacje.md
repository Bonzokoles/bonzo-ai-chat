# Platforma i operacje

## Główne usługi

- `api.yutro.company` -> OpisAI API
- `chat.yutro.company` -> SklepGPT
- `content.yutro.company` -> ContentFactory

## OpisAI i Shopify

OpisAI jest podłączone do Shopify przez istniejące dane aplikacji i Admin API.

Kluczowe elementy:
- aplikacja Shopify: `OpisAI`
- panel aplikacji: `https://yutro.company/app/panel/`
- wymagane środowisko: `SHOPIFY_SHOP_DOMAIN`, `SHOPIFY_ACCESS_TOKEN`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET`

## SklepGPT i Shopify

SklepGPT ma już działający sync katalogu Shopify do RAG.

Wymagane zmienne:
- `SHOPIFY_SHOP_DOMAIN`
- `SHOPIFY_ACCESS_TOKEN`
- `SKLEPGPT_API_TOKEN`
- `SKLEPGPT_PUBLIC_WIDGET_TOKEN`

SklepGPT jest już wdrożony produkcyjnie i umie:
- pobierać produkty,
- synchronizować produkty do RAG,
- odpowiadać na pytania z wiedzy i katalogu.

## Co jest publiczne, a co prywatne

Publiczne:
- panel i widget SklepGPT,
- panel OpisAI,
- publiczne domeny usług.

Prywatne:
- tokeny,
- runbooki operacyjne,
- decyzje wdrożeniowe,
- prywatny chatbox z tego katalogu.
