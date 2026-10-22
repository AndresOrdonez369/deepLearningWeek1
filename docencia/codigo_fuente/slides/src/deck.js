/* Deck engine · Semana 1 · "Sala de señales"
   Keys: → / Space / PageDown next · ← / PageUp previous · G index · P presenter view · F fullscreen
         L laser pointer · B blank screen · number + Enter jump · Home / End */
(function () {
  'use strict';
  var D = document, html = D.documentElement;
  html.classList.add('js');
  var Q = new URLSearchParams(location.search);
  var MODE = Q.has('presenter') ? 'presenter' : Q.has('print') ? 'print' : 'audience';
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var READING = MODE === 'audience' && (Q.has('leer') || (innerWidth < 760 && innerHeight > innerWidth));

  var C = {night:'#07101c', night2:'#0f1a29', night3:'#182436', line:'#2d394a', grid:'#151e2c', ink:'#f1f6fa', ink2:'#b6c6d7', ink3:'#899aae',
           amber:'#ffb541', azure:'#4abaf4', mint:'#64eab7', coral:'#fd7466', lilac:'#c2a7f4'};

  /* ---------- demo registry ---------- */
  var DEMOS = {};
  function demo(name, factory) { DEMOS[name] = factory; }
  window.DeckDemo = demo;
  window.DeckColors = C;
  window.DeckRM = RM;

  function boot() {
    var vp = D.getElementById('viewport'), stage = D.getElementById('stage');
    var slides = [].slice.call(stage.querySelectorAll('.slide'));
    var N = slides.length, cur = -1, step = 0;
    var meta = slides.map(function (s) {
      var m = +(s.dataset.steps || 0);
      [].forEach.call(s.querySelectorAll('[data-step]'), function (e) { m = Math.max(m, +e.dataset.step || 0); });
      return { id: s.id, title: s.dataset.title || '', block: s.dataset.block || '', steps: m, el: s };
    });

    /* demo instances, created lazily */
    function instances(s) {
      if (!s._demos) {
        s._demos = [];
        [].forEach.call(s.querySelectorAll('[data-demo]'), function (el) {
          var f = DEMOS[el.dataset.demo];
          if (!f) { console.warn('missing demo', el.dataset.demo); return; }
          var api = { el: el, slide: s, active: false, C: C, RM: RM, print: MODE === 'print' || READING };
          api.raf = function (fn) {           // runs fn(t, dt) every frame while the slide is active
            var last = 0, id = 0;
            function tick(t) { if (!api.active) { id = 0; return; } var dt = last ? Math.min(50, t - last) : 16; last = t; if (fn(t, dt) === false) { id = 0; return; } id = requestAnimationFrame(tick); }
            return { start: function () { if (!id) { last = 0; id = requestAnimationFrame(tick); } }, stop: function () { if (id) cancelAnimationFrame(id); id = 0; } };
          };
          try { var inst = f(el, api) || {}; inst.api = api; s._demos.push(inst); } catch (e) { console.error(el.dataset.demo, e); }
        });
      }
      return s._demos;
    }
    function call(s, fn, arg) {
      instances(s).forEach(function (d) { if (d[fn]) { try { d[fn](arg); } catch (e) { console.error(fn, e); } } });
    }
    function enter(s, st) { instances(s).forEach(function (d) { d.api.active = true; }); call(s, 'enter', st); }
    function leave(s) { call(s, 'leave'); instances(s).forEach(function (d) { d.api.active = false; }); }

    function applySteps(s, st) {
      [].forEach.call(s.querySelectorAll('[data-step]'), function (e) {
        var n = +e.dataset.step || 0;
        e.classList.toggle('on', n <= st);
        if (e.dataset.dim) e.classList.toggle('dim', st >= +e.dataset.dim);
      });
      call(s, 'step', st);
    }

    function find(h) {
      h = decodeURIComponent((h || '').replace(/^#\/?/, ''));
      if (!h) return 0;
      if (/^\d+$/.test(h)) return Math.max(0, Math.min(N - 1, +h - 1));
      for (var i = 0; i < N; i++) if (meta[i].id === h) return i;
      return 0;
    }

    /* ---------- reading mode: everything visible, demos start when scrolled into view ---------- */
    if (READING) {
      D.body.classList.add('reading');
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var s = e.target, i = slides.indexOf(s);
          if (e.isIntersecting) { enter(s, meta[i].steps); applySteps(s, meta[i].steps); }
          else if (s._demos) leave(s);
        });
      }, { rootMargin: '120px' });
      slides.forEach(function (s) { applySteps(s, 99); io.observe(s); });
      buildIndex();
      D.querySelector('#chrome [data-a=index]').onclick = function () { D.body.classList.toggle('show-index'); };
      return;
    }

    /* ---------- print mode: every slide, every step, demos in their final state ---------- */
    if (MODE === 'print') {
      D.body.classList.add('print');
      slides.forEach(function (s, i) { s.classList.add('active'); enter(s, meta[i].steps); applySteps(s, meta[i].steps); call(s, 'final'); });
      setTimeout(function () { window.__deckReady = true; }, 600);
      return;
    }

    /* ---------- fit the 1920x1080 stage ---------- */
    var fitBox = vp;
    function fit() {
      var w = fitBox.clientWidth, h = fitBox.clientHeight, k = Math.min(w / 1920, h / 1080);
      stage.style.transform = 'translate(' + (w - 1920 * k) / 2 + 'px,' + (h - 1080 * k) / 2 + 'px) scale(' + k + ')';
    }

    /* ---------- navigation ---------- */
    var chan = null;
    try { chan = new BroadcastChannel('dl1-deck'); chan.onmessage = function (e) { onMsg(e.data); }; } catch (e) {}
    var pw = null;
    function post(m) {
      m.k = 'dl1';
      try { if (pw && !pw.closed) pw.postMessage(m, '*'); } catch (e) {}
      try { if (window.opener && !window.opener.closed) window.opener.postMessage(m, '*'); } catch (e) {}
      try { if (chan) chan.postMessage(m); } catch (e) {}
    }
    function onMsg(m) { if (m && m.k === 'dl1' && m.t === 'go' && (m.i !== cur || m.s !== step)) go(m.i, m.s, true); }
    window.addEventListener('message', function (e) { onMsg(e.data); });

    function go(i, s, remote) {
      i = Math.max(0, Math.min(N - 1, i)); s = Math.max(0, Math.min(meta[i].steps, s || 0));
      if (i !== cur) {
        var old = slides[cur];
        if (old) { old.classList.remove('active'); old.classList.toggle('before', i > cur); leave(old); }
        var el = slides[i]; el.classList.remove('before'); el.classList.add('active');
        cur = i; enter(el, s);
      }
      step = s; applySteps(slides[i], s);
      chrome(); presenterUpdate();
      try { history.replaceState(null, '', '#' + meta[i].id); } catch (e) {}
      if (!remote) post({ t: 'go', i: i, s: s });
    }
    function next() { if (step < meta[cur].steps) go(cur, step + 1); else if (cur < N - 1) go(cur + 1, 0); }
    function prev() { if (step > 0) go(cur, step - 1); else if (cur > 0) go(cur - 1, meta[cur - 1].steps); }
    window.Deck = { go: go, next: next, prev: prev, get cur() { return cur; }, get step() { return step; }, meta: meta };

    /* ---------- chrome ---------- */
    var ch = D.getElementById('chrome'), bar = ch.querySelector('.bar i'), secl = ch.querySelector('.sec-l'), cnt = ch.querySelector('.cnt');
    var blocks = {};
    slides.forEach(function (s) { if (s.dataset.blockname) blocks[s.dataset.block] = s.dataset.blockname; });
    function chrome() {
      bar.style.width = (N > 1 ? cur / (N - 1) * 100 : 100) + '%';
      var b = meta[cur].block;
      secl.textContent = blocks[b] ? blocks[b] : (slides[cur].dataset.label || '');
      cnt.textContent = (cur + 1) + ' / ' + N;
    }
    ch.querySelector('[data-a=prev]').onclick = prev;
    ch.querySelector('[data-a=next]').onclick = next;
    ch.querySelector('[data-a=index]').onclick = function () { toggleIndex(); };
    ch.querySelector('[data-a=presenter]').onclick = openPresenter;
    ch.querySelector('[data-a=full]').onclick = full;
    var idleT = 0;
    function wake() { ch.classList.remove('idle'); clearTimeout(idleT); idleT = setTimeout(function () { ch.classList.add('idle'); }, 2600); }
    D.addEventListener('mousemove', wake); wake();

    function full() {
      if (!D.fullscreenElement) { (html.requestFullscreen || html.webkitRequestFullscreen || function () {}).call(html); }
      else { (D.exitFullscreen || D.webkitExitFullscreen).call(D); }
    }

    /* laser pointer: easier to follow than the mouse cursor in a Teams screen share */
    var laser = D.getElementById('laser');
    D.addEventListener('mousemove', function (e) { laser.style.left = e.clientX + 'px'; laser.style.top = e.clientY + 'px'; });

    /* ---------- index overlay ---------- */
    function buildIndex() {
      var ix = D.getElementById('index'), out = '<h2>Índice de la semana</h2>', last = null, open = false;
      meta.forEach(function (m, i) {
        var g = slides[i].dataset.group || '';
        if (g !== last) { if (open) out += '</div></div>'; out += '<div class="grp"><h3>' + g + '</h3><div>'; open = true; last = g; }
        out += '<button type="button" data-i="' + i + '"><b>' + (i + 1) + '</b>' + m.title + '</button>';
      });
      if (open) out += '</div></div>';
      out += '<p class="help"><kbd>→</kbd> <kbd>espacio</kbd> avanzar · <kbd>←</kbd> retroceder · <kbd>G</kbd> índice · <kbd>P</kbd> vista del presentador (notas y reloj en otra ventana) · <kbd>F</kbd> pantalla completa · <kbd>L</kbd> puntero láser · <kbd>B</kbd> pantalla negra · número + <kbd>Enter</kbd> ir a la lámina</p>';
      ix.innerHTML = out;
      ix.addEventListener('click', function (e) {
        var b = e.target.closest('button[data-i]'); if (!b) return;
        var i = +b.dataset.i;
        if (READING) { slides[i].scrollIntoView(); D.body.classList.remove('show-index'); return; }
        go(i, 0); toggleIndex(false);
      });
    }
    function toggleIndex(v) {
      var on = v === undefined ? !D.body.classList.contains('show-index') : v;
      D.body.classList.toggle('show-index', on);
      if (on) {
        [].forEach.call(D.querySelectorAll('#index button'), function (b) { b.classList.toggle('cur', +b.dataset.i === cur); });
        var c = D.querySelector('#index button.cur'); if (c) c.scrollIntoView({ block: 'center' });
      }
    }
    buildIndex();

    /* ---------- presenter view ---------- */
    function openPresenter() {
      var u = location.href.split('#')[0];
      u += (u.indexOf('?') >= 0 ? '&' : '?') + 'presenter';
      pw = window.open(u + '#' + meta[cur].id, 'dl1-presenter', 'width=1400,height=820');
    }
    var pv = null, t0 = Date.now();
    function presenterSetup() {
      D.body.classList.add('presenter');
      pv = D.getElementById('pv');
      pv.innerHTML = '<header><span class="clock">00:00</span><button type="button" data-a="reset">Reiniciar reloj</button>' +
        '<span class="now"></span><span class="pos"></span><button type="button" data-a="prev">← Anterior</button><button type="button" data-a="next">Siguiente →</button></header>' +
        '<div class="cur"><span class="lab">En pantalla</span></div><div class="side"><div class="next"><span class="lab">Sigue</span></div><div class="nt"></div></div>';
      var box = pv.querySelector('.cur');
      box.appendChild(vp); vp.style.position = 'absolute'; vp.style.display = 'block';
      fitBox = box;
      pv.querySelector('[data-a=reset]').onclick = function () { t0 = Date.now(); };
      pv.querySelector('[data-a=prev]').onclick = prev;
      pv.querySelector('[data-a=next]').onclick = next;
      setInterval(function () {
        var s = Math.floor((Date.now() - t0) / 1000);
        pv.querySelector('.clock').textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
      }, 500);
      new ResizeObserver(function () { fit(); fitNext(); }).observe(box);
    }
    function fitNext() {
      var nb = pv && pv.querySelector('.next .mini'); if (!nb) return;
      var w = nb.parentNode.clientWidth, k = w / 1920; nb.style.transform = 'scale(' + k + ')';
    }
    function presenterUpdate() {
      if (!pv) return;
      var s = slides[cur], m = meta[cur];
      pv.querySelector('.now').textContent = m.title;
      pv.querySelector('.pos').textContent = (cur + 1) + ' / ' + N + (m.steps ? ' · paso ' + step + ' de ' + m.steps : '');
      var n = s.querySelector('.notes');
      pv.querySelector('.nt').innerHTML = '<h4>' + (s.dataset.min ? 'Tiempo sugerido: ' + s.dataset.min + ' min' : 'Notas') + '</h4>' + (n ? n.innerHTML : '<p>Sin notas.</p>');
      var nx = pv.querySelector('.next'), old = nx.querySelector('.mini'); if (old) old.remove();
      if (cur < N - 1) {
        var c = slides[cur + 1].cloneNode(true);
        c.removeAttribute('id'); c.classList.add('active'); c.style.transition = 'none';
        [].forEach.call(c.querySelectorAll('[data-step]'), function (e) { e.classList.add('on'); });
        [].forEach.call(c.querySelectorAll('[id]'), function (e) { e.removeAttribute('id'); });
        var wrap = D.createElement('div'); wrap.className = 'mini'; wrap.appendChild(c);
        nx.appendChild(wrap); fitNext();
      }
    }

    /* ---------- input ---------- */
    var digits = '';
    D.addEventListener('keydown', function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      var t = e.target, tag = (t.tagName || '').toLowerCase(), k = e.key;
      var onRange = tag === 'input' && t.type === 'range';
      var onBtn = tag === 'button' || tag === 'a' || tag === 'select' || (tag === 'input' && !onRange);
      if (D.body.classList.contains('show-index') && (k === 'Escape' || k === 'g' || k === 'G')) { toggleIndex(false); e.preventDefault(); return; }
      if (/^[0-9]$/.test(k)) { digits += k; return; }
      if (k === 'Enter' && digits) { go(+digits - 1, 0); digits = ''; e.preventDefault(); return; }
      digits = '';
      if (k === 'PageDown' || (!onRange && (k === 'ArrowRight' || k === 'ArrowDown')) || (!onBtn && !onRange && (k === ' ' || k === 'Enter'))) { next(); e.preventDefault(); }
      else if (k === 'PageUp' || (!onRange && (k === 'ArrowLeft' || k === 'ArrowUp')) || (!onBtn && !onRange && k === 'Backspace')) { prev(); e.preventDefault(); }
      else if (k === 'Home') { go(0, 0); e.preventDefault(); }
      else if (k === 'End') { go(N - 1, meta[N - 1].steps); e.preventDefault(); }
      else if (k === 'f' || k === 'F') full();
      else if (k === 'g' || k === 'G' || k === 'Escape') { if (k !== 'Escape' || !D.fullscreenElement) toggleIndex(); }
      else if (k === 'p' || k === 'P') { if (MODE !== 'presenter') openPresenter(); }
      else if (k === 'l' || k === 'L') D.body.classList.toggle('laser');
      else if (k === 'b' || k === 'B' || k === '.') D.body.classList.toggle('blanked');
    });
    var tx = 0, ty = 0, tok = false;
    vp.addEventListener('touchstart', function (e) {
      var t = e.target; tok = !t.closest('input,button,canvas,[data-drag]');
      tx = e.touches[0].clientX; ty = e.touches[0].clientY;
    }, { passive: true });
    vp.addEventListener('touchend', function (e) {
      if (!tok) return;
      var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.4) { if (dx < 0) next(); else prev(); }
    }, { passive: true });

    if (MODE === 'presenter') presenterSetup();
    window.addEventListener('resize', fit);
    fit();
    var i0 = find(location.hash);
    go(i0, 0, MODE === 'presenter');
    window.addEventListener('hashchange', function () { var i = find(location.hash); if (i !== cur) go(i, 0); });
  }

  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else setTimeout(boot, 0);
})();
