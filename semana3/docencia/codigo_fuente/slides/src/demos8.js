/* Demos · Semana 3 · Tema 1: generalizar y ser robusto.
   Every number comes from the real runs of NB05 (tools/run_tema1.py → window.T1); photos from window.FMNIST. */
(function () {
  var T = window.T1, F = window.FMNIST, CL = F.clases, W = window.W2;
  var BOOT = F.samples[0].px;                       // the first test photo: a boot (also the adversarial example)
  var MONO = 'JetBrains Mono, monospace';
  function pc(v, d) { return f(v * 100, d == null ? 1 : d) + '\u00a0%'; }
  function miles(v) { return Math.round(v).toLocaleString('es-EC').replace(/[.,]/g, ' '); }
  var _cid = 0;
  function clipRect(svg, x, y, w, h) {             // a clip rectangle whose width we animate to reveal a curve
    var defs = svg.querySelector('defs') || S('defs', {}, svg), id = 'c8' + (++_cid);
    var cp = S('clipPath', { id: id }, defs), r = S('rect', { x: x, y: y, width: w, height: h }, cp);
    return { id: 'url(#' + id + ')', r: r };
  }
  /* shift a 28x28 photo by (dx, dy) pixels: 'zero' fills with black like mover() in the NB,
     'reflect' mirrors the border like keras.layers.RandomTranslation (its default fill_mode) */
  function shift(P, dx, dy, mode) {
    var n = P.length;
    function rf(i) { while (i < 0 || i >= n) i = i < 0 ? -i - 1 : 2 * n - i - 1; return i; }
    return range(n).map(function (r) {
      return range(n).map(function (c) {
        var rr = r - dy, cc = c - dx;
        if (mode === 'reflect') return P[rf(rr)][rf(cc)];
        return rr < 0 || rr >= n || cc < 0 || cc >= n ? 0 : P[rr][cc];
      });
    });
  }
  window.W3 = { shift: shift, pc: pc, miles: miles, clipRect: clipRect };

  /* ---------------- curvas: training vs validation loss, epoch by epoch (overfitting; with and without brakes) ---------------- */
  function lossPlot(svg, box, run, n, ymax) {
    var sx = lin(1, n, box.x, box.x + box.w), sy = lin(0, ymax, box.y + box.h, box.y), g = S('g', {}, svg);
    [0, 0.25, 0.5, 0.75, 1].forEach(function (v) {
      if (v > ymax + 1e-9) return;
      S('line', { x1: box.x, x2: box.x + box.w, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, g);
      txt(g, box.x - 14, sy(v) + 8, f(v, 2), { 'text-anchor': 'end', 'font-size': 24, fill: C.ink3, 'font-family': MONO });
    });
    var tick = n > 70 ? 20 : 10;
    for (var e = tick; e <= n; e += tick) txt(g, sx(e), box.y + box.h + 34, String(e), { 'text-anchor': 'middle', 'font-size': 24, fill: C.ink3 });
    txt(g, box.x + box.w / 2, box.y + box.h + 68, 'época (cada vuelta completa a las fotos de estudio)', { 'text-anchor': 'middle', 'font-size': 23, fill: C.ink3 });
    txt(g, box.x - 14, box.y - 18, 'pérdida', { 'text-anchor': 'end', 'font-size': 23, fill: C.ink3 });
    function path(vals) { return vals.map(function (v, i) { return (i ? 'L' : 'M') + sx(i + 1).toFixed(1) + ' ' + sy(Math.min(v, ymax * 1.15)).toFixed(1); }).join(''); }
    var all = clipRect(svg, box.x - 10, box.y - 6, box.w + 20, box.h + 12);
    var cT = clipRect(svg, box.x - 10, box.y - 40, 0, box.h + 80), cV = clipRect(svg, box.x - 10, box.y - 40, 0, box.h + 80);
    var gT = S('g', { 'clip-path': cT.id }, g), gV = S('g', { 'clip-path': cV.id }, g);
    S('path', { d: path(run.train_loss), fill: 'none', stroke: C.amber, 'stroke-width': 5, 'stroke-linejoin': 'round', 'clip-path': all.id }, gT);
    S('path', { d: path(run.val_loss), fill: 'none', stroke: C.ink, 'stroke-width': 4, 'stroke-dasharray': '12 9', 'stroke-linejoin': 'round', 'clip-path': all.id }, gV);
    return {
      sx: sx, sy: sy, g: g,
      reveal: function (which, e) { var w = clamp(sx(e) - box.x + 10, 0, box.w + 20); (which === 'v' ? cV : cT).r.setAttribute('width', w); }
    };
  }
  demo('curvas', function (el, api) {
    var two = el.dataset.mode === 'dos', A = T.sobreajuste, B = T.regularizada;
    if (!two) {
      /* one run: 1 000 photos, 60 epochs, no brakes; a slider scrubs the epochs */
      var n = A.train_loss.length, e = n, s0 = 0, tw = null;
      var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,1fr) 14em;grid-template-rows:minmax(0,1fr);gap:1.6em;height:100%';
      var lc = H('div', 'col', root); lc.style.cssText += ';gap:.7em;min-height:0';
      var pl = H('div', 'fig plate', lc); pl.style.flex = '1';
      var svg = svgIn(pl, 1300, 640, 'Pérdida de entrenamiento y de validación en 60 épocas con 1 000 fotos');
      var P = lossPlot(svg, { x: 110, y: 50, w: 1150, h: 470 }, A, n, 1);
      var zone = S('rect', { x: P.sx(A.best_epoch), y: 50, width: P.sx(n) - P.sx(A.best_epoch), height: 470, fill: C.coral, 'fill-opacity': 0.08 }, P.g);
      var zl = txt(P.g, P.sx(A.best_epoch) + 22, 92, 'aquí memoriza', { 'font-size': 26, 'font-weight': 700, fill: C.coral });
      var bl = S('line', { x1: P.sx(A.best_epoch), x2: P.sx(A.best_epoch), y1: 50, y2: 520, stroke: C.mint, 'stroke-width': 4, 'stroke-dasharray': '6 8' }, P.g);
      var bd = S('circle', { cx: P.sx(A.best_epoch), cy: P.sy(A.val_loss[A.best_epoch - 1]), r: 11, fill: C.mint }, P.g);
      var bt = txt(P.g, P.sx(A.best_epoch) - 16, P.sy(A.val_loss[A.best_epoch - 1]) + 50, 'época ' + A.best_epoch + ': el mejor simulacro', { 'text-anchor': 'end', 'font-size': 23, 'font-weight': 700, fill: C.mint });
      var mk = [zone, zl, bl, bd, bt];
      var cur = S('line', { y1: 50, y2: 520, stroke: C.ink3, 'stroke-width': 2 }, P.g);
      var dT = S('circle', { r: 9, fill: C.amber }, P.g), dV = S('circle', { r: 9, fill: C.ink }, P.g);
      var c = H('div', 'ctrl', lc); c.style.gridTemplateColumns = '6em 1fr 3.4em';
      H('label', '', c, 'época');
      var inp = H('input', '', c); inp.type = 'range'; inp.min = 1; inp.max = n; inp.step = 1; inp.value = n; inp.setAttribute('aria-label', 'época');
      var out = H('output', '', c);
      var rc = H('div', 'col', root); rc.style.cssText += ';gap:1em;justify-content:center';
      var lgd = H('div', 'legend', rc, '<span><i style="background:var(--amber)"></i>Entrenamiento · 1 000 fotos</span><span><i style="background:var(--ink)"></i>Simulacro · 2 000 fotos</span>'); lgd.style.flexDirection = 'column'; lgd.style.gap = '.4em';
      var r1 = H('div', 'rd8', rc), r2 = H('div', 'rd8', rc);
      var lockT = false;                           // step 2: the training curve stays complete while the validation one plays
      function show() {
        var i = e - 1, vOn = s0 >= 2;
        P.reveal('t', s0 >= 1 ? (lockT ? n : e) : 0); P.reveal('v', vOn ? e : 0);
        cur.setAttribute('x1', P.sx(e)); cur.setAttribute('x2', P.sx(e)); cur.style.opacity = s0 >= 1 ? 1 : 0;
        dT.setAttribute('cx', P.sx(e)); dT.setAttribute('cy', P.sy(Math.min(1.1, A.train_loss[i]))); dT.style.opacity = s0 >= 1 ? 1 : 0;
        dV.setAttribute('cx', P.sx(e)); dV.setAttribute('cy', P.sy(Math.min(1.1, A.val_loss[i]))); dV.style.opacity = vOn ? 1 : 0;
        out.textContent = e; inp.value = e;
        r1.innerHTML = '<span>entrenamiento</span><b class="num am">' + pc(A.train_acc[i]) + '</b><small>pérdida ' + f(A.train_loss[i], 2) + '</small>';
        r2.innerHTML = '<span>simulacro</span><b class="num">' + (vOn ? pc(A.val_acc[i]) : '?') + '</b><small>' + (vOn ? 'pérdida ' + f(A.val_loss[i], 2) : 'aparece en el paso 2') + '</small>';
        mk.forEach(function (m) { m.style.transition = 'opacity .5s'; m.style.opacity = s0 >= 3 ? 1 : 0; });
      }
      inp.addEventListener('input', function () { if (tw) tw.stop(); lockT = false; e = +inp.value; show(); });
      function play() { if (tw) tw.stop(); if (api.print || RM) { e = n; show(); return; } tw = tween(2200, function (k) { e = Math.max(1, Math.round(1 + k * (n - 1))); show(); }, function () { lockT = false; }); }
      show();
      return {
        step: function (s) { var prev = s0; s0 = s; if ((s === 1 && prev < 1) || (s === 2 && prev < 2)) { lockT = s === 2; play(); } else { if (s < prev) e = n; show(); } },
        leave: function () { if (tw) tw.stop(); },
        final: function () { s0 = 3; e = n; show(); }
      };
    }
    /* two runs side by side: without brakes (60 epochs) and with brakes (EarlyStopping stopped at 79, kept 71) */
    var svg2 = svgIn(el, 1600, 640, 'Curvas de pérdida sin frenos y con frenos');
    var LB = { x: 90, y: 120, w: 620, h: 370 }, RB = { x: 930, y: 120, w: 620, h: 370 };
    var L = lossPlot(svg2, LB, A, 60, 1), R = lossPlot(svg2, RB, B, 80, 1);
    txt(svg2, LB.x, 34, 'Sin frenos · 60 épocas', { 'font-size': 30, 'font-weight': 700, fill: C.coral });
    var rt = txt(svg2, RB.x, 34, 'Con frenos · se detuvo sola en la época ' + B.epochs, { 'font-size': 30, 'font-weight': 700, fill: C.mint });
    function marker(P, box, ep, lab, col, dy) {
      var g = S('g', {}, svg2);
      S('line', { x1: P.sx(ep), x2: P.sx(ep), y1: box.y, y2: box.y + box.h, stroke: col, 'stroke-width': 4, 'stroke-dasharray': '6 8' }, g);
      txt(g, P.sx(ep) - 12, box.y + 30 + (dy || 0), lab, { 'text-anchor': 'end', 'font-size': 21, 'font-weight': 700, fill: col });
      return g;
    }
    var mA = marker(L, LB, A.best_epoch, 'mejor simulacro: época ' + A.best_epoch, C.mint);
    var mB = marker(R, RB, B.best_epoch, 'se queda con la ' + B.best_epoch, C.mint, 0), mS = S('line', { x1: R.sx(B.epochs), x2: R.sx(B.epochs), y1: RB.y, y2: RB.y + RB.h, stroke: C.ink3, 'stroke-width': 3 }, svg2);
    var tA = txt(svg2, LB.x, 72, 'examen final ' + pc(A.test), { 'font-size': 27, 'font-weight': 700, fill: C.ink, 'font-family': MONO });
    var tB = txt(svg2, RB.x, 72, 'examen final ' + pc(B.test), { 'font-size': 27, 'font-weight': 700, fill: C.amber, 'font-family': MONO });
    var lg = S('g', {}, svg2);
    S('rect', { x: 600, y: 610, width: 34, height: 8, rx: 4, fill: C.amber }, lg); txt(lg, 646, 620, 'entrenamiento', { 'font-size': 22, fill: C.ink2 });
    S('line', { x1: 840, x2: 874, y1: 614, y2: 614, stroke: C.ink, 'stroke-width': 4, 'stroke-dasharray': '8 6' }, lg); txt(lg, 886, 620, 'simulacro', { 'font-size': 22, fill: C.ink2 });
    var st2 = 0, tws = [];
    function anim(P, nn, done) {
      if (api.print || RM) { P.reveal('t', nn); P.reveal('v', nn); return; }
      tws.push(tween(1800, function (k) { var e2 = 1 + k * (nn - 1); P.reveal('t', e2); P.reveal('v', e2); }, done));
    }
    function set(s, still) {
      var prev = st2; st2 = s;
      if (s >= 1 && (prev < 1 || still)) anim(L, 60); if (s < 1) { L.reveal('t', 0); L.reveal('v', 0); }
      if (s >= 2 && (prev < 2 || still)) anim(R, B.epochs); if (s < 2) { R.reveal('t', 0); R.reveal('v', 0); }
      [mA, tA].forEach(function (m) { m.style.transition = 'opacity .5s'; m.style.opacity = s >= 3 ? 1 : 0; });
      [mB, mS, tB].forEach(function (m) { m.style.transition = 'opacity .5s'; m.style.opacity = s >= 3 ? 1 : 0; });
      rt.style.opacity = s >= 2 ? 1 : 0.3;
    }
    set(0);
    return {
      step: function (s) { set(s); },
      leave: function () { tws.forEach(function (t) { t.stop(); }); },
      final: function () { st2 = 0; set(3, true); }
    };
  });

  /* ---------------- dropout: in every batch any neuron may be resting, so nobody can depend on one teammate ---------------- */
  demo('dropout', function (el, api) {
    var Ls = [4, 6, 6, 3], Wd = 440, Hd = 300, svg = svgIn(el, Wd, Hd, 'Red en la que algunas neuronas descansan al azar en cada lote');
    var xs = [40, 165, 290, 405], nodes = Ls.map(function (n, i) { return range(n).map(function (j) { return { x: xs[i], y: Hd / 2 - 18 + (j - (n - 1) / 2) * 40, l: i }; }); });
    var gE = S('g', {}, svg), gN = S('g', {}, svg), edges = [];
    for (var l = 0; l < 3; l++) nodes[l].forEach(function (a) { nodes[l + 1].forEach(function (b) { edges.push({ a: a, b: b, el: S('line', { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: C.amber, 'stroke-width': 2, opacity: 0.35 }, gE) }); }); });
    nodes.forEach(function (col) { col.forEach(function (n) { n.c = S('circle', { cx: n.x, cy: n.y, r: 13, fill: C.night2, stroke: n.l === 1 || n.l === 2 ? C.amber : C.ink3, 'stroke-width': 4 }, gN); n.t = txt(gN, n.x, n.y + 8, '×', { 'text-anchor': 'middle', 'font-size': 24, 'font-weight': 700, fill: C.coral, opacity: 0 }); }); });
    var lab = txt(svg, Wd / 2, Hd - 8, '', { 'text-anchor': 'middle', 'font-size': 21, fill: C.ink2 });
    var rnd = seeded(+(el.dataset.seed || 7)), lote = 0;
    function draw() {
      lote++; var off = 0;
      nodes.forEach(function (col, i) { col.forEach(function (n) { n.off = (i === 1 || i === 2) && rnd() < 0.3; if (n.off) off++; n.c.setAttribute('opacity', n.off ? 0.35 : 1); n.c.setAttribute('fill', n.off ? C.night : C.night2); n.t.setAttribute('opacity', n.off ? 1 : 0); }); });
      edges.forEach(function (e) { e.el.setAttribute('opacity', e.a.off || e.b.off ? 0.05 : 0.35); });
      lab.textContent = 'lote ' + lote + ' · descansan ' + off + ' de 12';
    }
    var acc = 0, loop = api.raf(function (t, dt) { acc += dt; if (acc > 1100) { acc = 0; draw(); } });
    draw();
    return { enter: function () { if (!RM && !api.print) loop.start(); }, leave: function () { loop.stop(); } };
  });

  /* ---------------- aumento: the same garment, moved a little (like RandomTranslation, a new version every epoch) ---------------- */
  demo('aumento', function (el, api) {
    var mini = el.dataset.mode === 'mini', cur = 0, rnd = seeded(2026), ep = 1;
    if (mini) {
      var pl = H('div', 'pplate', el); pl.style.cssText += ';width:auto;height:100%;margin:0 auto';
      var cv = W.canvas(pl, 28, 28);
      var o = svgIn(pl, 280, 280, 'La misma prenda, movida un poco en cada época');
      var lb = txt(o, 140, 266, '', { 'text-anchor': 'middle', 'font-size': 17, fill: C.ink2, 'font-family': MONO });
      function one() { var dx = Math.round(rnd() * 6 - 3), dy = Math.round(rnd() * 6 - 3); W.paint(cv, shift(BOOT, dx, dy, 'reflect'), W.gray); lb.textContent = (dx >= 0 ? '→ +' : '→ −') + Math.abs(dx) + '  ' + (dy >= 0 ? '↓ +' : '↓ −') + Math.abs(dy); }
      var a0 = 0, lp = api.raf(function (t, dt) { a0 += dt; if (a0 > 1000) { a0 = 0; one(); } });
      W.paint(cv, BOOT, W.gray);
      return { enter: function () { if (!RM && !api.print) lp.start(); }, leave: function () { lp.stop(); } };
    }
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,5fr) minmax(0,8fr);gap:2.2em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.cssText += ';gap:.7em;align-items:center';
    var big = H('div', 'pplate', lc); big.style.width = 'min(100%, 14em)';
    var bc = W.canvas(big, 28, 28);
    H('p', 'lab3', lc, '<b>La foto original</b> · siempre la misma respuesta');
    var th = H('div', 'thumbs', lc), tbs = [];
    [0, 1, 4, 6].forEach(function (k) {
      var s = F.samples[k], b = H('button', '', th); b.type = 'button'; b.setAttribute('aria-label', 'Usar ' + CL[s.label]);
      W.paint(W.canvas(b, 28, 28), s.px, W.gray); b.onclick = function () { cur = k; drawAll(); }; tbs.push([b, k]);
    });
    var rc = H('div', 'col', root); rc.style.gap = '.7em';
    var hd = H('p', 'lab3', rc);
    var g = H('div', '', rc); g.style.cssText = 'display:grid;grid-template-columns:repeat(5,minmax(0,7.4em));gap:.7em';
    var cells = range(10).map(function () {
      var c = H('div', 'col', g); c.style.cssText += ';gap:.25em;align-items:center';
      var p = H('div', 'pplate', c); p.style.width = '100%';
      var cv2 = W.canvas(p, 28, 28), lbl = H('span', 'mono8', c);
      return { cv: cv2, lbl: lbl };
    });
    H('p', 'cap', rc, '<code>RandomTranslation(0.15)</code>: cada copia se mueve al azar hasta 4 píxeles (15 % de 28) y el borde se rellena como un espejo. Sigue siendo un <b><span class="cn8"></span></b>.');
    function drawAll() {
      var P = F.samples[cur].px; W.paint(bc, P, W.gray);
      tbs.forEach(function (t) { t[0].classList.toggle('on', t[1] === cur); });
      cells.forEach(function (c) {
        var dx = Math.round(rnd() * 8 - 4), dy = Math.round(rnd() * 8 - 4);
        W.paint(c.cv, shift(P, dx, dy, 'reflect'), W.gray);
        c.lbl.textContent = (dx >= 0 ? '+' : '−') + Math.abs(dx) + ' · ' + (dy >= 0 ? '+' : '−') + Math.abs(dy);
      });
      hd.innerHTML = '<b>Lo que estudia la red en la época ' + ep + '</b> · 10 versiones movidas';
      [].forEach.call(el.querySelectorAll('.cn8'), function (x) { x.textContent = CL[F.samples[cur].label]; });
    }
    var acc = 0, loop = api.raf(function (t, dt) { acc += dt; if (acc > 1900) { acc = 0; ep++; drawAll(); } });
    drawAll();
    return { enter: function () { if (!RM && !api.print) loop.start(); }, leave: function () { loop.stop(); } };
  });

  /* ---------------- mover: accuracy on photos moved 0-4 px, without and with data augmentation ---------------- */
  demo('mover', function (el, api) {
    var Sn = T.aumento.sin, Cn = T.aumento.con, px = 0, s0 = 0, tw = null;
    var ys = { sin: [Sn.test, Sn.shift[1], Sn.shift[2], Sn.shift[3], Sn.shift[4]], con: [Cn.test, Cn.shift[1], Cn.shift[2], Cn.shift[3], Cn.shift[4]] };
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);grid-template-rows:minmax(0,1fr);gap:2.2em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.cssText += ';gap:.8em;align-items:stretch';
    var pl = H('div', 'pplate', lc); pl.style.cssText += ';width:min(100%,12em);margin:0 auto';
    var cv = W.canvas(pl, 28, 28);
    var cap = H('p', 'lab3', lc); cap.style.textAlign = 'center';
    var c = H('div', 'ctrl', lc); c.style.gridTemplateColumns = '5.2em 1fr 3.2em';
    H('label', '', c, 'mover');
    var inp = H('input', '', c); inp.type = 'range'; inp.min = 0; inp.max = 4; inp.step = 1; inp.value = 0; inp.setAttribute('aria-label', 'píxeles que se mueve la foto');
    var out = H('output', '', c);
    var rc = H('div', 'col', root); rc.style.cssText += ';gap:.6em;height:100%';
    var fg = H('div', 'fig plate', rc); fg.style.flex = '1';
    var svg = svgIn(fg, 1100, 560, 'Exactitud con fotos movidas de 0 a 4 píxeles, sin y con aumento de datos');
    var sx = lin(0, 4, 120, 1040), sy = lin(0, 1, 470, 40);
    [0, 0.25, 0.5, 0.75, 1].forEach(function (v) { S('line', { x1: 120, x2: 1040, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 104, sy(v) + 8, Math.round(v * 100) + '\u00a0%', { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 }); });
    [0, 1, 2, 3, 4].forEach(function (v) { txt(svg, sx(v), 506, v + ' px', { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 }); });
    txt(svg, 580, 546, 'cuántos píxeles se mueve la foto del examen', { 'text-anchor': 'middle', 'font-size': 21, fill: C.ink3 });
    var cur = S('rect', { y: 40, height: 430, width: 64, rx: 10, fill: C.ink, 'fill-opacity': 0.06 }, svg);
    function line(vals, col, lab) {
      var g = S('g', {}, svg);
      S('polyline', { points: vals.map(function (v, i) { return sx(i) + ',' + sy(v); }).join(' '), fill: 'none', stroke: col, 'stroke-width': 6, 'stroke-linejoin': 'round' }, g);
      var dots = vals.map(function (v, i) { return S('circle', { cx: sx(i), cy: sy(v), r: 9, fill: col }, g); });
      var t = txt(g, sx(4) + 4, sy(vals[4]) + (col === C.amber ? -22 : 40), lab, { 'text-anchor': 'end', 'font-size': 24, 'font-weight': 700, fill: col });
      return { g: g, dots: dots };
    }
    var Ls = line(ys.sin, C.azure, 'sin aumento'), Lc = line(ys.con, C.amber, 'con aumento');
    var rd = H('div', 'row', lc); rd.style.cssText += ';gap:.8em;justify-content:center;flex-wrap:nowrap';
    var r1 = H('div', 'rd8', rd), r2 = H('div', 'rd8', rd);
    function show() {
      W.paint(cv, shift(BOOT, px, 0, 'zero'), W.gray);
      cap.innerHTML = px ? '<b>El botín, movido ' + px + ' píxel' + (px > 1 ? 'es' : '') + '</b> a la derecha' : '<b>El botín</b>, sin mover';
      out.textContent = px + ' px'; inp.value = px;
      cur.setAttribute('x', sx(px) - 32);
      Ls.g.style.opacity = s0 >= 1 ? 1 : 0.06; Lc.g.style.opacity = s0 >= 2 ? 1 : 0.06;
      [Ls, Lc].forEach(function (L) { L.dots.forEach(function (d, i) { d.setAttribute('r', i === px ? 13 : 8); }); });
      r1.innerHTML = '<span>sin aumento</span><b class="num az">' + (s0 >= 1 ? pc(ys.sin[px]) : '?') + '</b>';
      r2.innerHTML = '<span>con aumento</span><b class="num am">' + (s0 >= 2 ? pc(ys.con[px]) : '?') + '</b>';
    }
    inp.addEventListener('input', function () { if (tw) tw.stop(); px = +inp.value; show(); });
    function sweep() { if (tw) tw.stop(); if (api.print || RM) { px = 4; show(); return; } tw = tween(2000, function (k) { px = Math.round(k * 4); show(); }); }
    [Ls.g, Lc.g].forEach(function (g) { g.style.transition = 'opacity .5s'; });
    show();
    return {
      step: function (s) { var p = s0; s0 = s; if (s > p && s <= 2) sweep(); else show(); },
      leave: function () { if (tw) tw.stop(); },
      final: function () { s0 = 2; px = 4; show(); }
    };
  });

  /* ---------------- adv: the real adversarial boot (FGSM, eps = 0.05): same photo to us, a sneaker to the network ---------------- */
  var EX = T.ejemplo_adv, SHOW4 = [9, 7, 5, 8];        // botín, zapatilla, sandalia, bolso
  var NOISE = EX.orig.map(function (r, i) { return r.map(function (v, j) { return EX.adv[i][j] - v; }); });
  function probBars(parent, probs, title) {
    var box = H('div', 'pb8', parent);
    if (title) H('p', 'lab3', box, title);
    var rows = SHOW4.map(function (k) {
      var r = H('div', 'pr8', box);
      H('span', 'n', r, CL[k]);
      var tr = H('span', 'tr', r), i = H('i', '', tr), v = H('b', 'num', r);
      return { k: k, i: i, v: v };
    });
    return {
      el: box,
      set: function (P) {
        var top = P.indexOf(Math.max.apply(null, P));
        rows.forEach(function (o) { var p = P[o.k]; o.i.style.width = (p * 100).toFixed(1) + '%'; o.i.style.background = o.k === top ? (o.k === EX.label ? C.mint : C.coral) : C.ink3; o.v.textContent = Math.round(p * 100) + '\u00a0%'; o.v.style.color = o.k === top ? (o.k === EX.label ? C.mint : C.coral) : C.ink3; });
      }
    };
  }
  demo('adv', function (el, api) {
    if (el.dataset.mode === 'cover') {
      var root0 = H('div', 'col', el); root0.style.cssText += ';gap:1.1em;height:100%;justify-content:center';
      var pl0 = H('div', 'pplate', root0); pl0.style.cssText += ';width:min(100%,24em);margin:0 auto';
      var cv0 = W.canvas(pl0, 28, 28);
      var tag = H('p', 'lab3', root0); tag.style.textAlign = 'center';
      var bars0 = probBars(root0, null, '');
      bars0.el.style.cssText += ';width:min(100%,24em);margin:0 auto';
      var on = false;
      function flip(v) { on = v; W.paint(cv0, on ? EX.adv : EX.orig, W.gray); bars0.set(on ? EX.p_adv : EX.p_orig); tag.innerHTML = on ? '<b style="color:var(--coral)">La misma foto con un ruido invisible</b> · la red dice zapatilla' : '<b>La foto original</b> · la red dice botín'; }
      var a0 = 0, lp = api.raf(function (t, dt) { a0 += dt; if (a0 > 2600) { a0 = 0; flip(!on); } });
      flip(false);
      return { enter: function () { if (!RM && !api.print) lp.start(); }, leave: function () { lp.stop(); }, final: function () { flip(false); } };
    }
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1fr);gap:.9em 1.4em;align-items:center;align-content:center;height:100%';
    function plate(label) { var c = H('div', 'col', root); c.style.cssText += ';gap:.5em;align-items:center'; var p = H('div', 'pplate', c); p.style.width = 'min(100%, 10.5em)'; H('p', 'lab3', c, label).style.textAlign = 'center'; return { c: c, p: p }; }
    var A = plate('<b>La foto</b> · botín del examen'), op1 = H('span', 'op8', root, '+');
    var B = plate('<b>Ruido</b> · aumentado para que se vea');
    var op2 = H('span', 'op8', root, '=');
    var Cc = plate('<b>La foto engañosa</b>');
    W.paint(W.canvas(A.p, 28, 28), EX.orig, W.gray);
    W.paint(W.canvas(B.p, 28, 28), NOISE.map(function (r) { return r.map(function (v) { return v / 13; }); }), W.signed);
    W.paint(W.canvas(Cc.p, 28, 28), EX.adv, W.gray);
    var b1 = probBars(root, null, 'La red dice'); b1.el.style.gridColumn = '1'; b1.set(EX.p_orig);
    var mid = H('p', 'cap', root, 'Ámbar: el píxel sube; azul: baja. Cada píxel cambia <b>como máximo 13 de 255</b> (ε = 0.05).'); mid.style.cssText = 'grid-column:2 / 5;text-align:center;align-self:start;margin-top:1.4em';
    var b2 = probBars(root, null, 'La red dice'); b2.el.style.gridColumn = '5'; b2.set(EX.p_adv);
    function set(s) {
      [A.c, b1.el].forEach(function (e) { e.style.opacity = s >= 1 ? 1 : 0.15; });
      [op1, B.c, mid].forEach(function (e) { e.style.opacity = s >= 2 ? 1 : 0.08; });
      [op2, Cc.c, b2.el].forEach(function (e) { e.style.opacity = s >= 3 ? 1 : 0.08; });
    }
    [A.c, b1.el, op1, B.c, mid, op2, Cc.c, b2.el].forEach(function (e) { e.style.transition = 'opacity .5s'; });
    set(0);
    return { step: set, final: function () { set(3); } };
  });

  /* ---------------- subir: training goes downhill on the weights; the attack goes uphill on the pixels ---------------- */
  demo('subir', function (el, api) {
    var svg = svgIn(el, 1000, 560, 'A la izquierda los pesos bajan por la pérdida; a la derecha el píxel sube por la pérdida');
    function panel(x0, title, sub, col) {
      var g = S('g', {}, svg), W0 = 440, sx = lin(-1, 1, x0 + 20, x0 + W0 - 20), sy = lin(0, 1.2, 470, 130);
      var Lf = function (v) { return 0.08 + 0.95 * v * v; };
      txt(g, x0 + W0 / 2, 40, title, { 'text-anchor': 'middle', 'font-size': 38, 'font-weight': 700, fill: col });
      txt(g, x0 + W0 / 2, 84, sub, { 'text-anchor': 'middle', 'font-size': 28, fill: C.ink2, 'font-family': MONO });
      S('path', { d: pathOf(Lf, -1, 1, sx, sy), fill: 'none', stroke: C.ink3, 'stroke-width': 5 }, g);
      txt(g, x0 + 24, 512, 'pérdida', { 'font-size': 24, fill: C.ink3 });
      return { g: g, sx: sx, sy: sy, L: Lf };
    }
    var A = panel(20, 'Entrenar · semana 1', 'peso − η · pendiente', C.mint), B = panel(540, 'Atacar · esta semana', 'píxel + ε · signo(pendiente)', C.coral);
    txt(A.g, 240, 545, 'los pesos bajan: la pérdida se achica', { 'text-anchor': 'middle', 'font-size': 27, fill: C.ink2 });
    txt(B.g, 760, 545, 'el píxel sube: la pérdida crece', { 'text-anchor': 'middle', 'font-size': 27, fill: C.ink2 });
    var ballA = S('circle', { r: 18, fill: C.mint }, A.g), ballB = S('circle', { r: 18, fill: C.coral }, B.g);
    var trail = S('path', { fill: 'none', stroke: C.coral, 'stroke-width': 4, 'stroke-dasharray': '8 8', opacity: 0 }, B.g);
    function put(P, b, v) { b.setAttribute('cx', P.sx(v)); b.setAttribute('cy', P.sy(P.L(v)) - 18); }
    var tw = null;
    function set(s, still) {
      if (tw) tw.stop();
      A.g.style.opacity = s >= 1 ? 1 : 0.15; B.g.style.opacity = s >= 2 ? 1 : 0.15;
      trail.setAttribute('opacity', s >= 2 ? 0.8 : 0);
      trail.setAttribute('d', pathOf(B.L, 0.05, 0.6, B.sx, function (y) { return B.sy(y) - 18; }, 40));
      var anim = !(api.print || RM || still);
      if (s === 1 && anim) tw = tween(1600, function (k) { put(A, ballA, -0.85 + 0.8 * k); });
      else put(A, ballA, s >= 1 ? -0.05 : -0.85);
      if (s === 2 && anim) tw = tween(1400, function (k) { put(B, ballB, 0.05 + 0.55 * k); });
      else put(B, ballB, s >= 2 ? 0.6 : 0.05);
    }
    [A.g, B.g].forEach(function (g) { g.style.transition = 'opacity .5s'; });
    set(0);
    return { step: function (s) { set(s); }, leave: function () { if (tw) tw.stop(); }, final: function () { set(2, true); } };
  });

  /* ---------------- fgsm: how much noise can it take? normal CNN vs the "vaccinated" one ---------------- */
  demo('fgsm', function (el, api) {
    var EPS = ['limpia', '0.01', '0.02', '0.05', '0.1'], EV = [0, 0.01, 0.02, 0.05, 0.1];
    var N = EPS.map(function (k) { return T.fgsm[k]; }), V = EPS.map(function (k) { return T.fgsm_entrenada[k]; });
    var SG = NOISE.map(function (r) { return r.map(function (v) { return v > 0 ? 1 : v < 0 ? -1 : 0; }); });
    var k = 3, s0 = 0;
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);grid-template-rows:minmax(0,1fr);gap:2.2em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.cssText += ';gap:.8em;align-items:center';
    var pl = H('div', 'pplate', lc); pl.style.width = 'min(100%, 12em)';
    var cv = W.canvas(pl, 28, 28);
    var cap = H('p', 'lab3', lc); cap.style.textAlign = 'center';
    var rd = H('div', 'row', lc); rd.style.cssText += ';gap:.8em;justify-content:center;flex-wrap:nowrap';
    var r1 = H('div', 'rd8', rd), r2 = H('div', 'rd8', rd);
    var rc = H('div', 'col', root); rc.style.cssText += ';gap:.6em;height:100%';
    var seg = H('div', 'seg', null), bs = EPS.map(function (e, i) { var b = H('button', 'btn', seg, i ? 'ε ' + e : 'sin ruido'); b.type = 'button'; b.onclick = function () { k = i; show(); }; return b; });
    var fg = H('div', 'fig plate', rc); fg.style.flex = '1'; rc.appendChild(seg); seg.style.justifyContent = 'center';
    var svg = svgIn(fg, 1100, 560, 'Exactitud según el tamaño del ruido, para la red normal y la vacunada');
    var sx = function (i) { return 140 + i * 215; }, sy = lin(0, 1, 470, 40);
    [0, 0.25, 0.5, 0.75, 1].forEach(function (v) { S('line', { x1: 120, x2: 1040, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 104, sy(v) + 8, Math.round(v * 100) + '\u00a0%', { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 }); });
    EPS.forEach(function (e, i) { txt(svg, sx(i), 506, i ? 'ε = ' + e : 'sin ruido', { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 }); });
    txt(svg, 580, 546, 'tamaño del ruido: cuánto puede moverse cada píxel (de 0 a 1)', { 'text-anchor': 'middle', 'font-size': 21, fill: C.ink3 });
    var cur = S('rect', { y: 40, height: 430, width: 120, rx: 10, fill: C.ink, 'fill-opacity': 0.06 }, svg);
    function line(vals, col, lab, dy) {
      var g = S('g', {}, svg);
      S('polyline', { points: vals.map(function (v, i) { return sx(i) + ',' + sy(v); }).join(' '), fill: 'none', stroke: col, 'stroke-width': 6, 'stroke-linejoin': 'round' }, g);
      var dots = vals.map(function (v, i) { return S('circle', { cx: sx(i), cy: sy(v), r: 9, fill: col }, g); });
      txt(g, sx(4) - 16, sy(vals[4]) + dy, lab, { 'text-anchor': 'end', 'font-size': 24, 'font-weight': 700, fill: col });
      g.style.transition = 'opacity .5s';
      return { g: g, dots: dots };
    }
    var Ln = line(N, C.azure, 'red normal', 40), Lv = line(V, C.amber, 'vacunada', 44);
    function show() {
      var e = EV[k];
      W.paint(cv, EX.orig.map(function (r, i) { return r.map(function (v, j) { return clamp(v + e * 255 * SG[i][j], 0, 255); }); }), W.gray);
      cap.innerHTML = k ? '<b>ε = ' + EPS[k] + '</b> · cada píxel cambia hasta ' + Math.round(e * 255) + ' de 255' : '<b>La foto limpia</b>';
      bs.forEach(function (b, i) { b.classList.toggle('on', i === k); });
      cur.setAttribute('x', sx(k) - 60);
      Ln.g.style.opacity = s0 >= 1 ? 1 : 0.06; Lv.g.style.opacity = s0 >= 2 ? 1 : 0.06;
      [Ln, Lv].forEach(function (L) { L.dots.forEach(function (d, i) { d.setAttribute('r', i === k ? 13 : 8); }); });
      r1.innerHTML = '<span>red normal</span><b class="num az">' + (s0 >= 1 ? pc(N[k]) : '?') + '</b>';
      r2.innerHTML = '<span>vacunada</span><b class="num am">' + (s0 >= 2 ? pc(V[k]) : '?') + '</b>';
    }
    show();
    return { step: function (s) { s0 = s; k = s >= 1 ? 3 : 0; show(); }, final: function () { s0 = 2; k = 3; show(); } };
  });

  /* ---------------- busqueda: random search, tuned on the validation set, tested once ---------------- */
  demo('busqueda', function (el, api) {
    var B = T.busqueda, rows = [], s0 = 0, tws = [];
    var root = H('div', 'tb8', el);
    var hd = H('div', 'tr8 h', root, '<span>#</span><span>learning rate</span><span>filtros</span><span>dropout</span><span>parámetros</span><span>simulacro</span>');
    B.trials.forEach(function (t, i) {
      var r = H('div', 'tr8', root);
      r.innerHTML = '<span class="num">' + (i + 1) + '</span><span class="num">' + String(t.lr) + '</span><span class="num">' + t.f1 + ' y ' + 2 * t.f1 + '</span><span class="num">' + String(t.drop).replace('0.0', '0') + '</span><span class="num">' + miles(t.params) + '</span>' +
        '<span class="bar8"><span class="tr"><i></i></span><b class="num"></b></span>';
      rows.push({ r: r, i: r.querySelector('i'), b: r.querySelector('b'), v: t.val });
    });
    var fin = H('div', 'fin8', root, 'La mejor combinación, en el <b>examen final</b> y una sola vez: <b class="num am">' + pc(B.test_best) + '</b>');
    var lo = 0.6;
    function fill(o, k) {                          // bar from 60 % to 90 %, counting up while it grows
      o.i.style.width = (clamp((o.v - lo) / (0.9 - lo), 0, 1) * 100 * k).toFixed(1) + '%';
      o.b.textContent = k > 0 ? pc(lo + (o.v - lo) * k) : '';
    }
    function set(s, still) {
      tws.forEach(function (t) { t.stop(); }); tws = [];
      var p = s0; s0 = s;
      rows.forEach(function (o, i) {
        o.r.classList.toggle('best', s >= 2 && i === B.best);
        o.r.classList.toggle('dim', s >= 2 && i !== B.best);
        if (s < 1) { o.r.style.opacity = 0.2; fill(o, 0); return; }
        if (p < 1 && s >= 1 && !still && !api.print && !RM) {
          o.r.style.opacity = 0.2; fill(o, 0);
          setTimeout(function () { o.r.style.opacity = 1; tws.push(tween(500, function (k) { fill(o, k); })); }, i * 380);
        } else { o.r.style.opacity = 1; fill(o, 1); }
      });
      fin.style.opacity = s >= 3 ? 1 : 0;
    }
    set(0);
    return { step: function (s) { set(s); }, final: function () { s0 = 0; set(3, true); } };
  });
})();
