# Studia — personalizované odkazy (multi-tenant)

Jeden nasazený web, každému zubaři pošleš vlastní odkaz `?studio=<slug>`.
Podle slugu se načte `studia/<slug>.json` a přepíše **jméno v hlavičce/patičce**
a **značkovou barvu** webu. Zbytek stránky zůstává stejný.

Přidat zubaře = jeden soubor `public/studia/<slug>.json`:

```json
{ "nazev": "MUDr. Kdokoli", "barva": "#c2185b" }
```

Odkaz: `.../?studio=<slug>`. Bez parametru se zobrazí výchozí branding.

> Volitelně lze předat i `"colors": { "primary": "...", ... }` pro přepsání
> konkrétních CSS proměnných. Pro běžné použití stačí `nazev` + `barva`.
