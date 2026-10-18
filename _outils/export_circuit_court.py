"""
Génère le PDF « Circuit court et économie locale » (chapitres 03 et 04 de la page Bas carbone),
présentés comme un seul et même chapitre, pour que les clients le joignent à leurs appels d'offres.

Lancer après chaque modification de ces chapitres :
    python3 _outils/export_circuit_court.py
Sortie : documents/plaquettes/L-Atelier-circuit-court-economie-locale.pdf
"""
import asyncio, datetime, pathlib
from playwright.async_api import async_playwright

SITE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = SITE / "documents" / "plaquettes" / "L-Atelier-circuit-court-economie-locale.pdf"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

PRINT_CSS = """
@page { size: A4; margin: 9mm 9mm 11mm; }
html, body { background: #fff !important; }
body > *:not(#export-root) { display: none !important; }
#export-root { display: block !important; }
.reveal { opacity: 1 !important; transform: none !important; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
/* Un seul chapitre : les deux cartes sont soudées en un bloc continu */
#export-root .cc { margin: 0 !important; border-radius: 22px 22px 0 0 !important; padding-bottom: 36px !important; }
#export-root .el { margin: 0 !important; border-radius: 0 0 22px 22px !important; padding-top: 30px !important; }
#export-root .el::before { display: none; }
#export-root .cc-dl, #export-root .lva-hint { display: none !important; }
#export-root #circuit-court .cc-head { max-width: 56% !important; }
#export-root .cc-brand { position: absolute !important; top: 30px; right: 36px; margin: 0 !important; zoom: .9; }
.cc-def, .cc-chain, .cc-zero-wrap, .cc-args, .lva, .el-foot, .el .cc-head { break-inside: avoid; }
.xp-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; font: 600 11.5px Inter, sans-serif; color: #1F3A5F; margin-bottom: 5mm; border-bottom: 2px solid #F07F2C; padding-bottom: 3mm; }
.xp-head b { font-family: Fraunces, Georgia, serif; font-weight: 500; font-size: 17px; }
.xp-head span { color: #5F5F5F; font-weight: 500; text-align: right; line-height: 1.5; }
.xp-foot { font: 400 10.5px Inter, sans-serif; color: #5F5F5F; text-align: center; margin-top: 4mm; }
"""

async def main():
    d = datetime.date.today()
    date_fr = f"{MOIS[d.month - 1]} {d.year}"
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto((SITE / "peinture-bas-carbone.html").as_uri())
        await pg.wait_for_timeout(1200)
        await pg.evaluate("""(date) => {
          const r = document.createElement('div'); r.id = 'export-root';
          r.innerHTML = '<div class="xp-head"><b>Circuit court et économie locale en Gironde</b>'
            + '<span>L\\'Atelier — Marchand de couleurs · Mérignac &amp; La Teste-de-Buch<br/>www.latelier33.fr · contact@latelier33.fr · 05 56 28 89 44</span></div>';
          const cc = document.getElementById('circuit-court').cloneNode(true);
          const el = document.getElementById('economie-locale').cloneNode(true);
          // Un seul chapitre : on retire la numérotation 03 / 04
          cc.querySelector('.engagement-eyebrow').textContent = 'Circuit court';
          el.querySelector('.engagement-eyebrow').textContent = 'Économie locale';
          r.appendChild(cc); r.appendChild(el);
          r.insertAdjacentHTML('beforeend', '<p class="xp-foot">Extrait de www.latelier33.fr/peinture-bas-carbone.html — ' + date + '</p>');
          document.body.appendChild(r);
        }""", date_fr)
        await pg.add_style_tag(content=PRINT_CSS)
        await pg.emulate_media(media="print")
        await pg.wait_for_timeout(400)
        await pg.pdf(path=str(SORTIE), format="A4", print_background=True, scale=0.62, prefer_css_page_size=True)
        await b.close()
    print("PDF :", SORTIE)

if __name__ == "__main__":
    asyncio.run(main())
