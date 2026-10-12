// La lettre chiffrée du roi Joseph — scripts communs : thème, langue, sommaire flottant (repris du site Wenmi).
(function () {
  'use strict';

  // ---------- thème clair / sombre ----------
  var root = document.documentElement;
  try { var saved = localStorage.getItem('jn-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.theme-toggle');
    if (!b) return;
    var dark = root.getAttribute('data-theme') === 'dark' ||
      (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('jn-theme', next); } catch (e) {}
  });

  // ---------- langue choisie : mémorisée pour la page d'accueil racine ----------
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('.lang-switch a[data-lang]');
    if (a) { try { localStorage.setItem('jn-lang', a.dataset.lang); } catch (e) {} }
  });

  // ---------- menu des langues : fermeture au clic extérieur ou par Échap ----------
  var langMenu = document.querySelector('.lang-switch details');
  if (langMenu) {
    document.addEventListener('click', function (ev) { if (langMenu.open && !langMenu.contains(ev.target)) langMenu.open = false; });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && langMenu.open) { langMenu.open = false; langMenu.querySelector('summary').focus(); }
    });
  }

  // ---------- hauteur réelle de l'en-tête : le sommaire flottant se cale dessous ----------
  var head = document.querySelector('.site-header');
  function headH() { if (head) root.style.setProperty('--head-h', head.offsetHeight + 'px'); }
  headH(); window.addEventListener('resize', headH);

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function mountFloatingToc() {
    var main = document.querySelector('main');
    if (!main || document.querySelector('.hero')) return;           // pas sur l'accueil
    var heads = Array.prototype.slice.call(main.querySelectorAll('h2'));
    if (heads.length < 3) return;
    var T = { fr: 'Sommaire', en: 'Contents' };
    var title = T[root.lang] || T.fr, n = 0;
    var items = heads.map(function (h) {
      var target = h.id ? h : (h.parentElement && h.parentElement.id && h.parentElement.tagName === 'SECTION' ? h.parentElement : h);
      if (!target.id) target.id = 'sec-' + (++n);
      var label = h.cloneNode(true); label.querySelectorAll('small, sup, .star').forEach(function (x) { x.remove(); });
      var txt = label.textContent.replace(/\s+/g, ' ').trim(), small = h.querySelector('small');
      return { id: target.id, el: h, txt: txt, sub: small ? small.textContent.trim() : '' };
    });
    var wrap = document.createElement('div'); wrap.className = 'ftoc';
    var h = '<button class="ftoc-btn" type="button" aria-expanded="false" aria-controls="ftoc-panel">☰ ' + esc(title) + '</button>' +
      '<nav class="ftoc-panel" id="ftoc-panel" aria-label="' + esc(title) + '"><p class="ftoc-title">' + esc(title) + '</p><ul>';
    items.forEach(function (it) {
      h += '<li><a href="#' + it.id + '" data-id="' + it.id + '">' + esc(it.txt) + (it.sub ? ' <small>' + esc(it.sub) + '</small>' : '') + '</a></li>';
    });
    wrap.innerHTML = h + '</ul></nav>';
    document.body.appendChild(wrap);
    var btn = wrap.querySelector('.ftoc-btn'), links = wrap.querySelectorAll('a');
    function setOpen(o) { wrap.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); }
    btn.addEventListener('click', function () { setOpen(!wrap.classList.contains('open')); });
    wrap.addEventListener('click', function (ev) { if (ev.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') setOpen(false); });
    document.addEventListener('click', function (ev) { if (!wrap.contains(ev.target)) setOpen(false); });
    // section en cours
    var current = null;
    function spy() {
      var y = window.scrollY + 120, cur = items[0];
      items.forEach(function (it) { if (it.el.getBoundingClientRect().top + window.scrollY <= y) cur = it; });
      if (cur !== current) {
        current = cur;
        links.forEach(function (a) { a.classList.toggle('on', a.dataset.id === cur.id); });
        var on = wrap.querySelector('a.on'), panel = wrap.querySelector('.ftoc-panel');
        if (on && panel.scrollHeight > panel.clientHeight) {
          var top = on.offsetTop - panel.clientHeight / 2;
          panel.scrollTop = Math.max(0, top);
        }
      }
    }
    window.addEventListener('scroll', spy, { passive: true }); spy();
    // les figures larges passent sous la colonne : on l'efface le temps qu'elles sont à l'écran
    var wide = Array.prototype.slice.call(document.querySelectorAll('figure.wide'));
    function hideOverWide() {
      var over = wide.some(function (f) { var r = f.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; });
      document.body.classList.toggle('ftoc-hide', over);
    }
    if (wide.length) { window.addEventListener('scroll', hideOverWide, { passive: true }); window.addEventListener('resize', hideOverWide); hideOverWide(); }
    // la colonne s'arrête au-dessus du pied de page : elle raccourcit, puis s'efface s'il ne reste plus de place
    var foot = document.querySelector('.site-footer'), panel = wrap.querySelector('.ftoc-panel');
    document.body.classList.add('has-ftoc');
    function fitFoot() {
      panel.style.maxHeight = '';
      var column = window.getComputedStyle(btn).display === 'none';
      if (!foot || !column) { document.body.classList.remove('ftoc-foot'); return; }
      var room = foot.getBoundingClientRect().top - panel.getBoundingClientRect().top - 24;
      if (room < panel.getBoundingClientRect().height) panel.style.maxHeight = Math.max(room, 0) + 'px';
      document.body.classList.toggle('ftoc-foot', room < 72);
    }
    window.addEventListener('scroll', fitFoot, { passive: true }); window.addEventListener('resize', fitFoot); fitFoot();
  }
  mountFloatingToc();
})();
