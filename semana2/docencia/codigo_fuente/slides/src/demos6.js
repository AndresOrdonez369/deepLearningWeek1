/* Demos · Semana 2 · viernes: cómo mira una red una imagen (real Fashion-MNIST data from NB03, window.FMNIST) */
(function () {
  var F = window.FMNIST, R = F.results, CL = F.clases;
  var NIGHT2 = [15, 26, 41], INK = [241, 246, 250], AMB = [255, 181, 65], AZU = [74, 186, 244], MINT = [100, 234, 183];
  function mix(a, b, t) { t = clamp(t, 0, 1); return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function gray(v) { return mix(NIGHT2, INK, v / 255); }
  function heat(v) { return v < 128 ? mix(NIGHT2, [150, 98, 40], v / 128) : mix([150, 98, 40], AMB, (v - 128) / 127); }
  function signed(v) { return v >= 0 ? mix(NIGHT2, AMB, v) : mix(NIGHT2, AZU, -v); }
  function canvas(parent, w, h, cls) {
    var c = H('canvas', cls || 'pixc', parent); c.width = w; c.height = h; return c;
  }
  function paint(c, A, cm) {
    var h = A.length, w = A[0].length, ctx = c.getContext('2d'), im = ctx.createImageData(w, h);
    for (var r = 0; r < h; r++) for (var q = 0; q < w; q++) {
      var v = A[r][q], col = v == null ? NIGHT2 : cm(v), k = (r * w + q) * 4;
      im.data[k] = col[0]; im.data[k + 1] = col[1]; im.data[k + 2] = col[2]; im.data[k + 3] = 255;
    }
    ctx.putImageData(im, 0, 0);
  }
  function img(i) { return F.samples[i].px; }
  function norm(A) { return A.map(function (r) { return r.map(function (v) { return v / 255; }); }); }
  function conv(A, K) {        // valid 3x3 convolution (cross-correlation, like Keras)
    var n = A.length, out = [];
    for (var r = 0; r < n - 2; r++) { var row = []; for (var q = 0; q < n - 2; q++) { var s = 0; for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) s += A[r + i][q + j] * K[i][j]; row.push(s); } out.push(row); }
    return out;
  }
  window.W2 = { F: F, canvas: canvas, paint: paint, gray: gray, heat: heat, signed: signed, norm: norm, conv: conv };
  var KERNELS = {
    vertical: { n: 'Borde vertical', k: [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], d: 'oscuro a la izquierda, claro a la derecha' },
    horizontal: { n: 'Borde horizontal', k: [[-1, -1, -1], [0, 0, 0], [1, 1, 1]], d: 'oscuro arriba, claro abajo' },
    blur: { n: 'Desenfoque', k: [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]], d: 'el promedio de los 9 vecinos' }
  };

  /* ---------------- pixels: a real photo is a 28 x 28 table of brightness values ---------------- */
  demo('pixels', function (el, api) {
    var cur = 0, zr = 9, zc = 11;
    var wrap = H('div', '', el); wrap.style.cssText = 'display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:2.4em;height:100%;align-items:center;justify-items:center';
    var left = H('div', 'col', wrap); left.style.cssText += ';gap:.8em;align-items:center;height:100%;justify-content:center';
    var plate = H('div', 'pplate', left); plate.style.width = 'min(100%, 19em)';
    var cv = canvas(plate, 28, 28);
    var ov = svgIn(plate, 280, 280, 'Recuadro de 8 por 8 píxeles que se amplía a la derecha');
    var box = S('rect', { width: 80, height: 80, fill: 'none', stroke: C.amber, 'stroke-width': 3, rx: 2 }, ov);
    var th = H('div', 'thumbs', left), tbs = [];
    F.samples.forEach(function (s, i) {
      var b = H('button', '', th); b.type = 'button'; b.setAttribute('aria-label', 'Ver ' + CL[s.label]);
      paint(canvas(b, 28, 28), s.px, gray); b.onclick = function () { cur = i; draw(); }; tbs.push(b);
    });
    var right = H('div', 'col', wrap); right.style.gap = '.8em';
    var cap = H('p', 'lab3', right);
    var z = H('div', 'zoom', right), cells = range(64).map(function () { return H('span', '', z); });
    var note = H('p', 'cap', right, 'Pasa el mouse por la foto para mover el recuadro.');
    function draw() {
      var P = img(cur); paint(cv, P, gray);
      tbs.forEach(function (b, i) { b.classList.toggle('on', i === cur); });
      box.setAttribute('x', zc * 10); box.setAttribute('y', zr * 10);
      cap.innerHTML = '<b>' + CL[F.samples[cur].label] + '</b> · filas ' + zr + '–' + (zr + 7) + ', columnas ' + zc + '–' + (zc + 7);
      cells.forEach(function (c, k) {
        var v = P[zr + (k >> 3)][zc + (k & 7)], col = gray(v);
        c.textContent = v; c.style.background = 'rgb(' + col.map(Math.round).join(',') + ')';
        c.style.color = v > 140 ? C.night : C.ink2;
      });
    }
    plate.addEventListener('pointermove', function (e) {
      var r = plate.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * 28, y = (e.clientY - r.top) / r.height * 28;
      zc = clamp(Math.round(x - 4), 0, 20); zr = clamp(Math.round(y - 4), 0, 20); draw();
    });
    plate.setAttribute('data-drag', '1');
    draw();
    return { step: function (s) { right.style.opacity = s >= 1 ? 1 : 0; right.style.transition = 'opacity .5s'; box.style.opacity = s >= 1 ? 1 : 0; }, final: function () { right.style.opacity = 1; box.style.opacity = 1; } };
  });

  /* ---------------- flatten: a dense network sees a row of 784 numbers; shuffling the pixels changes nothing for it ---------------- */
  demo('flatten', function (el, api) {
    var P = img(0), perm = range(784), rnd = seeded(2026);
    for (var i = 783; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
    var flat = [].concat.apply([], P), mixed = perm.map(function (k) { return flat[k]; });
    var M2 = range(28).map(function (r) { return mixed.slice(r * 28, r * 28 + 28); });
    var wrap = H('div', 'col', el); wrap.style.cssText += ';height:100%;gap:1.2em';
    var top = H('div', '', wrap); top.style.cssText = 'display:grid;grid-template-columns:repeat(2,minmax(0,12.5em)) 1fr;gap:2em;align-items:center';
    function card(t) { var c = H('div', 'col', top); c.style.gap = '.5em'; var p = H('div', 'pplate', c); H('p', 'lab3', c, t); return p; }
    var p1 = card('<b>La foto</b> · 28 × 28'), p2 = card('<b>Los mismos píxeles, mezclados</b>');
    var c1 = canvas(p1, 28, 28), c2 = canvas(p2, 28, 28);
    var o1 = svgIn(p1, 280, 280, 'Fila que se está aplanando'), rowr = S('rect', { x: 0, width: 280, height: 10, fill: 'none', stroke: C.amber, 'stroke-width': 3, opacity: 0 }, o1);
    var msg = H('div', 'col', top); msg.style.gap = '.8em'; msg.className = 'col fmsg';
    var m1 = H('p', 'say', msg, 'Para una capa <code>Dense</code>, la foto llega como <b>una fila de 784 números</b>: la fila 1, después la 2, y así hasta la 28.');
    var m2 = H('p', 'say', msg, 'Si mezclamos los píxeles (siempre igual en todas las fotos), la densa aprende <b>exactamente lo mismo</b>: <b class="num am">' + f(R.densa.mezclada * 100, 1) + ' %</b> contra <b class="num">' + f(R.densa.test * 100, 1) + ' %</b>. Nunca supo qué píxel era vecino de cuál.');
    var lane = H('div', 'col', wrap); lane.style.gap = '.4em';
    H('p', 'lab3', lane, '<b>Lo que recibe la red densa</b> · 784 números en fila (cada rayita es un píxel)');
    var sp = H('div', 'plate', lane); sp.style.height = '3.4em';
    var cs = canvas(sp, 784, 1); cs.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated';
    var fan = H('div', 'plate', lane); fan.style.height = '5.2em';
    var fs_ = svgIn(fan, 1600, 130, 'Una neurona conectada con los 784 píxeles');
    var gF = S('g', {}, fs_);
    for (var k = 0; k < 784; k += 6) S('line', { x1: 8 + k / 783 * 1584, y1: 0, x2: 800, y2: 112, stroke: C.amber, 'stroke-width': 1, opacity: 0.28 }, gF);
    S('circle', { cx: 800, cy: 112, r: 15, fill: C.amber }, fs_);
    txt(fs_, 830, 120, 'una neurona = 784 pesos · 128 neuronas: 100 480', { fill: C.ink, 'font-size': 24, 'font-weight': 600 });
    var shown = 0, mode = 0, tw = null;
    function strip(n, src) {
      var A = [src.map(function (v, i) { return i < n ? v : null; })]; paint(cs, A, gray);
    }
    function set(s) {
      if (tw) tw.stop();
      paint(c1, P, gray); paint(c2, s >= 2 ? M2 : range(28).map(function () { return range(28).map(function () { return null; }); }), gray);
      p2.parentNode.style.opacity = s >= 2 ? 1 : 0.25; m2.style.opacity = s >= 2 ? 1 : 0; m1.style.opacity = s >= 1 ? 1 : 0.35;
      fan.style.opacity = s >= 3 ? 1 : 0;
      if (s === 1 && mode < 1 && !api.print && !RM) {
        tw = tween(2600, function (k) { var n = Math.round(784 * k); strip(n, flat); rowr.setAttribute('y', Math.min(27, Math.floor(n / 28)) * 10); rowr.setAttribute('opacity', k < 1 ? 1 : 0); });
      } else { rowr.setAttribute('opacity', 0); strip(s >= 1 ? 784 : 0, s >= 2 ? mixed : flat); }
      mode = s;
    }
    [m1, m2, fan, p2.parentNode].forEach(function (e) { e.style.transition = 'opacity .5s'; });
    set(0);
    return { step: set, final: function () { mode = 3; set(3); } };
  });

  /* ---------------- conv: the 3x3 magnifier slides over the photo and fills a map ---------------- */
  demo('conv', function (el, api) {
    var cover = el.dataset.mode === 'cover', A = norm(img(+(el.dataset.img || 0))), kn = el.dataset.k || 'vertical';
    var K = KERNELS[kn].k, OUT = conv(A, K), pos = 0, N = 26 * 26, playing = false;
    var root = H('div', '', el); root.style.cssText = 'display:flex;flex-direction:column;height:100%';
    var g = H('div', 'convx', root); g.style.flex = '1'; g.style.minHeight = '0';
    if (cover) g.style.gridTemplateColumns = 'minmax(0,1fr) minmax(0,1fr)';
    function plateBox(parent, label) { var c = H('div', 'col', parent); c.style.cssText += ';gap:.5em;align-items:stretch'; var p = H('div', 'pplate', c); if (cover) p.style.width = '100%'; if (label) H('p', 'lab3', c, label); return p; }
    var pi = plateBox(g, cover ? '' : '<b>La foto</b> · el recuadro es la lupa de 3 × 3');
    var ci = canvas(pi, 28, 28); paint(ci, img(+(el.dataset.img || 0)), gray);
    var oi = svgIn(pi, 280, 280, 'La lupa de 3 por 3 sobre la foto');
    var win = S('rect', { width: 30, height: 30, fill: C.amber, 'fill-opacity': 0.18, stroke: C.amber, 'stroke-width': 3 }, oi);
    var side = null, mp, mk, res, kname;
    if (!cover) {
      side = H('div', 'side', g);
      H('p', 'lab3', side, '9 píxeles');
      mp = H('div', 'm3', side); var pc = range(9).map(function () { return H('span', '', mp); });
      H('p', 'op', side, '×');
      mk = H('div', 'm3 k', side); var kc = range(9).map(function () { return H('span', '', mk); });
      kname = H('p', 'lab3', side);
      H('p', 'op', side, '= suma');
      res = H('p', 'res', side);
    }
    var po = plateBox(g, cover ? '' : '<b>El mapa</b> · 26 × 26: dónde encontró el patrón');
    var co = canvas(po, 26, 26);
    var oo = svgIn(po, 260, 260, 'Casilla del mapa que se está calculando'), cell = S('rect', { width: 10, height: 10, fill: 'none', stroke: C.ink, 'stroke-width': 2.5 }, oo);
    var bar = null, btnPlay, kb = {};
    if (!cover) {
      bar = H('div', 'convbar', root);
      var seg = H('div', 'seg', bar);
      Object.keys(KERNELS).forEach(function (k) { var b = H('button', 'btn', seg, KERNELS[k].n); b.type = 'button'; b.onclick = function () { setK(k); restart(); }; kb[k] = b; });
      var seg2 = H('div', 'seg', bar);
      btnPlay = H('button', 'btn primary', seg2, '▶ Recorrer'); btnPlay.type = 'button';
      var bStep = H('button', 'btn', seg2, 'Un paso'); bStep.type = 'button';
      var bAll = H('button', 'btn', seg2, 'Todo'); bAll.type = 'button';
      btnPlay.onclick = function () { if (playing) stop(); else { if (pos >= N) pos = 0; play(); } };
      bStep.onclick = function () { stop(); pos = Math.min(N, pos + 1); draw(); };
      bAll.onclick = function () { stop(); pos = N; draw(); };
    }
    var mx = 1;
    function setK(k) {
      kn = k; K = KERNELS[k].k; OUT = conv(A, K);
      mx = 0; OUT.forEach(function (r) { r.forEach(function (v) { mx = Math.max(mx, Math.abs(v)); }); });
      if (!cover) {
        for (var k2 in kb) kb[k2].classList.toggle('on', k2 === k);
        kc.forEach(function (c, i) { var v = K[(i / 3) | 0][i % 3]; c.textContent = k === 'blur' ? '1/9' : (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v); c.style.color = v > 0 ? C.amber : v < 0 ? C.azure : C.ink3; });
        kname.innerHTML = '<b>' + KERNELS[k].n + '</b><br>' + KERNELS[k].d;
      }
    }
    function draw() {
      var shown = OUT.map(function (r, i) { return r.map(function (v, j) { return i * 26 + j < pos ? v / mx : null; }); });
      paint(co, shown, signed);
      var done = !cover && pos >= N;                    // finished: park the magnifier on the boot's edge (rows 11-13, cols 13-15, as in the next slide)
      var p = done ? 11 * 26 + 13 : Math.min(pos, N - 1), r = (p / 26) | 0, q = p % 26;
      win.setAttribute('x', q * 10); win.setAttribute('y', r * 10); cell.setAttribute('x', q * 10); cell.setAttribute('y', r * 10);
      var vis = (pos > 0 && pos < N) || done; win.setAttribute('opacity', vis || cover ? 1 : 0.0001); cell.setAttribute('opacity', vis ? 1 : 0);
      if (!cover) {
        var cr = done ? 11 : pos > 0 ? (((pos - 1) / 26) | 0) : 0, cq = done ? 13 : pos > 0 ? (pos - 1) % 26 : 0;
        pc.forEach(function (c, i) { var v = A[cr + ((i / 3) | 0)][cq + i % 3], col = gray(v * 255); c.textContent = v.toFixed(2); c.style.background = 'rgb(' + col.map(Math.round).join(',') + ')'; c.style.color = v > 0.55 ? C.night : C.ink2; });
        var s = OUT[cr][cq];
        res.textContent = (s > 0.005 ? '+' : s < -0.005 ? '−' : '') + Math.abs(s).toFixed(2);
        res.style.color = s > 0.05 ? C.amber : s < -0.05 ? C.azure : C.ink2;
        btnPlay.textContent = playing ? '⏸ Pausa' : '▶ Recorrer';
      }
    }
    var acc = 0, loop = api.raf(function (t, dt) {
      acc += dt * (cover ? 0.16 : 0.11);
      var n = Math.floor(acc); if (n > 0) { acc -= n; pos = Math.min(N, pos + n); draw(); }
      if (pos >= N) {
        if (cover) { acc = -320; pos = 0; var ks = Object.keys(KERNELS); setK(ks[(ks.indexOf(kn) + 1) % 2]); return; }
        stop(); return false;
      }
    });
    function play() { playing = true; acc = 0; loop.start(); draw(); }
    function stop() { playing = false; loop.stop(); draw(); }
    function restart() { stop(); pos = 0; draw(); if (!RM) play(); else { pos = N; draw(); } }
    setK(kn); draw();
    return {
      enter: function () { if (api.print) { pos = N; draw(); return; } restart(); },
      leave: function () { stop(); },
      final: function () { stop(); pos = N; draw(); }
    };
  });

  /* ---------------- fmaps: the 16 filters the CNN learned and what each one sees in the photo ---------------- */
  demo('fmaps', function (el, api) {
    var sel = 0, auto = true;
    var root = H('div', 'fm', el);
    var c1 = H('div', 'col', root); c1.style.gap = '.6em';
    H('p', 'lab3', c1, '<b>16 filtros aprendidos</b> · 3 × 3');
    var fg = H('div', 'fgrid', c1), fb = [];
    var mxw = 0; F.filters.forEach(function (fl) { fl.w.forEach(function (r) { r.forEach(function (v) { mxw = Math.max(mxw, Math.abs(v)); }); }); });
    F.filters.forEach(function (fl, i) {
      var b = H('button', '', fg); b.type = 'button'; b.setAttribute('aria-label', 'Filtro ' + (i + 1));
      paint(canvas(b, 3, 3), fl.w.map(function (r) { return r.map(function (v) { return v / mxw; }); }), signed);
      b.onclick = function () { auto = false; pick(i); }; fb.push(b);
    });
    H('p', 'cap', c1, 'ámbar = peso positivo · azul = negativo');
    var c2 = H('div', 'col', root); c2.style.gap = '.6em';
    H('p', 'lab3', c2, '<b>Sus 16 mapas</b> sobre el botín');
    var mg = H('div', 'mgrid', c2), md = [];
    F.act0.forEach(function (A, i) { var d = H('div', '', mg); paint(canvas(d, 26, 26), A, heat); d.onclick = function () { auto = false; pick(i); }; md.push(d); });
    var c3 = H('div', 'focus', root);
    var pair = H('div', 'pair', c3);
    var bigF = H('div', 'm3 k', pair); bigF.style.gridTemplateColumns = 'repeat(3,3.3em)';
    var bfc = range(9).map(function () { return H('span', '', bigF); });
    var bm = H('div', 'pplate', pair); var bmc = canvas(bm, 26, 26);
    var say = H('p', 'say', c3);
    function kind(w) {
      var v = (w[0][2] + w[1][2] + w[2][2]) - (w[0][0] + w[1][0] + w[2][0]), h = (w[2][0] + w[2][1] + w[2][2]) - (w[0][0] + w[0][1] + w[0][2]);
      var tot = Math.abs(w[0][0]) + Math.abs(w[0][1]) + Math.abs(w[0][2]) + Math.abs(w[1][0]) + Math.abs(w[1][1]) + Math.abs(w[1][2]) + Math.abs(w[2][0]) + Math.abs(w[2][1]) + Math.abs(w[2][2]);
      if (Math.abs(v) > 0.45 * tot && Math.abs(v) >= Math.abs(h)) return 'Parece un <b>detector de bordes verticales</b>, como el que hicimos a mano.';
      if (Math.abs(h) > 0.45 * tot) return 'Parece un <b>detector de bordes horizontales</b>: la suela, la caña.';
      var s = w[0][0] + w[0][1] + w[0][2] + w[1][0] + w[1][1] + w[1][2] + w[2][0] + w[2][1] + w[2][2];
      if (Math.abs(s) > 0.6 * tot) return s > 0 ? 'Casi todos sus pesos son positivos: responde a las <b>zonas claras</b> de la prenda.' : 'Casi todos sus pesos son negativos: se enciende en el <b>fondo oscuro</b> y en los huecos.';
      return 'Una mezcla: responde a <b>esquinas y diagonales</b>.';
    }
    function pick(i) {
      sel = i; var w = F.filters[i].w;
      fb.forEach(function (b, j) { b.classList.toggle('on', j === i); }); md.forEach(function (d, j) { d.classList.toggle('on', j === i); });
      bfc.forEach(function (c, k) { var v = w[(k / 3) | 0][k % 3]; c.textContent = (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(2); c.style.color = v >= 0 ? C.amber : C.azure; });
      paint(bmc, F.act0[i], heat);
      say.innerHTML = '<b>Filtro ' + (i + 1) + '.</b> ' + kind(w) + ' <span class="mu">Nadie lo programó: salió del entrenamiento.</span>';
    }
    var t0 = 0, loop = api.raf(function (t, dt) { if (!auto) return false; t0 += dt; if (t0 > 2200) { t0 = 0; pick((sel + 1) % 16); } });
    pick(0);
    return {
      step: function (s) { c2.style.opacity = s >= 1 ? 1 : 0.15; c3.style.opacity = s >= 2 ? 1 : 0; c2.style.transition = c3.style.transition = 'opacity .5s'; if (s >= 2 && auto && !RM && !api.print) loop.start(); },
      leave: function () { loop.stop(); },
      final: function () { c2.style.opacity = 1; c3.style.opacity = 1; pick(0); }
    };
  });

  /* ---------------- pool: max pooling 2x2, from a 4x4 example to a real map ---------------- */
  demo('pool', function (el, api) {
    var V = [[1, 3, 0, 2], [5, 2, 1, 0], [0, 1, 4, 6], [2, 0, 3, 1]];
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:2.4em;height:100%;align-items:center';
    var fg = H('div', 'fig', root);
    var svg = svgIn(fg, 900, 520, 'Una cuadrícula de 4 por 4 se resume en 2 por 2 quedándose con el máximo de cada ventana');
    var cs = 100, x0 = 40, y0 = 60, ox = 620, oy = 160;
    var cols = [C.amber, C.azure, C.mint, C.lilac];
    var wins = [], cellsT = [];
    for (var w = 0; w < 4; w++) {
      var wr = (w >> 1) * 2, wc = (w & 1) * 2;
      wins.push(S('rect', { x: x0 + wc * cs + 4, y: y0 + wr * cs + 4, width: 2 * cs - 8, height: 2 * cs - 8, rx: 14, fill: cols[w], 'fill-opacity': 0.12, stroke: cols[w], 'stroke-width': 4, opacity: 0 }, svg));
    }
    for (var r = 0; r < 4; r++) for (var q = 0; q < 4; q++) {
      S('rect', { x: x0 + q * cs + 10, y: y0 + r * cs + 10, width: cs - 20, height: cs - 20, rx: 10, fill: C.night3 }, svg);
      cellsT.push(txt(svg, x0 + q * cs + cs / 2, y0 + r * cs + cs / 2 + 14, String(V[r][q]), { 'text-anchor': 'middle', 'font-size': 40, 'font-weight': 700, fill: C.ink2, 'font-family': 'JetBrains Mono, monospace' }));
    }
    txt(svg, x0 + 2 * cs, y0 - 20, 'mapa de 4 × 4', { 'text-anchor': 'middle', fill: C.ink3, 'font-size': 24 });
    txt(svg, ox + cs, oy - 20, '2 × 2', { 'text-anchor': 'middle', fill: C.ink3, 'font-size': 24 });
    S('path', { d: 'M470 260 L590 260', stroke: C.ink3, 'stroke-width': 4, 'marker-end': '' }, svg);
    S('polygon', { points: '590,248 610,260 590,272', fill: C.ink3 }, svg);
    txt(svg, 530, 240, 'máx', { 'text-anchor': 'middle', fill: C.ink3, 'font-size': 22 });
    var outs = [];
    for (var w2 = 0; w2 < 4; w2++) {
      var rr = w2 >> 1, qq = w2 & 1, m = Math.max(V[rr * 2][qq * 2], V[rr * 2][qq * 2 + 1], V[rr * 2 + 1][qq * 2], V[rr * 2 + 1][qq * 2 + 1]);
      var g = S('g', { opacity: 0 }, svg);
      S('rect', { x: ox + qq * cs + 8, y: oy + rr * cs + 8, width: cs - 16, height: cs - 16, rx: 12, fill: cols[w2], 'fill-opacity': 0.2, stroke: cols[w2], 'stroke-width': 4 }, g);
      txt(g, ox + qq * cs + cs / 2, oy + rr * cs + cs / 2 + 14, String(m), { 'text-anchor': 'middle', 'font-size': 42, 'font-weight': 700, fill: C.ink, 'font-family': 'JetBrains Mono, monospace' });
      outs.push({ g: g, m: m, rr: rr, qq: qq });
    }
    var rt = H('div', 'col', root); rt.style.gap = '.6em';
    H('p', 'lab3', rt, '<b>Con un mapa real</b> · el borde vertical del botín');
    var pair = H('div', '', rt); pair.style.cssText = 'display:grid;grid-template-columns:1fr .5fr;gap:1em;align-items:end';
    var A = conv(norm(img(0)), KERNELS.vertical.k), mx = 0; A.forEach(function (r) { r.forEach(function (v) { mx = Math.max(mx, Math.abs(v)); }); });
    var A01 = A.map(function (r) { return r.map(function (v) { return Math.max(0, v) / mx; }); });
    var P = range(13).map(function (i) { return range(13).map(function (j) { return Math.max(A01[2 * i][2 * j], A01[2 * i][2 * j + 1], A01[2 * i + 1][2 * j], A01[2 * i + 1][2 * j + 1]); }); });
    var a = H('div', 'col', pair); a.style.gap = '.3em'; var pa = H('div', 'pplate', a); paint(canvas(pa, 26, 26), A01, function (v) { return heat(v * 255); }); H('p', 'cap', a, '26 × 26 = 676 números');
    var b = H('div', 'col', pair); b.style.gap = '.3em'; var pb = H('div', 'pplate', b); paint(canvas(pb, 13, 13), P, function (v) { return heat(v * 255); }); H('p', 'cap', b, '13 × 13 = 169');
    rt.style.transition = 'opacity .5s';
    function set(s) {
      for (var i = 0; i < 4; i++) { wins[i].setAttribute('opacity', s >= i + 1 ? 1 : 0); outs[i].g.setAttribute('opacity', s >= i + 1 ? 1 : 0); }
      cellsT.forEach(function (t, k) {
        var r = k >> 2, q = k & 3, w = (r >> 1) * 2 + (q >> 1), isMax = V[r][q] === outs[w].m && s >= w + 1;
        t.setAttribute('fill', isMax ? cols[w] : C.ink2);
      });
      rt.style.opacity = s >= 5 ? 1 : 0;
    }
    set(0);
    return { step: set, final: function () { set(5); } };
  });

  /* ---------------- shapes: the CNN as a table of tensors, synchronized with the code ---------------- */
  demo('shapes', function (el, api) {
    function glyph(kind, w, d, c) {
      var sv = '<svg viewBox="0 0 90 70" aria-hidden="true">';
      if (kind === 'flat') { for (var k = 0; k < 6; k++) sv += '<rect x="40" y="' + (4 + k * 11) + '" width="10" height="9" rx="2" fill="' + c + '"/>'; }
      else if (kind === 'dense') { for (var k2 = 0; k2 < 5; k2++) sv += '<circle cx="45" cy="' + (8 + k2 * 13.5) + '" r="5.5" fill="' + c + '"/>'; }
      else { var n = Math.min(d, 5); for (var j = n - 1; j >= 0; j--) sv += '<rect x="' + (45 - w / 2 + j * 5) + '" y="' + (35 - w / 2 - j * 5 + 6) + '" width="' + w + '" height="' + w + '" rx="3" fill="#0f1a29" stroke="' + c + '" stroke-width="2.5" opacity="' + (j ? 0.55 : 1) + '"/>'; }
      return sv + '</svg>';
    }
    var L = [['Input', '28 × 28 × 1', '—', glyph('t', 46, 1, C.ink)], ['Conv2D(16)', '26 × 26 × 16', '160', glyph('t', 42, 16, C.amber)],
             ['MaxPool', '13 × 13 × 16', '0', glyph('t', 24, 16, C.azure)], ['Conv2D(32)', '11 × 11 × 32', '4 640', glyph('t', 21, 32, C.amber)],
             ['MaxPool', '5 × 5 × 32', '0', glyph('t', 12, 32, C.azure)], ['Flatten', '800', '0', glyph('flat', 0, 0, C.ink3)], ['Dense(10)', '10', '8 010', glyph('dense', 0, 0, C.mint)]];
    var root = H('div', 'shp', el);
    var hd = H('div', 'r', root); ['', 'capa', 'forma de salida', 'parámetros'].forEach(function (t) { var e = H('span', 'lab3', hd, t); e.style.fontSize = '.85em'; });
    var rows = L.map(function (l) {
      var r = H('div', 'r', root);
      var g = H('span', 'g', r, l[3]), n = H('span', 'n', r, l[0]), s2 = H('span', 's', r, l[1]), p2 = H('span', 'p', r, l[2]);
      return [g, n, s2, p2];
    });
    var tot = H('div', 'tot', root, 'Total: <b class="num">12 810</b> parámetros · la densa: <span class="num">101 770</span>');
    function set(s) {
      rows.forEach(function (r, i) { var o = s === 0 || s >= 8 ? 1 : (i + 1 === s ? 1 : i + 1 < s ? 0.5 : 0.15); r.forEach(function (e) { e.style.opacity = o; }); r[1].style.color = i + 1 === s ? C.amber : ''; });
      tot.style.opacity = s >= 8 ? 1 : 0.15;
    }
    set(0);
    return { step: set, final: function () { set(8); } };
  });

  /* ---------------- softmax: ten probabilities that add up to 1 (real predictions of NB03) ---------------- */
  demo('softmax', function (el, api) {
    var cur = +(el.dataset.start || 0), net = 'cnn';
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:2.4em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.cssText += ';gap:.8em;align-items:center';
    var pl = H('div', 'pplate', lc); pl.style.width = 'min(100%, 17em)'; var cv = canvas(pl, 28, 28);
    var cap = H('p', 'lab3', lc);
    var th = H('div', 'thumbs', lc), tbs = [];
    F.samples.forEach(function (s, i) { var b = H('button', '', th); b.type = 'button'; b.setAttribute('aria-label', CL[s.label]); paint(canvas(b, 28, 28), s.px, gray); b.onclick = function () { cur = i; draw(true); }; tbs.push(b); });
    var rc = H('div', 'col', root); rc.style.gap = '.45em';
    var seg = H('div', 'seg', rc), bn = {};
    [['cnn', 'CNN · 12 810 parámetros'], ['densa', 'Densa · 101 770']].forEach(function (o) { var b = H('button', 'btn', seg, o[1]); b.type = 'button'; b.onclick = function () { net = o[0]; draw(true); }; bn[o[0]] = b; });
    var rows = CL.map(function (c) {
      var r = H('div', '', rc); r.style.cssText = 'display:grid;grid-template-columns:7.2em 1fr 4.2em;gap:.8em;align-items:center;font-size:1.15em';
      var l = H('span', '', r, c); var tr = H('span', '', r); tr.style.cssText = 'height:1.05em;border-radius:99px;background:var(--night-3);position:relative;overflow:hidden';
      var bar = H('i', '', tr); bar.style.cssText = 'position:absolute;left:0;top:0;bottom:0;width:0;border-radius:99px;background:var(--ink-3);transition:width .7s cubic-bezier(.16,1,.3,1)';
      var v = H('span', 'num', r); v.style.textAlign = 'right';
      return { l: l, bar: bar, v: v };
    });
    var sum = H('p', 'cap', rc);
    function draw() {
      var s = F.samples[cur], p = s[net], best = p.indexOf(Math.max.apply(null, p));
      paint(cv, s.px, gray); tbs.forEach(function (b, i) { b.classList.toggle('on', i === cur); });
      for (var k in bn) bn[k].classList.toggle('on', k === net);
      cap.innerHTML = 'La respuesta correcta: <b>' + CL[s.label] + '</b>';
      rows.forEach(function (r, i) {
        r.bar.style.width = (p[i] * 100).toFixed(1) + '%';
        r.bar.style.background = i === best ? (i === s.label ? C.amber : C.coral) : C.ink3;
        r.v.textContent = p[i] >= 0.005 ? Math.round(p[i] * 100) + ' %' : '0 %';
        r.l.style.color = i === s.label ? C.ink : C.ink3; r.l.style.fontWeight = i === s.label ? 700 : 400;
      });
      sum.innerHTML = 'Las 10 probabilidades suman <b class="num">' + p.reduce(function (a, b) { return a + b; }, 0).toFixed(2) + '</b>. La red elige la más alta.';
    }
    draw();
    return { step: function (s) { if (s >= 1 && cur !== 6) { cur = 6; draw(); } }, final: function () { draw(); } };
  });

  /* ---------------- duel: dense vs CNN, the real results of NB03 ---------------- */
  demo('duel', function (el, api) {
    var D = R.densa, Cn = R.cnn;
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.3em;height:100%';
    function panel(t) { var p = H('div', 'plate', root); p.style.cssText += ';padding:1em 1.1em;display:flex;flex-direction:column;gap:.5em;transition:opacity .5s'; H('p', 'lab3', p, t); return p; }
    function bars(p, a, b, fmt, mx, note) {
      var box = H('div', 'col', p); box.style.cssText += ';gap:.9em;flex:1;justify-content:center';
      [['Densa', a, C.azure], ['CNN', b, C.amber]].forEach(function (o) {
        var r = H('div', 'col', box); r.style.gap = '.3em';
        H('div', '', r, '<span style="font-size:1.15em;color:var(--ink-2)">' + o[0] + '</span> <b class="num" style="font-size:1.7em;color:' + o[2] + ';float:right">' + fmt(o[1]) + '</b>');
        var tr = H('div', '', r); tr.style.cssText = 'height:1.2em;border-radius:99px;background:var(--night-3);overflow:hidden';
        var i = H('i', '', tr); i.style.cssText = 'display:block;height:100%;border-radius:99px;background:' + o[2] + ';width:' + (o[1] / mx * 100).toFixed(1) + '%';
      });
      if (note) H('p', 'cap', p, note);
    }
    var pct = function (v) { return f(v * 100, 1) + ' %'; };
    var p1 = panel('<b>1 · Parámetros</b> que aprende'); bars(p1, D.params, Cn.params, function (v) { return v.toLocaleString('es-EC').replace(/,/g, ' ').replace(/\./g, ' '); }, D.params, '8 veces menos: la CNN comparte sus filtros.');
    var p2 = panel('<b>2 · Examen final</b> · 10 000 fotos'); bars(p2, D.test, Cn.test, pct, 1, 'La CNN acierta un poco más con mucho menos.');
    var p3 = panel('<b>3 · Mover la prenda</b> unos píxeles');
    var fg = H('div', 'fig', p3); fg.style.flex = '1';
    var svg = svgIn(fg, 400, 330, 'Exactitud de las dos redes cuando la prenda se mueve de 0 a 4 píxeles');
    var sx = lin(0, 4, 48, 380), sy = lin(0, 1, 290, 16);
    [0, 0.5, 1].forEach(function (v) { S('line', { x1: 48, x2: 380, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 40, sy(v) + 7, Math.round(v * 100) + '', { 'text-anchor': 'end', 'font-size': 18, fill: C.ink3 }); });
    [0, 1, 2, 3, 4].forEach(function (v) { txt(svg, sx(v), 318, v + ' px', { 'text-anchor': 'middle', 'font-size': 18, fill: C.ink3 }); });
    [[D, C.azure], [Cn, C.amber]].forEach(function (o) {
      var ys = [o[0].test, o[0].shift[1], o[0].shift[2], o[0].shift[3], o[0].shift[4]];
      S('polyline', { points: ys.map(function (v, i) { return sx(i) + ',' + sy(v); }).join(' '), fill: 'none', stroke: o[1], 'stroke-width': 5, 'stroke-linejoin': 'round' }, svg);
      ys.forEach(function (v, i) { S('circle', { cx: sx(i), cy: sy(v), r: 7, fill: o[1] }, svg); });
      txt(svg, sx(2) + 10, sy(ys[2]) + (o[1] === C.amber ? -14 : 30), pct(ys[2]), { 'font-size': 21, 'font-weight': 700, fill: o[1] });
    });
    H('p', 'cap', p3, 'Con 2 px la densa se cae; la CNN aguanta. Con 4 px caen las dos.');
    var p4 = panel('<b>4 · Mezclar los píxeles</b> (siempre igual)'); bars(p4, D.mezclada, Cn.mezclada, pct, 1, 'A la densa le da igual. A la CNN le duele: su suposición ya no es cierta.');
    var P = [p1, p2, p3, p4];
    function set(s) { P.forEach(function (p, i) { p.style.opacity = s >= i + 1 ? 1 : 0.12; }); }
    set(0);
    return { step: set, final: function () { set(4); } };
  });
})();
