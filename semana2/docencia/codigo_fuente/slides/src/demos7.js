/* Demos · Semana 2 · sábado: secuencias, la libreta, el olvido, LSTM y atención (real data from NB04, window.SEQ) */
(function () {
  var Q = window.SEQ;
  function bar(parent, w, color) {
    var tr = H('span', '', parent); tr.style.cssText = 'display:block;height:1em;border-radius:99px;background:var(--night-3);overflow:hidden;position:relative';
    var i = H('i', '', tr); i.style.cssText = 'position:absolute;top:0;bottom:0;left:0;border-radius:99px;transition:width .6s cubic-bezier(.16,1,.3,1),background .3s;background:' + (color || C.amber) + ';width:' + w + '%';
    return i;
  }

  /* ---------------- orden: the same 12 months, in the opposite order (same average) ---------------- */
  demo('orden', function (el, api) {
    var A = Q.orden.ejemplo, B = A.slice().reverse(), mean = A.reduce(function (a, b) { return a + b; }, 0) / 12;
    var svg = svgIn(el, 1500, 600, 'Dos historiales de 12 meses con los mismos valores en orden contrario');
    function chart(x0, vals, col, title, sub) {
      var g = S('g', {}, svg), W = 640, y0 = 470, sy = lin(0, 26, y0, 90), bw = W / 12;
      txt(g, x0, 44, title, { 'font-size': 32, 'font-weight': 700, fill: col });
      txt(g, x0, 78, sub, { 'font-size': 22, fill: C.ink3 });
      S('line', { x1: x0, x2: x0 + W, y1: y0, y2: y0, stroke: C.line, 'stroke-width': 3 }, g);
      var rects = vals.map(function (v, i) {
        var r = S('rect', { x: x0 + i * bw + 6, width: bw - 12, y: y0, height: 0, rx: 6, fill: col }, g);
        txt(g, x0 + i * bw + bw / 2, y0 + 30, String(i + 1), { 'text-anchor': 'middle', 'font-size': 19, fill: C.ink3 });
        return { r: r, v: v, y: sy(v) };
      });
      txt(g, x0 + W / 2, y0 + 62, 'mes', { 'text-anchor': 'middle', 'font-size': 20, fill: C.ink3 });
      var ml = S('line', { x1: x0, x2: x0 + W, y1: sy(mean), y2: sy(mean), stroke: C.ink, 'stroke-width': 3, 'stroke-dasharray': '10 8', opacity: 0 }, g);
      var mt = txt(g, x0 + W, sy(mean) - 12, 'promedio ' + f(mean, 1) + ' días', { 'text-anchor': 'end', 'font-size': 22, 'font-weight': 600, fill: C.ink, opacity: 0 });
      return { g: g, rects: rects, ml: ml, mt: mt, y0: y0 };
    }
    var a = chart(40, A, C.coral, 'Socio A · empeora', 'días de atraso de cada mes'), b = chart(820, B, C.mint, 'Socio B · mejora', 'los mismos 12 números, al revés');
    function grow(ch, on) { ch.rects.forEach(function (o, i) { var y = on ? o.y : ch.y0; o.r.style.transition = 'y .7s cubic-bezier(.16,1,.3,1) ' + (i * 0.04) + 's, height .7s cubic-bezier(.16,1,.3,1) ' + (i * 0.04) + 's'; o.r.setAttribute('y', y); o.r.setAttribute('height', ch.y0 - y); }); }
    function set(s) { grow(a, s >= 1); grow(b, s >= 2); [a, b].forEach(function (ch) { ch.ml.setAttribute('opacity', s >= 3 ? 0.85 : 0); ch.mt.setAttribute('opacity', s >= 3 ? 1 : 0); }); b.g.style.opacity = s >= 2 ? 1 : 0.25; }
    set(0);
    return { step: set, final: function () { set(3); } };
  });

  /* ---------------- rnnread: the RNN reads word by word and updates its small notebook (illustrative numbers) ---------------- */
  var SENT = {
    neg: { w: ['el', 'servicio', 'no', 'fue', 'bueno'], h: [[0.10, 0.00, 0.05], [0.55, 0.00, 0.10], [0.50, -0.75, 0.05], [0.45, -0.70, 0.10], [0.40, -0.55, -0.80]], out: 'opinión negativa', c: 'co' },
    pos: { w: ['el', 'servicio', 'fue', 'muy', 'bueno'], h: [[0.10, 0.00, 0.05], [0.55, 0.00, 0.10], [0.50, 0.00, 0.15], [0.45, 0.10, 0.35], [0.40, 0.05, 0.85]], out: 'opinión positiva', c: 'mi' }
  };
  var SLOTS = ['¿de qué habla?', '¿hubo un «no»?', '¿bien o mal?'];
  demo('rnnread', function (el, api) {
    var cover = el.dataset.mode === 'cover', key = 'neg', k = 0, S0 = SENT[key];
    var G = cover ? { W: 860, H: 940, wy: 110, cx: 430, cy: 330, nx: 70, ny: 540, nw: 720, wmax: 300, lab: 250, out: 860 }
                  : { W: 1240, H: 500, wy: 56, cx: 250, cy: 275, nx: 480, ny: 170, nw: 740, wmax: 320, lab: 250, out: 420 };
    var svg = svgIn(el, G.W, G.H, 'Una red recurrente lee una frase palabra por palabra y actualiza su libreta');
    var gW = S('g', {}, svg);
    S('rect', { x: G.cx - 110, y: G.cy - 66, width: 220, height: 132, rx: 28, fill: C.night2, stroke: C.amber, 'stroke-width': 4 }, svg);
    txt(svg, G.cx, G.cy - 8, 'la misma', { 'text-anchor': 'middle', 'font-size': 27, fill: C.ink2 });
    txt(svg, G.cx, G.cy + 30, 'celda', { 'text-anchor': 'middle', 'font-size': 32, 'font-weight': 700, fill: C.ink });
    var arrowIn = S('path', { d: '', stroke: C.amber, 'stroke-width': 4, fill: 'none', opacity: 0.8 }, svg);
    S('rect', { x: G.nx, y: G.ny, width: G.nw, height: 196, rx: 22, fill: C.night2, stroke: C.line, 'stroke-width': 3 }, svg);
    txt(svg, G.nx + 20, G.ny - 16, 'la libreta (estado oculto h)', { 'font-size': 25, 'font-weight': 600, fill: C.ink2 });
    if (cover) {
      S('path', { d: 'M' + G.cx + ' ' + (G.cy + 66) + ' L' + G.cx + ' ' + (G.ny - 40), stroke: C.amber, 'stroke-width': 4 }, svg);
      S('path', { d: 'M' + (G.nx + G.nw) + ' ' + (G.ny + 98) + ' C' + (G.nx + G.nw + 60) + ' ' + (G.ny + 98) + ' ' + (G.cx + 200) + ' ' + G.cy + ' ' + (G.cx + 112) + ' ' + G.cy, stroke: C.lilac, 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '10 8' }, svg);
    } else {
      S('path', { d: 'M' + (G.cx + 110) + ' ' + G.cy + ' L' + (G.nx - 6) + ' ' + G.cy, stroke: C.amber, 'stroke-width': 4 }, svg);
      S('path', { d: 'M' + (G.nx + 60) + ' ' + (G.ny + 196) + ' C' + (G.nx + 60) + ' ' + (G.cy + 175) + ' ' + G.cx + ' ' + (G.cy + 175) + ' ' + G.cx + ' ' + (G.cy + 70), stroke: C.lilac, 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '10 8' }, svg);
      txt(svg, (G.nx + G.cx) / 2 + 40, G.cy + 168, 'vuelve a entrar con la palabra siguiente', { 'text-anchor': 'middle', 'font-size': 22, fill: C.lilac });
    }
    var slots = SLOTS.map(function (n, i) {
      var y = G.ny + 44 + i * 54;
      txt(svg, G.nx + 22, y + 8, n, { 'font-size': 24, fill: C.ink3 });
      var x0 = G.nx + G.lab;
      S('line', { x1: x0 + G.wmax / 2, x2: x0 + G.wmax / 2, y1: y - 18, y2: y + 18, stroke: C.line, 'stroke-width': 3 }, svg);
      var r = S('rect', { x: x0 + G.wmax / 2, y: y - 13, width: 0, height: 26, rx: 8, fill: C.amber }, svg);
      return { r: r, x0: x0 };
    });
    var outT = txt(svg, cover ? G.cx : G.nx + 20, G.ny + 196 + (cover ? 80 : 56), '', { 'font-size': 32, 'font-weight': 700, fill: C.ink, 'text-anchor': cover ? 'middle' : 'start' });
    var words = [];
    function layoutWords() {
      gW.innerHTML = ''; words = [];
      var tot = 0; S0.w.forEach(function (w) { tot += 36 + w.length * 19 + 16; });
      var x = (G.W - tot + 16) / 2;
      S0.w.forEach(function (w) {
        var g = S('g', {}, gW), wd = 36 + w.length * 19;
        var r = S('rect', { x: x, y: G.wy - 38, width: wd, height: 56, rx: 14, fill: C.night3, stroke: C.line, 'stroke-width': 2 }, g);
        var t = txt(g, x + wd / 2, G.wy, w, { 'text-anchor': 'middle', 'font-size': 29, fill: C.ink2, 'font-family': 'JetBrains Mono, monospace' });
        words.push({ r: r, t: t, cx: x + wd / 2 }); x += wd + 16;
      });
    }
    function draw(anim) {
      words.forEach(function (o, i) {
        var read = i < k, now = i === k - 1;
        o.r.setAttribute('fill', now ? C.amber : read ? C.night2 : C.night3); o.r.setAttribute('stroke', now ? C.amber : C.line);
        o.t.setAttribute('fill', now ? C.night : read ? C.ink3 : C.ink2);
      });
      var h = k ? S0.h[k - 1] : [0, 0, 0];
      slots.forEach(function (sl, i) {
        var v = h[i], w = Math.abs(v) * G.wmax / 2;
        sl.r.style.transition = anim ? 'width .6s cubic-bezier(.16,1,.3,1), x .6s cubic-bezier(.16,1,.3,1)' : 'none';
        sl.r.setAttribute('width', w); sl.r.setAttribute('x', v >= 0 ? sl.x0 + G.wmax / 2 : sl.x0 + G.wmax / 2 - w);
        sl.r.setAttribute('fill', i === 2 ? (v >= 0 ? C.mint : C.coral) : v >= 0 ? C.amber : C.azure);
      });
      if (k > 0) { var o = words[k - 1]; arrowIn.setAttribute('d', 'M' + o.cx + ' ' + (G.wy + 22) + ' C' + o.cx + ' ' + (G.wy + 90) + ' ' + G.cx + ' ' + (G.cy - 150) + ' ' + G.cx + ' ' + (G.cy - 70)); }
      else arrowIn.setAttribute('d', '');
      outT.textContent = k === S0.w.length ? '→ ' + S0.out : '';
      outT.setAttribute('fill', S0.c === 'co' ? C.coral : C.mint);
    }
    var bs = {};
    if (!cover) {
      var ctr = H('div', 'under', el);
      var b1 = H('button', 'btn primary', ctr, 'Leer la siguiente palabra'); b1.type = 'button';
      var b2 = H('button', 'btn', ctr, 'Reiniciar'); b2.type = 'button';
      var seg = H('div', 'seg', ctr);
      [['neg', '«el servicio no fue bueno»'], ['pos', '«el servicio fue muy bueno»']].forEach(function (o) { var b = H('button', 'btn', seg, o[1]); b.type = 'button'; b.onclick = function () { loop.stop(); choose(o[0]); }; bs[o[0]] = b; });
      b1.onclick = function () { loop.stop(); if (k < S0.w.length) { k++; draw(true); } };
      b2.onclick = function () { loop.stop(); k = 0; draw(true); };
      el.style.display = 'flex'; el.style.flexDirection = 'column'; svg.style.flex = '1'; svg.style.minHeight = '0';
    }
    function choose(kk) { key = kk; S0 = SENT[kk]; k = 0; layoutWords(); draw(false); for (var q in bs) bs[q].classList.toggle('on', q === kk); }
    var t0 = 0, loop = api.raf(function (t, dt) {
      t0 += dt;
      if (t0 > (k === S0.w.length ? 2600 : 1150)) { t0 = 0; if (k < S0.w.length) { k++; draw(true); } else if (cover) { choose(key === 'neg' ? 'pos' : 'neg'); } else return false; }
    });
    choose('neg');
    return {
      enter: function () { if (api.print) { k = S0.w.length; draw(false); return; } if (cover || !RM) { k = 0; draw(false); t0 = 0; loop.start(); } },
      leave: function () { loop.stop(); },
      final: function () { k = S0.w.length; draw(false); }
    };
  });

  /* ---------------- eco: the footprint of the first word fades step by step ---------------- */
  demo('eco', function (el, api) {
    var u = 0.5, n = 20;
    var wrap = H('div', 'col', el); wrap.style.cssText += ';height:100%;gap:1em';
    var fg = H('div', 'fig plate', wrap); fg.style.flex = '1';
    var svg = svgIn(fg, 1600, 400, 'Cuánto queda del primer dato en la libreta después de cada paso');
    var sx = lin(0.5, n + 0.5, 90, 1570), sy = lin(0, 0.8, 340, 36);
    [0, 0.2, 0.4, 0.6, 0.8].forEach(function (v) { S('line', { x1: 90, x2: 1470, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 78, sy(v) + 8, f(v, 1), { 'text-anchor': 'end', 'font-size': 20, fill: C.ink3 }); });
    var bars = range(n).map(function (i) {
      var x = sx(i + 1);
      var r = S('rect', { x: x - 28, width: 56, y: sy(0), height: 0, rx: 6, fill: C.amber }, svg);
      var t = txt(svg, x, sy(0) - 10, '', { 'text-anchor': 'middle', 'font-size': 21, 'font-weight': 600, fill: C.ink2, 'font-family': 'JetBrains Mono, monospace' });
      txt(svg, x, 372, String(i + 1), { 'text-anchor': 'middle', 'font-size': 21, fill: C.ink3 });
      return { r: r, t: t };
    });
    txt(svg, 830, 398, 'paso', { 'text-anchor': 'middle', 'font-size': 20, fill: C.ink3 });
    var c = H('div', 'ctrl', wrap); c.style.gridTemplateColumns = '20em 1fr 5em';
    H('label', '', c, 'cuánto conserva la libreta: u');
    var inp = H('input', '', c); inp.type = 'range'; inp.min = 0.1; inp.max = 1; inp.step = 0.05; inp.value = u; inp.setAttribute('aria-label', 'u');
    var out = H('output', '', c);
    var msg = H('p', 'say', wrap);
    function eco(uu) { var h = [], v = Math.tanh(1); for (var i = 0; i < n; i++) { h.push(v); v = Math.tanh(uu * v); } return h; }
    function draw(anim) {
      var h = eco(u); out.textContent = f(u, 2); inp.value = u;
      bars.forEach(function (b, i) {
        var y = sy(h[i]); b.r.style.transition = anim ? 'y .5s, height .5s' : 'none';
        b.r.setAttribute('y', y); b.r.setAttribute('height', sy(0) - y); b.r.setAttribute('fill', h[i] < 0.01 ? C.coral : C.amber);
        b.t.setAttribute('y', y - 10); b.t.textContent = h[i] >= 0.0095 ? f(h[i], 2) : h[i] >= 0.00095 ? f(h[i], 3) : '≈0';
      });
      msg.innerHTML = 'Con u = <b class="num">' + f(u, 2) + '</b>, después de 10 pasos queda <b class="num ' + (h[9] < 0.01 ? 'co' : 'am') + '">' + (h[9] < 0.01 ? f(h[9], 3) : f(h[9], 2)) + '</b> del primer dato' + (u >= 0.95 ? ': casi no se apaga, pero la libreta se satura.' : h[9] < 0.01 ? ': prácticamente nada.' : ': se apaga más despacio, pero se apaga.');
    }
    inp.addEventListener('input', function () { u = +inp.value; draw(false); });
    draw(false);
    return {
      step: function (s) { var t = s >= 2 ? 0.9 : 0.5; if (t !== u) { var a = u; tween(900, function (k) { u = a + (t - a) * k; draw(false); }); } },
      final: function () { u = 0.5; draw(false); }
    };
  });

  /* ---------------- unroll: the same cell at every step; the blame travels backwards and shrinks ---------------- */
  demo('unroll', function (el, api) {
    var n = 6, W = 1560, Hh = 470;
    var svg = svgIn(el, W, Hh, 'La red recurrente desenrollada en seis pasos con los mismos pesos; la culpa viaja hacia atrás y se encoge');
    var xs = range(n).map(function (i) { return 110 + i * 240; }), y = 210, words = ['el', 'socio', 'pagó', 'la', 'cuota', 'tarde'];
    var GL = glow(svg, C.coral);
    for (var i = 0; i < n - 1; i++) { S('line', { x1: xs[i] + 70, x2: xs[i + 1] - 70, y1: y, y2: y, stroke: C.ink3, 'stroke-width': 4 }, svg); S('polygon', { points: (xs[i + 1] - 84) + ',' + (y - 10) + ' ' + (xs[i + 1] - 70) + ',' + y + ' ' + (xs[i + 1] - 84) + ',' + (y + 10), fill: C.ink3 }, svg); }
    var chips = [], halo = [], vals = [];
    xs.forEach(function (x, i) {
      S('line', { x1: x, x2: x, y1: y + 140, y2: y + 62, stroke: C.ink3, 'stroke-width': 3 }, svg);
      txt(svg, x, y + 176, words[i], { 'text-anchor': 'middle', 'font-size': 26, fill: C.ink2, 'font-family': 'JetBrains Mono, monospace' });
      halo.push(S('circle', { cx: x, cy: y, r: 110, fill: GL, opacity: 0 }, svg));
      S('rect', { x: x - 70, y: y - 60, width: 140, height: 120, rx: 24, fill: C.night2, stroke: C.amber, 'stroke-width': 3 }, svg);
      txt(svg, x, y + 10, 'celda', { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 600, fill: C.ink });
      chips.push(txt(svg, x, y - 78, 'w · u · b', { 'text-anchor': 'middle', 'font-size': 21, 'font-weight': 600, fill: C.mint, opacity: 0 }));
      vals.push(txt(svg, x, y + 98, '', { 'text-anchor': 'middle', 'font-size': 24, 'font-weight': 700, fill: C.coral, 'font-family': 'JetBrains Mono, monospace' }));
    });
    txt(svg, xs[n - 1] + 70, y - 100, 'error', { 'text-anchor': 'end', 'font-size': 24, 'font-weight': 700, fill: C.coral });
    var dot = S('circle', { r: 0, cx: xs[n - 1], cy: y, fill: C.coral }, svg);
    var cap = txt(svg, W / 2, 34, '', { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 600, fill: C.ink2 });
    var st = 0, t0 = 0;
    var loop = api.raf(function (t, dt) {
      if (st < 2) return;
      t0 += dt; var T = 3200, p = (t0 % T) / T, pos = (n - 1) * (1 - p), i = Math.floor(pos), fr = pos - i;
      var x = xs[Math.min(n - 1, i)] + (i < n - 1 ? (xs[i + 1] - xs[i]) * fr : 0), m = Math.pow(0.5, (n - 1) - pos);
      dot.setAttribute('cx', x); dot.setAttribute('r', (5 + 22 * Math.sqrt(m)).toFixed(1));
      halo.forEach(function (h, j) { var near = Math.max(0, 1 - Math.abs(pos - j) * 1.4); h.setAttribute('opacity', (near * Math.sqrt(Math.pow(0.5, n - 1 - j))).toFixed(3)); });
    });
    function set(s) {
      st = s;
      chips.forEach(function (c) { c.setAttribute('opacity', s >= 1 ? 1 : 0); });
      vals.forEach(function (v, i) { var m = Math.pow(0.5, n - 1 - i); v.textContent = s >= 2 ? (m >= 0.1 ? f(m, 2) : f(m, 3)) : ''; });
      cap.textContent = s >= 2 ? 'La culpa viaja hacia atrás en el tiempo y, en cada paso, se multiplica por ≈ 0.5' : s >= 1 ? 'Los mismos pesos w, u y b en todos los pasos: como la CNN usa el mismo filtro en toda la foto' : 'Leer una frase de 6 palabras = una red de 6 capas';
      dot.setAttribute('r', 0);
      if (s >= 2 && !RM && !api.print) loop.start(); else loop.stop();
    }
    set(0);
    return { step: set, leave: function () { loop.stop(); }, final: function () { set(2); } };
  });

  /* ---------------- lstm: a notebook with three valves on a memory belt ---------------- */
  demo('lstm', function (el, api) {
    var W = 1500, Hh = 560, svg = svgIn(el, W, Hh, 'Una LSTM: una cinta de memoria con tres válvulas: olvidar, guardar y mostrar');
    var yb = 140;
    S('rect', { x: 40, y: yb - 34, width: 1420, height: 68, rx: 34, fill: C.night2, stroke: C.lilac, 'stroke-width': 4 }, svg);
    txt(svg, 60, yb - 52, 'la cinta de memoria (c): viaja casi sin cambios de un paso al siguiente', { 'font-size': 24, 'font-weight': 600, fill: C.lilac });
    var dash = S('line', { x1: 70, x2: 1430, y1: yb, y2: yb, stroke: C.lilac, 'stroke-width': 6, 'stroke-dasharray': '18 26', opacity: 0.8 }, svg);
    var V = [
      { x: 380, n: 'Olvidar', d: 'qué borrar de la cinta', op: '×', ic: 'borrador', c: C.coral },
      { x: 760, n: 'Guardar', d: 'qué anotar de lo nuevo', op: '+', ic: 'lápiz', c: C.amber },
      { x: 1140, n: 'Mostrar', d: 'qué leer en voz alta (h)', op: '→', ic: 'ventana', c: C.mint }
    ];
    var G = V.map(function (v, i) {
      var g = S('g', {}, svg);
      S('circle', { cx: v.x, cy: yb, r: 40, fill: C.night, stroke: v.c, 'stroke-width': 5 }, g);
      txt(g, v.x, yb + 14, v.op, { 'text-anchor': 'middle', 'font-size': 40, 'font-weight': 700, fill: v.c });
      S('line', { x1: v.x, x2: v.x, y1: yb + 44, y2: 330, stroke: v.c, 'stroke-width': 4 }, g);
      S('rect', { x: v.x - 150, y: 330, width: 300, height: 130, rx: 22, fill: C.night2, stroke: v.c, 'stroke-width': 3 }, g);
      txt(g, v.x, 378, v.n, { 'text-anchor': 'middle', 'font-size': 32, 'font-weight': 700, fill: v.c });
      txt(g, v.x, 414, v.d, { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink2 });
      txt(g, v.x, 444, 'una sigmoide: 0 cierra, 1 abre', { 'text-anchor': 'middle', 'font-size': 19, fill: C.ink3 });
      var kn = S('rect', { x: v.x - 120, y: 486, width: 240, height: 18, rx: 9, fill: C.night3 }, g);
      var fill = S('rect', { x: v.x - 120, y: 486, width: 0, height: 18, rx: 9, fill: v.c }, g);
      return { g: g, fill: fill, v: v };
    });
    txt(svg, 750, 545, 'entra: la palabra de ahora + lo que mostró el paso anterior', { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3 });
    var off = 0, loop = api.raf(function (t, dt) { off -= dt * 0.08; dash.setAttribute('stroke-dashoffset', off.toFixed(1)); });
    var OPEN = [0.95, 0.35, 0.7];
    function set(s) {
      G.forEach(function (g, i) {
        g.g.style.transition = 'opacity .5s'; g.g.style.opacity = s === 0 || s >= 4 ? 1 : (i + 1 === s ? 1 : 0.2);
        g.fill.style.transition = 'width .8s cubic-bezier(.16,1,.3,1)'; g.fill.setAttribute('width', (s >= i + 1 ? OPEN[i] : 0) * 240);
      });
    }
    set(0);
    return { enter: function () { if (!RM && !api.print) loop.start(); }, leave: function () { loop.stop(); }, step: set, final: function () { set(4); } };
  });

  /* ---------------- memtest: the memory exam of NB04 (real results) ---------------- */
  demo('memtest', function (el, api) {
    var M = Q.memoria, Ts = ['10', '30', '80'], K = [['rnn', 'SimpleRNN', C.azure], ['lstm', 'LSTM', C.lilac], ['atencion', 'Atención', C.amber]];
    var svg = svgIn(el, 1500, 600, 'Exactitud de SimpleRNN, LSTM y atención cuando el dato importante está a 10, 30 u 80 pasos');
    var y0 = 470, sy = lin(0, 1, y0, 50);
    [0, 0.5, 1].forEach(function (v) { S('line', { x1: 110, x2: 1460, y1: sy(v), y2: sy(v), stroke: v === 0.5 ? C.ink3 : C.grid, 'stroke-width': v === 0.5 ? 3 : 2, 'stroke-dasharray': v === 0.5 ? '12 10' : '' }, svg); txt(svg, 96, sy(v) + 8, Math.round(v * 100) + ' %', { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 }); });
    txt(svg, 1460, sy(0.5) - 12, 'adivinar = 50 %', { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 });
    var G = Ts.map(function (T, gi) {
      var g = S('g', {}, svg), gx = 190 + gi * 440;
      K.forEach(function (k, j) {
        var r = M[T][k[0]], x = gx + j * 120, y = sy(r.test);
        S('rect', { x: x, y: y, width: 96, height: y0 - y, rx: 10, fill: k[2] }, g);
        txt(g, x + 48, y - 14, Math.round(r.test * 100) + ' %', { 'text-anchor': 'middle', 'font-size': 27, 'font-weight': 700, fill: k[2], 'font-family': 'JetBrains Mono, monospace' });
      });
      txt(g, gx + 168, y0 + 46, T + ' pasos', { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: C.ink });
      return g;
    });
    var leg = S('g', {}, svg);
    K.forEach(function (k, j) { S('rect', { x: 190 + j * 420, y: 560, width: 26, height: 26, rx: 6, fill: k[2] }, leg); txt(leg, 228 + j * 420, 582, k[1] + ' · ' + M['80'][k[0]].params.toLocaleString('es-EC').replace(/[.,]/g, ' ') + ' parámetros', { 'font-size': 22, fill: C.ink2 }); });
    function set(s) { G.forEach(function (g, i) { g.style.transition = 'opacity .5s'; g.style.opacity = s >= i + 1 ? 1 : 0.08; }); }
    set(0);
    return { step: set, final: function () { set(3); } };
  });

  /* ---------------- serial: the RNN reads in a queue; attention looks at everything at once ---------------- */
  demo('serial', function (el, api) {
    var n = 8, W = 1500, Hh = 560, svg = svgIn(el, W, Hh, 'Arriba la red recurrente procesa una palabra a la vez; abajo la atención procesa todas a la vez');
    var xs = range(n).map(function (i) { return 260 + i * 150; });
    function rowY(y, lab, sub) { txt(svg, 30, y + 4, lab, { 'font-size': 28, 'font-weight': 700, fill: C.ink }); txt(svg, 30, y + 38, sub, { 'font-size': 21, fill: C.ink3 }); }
    rowY(110, 'RNN', 'en fila'); rowY(400, 'Atención', 'todos a la vez');
    var top = xs.map(function (x) { return S('rect', { x: x - 55, y: 70, width: 110, height: 80, rx: 16, fill: C.night3, stroke: C.line, 'stroke-width': 2 }, svg); });
    var gl = S('g', {}, svg);
    for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) if (i !== j) {
      var x1 = xs[i], x2 = xs[j], mx = (x1 + x2) / 2, hgt = 30 + Math.abs(i - j) * 16;
      S('path', { d: 'M' + x1 + ' 350 Q' + mx + ' ' + (350 - hgt) + ' ' + x2 + ' 350', fill: 'none', stroke: C.amber, 'stroke-width': 1.5, opacity: 0.35 }, gl);
    }
    var bot = xs.map(function (x) { return S('rect', { x: x - 55, y: 360, width: 110, height: 80, rx: 16, fill: C.night3, stroke: C.line, 'stroke-width': 2 }, svg); });
    var c1 = txt(svg, W - 30, 170, '', { 'text-anchor': 'end', 'font-size': 24, 'font-weight': 600, fill: C.azure });
    var c2 = txt(svg, W - 30, 480, '', { 'text-anchor': 'end', 'font-size': 24, 'font-weight': 600, fill: C.amber });
    txt(svg, 750, 540, 'Una GPU hace miles de cuentas a la vez: con la RNN espera; con la atención trabaja toda.', { 'text-anchor': 'middle', 'font-size': 23, fill: C.ink2 });
    var t0 = 0, loop = api.raf(function (t, dt) {
      t0 += dt; var tick = Math.floor(t0 / 520) % (n + 3);
      top.forEach(function (r, i) { var on = i === tick, done = i < tick; r.setAttribute('fill', on ? C.azure : done ? C.night2 : C.night3); r.setAttribute('stroke', on ? C.azure : C.line); });
      var allOn = tick >= 1 && tick <= n; bot.forEach(function (r) { r.setAttribute('fill', allOn ? C.amber : C.night3); r.setAttribute('stroke', allOn ? C.amber : C.line); });
      gl.style.opacity = allOn ? 1 : 0.15;
      c1.textContent = 'paso ' + Math.min(tick + 1, n) + ' de ' + n; c2.textContent = '1 paso · ' + n * n + ' comparaciones';
    });
    return { enter: function () { if (!RM && !api.print) loop.start(); else { gl.style.opacity = 1; bot.forEach(function (r) { r.setAttribute('fill', C.amber); }); } }, leave: function () { loop.stop(); }, final: function () { gl.style.opacity = 1; } };
  });

  /* ---------------- attn: each word looks at all the others (illustrative weights) ---------------- */
  var WORDS = ['el', 'socio', 'pagó', 'la', 'cuota', 'porque', 'él', 'recibió', 'su', 'sueldo'];
  var ATT = {
    'él': [0.02, 0.62, 0.05, 0.01, 0.04, 0.03, 0.14, 0.06, 0.01, 0.02],
    'su': [0.01, 0.48, 0.02, 0.01, 0.03, 0.02, 0.27, 0.06, 0.06, 0.04],
    'sueldo': [0.01, 0.06, 0.08, 0.01, 0.10, 0.03, 0.06, 0.41, 0.14, 0.10],
    'pagó': [0.03, 0.40, 0.12, 0.04, 0.30, 0.02, 0.03, 0.02, 0.01, 0.03],
    'cuota': [0.02, 0.10, 0.38, 0.18, 0.22, 0.02, 0.02, 0.02, 0.01, 0.03]
  };
  demo('attn', function (el, api) {
    var sel = 'él', W = 1560, Hh = 520, svg = svgIn(el, W, Hh, 'Arcos que muestran a qué palabras mira la palabra elegida');
    var xs = [], x = 40, y = 440, boxes = [];
    WORDS.forEach(function (w) { var wd = 40 + w.length * 19; xs.push(x + wd / 2); x += wd + 22; });
    var shift = (W - x) / 2; xs = xs.map(function (v) { return v + shift; });
    var gA = S('g', {}, svg);
    WORDS.forEach(function (w, i) {
      var wd = 40 + w.length * 19, g = S('g', { style: 'cursor:pointer' }, svg);
      var r = S('rect', { x: xs[i] - wd / 2, y: y - 40, width: wd, height: 60, rx: 16, fill: C.night3, stroke: C.line, 'stroke-width': 2 }, g);
      var t = txt(g, xs[i], y, w, { 'text-anchor': 'middle', 'font-size': 30, fill: C.ink2, 'font-family': 'JetBrains Mono, monospace' });
      g.addEventListener('click', function () { if (ATT[w]) { auto = false; pick(w); } });
      boxes.push({ r: r, t: t, w: w });
    });
    var info = txt(svg, W / 2, 40, '', { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 600, fill: C.ink2 });
    function pick(w) {
      sel = w; gA.innerHTML = '';
      var qi = WORDS.indexOf(w), A = ATT[w];
      A.forEach(function (a, j) {
        if (j === qi || a < 0.025) return;
        var x1 = xs[qi], x2 = xs[j], mx = (x1 + x2) / 2, hgt = 70 + Math.abs(qi - j) * 30;
        S('path', { d: 'M' + x1 + ' ' + (y - 44) + ' Q' + mx + ' ' + (y - 44 - hgt * 1.4) + ' ' + x2 + ' ' + (y - 44), fill: 'none', stroke: C.amber, 'stroke-width': (2 + a * 34).toFixed(1), opacity: (0.25 + a * 1.2).toFixed(2), 'stroke-linecap': 'round' }, gA);
        if (a >= 0.08) txt(gA, mx, y - 52 - hgt * 0.7, Math.round(a * 100) + ' %', { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 700, fill: C.amber, stroke: C.night, 'stroke-width': 8, 'paint-order': 'stroke' });
      });
      boxes.forEach(function (b, j) {
        var on = b.w === w, a = A[j];
        b.r.setAttribute('fill', on ? C.amber : C.night3); b.r.setAttribute('stroke', on ? C.amber : ATT[b.w] ? C.ink3 : C.line);
        b.t.setAttribute('fill', on ? C.night : a >= 0.2 ? C.amber : C.ink2); b.t.setAttribute('font-weight', a >= 0.2 || on ? 700 : 400);
      });
      var best = A.map(function (a, j) { return [a, j]; }).filter(function (p) { return p[1] !== qi; }).sort(function (p, q) { return q[0] - p[0]; })[0];
      info.textContent = '«' + w + '» mira sobre todo a «' + WORDS[best[1]] + '» (' + Math.round(best[0] * 100) + ' %). Haz clic en otra palabra con borde claro.';
    }
    var order = ['él', 'su', 'sueldo'], auto = true;
    pick('él');
    return { step: function (s) { if (auto) pick(order[Math.min(s, 2)]); }, final: function () { pick('él'); } };
  });

  /* ---------------- attnw: what the attention network of NB04 really looked at (80 steps) ---------------- */
  demo('attnw', function (el, api) {
    var A = Q.atencion, P = A.pesos, n = P.length, mk = A.marca, W = 1560, Hh = 470;
    var svg = svgIn(el, W, Hh, 'Pesos de atención reales en los 80 pasos: casi todo el peso está en el paso marcado');
    var sx = lin(0, n, 80, 1520), sy = lin(0, 1, 330, 30), bw = (1520 - 80) / n;
    [0, 0.5, 1].forEach(function (v) { S('line', { x1: 80, x2: 1520, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 68, sy(v) + 8, Math.round(v * 100) + ' %', { 'text-anchor': 'end', 'font-size': 19, fill: C.ink3 }); });
    var R = P.map(function (p, i) { return S('rect', { x: sx(i) + 2, width: bw - 4, y: sy(0), height: 0, rx: 3, fill: i === mk ? C.amber : C.ink3 }, svg); });
    A.valores.forEach(function (v, i) { S('rect', { x: sx(i) + 3, y: 352, width: bw - 6, height: 26, rx: 3, fill: i === mk ? C.amber : v > 0 ? C.night3 : C.night2, stroke: i === mk ? C.amber : C.line, 'stroke-width': 1 }, svg); });
    txt(svg, 80, 412, 'cada cuadrito: un paso (valor +1 o −1). El ámbar es el paso marcado.', { 'font-size': 21, fill: C.ink3 });
    var lab = txt(svg, sx(mk) + 30, sy(P[mk]) + 10, Math.round(P[mk] * 1000) / 10 + ' % del peso en el paso marcado', { 'font-size': 28, 'font-weight': 700, fill: C.amber, opacity: 0 });
    var rest = txt(svg, 1520, 292, 'los otros 79 pasos se reparten el ' + f((1 - P[mk]) * 100, 1) + ' %', { 'text-anchor': 'end', 'font-size': 23, fill: C.ink2, opacity: 0 });
    function set(s) {
      R.forEach(function (r, i) { var y = sy(s >= 1 ? P[i] : 0); r.style.transition = 'y .8s cubic-bezier(.16,1,.3,1), height .8s cubic-bezier(.16,1,.3,1)'; r.setAttribute('y', y); r.setAttribute('height', sy(0) - y); });
      lab.setAttribute('opacity', s >= 1 ? 1 : 0); rest.setAttribute('opacity', s >= 2 ? 1 : 0);
    }
    set(0);
    return { step: set, final: function () { set(2); } };
  });

  /* ---------------- cost: n words, n × n comparisons ---------------- */
  demo('cost', function (el, api) {
    var n = 8;
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:2.4em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.gap = '.8em';
    var pl = H('div', 'plate', lc); pl.style.aspectRatio = '1/1'; pl.style.width = 'min(100%, 18.5em)';
    var svg = svgIn(pl, 400, 400, 'Cuadrícula de n por n comparaciones');
    var gG = S('g', {}, svg);
    var c = H('div', 'ctrl', lc); c.style.gridTemplateColumns = '6em 1fr 3em';
    H('label', '', c, 'palabras');
    var inp = H('input', '', c); inp.type = 'range'; inp.min = 2; inp.max = 32; inp.step = 1; inp.value = n; inp.setAttribute('aria-label', 'número de palabras');
    var out = H('output', '', c);
    var read = H('p', 'say', lc);
    var rc = H('div', 'col', root); rc.style.gap = '.7em';
    var rows = [['1 000', 'una carta', '1 000 000'], ['10 000', 'un informe', '100 millones'], ['100 000', 'un expediente', '10 000 millones'], ['1 000 000', 'una biblioteca pequeña', '1 billón (10¹²)']];
    var hdr = H('div', '', rc); hdr.style.cssText = 'display:grid;grid-template-columns:7em 1fr 10em;gap:1em;font:600 1em/1 var(--sans);color:var(--ink-3);letter-spacing:.03em';
    hdr.innerHTML = '<span>PALABRAS</span><span>ES COMO</span><span style="text-align:right">COMPARACIONES</span>';
    var R = rows.map(function (r, i) {
      var d = H('div', '', rc); d.style.cssText = 'display:grid;grid-template-columns:7em 1fr 10em;gap:1em;align-items:baseline;font-size:1.4em;padding:.5em 0;border-top:1px solid var(--line);transition:opacity .5s';
      d.innerHTML = '<b class="num">' + r[0] + '</b><span class="mu">' + r[1] + '</span><b class="num am" style="text-align:right">' + r[2] + '</b>';
      return d;
    });
    function draw() {
      out.textContent = n; inp.value = n; gG.innerHTML = '';
      var cs = 360 / n;
      for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) S('rect', { x: 20 + j * cs + 1, y: 20 + i * cs + 1, width: Math.max(1, cs - 2), height: Math.max(1, cs - 2), rx: Math.min(6, cs / 4), fill: i === j ? C.ink3 : C.amber, opacity: i === j ? 0.6 : 0.75 }, gG);
      read.innerHTML = '<b class="num">' + n + '</b> palabras → <b class="num am">' + n * n + '</b> comparaciones. El doble de palabras, <b>cuatro veces</b> más cuentas.';
    }
    inp.addEventListener('input', function () { n = +inp.value; draw(); });
    draw();
    return { step: function (s) { R.forEach(function (d, i) { d.style.opacity = s >= i + 1 ? 1 : 0.1; }); }, final: function () { R.forEach(function (d) { d.style.opacity = 1; }); } };
  });
})();
