// Shared behaviour for every page (loaded with defer). The per-page scripts own the menu toggle,
// reveal animation and forms; this file adds the accessibility layer around them.
(function () {
  'use strict';
  var body = document.body;

  // 1. While the mobile drawer is open, everything behind it is inert; the Services parent reports its state.
  var main = document.querySelector('main'), footer = document.querySelector('footer'), bar = document.querySelector('.mobile-bar');
  var servicesItem = document.querySelector('.nav-item'), servicesLink = servicesItem && servicesItem.querySelector(':scope > a');
  function syncNavState() {
    var open = body.classList.contains('nav-open');
    [main, footer, bar].forEach(function (el) { if (el) { if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert'); } });
    if (servicesLink) servicesLink.setAttribute('aria-expanded', servicesItem.classList.contains('open') ? 'true' : 'false');
  }
  new MutationObserver(syncNavState).observe(body, { attributes: true, attributeFilter: ['class'] });
  if (servicesItem) new MutationObserver(syncNavState).observe(servicesItem, { attributes: true, attributeFilter: ['class'] });

  // 2. Gallery tiles are keyboard-operable (Enter / Space triggers the tile's click handler).
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var t = e.target;
    if (t && t.matches && t.matches('.hero-gallery-item, .port-item')) { e.preventDefault(); t.click(); }
  });

  // 3. Lightbox / modal focus management: move focus to Close on open, return it on close.
  var lastTile = null;
  document.addEventListener('click', function (e) { var tile = e.target.closest && e.target.closest('.hero-gallery-item, .port-item'); if (tile) lastTile = tile; }, true);
  ['modal', 'lightbox'].forEach(function (id) {
    var dlg = document.getElementById(id); if (!dlg) return;
    var closeBtn = dlg.querySelector('button');
    new MutationObserver(function () {
      var open = dlg.classList.contains('open') || dlg.classList.contains('active');
      if (open) { if (closeBtn) closeBtn.focus(); }
      else if (lastTile && document.activeElement !== lastTile) { try { lastTile.focus(); } catch (err) { /* tile may be gone */ } }
    }).observe(dlg, { attributes: true, attributeFilter: ['class'] });
  });

  // 4. Announce the form success message and move focus to it.
  var success = document.getElementById('form-success');
  if (success) new MutationObserver(function () { if (success.style.display === 'block') success.focus(); }).observe(success, { attributes: true, attributeFilter: ['style'] });
})();
