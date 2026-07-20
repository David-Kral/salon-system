# Studia — personalizované odkazy (multi-tenant)

Jeden nasazený web, každému zubaři pošleš vlastní odkaz. Rozhraní se pro něj
změní podle jeho JSON souboru v této složce.

## Jak to funguje

Odkaz nese slug: `.../dentist/template/?studio=<slug>`

Šablona podle slugu načte `studia/<slug>.json` a přepíše:

- **`nazev`** — jméno kliniky / zubaře (navbar, patička, `<title>`),
- **`barva`** — jedna značková barva (hex). Z ní se odvodí accent a jemné
  tónování teplých ploch, takže se web obarví, ale zůstane čitelný.

Bez `?studio=` se zobrazí výchozí obsah z `config.json`.
Když slug neexistuje, ukáže se hláška (ne prázdná stránka).

## Přidat zubaře = jeden soubor

`studia/muj-slug.json`:

```json
{
  "nazev": "Zubní ordinace MUDr. Kdokoli",
  "barva": "#c2185b"
}
```

Odkaz pak je: `.../dentist/template/?studio=muj-slug`

> Volitelně lze v JSONu předat i `"colors": { ... }` pro úplné přepsání palety
> (klíče: `ink, paper, warm, oak, cream, fg, fgInv, muted, mutedInv, border, borderInv`).
> Pro běžné použití stačí `nazev` + `barva`.

## Příklady v této složce

| Odkaz | Zobrazí |
|---|---|
| `?studio=petr-seda`  | Zubní klinika MUDr. Petr Šeda — bordó |
| `?studio=usmev-jana` | Dentální studio Úsměv — tyrkysová |
