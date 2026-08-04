"""Z hotovych .txt udela HTML maily ve stylu fitego.cz.

Text se NEPISE znovu — parsuje se z MAILY-195-242.txt a MAILY-DAVKA-B.txt,
takze zneni je slovo za slovem stejne jako v textove verzi.

Vystup: pro kazdou davku jedna HTML stranka s nahledem vsech mailu.
U kazdeho je tlacitko "Kopirovat HTML" (vlozi se do Roundcube pres
zobrazeni zdrojoveho kodu) a soucasne se da oznacit a zkopirovat
vyrenderovana verze.

Design tokeny odectene z fitego.cz (svetle tema):
  pozadi #FFFFFF, text #0A2842, plochy #F1F5F9, ramecky #E1E7EF,
  tlumeny text #667B99, tlacitko pill 9999px / 10px 24px / weight 600,
  fonty: Plus Jakarta Sans (nadpisy) + Inter (text)

Emailova specifika:
  * tabulkovy layout + inline styly (klienti ignoruji <style>)
  * bulletproof tlacitko vcetne VML fallbacku pro Outlook (jinak by
    prisel o zakulaceni i vysku)
  * skryty preheader — ridi text, ktery se ukaze v nahledu schranky
  * odstavce vlevo (centrovany dlouhy text se spatne cte), nadpis,
    tlacitko a paticka na stred

Spusteni:  python gen-maily-html.py
"""

import html as H
import json
import re

INK = "#0A2842"
MUTED = "#667B99"
SURFACE = "#F1F5F9"
BORDER = "#E1E7EF"
WHITE = "#FFFFFF"
FONT = ("'Plus Jakarta Sans','Inter',-apple-system,BlinkMacSystemFont,"
        "'Segoe UI',Roboto,Helvetica,Arial,sans-serif")

SIGN_START = "S pozdravem,"


def parse(path):
    """Rozdeli .txt na maily. Vraci list dictu s klici:
    nazev, flags, komu, predmet, items (p/url v poradi), covered."""
    lines = open(path, encoding="utf-8").read().split("\n")
    starts = [i for i, ln in enumerate(lines) if re.match(r"^\d+\. \S", ln)]
    mails = []
    for n, s in enumerate(starts):
        e = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[s:e]
        head = block[0]
        num, rest = head.split(".", 1)
        flags = ""
        m = re.search(r"\s{2,}\[(.+?)\]\s*$", rest)
        if m:
            flags = m.group(1)
            rest = rest[: m.start()]
        nazev = rest.strip()

        covered = any("NEPOSILAT" in ln for ln in block[:5])
        komu = predmet = None
        items = []
        i = 0
        while i < len(block):
            ln = block[i].strip()
            if ln == "KOMU ↓":
                komu = block[i + 1].strip(); i += 2; continue
            if ln == "PREDMET ↓":
                predmet = block[i + 1].strip(); i += 2; continue
            if ln == SIGN_START:
                break
            i += 1
        # telo: od "Dobrý den," po podpis
        try:
            b0 = next(k for k, ln in enumerate(block) if ln.strip() == "Dobrý den,")
        except StopIteration:
            mails.append(dict(num=int(num), nazev=nazev, flags=flags, komu=komu,
                              predmet=predmet, items=[], covered=covered))
            continue
        b1 = next((k for k, ln in enumerate(block) if ln.strip() == SIGN_START), len(block))
        for ln in block[b0 + 1:b1]:
            t = ln.strip()
            if not t:
                continue
            if t.startswith("http"):
                items.append(("url", t))
            else:
                items.append(("p", t))
        mails.append(dict(num=int(num), nazev=nazev, flags=flags, komu=komu,
                          predmet=predmet, items=items, covered=covered))
    return mails


def button(url, label="Zobrazit ukázku"):
    """Bulletproof pill tlacitko. VML varianta drzi tvar i vysku v Outlooku."""
    return f"""
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto;">
  <tr><td align="center" style="border-radius:9999px;background:{INK};">
    <!--[if mso]>
    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word"
      href="{H.escape(url, quote=True)}" style="height:46px;v-text-anchor:middle;width:230px;"
      arcsize="50%" stroke="f" fillcolor="{INK}">
      <w:anchorlock/>
      <center style="color:{WHITE};font-family:Arial,sans-serif;font-size:16px;font-weight:600;">{label} &#8594;</center>
    </v:roundrect>
    <![endif]-->
    <!--[if !mso]><!-- -->
    <a href="{H.escape(url, quote=True)}" target="_blank"
       style="display:inline-block;padding:13px 30px;font-family:{FONT};font-size:16px;font-weight:600;
              line-height:20px;color:{WHITE};text-decoration:none;border-radius:9999px;background:{INK};">
      {label} <span style="font-size:15px;">&#8594;</span>
    </a>
    <!--<![endif]-->
  </td></tr>
</table>"""


def email_html(m):
    """Jeden mail jako samostatny HTML dokument."""
    paras = [t for k, t in m["items"] if k == "p"]
    preheader = H.escape(paras[0][:110] + "…") if paras else ""
    body = []
    first_url_done = False
    for kind, val in m["items"]:
        if kind == "p":
            body.append(
                f'<p style="margin:0 0 18px 0;font-family:{FONT};font-size:15px;'
                f'line-height:25px;color:{INK};text-align:left;">{H.escape(val)}</p>')
        else:
            label = "Zobrazit ukázku" if not first_url_done else "Zobrazit druhou pobočku"
            body.append(f'<div style="margin:26px 0 28px 0;">{button(val, label)}</div>')
            body.append(
                f'<p style="margin:0 0 18px 0;font-family:{FONT};font-size:12px;'
                f'line-height:18px;color:{MUTED};text-align:center;">'
                f'{H.escape(val)}</p>')
            first_url_done = True

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{H.escape(m["predmet"] or "")}</title>
</head>
<body style="margin:0;padding:0;background:{SURFACE};">
<div style="display:none;font-size:1px;color:{SURFACE};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{SURFACE};">
<tr><td align="center" style="padding:28px 12px;">

  <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"
         style="width:600px;max-width:600px;background:{WHITE};border:1px solid {BORDER};border-radius:14px;">

    <tr><td align="center" style="padding:30px 34px 6px 34px;">
      <div style="font-family:{FONT};font-size:21px;font-weight:700;letter-spacing:-0.4px;color:{INK};">fitego</div>
      <div style="height:1px;background:{BORDER};margin:22px 0 0 0;line-height:1px;">&nbsp;</div>
    </td></tr>

    <tr><td style="padding:26px 34px 0 34px;">
      <p style="margin:0 0 18px 0;font-family:{FONT};font-size:15px;line-height:25px;color:{INK};text-align:left;">Dobrý den,</p>
      {''.join(body)}
    </td></tr>

    <tr><td style="padding:6px 34px 30px 34px;">
      <div style="height:1px;background:{BORDER};margin:0 0 20px 0;line-height:1px;">&nbsp;</div>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr><td align="center" style="font-family:{FONT};font-size:14px;line-height:22px;color:{INK};">
          <strong style="font-weight:600;">David Král</strong><br>
          <a href="tel:+420777122178" style="color:{MUTED};text-decoration:none;">777 122 178</a>
          &nbsp;·&nbsp;
          <a href="https://fitego.cz" style="color:{MUTED};text-decoration:none;">fitego.cz</a>
        </td></tr>
      </table>
    </td></tr>

  </table>

  <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">
    <tr><td align="center" style="padding:16px 20px 0 20px;font-family:{FONT};font-size:11px;line-height:17px;color:{MUTED};">
      Tvorba webů a systémů na míru · fitego.cz
    </td></tr>
  </table>

</td></tr>
</table>
</body>
</html>"""


def page(mails, title, note_lines, out):
    """Prehledova stranka: nahled + zdrojak ke zkopirovani."""
    cards = []
    for m in mails:
        if m["covered"]:
            cards.append(f"""
<section class="card muted">
  <h2>{m['num']}. {H.escape(m['nazev'])}</h2>
  <p class="warn">POKRYTO jiným mailem (stejná adresa) — neposílat.</p>
</section>""")
            continue
        src = email_html(m)
        cards.append(f"""
<section class="card">
  <h2>{m['num']}. {H.escape(m['nazev'])}{f' <span class="flag">{H.escape(m["flags"])}</span>' if m['flags'] else ''}</h2>
  <div class="meta">
    {f'<div><span>KOMU</span><code>{H.escape(m["komu"])}</code></div>' if m['komu'] else ''}
    <div><span>PŘEDMĚT</span><code>{H.escape(m['predmet'] or '')}</code></div>
  </div>
  <div class="actions">
    <button onclick="copySrc(this)">Kopírovat HTML</button>
    <span class="hint">→ v Roundcube přepni na HTML a vlož přes „zdrojový kód“</span>
  </div>
  <textarea class="src" readonly>{H.escape(src)}</textarea>
  <div class="preview">{src.split('<body', 1)[1].split('>', 1)[1].rsplit('</body>', 1)[0]}</div>
</section>""")

    notes = "".join(f"<li>{n}</li>" for n in note_lines)
    doc = f"""<!DOCTYPE html>
<html lang="cs"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(title)}</title>
<style>
 :root{{--ink:{INK};--muted:{MUTED};--surface:{SURFACE};--border:{BORDER}}}
 *{{box-sizing:border-box}}
 body{{margin:0;background:#fff;color:var(--ink);
   font:15px/1.6 'Plus Jakarta Sans',Inter,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}}
 header{{padding:34px 20px 10px;text-align:center;border-bottom:1px solid var(--border)}}
 header h1{{margin:0 0 6px;font-size:24px;letter-spacing:-.4px}}
 header p{{margin:0;color:var(--muted);font-size:14px}}
 .notes{{max-width:760px;margin:22px auto;padding:16px 20px;background:var(--surface);
   border:1px solid var(--border);border-radius:12px}}
 .notes ul{{margin:0;padding-left:20px}} .notes li{{margin:5px 0;font-size:14px}}
 .card{{max-width:760px;margin:26px auto;padding:20px;border:1px solid var(--border);border-radius:14px}}
 .card.muted{{opacity:.6}}
 .card h2{{margin:0 0 12px;font-size:17px}}
 .flag{{font-size:11px;font-weight:600;color:#8a5a00;background:#fff6e0;
   border:1px solid #f0dca8;border-radius:99px;padding:2px 9px;vertical-align:middle}}
 .warn{{margin:0;color:#9a3412;font-size:14px}}
 .meta div{{display:flex;gap:10px;align-items:center;margin:4px 0;flex-wrap:wrap}}
 .meta span{{font-size:10px;letter-spacing:.09em;color:var(--muted);min-width:74px}}
 .meta code{{font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
   background:var(--surface);border:1px solid var(--border);border-radius:7px;padding:4px 9px;
   user-select:all;word-break:break-all}}
 .actions{{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:14px 0 0}}
 .actions button{{font:600 14px 'Plus Jakarta Sans',Inter,sans-serif;color:#fff;background:var(--ink);
   border:0;border-radius:999px;padding:10px 22px;cursor:pointer}}
 .actions button.ok{{background:#15803d}}
 .hint{{font-size:12px;color:var(--muted)}}
 .src{{display:none}}
 .preview{{margin-top:16px;border:1px solid var(--border);border-radius:12px;overflow:hidden}}
 @media(max-width:640px){{.card{{margin:18px 10px}}}}
</style></head><body>
<header><h1>{H.escape(title)}</h1><p>Náhled je to, co adresát uvidí. Text je totožný s .txt verzí.</p></header>
<div class="notes"><ul>{notes}</ul></div>
{''.join(cards)}
<script>
function copySrc(btn){{
  const ta = btn.closest('.card').querySelector('.src');
  const done = () => {{ const t=btn.textContent; btn.textContent='Zkopírováno ✓'; btn.classList.add('ok');
    setTimeout(()=>{{btn.textContent=t;btn.classList.remove('ok')}},1600); }};
  // navigator.clipboard nemusi byt dostupny na file:// — proto fallback
  if (navigator.clipboard && window.isSecureContext) {{
    navigator.clipboard.writeText(ta.value).then(done, legacy);
  }} else legacy();
  function legacy(){{
    ta.style.display='block'; ta.select();
    try {{ document.execCommand('copy'); done(); }}
    catch(e) {{ alert('Zkopíruj ručně z označeného pole.'); }}
    ta.style.display='none';
  }}
}}
</script>
</body></html>"""
    open(out, "w", encoding="utf-8").write(doc)
    return doc


A = parse("MAILY-195-242.txt")
B = parse("MAILY-DAVKA-B.txt")

page(A, "Maily — dávka A (ordinace bez webu, řádky 195–242)", [
    "<strong>46 mailů.</strong> Adresáta si vyplňte sám — v tabulce u těchto řádků e-maily nejsou.",
    "Šablona ukázek: <code>ukazka-2</code>. Odstavec o rezervačním formuláři je od mailu 12 dál.",
    "<strong>ř. 195 a ř. 204</strong> mají vlastní web — jejich text je psaný na redesign.",
    "Odstavce jsou zarovnané vlevo záměrně: vycentrovaný dlouhý text se čte špatně. "
    "Nadpis, tlačítko a podpis jsou na střed.",
], "MAILY-DAVKA-A.html")

page(B, "Maily — dávka B (51 ordinací, šablona Dentaline)", [
    "<strong>47 mailů k odeslání</strong> z 51 — čtyři adresy se opakují (dvě pobočky, jeden mail), "
    "takže druhý výskyt je označený jako pokrytý.",
    "<code>mkolc@cebtrum.cz</code> — doména vypadá jako překlep, nejspíš <code>centrum.cz</code>.",
    "<code>222x222@seznam.cz</code> — ověřte, že je správná.",
    "Kolčavová a MŽ (2×) už jsou v dávce A — pošlete jen jednu verzi.",
], "MAILY-DAVKA-B.html")

# ── kontroly ───────────────────────────────────────────────────────────
problems = []
for name, mails, expect in (("A", A, 46), ("B", B, 51)):
    if len(mails) != expect:
        problems.append(f"davka {name}: rozparsovano {len(mails)}, ocekavano {expect}")
    for m in mails:
        if m["covered"]:
            continue
        if not m["predmet"]:
            problems.append(f"{name}#{m['num']}: chybi predmet")
        if not any(k == "url" for k, _ in m["items"]):
            problems.append(f"{name}#{m['num']}: chybi odkaz")
        if len([1 for k, _ in m["items"] if k == "p"]) < 3:
            problems.append(f"{name}#{m['num']}: podezrele malo odstavcu")
        if name == "B" and not m["komu"]:
            problems.append(f"B#{m['num']}: chybi adresat")

send_a = sum(1 for m in A if not m["covered"])
send_b = sum(1 for m in B if not m["covered"])
print(f"MAILY-DAVKA-A.html — {send_a} mailu")
print(f"MAILY-DAVKA-B.html — {send_b} mailu (+{len(B)-send_b} pokryto jinym)")
print("problemy: " + ("; ".join(problems) if problems else "zadne"))
