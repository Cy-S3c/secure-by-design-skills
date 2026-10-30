/* Threat-model report behaviour — inlined into threat-model.html by build_report.py. No dependencies. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* audience view: exec | tech | all */
  function setView(v) {
    document.body.setAttribute('data-view', v);
    $$('.switch [data-view]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-view') === v)); });
  }
  $$('.switch [data-view]').forEach(function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-view')); }); });
  var pr = $('#print'); if (pr) pr.addEventListener('click', function () { window.print(); });

  /* contents: highlight the section in view */
  var links = $$('.toc a[href^="#"]');
  if ('IntersectionObserver' in window && links.length) {
    var map = new Map();
    links.forEach(function (a) { var el = document.getElementById(a.getAttribute('href').slice(1)); if (el) map.set(el, a); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (a) { a.classList.remove('active'); }); map.get(e.target).classList.add('active'); } });
    }, { rootMargin: '-15% 0px -75% 0px' });
    map.forEach(function (a, el) { io.observe(el); });
  }

  /* threat register: filters, expand/collapse, sort, deep links */
  var reg = $('#reg');
  if (reg) {
    var rows = $$('tbody tr.t', reg), total = rows.length;
    var f = { cat: $('#f-cat'), band: $('#f-band'), status: $('#f-status'), owner: $('#f-owner'), q: $('#f-q') };
    var cell = null;
    var det = function (r) { var n = r.nextElementSibling; return n && n.classList.contains('d') ? n : null; };
    function apply() {
      var n = 0, q = f.q && f.q.value.toLowerCase().trim();
      rows.forEach(function (r) {
        var d = r.dataset, x = det(r);
        var text = (r.textContent + ' ' + (x ? x.textContent : '')).toLowerCase();
        var ok = (!f.cat.value || d.cat === f.cat.value) && (!f.band.value || d.band === f.band.value) &&
          (!f.status.value || d.status === f.status.value) && (!f.owner.value || d.owner === f.owner.value) &&
          (!cell || (d.l === cell.l && d.i === cell.i)) && (!q || text.indexOf(q) > -1);
        r.hidden = !ok; if (x) x.hidden = !ok || d.open !== '1'; if (ok) n++;
      });
      $('#reg-count').textContent = (n === total ? total : n + ' of ' + total) + ' threats';
      var chip = $('#cell-chip');
      if (chip) { chip.hidden = !cell; if (cell) $('#cell-chip-text').textContent = 'Likelihood ' + cell.l + ' × Impact ' + cell.i; }
    }
    function clear() { Object.keys(f).forEach(function (k) { if (f[k]) f[k].value = ''; }); cell = null; }
    function setRow(r, open) {
      r.dataset.open = open ? '1' : '0';
      var x = det(r); if (x) x.hidden = !open || r.hidden;
      var b = $('.rowtoggle', r); if (b) b.setAttribute('aria-expanded', String(open));
    }
    Object.keys(f).forEach(function (k) { var el = f[k]; if (el) el.addEventListener(el.tagName === 'INPUT' ? 'input' : 'change', apply); });
    var fc = $('#f-clear'); if (fc) fc.addEventListener('click', function () { clear(); apply(); });
    var cx = $('#cell-chip-x'); if (cx) cx.addEventListener('click', function () { cell = null; apply(); });
    rows.forEach(function (r) { var b = $('.rowtoggle', r); if (b) b.addEventListener('click', function () { setRow(r, r.dataset.open !== '1'); }); });
    var ex = $('#reg-expand'); if (ex) ex.addEventListener('click', function () { rows.forEach(function (r) { setRow(r, true); }); });
    var co = $('#reg-collapse'); if (co) co.addEventListener('click', function () { rows.forEach(function (r) { setRow(r, false); }); });
    $$('th[data-sort]', reg).forEach(function (th) {
      th.addEventListener('click', function () {
        var key = th.dataset.sort, dir = th.dataset.dir === 'asc' ? 'desc' : 'asc';
        $$('th[data-sort]', reg).forEach(function (x) { x.dataset.dir = ''; x.removeAttribute('aria-sort'); });
        th.dataset.dir = dir; th.setAttribute('aria-sort', dir === 'asc' ? 'ascending' : 'descending');
        var tb = $('tbody', reg), pairs = rows.map(function (r) { return [r, det(r)]; });
        pairs.sort(function (a, b) {
          var x = a[0].dataset[key], y = b[0].dataset[key], nx = parseFloat(x), ny = parseFloat(y);
          var c = (!isNaN(nx) && !isNaN(ny)) ? nx - ny : String(x).localeCompare(String(y), undefined, { numeric: true });
          return dir === 'asc' ? c : -c;
        });
        pairs.forEach(function (p) { tb.appendChild(p[0]); if (p[1]) tb.appendChild(p[1]); });
      });
    });
    $$('.heat td[data-l]').forEach(function (td) {
      td.addEventListener('click', function () { if (td.dataset.n === '0') return; clear(); cell = { l: td.dataset.l, i: td.dataset.i }; apply(); location.hash = '#register'; });
    });
    $$('a[data-q]').forEach(function (a) { a.addEventListener('click', function () { clear(); f.q.value = a.dataset.q; apply(); }); });
    function reveal() {
      var id = decodeURIComponent(location.hash.slice(1)), r = id && document.getElementById('row-' + id);
      if (!r) return;
      clear(); apply(); setRow(r, true); r.scrollIntoView({ block: 'center', behavior: 'instant' });
      r.classList.remove('flash'); void r.offsetWidth; r.classList.add('flash');
    }
    window.addEventListener('hashchange', reveal);
    apply(); reveal();
  }

  /* data flows: cross-boundary filter */
  var fx = $('#flows-cross');
  if (fx) {
    var fr = $$('#flows-table tbody tr');
    var upd = function () { var n = 0; fr.forEach(function (r) { var ok = !fx.checked || r.dataset.cross === '1'; r.hidden = !ok; if (ok) n++; }); $('#flows-count').textContent = n + ' of ' + fr.length + ' flows'; };
    fx.addEventListener('change', upd); upd();
  }

  /* diagrams: zoom, fit, full screen */
  $$('.fig').forEach(function (fig) {
    var svg = $('svg', fig), canvas = $('.fig-canvas', fig), zl = $('.fig-zoom', fig);
    if (!svg || !canvas) return;
    var vb = svg.viewBox && svg.viewBox.baseVal;
    var base = (vb && vb.width) || (svg.width && svg.width.baseVal && svg.width.baseVal.value) || 1000, z = 1;
    var set = function (nz) { z = Math.min(4, Math.max(0.25, nz)); svg.style.maxWidth = 'none'; svg.style.width = Math.round(base * z) + 'px'; if (zl) zl.textContent = Math.round(z * 100) + '%'; };
    var fit = function () { svg.style.width = ''; svg.style.maxWidth = '100%'; z = Math.min(1, (canvas.clientWidth - 24) / base); if (zl) zl.textContent = 'fit'; };
    var on = function (act, fn) { var b = $('[data-act="' + act + '"]', fig); if (b) b.addEventListener('click', fn); };
    on('in', function () { set(z * 1.25); }); on('out', function () { set(z / 1.25); }); on('fit', fit);
    on('full', function () { if (document.fullscreenElement) { document.exitFullscreen(); } else if (fig.requestFullscreen) { fig.requestFullscreen(); } });
    fit();
  });
})();
