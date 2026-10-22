/* Demos · blocks 03-04 · learning (perceptron, xor, mse, bce, mountain, slope, gdsteps, eta) */

/* ---------------- perceptron: learns error by error ---------------- */
demo('perceptron', function (el, api) {
  var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:1fr 15em;gap:28px;height:100%';
  var fg = H('div', 'fig plate', wrap);
  var W = 760, Hh = 680, x0 = 40, y0 = 40, x1 = 720, y1 = 640;
  var svg = svgIn(fg, W, Hh, 'Puntos de dos clases y la línea del perceptrón que se corrige con cada error');
  var sx = lin(-1, 1, x0, x1), sy = lin(-1, 1, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 85);
  var zA = S('polygon', { fill: C.amber, 'fill-opacity': 0.12 }, svg), zB = S('polygon', { fill: C.azure, 'fill-opacity': 0.12 }, svg);
  var ln = S('line', { stroke: C.ink, 'stroke-width': 6, 'stroke-linecap': 'round' }, svg);
  var rnd = seeded(21), P = [];
  while (P.length < 14) {
    var a = rnd() * 1.7 - 0.85, b = rnd() * 1.7 - 0.85, s = 0.9 * a + 1.1 * b - 0.1;
    if (Math.abs(s) < 0.35) continue;
    P.push({ x: a, y: b, y_: s > 0 ? 1 : -1 });
  }
  P.forEach(function (p) {
    p.ring = S('circle', { cx: sx(p.x), cy: sy(p.y), r: 27, fill: 'none', stroke: C.ink, 'stroke-width': 4, opacity: 0 }, svg);
    p.dot = S('circle', { cx: sx(p.x), cy: sy(p.y), r: 15, fill: p.y_ > 0 ? C.amber : C.azure, stroke: C.night, 'stroke-width': 4 }, svg);
  });
  var side = H('div', 'col', wrap); side.style.justifyContent = 'space-between';
  var top = H('div', 'col', side);
  var status = H('div', 'big', top, 'Línea al azar');
  var log = H('ol', 'steps-list', top); log.style.fontSize = '0.85em';
  var ctr = H('div', 'col', side); ctr.style.gap = '10px';
  var bPlay = H('button', 'btn primary', ctr, '▶ Entrenar'); bPlay.type = 'button';
  var bStep = H('button', 'btn', ctr, 'Un paso'); bStep.type = 'button';
  var bReset = H('button', 'btn', ctr, 'Reiniciar'); bReset.type = 'button';
  var w, b, i, epoch, errs, done, playing = false, timer = 0, lineTw = null, shown = { w: [0, 0], b: 0 };
  function reset() {
    w = [-0.7, 0.35]; b = 0.25; i = 0; epoch = 1; errs = 0; done = false;
    log.innerHTML = ''; status.textContent = 'Línea al azar'; status.className = 'big';
    P.forEach(function (p) { p.ring.setAttribute('opacity', 0); });
    show(true); stop();
  }
  function draw(ww, bb, learned) {
    var rect = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
    zA.setAttribute('points', poly(halfPlane(rect, ww[0], ww[1], bb).map(function (p) { return [sx(p[0]), sy(p[1])]; })));
    zB.setAttribute('points', poly(halfPlane(rect, -ww[0], -ww[1], -bb).map(function (p) { return [sx(p[0]), sy(p[1])]; })));
    var seg = lineInRect(ww[0], ww[1], bb, -1, -1, 1, 1);
    if (seg) { ln.setAttribute('x1', sx(seg[0][0])); ln.setAttribute('y1', sy(seg[0][1])); ln.setAttribute('x2', sx(seg[1][0])); ln.setAttribute('y2', sy(seg[1][1])); }
    ln.setAttribute('stroke', learned ? C.mint : C.ink);
  }
  function show(now) {
    var fw = shown.w.slice(), fb = shown.b, tw = w.slice(), tb = b;
    if (lineTw) lineTw.stop();
    if (now) { shown = { w: tw, b: tb }; draw(tw, tb, done); return; }
    lineTw = tween(380, function (k) { shown = { w: [fw[0] + (tw[0] - fw[0]) * k, fw[1] + (tw[1] - fw[1]) * k], b: fb + (tb - fb) * k }; draw(shown.w, shown.b, done); });
  }
  function one() {
    if (done) return;
    var p = P[i];
    P.forEach(function (q) { q.ring.setAttribute('opacity', 0); });
    var pred = w[0] * p.x + w[1] * p.y + b >= 0 ? 1 : -1;
    p.ring.setAttribute('opacity', 1);
    if (pred !== p.y_) {
      errs++; p.ring.setAttribute('stroke', C.coral);
      var eta = 0.5; w = [w[0] + eta * p.y_ * p.x, w[1] + eta * p.y_ * p.y]; b += eta * p.y_;
      status.innerHTML = '<span class="co">Se equivocó:</span> corrige la línea'; show(false);
    } else { p.ring.setAttribute('stroke', C.mint); status.innerHTML = '<span class="mi">Acertó:</span> no toca nada'; }
    i++;
    if (i === P.length) {
      var li = H('li', '', log, '<span class="k">' + epoch + '</span><span>Vuelta ' + epoch + ': <b class="' + (errs ? 'co' : 'mi') + '">' + errs + ' error' + (errs === 1 ? '' : 'es') + '</b></span>');
      if (errs === 0) { done = true; status.innerHTML = '<span class="mi">¡Aprendió! 0 errores</span>'; show(false); stop(); P.forEach(function (q) { q.ring.setAttribute('opacity', 0); }); return; }
      i = 0; errs = 0; epoch++;
      if (epoch > 8) { stop(); }
    }
  }
  function loop() { one(); if (playing && !done) timer = setTimeout(loop, RM ? 120 : 260); }
  function play() { if (done) reset(); playing = true; bPlay.textContent = '❚❚ Pausa'; loop(); }
  function stop() { playing = false; clearTimeout(timer); bPlay.textContent = '▶ Entrenar'; }
  bPlay.onclick = function () { if (playing) stop(); else play(); };
  bStep.onclick = function () { stop(); one(); };
  bReset.onclick = reset;
  reset();
  return {
    step: function (s) { if (s >= 1 && !playing && !done) play(); },
    leave: stop,
    final: function () { reset(); for (var k = 0; k < 200 && !done; k++) one(); show(true); }
  };
});

/* ---------------- xor: try to separate the staircase light with one line ---------------- */
demo('xor', function (el) {
  var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:1fr;gap:16px;height:100%';
  var fg = H('div', 'fig plate', wrap);
  var W = 760, Hh = 640, x0 = 110, y0 = 60, x1 = 690, y1 = 560;
  var svg = svgIn(fg, W, Hh, 'Cuatro puntos de XOR y una línea que se puede arrastrar: nunca separa los cuatro');
  var sx = lin(-0.25, 1.25, x0, x1), sy = lin(-0.25, 1.25, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 100);
  var zA = S('polygon', { fill: C.amber, 'fill-opacity': 0.13 }, svg), zB = S('polygon', { fill: C.azure, 'fill-opacity': 0.13 }, svg);
  var ln = S('line', { stroke: C.ink, 'stroke-width': 6, 'stroke-linecap': 'round' }, svg);
  txt(svg, sx(0), y1 + 44, 'abajo', { 'text-anchor': 'middle', fill: C.ink3 }); txt(svg, sx(1), y1 + 44, 'arriba', { 'text-anchor': 'middle', fill: C.ink3 });
  txt(svg, (x0 + x1) / 2, y1 + 78, 'interruptor 1', { 'text-anchor': 'middle', fill: C.ink2, 'font-weight': 600 });
  txt(svg, x0 - 16, sy(0) + 8, 'abajo', { 'text-anchor': 'end', fill: C.ink3 }); txt(svg, x0 - 16, sy(1) + 8, 'arriba', { 'text-anchor': 'end', fill: C.ink3 });
  txt(svg, x0 - 16, y0 - 20, 'interruptor 2', { 'text-anchor': 'start', fill: C.ink2, 'font-weight': 600, x: x0 - 90 });
  var P = [[0, 0, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1]];
  P.forEach(function (p) {
    p.ring = S('circle', { cx: sx(p[0]), cy: sy(p[1]), r: 38, fill: 'none', stroke: C.coral, 'stroke-width': 6, opacity: 0 }, svg);
    if (p[2]) S('circle', { cx: sx(p[0]), cy: sy(p[1]), r: 62, fill: glow(svg, C.amber) }, svg);
    S('circle', { cx: sx(p[0]), cy: sy(p[1]), r: 26, fill: p[2] ? C.amber : C.azure, stroke: C.night, 'stroke-width': 5 }, svg);
    txt(svg, sx(p[0]) + 40, sy(p[1]) - 30, p[2] ? 'encendida' : 'apagada', { 'font-size': 22, 'font-weight': 600, fill: p[2] ? C.amber : C.azure });
  });
  var h1 = { x: -0.15, y: 0.55 }, h2 = { x: 1.15, y: 0.75 };
  var g1 = S('circle', { r: 20, fill: C.ink, stroke: C.night, 'stroke-width': 5 }, svg), g2 = S('circle', { r: 20, fill: C.ink, stroke: C.night, 'stroke-width': 5 }, svg);
  var foot = H('div', 'row', wrap); foot.style.justifyContent = 'space-between';
  var score = H('div', 'big', foot);
  var bR = H('button', 'btn', foot, 'Probar 1 000 líneas al azar'); bR.type = 'button';
  function count(a, b, c) {
    var good = 0; P.forEach(function (p) { if ((a * p[0] + b * p[1] + c >= 0 ? 1 : 0) === p[2]) good++; });
    return good;
  }
  function draw() {
    var a = h1.y - h2.y, b = h2.x - h1.x, c = -(a * h1.x + b * h1.y);
    var good = count(a, b, c);
    if (good < 2) { a = -a; b = -b; c = -c; good = 4 - good; }
    var rect = [[-0.25, -0.25], [1.25, -0.25], [1.25, 1.25], [-0.25, 1.25]];
    zA.setAttribute('points', poly(halfPlane(rect, a, b, c).map(function (p) { return [sx(p[0]), sy(p[1])]; })));
    zB.setAttribute('points', poly(halfPlane(rect, -a, -b, -c).map(function (p) { return [sx(p[0]), sy(p[1])]; })));
    var seg = lineInRect(a, b, c, -0.25, -0.25, 1.25, 1.25);
    if (seg) { ln.setAttribute('x1', sx(seg[0][0])); ln.setAttribute('y1', sy(seg[0][1])); ln.setAttribute('x2', sx(seg[1][0])); ln.setAttribute('y2', sy(seg[1][1])); }
    g1.setAttribute('cx', sx(h1.x)); g1.setAttribute('cy', sy(h1.y)); g2.setAttribute('cx', sx(h2.x)); g2.setAttribute('cy', sy(h2.y));
    P.forEach(function (p) { p.ring.setAttribute('opacity', (a * p[0] + b * p[1] + c >= 0 ? 1 : 0) === p[2] ? 0 : 1); });
    score.innerHTML = 'Bien separados: <b class="num ' + (good === 4 ? 'mi' : 'co') + '">' + good + ' de 4</b>';
    return good;
  }
  var inv = function (p) { return { x: clamp(lin(x0, x1, -0.25, 1.25)(p.x), -0.25, 1.25), y: clamp(lin(y1, y0, -0.25, 1.25)(p.y), -0.25, 1.25) }; };
  drag(svg, g1, function (p) { h1 = inv(p); draw(); });
  drag(svg, g2, function (p) { h2 = inv(p); draw(); });
  bR.onclick = function () {
    var r = Math.random, n = 0, best = 0;
    (function burst() {
      for (var k = 0; k < 40; k++) { h1 = { x: -0.25, y: r() * 1.5 - 0.25 }; h2 = { x: 1.25, y: r() * 1.5 - 0.25 }; if (r() < 0.5) { h1 = { x: r() * 1.5 - 0.25, y: -0.25 }; h2 = { x: r() * 1.5 - 0.25, y: 1.25 }; } best = Math.max(best, draw()); n++; }
      if (n < 1000 && !RM) requestAnimationFrame(burst);
      else score.innerHTML = '1 000 líneas: la mejor separa <b class="num co">' + best + ' de 4</b>. Ninguna logra 4.';
    })();
  };
  draw();
  return {};
});

/* ---------------- mse: errors, squares and the average ---------------- */
demo('mse', function (el) {
  var W = 1000, Hh = 560, x0 = 90, x1 = 960, y0 = 40, y1 = 470;
  var svg = svgIn(el, W, Hh, 'Errores de cuatro casas y sus cuadrados: el error grande domina el promedio');
  var E = [10, 5, 20, 2], names = ['Casa 1', 'Casa 2', 'Casa 3', 'Casa 4'];
  var sy = lin(0, 420, y1, y0), bw = 70, gap = (x1 - x0) / 4;
  grid(S('g', {}, svg), x0, y0, x1, y1, 86);
  axes(svg, x0, y0, x1, y1);
  var bars = E.map(function (e, i) {
    var cx = x0 + gap * (i + 0.5);
    var g = S('g', {}, svg);
    var r1 = S('rect', { x: cx - bw - 6, width: bw, y: y1, height: 0, rx: 8, fill: C.azure }, g);
    var r2 = S('rect', { x: cx + 6, width: bw, y: y1, height: 0, rx: 8, fill: C.amber }, g);
    var t1 = txt(g, cx - bw / 2 - 6, y1 - 12, '', { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 700, fill: C.azure, 'font-family': 'JetBrains Mono, monospace' });
    var t2 = txt(g, cx + bw / 2 + 6, y1 - 12, '', { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 700, fill: C.amber, 'font-family': 'JetBrains Mono, monospace' });
    txt(g, cx, y1 + 40, names[i], { 'text-anchor': 'middle', 'font-size': 23, fill: C.ink2 });
    return { e: e, r1: r1, r2: r2, t1: t1, t2: t2 };
  });
  var avg = S('line', { x1: x0, x2: x1, y1: sy(132.25), y2: sy(132.25), stroke: C.ink, 'stroke-width': 4, 'stroke-dasharray': '12 10', opacity: 0 }, svg);
  var avgT = S('g', { opacity: 0 }, svg);
  txt(avgT, x1 - 8, sy(132.25) - 56, 'promedio', { 'text-anchor': 'end', 'font-size': 26, fill: C.ink2 });
  txt(avgT, x1 - 8, sy(132.25) - 18, 'MSE = 132.25', { 'text-anchor': 'end', 'font-size': 30, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
  var tw = [];
  function set(s) {
    tw.forEach(function (t) { t.stop(); }); tw = [];
    bars.forEach(function (b) {
      var h1 = s >= 1 ? y1 - sy(b.e * 4) : 0, h2 = s >= 2 ? y1 - sy(b.e * b.e) : 0;
      var c1 = +b.r1.getAttribute('height'), c2 = +b.r2.getAttribute('height');
      tw.push(tween(700, function (k) {
        var a = c1 + (h1 - c1) * k, c = c2 + (h2 - c2) * k;
        b.r1.setAttribute('height', a); b.r1.setAttribute('y', y1 - a); b.t1.setAttribute('y', y1 - a - 12);
        b.r2.setAttribute('height', c); b.r2.setAttribute('y', y1 - c); b.t2.setAttribute('y', y1 - c - 12);
      }));
      b.t1.textContent = s >= 1 ? b.e : ''; b.t2.textContent = s >= 2 ? b.e * b.e : '';
    });
    avg.setAttribute('opacity', s >= 3 ? 1 : 0); avgT.setAttribute('opacity', s >= 3 ? 1 : 0);
  }
  return { step: set, final: function () { set(3); } };
});

/* ---------------- bce: punishing false confidence ---------------- */
demo('bce', function (el) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
  var W = 1000, Hh = 520, x0 = 90, x1 = 960, y0 = 40, y1 = 430;
  var svg = svgIn(fg, W, Hh, 'Pérdida de entropía cruzada: crece muchísimo cuando el modelo estaba seguro y se equivocó');
  var sx = lin(0, 1, x0, x1), sy = lin(0, 5, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 87);
  axes(svg, x0, y0, x1, y1);
  [0, 25, 50, 75, 100].forEach(function (v) { txt(svg, sx(v / 100), y1 + 38, v + ' %', { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 }); });
  [0, 1, 2, 3, 4, 5].forEach(function (v) { txt(svg, x0 - 14, sy(v) + 8, v, { 'text-anchor': 'end', 'font-size': 22, fill: C.ink3 }); });
  txt(svg, x1, y1 + 74, 'probabilidad que el modelo le dio a «sí pagó» →', { 'text-anchor': 'end', 'font-size': 23, fill: C.ink3 });
  txt(svg, x0 + 10, y0 + 4, 'pérdida', { 'font-size': 23, fill: C.ink3 });
  S('path', { d: pathOf(function (p) { return -Math.log(p); }, 0.0068, 1, sx, sy), stroke: C.coral, 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round' }, svg);
  var gl = S('line', { stroke: C.ink3, 'stroke-width': 2.5, 'stroke-dasharray': '7 7' }, svg);
  var dot = S('circle', { r: 17, fill: C.ink, stroke: C.night, 'stroke-width': 5 }, svg);
  var lab = txt(svg, 0, 0, '', { 'font-size': 30, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
  var c = H('div', 'ctrl', wrap); c.style.gridTemplateColumns = '9.5em 1fr 4.5em';
  H('label', '', c, 'el modelo dijo');
  var inp = H('input', '', c); inp.type = 'range'; inp.min = 1; inp.max = 99; inp.step = 1; inp.value = 50; inp.setAttribute('aria-label', 'probabilidad');
  var out = H('output', '', c);
  var seg = H('div', 'seg', wrap);
  var msg = H('div', 'big', wrap);
  [[99, '99 %'], [50, '50 %'], [1, '1 %']].forEach(function (q) { var b = H('button', 'btn', seg, q[1]); b.type = 'button'; b.onclick = function () { go(q[0]); }; });
  var p = 50;
  function draw() {
    var pr = p / 100, L = -Math.log(pr), cx = sx(pr), cy = sy(L);
    dot.setAttribute('cx', cx); dot.setAttribute('cy', cy);
    gl.setAttribute('x1', cx); gl.setAttribute('x2', cx); gl.setAttribute('y1', cy); gl.setAttribute('y2', y1);
    lab.textContent = 'pérdida ' + L.toFixed(2);
    lab.setAttribute('x', cx + (pr > 0.6 ? -26 : 26)); lab.setAttribute('y', cy - 24); lab.setAttribute('text-anchor', pr > 0.6 ? 'end' : 'start');
    out.textContent = Math.round(p) + ' %'; inp.value = Math.round(p);
    msg.innerHTML = pr >= 0.9 ? '<b class="mi">Casi sin castigo:</b> estaba seguro y acertó.' : pr <= 0.1 ? '<b class="co">Castigo enorme:</b> estaba seguro… y se equivocó.' : 'Dudó: castigo moderado.';
  }
  function go(t) { var s = p; tween(800, function (k) { p = s + (t - s) * k; draw(); }); }
  inp.addEventListener('input', function () { p = +inp.value; draw(); });
  draw();
  return {};
});

/* ---------------- mountain: walking down Cotopaxi in the fog ---------------- */
demo('mountain', function (el, api) {
  var W = 1100, Hh = 640;
  var svg = svgIn(el, W, Hh, 'Silueta de un volcán con neblina y una persona que baja paso a paso hacia la laguna');
  var prof = function (x) { var u = (x - 560) / 330; return 560 - 430 * Math.exp(-u * u * 1.15) - 18 * Math.cos(x / 37); };
  var d = 'M0 ' + Hh; for (var x = 0; x <= W; x += 10) d += 'L' + x + ' ' + prof(x).toFixed(1); d += 'L' + W + ' ' + Hh + 'Z';
  var defs = S('defs', {}, svg);
  var gr = S('linearGradient', { id: 'mtn', x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
  S('stop', { offset: 0, 'stop-color': '#24324a' }, gr); S('stop', { offset: 1, 'stop-color': '#121c2c' }, gr);
  var bl = S('filter', { id: 'fogb', x: '-20%', y: '-50%', width: '140%', height: '200%' }, defs); S('feGaussianBlur', { stdDeviation: 18 }, bl);
  S('path', { d: d, fill: 'url(#mtn)' }, svg);
  var snow = 'M'; for (x = 430; x <= 690; x += 6) snow += (x === 430 ? '' : 'L') + x + ' ' + prof(x).toFixed(1);
  S('path', { d: snow + 'L650 ' + (prof(650) + 26) + 'L600 ' + (prof(600) + 14) + 'L560 ' + (prof(560) + 30) + 'L520 ' + (prof(520) + 12) + 'L470 ' + (prof(470) + 24) + 'Z', fill: C.ink, opacity: 0.85 }, svg);
  S('ellipse', { cx: 1010, cy: 600, rx: 80, ry: 14, fill: C.azure, opacity: 0.55 }, svg);
  txt(svg, 1010, 636, 'la laguna (pérdida mínima)', { 'text-anchor': 'middle', 'font-size': 21, fill: C.azure });
  var fogs = [0, 1, 2].map(function (i) { return S('ellipse', { cx: 300 + i * 320, cy: 260 + i * 70, rx: 260, ry: 46, fill: C.ink2, opacity: 0.14, filter: 'url(#fogb)' }, svg); });
  var trail = S('path', { d: '', fill: 'none', stroke: C.amber, 'stroke-width': 4, 'stroke-dasharray': '2 12', 'stroke-linecap': 'round' }, svg);
  var who = S('g', {}, svg);
  S('circle', { r: 24, fill: C.amber, opacity: 0.22 }, who);
  S('circle', { r: 13, fill: C.amber }, who);
  var arrow = S('path', { d: 'M0 0', stroke: C.amber, 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg);
  var xs = [640, 725, 800, 862, 912, 952, 985];
  var cur = xs[0], tw = null;
  function place(xx) {
    var y = prof(xx) - 16; who.setAttribute('transform', 'translate(' + xx + ' ' + y + ')');
    var dx = 46, y2 = prof(xx + dx) - 16;
    arrow.setAttribute('d', 'M' + (xx + 22) + ' ' + (y + 4) + 'L' + (xx + dx + 8) + ' ' + (y2 + 2) + 'M' + (xx + dx - 6) + ' ' + (y2 - 12) + 'L' + (xx + dx + 8) + ' ' + (y2 + 2) + 'L' + (xx + dx - 12) + ' ' + (y2 + 8));
  }
  function set(s) {
    var n = Math.min(s, xs.length - 1), t = xs[n], f0 = cur;
    var pts = xs.slice(0, n + 1).map(function (x) { return x + ' ' + (prof(x) - 16).toFixed(1); });
    trail.setAttribute('d', pts.length > 1 ? 'M' + pts.join('L') : '');
    if (tw) tw.stop();
    tw = tween(700, function (k) { cur = f0 + (t - f0) * k; place(cur); });
  }
  var loop = api.raf(function (t) { fogs.forEach(function (fg, i) { fg.setAttribute('cx', (300 + i * 320 + Math.sin(t / 4000 + i) * 60).toFixed(1)); }); });
  place(cur);
  return { enter: function (s) { set(s); if (!RM) loop.start(); }, leave: function () { loop.stop(); }, step: set, final: function () { set(xs.length - 1); } };
});

/* ---------------- slope: the slope tells where to go ---------------- */
demo('slope', function (el) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
  var W = 1000, Hh = 560, x0 = 80, x1 = 960, y0 = 30, y1 = 490;
  var svg = svgIn(fg, W, Hh, 'Parábola de pérdida con un punto que se puede mover, su pendiente y la dirección del paso');
  var L = function (w) { return (w - 3) * (w - 3); };
  var sx = lin(-1, 7, x0, x1), sy = lin(-0.5, 16.5, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 110);
  axes(svg, x0, y0, x1, y1);
  for (var v = -1; v <= 7; v++) txt(svg, sx(v), y1 + 38, (v < 0 ? '−' : '') + Math.abs(v), { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 });
  txt(svg, x1, y1 + 70, 'peso w →', { 'text-anchor': 'end', fill: C.ink3, 'font-size': 23 });
  txt(svg, x0 + 12, y0 + 18, 'pérdida', { fill: C.ink3, 'font-size': 23 });
  S('path', { d: pathOf(L, -1, 7, sx, sy), stroke: C.coral, 'stroke-width': 7, fill: 'none' }, svg);
  S('circle', { cx: sx(3), cy: sy(0), r: 10, fill: C.mint }, svg);
  txt(svg, sx(3), sy(0) - 22, 'mínimo', { 'text-anchor': 'middle', fill: C.mint, 'font-size': 22, 'font-weight': 600 });
  var tan = S('line', { stroke: C.ink, 'stroke-width': 4, 'stroke-dasharray': '12 8' }, svg);
  var arr = S('path', { stroke: C.amber, 'stroke-width': 7, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg);
  var hnd = S('circle', { r: 20, fill: C.ink, stroke: C.night, 'stroke-width': 5 }, svg);
  var lab = txt(svg, 0, 0, '', { 'font-size': 28, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
  var c = H('div', 'ctrl', wrap); c.style.gridTemplateColumns = '6em 1fr 4em';
  H('label', '', c, 'peso w');
  var inp = H('input', '', c); inp.type = 'range'; inp.min = -0.5; inp.max = 6.5; inp.step = 0.05; inp.value = 0.5; inp.setAttribute('aria-label', 'peso w');
  var out = H('output', '', c);
  var msg = H('div', 'big', wrap);
  var w = 0.5;
  function draw() {
    var y = L(w), m = 2 * (w - 3), cx = sx(w), cy = sy(y);
    hnd.setAttribute('cx', cx); hnd.setAttribute('cy', cy);
    var dw = 1.1; tan.setAttribute('x1', sx(w - dw)); tan.setAttribute('y1', sy(y - m * dw)); tan.setAttribute('x2', sx(w + dw)); tan.setAttribute('y2', sy(y + m * dw));
    var dir = m > 0.05 ? -1 : m < -0.05 ? 1 : 0, len = 110;
    arr.setAttribute('d', dir ? 'M' + cx + ' ' + (cy + 52) + 'h' + dir * len + 'm' + (-dir * 22) + ' -16l' + (dir * 22) + ' 16l' + (-dir * 22) + ' 16' : 'M0 0');
    lab.textContent = 'pendiente = ' + f(m, 1);
    lab.setAttribute('x', cx + (w > 3 ? -30 : 30)); lab.setAttribute('y', cy - 30); lab.setAttribute('text-anchor', w > 3 ? 'end' : 'start');
    out.textContent = f(w, 2); inp.value = w;
    msg.innerHTML = dir > 0 ? 'Pendiente <b class="co">negativa</b> → el peso <b class="am">sube</b> (paso a la derecha)' : dir < 0 ? 'Pendiente <b class="co">positiva</b> → el peso <b class="am">baja</b> (paso a la izquierda)' : '<b class="mi">Pendiente ≈ 0:</b> estás en el fondo';
  }
  drag(svg, hnd, function (p) { w = clamp(lin(x0, x1, -1, 7)(p.x), -0.5, 6.5); draw(); });
  inp.addEventListener('input', function () { w = +inp.value; draw(); });
  draw();
  return {};
});

/* ---------------- gdsteps: four steps by hand with eta = 0.1 ---------------- */
demo('gdsteps', function (el) {
  var W = 900, Hh = 560, x0 = 70, x1 = 860, y0 = 30, y1 = 490;
  var svg = svgIn(el, W, Hh, 'Parábola con una bola que baja en cuatro pasos y los pasos se acortan');
  var L = function (w) { return (w - 3) * (w - 3); };
  var sx = lin(-0.5, 6.5, x0, x1), sy = lin(-0.4, 10, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 113);
  axes(svg, x0, y0, x1, y1);
  for (var v = 0; v <= 6; v++) txt(svg, sx(v), y1 + 38, v, { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 });
  S('path', { d: pathOf(L, -0.2, 6.2, sx, sy), stroke: C.coral, 'stroke-width': 7, fill: 'none' }, svg);
  var ws = [0, 0.6, 1.08, 1.464, 1.7712], gT = S('g', {}, svg);
  var ball = S('circle', { r: 19, fill: C.amber, stroke: C.night, 'stroke-width': 5 }, svg), cur = 0, tw = null;
  function place(w) { ball.setAttribute('cx', sx(w)); ball.setAttribute('cy', sy(L(w)) - 19); }
  function set(s) {
    var n = Math.min(s, 4); gT.innerHTML = '';
    for (var i = 0; i < n; i++) S('path', { d: 'M' + sx(ws[i]) + ' ' + (sy(L(ws[i])) - 19) + 'Q' + (sx((ws[i] + ws[i + 1]) / 2)) + ' ' + (sy(L(ws[i])) - 90) + ' ' + sx(ws[i + 1]) + ' ' + (sy(L(ws[i + 1])) - 19), stroke: C.amber, 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '3 10', 'stroke-linecap': 'round' }, gT);
    var a = cur, b = ws[n]; if (tw) tw.stop();
    tw = tween(650, function (k) { cur = a + (b - a) * k; place(cur); });
  }
  place(0);
  return { step: set, final: function () { set(4); } };
});

/* ---------------- eta: the step size ---------------- */
demo('eta', function (el) {
  var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:1.45fr 1fr;grid-template-rows:1fr auto;gap:18px 24px;height:100%';
  var fg = H('div', 'fig plate', wrap);
  var W = 820, Hh = 560, x0 = 60, x1 = 790, y0 = 30, y1 = 500;
  var svg = svgIn(fg, W, Hh, 'Camino del descenso de gradiente sobre la parábola para el tamaño de paso elegido');
  var L = function (w) { return (w - 3) * (w - 3); };
  var sx = lin(-4, 10, x0, x1), sy = lin(-1, 50, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 104);
  axes(svg, x0, y0, x1, y1);
  S('path', { d: pathOf(L, -4, 10, sx, sy), stroke: C.coral, 'stroke-width': 6, fill: 'none' }, svg);
  var path = S('path', { stroke: C.amber, 'stroke-width': 4, fill: 'none', 'stroke-linejoin': 'round' }, svg);
  var gD = S('g', {}, svg);
  var fg2 = H('div', 'fig plate', wrap);
  var W2 = 520, H2 = 560, a0 = 60, a1 = 500, b0 = 40, b1 = 500;
  var svg2 = svgIn(fg2, W2, H2, 'Pérdida en cada paso');
  grid(S('g', {}, svg2), a0, b0, a1, b1, 92);
  axes(svg2, a0, b0, a1, b1);
  txt(svg2, a1, b1 + 40, 'pasos →', { 'text-anchor': 'end', fill: C.ink3, 'font-size': 22 });
  txt(svg2, a0 + 10, b0 + 4, 'pérdida', { fill: C.ink3, 'font-size': 22 });
  var curve = S('path', { stroke: C.amber, 'stroke-width': 5, fill: 'none', 'stroke-linejoin': 'round' }, svg2);
  var verdict = txt(svg2, (a0 + a1) / 2, b0 + 60, '', { 'text-anchor': 'middle', 'font-size': 34, 'font-weight': 700, fill: C.ink });
  var ctr = H('div', 'col', wrap); ctr.style.gridColumn = '1 / 3';
  var c = H('div', 'ctrl', ctr); c.style.gridTemplateColumns = '7.5em 1fr 4.5em';
  H('label', '', c, 'tamaño de paso η');
  var inp = H('input', '', c); inp.type = 'range'; inp.min = 0.01; inp.max = 1.1; inp.step = 0.01; inp.value = 0.4; inp.setAttribute('aria-label', 'tamaño de paso eta');
  var out = H('output', '', c);
  var seg = H('div', 'seg', ctr);
  [['muy corto · 0.02', 0.02], ['bien · 0.4', 0.4], ['muy largo · 1.02', 1.02]].forEach(function (q) { var b = H('button', 'btn', seg, q[0]); b.type = 'button'; b.onclick = function () { eta = q[1]; run(); }; });
  var eta = 0.4, tw = null;
  function run() {
    out.textContent = eta.toFixed(2); inp.value = eta;
    var w = 0, ws = [w];
    for (var i = 0; i < 24; i++) { w = w - eta * 2 * (w - 3); ws.push(w); }
    var maxL = Math.max(9, Math.min(60, L(ws[ws.length - 1])));
    var ty = lin(0, Math.max(10, maxL), b1, b0), tx = lin(0, 24, a0, a1);
    if (tw) tw.stop();
    tw = tween(1600, function (k) {
      var n = Math.max(1, Math.round(k * 24));
      path.setAttribute('d', ws.slice(0, n + 1).map(function (v, i) { return (i ? 'L' : 'M') + sx(clamp(v, -4, 10)).toFixed(1) + ' ' + sy(Math.min(L(v), 50)).toFixed(1); }).join(''));
      gD.innerHTML = '';
      ws.slice(0, n + 1).forEach(function (v, i) { if (i % (eta < 0.1 ? 3 : 1) === 0 || i === n) S('circle', { cx: sx(clamp(v, -4, 10)), cy: sy(Math.min(L(v), 50)), r: i === n ? 14 : 7, fill: i === n ? C.amber : C.ink2 }, gD); });
      curve.setAttribute('d', ws.slice(0, n + 1).map(function (v, i) { return (i ? 'L' : 'M') + tx(i).toFixed(1) + ' ' + ty(Math.min(L(v), Math.max(10, maxL))).toFixed(1); }).join(''));
    });
    var last = L(ws[24]);
    verdict.textContent = last > 9 ? 'Se pasa y diverge' : eta < 0.1 ? 'Lento: le faltan pasos' : eta > 0.9 ? 'Zigzaguea' : 'Llega rápido';
    verdict.setAttribute('fill', last > 9 ? C.coral : eta < 0.1 ? C.ink2 : C.mint);
  }
  inp.addEventListener('input', function () { eta = +inp.value; run(); });
  run();
  return {};
});
