"""
Publication des articles « Conseils » du site.

Chaque article = une entrée dans _outils/articles.json + son texte dans _outils/articles/<slug>.html
Lancer :  python _outils/publier.py
Le script (re)génère :
  - conseil-<slug>.html pour chaque article
  - conseils.html (liste des articles, le plus récent en premier)
  - sitemap.xml (ajoute les articles manquants)
  - js/recherche.js (entrées « Conseils » du moteur de recherche)
"""
import json, os, re, html, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen

O = gen.RACINE + "_outils" + os.sep
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

def date_fr(d):
    y, m, j = map(int, d.split("-"))
    return f"{j} {MOIS[m-1]} {y}"

CSS = r"""
.art { max-width: 820px; margin: 0 auto; padding: 50px 48px 100px; }
.art-meta { display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: 13px; color: var(--orange-clair); margin-top: 6px; font-weight: 500; }
.art-cover { margin: 44px auto 0; max-width: 820px; padding: 0 48px; position: relative; z-index: 2; }
.art-cover-in { background: linear-gradient(135deg, #EAF4ED, #F5F0E8); border-radius: 24px; height: 260px; display: flex; align-items: flex-end; justify-content: center; gap: 22px; padding: 26px 20px 0; overflow: hidden; box-shadow: 0 24px 50px -30px rgba(31,58,95,.45); }
.art-cover-in img { height: 220px; width: auto; object-fit: contain; filter: drop-shadow(0 14px 18px rgba(31,58,95,.25)); }
.art h2 { font-family: var(--display); font-weight: 400; font-size: clamp(26px, 3vw, 34px); line-height: 1.2; color: var(--bleu); margin: 52px 0 16px; letter-spacing: -.4px; }
.art h2 em { font-style: italic; color: var(--vert-eco); }
.art h3 { font-size: 18px; color: var(--bleu); margin: 30px 0 10px; }
.art p, .art li { font-size: 16.5px; line-height: 1.8; color: var(--gris-fonce); }
.art p { margin-bottom: 18px; }
.art ul, .art ol { padding-left: 22px; margin: 0 0 20px; }
.art li { margin-bottom: 8px; }
.art a { color: var(--bleu); text-decoration: underline; text-decoration-color: rgba(31,58,95,.3); text-underline-offset: 3px; }
.art a:hover { color: var(--orange); }
.art a.blog-card { text-decoration: none; color: inherit; }
.art .blog-card p { font-size: 14.5px; line-height: 1.6; color: var(--gris); margin: 0; }
.art .blog-card h3 { margin: 0; font-family: var(--display); font-weight: 400; font-size: 22px; }
.art strong { color: var(--bleu-fonce); }
.art .chapo { font-size: 19px; line-height: 1.7; color: var(--bleu); font-weight: 400; }
.art-callout { background: #EAF4ED; border-left: 4px solid var(--vert-eco); border-radius: 0 16px 16px 0; padding: 20px 24px; margin: 28px 0; }
.art-callout p { margin: 0; font-size: 15.5px; }
.art-table-wrap { overflow-x: auto; margin: 24px 0 28px; border-radius: 16px; border: 1px solid rgba(31,58,95,.1); }
.art table { width: 100%; border-collapse: collapse; font-size: 14.5px; min-width: 520px; }
.art th { background: var(--bleu); color: #fff; text-align: left; font-weight: 600; padding: 12px 14px; }
.art td { padding: 11px 14px; border-top: 1px solid rgba(31,58,95,.08); color: var(--gris-fonce); }
.art tr:nth-child(even) td { background: var(--gris-clair); }
.art .num { font-variant-numeric: tabular-nums; font-weight: 600; color: #2F6940; white-space: nowrap; }
.art-cta { margin: 56px 0 0; background: var(--bleu); color: #fff; border-radius: 24px; padding: 34px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px; }
.art-cta p { color: #fff; margin: 0; font-size: 17px; max-width: 460px; }
.art-cta p strong { color: #fff; }
.art-cta a { background: var(--orange); color: #fff !important; text-decoration: none !important; padding: 14px 24px; border-radius: 50px; font-weight: 600; white-space: nowrap; }
.art-cta a:hover { background: var(--orange-fonce); }
.art-more { margin-top: 56px; }
.art-more h2 { margin-top: 0; }
.art-sources { font-size: 13.5px !important; color: var(--gris) !important; margin-top: 40px; }

.blog { max-width: 1200px; margin: 0 auto; padding: 80px 48px 110px; }
.blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.blog-card { display: flex; flex-direction: column; text-decoration: none; color: inherit; background: var(--blanc); border: 1px solid rgba(31,58,95,.1); border-radius: 22px; overflow: hidden; transition: transform .3s var(--transition), box-shadow .3s; }
.blog-card:hover { transform: translateY(-4px); box-shadow: 0 24px 50px -28px rgba(31,58,95,.45); }
.blog-card-img { background: linear-gradient(135deg, #EAF4ED, #F5F0E8); height: 190px; display: flex; align-items: flex-end; justify-content: center; padding-top: 18px; }
.blog-card-img img { height: 165px; width: auto; object-fit: contain; filter: drop-shadow(0 10px 14px rgba(31,58,95,.22)); }
.blog-card-body { padding: 22px 24px 26px; display: flex; flex-direction: column; gap: 10px; flex: 1; }
.blog-card-tag { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--vert-eco); font-weight: 700; }
.blog-card h2, .blog-card h3 { font-family: var(--display); font-weight: 400; font-size: 22px; line-height: 1.25; color: var(--bleu); }
.blog-card p { font-size: 14.5px; line-height: 1.6; color: var(--gris); }
.blog-card-date { margin-top: auto; font-size: 12.5px; color: var(--gris); opacity: .8; }
.art-more .blog-grid { grid-template-columns: repeat(2, 1fr); }
@media (max-width: 1000px) { .blog-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 760px) {
  .art { padding: 50px 20px 80px; }
  .art-cover { padding: 0 20px; }
  .art-cover-in { height: 190px; gap: 10px; }
  .art-cover-in img { height: 160px; }
  .art p, .art li { font-size: 16px; }
  .art-cta { padding: 26px 22px; }
  .art-cta a { white-space: normal; text-align: center; width: 100%; }
  .blog { padding: 56px 20px 80px; }
  .blog-grid, .art-more .blog-grid { grid-template-columns: 1fr; }
}
"""

def dim(p):
    from PIL import Image
    return Image.open(gen.RACINE + p).size

def carte(a, h="h2"):
    return (f'<a class="blog-card" href="conseil-{a["slug"]}.html">'
            f'<div class="blog-card-img"><img src="{a["images"][0]}" alt="" width="{dim(a["images"][0])[0]}" height="{dim(a["images"][0])[1]}" loading="lazy" decoding="async"/></div>'
            f'<div class="blog-card-body"><span class="blog-card-tag">{a["tag"]}</span>'
            f'<{h}>{a["titre_court"]}</{h}><p>{a["description"]}</p>'
            f'<span class="blog-card-date">{date_fr(a["date"])} · {a["lecture"]} min de lecture</span></div></a>')

def main():
    arts = json.load(open(O + "articles.json", encoding="utf-8"))
    arts.sort(key=lambda a: a["date"], reverse=True)

    for a in arts:
        corps = open(O + "articles" + os.sep + a["slug"] + ".html", encoding="utf-8").read()
        autres = [b for b in arts if b["slug"] != a["slug"]][:2]
        plus = ""
        if autres:
            plus = '<section class="art-more"><h2>À lire <em>aussi</em></h2><div class="blog-grid">' + "".join(carte(b, "h3") for b in autres) + "</div></section>"
        cover = '<div class="art-cover"><div class="art-cover-in">' + "".join(f'<img src="{i}" alt="" width="{dim(i)[0]}" height="{dim(i)[1]}"/>' for i in a["images"][:3]) + "</div></div>"
        fichier = f'conseil-{a["slug"]}.html'
        contenu = cover + '<main class="art"><article>' + corps + "</article>" + plus + "</main>"
        ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre_court"], "description": a["description"],
               "datePublished": a["date"], "dateModified": a.get("maj", a["date"]), "inLanguage": "fr-FR",
               "image": gen.SITE + a["images"][0], "mainEntityOfPage": gen.SITE + fichier,
               "author": {"@type": "Organization", "name": "L'Atelier — Marchand de couleurs", "url": gen.SITE},
               "publisher": {"@type": "Organization", "name": "L'Atelier", "logo": {"@type": "ImageObject", "url": gen.SITE + "images/logo.png"}}}]
        meta = f'<div class="art-meta"><span>{date_fr(a["date"])}</span><span>{a["lecture"]} min de lecture</span><span>Par l\'équipe L\'Atelier</span></div>\n'
        p = gen.page(fichier, a["titre"], a["description"], a["h1"], a["tag"], a["chapo"],
                     [("Conseils", "conseils.html"), (a["titre_court"], None)], contenu, CSS, ld,
                     og_image=a["images"][0], og_type="article", hero_extra=meta)
        gen.ecrire(fichier, p)

    # Page liste
    contenu = '<main class="blog"><div class="blog-grid">' + "".join(carte(a) for a in arts) + "</div></main>"
    ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Conseils peinture bas carbone — L'Atelier", "url": gen.SITE + "conseils.html",
           "blogPost": [{"@type": "BlogPosting", "headline": a["titre_court"], "url": gen.SITE + f'conseil-{a["slug"]}.html', "datePublished": a["date"]} for a in arts]}]
    p = gen.page("conseils.html", "Conseils peinture bas carbone, RE2020 et FDES | L'Atelier",
                 "Guides pratiques pour les pros de la peinture : choisir une peinture bas carbone, lire une FDES, réussir ses chantiers RE2020. Par L'Atelier, Gironde.",
                 "Nos <em>conseils</em>.", "Guides pratiques", "Peinture bas carbone, FDES, RE2020, mise en œuvre : les réponses de notre équipe aux questions de nos clients professionnels.",
                 [("Conseils", None)], contenu, CSS, ld)
    gen.ecrire("conseils.html", p)

    # Sitemap
    sm = gen.RACINE + "sitemap.xml"; t = open(sm, encoding="utf-8").read()
    for u, d, pr in [("conseils.html", arts[0]["date"], "0.7")] + [(f'conseil-{a["slug"]}.html', a.get("maj", a["date"]), "0.6") for a in arts]:
        loc = gen.SITE + u
        if loc in t:
            t = re.sub(r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[^<]*", r"\g<1>" + d, t)
        else:
            t = t.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{d}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>\n\n</urlset>")
    open(sm, "w", encoding="utf-8").write(t)

    # Moteur de recherche
    js = gen.RACINE + "js" + os.sep + "recherche.js"; t = open(js, encoding="utf-8").read()
    q = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
    lignes = ['    { t: "Conseils", d: "Guides peinture bas carbone, FDES et RE2020", u: "conseils.html", k: "blog article guide conseil actualité", g: "Pages" },']
    lignes += [f'    {{ t: "{q(a["titre_court"])}", d: "{q(a["description"][:90])}", u: "conseil-{a["slug"]}.html", k: "{q(a["mots_cles"])}", g: "Conseils" }},' for a in arts]
    bloc = "    // ---- CONSEILS (généré par _outils/publier.py) ----\n" + "\n".join(lignes) + "\n    // ---- FIN CONSEILS ----\n"
    if "// ---- CONSEILS (généré" in t:
        t = re.sub(r"    // ---- CONSEILS \(généré.*?// ---- FIN CONSEILS ----\n", lambda m: bloc, t, flags=re.S)
    else:
        t = t.replace("  const INDEX = [\n", "  const INDEX = [\n" + bloc, 1)
    open(js, "w", encoding="utf-8").write(t)
    print("Articles publiés :", ", ".join(a["slug"] for a in arts))

if __name__ == "__main__":
    main()
