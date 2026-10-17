/* =====================================================================
   L'Atelier — script commun à toutes les pages
   1) Mesure d'audience Matomo (sans cookie, exemptée de consentement CNIL)
   2) Suivi des actions utiles : appels, e-mails, itinéraires, PDF, devis
   3) Barre d'actions fixe en bas d'écran sur téléphone
   ===================================================================== */
(function () {
  /* ---------- 1) MATOMO ----------
     Compte Matomo Cloud « latelier33 » → https://latelier33.matomo.cloud/
     Si l'adresse du compte change : modifier MATOMO_URL et MATOMO_JS
     (et la ligne Content-Security-Policy en tête de chaque page). */
  var MATOMO_URL = 'https://latelier33.matomo.cloud/';
  var MATOMO_JS = 'https://cdn.matomo.cloud/latelier33.matomo.cloud/matomo.js';
  var MATOMO_SITE = '1';

  var _paq = window._paq = window._paq || [];
  var enLigne = /(^|\.)latelier33\.fr$/.test(location.hostname); // pas de mesure en local
  if (enLigne) {
    _paq.push(['disableCookies']);            // aucun cookie déposé
    _paq.push(['setDownloadExtensions', 'pdf']);
    _paq.push(['trackPageView']);
    _paq.push(['enableLinkTracking']);         // compte les téléchargements PDF et liens sortants
    _paq.push(['setTrackerUrl', MATOMO_URL + 'matomo.php']);
    _paq.push(['setSiteId', MATOMO_SITE]);
    var g = document.createElement('script');
    g.async = true; g.src = MATOMO_JS;
    document.head.appendChild(g);
  }

  /* Fonction partagée : atelierTrack('Catégorie', 'Action', 'Nom') */
  window.atelierTrack = function (cat, act, name) {
    _paq.push(['trackEvent', cat, act, name || '']);
  };

  /* ---------- 2) ÉVÉNEMENTS ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('tel:') === 0) {
      atelierTrack('Contact', 'Appel', h.indexOf('0557') > -1 ? 'Bassin' : 'Mérignac');
    } else if (h.indexOf('mailto:') === 0) {
      atelierTrack('Contact', 'E-mail', location.pathname);
    } else if (h.indexOf('google.com/maps') > -1) {
      atelierTrack('Contact', 'Itinéraire', h.indexOf('Teste') > -1 ? 'Bassin' : 'Mérignac');
    } else if (a.classList.contains('search-result')) {
      var inp = document.querySelector('.nav-search-input');
      if (inp && inp.value.trim()) _paq.push(['trackSiteSearch', inp.value.trim(), false, false]);
    }
  }, true);

  /* ---------- 3) BARRE MOBILE (≤ 760 px) ---------- */
  function barre() {
    if (document.querySelector('.mbar')) return;
    var css = document.createElement('style');
    css.textContent =
      '.mbar{display:none}' +
      '@media (max-width:760px){' +
      '.mbar{display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:6px;position:fixed;left:0;right:0;bottom:0;z-index:990;' +
      'padding:8px 8px calc(8px + env(safe-area-inset-bottom));background:rgba(255,255,255,.97);' +
      'box-shadow:0 -6px 24px rgba(31,58,95,.14);border-top:1px solid rgba(31,58,95,.08)}' +
      '.mbar a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;min-height:46px;border-radius:12px;' +
      'font:600 12.5px/1.15 Inter,system-ui,sans-serif;text-decoration:none;color:#1F3A5F;background:#E8EEF5;text-align:center}' +
      '.mbar a small{font-weight:400;font-size:10.5px;opacity:.75}' +
      '.mbar a.mbar-devis{background:#F07F2C;color:#fff}' +
      'body{padding-bottom:70px}' +
      '.google-floating{bottom:78px!important}' +
      'body.menu-open .mbar{display:none}' +
      '}';
    document.head.appendChild(css);
    var b = document.createElement('nav');
    b.className = 'mbar'; b.setAttribute('aria-label', 'Contact rapide');
    var base = document.body.getAttribute('data-base') || '';
    b.innerHTML =
      '<a href="tel:0556288944">📞 Appeler<small>Mérignac</small></a>' +
      '<a href="tel:0557526477">📞 Appeler<small>Bassin</small></a>' +
      '<a class="mbar-devis" href="' + base + 'espace-pro.html#devis">Demander<small>un devis</small></a>';
    document.body.appendChild(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', barre); else barre();
})();
