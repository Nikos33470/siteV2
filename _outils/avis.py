"""
Met à jour la section « avis » de l'accueil (notes, nombres d'avis, carrousel, badge flottant)
à partir des avis Google réels de _outils/avis_google.json, et les données locales (PaintStore) de l'accueil.
Lancer :  python3 _outils/avis.py
"""
import json, os, re, html

O = os.path.dirname(os.path.abspath(__file__)) + os.sep
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
AV = json.load(open(O + "avis_google.json", encoding="utf-8"))
M = AV["magasins"]; E = lambda s: html.escape(s, quote=True)
TOTAL = M["cub"]["nb"] + M["bassin"]["nb"]
MOY = round((float(M["cub"]["note"].replace(",", ".")) * M["cub"]["nb"] + float(M["bassin"]["note"].replace(",", ".")) * M["bassin"]["nb"]) / TOTAL, 1)
MOY_FR = str(MOY).replace(".", ",")
LIEU = {"cub": "L'Atelier CUB · Mérignac", "bassin": "L'Atelier Bassin · La Teste"}


def initiales(n):
    p = [x for x in re.split(r"[\s.]+", n) if x]
    return (p[0][0] + (p[1][0] if len(p) > 1 else "")).upper()


def carte(a):
    return ('<div class="avis-card"><div class="avis-card-head">'
            f'<div class="avis-card-avatar">{initiales(a["auteur"])}</div>'
            f'<div class="avis-card-meta"><div class="avis-card-name">{E(a["auteur"])}</div><div class="avis-card-date">Avis Google</div></div></div>'
            f'<div class="avis-card-stars" aria-label="{a["note"]} sur 5">{"★" * a["note"]}</div>'
            f'<p class="avis-card-text">{E(a["texte"])}</p>'
            f'<div class="avis-card-store">{LIEU[a["m"]]}</div></div>')


def main():
    f = R + "index.html"; t = open(f, encoding="utf-8").read()
    # Intro + badge
    t = re.sub(r'(<section class="avis" id="avis">.*?<p class="section-intro">).*?(</p>)',
               lambda m: m.group(1) + f"{TOTAL} avis sur Google, notés {MOY_FR}/5 en moyenne, partagés entre nos deux magasins. Voici ce qu'en disent nos clients pros et particuliers." + m.group(2), t, 1, re.S)
    t = t.replace("      Avis vérifiés Google\n", "      Avis clients Google\n")
    # Cartes de note par magasin
    for cle in ("cub", "bassin"):
        nom = "CUB" if cle == "cub" else "Bassin"
        pat = r'(<div class="avis-store-name">L\'Atelier <em>' + nom + r'</em></div>.*?<div class="avis-store-score">)[^<]*(<small>/5</small></div>.*?<div class="avis-store-count">)[^<]*(</div>)'
        t = re.sub(pat, lambda m: m.group(1) + M[cle]["note"] + m.group(2) + f'<a href="{E(M[cle]["maps_avis"])}" rel="noopener" target="_blank">{M[cle]["nb"]} avis Google</a>' + m.group(3), t, 1, re.S)
    # Carrousel : les avis réels, en double pour la boucle infinie
    a = t.index('<div class="avis-carousel">')
    if '<!-- /avis-carousel -->' in t:
        b = t.index('<!-- /avis-carousel -->') + len('<!-- /avis-carousel -->')
    else:
        # première fois : fin du carrousel = 1er des 4 </div> qui précèdent la fin de la section avis
        b = t.index("</div>\n</div>\n</div>\n</section>", a) + len("</div>")
    cartes = "".join(carte(x) for x in AV["avis"])
    bloc = ('<div class="avis-carousel">\n<!-- Avis Google réels (_outils/avis_google.json) -->\n' + cartes +
            '\n<!-- duplication pour la boucle infinie -->\n' + cartes.replace('<div class="avis-card">', '<div class="avis-card" aria-hidden="true">') +
            '\n</div><!-- /avis-carousel -->')
    t = t[:a] + bloc + t[b:]
    # Badge flottant
    t = re.sub(r'(<span class="google-floating-num">)[^<]*(<span class="google-floating-num-max">)', lambda m: m.group(1) + MOY_FR + m.group(2), t, 1)
    t = re.sub(r'(<div class="google-floating-sub">)[^<]*(</div>)', lambda m: m.group(1) + f"{TOTAL} avis · 2 magasins" + m.group(2), t, 1)
    # Données locales : coordonnées Google exactes et lien vers la page de chaque magasin
    for cle, ident, page in (("cub", "#merignac", "magasin-peinture-merignac.html"), ("bassin", "#la-teste", "magasin-peinture-la-teste-de-buch.html")):
        def fix(m):
            d = json.loads(m.group(1))
            d["url"] = "https://www.latelier33.fr/" + page
            d["geo"] = {"@type": "GeoCoordinates", "latitude": M[cle]["geo"][0], "longitude": M[cle]["geo"][1]}
            d["hasMap"] = M[cle]["maps_avis"]
            return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
        t = re.sub(r'<script type="application/ld\+json">\s*(\{[^<]*?"@id":\s*"https://www.latelier33.fr/' + ident + r'"[^<]*)</script>', fix, t, count=1, flags=re.S)
    open(f, "w", encoding="utf-8").write(t)
    print("accueil : avis et données locales mis à jour —", MOY_FR, "/5,", TOTAL, "avis")


if __name__ == "__main__":
    main()
