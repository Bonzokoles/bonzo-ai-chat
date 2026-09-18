# Shopify i panel FAQ

## Gdzie co jest

OpisAI:
- panel: `https://yutro.company/app/panel/`

SklepGPT:
- panel i API: `https://chat.yutro.company`

ContentFactory:
- panel: `https://yutro.company/app/content`

## Typowe pytania prywatnego chata

### Jak podłączyć Shopify?

To zależy od produktu:
- OpisAI używa połączenia aplikacji Shopify i Admin API,
- SklepGPT używa `SHOPIFY_SHOP_DOMAIN` i `SHOPIFY_ACCESS_TOKEN` do pobierania katalogu.

### Gdzie ustawia się tokeny?

Zależnie od usługi:
- lokalnie w `.env`,
- produkcyjnie w Railway environment,
- w panelach tylko tam, gdzie dana aplikacja wymaga tokenu użytkownika lub admina.

### Czy wszystko jest public app?

Nie.

Na dziś:
- `OpisAI` działa jako podłączona aplikacja Shopify,
- `SklepGPT` to osobna usługa z panelem i widgetem,
- `LeadBot` nie jest gotową aplikacją Shopify.

### Co jest demo, a co działa produkcyjnie?

Produkcyjnie działają:
- OpisAI,
- SklepGPT,
- ContentFactory.

Demo / MVP / osobny tryb:
- LeadBot.
