"""
Génère les plaquettes commerciales PDF (A4, 3 pages) des gammes L'Atelier 45 et TITANE hydro.
Toutes les données viennent des fiches techniques (documents/ft) et des FDES (documents/fdes).
Lancer :  python3 _outils/plaquettes/generer.py   (nécessite Playwright + Chromium)
Sorties :  documents/plaquettes/Plaquette-Atelier-45.pdf  et  Plaquette-Titane-Hydro.pdf
"""
import asyncio, base64, io, os, pathlib
import qrcode, qrcode.image.svg
from playwright.async_api import async_playwright

ICI = pathlib.Path(__file__).resolve().parent
SITE = ICI.parent.parent
FONTS = ICI / "fonts"

# Référence profession : FDES collectives SIPEV (valeurs moyennes, ramenées à 10 ans)
REF_IMPRESSION = 0.246   # impression (FDES collective utilisée pour TITANE hydro Prim)
REF_FINITION = 1.30      # finitions mat / velours / satin

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def img(nom):
    return "data:image/webp;base64," + b64(SITE / "images" / "produits" / nom)

def qr(url):
    im = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=0)
    s = io.BytesIO(); im.save(s); return s.getvalue().decode().replace('<?xml version=\'1.0\' encoding=\'UTF-8\'?>', "")

def fr(v):
    return (f"{v:.3f}" if v < 1 else f"{v:.2f}").replace(".", ",")

GAMMES = {
 "45": {
  "fichier": "Plaquette-Atelier-45.pdf",
  "logo": '<span class="b45">l\'atelier <span class="b45f">45</span></span>',
  "accent": "#F07F2C", "fond": "#15273F", "fond2": "#1F3A5F",
  "eyebrow": "La gamme cœur de chantier",
  "titre": "La performance <em>pro</em>,<br/>l'empreinte <span class=\"eco\">bas carbone</span>.",
  "intro": "Six peintures professionnelles fabriquées en France, de l'impression à la finition. "
           "Phase aqueuse, classées A+, conditionnées en fûts recyclés, avec une FDES pour chaque produit : "
           "dès <b>0,043 kg CO₂/m²</b> sur 10 ans.",
  "hero": ["45_impress_GT.webp", "45_Mat_2en1.webp", "45_impress_.webp"],
  "stats": [("0,043", "kg CO₂/m²", "Impress 45 Grands Travaux<br/>FDES vérifiée INIES"),
            ("&lt; 1 g/L", "COV", "Impress, Grands Travaux<br/>et Mat 45 2en1"),
            ("A+", "air intérieur", "toute la gamme aqueuse")],
  "pourquoi_titre": "Pourquoi choisir <span class=\"b45\">L'Atelier <span class=\"b45f\">45</span></span> ?",
  "pourquoi_intro": "Une gamme pensée pour les chantiers exigeants, où la performance technique se conjugue avec la réduction de l'empreinte carbone.",
  "atouts": [
    ("🌱", "Bas carbone mesuré", "Empreintes carbone issues des FDES : 0,043 (Impress GT), 0,125 (Mat 45 2en1), 0,164 (Impress evo) kg CO₂/m² sur 10 ans."),
    ("📄", "FDES & RE2020", "Une FDES pour chaque produit, utilisable dans le calcul carbone RE2020 de vos bâtiments."),
    ("💨", "COV ultra-réduits", "Moins de 1 g/L de COV sur Impress, Grands Travaux et Mat 45 2en1. Phase aqueuse, faible odeur."),
    ("A+", "Émissions A+", "Classement A+ pour la qualité de l'air intérieur sur toute la gamme aqueuse."),
    ("♻️", "Fûts recyclés", "Conditionnements issus de filières de recyclage : moins de plastique vierge sur vos chantiers."),
    ("🇫🇷", "Fabriquée en France", "Formulée avec nos partenaires fabricants français Théolaur (Colomiers) et SOFEC (Roquemaure)."),
  ],
  "produits": [
    ("Impression grands chantiers", "Impress 45 Grands Travaux", "45_impress_GT.webp",
     [("Rendement", "≈ 130 m²/seau"), ("Format", "16 L"), ("COV", "&lt; 1 g/L"), ("Aspect", "Mat")], 0.043, "FDES vérifiée"),
    ("Impression universelle", "Impress 45 evo", "45_impress_.webp",
     [("Rendement", "8 à 9 m²/L"), ("Format", "16 L"), ("COV", "&lt; 1 g/L"), ("Lessivable", "Classe 3")], 0.164, "FDES vérifiée"),
    ("Impression + finition 2 en 1", "Mat 45 2en1", "45_Mat_2en1.webp",
     [("Rendement", "8 à 9 m²/L"), ("Format", "16 L"), ("COV", "&lt; 1 g/L"), ("Lessivable", "Classe 2")], 0.125, "FDES provisoire"),
    ("Acrylique veloutée garnissante", "Velours 45", "45_velours.webp",
     [("Rendement", "7 à 9 m²/L"), ("Format", "16 L"), ("COV", "≤ 30 g/L"), ("Lessivable", "Classe 2")], None, ""),
    ("Acrylique satinée lessivable", "Satin 45", "45_satin.webp",
     [("Rendement", "8 à 10 m²/L"), ("Format", "16 L"), ("COV", "≤ 30 g/L"), ("Brillance", "14 % à 60°")], None, ""),
    ("Glycéro satinée · boiseries", "Glycéro 45", "45_glycero_satin.webp",
     [("Rendement", "10 à 12 m²/L"), ("Format", "16 L"), ("COV", "≤ 300 g/L (A/d)"), ("Brillance", "35 % à 60°")], None, ""),
  ],
  "carbone_titre": "Jusqu'à <em>10 fois moins</em> de CO₂ que la moyenne.",
  "carbone_intro": "Empreinte carbone pour 1 m² peint sur 10 ans, d'après les FDES, comparée à la valeur moyenne de la profession (FDES collectives SIPEV).",
  "barres": [("Impress 45 Grands Travaux", 0.043, "imp"), ("Impress 45 evo", 0.164, "imp"), ("Moyenne profession · impression", REF_IMPRESSION, "ref"),
             ("Mat 45 2en1", 0.125, "fin"), ("Moyenne profession · finition", REF_FINITION, "ref")],
  "bio": None,
  "partenaire": ("Fabriquée en France", "Une formulation française, <em>des partenaires de confiance</em>.",
                 "L'Atelier 45 est formulée avec nos partenaires fabricants français Théolaur (Colomiers) et SOFEC (Roquemaure). "
                 "Nos équipes en magasin connaissent chaque produit et vous accompagnent du choix à la mise en œuvre."),
 },
 "titane": {
  "fichier": "Plaquette-Titane-Hydro.pdf",
  "logo": '<span class="bti">TITANE <small>hydro</small></span>',
  "accent": "#F89B5A", "fond": "#1B1F3B", "fond2": "#2A2F55",
  "eyebrow": "La chimie du végétal",
  "titre": "Le biosourcé,<br/>en <em>version pro</em>.",
  "intro": "Quatre peintures en phase aqueuse, de l'impression à la finition. Fer de lance de la gamme, le TITANE hydro MV evo "
           "repose sur une résine alkyde végétale <b>biosourcée à 85 %</b>, avec <b>78 % de matières premières d'origine naturelle</b> "
           "sur le produit fini.",
  "hero": ["titane_hydro_prim.webp", "titane_hydro_mat_veloute.webp", "titane_hydro_velours.webp"],
  "stats": [("85 %", "résine biosourcée", "TITANE hydro MV evo"),
            ("0,210", "kg CO₂/m²", "MV evo · sur 10 ans<br/>FDES provisoire"),
            ("&lt; 1 g/L", "COV", "MV evo et Velours")],
  "pourquoi_titre": "Pourquoi choisir <span class=\"bti\">TITANE <small>hydro</small></span> ?",
  "pourquoi_intro": "Une gamme cohérente pour les chantiers où la performance environnementale et la santé des occupants ne se négocient pas.",
  "atouts": [
    ("🌿", "Résine biosourcée", "TITANE hydro MV evo : résine alkyde végétale biosourcée à 85 % et 78 % de matières premières naturelles."),
    ("🌱", "Bas carbone", "MV evo à 0,210 kg CO₂/m² sur 10 ans (FDES provisoire), impression et finition réunies."),
    ("💨", "Moins de 1 g/L de COV", "MV evo et Velours descendent sous 1 g/L de COV : idéal en milieu occupé et ERP."),
    ("A+", "Émissions A+", "Toute la gamme TITANE hydro est classée A+ pour la qualité de l'air intérieur."),
    ("📄", "FDES & RE2020", "Une FDES pour chaque produit, utilisable dans le calcul carbone RE2020."),
    ("♻️", "Fûts recyclés · France", "Conditionnements recyclés et fabrication française. MV evo fabriqué par SOFEC (Roquemaure)."),
  ],
  "produits": [
    ("Impression · accrochage", "TITANE hydro Prim", "titane_hydro_prim.webp",
     [("Rendement", "± 8 m²/L"), ("Format", "15 L"), ("COV", "≤ 30 g/L"), ("Aspect", "Mat")], None, "", "#3B1F5C"),
    ("Mat profond garnissant", "TITANE hydro Mat", "titane_hydro_mat.webp",
     [("Rendement", "± 9 m²/L"), ("Format", "14,4 / 15 L"), ("COV", "≤ 30 g/L"), ("Lessivable", "Classe 3")], None, "", "#232849"),
    ("Mat velouté 2 en 1 biosourcé", "TITANE hydro MV evo", "titane_hydro_mat_veloute.webp",
     [("Rendement", "12 à 14 m²/L"), ("Format", "4 et 15 L"), ("COV", "&lt; 1 g/L"), ("Lessivable", "Classe 1")], 0.210, "FDES provisoire", "#E8572F"),
    ("Velours 2 en 1 · séchage rapide", "TITANE hydro Velours", "titane_hydro_velours.webp",
     [("Rendement", "± 10 m²/L"), ("Format", "15 L"), ("COV", "&lt; 1 g/L"), ("Lessivable", "Classe 1")], None, "", "#1D4D2C"),
  ],
  "carbone_titre": "Environ <em>6 fois moins</em> de CO₂ que la moyenne.",
  "carbone_intro": "Empreinte carbone pour 1 m² peint sur 10 ans : le TITANE hydro MV evo, impression et finition réunies, face à la valeur moyenne de la profession pour une finition (FDES collective SIPEV).",
  "barres": [("TITANE hydro MV evo", 0.210, "fin"), ("Moyenne profession · finition", REF_FINITION, "ref")],
  "bio": (85, 78),
  "partenaire": ("Fabriquée en France", "La chimie du végétal, <em>fabriquée en France</em>.",
                 "Le TITANE hydro MV evo est fabriqué par SOFEC à Roquemaure (Gard). Sa résine alkyde végétale en émulsion remplace une partie des "
                 "matières d'origine pétrolière, sans renoncer à la grande blancheur ni à la lessivabilité classe 1."),
 },
}

CSS = """
@font-face { font-family: Fraunces; src: url(data:font/woff2;base64,%(fr)s) format('woff2'); font-weight: 100 900; font-style: normal; }
@font-face { font-family: Fraunces; src: url(data:font/woff2;base64,%(fri)s) format('woff2'); font-weight: 100 900; font-style: italic; }
@font-face { font-family: Barlow; src: url(data:font/woff2;base64,%(b7)s) format('woff2'); font-weight: 700; font-style: italic; }
@font-face { font-family: Barlow; src: url(data:font/woff2;base64,%(b8)s) format('woff2'); font-weight: 800; font-style: italic; }
@font-face { font-family: 'Barlow Condensed'; src: url(data:font/woff2;base64,%(bc7)s) format('woff2'); font-weight: 700; font-style: italic; }
@font-face { font-family: 'Barlow Condensed'; src: url(data:font/woff2;base64,%(bc8)s) format('woff2'); font-weight: 800; font-style: italic; }
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --acc: %(acc)s; --fond: %(fond)s; --fond2: %(fond2)s; --vert: #4A8B5C; --vertf: #2F6940; --mousse: #A8E6BE; --gris: #5F6670; --clair: #F6F3EE; }
body { font-family: Inter, sans-serif; color: #15273F; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; }
.page:last-child { page-break-after: auto; }
.b45 { font-family: Barlow, Inter, sans-serif; font-style: italic; font-weight: 700; }
.b45f { font-size: 1.35em; font-weight: 800; letter-spacing: -.02em; }
.bti { font-family: 'Barlow Condensed', Barlow, sans-serif; font-style: italic; font-weight: 800; letter-spacing: .5px; }
.bti small { font-size: .62em; font-weight: 700; letter-spacing: 0; }
.eyebrow { font-size: 8.5pt; letter-spacing: 2.4px; text-transform: uppercase; font-weight: 700; color: var(--acc); }
h2 { font-family: Fraunces, serif; font-weight: 400; font-size: 25pt; line-height: 1.08; letter-spacing: -.4px; color: #15273F; }
h2 em { font-style: italic; color: var(--vert); font-weight: 400; }

/* ---------- Couverture ---------- */
.cover { background: radial-gradient(120%% 80%% at 85%% 0%%, var(--fond2) 0%%, var(--fond) 62%%); color: #fff; padding: 18mm 16mm 14mm; }
.cover .stripes { position: absolute; top: -10mm; right: -6mm; width: 70mm; height: 70mm; background: repeating-linear-gradient(135deg, transparent 0 6mm, var(--acc) 6mm 7.2mm, transparent 7.2mm 13mm); opacity: .9; clip-path: polygon(30%% 0, 100%% 0, 100%% 70%%); }
.cover .logo { font-size: 30pt; color: #fff; line-height: 1; }
.cover .logo .b45f, .cover .logo .bti { color: var(--acc); }
.cover .maison { margin-top: 3mm; font-size: 8pt; letter-spacing: 2.6px; text-transform: uppercase; color: rgba(255,255,255,.7); font-weight: 600; }
.cover .eyebrow { margin-top: 20mm; display: block; }
.cover h1 { font-family: Fraunces, serif; font-weight: 300; font-size: 44pt; line-height: 1.02; letter-spacing: -1.2px; margin-top: 5mm; }
.cover h1 em { font-style: italic; color: var(--acc); font-weight: 400; }
.cover h1 .eco { color: var(--mousse); font-weight: 500; }
.cover .intro { margin-top: 7mm; font-size: 11pt; line-height: 1.6; color: rgba(255,255,255,.86); max-width: 150mm; font-weight: 300; }
.cover .intro b { color: #fff; font-weight: 600; }
.cover .pots { position: absolute; left: 0; right: 0; top: 136mm; height: 82mm; display: flex; justify-content: center; align-items: flex-end; gap: 4mm; }
.cover .pots img { height: 70mm; width: auto; filter: drop-shadow(0 6mm 6mm rgba(0,0,0,.45)); }
.cover .pots img:nth-child(2) { height: 80mm; }
.cover .floor { position: absolute; left: 30mm; right: 30mm; top: 212mm; height: 10mm; background: radial-gradient(ellipse at center, rgba(0,0,0,.4), transparent 70%%); }
.cover .stats { position: absolute; left: 16mm; right: 16mm; top: 226mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }
.stat { border: 1px solid rgba(255,255,255,.16); background: rgba(255,255,255,.06); border-radius: 4mm; padding: 4.5mm 5mm; }
.stat .v { font-family: Fraunces, serif; font-size: 22pt; line-height: 1; color: var(--mousse); }
.stat .u { font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1.4px; color: #fff; margin-top: 1.5mm; }
.stat .d { font-size: 7.5pt; line-height: 1.4; color: rgba(255,255,255,.65); margin-top: 1.5mm; }
.cover .pied { position: absolute; left: 16mm; right: 16mm; bottom: 10mm; display: flex; justify-content: space-between; align-items: flex-end; font-size: 7.5pt; color: rgba(255,255,255,.65); line-height: 1.5; }
.cover .pied b { color: #fff; font-weight: 600; }

/* ---------- Pages intérieures ---------- */
.top { height: 15mm; background: var(--fond); color: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 14mm; }
.top .logo { font-size: 14pt; }
.top .logo .b45f, .top .logo .bti { color: var(--acc); }
.top span.r { font-size: 7.5pt; letter-spacing: 1.4px; text-transform: uppercase; color: rgba(255,255,255,.7); }
.in { padding: 9mm 14mm 0; }
.lead { font-size: 9.5pt; line-height: 1.6; color: var(--gris); margin-top: 3mm; max-width: 165mm; }
.atouts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 6mm; }
.atout { background: var(--clair); border-radius: 3.5mm; padding: 3.2mm 4mm; border-left: 1.2mm solid var(--vert); }
.atout .i { font-size: 10.5pt; font-weight: 800; color: var(--vertf); float: left; margin-right: 2mm; line-height: 1.2; }
.atout h3 { font-size: 9.3pt; margin: .4mm 0 1.4mm; color: #15273F; line-height: 1.3; }
.atout p { font-size: 7.6pt; line-height: 1.5; color: var(--gris); }
.sect { margin-top: 6.5mm; }
.prods { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; margin-top: 4mm; }
.prod { display: grid; grid-template-columns: 22mm 1fr; gap: 2.5mm 3.5mm; align-content: start; border: 1px solid rgba(21,39,63,.1); border-radius: 3.5mm; padding: 3.5mm 4mm 3.5mm 3mm; position: relative; border-top: 1.2mm solid var(--pc, var(--acc)); }
.prod img { width: 22mm; height: 24mm; object-fit: contain; align-self: center; }
.prod .t { font-size: 6.8pt; letter-spacing: 1.2px; text-transform: uppercase; font-weight: 700; color: var(--pc, var(--acc)); }
.prod h4 { font-size: 11pt; margin: .8mm 0 2mm; color: #15273F; }
.prod dl { display: grid; grid-template-columns: repeat(2, auto); justify-content: start; gap: 1mm 6mm; }
.prod dt { font-size: 6pt; letter-spacing: 1px; text-transform: uppercase; color: #8A9099; font-weight: 600; }
.prod dd { font-size: 8pt; font-weight: 600; color: #15273F; }
.co2 { grid-column: 1 / -1; background: var(--vertf); color: #fff; border-radius: 2mm; padding: 1.6mm 3mm; display: flex; align-items: baseline; gap: 2mm; margin-top: .5mm; }
.co2 .k { font-size: 6.5pt; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; }
.co2 b { font-size: 10.5pt; }
.co2 small { font-size: 6.6pt; opacity: .9; }
.co2 .ty { margin-left: auto; font-size: 6.3pt; opacity: .85; }
.co2.prov { background: var(--vert); }
.foot { position: absolute; left: 0; right: 0; bottom: 0; height: 11mm; background: var(--fond); color: rgba(255,255,255,.8); font-size: 7.3pt; display: flex; justify-content: space-between; align-items: center; padding: 0 14mm; }
.foot b { color: var(--acc); }

/* ---------- Page 3 ---------- */
.bandeau { background: var(--fond); color: #fff; padding: 8mm 14mm 7mm; position: relative; }
.bandeau .logo { font-size: 14pt; }
.bandeau .logo .b45f, .bandeau .logo .bti { color: var(--acc); }
.bandeau h2 { color: #fff; margin-top: 5mm; font-size: 24pt; }
.bandeau h2 em { color: var(--mousse); }
.bandeau .lead { color: rgba(255,255,255,.75); }
.chart { margin-top: 7mm; background: #fff; border-radius: 4mm; padding: 5mm 6mm; border: 1px solid rgba(21,39,63,.08); }
.bar { display: grid; grid-template-columns: 56mm 1fr 18mm; align-items: center; gap: 3mm; margin: 2.6mm 0; }
.bar .n { font-size: 9.5pt; font-weight: 600; }
.bar .n.ref { color: #8A9099; font-weight: 500; }
.bar .tr { height: 7mm; background: #EEF0F2; border-radius: 1.5mm; overflow: hidden; }
.bar .f { height: 100%%; border-radius: 1.5mm; }
.bar .f.imp { background: #3F9B4C; } .bar .f.fin { background: var(--vertf); } .bar .f.ref { background: #B9C0C8; }
.bar .v { font-size: 11pt; font-weight: 700; text-align: right; font-variant-numeric: tabular-nums; }
.note { font-size: 6.8pt; color: #8A9099; line-height: 1.5; margin-top: 3mm; }
.duo { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 6mm; }
.card { background: #fff; border-radius: 4mm; padding: 5mm 6mm; border: 1px solid rgba(21,39,63,.08); }
.card h3 { font-family: Fraunces, serif; font-weight: 400; font-size: 16pt; line-height: 1.2; color: #15273F; margin-top: 2mm; }
.card h3 em { font-style: italic; color: var(--vert); }
.card p { font-size: 9pt; line-height: 1.6; color: var(--gris); margin-top: 2.5mm; }
.ring { display: flex; gap: 6mm; margin-top: 4mm; }
.ring div { text-align: center; font-size: 7.3pt; color: var(--gris); line-height: 1.35; }
.ring svg { width: 21mm; height: 21mm; display: block; margin: 0 auto 1.5mm; }
.mag { position: absolute; left: 0; right: 0; bottom: 0; background: var(--fond); color: #fff; padding: 8mm 14mm 8mm; display: grid; grid-template-columns: 1fr 1fr 30mm; gap: 6mm; align-items: center; }
.mag h4 { font-family: Fraunces, serif; font-weight: 400; font-size: 13pt; }
.mag h4 em { color: var(--acc); }
.mag p { font-size: 7.8pt; line-height: 1.6; color: rgba(255,255,255,.78); margin-top: 1.5mm; }
.mag p b { color: #fff; }
.mag .qr { background: #fff; border-radius: 2.5mm; padding: 2.5mm; text-align: center; }
.mag .qr svg { width: 100%%; height: auto; display: block; }
.mag .qr span { font-size: 5.8pt; color: #15273F; font-weight: 600; display: block; margin-top: 1.2mm; line-height: 1.3; }
.mag .tete { grid-column: 1 / -1; display: flex; justify-content: space-between; align-items: baseline; }
.mag .tete .eyebrow { color: var(--acc); }
.mag .tete .web { font-size: 9pt; font-weight: 600; color: var(--acc); }
"""

def anneau(pct, coul, label):
    r = 40; c = 2 * 3.14159 * r; d = c * pct / 100
    return (f'<div><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="{r}" fill="none" stroke="#E2E6E3" stroke-width="12"/>'
            f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{coul}" stroke-width="12" stroke-linecap="round" stroke-dasharray="{d:.1f} {c:.1f}" transform="rotate(-90 50 50)"/>'
            f'<text x="50" y="57" text-anchor="middle" font-family="Fraunces" font-size="24" fill="#15273F">{pct} %</text></svg>{label}</div>')

def construire(cle):
    g = GAMMES[cle]
    css = CSS % {"fr": b64(FONTS / "fraunces-latin-wght-normal.woff2"), "fri": b64(FONTS / "fraunces-latin-wght-italic.woff2"),
                 "b7": b64(FONTS / "barlow-latin-700-italic.woff2"), "b8": b64(FONTS / "barlow-latin-800-italic.woff2"),
                 "bc7": b64(FONTS / "barlow-condensed-latin-700-italic.woff2"), "bc8": b64(FONTS / "barlow-condensed-latin-800-italic.woff2"),
                 "acc": g["accent"], "fond": g["fond"], "fond2": g["fond2"]}
    stats = "".join(f'<div class="stat"><div class="v">{v}</div><div class="u">{u}</div><div class="d">{d}</div></div>' for v, u, d in g["stats"])
    pots = "".join(f'<img src="{img(p)}" alt=""/>' for p in g["hero"])
    p1 = f"""<section class="page cover"><div class="stripes"></div>
<div class="logo">{g["logo"]}</div><div class="maison">L'Atelier · Marchand de couleurs · Gironde</div>
<span class="eyebrow">— {g["eyebrow"]}</span><h1>{g["titre"]}</h1><p class="intro">{g["intro"]}</p>
<div class="floor"></div><div class="pots">{pots}</div><div class="stats">{stats}</div>
<div class="pied"><div><b>L'Atelier — Marchand de couleurs</b><br/>Mérignac · 7 avenue de la Grande Semaine · 05 56 28 89 44<br/>La Teste-de-Buch · 1111 av. du Parc des Expositions · 05 57 52 64 77</div>
<div style="text-align:right">Plaquette commerciale<br/><b>Édition 2026</b></div></div></section>"""

    atouts = "".join(f'<div class="atout"><div class="i">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in g["atouts"])
    prods = ""
    for p in g["produits"]:
        t, n, im, specs, co2, typ = p[:6]; pc = p[6] if len(p) > 6 else None
        dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in specs)
        badge = (f'<div class="co2{" prov" if "provisoire" in typ else ""}"><span class="k">Bas carbone</span><b>{fr(co2)}</b><small>kg CO₂/m² · 10 ans</small><span class="ty">{typ}</span></div>' if co2 else "")
        style = f' style="--pc:{pc}"' if pc else ""
        prods += f'<div class="prod"{style}><img src="{img(im)}" alt=""/><div><div class="t">{t}</div><h4>{n}</h4><dl>{dl}</dl></div>{badge}</div>'
    nb = len(g["produits"])
    p2 = f"""<section class="page"><div class="top"><div class="logo">{g["logo"]}</div><span class="r">Bas carbone · A+ · Fabriquée en France</span></div>
<div class="in"><span class="eyebrow">— Nos engagements</span><h2 style="margin-top:2mm">{g["pourquoi_titre"]}</h2><p class="lead">{g["pourquoi_intro"]}</p>
<div class="atouts">{atouts}</div>
<div class="sect"><span class="eyebrow">— Les {nb} produits de la gamme</span><h2 style="margin-top:2mm">Du fond à la finition, <em>un seul système</em>.</h2>
<div class="prods">{prods}</div></div></div>
<div class="foot"><span>L'Atelier — Marchand de couleurs · Mérignac &amp; La Teste-de-Buch</span><span>Fiches techniques &amp; FDES : <b>latelier33.fr/documents.html</b></span></div></section>"""

    mx = max(v for _, v, _ in g["barres"])
    barres = "".join(f'<div class="bar"><div class="n{" ref" if k == "ref" else ""}">{n}</div><div class="tr"><div class="f {k}" style="width:{max(v / mx * 100, 2.5):.1f}%"></div></div><div class="v">{fr(v)}</div></div>' for n, v, k in g["barres"])
    if g["bio"]:
        gauche = (f'<div class="card"><span class="eyebrow" style="color:var(--vertf)">— Biosourcé</span><h3>Moins de pétrole, <em>plus de végétal</em>.</h3>'
                  f'<div class="ring">{anneau(g["bio"][0], "#2F6940", "de la résine<br/>biosourcée")}{anneau(g["bio"][1], "#4A8B5C", "de matières premières<br/>d\'origine naturelle")}</div>'
                  f'<p>TITANE hydro MV evo, produit fini. Une alkyde végétale en émulsion aqueuse, à moins de 1 g/L de COV.</p></div>')
    else:
        gauche = ('<div class="card"><span class="eyebrow" style="color:var(--vertf)">— RE2020</span><h3>Vos FDES, <em>prêtes pour le calcul carbone</em>.</h3>'
                  '<p>La RE2020 calcule l\'empreinte carbone du bâtiment à partir des FDES de ses produits. Sans FDES, une valeur par défaut pénalisante est appliquée. '
                  'Chaque produit L\'Atelier 45 dispose de la sienne : transmettez-la dès le devis à votre bureau d\'études.</p></div>')
    pt, ph, pp = g["partenaire"]
    droite = f'<div class="card"><span class="eyebrow" style="color:var(--vertf)">— {pt}</span><h3>{ph}</h3><p>{pp}</p></div>'
    q = qr("https://www.latelier33.fr/peinture-bas-carbone.html")
    p3 = f"""<section class="page" style="background:var(--clair)"><div class="bandeau"><div class="logo">{g["logo"]}</div>
<span class="eyebrow" style="display:block;margin-top:5mm">— Bas carbone, preuves à l'appui</span><h2>{g["carbone_titre"]}</h2><p class="lead">{g["carbone_intro"]}</p></div>
<div class="in"><div class="chart"><span class="eyebrow" style="color:var(--vertf)">kg CO₂ éq. / m² · 10 ans</span>{barres}
<p class="note">Indicateur « changement climatique – total » (modules A1 à C4) des FDES, ramené à 10 ans. FDES provisoire : calculée, vérification INIES en cours. Moyenne profession : FDES collectives SIPEV, non spécifiques à un produit.</p></div>
<div class="duo">{gauche}{droite}</div></div>
<div class="mag"><div class="tete"><span class="eyebrow">— Deux magasins, une expertise</span><span class="web">www.latelier33.fr</span></div>
<div><h4>L'Atelier <em>CUB</em> · Mérignac</h4><p>7 avenue de la Grande Semaine, 33700 Mérignac<br/><b>05 56 28 89 44</b> · Lun–Ven 8h–12h / 14h–18h</p></div>
<div><h4>L'Atelier <em>Bassin</em> · La Teste</h4><p>1111 av. du Parc des Expositions, 33260 La Teste-de-Buch<br/><b>05 57 52 64 77</b> · Lun–Ven 8h–12h / 14h–18h · Sam 9h–12h</p></div>
<div class="qr">{q}<span>Comparatif carbone<br/>de 20 peintures</span></div>
<p style="grid-column:1/-1;margin-top:0">contact@latelier33.fr · Devis, échantillons et FDES : latelier33.fr/espace-pro.html</p></div></section>"""
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"/><title>{g["fichier"]}</title><style>{css}</style></head><body>{p1}{p2}{p3}</body></html>'

async def main(sortie=None):
    sortie = pathlib.Path(sortie) if sortie else SITE / "documents" / "plaquettes"
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for cle in GAMMES:
            h = construire(cle)
            (ICI / f"{cle}.html").write_text(h, encoding="utf-8")
            pg = await b.new_page()
            await pg.set_content(h, wait_until="load"); await pg.wait_for_timeout(400)
            await pg.pdf(path=str(sortie / GAMMES[cle]["fichier"]), format="A4", print_background=True, prefer_css_page_size=True)
            await pg.close()
        await b.close()

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else None))
