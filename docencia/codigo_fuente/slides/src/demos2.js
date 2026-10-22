/* Demos · block 02 · the neuron (line, act, sigmoid, bend, calc bars) */

/* ---------------- line: one neuron draws one line; sliders move it ---------------- */
demo('line', function (el, api) {
  var W = 820, Hh = 700, x0 = 90, y0 = 30, x1 = 790, y1 = 610;
  var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:minmax(0,1fr) 14em;gap:28px;height:100%;align-items:center';
  var fig = H('div', 'fig', wrap); fig.style.minHeight = '0'; fig.style.alignSelf = 'stretch';
  var svg = svgIn(fig, W, Hh, 'Socios en un plano: ingreso en el eje horizontal y atrasos previos en el vertical, con la línea de decisión de la neurona');
  var sx = lin(-1, 1, x0, x1), sy = lin(-1, 1, y1, y0);
  var g0 = S('g', {}, svg); grid(g0, x0, y0, x1, y1, 70);
  var zoneA = S('polygon', { fill: C.amber, 'fill-opacity': 0.13 }, svg), zoneB = S('polygon', { fill: C.azure, 'fill-opacity': 0.13 }, svg);
  axes(svg, x0, y0, x1, y1);
  txt(svg, x1, y1 + 50, 'más ingreso →', { 'text-anchor': 'end', fill: C.ink3, 'font-size': 23 });
  txt(svg, x0 - 30, (y0 + y1) / 2, '↑ más atrasos', { 'text-anchor': 'middle', fill: C.ink3, 'font-size': 23, transform: 'rotate(-90 ' + (x0 - 30) + ' ' + ((y0 + y1) / 2) + ')' });
  var ln = S('line', { stroke: C.ink, 'stroke-width': 6, 'stroke-linecap': 'round' }, svg);
  var rnd = seeded(5), P = [];
  while (P.length < 18) {
    var a = rnd() * 1.8 - 0.9, b = rnd() * 1.8 - 0.9, s = 1.3 * a - 1.5 * b + 0.05;
    if (Math.abs(s) < 0.28) continue;
    P.push({ x: a, y: b, c: s > 0 ? 1 : 0 });
  }
  var gP = S('g', {}, svg);
  P.forEach(function (p) {
    p.ring = S('circle', { cx: sx(p.x), cy: sy(p.y), r: 25, fill: 'none', stroke: C.coral, 'stroke-width': 5, opacity: 0 }, gP);
    p.dot = S('circle', { cx: sx(p.x), cy: sy(p.y), r: 15, fill: p.c ? C.amber : C.azure, stroke: C.night, 'stroke-width': 4 }, gP);
  });
  var lab1 = txt(svg, 0, 0, 'aprueba', { 'font-size': 30, 'font-weight': 700, fill: C.amber, 'text-anchor': 'middle', stroke: C.night, 'stroke-width': 9, 'paint-order': 'stroke' });
  var lab0 = txt(svg, 0, 0, 'rechaza', { 'font-size': 30, 'font-weight': 700, fill: C.azure, 'text-anchor': 'middle', stroke: C.night, 'stroke-width': 9, 'paint-order': 'stroke' });
  var panel = H('div', 'col', wrap); panel.style.gap = '14px';
  var vals = { w1: 0.3, w2: 1.0, b: -0.2 };
  var defs = [['w1', 'w₁ ingreso', -2, 2], ['w2', 'w₂ atrasos', -2, 2], ['b', 'b sesgo', -1.5, 1.5]], outs = {}, ins = {};
  defs.forEach(function (d) {
    var r = H('div', 'ctrl', panel); r.style.gridTemplateColumns = '1fr auto'; r.style.rowGap = '2px';
    H('label', '', r, d[1]);
    var i = H('input', '', r); i.type = 'range'; i.min = d[2]; i.max = d[3]; i.step = 0.05; i.value = vals[d[0]]; i.setAttribute('aria-label', d[1]);
    var o = H('output', '', r); r.insertBefore(o, i); i.style.gridColumn = '1 / 3';
    i.addEventListener('input', function () { vals[d[0]] = +i.value; draw(); });
    ins[d[0]] = i; outs[d[0]] = o;
  });
  var score = H('div', 'big', panel); score.style.margin = '10px 0 4px';
  var btns = H('div', 'col', panel); btns.style.gap = '10px';
  var best = H('button', 'btn', btns, 'Buscar la mejor línea'); best.type = 'button';
  var reset = H('button', 'btn', btns, 'Reiniciar'); reset.type = 'button';
  function draw() {
    var w1 = vals.w1, w2 = vals.w2, b = vals.b;
    for (var k in outs) { outs[k].textContent = f(vals[k], 2); ins[k].value = vals[k]; }
    var rect = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
    var A = halfPlane(rect, w1, w2, b), B = halfPlane(rect, -w1, -w2, -b);
    zoneA.setAttribute('points', poly(A.map(function (p) { return [sx(p[0]), sy(p[1])]; })));
    zoneB.setAttribute('points', poly(B.map(function (p) { return [sx(p[0]), sy(p[1])]; })));
    var seg = lineInRect(w1, w2, b, -1, -1, 1, 1);
    if (seg) { ln.setAttribute('x1', sx(seg[0][0])); ln.setAttribute('y1', sy(seg[0][1])); ln.setAttribute('x2', sx(seg[1][0])); ln.setAttribute('y2', sy(seg[1][1])); ln.style.display = ''; } else ln.style.display = 'none';
    var ok = 0;
    P.forEach(function (p) { var pred = w1 * p.x + w2 * p.y + b >= 0 ? 1 : 0, good = pred === p.c; ok += good; p.ring.setAttribute('opacity', good ? 0 : 1); });
    if (seg) {
      var mx = (seg[0][0] + seg[1][0]) / 2, my = (seg[0][1] + seg[1][1]) / 2, nn = Math.hypot(w1, w2) || 1, ux = w1 / nn, uy = w2 / nn, d = 0.22;
      lab1.setAttribute('x', sx(clamp(mx + ux * d, -0.85, 0.85))); lab1.setAttribute('y', sy(clamp(my + uy * d, -0.9, 0.9)) + 10);
      lab0.setAttribute('x', sx(clamp(mx - ux * d, -0.85, 0.85))); lab0.setAttribute('y', sy(clamp(my - uy * d, -0.9, 0.9)) + 10);
    }
    lab1.style.display = A.length > 2 && seg ? '' : 'none'; lab0.style.display = B.length > 2 && seg ? '' : 'none';
    score.innerHTML = 'Aciertos: <b class="num ' + (ok === P.length ? 'mi' : 'am') + '">' + ok + ' de ' + P.length + '</b>' + (ok === P.length ? ' <span class="chip ok">¡todos!</span>' : '');
  }
  function animateTo(t) {
    var s = { w1: vals.w1, w2: vals.w2, b: vals.b };
    tween(900, function (k) { for (var q in t) vals[q] = s[q] + (t[q] - s[q]) * k; draw(); });
  }
  best.onclick = function () { animateTo({ w1: 1.3, w2: -1.5, b: 0.05 }); };
  reset.onclick = function () { animateTo({ w1: 0.3, w2: 1.0, b: -0.2 }); };
  draw();
  return { final: function () { vals = { w1: 1.3, w2: -1.5, b: 0.05 }; draw(); } };
});

/* ---------------- act: the same z through step, sigmoid and ReLU ---------------- */
demo('act', function (el) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%'; wrap.style.gap = '18px';
  var row = H('div', '', wrap); row.style.cssText = 'display:grid;grid-template-columns:repeat(3,1fr);gap:22px;flex:1;min-height:0';
  var defs = [
    { n: 'Escalón', an: 'un interruptor', fn: function (z) { return z >= 0 ? 1 : 0; }, lo: -0.15, hi: 1.25, out: function (v) { return f(v, 0); }, d: 'Solo 0 o 1: sí o no.' },
    { n: 'Sigmoide', an: 'un regulador de luz', fn: sig, lo: -0.15, hi: 1.25, out: function (v) { return f(v, 3); }, d: 'Entre 0 y 1: una probabilidad.' },
    { n: 'ReLU', an: 'una válvula', fn: function (z) { return Math.max(0, z); }, lo: -0.8, hi: 6.5, out: function (v) { return f(v, 2); }, d: 'Si es negativo, 0; si no, pasa igual.' }
  ];
  var z = 2.81, items = [];
  defs.forEach(function (d) {
    var card = H('div', 'plate', row); card.style.cssText += ';display:flex;flex-direction:column;padding:18px 20px 16px;gap:6px';
    H('div', '', card, '<b style="font-size:1.3em">' + d.n + '</b> <span class="mu">· ' + d.an + '</span>');
    var fg = H('div', 'fig', card); fg.style.flex = '1';
    var W = 440, Hh = 290, x0 = 30, x1 = 420, y0 = 14, y1 = 268;
    var svg = svgIn(fg, W, Hh, 'Función ' + d.n);
    var sx = lin(-6, 6, x0, x1), sy = lin(d.lo, d.hi, y1, y0);
    S('line', { x1: x0, y1: sy(0), x2: x1, y2: sy(0), stroke: C.line, 'stroke-width': 3 }, svg);
    S('line', { x1: sx(0), y1: y0, x2: sx(0), y2: y1, stroke: C.line, 'stroke-width': 3 }, svg);
    if (d.n === 'Escalón') S('path', { d: 'M' + x0 + ' ' + sy(0) + 'H' + sx(0) + 'M' + sx(0) + ' ' + sy(1) + 'H' + x1, stroke: C.amber, 'stroke-width': 7, fill: 'none', 'stroke-linecap': 'round' }, svg);
    else S('path', { d: pathOf(d.fn, -6, 6, sx, sy), stroke: C.amber, 'stroke-width': 7, fill: 'none', 'stroke-linecap': 'round' }, svg);
    var guide = S('line', { stroke: C.ink3, 'stroke-width': 2, 'stroke-dasharray': '6 6' }, svg);
    var dot = S('circle', { r: 13, fill: C.ink, stroke: C.night, 'stroke-width': 4 }, svg);
    var o = H('div', '', card); o.style.cssText = 'display:flex;justify-content:space-between;align-items:baseline';
    H('span', 'mu', o, d.d);
    var val = H('span', 'num', o); val.style.cssText = 'font-size:1.6em;font-weight:700;color:var(--amber)';
    items.push({ d: d, sx: sx, sy: sy, dot: dot, guide: guide, val: val });
  });
  var c = H('div', 'ctrl', wrap); c.style.gridTemplateColumns = '7em 1fr 5em';
  H('label', '', c, 'puntaje z');
  var inp = H('input', '', c); inp.type = 'range'; inp.min = -6; inp.max = 6; inp.step = 0.01; inp.value = z; inp.setAttribute('aria-label', 'puntaje z');
  var out = H('output', '', c);
  var pre = H('div', 'seg', wrap);
  [['socio A · z = 2.81', 2.81], ['z = 0', 0], ['z = −2.81', -2.81]].forEach(function (p) { var b = H('button', 'btn', pre, p[0]); b.type = 'button'; b.onclick = function () { go(p[1]); }; });
  function draw() {
    out.textContent = f(z, 2); inp.value = z;
    items.forEach(function (it) {
      var v = it.d.fn(z), cx = it.sx(z), cy = it.sy(Math.min(v, it.d.hi));
      it.dot.setAttribute('cx', cx); it.dot.setAttribute('cy', cy);
      it.guide.setAttribute('x1', cx); it.guide.setAttribute('y1', it.sy(0)); it.guide.setAttribute('x2', cx); it.guide.setAttribute('y2', cy);
      it.val.textContent = it.d.out(v);
    });
  }
  function go(t) { var s = z; tween(800, function (k) { z = s + (t - s) * k; draw(); }); }
  inp.addEventListener('input', function () { z = +inp.value; draw(); });
  draw();
  return {};
});

/* ---------------- sigmoid: from score to probability ---------------- */
demo('sigmoid', function (el) {
  var W = 1000, Hh = 600, x0 = 80, x1 = 960, y0 = 30, y1 = 520;
  var svg = svgIn(el, W, Hh, 'Curva sigmoide: puntajes negativos dan probabilidades cercanas a 0, z igual a 0 da 50 %, puntajes positivos se acercan a 100 %');
  var sx = lin(-6, 6, x0, x1), sy = lin(0, 1, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 98);
  [0, 0.5, 1].forEach(function (p) { txt(svg, x0 - 14, sy(p) + 8, (p * 100) + ' %', { 'text-anchor': 'end', 'font-size': 22, fill: C.ink3 }); });
  [-6, -3, 0, 3, 6].forEach(function (v) { txt(svg, sx(v), y1 + 40, (v < 0 ? '−' : '') + Math.abs(v), { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 }); });
  txt(svg, x1, y1 + 76, 'puntaje z →', { 'text-anchor': 'end', 'font-size': 23, fill: C.ink3 });
  axes(svg, x0, y0, x1, y1);
  S('path', { d: pathOf(sig, -6, 6, sx, sy), stroke: C.amber, 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round' }, svg);
  var pts = [[-2.81, '6 %'], [0, '50 %'], [2.81, '94 %']], marks = [];
  pts.forEach(function (p, i) {
    var g = S('g', { opacity: 0 }, svg), cx = sx(p[0]), cy = sy(sig(p[0]));
    S('line', { x1: cx, y1: cy, x2: cx, y2: y1, stroke: C.ink3, 'stroke-width': 2.5, 'stroke-dasharray': '7 7' }, g);
    S('line', { x1: x0, y1: cy, x2: cx, y2: cy, stroke: C.ink3, 'stroke-width': 2.5, 'stroke-dasharray': '7 7' }, g);
    S('circle', { cx: cx, cy: cy, r: 17, fill: C.ink, stroke: C.night, 'stroke-width': 5 }, g);
    var lx = i === 2 ? cx - 30 : cx + 34, ly = i === 0 ? cy + 10 : i === 1 ? cy + 44 : cy - 26, anchor = i === 2 ? 'end' : 'start';
    txt(g, lx, ly, 'z = ' + ['−2.81', '0', '2.81'][i] + '  →  ' + p[1], { 'text-anchor': anchor, 'font-size': 30, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
    marks.push(g);
  });
  return { step: function (s) { marks.forEach(function (g, i) { g.style.transition = 'opacity .5s'; g.setAttribute('opacity', s >= i + 1 ? 1 : 0); }); } };
});

/* ---------------- bend: without activation every stack is a line; with ReLU it bends ---------------- */
demo('bend', function (el) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
  var W = 1600, Hh = 560, x0 = 80, x1 = 1540, y0 = 40, y1 = 470;
  var svg = svgIn(fg, W, Hh, 'Curva que queremos aprender y la aproximación de la red');
  var target = function (t) { return 0.35 + 0.22 * Math.sin((t - 6) / 24 * 2 * Math.PI) + 0.38 * Math.exp(-Math.pow(t - 19, 2) / 5) + 0.18 * Math.exp(-Math.pow(t - 8, 2) / 3); };
  var sx = lin(0, 24, x0, x1), sy = lin(0, 1.05, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 86);
  axes(svg, x0, y0, x1, y1);
  [0, 6, 12, 18, 24].forEach(function (h) { txt(svg, sx(h), y1 + 42, h + ' h', { 'text-anchor': 'middle', 'font-size': 28, fill: C.ink3 }); });
  S('path', { d: pathOf(target, 0, 24, sx, sy), stroke: C.ink2, 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '10 10' }, svg);
  txt(svg, sx(19) + 34, sy(target(19)) - 10, 'lo que queremos aprender', { 'font-size': 30, fill: C.ink2 });
  var fit = S('path', { stroke: C.amber, 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg);
  var gK = S('g', {}, svg);
  var T = range(97).map(function (i) { return i / 4; }), Y = T.map(target);
  function solve(K) {
    var knots = range(K).map(function (i) { return 24 * (i + 0.5) / K; });
    var phi = function (t) { return [1, t / 24].concat(knots.map(function (k) { return Math.max(0, t - k) / 24; })); };
    var M = phi(0).length, A = range(M).map(function () { return range(M).map(function () { return 0; }); }), bb = range(M).map(function () { return 0; });
    T.forEach(function (t, n) { var p = phi(t); for (var i = 0; i < M; i++) { bb[i] += p[i] * Y[n]; for (var j = 0; j < M; j++) A[i][j] += p[i] * p[j]; } });
    for (var i = 0; i < M; i++) A[i][i] += 1e-6;
    for (i = 0; i < M; i++) { var piv = i; for (var r = i + 1; r < M; r++) if (Math.abs(A[r][i]) > Math.abs(A[piv][i])) piv = r; var tmp = A[i]; A[i] = A[piv]; A[piv] = tmp; var tb = bb[i]; bb[i] = bb[piv]; bb[piv] = tb; for (r = i + 1; r < M; r++) { var m = A[r][i] / A[i][i]; for (var c = i; c < M; c++) A[r][c] -= m * A[i][c]; bb[r] -= m * bb[i]; } }
    var x = range(M).map(function () { return 0; });
    for (i = M - 1; i >= 0; i--) { var s = bb[i]; for (var c2 = i + 1; c2 < M; c2++) s -= A[i][c2] * x[c2]; x[i] = s / A[i][i]; }
    var Yh = T.map(function (t) { var p = phi(t), s = 0; for (var i = 0; i < M; i++) s += p[i] * x[i]; return s; });
    var err = Yh.reduce(function (a, v, n) { return a + Math.pow(v - Y[n], 2); }, 0) / Yh.length;
    return { Yh: Yh, knots: knots, err: err };
  }
  var cur = T.map(function () { return 0.5; }), tw = null;
  var ctr = H('div', 'row', wrap); ctr.style.justifyContent = 'space-between';
  var seg = H('div', 'seg', ctr), info = H('div', 'big', ctr);
  var opts = [['Sin activación', 0], ['2 neuronas ReLU', 2], ['4', 4], ['8', 8], ['16', 16]], btns = [];
  opts.forEach(function (o) { var b = H('button', 'btn', seg, o[0]); b.type = 'button'; b.onclick = function () { set(o[1]); }; btns.push(b); });
  function render(Yh, knots) {
    fit.setAttribute('d', T.map(function (t, i) { return (i ? 'L' : 'M') + sx(t).toFixed(1) + ' ' + sy(clamp(Yh[i], -0.05, 1.1)).toFixed(1); }).join(''));
  }
  function set(K) {
    btns.forEach(function (b, i) { b.classList.toggle('on', opts[i][1] === K); });
    var r = solve(K), from = cur.slice();
    if (tw) tw.stop();
    gK.innerHTML = '';
    r.knots.forEach(function (k) { S('line', { x1: sx(k), y1: y1, x2: sx(k), y2: y1 - 16, stroke: C.amber, 'stroke-width': 4 }, gK); });
    tw = tween(900, function (q) { cur = from.map(function (v, i) { return v + (r.Yh[i] - v) * q; }); render(cur); });
    info.innerHTML = K === 0 ? 'Una línea recta, <b class="co">aunque apiles 100 capas</b>' : '<b class="am num">' + K + '</b> dobleces · error <b class="num">' + r.err.toFixed(4) + '</b>';
  }
  set(0);
  return { final: function () { set(8); } };
});
