"""
Génère les pages magasins (référencement local) :
  - magasin-peinture-merignac.html        (L'Atelier CUB)
  - magasin-peinture-la-teste-de-buch.html (L'Atelier Bassin)
et met à jour le sitemap.

Données : ci-dessous (coordonnées, horaires, services) + _outils/avis_google.json (notes et avis Google réels).
Lancer :  python3 _outils/magasins.py
"""
import json, os, html, datetime, re
import gen

O = os.path.dirname(os.path.abspath(__file__)) + os.sep
AV = json.load(open(O + "avis_google.json", encoding="utf-8"))
E = lambda s: html.escape(s, quote=True)

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
JOURS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEMAINE = [("08:00", "12:00"), ("14:00", "18:00")]

MAGASINS = [
    {
        "cle": "cub", "fichier": "magasin-peinture-merignac.html",
        "nom": "L'Atelier CUB", "court": "CUB", "ville": "Mérignac", "cp": "33700",
        "rue": "7 avenue de la Grande Semaine", "tel": "05 56 28 89 44", "tel_int": "+33556288944",
        "zone_nom": "la métropole bordelaise",
        "titre": "Magasin de peinture à Mérignac — L'Atelier CUB | Bordeaux Métropole",
        "description": "Magasin de peinture professionnelle à Mérignac : peintures bas carbone L'Atelier 45 et TITANE hydro, mise à la teinte, conseil technique, livraison chantier. Ouvert du lundi au vendredi.",
        "h1": "L'Atelier <em>CUB</em>, votre magasin de peinture à Mérignac.",
        "chapo": "Au cœur de la métropole bordelaise, notre magasin de Mérignac accueille professionnels et particuliers : peintures pro bas carbone, mise à la teinte, bureau d'études et livraison sur vos chantiers.",
        "horaires": {0: SEMAINE, 1: SEMAINE, 2: SEMAINE, 3: SEMAINE, 4: SEMAINE},
        "photo_web": "images/opt/magasin-merignac-1100.webp", "photo": ("images/magasin-merignac.webp", "Façade du magasin L'Atelier CUB à Mérignac"),
        "photo2": ("images/showroom/INTERIEURS_ATELIER_CUB_V2.webp", "Espace conseil et nuanciers du magasin de Mérignac"),
        "intro": [
            "Implanté avenue de la Grande Semaine à <strong>Mérignac</strong>, L'Atelier CUB est notre magasin de la métropole bordelaise. C'est ici que nous stockons nos gammes <span class=\"brand-45\">L'Atelier <span class=\"brand-45-fig\">45</span></span> et <span class=\"brand-titane\">TITANE hydro</span> avant de les livrer sur vos chantiers : un vrai circuit court, sans intermédiaire entre nos formules et votre chantier.",
            "Notre équipe y accompagne artisans, entreprises de peinture, maîtres d'œuvre et particuliers : choix du produit selon le support, lecture des FDES pour vos dossiers RE2020, mise à la teinte et préparation des commandes de chantier.",
        ],
        "services": [
            ("🎨", "Peintures pro bas carbone", "Nos gammes L'Atelier 45 et TITANE hydro en stock, avec leur empreinte carbone déclarée par FDES."),
            ("🧪", "Mise à la teinte", "Plus de 80 000 teintes : Chromatic, Polycrom, Colorimix, RAL, NCS, préparées sur place."),
            ("📐", "Bureau d'études", "Préconisations techniques, choix des systèmes et dossiers produits pour vos appels d'offres."),
            ("🚚", "Livraison chantier", "Livraison de vos commandes sur chantier en Gironde, par des transporteurs locaux."),
            ("🧱", "Murs & sols", "Papiers peints, revêtements muraux, parquets et sols LVT : catalogues et échantillons."),
            ("💼", "Compte pro", "Conditions négociées, paiement différé et suivi commercial dédié."),
        ],
        "zone": ["Mérignac", "Bordeaux", "Pessac", "Le Haillan", "Eysines", "Saint-Médard-en-Jalles", "Bruges", "Talence", "Martignas-sur-Jalle", "Saint-Jean-d'Illac"],
    },
    {
        "cle": "bassin", "fichier": "magasin-peinture-la-teste-de-buch.html",
        "nom": "L'Atelier Bassin", "court": "Bassin", "ville": "La Teste-de-Buch", "cp": "33260",
        "rue": "1111 avenue du Parc des Expositions", "tel": "05 57 52 64 77", "tel_int": "+33557526477",
        "zone_nom": "le Bassin d'Arcachon",
        "titre": "Magasin de peinture à La Teste-de-Buch — L'Atelier Bassin d'Arcachon",
        "description": "Magasin de peinture sur le Bassin d'Arcachon, à La Teste-de-Buch : peintures pro bas carbone, peintures marines, showroom déco, mise à la teinte. Ouvert du lundi au samedi matin.",
        "h1": "L'Atelier <em>Bassin</em>, votre magasin de peinture sur le Bassin d'Arcachon.",
        "chapo": "À La Teste-de-Buch, notre magasin du Bassin d'Arcachon réunit peintures pro bas carbone, peintures marines, showroom décoration et atelier de mise à la teinte, pour les professionnels comme pour les particuliers.",
        "horaires": {0: SEMAINE, 1: SEMAINE, 2: SEMAINE, 3: SEMAINE, 4: SEMAINE, 5: [("09:00", "12:00")]},
        "photo_web": "images/opt/magasin-la-teste-1100.webp", "photo": ("images/magasin-la-teste.webp", "Façade du magasin L'Atelier Bassin à La Teste-de-Buch"),
        "photo2": ("images/showroom/INTERIEUR_ATELIER_BASSIN_V2.webp", "Showroom décoration du magasin de La Teste-de-Buch"),
        "intro": [
            "Avenue du Parc des Expositions à <strong>La Teste-de-Buch</strong>, L'Atelier Bassin est notre magasin du Bassin d'Arcachon. Peintures du bâtiment, peintures marines, outillage, revêtements de sols et de murs : tout est réuni pour vos chantiers comme pour vos projets de décoration.",
            "Notre showroom et notre atelier de colorimétrie vous aident à choisir la bonne teinte, échantillons en main. Nos gammes <span class=\"brand-45\">L'Atelier <span class=\"brand-45-fig\">45</span></span> et <span class=\"brand-titane\">TITANE hydro</span>, bas carbone et fabriquées en France, sont disponibles en magasin.",
        ],
        "services": [
            ("🎨", "Peintures pro bas carbone", "Nos gammes L'Atelier 45 et TITANE hydro, avec leur empreinte carbone déclarée par FDES."),
            ("⛵", "Peintures marines", "Peintures et produits pour le nautisme, adaptés à l'environnement du Bassin."),
            ("🧪", "Atelier colorimétrie", "Plus de 80 000 teintes : Chromatic, Polycrom, Colorimix, RAL, NCS, préparées sur place."),
            ("🛋️", "Showroom déco", "Papiers peints, revêtements muraux et espace Argile pour vos projets de décoration."),
            ("🚚", "Livraison chantier", "Livraison de vos commandes sur chantier en Gironde, par des transporteurs locaux."),
            ("🧰", "Outillage", "Le matériel d'application et de préparation pour les pros et les particuliers."),
        ],
        "zone": ["La Teste-de-Buch", "Arcachon", "Gujan-Mestras", "Le Teich", "Biganos", "Audenge", "Lanton", "Andernos-les-Bains", "Arès", "Lège-Cap-Ferret"],
    },
]

CSS = """
.st { max-width: 1200px; margin: 0 auto; padding: 70px 48px 110px; }
.st-top { display: grid; grid-template-columns: 1.15fr .85fr; gap: 28px; align-items: stretch; }
.st-photo { border-radius: 24px; overflow: hidden; background: var(--bleu-pale); min-height: 320px; }
.st-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.st-card { background: var(--bleu); color: #fff; border-radius: 24px; padding: 30px 30px 28px; display: flex; flex-direction: column; gap: 16px; }
.st-status { display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 700; letter-spacing: .4px; padding: 6px 14px; border-radius: 40px; background: rgba(255,255,255,.1); width: max-content; }
.st-status::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: var(--orange-clair); }
.st-status.is-open::before { background: #fff; box-shadow: 0 0 0 3px rgba(255,255,255,.25); }
.st-line { display: flex; gap: 12px; font-size: 15px; line-height: 1.5; }
.st-line b { color: var(--orange-clair); font-weight: 600; min-width: 22px; }
.st-line a { color: #fff; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,.3); }
.st-line a:hover { color: var(--orange-clair); }
.st-hours { width: 100%; border-collapse: collapse; font-size: 14px; }
.st-hours td { padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,.1); }
.st-hours td:last-child { text-align: right; color: rgba(255,255,255,.85); }
.st-hours tr.is-today td { color: var(--orange-clair); font-weight: 700; }
.st-btns { display: flex; flex-wrap: wrap; gap: 10px; margin-top: auto; }
.st-btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 50px; font-size: 14px; font-weight: 600; text-decoration: none; transition: transform .3s var(--transition); }
.st-btn:hover { transform: translateY(-2px); }
.st-btn.pri { background: var(--orange); color: #fff; }
.st-btn.sec { background: rgba(255,255,255,.1); color: #fff; border: 1px solid rgba(255,255,255,.35); }
.st-rating { margin: 28px 0 0; display: flex; align-items: center; justify-content: space-between; gap: 18px; flex-wrap: wrap; background: var(--bleu-pale); border-radius: 18px; padding: 18px 24px; }
.st-rating-l { display: flex; align-items: center; gap: 14px; }
.st-rating-n { font-family: var(--display); font-size: 40px; font-weight: 500; color: var(--bleu); line-height: 1; }
.st-rating-n small { font-size: 18px; color: var(--gris); }
.st-rating-s { color: var(--orange); letter-spacing: 2px; font-size: 16px; }
.st-rating-c { font-size: 13px; color: var(--gris); }
.st-rating a { font-size: 14px; font-weight: 600; color: var(--bleu); text-decoration: none; border-bottom: 2px solid var(--orange); padding-bottom: 2px; }
.st-sec { margin-top: 80px; }
.st-eye { font-size: 12px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--orange); }
.st-h2 { font-family: var(--display); font-weight: 400; font-size: clamp(28px, 3.2vw, 42px); line-height: 1.12; color: var(--bleu); letter-spacing: -.5px; margin: 10px 0 18px; }
.st-h2 em { font-style: italic; color: var(--orange); }
.st-two { display: grid; grid-template-columns: 1fr 1fr; gap: 44px; align-items: center; }
.st-two p { font-size: 16px; line-height: 1.75; color: var(--gris); margin-bottom: 14px; }
.st-two p strong { color: var(--bleu); }
.st-link { display: inline-block; font-size: 15px; font-weight: 600; color: var(--bleu); text-decoration: none; border-bottom: 2px solid var(--orange); padding-bottom: 2px; }
.st-link:hover { color: var(--orange); }
.st-two img { width: 100%; height: auto; border-radius: 22px; display: block; }
.st-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 10px; }
.st-serv { background: #fff; border: 1px solid rgba(31,58,95,.1); border-radius: 18px; padding: 22px 22px 20px; }
.st-serv i { font-style: normal; font-size: 24px; display: block; margin-bottom: 10px; }
.st-serv b { display: block; font-size: 16px; color: var(--bleu); margin-bottom: 6px; }
.st-serv span { font-size: 14px; line-height: 1.55; color: var(--gris); }
.st-revs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.st-rev { background: #fff; border: 1px solid rgba(31,58,95,.1); border-radius: 18px; padding: 20px 22px; display: flex; flex-direction: column; gap: 10px; }
.st-rev-s { color: var(--orange); letter-spacing: 1.5px; font-size: 14px; }
.st-rev p { font-size: 14.5px; line-height: 1.6; color: var(--bleu-fonce); }
.st-rev cite { font-style: normal; font-size: 13px; font-weight: 600; color: var(--gris); margin-top: auto; }
.st-src { font-size: 12.5px; color: var(--gris); margin-top: 12px; }
.st-zone { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.st-zone span { font-size: 13.5px; color: var(--bleu); background: var(--bleu-pale); border-radius: 40px; padding: 7px 14px; }
.st-faq details { border-bottom: 1px solid rgba(31,58,95,.12); padding: 16px 0; }
.st-faq summary { cursor: pointer; font-size: 17px; font-weight: 600; color: var(--bleu); list-style: none; display: flex; justify-content: space-between; gap: 20px; }
.st-faq summary::-webkit-details-marker { display: none; }
.st-faq summary::after { content: '+'; color: var(--orange); font-size: 22px; line-height: 1; }
.st-faq details[open] summary::after { content: '−'; }
.st-faq p { margin-top: 10px; font-size: 15px; line-height: 1.7; color: var(--gris); }
.st-other { margin-top: 80px; display: flex; justify-content: space-between; align-items: center; gap: 24px; flex-wrap: wrap; background: var(--bleu); color: #fff; border-radius: 24px; padding: 30px 34px; }
.st-other b { font-family: var(--display); font-weight: 400; font-size: 26px; }
.st-other b em { color: var(--orange-clair); font-style: italic; }
.st-other p { font-size: 14px; color: rgba(255,255,255,.75); margin-top: 4px; }
@media (max-width: 960px) {
  .st-top, .st-two { grid-template-columns: 1fr; }
  .st-grid, .st-revs { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .st { padding: 44px 20px 80px; }
  .st-grid, .st-revs { grid-template-columns: 1fr; }
  .st-card { padding: 24px 20px; }
  .st-sec, .st-other { margin-top: 56px; }
  .st-photo { min-height: 220px; }
}
"""

JS = """<script>
/* Horaires : met en évidence le jour en cours et affiche « Ouvert / Fermé » (heure de Paris) */
(function () {
  var t = document.querySelector('.st-hours'); if (!t) return;
  var h = JSON.parse(t.getAttribute('data-h'));
  var now = new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Paris' }));
  var d = (now.getDay() + 6) % 7, m = now.getHours() * 60 + now.getMinutes();
  var row = t.querySelectorAll('tr')[d]; if (row) row.classList.add('is-today');
  var s = document.querySelector('.st-status'); if (!s) return;
  var open = (h[d] || []).some(function (p) {
    var a = p[0].split(':'), b = p[1].split(':');
    return m >= +a[0] * 60 + +a[1] && m < +b[0] * 60 + +b[1];
  });
  s.textContent = open ? 'Ouvert en ce moment' : 'Fermé en ce moment';
  s.classList.toggle('is-open', open);
})();
</script>"""


def dims(p):
    from PIL import Image
    w, h = Image.open(gen.RACINE + p).size
    return f'width="{w}" height="{h}"'


def fr_h(p):
    return p.replace(":00", "h").replace(":", "h")


def page(m, autre):
    a = AV["magasins"][m["cle"]]
    lat, lng = a["geo"]
    itin = "https://www.google.com/maps/dir/?api=1&destination=" + (m["rue"] + ", " + m["cp"] + " " + m["ville"]).replace(" ", "+").replace(",", "%2C").replace("'", "%27")
    rows, hjs = "", []
    for i, j in enumerate(JOURS):
        plages = m["horaires"].get(i, [])
        hjs.append([[p[0], p[1]] for p in plages])
        txt = " · ".join(fr_h(p[0]) + "–" + fr_h(p[1]) for p in plages) or "Fermé"
        rows += f"<tr><td>{j}</td><td>{txt}</td></tr>"
    serv = "".join(f'<div class="st-serv"><i aria-hidden="true">{ic}</i><b>{t}</b><span>{d}</span></div>' for ic, t, d in m["services"])
    revs = [r for r in AV["avis"] if r["m"] == m["cle"]][:3]
    revh = "".join(f'<blockquote class="st-rev"><div class="st-rev-s" aria-label="{r["note"]} sur 5">{"★" * r["note"]}</div><p>« {E(r["texte"])} »</p><cite>{E(r["auteur"])} · avis Google</cite></blockquote>' for r in revs)
    zone = "".join(f"<span>{z}</span>" for z in m["zone"])
    samedi = "le samedi de 9h à 12h" if 5 in m["horaires"] else "fermé le samedi"
    faq = [
        (f"Quels sont les horaires du magasin {m['nom']} ?",
         f"Le magasin est ouvert du lundi au vendredi de 8h à 12h et de 14h à 18h, {samedi}, et fermé le dimanche."),
        ("Puis-je faire faire ma teinte sur place ?",
         "Oui. Nous préparons votre teinte en magasin parmi plus de 80 000 références (Chromatic, Polycrom, Colorimix, RAL, NCS)."),
        ("Livrez-vous sur les chantiers ?",
         "Oui, nous livrons vos commandes sur chantier en Gironde, avec des transporteurs locaux. Demandez votre livraison à l'équipe du magasin ou depuis l'espace pro."),
        ("Le magasin est-il ouvert aux particuliers ?",
         "Oui. Nous accueillons les professionnels comme les particuliers, et notre équipe vous conseille quel que soit votre projet."),
        ("Où trouver les FDES de vos peintures bas carbone ?",
         "Toutes les FDES et fiches techniques sont téléchargeables dans nos documents techniques, et notre équipe peut vous les transmettre pour vos dossiers RE2020."),
    ]
    faqh = "".join(f"<details><summary>{q}</summary><p>{r}</p></details>" for q, r in faq)
    contenu = f"""<main class="st">
<div class="st-top">
<div class="st-photo"><img src="{m['photo_web']}" alt="{E(m['photo'][1])}" {dims(m['photo_web'])} fetchpriority="high" decoding="async"/></div>
<div class="st-card">
<span class="st-status">Horaires d'ouverture</span>
<div class="st-line"><b>📍</b><span>{m['rue']}<br/>{m['cp']} {m['ville']}</span></div>
<div class="st-line"><b>📞</b><a href="tel:{m['tel_int']}">{m['tel']}</a></div>
<div class="st-line"><b>✉️</b><a href="mailto:contact@latelier33.fr">contact@latelier33.fr</a></div>
<table class="st-hours" data-h='{json.dumps(hjs)}'><tbody>{rows}</tbody></table>
<div class="st-btns"><a class="st-btn pri" href="{itin}" rel="noopener" target="_blank">Itinéraire →</a><a class="st-btn sec" href="tel:{m['tel_int']}">Appeler</a><a class="st-btn sec" href="espace-pro.html#devis">Demander un devis</a></div>
</div>
</div>
<div class="st-rating"><div class="st-rating-l"><div class="st-rating-n">{a['note']}<small>/5</small></div><div><div class="st-rating-s" aria-hidden="true">★★★★★</div><div class="st-rating-c">{a['nb']} avis clients sur Google</div></div></div><a href="{a['maps_avis']}" rel="noopener" target="_blank">Lire nos avis Google →</a></div>

<section class="st-sec st-two">
<div><div class="st-eye">— Le magasin</div><h2 class="st-h2">Peintures, conseils et <em>circuit court</em> à {m['ville']}.</h2>{''.join('<p>' + p + '</p>' for p in m['intro'])}
<p><a class="st-link" href="peinture-bas-carbone.html">Notre engagement bas carbone et circuit court →</a></p></div>
<img src="{m['photo2'][0]}" alt="{E(m['photo2'][1])}" {dims(m['photo2'][0])} loading="lazy" decoding="async"/>
</section>

<section class="st-sec"><div class="st-eye">— Sur place</div><h2 class="st-h2">Ce que vous trouvez <em>dans ce magasin</em>.</h2><div class="st-grid">{serv}</div></section>

<section class="st-sec"><div class="st-eye">— Avis clients</div><h2 class="st-h2">Ils parlent de <em>{m['nom']}</em>.</h2><div class="st-revs">{revh}</div>
<p class="st-src">Extraits d'avis publiés sur la fiche Google du magasin. Note moyenne {a['note']}/5 sur {a['nb']} avis.</p></section>

<section class="st-sec"><div class="st-eye">— Zone desservie</div><h2 class="st-h2">Au service de <em>{m['zone_nom']}</em>.</h2>
<p class="st-src" style="font-size:15px;color:var(--gris);margin:0 0 14px">Le magasin dessert notamment :</p><div class="st-zone">{zone}</div></section>

<section class="st-sec st-faq"><div class="st-eye">— Questions fréquentes</div><h2 class="st-h2">Bon à savoir <em>avant de venir</em>.</h2>{faqh}</section>

<div class="st-other"><div><b>Notre autre magasin : <em>{autre['nom']}</em></b><p>{autre['rue']}, {autre['cp']} {autre['ville']} · {autre['tel']}</p></div><a class="st-btn pri" href="{autre['fichier']}">Voir le magasin de {autre['ville']} →</a></div>
</main>
{JS}"""

    oh = []
    for i, plages in m["horaires"].items():
        for p in plages:
            oh.append({"@type": "OpeningHoursSpecification", "dayOfWeek": JOURS_EN[i], "opens": p[0], "closes": p[1]})
    ld = [
        {"@context": "https://schema.org", "@type": "PaintStore", "@id": gen.SITE + m["fichier"] + "#magasin",
         "name": m["nom"] + " — " + m["ville"], "url": gen.SITE + m["fichier"],
         "image": [gen.SITE + m["photo"][0], gen.SITE + m["photo2"][0]], "telephone": m["tel_int"], "email": "contact@latelier33.fr",
         "priceRange": "€€", "hasMap": a["maps_avis"],
         "address": {"@type": "PostalAddress", "streetAddress": m["rue"], "addressLocality": m["ville"], "postalCode": m["cp"], "addressRegion": "Nouvelle-Aquitaine", "addressCountry": "FR"},
         "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
         "openingHoursSpecification": oh,
         "areaServed": [{"@type": "City", "name": z} for z in m["zone"]],
         "parentOrganization": {"@type": "Organization", "name": "L'Atelier — Marchand de couleurs", "url": gen.SITE}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]},
    ]
    p = gen.page(m["fichier"], m["titre"], m["description"], m["h1"], "Magasin de peinture · " + m["ville"], m["chapo"],
                 [("Nos magasins", "index.html#magasins"), (m["nom"], None)], contenu, CSS, ld, og_image=m["photo"][0])
    gen.ecrire(m["fichier"], p)


def main():
    page(MAGASINS[0], MAGASINS[1]); page(MAGASINS[1], MAGASINS[0])
    # Sitemap
    sm = gen.RACINE + "sitemap.xml"; t = open(sm, encoding="utf-8").read(); d = datetime.date.today().isoformat()
    for m in MAGASINS:
        loc = gen.SITE + m["fichier"]
        if loc not in t:
            t = t.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{d}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>")
    open(sm, "w", encoding="utf-8").write(t)
    print("pages magasins + sitemap OK")


if __name__ == "__main__":
    main()
