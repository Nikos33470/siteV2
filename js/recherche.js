
(function() {
  // ============ INDEX DE RECHERCHE COMPLET DU SITE ============
  // Chaque entrée : { t: titre, d: description, u: URL, k: mots-clés cachés, g: groupe }
  const INDEX = [
    // ---- CONSEILS (généré par _outils/publier.py) ----
    { t: "Conseils", d: "Guides peinture bas carbone, FDES et RE2020", u: "conseils.html", k: "blog article guide conseil actualité", g: "Pages" },
    { t: "Peinture biosourcée : que veulent vraiment dire les pourcentages ?", d: "Résine biosourcée, matières naturelles, norme ASTM D6866, label Karibati : comment lire le", u: "conseil-peinture-biosourcee.html", k: "biosourcé biosourcée résine végétale algues astm d6866 karibati renouvelable naturel titane mv algo pro dragocryl", g: "Conseils" },
    { t: "Peinture et RE2020 : comment choisir une peinture bas carbone", d: "RE2020 et peinture : pourquoi la FDES compte, comment comparer l'empreinte carbone des pei", u: "conseil-peinture-bas-carbone-re2020.html", k: "re2020 bas carbone fdes peinture choisir impression finition bureau etudes acv inies", g: "Conseils" },
    { t: "Comment lire la FDES d'une peinture : les chiffres qui comptent", d: "Unité fonctionnelle, durée de vie, indicateur changement climatique, type de FDES : le gui", u: "conseil-lire-fdes-peinture.html", k: "fdes lire comprendre unite fonctionnelle duree vie changement climatique a1 c4 verifiee provisoire collective inies", g: "Conseils" },
    // ---- FIN CONSEILS ----
    // ---- PAGES PRINCIPALES ----
    { t: "Espace pro — demande de devis", d: "Devis, échantillons, FDES, ouverture de compte pro", u: "espace-pro.html#devis", k: "devis pro compte professionnel echantillon contact formulaire tarif prix livraison chantier", g: "Pages" },
    { t: "Accueil", d: "Marchand de couleurs en Gironde — fabricant de peintures", u: "index.html", k: "accueil home homepage", g: "Pages" },
    { t: "Nos gammes de peinture", d: "L'Atelier 45 et Titane Hydro — toutes nos peintures fabriquées en France", u: "gammes.html", k: "peinture gamme catalogue", g: "Pages" },
    { t: "Nuanciers", d: "Téléchargez tous les nuanciers PDF — Chromatic, RAL, NCS, Polycrom, KEIM, bois", u: "nuanciers.html", k: "couleur teinte palette pdf", g: "Pages" },
    { t: "Revêtements muraux", d: "Papiers peints haut de gamme et revêtements professionnels", u: "revetement-mural.html", k: "papier peint mur tapisserie", g: "Pages" },
    { t: "Revêtements de sol", d: "Parquets bois, sols souples, LVT et vinyles", u: "revetement-sol.html", k: "sol parquet lvt vinyle moquette", g: "Pages" },
    { t: "Documents techniques", d: "Fiches techniques (FT), FDES, nuanciers et plaquettes en téléchargement", u: "documents.html", k: "ft fdes fiche document pdf téléchargement", g: "Pages" },

    // ---- GAMME L'ATELIER 45 ----
    { t: "L'Atelier 45 Impress Évo", d: "Impression universelle phase aqueuse — la base de tous les chantiers", u: "gammes.html#p-impress-evo", k: "impression primaire sous-couche fond aqueuse 45", g: "Peintures · L'Atelier 45" },
    { t: "L'Atelier 45 Impress Grands Travaux", d: "Impression haut rendement pour gros chantiers", u: "gammes.html#p-grands-travaux", k: "impression grands travaux chantier rendement", g: "Peintures · L'Atelier 45" },
    { t: "L'Atelier 45 Mat 2 en 1", d: "Peinture mate intérieure — impression + finition en une seule peinture", u: "gammes.html#p-mat-45", k: "mat mate 2en1 intérieur finition", g: "Peintures · L'Atelier 45" },
    { t: "L'Atelier 45 Velours", d: "Finition velours pour murs et plafonds — lessivable", u: "gammes.html#p-velours-45", k: "velours satinée lessivable mur plafond", g: "Peintures · L'Atelier 45" },
    { t: "L'Atelier 45 Satin Acryl", d: "Peinture satinée acrylique haute résistance", u: "gammes.html#p-satin-45", k: "satin satinée acryl acrylique brillant", g: "Peintures · L'Atelier 45" },
    { t: "L'Atelier 45 Glycéro Satin", d: "Peinture glycéro satinée — boiseries, métal, supports difficiles", u: "gammes.html#p-glycero-45", k: "glycéro glycero solvant satin boiserie métal", g: "Peintures · L'Atelier 45" },

    // ---- GAMME TITANE HYDRO ----
    { t: "Titane Hydro Prim", d: "Impression biosourcée phase aqueuse — primaire d'accrochage", u: "gammes.html#p-titane-prim", k: "titane prim impression primaire biosourcé hydro", g: "Peintures · Titane Hydro" },
    { t: "Titane Hydro Mat", d: "Peinture mate biosourcée — finition haut de gamme", u: "gammes.html#p-titane-mat", k: "titane mat mate biosourcé hydro", g: "Peintures · Titane Hydro" },
    { t: "Titane Hydro Mat Velouté (MV)", d: "Finition mat velouté — fini contemporain et chic", u: "gammes.html#p-titane-mv", k: "titane mat velouté mv biosourcé", g: "Peintures · Titane Hydro" },
    { t: "Titane Hydro Velours", d: "Finition velours biosourcée — lessivable et résistante", u: "gammes.html#p-titane-velours", k: "titane velours biosourcé lessivable", g: "Peintures · Titane Hydro" },

    // ---- PARTENAIRES (Dragopaint) ----
    { t: "Dragocryl Mat Airless Bas Carbone", d: "Peinture mate airless bas carbone — sous-couche ou finition", u: "gammes.html#p-dragocryl-mat-airless", k: "dragopaint dragocryl mat airless bas carbone partenaire mécanisée aqueuse", g: "Peintures · Partenaires" },
    { t: "Dragocryl MS Soyeux Bas Carbone", d: "Finition mat velouté soyeuse — 69% renouvelable dont 39% biosourcé", u: "gammes.html#p-dragocryl-ms-soyeux", k: "dragopaint dragocryl ms soyeux bas carbone velouté renouvelable biosourcé partenaire", g: "Peintures · Partenaires" },
    { t: "COMUS IZI R Prim", d: "Impression recyclée 60% — homogénéise le support", u: "gammes.html#p-comus-izi-prim", k: "comus izi r prim impression recyclée 60 partenaire éco aqueuse", g: "Peintures · Partenaires" },
    { t: "COMUS IZI R Mat", d: "Finition mate recyclée 56% — lessivable, HQE bas carbone", u: "gammes.html#p-comus-izi-mat", k: "comus izi r mat mate recyclée 56 lessivable hqe bas carbone partenaire", g: "Peintures · Partenaires" },
    { t: "COMUS IZI R Velours", d: "Finition velours recyclée 56% — lessivable classe 1, HQE", u: "gammes.html#p-comus-izi-velours", k: "comus izi r velours recyclée 56 lessivable hqe bas carbone partenaire", g: "Peintures · Partenaires" },
    { t: "Algo Pro Primaire", d: "Impression biosourcée aux algues — microporeuse, certifiée Karibati", u: "gammes.html#p-algo-primaire", k: "algo pro primaire impression biosourcée algues karibati partenaire", g: "Peintures · Partenaires" },
    { t: "Algo Pro Mat", d: "Finition mate 80% biosourcée aux algues — lessivable classe 1", u: "gammes.html#p-algo-mat", k: "algo pro mat mate biosourcée 80 algues lessivable partenaire", g: "Peintures · Partenaires" },
    { t: "Algo Pro Velours", d: "Finition velours 80% biosourcée aux algues — lessivable classe 1", u: "gammes.html#p-algo-velours", k: "algo pro velours biosourcée 80 algues lessivable partenaire", g: "Peintures · Partenaires" },
    { t: "Sofec Multimat Plus", d: "Peinture mate lavable intérieur et extérieur — bas carbone 0,234 kg CO₂/UF", u: "gammes.html#p-sofec-multimat-plus", k: "sofec multimat plus + mate mat lavable intérieur extérieur bas carbone partenaire", g: "Peintures · Partenaires" },
    { t: "Sofec Multimat Velouté Soyeux", d: "Peinture garnissante mat velouté soyeux — bas carbone 0,245 kg CO₂/UF", u: "gammes.html#p-sofec-multimat-veloute-soyeux", k: "sofec multimat velouté soyeux garnissante mat lavable intérieur bas carbone partenaire", g: "Peintures · Partenaires" },

    // ---- NUANCIERS ----
    { t: "Chromatic CH1 — Jonone", d: "Édition signature artistique — palette d'expression", u: "nuanciers.html#nuanciers-cartes", k: "chromatic ch1 jonone artiste signature pdf", g: "Nuanciers" },
    { t: "Chromatic Dorval CH2", d: "Teintes contemporaines et nuances apaisées — nouvelle édition", u: "nuanciers.html#nuanciers-cartes", k: "chromatic ch2 dorval contemporain nouveau pdf", g: "Nuanciers" },
    { t: "Chromatic Inspirations · Styles", d: "Ambiances et harmonies clés-en-main par style décoratif", u: "nuanciers.html#nuanciers-cartes", k: "chromatic inspirations styles ambiance harmonie pdf", g: "Nuanciers" },
    { t: "Polycrom 1320 teintes", d: "Le système Polycrom complet — version PDF", u: "nuanciers.html#nuanciers-cartes", k: "polycrom 1320 mise à la teinte machine pdf", g: "Nuanciers" },
    { t: "Chromatic Façade", d: "250 teintes pour les enduits et peintures de façade", u: "nuanciers.html#nuanciers-cartes", k: "chromatic façade extérieur enduit 250 pdf", g: "Nuanciers" },
    { t: "Polycrom Façade 170T", d: "Nuancier façade — 170 teintes spécifiques extérieur", u: "nuanciers.html#nuanciers-cartes", k: "polycrom façade extérieur 170 pdf", g: "Nuanciers" },
    { t: "KEIM Lasure Béton (Concretal)", d: "Lasures minérales pour béton — palette KEIM", u: "nuanciers.html#nuanciers-cartes", k: "keim lasure béton concretal minéral pdf", g: "Nuanciers" },
    { t: "KEIM Palette Exclusiv", d: "Palette Spektrum — peintures silicates KEIM", u: "nuanciers.html#nuanciers-cartes", k: "keim spektrum exclusiv silicate minéral pdf", g: "Nuanciers" },
    { t: "Nuancier RAL Classic 190 teintes", d: "Le standard industriel RAL — 190 teintes", u: "nuanciers.html#nuanciers-cartes", k: "ral classic industriel standard 190 pdf", g: "Nuanciers" },
    { t: "Nuancier NCS", d: "Natural Color System — système chromatique scientifique", u: "nuanciers.html#nuanciers-cartes", k: "ncs natural color system suède pdf", g: "Nuanciers" },
    { t: "Chromatic Bois CH10", d: "Nuancier teintes bois — nouvelle édition", u: "nuanciers.html#nuanciers-cartes", k: "chromatic bois ch10 lasure teinte pdf", g: "Nuanciers" },
    { t: "Nuancier Bois Chromatic (ancien)", d: "Édition antérieure du nuancier bois", u: "nuanciers.html#nuanciers-cartes", k: "chromatic bois ancien lasure pdf", g: "Nuanciers" },

    // ---- PAPIERS PEINTS / MURAUX ----
    { t: "Papiers peints haut de gamme", d: "Panoramiques, motifs, unis texturés — éditeurs français et internationaux", u: "revetement-mural.html#papiers-peints", k: "papier peint panoramique motif éditeur décoration", g: "Revêtements muraux" },
    { t: "Revêtements muraux professionnels", d: "Vinyles techniques contract — hôtellerie, tertiaire, CHR", u: "revetement-mural.html#revetements-pros", k: "vinyle pro contract hôtellerie tertiaire chr feu m1", g: "Revêtements muraux" },
    { t: "Isidore Leroy", d: "Maison parisienne de papier peint depuis 1842 — panoramiques", u: "revetement-mural.html#papiers-peints", k: "isidore leroy paris 1842 panoramique", g: "Marques · Papiers peints" },
    { t: "Élitis", d: "Éditeur toulousain — papiers peints et textiles muraux", u: "revetement-mural.html#papiers-peints", k: "elitis élitis toulouse textile mural", g: "Marques · Papiers peints" },
    { t: "Casamance", d: "Maison parisienne — papiers peints et tissus", u: "revetement-mural.html#papiers-peints", k: "casamance paris tissu", g: "Marques · Papiers peints" },
    { t: "Pierre Frey", d: "Maison Pierre Frey — papiers peints et tissus depuis 1935", u: "revetement-mural.html#papiers-peints", k: "pierre frey paris 1935 tissu", g: "Marques · Papiers peints" },
    { t: "Nobilis", d: "Maison parisienne — depuis 1928", u: "revetement-mural.html#papiers-peints", k: "nobilis paris 1928", g: "Marques · Papiers peints" },
    { t: "Bien Fait Paris", d: "Éditeur design contemporain — Paris", u: "revetement-mural.html#papiers-peints", k: "bien fait paris design", g: "Marques · Papiers peints" },
    { t: "Atelier d'Offard", d: "Tours — papiers peints artisanaux à la planche", u: "revetement-mural.html#papiers-peints", k: "offard tours artisanat planche", g: "Marques · Papiers peints" },
    { t: "Little Cabari", d: "Bordeaux — éditeur indépendant", u: "revetement-mural.html#papiers-peints", k: "little cabari bordeaux", g: "Marques · Papiers peints" },
    { t: "Ananbô", d: "Panoramiques peints à la main — France", u: "revetement-mural.html#papiers-peints", k: "ananbo panoramique france", g: "Marques · Papiers peints" },
    { t: "Le Grand Siècle", d: "Éditeur français — papiers peints", u: "revetement-mural.html#papiers-peints", k: "grand siècle france", g: "Marques · Papiers peints" },
    { t: "Papiers de Paris", d: "Éditeur parisien", u: "revetement-mural.html#papiers-peints", k: "papiers de paris", g: "Marques · Papiers peints" },
    { t: "Lé Papiers de Ninon", d: "Éditeur français", u: "revetement-mural.html#papiers-peints", k: "ninon le papiers", g: "Marques · Papiers peints" },
    { t: "Muraem", d: "Papiers peints sur mesure", u: "revetement-mural.html#papiers-peints", k: "muraem sur mesure", g: "Marques · Papiers peints" },
    { t: "Wall&decò France", d: "Éditeur italien design", u: "revetement-mural.html#papiers-peints", k: "wall deco italie design", g: "Marques · Papiers peints" },
    { t: "Au fil des Couleurs", d: "Maison parisienne — papiers peints", u: "revetement-mural.html#papiers-peints", k: "au fil des couleurs paris", g: "Marques · Papiers peints" },
    { t: "Texdecor", d: "Tourcoing — éditeur", u: "revetement-mural.html#papiers-peints", k: "texdecor tourcoing", g: "Marques · Papiers peints" },
    { t: "Vescom", d: "Pays-Bas — revêtements muraux textiles et vinyles contract hospitality", u: "revetement-mural.html#revetements-pros", k: "vescom pays-bas hospitality contract textile", g: "Marques · Contract" },
    { t: "Muraspec", d: "UK — PVC technique contract", u: "revetement-mural.html#revetements-pros", k: "muraspec uk pvc technique", g: "Marques · Contract" },
    { t: "Lutèce", d: "Semi-pro et résidentiel — papiers peints", u: "revetement-mural.html#revetements-pros", k: "lutèce semi-pro résidentiel", g: "Marques · Contract" },
    { t: "Texdecor Contract", d: "Vinacoustic et Polyform — revêtements contract", u: "revetement-mural.html#revetements-pros", k: "texdecor vinacoustic polyform contract", g: "Marques · Contract" },

    // ---- REVÊTEMENTS DE SOL ----
    { t: "Parquets bois", d: "Massif, contrecollé, stratifié — chêne français et essences nobles", u: "revetement-sol.html#parquet", k: "parquet bois chêne massif contrecollé stratifié", g: "Revêtements de sol" },
    { t: "Sols souples & LVT", d: "Vinyle, LVT, contract pour pièces humides et passage intense", u: "revetement-sol.html#sols-souples", k: "lvt vinyle sol souple contract hôtellerie", g: "Revêtements de sol" },
    { t: "Panaget", d: "Fabricant de parquets français depuis 1929 — Bretagne", u: "revetement-sol.html#parquet", k: "panaget france 1929 parquet bretagne", g: "Marques · Parquet" },
    { t: "Design Parquet", d: "Fabricant français spécialiste du chêne", u: "revetement-sol.html#parquet", k: "design parquet france chêne", g: "Marques · Parquet" },
    { t: "Parqueterie Berrichonne", d: "Parqueterie française — Berry", u: "revetement-sol.html#parquet", k: "parqueterie berrichonne berry france", g: "Marques · Parquet" },
    { t: "Haro", d: "Allemagne — parqueterie depuis 1866", u: "revetement-sol.html#parquet", k: "haro allemagne 1866 parquet", g: "Marques · Parquet" },
    { t: "Bauwerk", d: "Suisse — parquetterie haut de gamme", u: "revetement-sol.html#parquet", k: "bauwerk suisse parquet", g: "Marques · Parquet" },
    { t: "Kährs", d: "Suède depuis 1857 — contrecollé scandinave", u: "revetement-sol.html#parquet", k: "kahrs kährs suède 1857 scandinave", g: "Marques · Parquet" },
    { t: "Boen", d: "Norvège — parquets contrecollés", u: "revetement-sol.html#parquet", k: "boen norvège", g: "Marques · Parquet" },
    { t: "BerryAlloc", d: "Belgique-Norvège — sols", u: "revetement-sol.html#parquet", k: "berryalloc belgique norvège", g: "Marques · Parquet" },
    { t: "Gerflor", d: "Lyon — LVT Creation et sols souples", u: "revetement-sol.html#sols-souples", k: "gerflor lyon lvt creation", g: "Marques · LVT" },
    { t: "Tarkett", d: "iD Inspiration — sols vinyle LVT", u: "revetement-sol.html#sols-souples", k: "tarkett id inspiration lvt", g: "Marques · LVT" },
    { t: "Forbo", d: "Suisse — Allura LVT", u: "revetement-sol.html#sols-souples", k: "forbo suisse allura lvt", g: "Marques · LVT" },
    { t: "Amtico", d: "UK — LVT luxe", u: "revetement-sol.html#sols-souples", k: "amtico uk luxe lvt", g: "Marques · LVT" },
    { t: "Moduleo", d: "Pays-Bas — sols vinyle", u: "revetement-sol.html#sols-souples", k: "moduleo pays-bas vinyle", g: "Marques · LVT" },
    { t: "Interface", d: "USA — dalles moquette contract", u: "revetement-sol.html#sols-souples", k: "interface usa dalle moquette", g: "Marques · LVT" },
    { t: "Polyflor", d: "UK — sols contract", u: "revetement-sol.html#sols-souples", k: "polyflor uk contract", g: "Marques · LVT" },
    { t: "IVC", d: "Belgique — sols souples", u: "revetement-sol.html#sols-souples", k: "ivc belgique", g: "Marques · LVT" },

    // ---- DOCUMENTS ----
    { t: "Fiches techniques (FT)", d: "Toutes les fiches techniques de nos peintures L'Atelier 45 et Titane Hydro", u: "documents.html#section-ft", k: "ft fiche technique caractéristique application", g: "Documents" },
    { t: "FDES", d: "Fiches de Déclaration Environnementale et Sanitaire", u: "documents.html#section-fdes", k: "fdes environnement sanitaire ACV", g: "Documents" },
    { t: "Nuanciers PDF (téléchargement)", d: "Tous les nuanciers en téléchargement direct", u: "documents.html#section-nuancier", k: "nuancier pdf téléchargement", g: "Documents" },
    { t: "Plaquettes", d: "Plaquettes commerciales et catalogues", u: "documents.html#section-plaquette", k: "plaquette catalogue commercial", g: "Documents" },

    // ---- SECTIONS INDEX ----
    { t: "Peinture bas carbone — comparatif", d: "Empreinte CO₂ de 20 peintures d'après leur FDES", u: "peinture-bas-carbone.html", k: "bio biosourcé écologique éco environnement carbone fdes", g: "À propos" },
    { t: "Nos marques distribuées", d: "Théolaur, Dragopaint, Sigma, Soframap, Sofec, Comus, KEIM…", u: "index.html#marques", k: "marque théolaur dragopaint sigma soframap sofec comus keim distribué", g: "À propos" },
    { t: "Avis Google", d: "4,85/5 — 137 avis sur 2 magasins", u: "index.html#avis", k: "avis google note témoignage client", g: "À propos" },
    { t: "Services aux professionnels", d: "Mise à la teinte, conseil technique, livraison chantier, compte pro", u: "index.html#services", k: "service pro teinte conseil livraison compte", g: "À propos" },
    { t: "Colorimétrie & nuanciers en magasin", d: "Plus de 80 000 teintes — Polycrom, Colorimix, RAL, NCS", u: "index.html#nuanciers", k: "colorimétrie teinte mise machine polycrom colorimix", g: "À propos" },

    // ---- MAGASINS ----
    { t: "L'Atelier CUB — Mérignac", d: "7 av. de la grande semaine, 33700 Mérignac · 05 56 28 89 44", u: "index.html#magasins", k: "magasin merignac mérignac cub bordeaux 33700 adresse", g: "Magasins" },
    { t: "L'Atelier Bassin — La Teste-de-Buch", d: "1111 av. du Parc des Expositions, 33260 La Teste-de-Buch · 05 57 52 64 77", u: "index.html#magasins", k: "magasin teste bassin arcachon 33260 la-teste adresse", g: "Magasins" },

    // ---- CONTACT ----
    { t: "Contact", d: "contact@latelier33.fr — formulaire, devis, demande d'info", u: "index.html#magasins", k: "contact email mail téléphone devis", g: "Contact" },
  ];

  // ============ NORMALISATION (accents, casse) ============
  function normalize(s) {
    return s.toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9 ]/g, ' ');
  }

  // Pré-calcul des champs normalisés pour chaque entrée
  const NORM = INDEX.map(it => ({
    item: it,
    blob: normalize(it.t + ' ' + it.d + ' ' + (it.k || '') + ' ' + it.g),
    title: normalize(it.t)
  }));

  // ============ RECHERCHE avec score ============
  function search(query, limit) {
    const q = normalize(query).trim();
    if (!q) return [];
    const words = q.split(/\s+/).filter(Boolean);
    const results = [];

    for (const entry of NORM) {
      let score = 0;
      let allMatch = true;
      for (const w of words) {
        if (entry.title.includes(w)) {
          // Bonus si le mot est dans le titre
          score += entry.title.startsWith(w) ? 10 : 6;
        } else if (entry.blob.includes(w)) {
          score += 2;
        } else {
          allMatch = false;
          break;
        }
      }
      if (allMatch && score > 0) {
        results.push({ item: entry.item, score });
      }
    }
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit || 10).map(r => r.item);
  }

  // ============ MISE EN VALEUR (highlight) ============
  function highlight(text, query) {
    if (!query) return text;
    const words = normalize(query).split(/\s+/).filter(Boolean);
    if (!words.length) return text;
    // Escape HTML
    let safe = text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    // Pour chaque mot, on cherche dans la version normalisée et on souligne dans l'original
    // Approche simple : on souligne mot à mot avec un regex insensible aux accents
    for (const w of words) {
      if (!w) continue;
      // Construit un pattern qui matche le mot en ignorant les accents
      const pattern = w.split('').map(c => {
        const map = { 'a':'[aàâä]', 'e':'[eéèêë]', 'i':'[iîï]', 'o':'[oôö]', 'u':'[uùûü]', 'c':'[cç]', 'n':'[nñ]' };
        return map[c] || c;
      }).join('');
      try {
        const re = new RegExp('(' + pattern + ')', 'gi');
        safe = safe.replace(re, '<strong style="color:var(--orange);background:rgba(240,127,44,0.1)">$1</strong>');
      } catch(e) { /* ignore */ }
    }
    return safe;
  }

  // ============ AFFICHAGE DU DROPDOWN ============
  function renderResults(container, query) {
    const results = search(query, 10);
    if (!results.length) {
      container.innerHTML = '<div class="search-empty">Aucun résultat pour <strong>' + query.replace(/</g,'&lt;') + '</strong><br><span style="font-size:12px;opacity:0.7">Essayez : peinture, nuancier, parquet, mérignac, biosourcé…</span></div>';
      container.classList.add('is-open');
      return;
    }
    // Regroupement par catégorie (g)
    const groups = {};
    results.forEach(r => { (groups[r.g] = groups[r.g] || []).push(r); });
    let html = '';
    Object.keys(groups).forEach(g => {
      html += '<div class="search-results-group">' + g + '</div>';
      groups[g].forEach(r => {
        html += '<a href="' + (document.body.getAttribute('data-base') || '') + r.u + '" class="search-result">';
        html += '<div class="search-result-title">' + highlight(r.t, query) + '</div>';
        html += '<div class="search-result-desc">' + highlight(r.d, query) + '</div>';
        html += '</a>';
      });
    });
    html += '<div class="search-hint"><kbd>↑</kbd><kbd>↓</kbd> naviguer · <kbd>Entrée</kbd> ouvrir · <kbd>Esc</kbd> fermer</div>';
    container.innerHTML = html;
    container.classList.add('is-open');
  }

  // ============ INITIALISATION sur chaque formulaire de recherche ============
  function initSearch(form) {
    const input = form.querySelector('.nav-search-input');
    if (!input) return;

    // Création du conteneur de résultats
    const results = document.createElement('div');
    results.className = 'search-results';
    results.setAttribute('role', 'listbox');
    results.setAttribute('aria-label', 'Résultats de recherche');
    form.appendChild(results);

    // S'assurer que le form est positionné en relatif pour le dropdown absolu
    if (getComputedStyle(form).position === 'static') {
      form.style.position = 'relative';
    }

    let activeIndex = -1;

    function getItems() {
      return Array.from(results.querySelectorAll('.search-result'));
    }
    function updateActive() {
      getItems().forEach((el, i) => {
        el.classList.toggle('is-active', i === activeIndex);
        if (i === activeIndex) el.scrollIntoView({ block: 'nearest' });
      });
    }
    function close() {
      results.classList.remove('is-open');
      activeIndex = -1;
    }
    function doSearch() {
      const q = input.value.trim();
      activeIndex = -1;
      if (!q) { close(); return; }
      renderResults(results, q);
    }

    input.addEventListener('input', doSearch);
    input.addEventListener('focus', () => { if (input.value.trim()) doSearch(); });

    // Empêche la soumission par défaut et redirige vers le 1er résultat
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const items = getItems();
      if (items.length) {
        const idx = activeIndex >= 0 ? activeIndex : 0;
        window.location.href = items[idx].getAttribute('href');
      }
    });

    // Navigation clavier
    input.addEventListener('keydown', (e) => {
      const items = getItems();
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!items.length) return;
        activeIndex = (activeIndex + 1) % items.length;
        updateActive();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (!items.length) return;
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        updateActive();
      } else if (e.key === 'Escape') {
        close();
        input.blur();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (items.length) {
          const idx = activeIndex >= 0 ? activeIndex : 0;
          window.location.href = items[idx].getAttribute('href');
        }
      }
    });

    // Fermeture au clic extérieur
    document.addEventListener('click', (e) => {
      if (!form.contains(e.target)) close();
    });
  }

  // Lancer sur tous les formulaires .nav-search de la page
  function init() {
    document.querySelectorAll('form.nav-search, .nav-search').forEach(initSearch);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
