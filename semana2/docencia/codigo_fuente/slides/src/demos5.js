/* Demos · iteration 3 · grade (your course grade is a neuron) · moons (arrays, fit, predict: real Keras data from NB02) */

/* ---------------- grade: Nota final = 0.267·S1 + 0.267·S2 + 0.267·S3 + 0.20·Final, compared with a bar of 70 ---------------- */
demo('grade', function (el, api) {
  var WT = [0.8 / 3, 0.8 / 3, 0.8 / 3, 0.2], NAMES = ['Semana 1', 'Semana 2', 'Semana 3', 'Entrega final'], BAR = 70;
  var ANA = [80, 70, 90, 60], BETO = [60, 55, 65, 70], ANA_JUSTO = [80, 70, 90, 30];
  var v = ANA.slice(), level = 0, tw = null, who = 'Ana', lastS = -1;
  var root = H('div', 'grade', el);
  var rows = H('div', 'g-rows', root);
  var hdr = H('div', 'g-row g-hdr', rows);
  ['', 'tu nota (x)', '', 'cuánto pesa (w)', 'aporta'].forEach(function (s) { H('span', '', hdr, s); });
  var ins = [], outs = [], cons = [];
  NAMES.forEach(function (n, i) {
    var r = H('div', 'g-row', rows);
    H('span', 'g-name', r, n);
    var inp = H('input', '', r); inp.type = 'range'; inp.min = 0; inp.max = 100; inp.step = 1; inp.value = v[i];
    inp.setAttribute('aria-label', 'Nota de ' + n);
    var o = H('output', 'g-val num', r);
    H('span', 'g-w num', r, '× ' + (i < 3 ? '0.267' : '0.20'));
    var c = H('span', 'g-c num', r);
    inp.addEventListener('input', function () { stop(); v[i] = +inp.value; who = ''; draw(); });
    ins.push(inp); outs.push(o); cons.push(c);
  });
  var W = 1000, Hh = 190, x0 = 24, x1 = 976, by = 64, bH = 62;
  var svg = svgIn(H('div', 'g-bar', root), W, Hh, 'Barra de la nota final comparada con una exigencia de 70');
  var sx = lin(0, 100, x0, x1);
  S('rect', { x: x0, y: by, width: x1 - x0, height: bH, rx: 14, fill: C.night3 }, svg);
  var segs = [0, 1, 2, 3].map(function () { return S('rect', { y: by, height: bH, stroke: C.night2, 'stroke-width': 5 }, svg); });
  [0, 50, 100].forEach(function (t) { txt(svg, sx(t), by + bH + 42, String(t), { 'text-anchor': 'middle', 'font-size': 24, fill: C.ink3, 'font-family': 'JetBrains Mono, monospace' }); });
  var th = S('g', {}, svg);
  S('line', { x1: sx(BAR), x2: sx(BAR), y1: by - 22, y2: by + bH + 14, stroke: C.ink, 'stroke-width': 5, 'stroke-dasharray': '10 7' }, th);
  txt(th, sx(BAR), by - 32, 'exigencia: 70 (ejemplo)', { 'text-anchor': 'middle', 'font-size': 25, 'font-weight': 600, fill: C.ink });
  var out = H('div', 'g-out', root);
  var btns = H('div', 'seg', root);
  var bA = H('button', 'btn', btns, 'Ana'), bB = H('button', 'btn', btns, 'Beto'), bN = H('button', 'btn', btns, '¿Cuánto necesita Ana en el final?');
  [bA, bB, bN].forEach(function (b) { b.type = 'button'; });
  bA.onclick = function () { go(ANA, 'Ana'); };
  bB.onclick = function () { go(BETO, 'Beto'); };
  bN.onclick = function () { if (level < 1) level = 1; go(ANA_JUSTO, 'Ana', 1600); };
  function total() { return v.reduce(function (s, x, i) { return s + x * WT[i]; }, 0); }
  function draw() {
    var t = total(), z = t - BAR, pass = z > -0.005, col = pass ? C.amber : C.azure, acc = 0;
    v.forEach(function (x, i) {
      var c = x * WT[i];
      ins[i].value = x; outs[i].textContent = Math.round(x);
      cons[i].textContent = '= ' + f(c, 1);
      segs[i].setAttribute('x', sx(acc)); segs[i].setAttribute('width', Math.max(0, sx(acc + c) - sx(acc)));
      segs[i].setAttribute('fill', col); segs[i].setAttribute('fill-opacity', 0.55 + 0.15 * i);
      acc += c;
    });
    th.style.opacity = level >= 1 ? 1 : 0;
    var name = who ? who + ': ' : '';
    if (level < 1) out.innerHTML = name + 'Nota final <b class="num">' + f(t, 1) + '</b>';
    else out.innerHTML = name + 'Nota final <b class="num">' + f(t, 1) + '</b> − 70 = <b class="num ' + (pass ? 'am' : 'az') + '">z = ' + fs(Math.abs(z) < 0.05 ? 0 : z, 1) + '</b> → ' +
      '<span class="verdict ' + (pass ? 'yes' : 'no') + '">' + (pass ? (Math.abs(z) < 0.05 ? 'Aprueba, justo' : 'Aprueba') : 'No aprueba') + '</span>';
    [bA, bB, bN].forEach(function (b) { b.classList.remove('on'); });
  }
  function stop() { if (tw) { tw.stop(); tw = null; } }
  function go(target, name, ms) {
    stop(); who = name;
    var from = v.slice();
    tw = tween(api.print ? 0 : (ms || 700), function (k) { v = from.map(function (a, i) { return a + (target[i] - a) * k; }); draw(); }, function () { v = target.slice(); draw(); });
  }
  draw();
  return {
    step: function (s) {
      level = s >= 1 ? 1 : 0;
      if (s === lastS) { draw(); return; }
      lastS = s;
      if (s >= 3) go(ANA_JUSTO, 'Ana', 1600);
      else if (s === 2) go(BETO, 'Beto');
      else go(ANA, 'Ana');
    },
    final: function () { level = 1; v = ANA_JUSTO.slice(); who = 'Ana'; draw(); }
  };
});

/* ---------------- moons: the NB02 network on the two moons (arrays · fit · predict) ---------------- */
(function () {
  var M = window.MOONS;
  if (!M) return;
  var SN = Object.keys(M.snaps).map(Number).sort(function (a, b) { return a - b; });
  var GRID = {};
  SN.forEach(function (k) { var s = M.snaps[k], a = new Float32Array(s.length); for (var i = 0; i < s.length; i++) a[i] = (s.charCodeAt(i) - 48) / 9; GRID[k] = a; });
  function probsAt(e) {           // blend the two snapshots around epoch e (fractional)
    var lo = SN[0], hi = SN[SN.length - 1];
    for (var i = 0; i < SN.length - 1; i++) if (e >= SN[i] && e <= SN[i + 1]) { lo = SN[i]; hi = SN[i + 1]; break; }
    if (e >= SN[SN.length - 1]) return GRID[hi];
    var t = hi === lo ? 0 : (e - lo) / (hi - lo), A = GRID[lo], B = GRID[hi], out = new Float32Array(A.length);
    for (var j = 0; j < A.length; j++) out[j] = A[j] + (B[j] - A[j]) * t;
    return out;
  }
  var AMB = [255, 181, 65], AZU = [74, 186, 244], BG = [15, 26, 41];
  function heatURL(P) {
    var cv = document.createElement('canvas'); cv.width = M.gx; cv.height = M.gy;
    var g = cv.getContext('2d'), im = g.createImageData(M.gx, M.gy);
    for (var i = 0; i < P.length; i++) {
      var p = P[i], c = p >= 0.5 ? AMB : AZU, a = Math.min(1, Math.abs(p - 0.5) * 2) * 0.3;
      im.data[i * 4] = BG[0] + (c[0] - BG[0]) * a; im.data[i * 4 + 1] = BG[1] + (c[1] - BG[1]) * a; im.data[i * 4 + 2] = BG[2] + (c[2] - BG[2]) * a; im.data[i * 4 + 3] = 255;
    }
    g.putImageData(im, 0, 0);
    return cv.toDataURL();
  }
  /* the 0.5 contour of the probability grid (marching squares) as an SVG path */
  function contour(P, sx, sy) {
    var gx = M.gx, gy = M.gy, b = M.box, d = '';
    function X(i) { return sx(b[0] + (b[1] - b[0]) * i / (gx - 1)); }
    function Y(j) { return sy(b[3] - (b[3] - b[2]) * j / (gy - 1)); }
    for (var j = 0; j < gy - 1; j++) for (var i = 0; i < gx - 1; i++) {
      var q = [P[j * gx + i], P[j * gx + i + 1], P[(j + 1) * gx + i + 1], P[(j + 1) * gx + i]];
      var pts = [], E = [[0, 1, i, j, i + 1, j], [1, 2, i + 1, j, i + 1, j + 1], [3, 2, i, j + 1, i + 1, j + 1], [0, 3, i, j, i, j + 1]];
      E.forEach(function (e) {
        var a = q[e[0]] - 0.5, c = q[e[1]] - 0.5;
        if ((a >= 0) !== (c >= 0)) { var t = a / (a - c); pts.push([X(e[2] + (e[4] - e[2]) * t), Y(e[3] + (e[5] - e[3]) * t)]); }
      });
      if (pts.length >= 2) d += 'M' + pts[0][0].toFixed(1) + ' ' + pts[0][1].toFixed(1) + 'L' + pts[1][0].toFixed(1) + ' ' + pts[1][1].toFixed(1);
      if (pts.length === 4) d += 'M' + pts[2][0].toFixed(1) + ' ' + pts[2][1].toFixed(1) + 'L' + pts[3][0].toFixed(1) + ' ' + pts[3][1].toFixed(1);
    }
    return d;
  }
  function plate(parent, label) {
    var W = 900, Hh = 640, b = M.box, x0 = 20, x1 = W - 20, y0 = 20, y1 = Hh - 20;
    var svg = svgIn(parent, W, Hh, label);
    var sx = lin(b[0], b[1], x0, x1), sy = lin(b[2], b[3], y1, y0);
    S('rect', { x: x0, y: y0, width: x1 - x0, height: y1 - y0, rx: 18, fill: C.night2 }, svg);
    var img = S('image', { x: x0, y: y0, width: x1 - x0, height: y1 - y0, preserveAspectRatio: 'none' }, svg);
    var cpath = S('path', { fill: 'none', stroke: C.ink, 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.9 }, svg);
    var gP = S('g', {}, svg);
    var dots = M.pts.map(function (p) { return S('circle', { cx: sx(p[0]), cy: sy(p[1]), r: 6.5, fill: p[2] ? C.amber : C.azure, stroke: C.night, 'stroke-width': 2 }, gP); });
    return { svg: svg, sx: sx, sy: sy, img: img, cpath: cpath, dots: dots, gP: gP,
      paint: function (P, line) { img.setAttribute('href', heatURL(P)); cpath.setAttribute('d', line ? contour(P, sx, sy) : ''); },
      clear: function () { img.removeAttribute('href'); cpath.setAttribute('d', ''); } };
  }

  demo('moons', function (el, api) {
    var mode = el.dataset.mode || 'fit';
    var wrap = H('div', 'moons m-' + mode, el);
    var left = H('div', 'fig', wrap);
    var P = plate(left, mode === 'arrays' ? 'Las lunas: 480 socios ficticios, cada uno un punto' : 'Frontera de decisión de la red sobre las lunas');

    if (mode === 'arrays') {
      var side = H('div', 'm-side', wrap);
      var tb = H('table', 'arr', side);
      tb.innerHTML = '<caption>Las primeras filas de la tabla</caption><thead><tr><th>fila</th><th>dato 1</th><th>dato 2</th><th>respuesta y</th></tr></thead>';
      var body = H('tbody', '', tb), trs = [];
      for (var i = 0; i < 6; i++) {
        var p = M.pts[i], tr = H('tr', '', body);
        tr.innerHTML = '<td class="num">' + i + '</td><td class="num">' + f(p[0], 2) + '</td><td class="num">' + f(p[1], 2) + '</td><td class="num ' + (p[2] ? 'am' : 'az') + '">' + p[2] + '</td>';
        tr.tabIndex = 0; tr.setAttribute('role', 'button'); tr.setAttribute('aria-label', 'Ver la fila ' + i + ' en el plano');
        (function (k) { tr.onclick = function () { auto = false; pick(k); }; tr.onkeydown = function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); auto = false; pick(k); } }; })(i);
        trs.push(tr);
      }
      H('p', 'm-shape', side, '<span class="num">X.shape → (' + M.n_train + ', 2)</span><span class="num">y.shape → (' + M.n_train + ',)</span>');
      var ring = S('circle', { r: 22, fill: 'none', stroke: C.ink, 'stroke-width': 5, opacity: 0 }, P.svg);
      var tag = txt(P.svg, 0, 0, '', { 'font-size': 28, 'font-weight': 700, fill: C.ink, stroke: C.night, 'stroke-width': 8, 'paint-order': 'stroke' });
      var cur = -1, auto = true, acc = 0;
      function pick(k) {
        cur = k; var p = M.pts[k];
        trs.forEach(function (t, j) { t.classList.toggle('on', j === k); });
        ring.setAttribute('cx', P.sx(p[0])); ring.setAttribute('cy', P.sy(p[1])); ring.setAttribute('opacity', 1);
        var lx = P.sx(p[0]) + 30, ly = P.sy(p[1]) - 26;
        tag.setAttribute('x', Math.min(lx, 640)); tag.setAttribute('y', Math.max(ly, 60)); tag.textContent = 'fila ' + k + ' → (' + f(p[0], 2) + ', ' + f(p[1], 2) + ')';
      }
      var loop = api.raf(function (t, dt) { if (!auto) return false; acc += dt; if (acc > 1700) { acc = 0; pick((cur + 1) % 6); } });
      return {
        enter: function () { pick(0); auto = !RM && !api.print; acc = 0; if (auto) loop.start(); },
        leave: function () { loop.stop(); },
        final: function () { pick(0); }
      };
    }

    if (mode === 'predict') {
      P.paint(GRID[60], true);
      P.dots.forEach(function (d) { d.setAttribute('opacity', 0.35); d.setAttribute('r', 5); });
      var NEW = M.nuevos.map(function (q, i) {
        var g = S('g', { 'data-step': i + 1 }, P.svg), p = M.pn[i], yes = p >= 0.5;
        var x = P.sx(q[0]), y = P.sy(q[1]);
        S('circle', { cx: x, cy: y, r: 30, fill: 'none', stroke: C.ink, 'stroke-width': 5 }, g);
        S('circle', { cx: x, cy: y, r: 15, fill: yes ? C.amber : C.azure, stroke: C.night, 'stroke-width': 4 }, g);
        var lbl = 'p = ' + p.toFixed(p < 0.01 || p > 0.99 ? 3 : 2) + ' → ' + (yes ? 1 : 0);
        txt(g, x + 42, y + 10, lbl, { 'font-size': 30, 'font-weight': 700, fill: yes ? C.amber : C.azure, stroke: C.night, 'stroke-width': 9, 'paint-order': 'stroke', 'font-family': 'JetBrains Mono, monospace' });
        return g;
      });
      return {};
    }

    /* fit: watch the boundary and the loss curves while Keras trains for 60 epochs */
    var right = H('div', 'm-side', wrap);
    var top = H('div', 'm-top', right);
    var ro = H('div', 'm-read', top);
    var CW = 760, CH = 360, cx0 = 90, cx1 = 730, cy0 = 30, cy1 = 296;
    var cs = svgIn(H('div', 'fig', right), CW, CH, 'Curvas de pérdida de entrenamiento y de validación por época');
    var ex = lin(0, 60, cx0, cx1), ey = lin(0, 0.65, cy1, cy0);
    grid(S('g', {}, cs), cx0, cy0, cx1, cy1, 74);
    axes(cs, cx0, cy0, cx1, cy1);
    [0, 20, 40, 60].forEach(function (e) { txt(cs, ex(e), cy1 + 34, String(e), { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3, 'font-family': 'JetBrains Mono, monospace' }); });
    [0, 0.2, 0.4, 0.6].forEach(function (l) { txt(cs, cx0 - 14, ey(l) + 8, l.toFixed(1), { 'text-anchor': 'end', 'font-size': 22, fill: C.ink3, 'font-family': 'JetBrains Mono, monospace' }); });
    txt(cs, cx1, cy1 + 62, 'época →', { 'text-anchor': 'end', 'font-size': 23, fill: C.ink3 });
    txt(cs, cx0, cy0 - 4, 'pérdida', { 'font-size': 23, fill: C.ink3 });
    var pT = S('path', { fill: 'none', stroke: C.amber, 'stroke-width': 6, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, cs);
    var pV = S('path', { fill: 'none', stroke: C.ink, 'stroke-width': 4, 'stroke-dasharray': '12 9', 'stroke-linecap': 'round' }, cs);
    var head = S('circle', { r: 10, fill: C.amber }, cs);
    S('line', { x1: cx1 - 330, x2: cx1 - 286, y1: cy0 + 22, y2: cy0 + 22, stroke: C.amber, 'stroke-width': 6, 'stroke-linecap': 'round' }, cs);
    txt(cs, cx1 - 274, cy0 + 30, 'entrenamiento (estudiar)', { 'font-size': 23, fill: C.ink2 });
    S('line', { x1: cx1 - 330, x2: cx1 - 286, y1: cy0 + 60, y2: cy0 + 60, stroke: C.ink, 'stroke-width': 4, 'stroke-dasharray': '10 7' }, cs);
    txt(cs, cx1 - 274, cy0 + 68, 'validación (el simulacro)', { 'font-size': 23, fill: C.ink2 });
    var bt = H('div', 'seg', top);
    var bRun = H('button', 'btn primary', bt, 'Entrenar 60 épocas'), bReset = H('button', 'btn', bt, 'Reiniciar');
    bRun.type = bReset.type = 'button';
    var ep = 0, playing = false;
    function curve(arr, last) {            // the curve up to epoch last + 1
      var d = '';
      for (var i = 0; i <= Math.min(last, 59); i++) d += (i ? 'L' : 'M') + ex(i + 1).toFixed(1) + ' ' + ey(Math.min(0.65, arr[i])).toFixed(1);
      return d;
    }
    function render(e) {
      ep = e;
      var n = Math.max(0, Math.min(60, Math.floor(e)));
      pT.setAttribute('d', n >= 1 ? curve(M.loss, n - 1) : '');
      pV.setAttribute('d', n >= 1 ? curve(M.val_loss, n - 1) : '');
      if (n >= 1) { head.setAttribute('cx', ex(n)); head.setAttribute('cy', ey(Math.min(0.65, M.loss[n - 1]))); head.style.display = ''; } else head.style.display = 'none';
      P.paint(probsAt(e), e > 0.2);
      var steps = Math.round(e * 12);
      ro.innerHTML = '<span>época <b class="num">' + n + '</b>/60</span><span>paso <b class="num">' + steps + '</b>/720</span>' +
        (n ? '<span>pérdida <b class="num am">' + M.loss[n - 1].toFixed(2) + '</b></span><span>simulacro <b class="num">' + Math.round(M.val_acc[n - 1] * 100) + ' %</b></span>' : '<span>pesos al azar: la red adivina</span>');
    }
    var loop = api.raf(function (t, dt) {
      if (!playing) return false;
      var e = ep + dt / 120;
      if (e >= 60) { e = 60; playing = false; }
      render(e);
      if (!playing) return false;
    });
    function play() { if (ep >= 60) render(0); if (RM || api.print) { render(60); return; } playing = true; loop.start(); }
    bRun.onclick = play;
    bReset.onclick = function () { playing = false; loop.stop(); render(0); };
    render(0);
    return {
      enter: function (s) { if (s >= 1 && ep === 0) play(); },
      step: function (s) { if (s >= 1 && ep === 0) play(); if (s === 0) { playing = false; render(0); } },
      leave: function () { playing = false; loop.stop(); },
      final: function () { playing = false; render(60); }
    };
  });
})();
