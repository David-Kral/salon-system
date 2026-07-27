# Studia — personalizované odkazy (multi-tenant)

Jeden nasazený web, každému zubaři pošleš vlastní odkaz `?studio=<slug>`.
Podle slugu se načte `studia/<slug>.json` a přepíše **jméno v hlavičce**
(nahradí logo textem) a **značkovou barvu** webu. Zbytek stránky zůstává stejný.

Přidat zubaře = jeden soubor `public/studia/<slug>.json`:

```json
{ "nazev": "MUDr. Kdokoli", "barva": "#4a5d7e" }
```

Odkaz: `.../?studio=<slug>`. Bez parametru se zobrazí výchozí logo a branding.

> Domident je monochromatický (charcoal/mist) — značková barva tónuje tmavý ink,
> takže se nejlépe hodí tmavší, sytější barvy. Volitelně lze předat i
> `"colors": { "charcoal": "...", ... }` pro přesné přepsání palety.
