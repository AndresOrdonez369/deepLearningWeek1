/* Demos · blocks 05-09 · networks (xor2, digit, playground, fwd221, chain, gears, vanish, clones, batches, race, trap, rank) */

/* ---------------- xor2: two neurons beat the staircase light ---------------- */
demo('xor2', function (el) {
  var W = 760, Hh = 640, x0 = 110, y0 = 50, x1 = 690, y1 = 560;
  var svg = svgIn(el, W, Hh, 'XOR resuelto con dos líneas: la franja entre ellas contiene las dos luces encendidas');
  var sx = lin(-0.25, 1.25, x0, x1), sy = lin(-0.25, 1.25, y1, y0);
  grid(S('g', {}, svg), x0, y0, x1, y1, 100);
  var R = [[-0.25, -0.25], [1.25, -0.25], [1.25, 1.25], [-0.25, 1.25]];
  var band = halfPlane(halfPlane(R, 1, 1, -0.5), -1, -1, 1.5);
  var gB = S('polygon', { points: poly(band.map(function (p) { return [sx(p[0]), sy(p[1])]; })), fill: C.amber, 'fill-opacity': 0, style: 'transition:fill-opacity .6s' }, svg);
  [[0, 1], [1, 0]].forEach(function (q) { S('circle', { cx: sx(q[0]), cy: sy(q[1]), r: 70, fill: glow(svg, C.amber), class: 'x2glow', opacity: 0, style: 'transition:opacity .6s' }, svg); });
  function L(c, col, label, lx, ly, anchor) {
    var s = lineInRect(1, 1, c, -0.25, -0.25, 1.25, 1.25);
    var g = S('g', {}, svg);
    var p = S('line', { x1: sx(s[0][0]), y1: sy(s[0][1]), x2: sx(s[1][0]), y2: sy(s[1][1]), stroke: col, 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
    var t = txt(g, lx, ly, label, { 'font-size': 34, 'font-weight': 700, fill: col, 'text-anchor': anchor || 'start', stroke: C.night, 'stroke-width': 8, 'paint-order': 'stroke' });
    var len = Math.hypot(sx(s[1][0]) - sx(s[0][0]), sy(s[1][1]) - sy(s[0][1]));
    p.style.strokeDasharray = len; p.style.strokeDashoffset = len; t.style.opacity = 0;
    return { p: p, t: t, len: len };
  }
  var A = L(-0.5, C.ink, '1', sx(-0.2), sy(0.62), 'middle'), B = L(-1.5, C.ink2, '2', sx(0.62), sy(1.19) - 4, 'middle');
  [[0, 0, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1]].forEach(function (p) {
    S('circle', { cx: sx(p[0]), cy: sy(p[1]), r: 26, fill: p[2] ? C.amber : C.azure, stroke: C.night, 'stroke-width': 5 }, svg);
  });
  txt(svg, sx(0.5), sy(0.5) + 10, 'encendida', { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: C.amber, opacity: 0, id: '' }).setAttribute('class', 'x2lab');
  var lab = svg.querySelector('.x2lab');
  function show(o, on) { o.p.style.transition = 'stroke-dashoffset .9s cubic-bezier(.16,1,.3,1)'; o.p.style.strokeDashoffset = on ? 0 : o.len; o.t.style.transition = 'opacity .5s'; o.t.style.opacity = on ? 1 : 0; }
  function set(s) { show(A, s >= 1); show(B, s >= 2); gB.setAttribute('fill-opacity', s >= 3 ? 0.1 : 0); lab.setAttribute('opacity', s >= 3 ? 1 : 0); [].forEach.call(svg.querySelectorAll('.x2glow'), function (c) { c.setAttribute('opacity', s >= 3 ? 1 : 0); }); }
  return { step: set, final: function () { set(3); } };
});

/* ---------------- digit: each layer builds richer clues ---------------- */
demo('digit', function (el) {
  var W = 1500, Hh = 600;
  var svg = svgIn(el, W, Hh, 'Un siete escrito a mano: la primera capa detecta trazos, la segunda formas y la salida reconoce el dígito');
  function tile(x, y, s, d, on) {
    var g = S('g', { transform: 'translate(' + x + ' ' + y + ')' }, svg);
    var r = S('rect', { width: s, height: s, rx: 18, fill: C.night2, stroke: C.line, 'stroke-width': 3 }, g);
    var p = S('path', { d: d, stroke: C.ink3, 'stroke-width': 10, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
    return { g: g, r: r, p: p, on: on };
  }
  var dg = S('g', { transform: 'translate(40 120)' }, svg);
  S('rect', { width: 340, height: 340, rx: 24, fill: C.night2, stroke: C.line, 'stroke-width': 3 }, dg);
  S('path', { d: 'M70 92 C120 84 200 80 268 86 C240 150 196 220 168 290', stroke: C.ink, 'stroke-width': 22, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, dg);
  S('path', { d: 'M150 196 L236 186', stroke: C.ink, 'stroke-width': 18, fill: 'none', 'stroke-linecap': 'round' }, dg);
  txt(svg, 210, 505, 'la imagen', { 'text-anchor': 'middle', fill: C.ink3, 'font-size': 24 });
  var s1 = [tile(500, 70, 130, 'M22 65 H108', 1), tile(650, 70, 130, 'M90 20 L40 110', 1), tile(500, 220, 130, 'M65 20 V110', 0), tile(650, 220, 130, 'M25 90 C40 30 90 30 105 90', 0), tile(575, 370, 130, 'M30 70 L100 60', 1)];
  txt(svg, 650, 560, 'capa 1 · trazos', { 'text-anchor': 'middle', fill: C.ink2, 'font-size': 26, 'font-weight': 600 });
  var s2 = [tile(900, 140, 150, 'M30 45 H115 L70 125', 1), tile(900, 320, 150, 'M40 40 V110 H115', 0)];
  txt(svg, 975, 560, 'capa 2 · formas', { 'text-anchor': 'middle', fill: C.ink2, 'font-size': 26, 'font-weight': 600 });
  var out = S('g', { transform: 'translate(1150 170)' }, svg), bars = [];
  [['7', 0.92], ['1', 0.05], ['4', 0.03]].forEach(function (b, i) {
    var y = i * 92;
    txt(out, 0, y + 44, b[0], { 'font-size': 46, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
    S('rect', { x: 50, y: y + 10, width: 260, height: 44, rx: 10, fill: C.night3 }, out);
    var r = S('rect', { x: 50, y: y + 10, width: 0, height: 44, rx: 10, fill: i ? C.ink3 : C.amber }, out);
    var t = txt(out, 320, y + 44, '', { 'font-size': 26, 'font-weight': 700, fill: i ? C.ink3 : C.amber, 'font-family': 'JetBrains Mono, monospace' });
    bars.push({ r: r, t: t, v: b[1] });
  });
  txt(svg, 1300, 560, 'salida', { 'text-anchor': 'middle', fill: C.ink2, 'font-size': 26, 'font-weight': 600 });
  var links = S('g', {}, svg);
  function lit(T, on) { T.forEach(function (t) { var o = on && t.on; t.r.setAttribute('stroke', o ? C.amber : C.line); t.p.setAttribute('stroke', o ? C.amber : C.ink3); t.g.style.opacity = on && !t.on ? 0.45 : 1; }); }
  function set(s) {
    lit(s1, s >= 1); lit(s2, s >= 2);
    bars.forEach(function (b) { var w = s >= 3 ? 260 * b.v : 0; b.r.style.transition = 'width .8s cubic-bezier(.16,1,.3,1)'; b.r.setAttribute('width', w); b.t.textContent = s >= 3 ? Math.round(b.v * 100) + ' %' : ''; });
    links.innerHTML = '';
    if (s >= 1) [[380, 290, 500, 135], [380, 290, 650, 135], [380, 290, 575, 435]].forEach(function (l) { S('line', { x1: l[0], y1: l[1], x2: l[2], y2: l[3], stroke: C.amber, 'stroke-width': 3, opacity: 0.5 }, links); });
    if (s >= 2) [[780, 135, 900, 215], [705, 435, 900, 215]].forEach(function (l) { S('line', { x1: l[0], y1: l[1], x2: l[2], y2: l[3], stroke: C.amber, 'stroke-width': 3, opacity: 0.5 }, links); });
    if (s >= 3) S('line', { x1: 1050, y1: 215, x2: 1150, y2: 202, stroke: C.amber, 'stroke-width': 3, opacity: 0.5 }, links);
  }
  set(0);
  return { step: set, final: function () { set(3); } };
});

/* ---------------- playground: a small network trained live in the browser ---------------- */
demo('playground', function (el, api) {
  var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:auto 19em;justify-content:center;gap:40px;height:100%';
  var box = H('div', 'plate', wrap); box.style.cssText += ';aspect-ratio:1/1;height:100%;max-height:100%';
  var cv = H('canvas', '', box); cv.width = 720; cv.height = 720; cv.setAttribute('role', 'img'); cv.setAttribute('aria-label', 'Frontera de decisión que aprende la red sobre los puntos');
  var g = cv.getContext('2d');
  var side = H('div', 'col', wrap); side.style.justifyContent = 'center';
  H('div', 'mu', side, 'Datos');
  var sData = H('div', 'seg', side);
  H('div', 'mu', side, 'Neuronas en la capa oculta');
  var sH = H('div', 'seg', side);
  var bRow = H('div', 'seg', side);
  var bPlay = H('button', 'btn primary', bRow, '▶ Entrenar'); bPlay.type = 'button';
  var bReset = H('button', 'btn', bRow, '↺'); bReset.type = 'button'; bReset.setAttribute('aria-label', 'Reiniciar');
  var rd = H('dl', 'readout', side); rd.style.marginTop = '8px';
  rd.innerHTML = '<dt>época</dt><dd data-r="ep">0</dd><dt>pérdida</dt><dd data-r="loss">—</dd><dt>exactitud</dt><dd data-r="acc">—</dd><dt>números que aprende</dt><dd data-r="par">—</dd>';
  var R = {}; [].forEach.call(rd.querySelectorAll('dd'), function (d) { R[d.dataset.r] = d; });
  var DATA = {}, rnd = seeded(31);
  function mk(name, gen) { var a = []; for (var i = 0; i < 220; i++) a.push(gen(i)); DATA[name] = a; }
  mk('XOR', function () { var x = rnd() * 2 - 1, y = rnd() * 2 - 1; if (Math.abs(x) < 0.08) x += 0.16 * Math.sign(x || 1); if (Math.abs(y) < 0.08) y += 0.16 * Math.sign(y || 1); return [x * 0.92, y * 0.92, x * y > 0 ? 0 : 1]; });
  mk('Círculos', function (i) { var r = i % 2 ? 0.15 + rnd() * 0.33 : 0.62 + rnd() * 0.3, t = rnd() * 6.283; return [r * Math.cos(t), r * Math.sin(t), i % 2 ? 1 : 0]; });
  mk('Lunas', function (i) { var t = rnd() * Math.PI, c = i % 2; var x = c ? 1 - Math.cos(t) : Math.cos(t), y = c ? 0.5 - Math.sin(t) : Math.sin(t); return [(x - 0.5) * 0.62 + gauss(rnd) * 0.06, (y - 0.25) * 0.75 + gauss(rnd) * 0.06, c]; });
  var ds = 'Círculos', Hn = 1, net = null, ep = 0, playing = false;
  function init() {
    var r = seeded(7 + Hn), s1 = Math.sqrt(1 / 2), s2 = Math.sqrt(1 / Hn);
    net = { W1: range(Hn).map(function () { return [gauss(r) * s1 * 1.5, gauss(r) * s1 * 1.5]; }), b1: range(Hn).map(function () { return gauss(r) * 0.3; }), W2: range(Hn).map(function () { return gauss(r) * s2; }), b2: 0 };
    net.m = zero(); net.v = zero(); net.t = 0; ep = 0;
    R.par.textContent = 4 * Hn + 1;
  }
  function zero() { return { W1: range(Hn).map(function () { return [0, 0]; }), b1: range(Hn).map(function () { return 0; }), W2: range(Hn).map(function () { return 0; }), b2: 0 }; }
  function fwd(x, y, keep) {
    var h = new Array(Hn), z = net.b2;
    for (var j = 0; j < Hn; j++) { h[j] = Math.tanh(net.W1[j][0] * x + net.W1[j][1] * y + net.b1[j]); z += net.W2[j] * h[j]; }
    var p = 1 / (1 + Math.exp(-z));
    return keep ? { h: h, p: p } : p;
  }
  function train(iters) {
    var D = DATA[ds], n = D.length, lr = 0.04, b1 = 0.9, b2 = 0.999;
    var loss = 0, acc = 0;
    for (var it = 0; it < iters; it++) {
      var G = zero(); loss = 0; acc = 0;
      for (var i = 0; i < n; i++) {
        var d = D[i], o = fwd(d[0], d[1], true), e = o.p - d[2];
        loss += -(d[2] * Math.log(o.p + 1e-9) + (1 - d[2]) * Math.log(1 - o.p + 1e-9));
        acc += (o.p >= 0.5 ? 1 : 0) === d[2] ? 1 : 0;
        G.b2 += e;
        for (var j = 0; j < Hn; j++) {
          G.W2[j] += e * o.h[j];
          var dh = e * net.W2[j] * (1 - o.h[j] * o.h[j]);
          G.W1[j][0] += dh * d[0]; G.W1[j][1] += dh * d[1]; G.b1[j] += dh;
        }
      }
      net.t++;
      var c1 = 1 - Math.pow(b1, net.t), c2 = 1 - Math.pow(b2, net.t);
      function upd(obj, key, gval, m, v) {
        gval /= n; m[key] = b1 * m[key] + (1 - b1) * gval; v[key] = b2 * v[key] + (1 - b2) * gval * gval;
        obj[key] -= lr * (m[key] / c1) / (Math.sqrt(v[key] / c2) + 1e-8);
      }
      upd(net, 'b2', G.b2, net.m, net.v);
      for (j = 0; j < Hn; j++) {
        upd(net.W2, j, G.W2[j], net.m.W2, net.v.W2); upd(net.b1, j, G.b1[j], net.m.b1, net.v.b1);
        upd(net.W1[j], 0, G.W1[j][0], net.m.W1[j], net.v.W1[j]); upd(net.W1[j], 1, G.W1[j][1], net.m.W1[j], net.v.W1[j]);
      }
      ep++;
    }
    return { loss: loss / n, acc: acc / n };
  }
  var AM = [255, 181, 65], AZ = [74, 186, 244], BG = [15, 26, 41];
  var img = g.createImageData(90, 90);
  var off = document.createElement('canvas'); off.width = 90; off.height = 90; var og = off.getContext('2d');
  function render(stats) {
    var k = 0;
    for (var py = 0; py < 90; py++) for (var px = 0; px < 90; px++) {
      var x = px / 89 * 2.2 - 1.1, y = 1.1 - py / 89 * 2.2, p = fwd(x, y), c = p >= 0.5 ? AM : AZ, a = Math.min(1, Math.abs(p - 0.5) * 2) * 0.55 + 0.08;
      img.data[k++] = BG[0] + (c[0] - BG[0]) * a; img.data[k++] = BG[1] + (c[1] - BG[1]) * a; img.data[k++] = BG[2] + (c[2] - BG[2]) * a; img.data[k++] = 255;
    }
    og.putImageData(img, 0, 0);
    g.imageSmoothingEnabled = true; g.drawImage(off, 0, 0, 720, 720);
    DATA[ds].forEach(function (d) {
      var X = (d[0] + 1.1) / 2.2 * 720, Y = (1.1 - d[1]) / 2.2 * 720;
      g.beginPath(); g.arc(X, Y, 9, 0, 6.283); g.fillStyle = d[2] ? C.amber : C.azure; g.fill(); g.lineWidth = 3.5; g.strokeStyle = C.night; g.stroke();
    });
    if (stats) { R.ep.textContent = ep; R.loss.textContent = stats.loss.toFixed(3); R.acc.textContent = Math.round(stats.acc * 100) + ' %'; R.acc.style.color = stats.acc > 0.97 ? C.mint : ''; }
  }
  var loop = api.raf(function () {
    var st = train(4); render(st);
    if (ep >= 2400 || st.loss < 0.03) { stop(); }
  });
  function play() { playing = true; bPlay.textContent = '❚❚ Pausa'; loop.start(); }
  function stop() { playing = false; bPlay.textContent = '▶ Entrenar'; loop.stop(); }
  function reset() { stop(); init(); render(train(0)); R.ep.textContent = 0; R.loss.textContent = '—'; R.acc.textContent = '—'; }
  function segBtns(parent, opts, getter, setter) {
    var bs = opts.map(function (o) { var b = H('button', 'btn', parent, String(o)); b.type = 'button'; b.onclick = function () { setter(o); bs.forEach(function (x, i) { x.classList.toggle('on', opts[i] === getter()); }); reset(); }; return b; });
    bs.forEach(function (x, i) { x.classList.toggle('on', opts[i] === getter()); });
  }
  segBtns(sData, ['XOR', 'Círculos', 'Lunas'], function () { return ds; }, function (v) { ds = v; });
  segBtns(sH, [1, 2, 4, 8], function () { return Hn; }, function (v) { Hn = v; });
  bPlay.onclick = function () { if (playing) stop(); else play(); };
  bReset.onclick = reset;
  reset();
  return { leave: stop, final: function () { Hn = 4; init(); render(train(600)); } };
});

/* ---------------- fwd221: the 2-2-1 network with numbers (forward, backward, update) ---------------- */
demo('fwd221', function (el, api) {
  var mode = el.dataset.mode || 'forward';
  var W = 1200, Hh = 580;
  var svg = svgIn(el, W, Hh, 'Red de dos entradas, dos neuronas ocultas y una salida con sus números');
  var N = { x1: [130, 170], x2: [130, 430], h1: [600, 170], h2: [600, 430], o: [1050, 300] };
  // [from, to, weight, label position along the edge, new value after one step]
  var E = [['x1', 'h1', '0.5', 0.3, '0.54'], ['x2', 'h1', '−0.3', 0.24, '−0.28'], ['x1', 'h2', '0.2', 0.24, '0.18'], ['x2', 'h2', '0.8', 0.3, '0.79'],
           ['h1', 'o', '0.7', 0.42, '0.84'], ['h2', 'o', '−0.4', 0.42, '−0.26']];
  var B = { h1: ['+0.1', '+0.14'], h2: ['−0.1', '−0.12'], o: ['+0.05', '+0.27'] };
  var gE = S('g', {}, svg), gP = S('g', {}, svg), gN = S('g', {}, svg), GL = glow(svg, C.amber);
  var edges = {};
  E.forEach(function (e) {
    var a = N[e[0]], b = N[e[1]], neg = e[2][0] === '−';
    var l = S('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: neg ? C.azure : C.amber, 'stroke-width': 5, 'stroke-opacity': 0.55 }, gE);
    var t = e[3], mx = a[0] + (b[0] - a[0]) * t, my = a[1] + (b[1] - a[1]) * t;
    var cg = S('g', {}, gE);
    S('rect', { x: mx - 50, y: my - 24, width: 100, height: 44, rx: 22, fill: C.night }, cg);
    var wt = txt(cg, mx, my + 9, e[2], { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: neg ? C.azure : C.amber, 'font-family': 'JetBrains Mono, monospace' });
    edges[e[0] + e[1]] = { l: l, a: a, b: b, t: wt, w0: e[2], w1: e[4], col: neg ? C.azure : C.amber };
  });
  var nodes = {};
  Object.keys(N).forEach(function (k) {
    var p = N[k], isIn = k[0] === 'x';
    var halo = S('circle', { cx: p[0], cy: p[1], r: 112, fill: GL, opacity: 0 }, gN);
    S('circle', { cx: p[0], cy: p[1], r: 66, fill: C.night2, stroke: C.ink3, 'stroke-width': 4 }, gN);
    var v = txt(gN, p[0], p[1] + 13, '', { 'text-anchor': 'middle', 'font-size': 38, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
    var sub = txt(gN, p[0], p[1] + 104, '', { 'text-anchor': 'middle', 'font-size': 25, fill: C.ink2 });
    var blame = txt(gN, p[0], p[1] - 88, '', { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: C.coral, 'font-family': 'JetBrains Mono, monospace' });
    var bias = null;
    if (B[k]) bias = txt(gN, p[0] + 74, p[1] + (k === 'h2' ? 82 : -58), 'b ' + B[k][0], { 'text-anchor': 'start', 'font-size': 24, 'font-weight': 600, fill: C.ink2, 'font-family': 'JetBrains Mono, monospace' });
    nodes[k] = { halo: halo, v: v, sub: sub, blame: blame, bias: bias };
  });
  nodes.x1.sub.textContent = 'antigüedad'; nodes.x2.sub.textContent = 'carga de la cuota';
  var pulses = [];
  function send(keys, color, back) {
    keys.forEach(function (k) { var e = edges[k], c = S('circle', { r: 12, fill: color }, gP); pulses.push({ e: e, c: c, t: 0, back: back }); });
    loop.start();
  }
  var loop = api.raf(function (t, dt) {
    for (var i = pulses.length - 1; i >= 0; i--) {
      var p = pulses[i]; p.t += dt / 700;
      if (p.t >= 1) { p.c.remove(); pulses.splice(i, 1); continue; }
      var a = p.back ? p.e.b : p.e.a, b = p.back ? p.e.a : p.e.b;
      p.c.setAttribute('cx', a[0] + (b[0] - a[0]) * p.t); p.c.setAttribute('cy', a[1] + (b[1] - a[1]) * p.t);
    }
    if (!pulses.length) return false;
  });
  function lit(k, a) { nodes[k].halo.setAttribute('opacity', Math.min(1, a * 4)); }
  function fwdState(s) {
    nodes.x1.v.textContent = s >= 1 ? '1.0' : ''; nodes.x2.v.textContent = s >= 1 ? '0.5' : '';
    nodes.h1.v.textContent = s >= 2 ? '0.61' : ''; nodes.h1.sub.textContent = s >= 2 ? 'z = 0.45' : '';
    nodes.h2.v.textContent = s >= 3 ? '0.62' : ''; nodes.h2.sub.textContent = s >= 3 ? 'z = 0.50' : '';
    nodes.o.v.textContent = s >= 4 ? '0.56' : ''; nodes.o.sub.textContent = s >= 4 ? 'z = 0.23' : '';
    lit('x1', s >= 1 ? 0.2 : 0); lit('x2', s >= 1 ? 0.12 : 0); lit('h1', s >= 2 ? 0.15 : 0); lit('h2', s >= 3 ? 0.15 : 0); lit('o', s >= 4 ? 0.14 : 0);
  }
  function params(updated) {
    Object.keys(edges).forEach(function (k) { var e = edges[k]; e.t.textContent = updated ? e.w1 : e.w0; e.t.setAttribute('fill', updated ? C.mint : e.col); });
    Object.keys(B).forEach(function (k) { nodes[k].bias.textContent = 'b ' + B[k][updated ? 1 : 0]; nodes[k].bias.setAttribute('fill', updated ? C.mint : C.ink2); });
  }
  var last = 0;
  function set(s, anim) {
    if (mode === 'forward') {
      fwdState(s); params(false);
      if (anim && !RM && s > last) { if (s === 2) send(['x1h1', 'x2h1'], C.amber); if (s === 3) send(['x1h2', 'x2h2'], C.amber); if (s === 4) send(['h1o', 'h2o'], C.amber); }
    } else if (mode === 'backward') {
      fwdState(4); params(false);
      nodes.o.blame.textContent = s >= 1 ? 'culpa −0.44' : '';
      edges.h1o.t.textContent = s >= 2 ? '−0.27' : '0.7'; edges.h2o.t.textContent = s >= 2 ? '−0.28' : '−0.4';
      edges.h1o.t.setAttribute('fill', s >= 2 ? C.coral : C.amber); edges.h2o.t.setAttribute('fill', s >= 2 ? C.coral : C.azure);
      nodes.h1.blame.textContent = s >= 3 ? '−0.07' : ''; nodes.h2.blame.textContent = s >= 3 ? '+0.04' : '';
      if (anim && !RM && s > last) { if (s === 2) send(['h1o', 'h2o'], C.coral, true); if (s === 3) send(['x1h1', 'x2h1', 'x1h2', 'x2h2'], C.coral, true); }
    } else {
      fwdState(4); params(s >= 1);
      nodes.o.v.textContent = s >= 2 ? '0.65' : '0.56'; nodes.o.v.setAttribute('fill', s >= 2 ? C.mint : C.ink);
      if (anim && !RM && s === 2 && last < 2) send(['x1h1', 'x2h1', 'x1h2', 'x2h2', 'h1o', 'h2o'], C.mint);
    }
    last = s;
  }
  return { enter: function (s) { last = s; set(s, false); }, step: function (s) { set(s, true); }, leave: function () { loop.stop(); }, final: function () { set(9, false); } };
});

/* ---------------- chain: the cacao chain and the blame that travels back ---------------- */
demo('chain', function (el, api) {
  var W = 1500, Hh = 400;
  var svg = svgIn(el, W, Hh, 'Cadena del cacao: cosecha, fermentado, tostado y barra; el error se descubre al final y la culpa viaja hacia atrás');
  var defs = S('defs', {}, svg), mk = S('marker', { id: 'chain-arr', viewBox: '0 0 10 10', refX: 6, refY: 5, markerWidth: 3.2, markerHeight: 3.2, orient: 'auto' }, defs);
  S('path', { d: 'M0 0 L10 5 L0 10 z', fill: C.coral }, mk);
  var st = [['Cosecha', 'poca culpa'], ['Fermentado', 'algo de culpa'], ['Tostado', 'mucha culpa'], ['Barra', 'aquí aparece el error']], xs = [150, 520, 890, 1230];
  var gL = S('g', {}, svg), gB = S('g', {}, svg);
  var boxes = st.map(function (s, i) {
    var g = S('g', {}, svg);
    var r = S('rect', { x: xs[i] - 130, y: 170, width: 260, height: 120, rx: 22, fill: C.night2, stroke: C.ink3, 'stroke-width': 4 }, g);
    txt(g, xs[i], 243, s[0], { 'text-anchor': 'middle', 'font-size': 34, 'font-weight': 600, fill: C.ink });
    var b = txt(g, xs[i], 340, '', { 'text-anchor': 'middle', 'font-size': 27, 'font-weight': 600, fill: C.coral });
    return { r: r, b: b, label: s[1] };
  });
  for (var i = 0; i < 3; i++) S('line', { x1: xs[i] + 130, y1: 230, x2: xs[i + 1] - 130, y2: 230, stroke: C.line, 'stroke-width': 5 }, gL);
  S('line', { x1: xs[3] + 130, y1: 230, x2: 1400, y2: 230, stroke: C.line, 'stroke-width': 5 }, gL);
  var bad = S('g', { opacity: 0 }, svg);
  S('circle', { cx: 1440, cy: 230, r: 40, fill: C.coral }, bad);
  txt(bad, 1440, 244, '!', { 'text-anchor': 'middle', 'font-size': 42, 'font-weight': 700, fill: C.night });
  txt(bad, 1440, 120, '«¡Está amarga!»', { 'text-anchor': 'end', 'font-size': 28, 'font-weight': 700, fill: C.coral, x: 1490 });
  var widths = [6, 12, 20];
  function set(s) {
    gB.innerHTML = '';
    boxes.forEach(function (b, i) { b.r.setAttribute('stroke', s >= 1 && s < 3 ? C.amber : s >= 3 ? C.coral : C.ink3); b.b.textContent = s >= 3 || (s >= 2 && i === 3) ? b.label : ''; });
    bad.setAttribute('opacity', s >= 2 ? 1 : 0);
    if (s >= 3) {
      var arcs = [];
      for (var i = 2; i >= 0; i--) {
        var xa = xs[i + 1], xb = xs[i], top = 166, peak = 40 + i * 10;
        arcs.push(S('path', { d: 'M' + xa + ' ' + top + ' Q ' + ((xa + xb) / 2) + ' ' + peak + ' ' + (xb + 20) + ' ' + (top - 4), stroke: C.coral, 'stroke-width': widths[i], fill: 'none', 'stroke-linecap': 'round', 'marker-end': 'url(#chain-arr)', opacity: 0.95 }, gB));
      }
      arcs.forEach(function (p, k) {
        var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = RM ? 0 : L;
        setTimeout(function () { tween(700, function (q) { p.style.strokeDashoffset = L * (1 - q); }); }, k * 420);
      });
    }
  }
  return { step: set, final: function () { set(3); } };
});

/* ---------------- gears: the chain rule multiplies ---------------- */
demo('gears', function (el, api) {
  var W = 1300, Hh = 600;
  var svg = svgIn(el, W, Hh, 'Engranajes: cuando A da una vuelta, B da tres y C da dieciocho');
  var gS = S('g', {}, svg);
  function gear(cx, cy, r, teeth, col) {
    var g = S('g', { transform: 'translate(' + cx + ' ' + cy + ')' }, svg), rot = S('g', {}, g), d = '', n = teeth * 2, th = Math.max(13, r * 0.12);
    for (var i = 0; i < n; i++) {
      var a = i / n * Math.PI * 2, a2 = (i + 1) / n * Math.PI * 2, rr = i % 2 ? r : r + th;
      d += (i ? 'L' : 'M') + (rr * Math.cos(a + 0.03)).toFixed(1) + ' ' + (rr * Math.sin(a + 0.03)).toFixed(1) + 'L' + (rr * Math.cos(a2 - 0.03)).toFixed(1) + ' ' + (rr * Math.sin(a2 - 0.03)).toFixed(1);
    }
    S('path', { d: d + 'Z', fill: C.night2, stroke: col, 'stroke-width': 5, 'stroke-linejoin': 'round' }, rot);
    S('circle', { r: Math.max(9, r * 0.2), fill: 'none', stroke: col, 'stroke-width': 5 }, rot);
    S('line', { x1: 0, y1: 0, x2: r * 0.78, y2: 0, stroke: col, 'stroke-width': 8, 'stroke-linecap': 'round' }, rot);
    return rot;
  }
  var ax = 240, ay = 300, bx = ax + 180 + 60 + 18, b2x = 860, cx = b2x + 150 + 25 + 18;
  S('line', { x1: bx, y1: ay, x2: b2x, y2: ay, stroke: C.ink3, 'stroke-width': 10, 'stroke-linecap': 'round', opacity: 0.55 }, gS);
  var mx = (bx + 78 + b2x - 168) / 2;
  S('line', { x1: mx, y1: ay + 14, x2: mx, y2: ay + 64, stroke: C.ink3, 'stroke-width': 2, 'stroke-dasharray': '4 5' }, svg);
  txt(svg, mx, ay + 96, 'mismo eje', { 'text-anchor': 'middle', 'font-size': 26, fill: C.ink2 });
  var A = gear(ax, ay, 180, 30, C.ink3), B = gear(bx, ay, 60, 10, C.ink2), B2 = gear(b2x, ay, 150, 36, C.ink2), Cg = gear(cx, ay, 25, 6, C.amber);
  txt(svg, ax, 560, 'A: 1 vuelta', { 'text-anchor': 'middle', 'font-size': 30, 'font-weight': 700, fill: C.ink2 });
  txt(svg, (bx + b2x) / 2, 560, 'B: 3 vueltas', { 'text-anchor': 'middle', 'font-size': 30, 'font-weight': 700, fill: C.ink });
  txt(svg, cx, 430, 'C: 18', { 'text-anchor': 'middle', 'font-size': 30, 'font-weight': 700, fill: C.amber });
  txt(svg, bx, 180, '× 3', { 'text-anchor': 'middle', 'font-size': 36, 'font-weight': 700, fill: C.ink });
  txt(svg, cx, 240, '× 6', { 'text-anchor': 'middle', 'font-size': 36, 'font-weight': 700, fill: C.ink });
  var th = 0;
  function pose() {
    var d = th * 57.2958;
    A.setAttribute('transform', 'rotate(' + d.toFixed(2) + ')');
    B.setAttribute('transform', 'rotate(' + (-3 * d).toFixed(2) + ')');
    B2.setAttribute('transform', 'rotate(' + (-3 * d).toFixed(2) + ')');
    Cg.setAttribute('transform', 'rotate(' + (18 * d).toFixed(2) + ')');
  }
  var loop = api.raf(function (t, dt) { th += dt / 1000 * (Math.PI * 2 / 36); pose(); });
  pose();
  return { enter: function () { if (!RM) loop.start(); }, leave: function () { loop.stop(); } };
});

/* ---------------- vanish: the signal that fades with sigmoids ---------------- */
demo('vanish', function (el, api) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
  var W = 1500, Hh = 440, n = 6;
  var svg = svgIn(fg, W, Hh, 'Seis capas en fila: la culpa viaja de derecha a izquierda y con sigmoide se encoge a la cuarta parte en cada capa');
  var xs = range(n).map(function (i) { return 160 + i * 236; }), y = 200, GLc = glow(svg, C.coral);
  S('line', { x1: xs[0], y1: y, x2: xs[n - 1], y2: y, stroke: C.line, 'stroke-width': 6 }, svg);
  var nodes = xs.map(function (x, i) {
    var h = S('circle', { cx: x, cy: y, r: 96, fill: GLc, opacity: 0 }, svg);
    S('circle', { cx: x, cy: y, r: 46, fill: C.night2, stroke: C.ink3, 'stroke-width': 4 }, svg);
    var c = S('circle', { cx: x, cy: y, r: 0, fill: C.coral }, svg);
    var t = txt(svg, x, y + 112, '', { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: C.coral, 'font-family': 'JetBrains Mono, monospace' });
    txt(svg, x, y - 86, i === n - 1 ? 'salida' : 'capa ' + (i + 1), { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 });
    return { h: h, c: c, t: t };
  });
  var dot = S('circle', { r: 0, fill: C.coral }, svg);
  var ctr = H('div', 'row', wrap); ctr.style.justifyContent = 'space-between';
  var seg = H('div', 'seg', ctr), msg = H('div', 'big', ctr);
  var k = 0.25, bs = [];
  [['Sigmoide · ×0.25', 0.25], ['ReLU · ×1', 1]].forEach(function (o) { var b = H('button', 'btn', seg, o[0]); b.type = 'button'; b.onclick = function () { k = o[1]; bs.forEach(function (x, i) { x.classList.toggle('on', i === (k === 1 ? 1 : 0)); }); labels(); t0 = 0; }; bs.push(b); });
  bs[0].classList.add('on');
  function mag(i) { return Math.pow(k, n - 1 - i); }
  function labels() {
    nodes.forEach(function (nd, i) { var m = mag(i); nd.t.textContent = m >= 0.01 ? m.toFixed(m >= 0.1 ? 2 : 3) : m.toFixed(4); nd.c.setAttribute('r', (8 + 30 * Math.sqrt(m)).toFixed(1)); });
    msg.innerHTML = k < 1 ? 'A la primera capa llega <b class="co num">0.001</b>: casi no aprende' : 'La culpa llega <b class="mi">entera</b> a todas las capas';
  }
  var t0 = 0, loop = api.raf(function (t, dt) {
    t0 += dt; var T = 2600, p = (t0 % T) / T, pos = (n - 1) * (1 - p), i = Math.floor(pos), fr = pos - i;
    var x = xs[Math.min(n - 1, i)] + (i < n - 1 ? (xs[i + 1] - xs[i]) * fr : 0);
    var m = Math.pow(k, (n - 1) - pos);
    dot.setAttribute('cx', x); dot.setAttribute('cy', y); dot.setAttribute('r', (6 + 22 * Math.sqrt(m)).toFixed(1));
    nodes.forEach(function (nd, j) { var near = Math.max(0, 1 - Math.abs(pos - j) * 1.5); nd.h.setAttribute('opacity', (near * Math.sqrt(mag(j))).toFixed(3)); });
  });
  labels();
  return { enter: function () { if (!RM) loop.start(); }, leave: function () { loop.stop(); } };
});

/* ---------------- clones: weights that start at zero learn the same thing ---------------- */
demo('clones', function (el, api) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
  var W = 1100, Hh = 560;
  var svg = svgIn(fg, W, Hh, 'Red con cuatro neuronas ocultas: si todas empiezan en cero quedan idénticas');
  var I = [[180, 160], [180, 280], [180, 400]], Hd = [[560, 100], [560, 220], [560, 340], [560, 460]], O = [940, 280];
  var gE = S('g', {}, svg), gN = S('g', {}, svg), ed = [];
  I.forEach(function (a, i) { Hd.forEach(function (b, j) { ed.push({ i: i, j: j, l: S('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], 'stroke-linecap': 'round' }, gE) }); }); });
  var out = Hd.map(function (b) { return S('line', { x1: b[0], y1: b[1], x2: O[0], y2: O[1], stroke: C.ink3, 'stroke-width': 4 }, gE); });
  I.forEach(function (p) { S('circle', { cx: p[0], cy: p[1], r: 34, fill: C.night2, stroke: C.ink3, 'stroke-width': 4 }, gN); });
  var hs = Hd.map(function (p) { return S('circle', { cx: p[0], cy: p[1], r: 42, fill: C.night2, stroke: C.ink3, 'stroke-width': 5 }, gN); });
  var hl = Hd.map(function (p) { return txt(gN, p[0] + 66, p[1] + 9, '', { 'font-size': 24, 'font-weight': 600, fill: C.ink2 }); });
  S('circle', { cx: O[0], cy: O[1], r: 42, fill: C.night2, stroke: C.ink3, 'stroke-width': 5 }, gN);
  var ctr = H('div', 'row', wrap); ctr.style.justifyContent = 'space-between';
  var seg = H('div', 'seg', ctr), msg = H('div', 'big', ctr), bs = [], mode = 'zero';
  var ideas = ['ingreso alto', 'muchos atrasos', 'cuota pesada', 'socio nuevo'], palette = [C.ink, C.ink, C.ink, C.ink];
  function draw() {
    var r = seeded(3);
    ed.forEach(function (e) {
      var w = mode === 'zero' ? 0.45 : (r() * 2 - 1);
      e.l.setAttribute('stroke', mode === 'zero' ? C.ink3 : w > 0 ? C.amber : C.azure);
      e.l.setAttribute('stroke-width', (2 + 6 * Math.abs(w)).toFixed(1)); e.l.setAttribute('stroke-opacity', mode === 'zero' ? 0.7 : (0.35 + 0.5 * Math.abs(w)).toFixed(2));
    });
    hs.forEach(function (h, j) { h.setAttribute('stroke', mode === 'zero' ? C.ink2 : palette[j]); h.setAttribute('fill', mode === 'zero' ? C.night3 : C.night2); });
    hl.forEach(function (t, j) { t.textContent = mode === 'zero' ? 'la misma idea' : ideas[j]; t.setAttribute('fill', mode === 'zero' ? C.ink3 : C.ink); });
    msg.innerHTML = mode === 'zero' ? '4 neuronas, <b class="co">1 sola idea</b> (clones)' : '4 neuronas, <b class="mi">4 ideas distintas</b>';
    bs.forEach(function (b, i) { b.classList.toggle('on', (i === 0) === (mode === 'zero')); });
  }
  [['Todos los pesos en cero', 'zero'], ['Al azar, bien escalados', 'rand']].forEach(function (o) { var b = H('button', 'btn', seg, o[0]); b.type = 'button'; b.onclick = function () { mode = o[1]; draw(); }; bs.push(b); });
  draw();
  return { step: function (s) { mode = s >= 1 ? 'rand' : 'zero'; draw(); }, final: function () { mode = 'rand'; draw(); } };
});

/* ---------------- batches: learning by survey, not census ---------------- */
demo('batches', function (el, api) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var box = H('div', 'plate', wrap); box.style.flex = '1';
  var cv = H('canvas', '', box); cv.width = 1600; cv.height = 840; cv.setAttribute('role', 'img'); cv.setAttribute('aria-label', 'Cuatro mil ochocientos socios como puntos; en cada paso se ilumina un lote de 32 al azar');
  var g = cv.getContext('2d'), cols = 96, rows = 50, n = 4800, cw = 1600 / cols, chh = 840 / rows;
  var rd = H('div', 'row', wrap); rd.style.justifyContent = 'space-between';
  var info = H('div', 'big', rd), seg = H('div', 'seg', rd);
  var bP = H('button', 'btn primary', seg, '▶ Entrenar'); bP.type = 'button';
  var used = new Uint8Array(n), order = [], batch = 0, epoch = 1, cur = [], acc = 0, playing = false;
  function shuffle() { order = range(n); for (var i = n - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = order[i]; order[i] = order[j]; order[j] = t; } used.fill(0); batch = 0; }
  function draw() {
    g.fillStyle = C.night2; g.fillRect(0, 0, 1600, 840);
    for (var i = 0; i < n; i++) {
      var x = (i % cols) * cw + cw / 2, y = Math.floor(i / cols) * chh + chh / 2;
      g.fillStyle = used[i] === 2 ? C.amber : used[i] === 1 ? '#3b4a60' : '#233044';
      g.beginPath(); g.arc(x, y, used[i] === 2 ? 6.5 : 4.5, 0, 6.283); g.fill();
    }
    info.innerHTML = 'Lote <b class="num am">' + batch + '</b> de 150 · <b class="num">' + batch + '</b> pasos · época <b class="num">' + epoch + '</b>';
  }
  function next() {
    cur.forEach(function (i) { used[i] = 1; });
    if (batch >= 150) { epoch++; shuffle(); }
    cur = order.slice(batch * 32, batch * 32 + 32); cur.forEach(function (i) { used[i] = 2; }); batch++;
    draw();
  }
  var loop = api.raf(function (t, dt) { acc += dt; if (acc > 110) { acc = 0; next(); } });
  bP.onclick = function () { if (playing) { playing = false; loop.stop(); bP.textContent = '▶ Entrenar'; } else { playing = true; loop.start(); bP.textContent = '❚❚ Pausa'; } };
  shuffle(); draw();
  return { step: function (s) { if (s >= 1 && !playing) bP.onclick(); }, leave: function () { playing = false; loop.stop(); bP.textContent = '▶ Entrenar'; }, final: function () { for (var i = 0; i < 40; i++) next(); } };
});

/* ---------------- race: SGD, momentum and Adam down a long narrow valley ---------------- */
demo('race', function (el, api) {
  var wrap = H('div', 'col', el); wrap.style.height = '100%';
  var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
  var W = 1400, Hh = 520, x0 = 40, x1 = 1360, y0 = 20, y1 = 500;
  var svg = svgIn(fg, W, Hh, 'Mapa de curvas de nivel de un valle largo y angosto con tres caminos de optimizadores');
  var sx = lin(-10.5, 1.5, x0, x1), sy = lin(-2.6, 2.6, y1, y0);
  var fx = function (x, y) { return 0.05 * x * x + 2 * y * y; };
  for (var lv = 0.15; lv < 7; lv *= 1.7) S('ellipse', { cx: sx(0), cy: sy(0), rx: Math.abs(sx(Math.sqrt(lv / 0.05)) - sx(0)), ry: Math.abs(sy(Math.sqrt(lv / 2)) - sy(0)), fill: 'none', stroke: C.line, 'stroke-width': 3 }, svg);
  S('circle', { cx: sx(0), cy: sy(0), r: 16, fill: C.mint }, svg);
  txt(svg, sx(0), sy(0) + 56, 'meta', { 'text-anchor': 'middle', fill: C.mint, 'font-weight': 700, 'font-size': 32 });
  var start = [-10, 2.2];
  S('circle', { cx: sx(start[0]), cy: sy(start[1]), r: 10, fill: C.ink3 }, svg);
  var R = [
    { n: 'SGD', col: C.ink3, st: function (p, s, g) { return [p[0] - 0.45 * g[0], p[1] - 0.45 * g[1]]; } },
    { n: 'Momentum', col: C.ink, st: function (p, s, g) { s.v = s.v || [0, 0]; s.v = [0.9 * s.v[0] - 0.06 * g[0], 0.9 * s.v[1] - 0.06 * g[1]]; return [p[0] + s.v[0], p[1] + s.v[1]]; } },
    { n: 'Adam', col: C.lilac, st: function (p, s, g) { s.m = s.m || [0, 0]; s.u = s.u || [0, 0]; s.t = (s.t || 0) + 1; var o = []; for (var i = 0; i < 2; i++) { s.m[i] = 0.9 * s.m[i] + 0.1 * g[i]; s.u[i] = 0.999 * s.u[i] + 0.001 * g[i] * g[i]; var mh = s.m[i] / (1 - Math.pow(0.9, s.t)), vh = s.u[i] / (1 - Math.pow(0.999, s.t)); o.push(p[i] - 0.25 * mh / (Math.sqrt(vh) + 1e-8)); } return o; } }
  ];
  R.forEach(function (r) {
    r.path = S('path', { fill: 'none', stroke: r.col, 'stroke-width': 5, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, svg);
    r.head = S('circle', { r: 14, fill: r.col, stroke: C.night, 'stroke-width': 4 }, svg);
    r.lab = txt(svg, 0, 0, r.n, { 'font-size': 34, 'font-weight': 700, fill: r.col, stroke: C.night2, 'stroke-width': 8, 'paint-order': 'stroke' });
  });
  var rd = H('div', 'row', wrap); rd.style.justifyContent = 'space-between';
  var info = H('div', 'legend', rd); var bR = H('button', 'btn', rd, '↺ Repetir la carrera'); bR.type = 'button';
  function sim() {
    R.forEach(function (r) {
      var p = start.slice(), s = {}; r.pts = [p]; r.done = 0;
      for (var k = 1; k <= 160; k++) { var g = [0.1 * p[0], 4 * p[1]]; p = r.st(p, s, g); r.pts.push(p); if (!r.done && Math.hypot(p[0], p[1]) < 0.3) r.done = k; }
    });
  }
  var k = 0, acc = 0;
  function render(n) {
    R.forEach(function (r, i) {
      var P = r.pts.slice(0, n + 1);
      r.path.setAttribute('d', P.map(function (p, j) { return (j ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(clamp(p[1], -2.6, 2.6)).toFixed(1); }).join(''));
      var h = P[P.length - 1]; r.head.setAttribute('cx', sx(h[0])); r.head.setAttribute('cy', sy(clamp(h[1], -2.6, 2.6)));
      r.lab.setAttribute('x', sx(h[0]) + 24); r.lab.setAttribute('y', sy(clamp(h[1], -2.6, 2.6)) + [-26, 50, -26][i] + (i === 2 ? -36 : 0)); r.lab.style.opacity = Math.hypot(h[0], h[1]) < 1.2 ? 0 : 1;
    });
    info.innerHTML = R.map(function (r) { var d = r.done && r.done <= n; return '<span><i style="background:' + r.col + '"></i>' + r.n + ': ' + (d ? '<b class="num">' + r.done + ' pasos</b>' : '<span class="mu">en camino…</span>') + '</span>'; }).join('');
  }
  var loop = api.raf(function (t, dt) { acc += dt; while (acc > 45) { acc -= 45; k++; } render(Math.min(k, 160)); if (k >= 160) return false; });
  function run() { k = 0; acc = 0; sim(); if (RM) { render(160); return; } loop.start(); }
  bR.onclick = run;
  sim(); render(0);
  return { enter: run, leave: function () { loop.stop(); }, final: function () { sim(); render(160); } };
});

/* ---------------- trap: 87 % accuracy that finds nobody ---------------- */
demo('trap', function (el, api) {
  var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:auto 1fr;gap:34px;height:100%;align-items:center';
  var fg = H('div', 'plate', wrap); fg.style.padding = '22px';
  var W = 640, Hh = 640;
  var svg = svgIn(fg, W, Hh, 'Cien socios; trece caen en mora');
  svg.style.width = '25em'; svg.style.height = '25em';
  var r = seeded(2), idx = range(100);   // seed 2: at threshold 0.5 → 10 TP, 3 FN, 8 FP, 79 TN (the guide's matrix)
  for (var i = 99; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
  var mora = {}; idx.slice(0, 13).forEach(function (k) { mora[k] = 1; });
  var D = range(100).map(function (k) {
    var m = !!mora[k], sc = m ? clamp(0.62 + gauss(r) * 0.17, 0.02, 0.98) : clamp(0.3 + gauss(r) * 0.16, 0.01, 0.97);
    var x = 40 + (k % 10) * 62, y = 40 + Math.floor(k / 10) * 62;
    return { m: m, sc: sc, ring: S('circle', { cx: x, cy: y, r: 27, fill: 'none', stroke: C.ink, 'stroke-width': 4, opacity: 0 }, svg), dot: S('circle', { cx: x, cy: y, r: 18, fill: C.ink3 }, svg) };
  });
  var side = H('div', 'col', wrap);
  var title = H('div', 'big', side);
  var rd = H('dl', 'readout', side); rd.style.fontSize = '1.25em';
  var ctr = H('div', 'ctrl', side); ctr.style.gridTemplateColumns = '7em 1fr 4em';
  H('label', '', ctr, 'umbral');
  var inp = H('input', '', ctr); inp.type = 'range'; inp.min = 0.05; inp.max = 0.95; inp.step = 0.01; inp.value = 0.5; inp.setAttribute('aria-label', 'umbral de riesgo');
  var out = H('output', '', ctr);
  var legend = H('div', 'legend', side, '<span><i style="background:' + C.amber + '"></i>cae en mora</span><span><i style="background:' + C.ink3 + '"></i>al día</span><span><i style="background:transparent;border:3px solid ' + C.ink + '"></i>el modelo lo marca</span>');
  var s = 0, th = 0.5;
  function stats(pred) {
    var tp = 0, fp = 0, fn = 0, tn = 0;
    D.forEach(function (d, k) { var p = pred(d); if (p && d.m) tp++; else if (p) fp++; else if (d.m) fn++; else tn++; });
    return { acc: (tp + tn) / 100, rec: tp / 13, prec: tp + fp ? tp / (tp + fp) : 0, tp: tp, fp: fp };
  }
  function draw() {
    D.forEach(function (d) { d.dot.setAttribute('fill', s >= 1 && d.m ? C.amber : C.ink3); });
    var st, pred;
    if (s < 2) { title.innerHTML = s >= 1 ? '<b class="am">13</b> de 100 socios caen en mora' : '100 socios de la cooperativa (ficticia)'; rd.innerHTML = ''; ctr.style.display = 'none'; D.forEach(function (d) { d.ring.setAttribute('opacity', 0); }); return; }
    if (s === 2) { pred = function () { return false; }; title.innerHTML = 'Modelo perezoso: <b>«todos están al día»</b>'; ctr.style.display = 'none'; }
    else { pred = function (d) { return d.sc >= th; }; title.innerHTML = 'Una red de verdad: marca a quien supera el umbral'; ctr.style.display = ''; }
    st = stats(pred);
    D.forEach(function (d) { d.ring.setAttribute('opacity', pred(d) ? 1 : 0); });
    rd.innerHTML = '<dt>exactitud</dt><dd class="' + (s === 2 ? 'am' : '') + '">' + Math.round(st.acc * 100) + ' %</dd><dt>morosos encontrados</dt><dd class="' + (st.tp ? 'mi' : 'co') + '">' + st.tp + ' de 13</dd>' + (s >= 3 ? '<dt>falsas alarmas</dt><dd>' + st.fp + '</dd>' : '');
    out.textContent = th.toFixed(2); inp.value = th;
  }
  inp.addEventListener('input', function () { th = +inp.value; draw(); });
  draw();
  return { step: function (n) { s = n; draw(); }, final: function () { s = 3; draw(); } };
});

/* ---------------- rank: AUC = how well the model orders the risk ---------------- */
demo('rank', function (el) {
  var W = 760, Hh = 640;
  var svg = svgIn(el, W, Hh, 'Dos listas de socios ordenadas por riesgo: el buen modelo pone a los morosos arriba; la moneda los reparte al azar');
  var r = seeded(9);
  function col(x, title, sub, order) {
    txt(svg, x, 38, title, { 'text-anchor': 'middle', 'font-size': 30, 'font-weight': 700, fill: C.ink });
    txt(svg, x, 74, sub, { 'text-anchor': 'middle', 'font-size': 26, fill: C.ink2 });
    order.forEach(function (m, i) { S('rect', { x: x - 120, y: 104 + i * 26, width: 240, height: 19, rx: 9, fill: m ? C.amber : C.night3 }, svg); });
  }
  var good = [1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  var coin = range(20).map(function (i) { return i; }).sort(function () { return r() - 0.5; }).map(function (i) { return good[i]; });
  col(150, 'Buen modelo', 'AUC ≈ 0.9', good);
  col(610, 'Moneda al aire', 'AUC = 0.5', coin);
  txt(svg, 380, 122, 'más riesgo', { 'text-anchor': 'middle', 'font-size': 24, fill: C.ink2 });
  txt(svg, 380, 630, 'menos riesgo', { 'text-anchor': 'middle', 'font-size': 24, fill: C.ink2 });
  S('path', { d: 'M380 142 V600 M366 582 L380 600 L394 582', stroke: C.ink3, 'stroke-width': 4, fill: 'none' }, svg);
  return {};
});
