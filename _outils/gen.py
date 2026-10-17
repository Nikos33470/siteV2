"""
Générateur de pages simples (Espace pro, Conseils, articles) à partir de la page
mentions-legales.html : on réutilise son en-tête, son menu, son pied de page et ses styles
pour que toutes les pages restent identiques au reste du site.

Le dossier _outils/ n'est pas publié par GitHub Pages (les dossiers commençant par « _ » sont ignorés).
"""
import json, re, html, os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
SITE = "https://www.latelier33.fr/"


def _modele():
    return open(RACINE + "mentions-legales.html", encoding="utf-8").read()


def page(fichier, titre, description, h1, eyebrow, sous_titre, fil, contenu,
         css="", ld=(), og_image="images/logo.png", og_type="website", hero_extra=""):
    """Construit une page complète et renvoie le HTML.
    fil : liste [(nom, url ou None)] du fil d'Ariane après « Accueil »."""
    t = _modele()
    url = SITE + fichier
    e = lambda s: html.escape(s, quote=True)

    t = re.sub(r"<title>.*?</title>", "<title>" + html.escape(titre, quote=False) + "</title>", t, 1, re.S)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', '<meta content="' + e(description) + '" name="description"/>', t, 1)
    t = t.replace('<meta name="robots" content="noindex, follow"/>', '<meta name="robots" content="index, follow, max-image-preview:large"/>', 1)
    t = t.replace(SITE + "mentions-legales.html", url)
    t = re.sub(r'<meta property="og:type" content="[^"]*"/>', '<meta property="og:type" content="' + og_type + '"/>', t, 1)
    t = re.sub(r'<meta property="og:title" content="[^"]*"/>', '<meta property="og:title" content="' + e(titre) + '"/>', t, 1)
    t = re.sub(r'<meta name="twitter:title" content="[^"]*"/>', '<meta name="twitter:title" content="' + e(titre) + '"/>', t, 1)
    t = re.sub(r'<meta property="og:description" content="[^"]*"/>', '<meta property="og:description" content="' + e(description) + '"/>', t, 1)
    t = re.sub(r'<meta name="twitter:description" content="[^"]*"/>', '<meta name="twitter:description" content="' + e(description) + '"/>', t, 1)
    t = t.replace(SITE + "images/logo.png\"/>\n<meta property=\"og:locale\"", SITE + og_image + "\"/>\n<meta property=\"og:locale\"", 1)
    t = re.sub(r'<meta name="twitter:image" content="[^"]*"/>', '<meta name="twitter:image" content="' + SITE + og_image + '"/>', t, 1)

    # Fil d'Ariane (données structurées + visuel)
    items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE}]
    for i, (nom, u) in enumerate(fil, 2):
        items.append({"@type": "ListItem", "position": i, "name": nom, "item": SITE + (u or fichier)})
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    t = re.sub(r'<!-- Fil d\'ariane Schema.org -->\s*<script type="application/ld\+json">.*?</script>',
               "<!-- Fil d'ariane Schema.org -->\n" + '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + "</script>"
               + "".join('\n<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>" for d in ld),
               t, 1, flags=re.S)
    vis = '<a href="index.html">Accueil</a>'
    for nom, u in fil:
        vis += '\n<span class="breadcrumb-sep">/</span>\n'
        vis += ('<a href="' + u + '">' + nom + '</a>') if u and u != fichier else ('<span class="breadcrumb-current">' + nom + '</span>')
    t = re.sub(r'(<nav aria-label="Fil d\'Ariane" class="breadcrumb">).*?(</nav>)', lambda m: m.group(1) + "\n" + vis + "\n" + m.group(2), t, 1, re.S)

    # Bandeau titre
    hero = ('<section class="legal-hero">\n<div class="legal-hero-inner">\n'
            '<span class="legal-eyebrow">' + eyebrow + '</span>\n'
            '<h1 class="legal-title">' + h1 + '</h1>\n'
            '<p class="legal-subtitle">' + sous_titre + '</p>\n' + hero_extra + '</div>\n</section>')
    t = re.sub(r'<section class="legal-hero">.*?</section>', lambda m: hero, t, 1, re.S)

    # Contenu
    t = re.sub(r'<main class="legal-content">.*?</main>', lambda m: contenu, t, 1, re.S)
    if css:
        t = t.replace("</head>", "<style>\n" + css + "\n</style>\n</head>", 1)
    return t


def ecrire(fichier, html_page):
    open(RACINE + fichier, "w", encoding="utf-8").write(html_page)
