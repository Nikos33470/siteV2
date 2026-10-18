/* =====================================================================
   L'Atelier — script commun à toutes les pages
   Barre d'actions fixe en bas d'écran sur téléphone
   ===================================================================== */
(function () {
  /* Pas d'outil de mesure d'audience (suivi via Google Search Console).
     Fonction conservée vide : les appels existants (quiz nuanciers, devis) restent sans effet. */
  window.atelierTrack = function () {};

  /* ---------- BARRE MOBILE (≤ 760 px) ---------- */
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
