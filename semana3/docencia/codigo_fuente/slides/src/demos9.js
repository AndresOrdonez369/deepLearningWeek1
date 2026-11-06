/* Demos · Semana 3 · Tema 2: reutilizar y explicar.
   Every number comes from the real runs of NB06 (tools/run_tema2.py → window.T2); photos from window.FMNIST and window.FMX. */
(function () {
  var T = window.T2, F = window.FMNIST, CL = F.clases, W = window.W2, W3 = window.W3, pc = W3.pc;
  var MONO = 'JetBrains Mono, monospace';
  var NIGHT2 = [15, 26, 41], AMB = [255, 181, 65], CORAL = [253, 116, 102], INK = [241, 246, 250];
  function mix(a, b, t) { t = clamp(t, 0, 1); return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function hot(v) { return v < 0.6 ? mix(NIGHT2, AMB, v / 0.6) : mix(AMB, [255, 236, 190], (v - 0.6) / 0.4); }   // 0..1 heat
  var PHOTOS = {};                                    // label -> 28x28 photo (first test photo of each class)
  F.samples.concat(window.FMX || []).forEach(function (s) { if (!PHOTOS[s.label]) PHOTOS[s.label] = s.px; });
  var PH = {}; F.samples.forEach(function (s) { PH[s.i] = s.px; });   // by test index (the explained photos: 0, 4, 18)
  function thumb(parent, label, cls) {
    var p = H('span', cls || 'th9', parent); W.paint(W.canvas(p, 28, 28), PHOTOS[label], W.gray); return p;
  }
  var LOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2.5"/><path class="sh" d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>';

  /* ---------------- transfer: a network that never saw tops lends its eyes; we only teach it a new head ---------------- */
  demo('transfer', function (el, api) {
    var OLD = [1, 3, 5, 7, 8, 9], NEW = [0, 2, 4, 6], s0 = 0, ti = 0;
    var root = H('div', 'col', el); root.style.cssText += ';gap:1.1em;height:100%;justify-content:center';
    var row = H('div', 'tf9', root);
    var inp = H('div', 'bk9 in', row); var ic = H('div', 'pplate', inp); var icv = W.canvas(ic, 28, 28); H('b', '', inp, 'la foto');
    H('span', 'ar9', row, '→');
    var base = H('div', 'base9', row);
    var BL = [['Conv2D', '16 filtros'], ['MaxPooling', 'resumen'], ['Conv2D', '32 filtros'], ['MaxPooling', 'resumen'], ['Flatten', '800 números']];
    var blocks = BL.map(function (b, i) { var d = H('div', 'bk9', base, '<span class="lk">' + LOCK + '</span><b>' + b[0] + '</b><span>' + b[1] + '</span>'); return d; });
    H('span', 'ar9', row, '→');
    var head = H('div', 'bk9 head', row, '<b class="ht"></b><span class="hs"></span>');
    var lab = H('div', 'lab9', root);
    var lb1 = H('div', '', lab, '<span>La parte que <b>mira</b>: bordes, esquinas y formas · <b class="num">4 800</b> números</span>');
    var lb2 = H('div', '', lab, '<span>La parte que <b>decide</b></span>');
    var cls = H('div', 'cls9', root);
    var msg = H('p', 'say', root); msg.style.textAlign = 'center';
    function draw() {
      var set = s0 >= 2 ? NEW : OLD;
      head.querySelector('.ht').textContent = 'Dense(' + set.length + ')';
      head.querySelector('.hs').textContent = s0 >= 2 ? 'cabeza nueva' : 'cabeza vieja';
      head.classList.toggle('new', s0 >= 2);
      cls.innerHTML = '';
      set.forEach(function (c) { var t = H('div', 'cl9', cls); thumb(t, c); H('span', '', t, CL[c]); });
      blocks.forEach(function (b) { b.classList.toggle('frozen', s0 === 2); b.classList.toggle('fine', s0 >= 3); });
      base.classList.toggle('frozen', s0 === 2); base.classList.toggle('fine', s0 >= 3);
      msg.innerHTML = s0 <= 1 ? 'Primero aprende con <b>6 prendas que no son de arriba</b>: acierta el <b class="num">' + pc(T.base_6clases) + '</b>. Nunca vio una camiseta.'
        : s0 === 2 ? '<b>Congelar:</b> sus <b class="num">4 800</b> números quedan fijos y solo se entrenan los <b class="num">' + W3.miles(T.transfer['5'].entrenables_congelada) + '</b> de la cabeza nueva, para <b>4 prendas de arriba</b> muy parecidas.'
        : '<b>Ajuste fino:</b> después se descongela todo y se entrena con <b>pasos 10 veces más pequeños</b> (<code>learning rate 0.0001</code>), para no borrar lo que sabía.';
      W.paint(icv, PHOTOS[set[ti % set.length]], W.gray);
    }
    var acc = 0, loop = api.raf(function (t, dt) { acc += dt; if (acc > 1300) { acc = 0; ti++; W.paint(icv, PHOTOS[(s0 >= 2 ? NEW : OLD)[ti % (s0 >= 2 ? 4 : 6)]], W.gray); } });
    draw();
    return {
      step: function (s) { s0 = s; draw(); },
      enter: function () { if (!RM && !api.print) loop.start(); }, leave: function () { loop.stop(); },
      final: function () { s0 = 3; draw(); }
    };
  });

  /* ---------------- transferbars: 5, 20 and 100 photos per class: from scratch vs frozen vs fine-tuned ---------------- */
  demo('transferbars', function (el, api) {
    var N = ['5', '20', '100'], K = [['desde_cero', 'desde cero', C.azure], ['congelada', 'congelada', C.mint], ['ajuste_fino', 'ajuste fino', C.amber]];
    var svg = svgIn(el, 1500, 600, 'Exactitud con 5, 20 y 100 fotos por clase: desde cero, congelada y con ajuste fino');
    var y0 = 470, sy = lin(0, 0.8, y0, 40);
    [0, 0.2, 0.4, 0.6, 0.8].forEach(function (v) { S('line', { x1: 110, x2: 1460, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 96, sy(v) + 8, Math.round(v * 100) + '\u00a0%', { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 }); });
    S('line', { x1: 110, x2: 1460, y1: sy(0.25), y2: sy(0.25), stroke: C.ink3, 'stroke-width': 3, 'stroke-dasharray': '12 10' }, svg);
    var G = N.map(function (n, gi) {
      var g = S('g', {}, svg), gx = 190 + gi * 440;
      K.forEach(function (k, j) {
        var v = T.transfer[n][k[0]], x = gx + j * 120, y = sy(v);
        S('rect', { x: x, y: y, width: 96, height: y0 - y, rx: 10, fill: k[2] }, g);
        txt(g, x + 48, y - 14, f(v * 100, 1), { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 700, fill: k[2], 'font-family': MONO });
      });
      txt(g, gx + 168, y0 + 44, n + ' fotos por clase', { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: C.ink });
      txt(g, gx + 168, y0 + 76, '(' + 4 * n + ' fotos para estudiar)', { 'text-anchor': 'middle', 'font-size': 21, fill: C.ink3 });
      g.style.transition = 'opacity .5s';
      return g;
    });
    var d5 = T.transfer['5'], up = S('g', {}, svg);
    S('path', { d: 'M 238 ' + (sy(d5.desde_cero) - 52) + ' C 238 ' + (sy(d5.congelada) - 90) + ', 358 ' + (sy(d5.congelada) - 90) + ', 358 ' + (sy(d5.congelada) - 52), fill: 'none', stroke: C.mint, 'stroke-width': 4 }, up);
    txt(up, 298, sy(d5.congelada) - 96, '+' + Math.round((d5.congelada - d5.desde_cero) * 100) + ' puntos', { 'text-anchor': 'middle', 'font-size': 25, 'font-weight': 700, fill: C.mint });
    var leg = S('g', {}, svg);
    K.forEach(function (k, j) { S('rect', { x: 190 + j * 300, y: 572, width: 26, height: 26, rx: 6, fill: k[2] }, leg); txt(leg, 228 + j * 300, 594, k[1], { 'font-size': 23, fill: C.ink2 }); });
    S('line', { x1: 1100, x2: 1150, y1: 585, y2: 585, stroke: C.ink3, 'stroke-width': 3, 'stroke-dasharray': '10 8' }, leg); txt(leg, 1162, 594, 'adivinar: 25 %', { 'font-size': 23, fill: C.ink2 });
    function set(s) { G.forEach(function (g, i) { g.style.opacity = s >= i + 1 ? 1 : 0.07; }); up.style.opacity = s >= 1 ? 1 : 0; }
    up.style.transition = 'opacity .5s';
    set(0);
    return { step: set, final: function () { set(3); } };
  });

  /* ---------------- mapas: where did the network look? occlusion (cover with a hand), Grad-CAM and gradient x image ---------------- */
  var METHODS = {
    oclusion: { n: 'Oclusión', d: '<b>Tapar con la mano.</b> Un cuadro negro de 6 × 6 recorre la foto; en cada lugar medimos cuánto baja la confianza de la red. Brillante = taparlo ahí le cuesta más.' },
    gradcam: { n: 'Grad-CAM', d: '<b>Un mapa de calor.</b> Usa los gradientes de la última capa convolucional (11 × 11) para pintar qué zonas empujaron hacia la respuesta (Selvaraju et al., 2017).' },
    gradx: { n: 'Gradiente × imagen', d: '<b>El más barato.</b> Cuánto cambia la respuesta si se mueve cada píxel, por el brillo del píxel. Mira lo mucho que se parece a la foto misma.' }
  };
  function p98(M) { var a = [].concat.apply([], M).filter(function (v) { return v > 0; }).sort(function (x, y) { return x - y; }); return a.length ? a[Math.floor(a.length * 0.98)] : 1; }
  function overlay(px, M, mask) {               // dim photo + heat on top (mask: which pixels are already revealed)
    var mx = p98(M);
    return px.map(function (r, i) { return r.map(function (p, j) { var base = mix(NIGHT2, INK, p / 255 * 0.42), v = mask && !mask(i, j) ? 0 : clamp(M[i][j] / (mx || 1), 0, 1); return mix(base, hot(v), Math.pow(v, 0.7)); }); });
  }
  function paintRGB(c, A) {
    var h = A.length, w = A[0].length, ctx = c.getContext('2d'), im = ctx.createImageData(w, h);
    for (var r = 0; r < h; r++) for (var q = 0; q < w; q++) { var col = A[r][q], k = (r * w + q) * 4; im.data[k] = col[0]; im.data[k + 1] = col[1]; im.data[k + 2] = col[2]; im.data[k + 3] = 255; }
    ctx.putImageData(im, 0, 0);
  }
  demo('mapas', function (el, api) {
    var cur = 0, meth = 'oclusion', s0 = 0, tw = null;
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,6fr) minmax(0,7fr);gap:2.4em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.cssText += ';align-items:center;gap:.6em';
    var pl = H('div', 'pplate', lc); pl.style.width = 'min(100%, 19em)';
    var cv = W.canvas(pl, 28, 28);
    var ov = svgIn(pl, 280, 280, 'Cuadro que tapa una parte de la foto');
    var patch = S('rect', { width: 60, height: 60, fill: C.night, 'fill-opacity': 0.92, stroke: C.ink, 'stroke-width': 3, opacity: 0 }, ov);
    var cap = H('p', 'lab3', lc); cap.style.textAlign = 'center';
    var rc = H('div', 'col', root); rc.style.gap = '1em';
    var th = H('div', 'gar9', rc);
    var gbs = T.mapas.map(function (m, i) {
      var b = H('button', 'btn', th); b.type = 'button';
      var t = H('span', 'th9 sm', b); W.paint(W.canvas(t, 28, 28), PH[m.i], W.gray);
      H('span', '', b, CL[m.label] + ' · <b class="num">' + Math.round(m.p * 100) + ' %</b>');
      b.onclick = function () { if (tw) tw.stop(); cur = i; show(); };
      return b;
    });
    var seg = H('div', 'seg', rc), mbs = {};
    Object.keys(METHODS).forEach(function (k) { var b = H('button', 'btn', seg, METHODS[k].n); b.type = 'button'; b.onclick = function () { if (tw) tw.stop(); meth = k; show(); }; mbs[k] = b; });
    var desc = H('p', 'say', rc);
    H('div', 'legend', rc, '<span><i style="background:#0f1a29;border:2px solid var(--line)"></i>no influyó</span><span><i style="background:var(--amber)"></i>influyó</span><span><i style="background:#ffecbe"></i>influyó mucho</span>');
    function show(mask, pi, pj) {
      var m = T.mapas[cur];
      paintRGB(cv, overlay(PH[m.i], m[meth], mask));
      patch.setAttribute('opacity', mask ? 1 : 0);
      if (mask) { patch.setAttribute('x', pj * 10); patch.setAttribute('y', pi * 10); }
      cap.innerHTML = '<b>' + CL[m.label] + '</b> · la red dice ' + CL[m.label] + ' con ' + Math.round(m.p * 100) + '\u00a0%';
      gbs.forEach(function (b, i) { b.classList.toggle('on', i === cur); });
      Object.keys(mbs).forEach(function (k) { mbs[k].classList.toggle('on', k === meth); });
      desc.innerHTML = METHODS[meth].d;
    }
    function sweep() {                            // the occlusion patch slides with stride 2 (12 x 12 positions), revealing the map
      if (tw) tw.stop();
      if (api.print || RM) { show(); return; }
      var P = []; for (var i = 0; i <= 22; i += 2) for (var j = 0; j <= 22; j += 2) P.push([i, j]);
      tw = tween(3600, function (k) {
        var q = Math.min(P.length - 1, Math.floor(k * P.length)), pi = P[q][0], pj = P[q][1];
        if (k >= 1) { show(); return; }
        show(function (r, c) { return r < pi || (r < pi + 6 && c < pj + 6); }, pi, pj);
      });
    }
    show();
    return {
      step: function (s) { var p = s0; s0 = s; meth = s <= 1 ? 'oclusion' : s === 2 ? 'gradcam' : 'gradx'; if (s === 1 && p !== 1) sweep(); else { if (tw) tw.stop(); show(); } },
      leave: function () { if (tw) tw.stop(); },
      final: function () { meth = 'gradcam'; show(); }
    };
  });

  /* ---------------- cordura: the sanity check (Adebayo et al., 2018): erase what the network learned and explain again ---------------- */
  demo('cordura', function (el, api) {
    var m = T.mapas[0], R0 = T.cordura_mapas, Cr = T.cordura;
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,4.5fr) minmax(0,7.5fr);grid-template-rows:minmax(0,1fr);gap:2.2em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.cssText += ';align-items:center;gap:.5em';
    var pp = H('div', 'pplate', lc); pp.style.width = 'min(100%, 9em)'; W.paint(W.canvas(pp, 28, 28), PH[m.i], W.gray);
    H('p', 'lab3', lc, '<b>La foto</b> · botín').style.textAlign = 'center';
    if (el.dataset.at) { var an = H('div', 'analog', lc, '<span class="t">' + el.dataset.at + '</span><p>' + el.dataset.ap + '</p>'); an.style.cssText += ';margin-top:.6em;align-self:stretch'; }
    var g = H('div', 'cg9', root);
    H('span', '', g); H('p', 'ch9', g, 'Grad-CAM'); H('p', 'ch9', g, 'Gradiente<br>× imagen');
    function heat(M) { var mx = p98(M); return M.map(function (r) { return r.map(function (v) { return hot(clamp(v / (mx || 1), 0, 1)); }); }); }
    function rowOf(lab, sub, a, b) {
      var l = H('div', 'rl9', g, '<b>' + lab + '</b><span>' + sub + '</span>');
      var cells = [a, b].map(function (M) { var p = H('div', 'pplate', g); paintRGB(W.canvas(p, 28, 28), heat(M)); return p; });
      return [l].concat(cells);
    }
    var r1 = rowOf('Red entrenada', 'acierta el ' + pc(T.cnn10), m.gradcam, m.gradx);
    var r2 = rowOf('Pesos al azar', 'no sabe nada', R0.gradcam, R0.gradx);
    H('span', '', g);
    var v1 = H('div', 'vd9 ok', g, '<b class="num">' + f(Cr.gradcam, 2) + '</b><span>cambia: <b>pasa</b></span>');
    var v2 = H('div', 'vd9 bad', g, '<b class="num">' + f(Cr.gradx, 2) + '</b><span>casi igual: <b>no pasa</b></span>');
    function set(s) {
      r1.forEach(function (e) { e.style.opacity = s >= 1 ? 1 : 0.1; });
      r2.forEach(function (e) { e.style.opacity = s >= 2 ? 1 : 0.06; });
      [v1, v2].forEach(function (e) { e.style.opacity = s >= 3 ? 1 : 0; });
    }
    r1.concat(r2, [v1, v2]).forEach(function (e) { e.style.transition = 'opacity .5s'; });
    set(0);
    return { step: set, final: function () { set(3); } };
  });

  /* ---------------- credito: what matters in general (permutation importance) vs what weighed in her case (SHAP) ---------------- */
  var CO = T.coop, SO = CO.socia, V = SO.valores;
  var NAMES = { ingreso: 'Ingreso', carga: 'Carga de la cuota', antiguedad: 'Antigüedad', atrasos: 'Atrasos', garante: 'Garante', ahorro: 'Ahorro', rural: 'Zona rural' };
  var HERS = { ingreso: '$' + Math.round(V.ingreso), carga: Math.round(V.carga * 100) + ' % del ingreso', antiguedad: Math.round(V.antiguedad) + ' mes', atrasos: Math.round(V.atrasos) + ' en 12 meses',
               garante: V.garante ? 'sí' : 'no tiene', ahorro: f(V.ahorro, 1) + ' meses', rural: V.rural ? 'rural' : 'urbana' };
  demo('credito', function (el, api) {
    var s0 = 0, tws = [];
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:1.8em;height:100%';
    var lp = H('div', 'plate', root); lp.style.cssText += ';padding:1em 1.2em;display:flex;flex-direction:column;gap:.6em;transition:opacity .5s';
    H('p', 'lab3', lp, '<b>1 · En general</b> · importancia por permutación');
    H('p', 'cap', lp, 'Cuánto baja el AUC si se mezcla esa columna en los 1 200 socios de prueba.').style.marginTop = '0';
    var imp = Object.keys(CO.importancia).sort(function (a, b) { return CO.importancia[b] - CO.importancia[a]; });
    var mx = CO.importancia[imp[0]];
    var irows = imp.map(function (k) {
      var r = H('div', 'ir9', lp), v = CO.importancia[k];
      H('span', 'n', r, NAMES[k]);
      var tr = H('span', 'tr', r), i = H('i', '', tr); i.style.width = (Math.max(0, v) / mx * 100).toFixed(1) + '%';
      H('b', 'num', r, f(v, 3));
      return { k: k, r: r };
    });
    var rp = H('div', 'plate', root); rp.style.cssText += ';padding:1em 1.2em;display:flex;flex-direction:column;gap:.4em;transition:opacity .5s';
    H('p', 'lab3', rp, '<b>2 · En su caso</b> · SHAP reparte su probabilidad entre sus datos, como el mérito de un gol entre los jugadores');
    var fg = H('div', 'fig', rp); fg.style.flex = '1';
    var order = Object.keys(SO.shap).sort(function (a, b) { return Math.abs(SO.shap[b]) - Math.abs(SO.shap[a]); });
    var nR = order.length + 2, Wd = 1000, Hd = 58 * nR + 44, svg = svgIn(fg, Wd, Hd, 'Cascada SHAP de la socia: desde el promedio hasta su probabilidad');
    var sx = lin(0, 0.7, 330, 970), y = function (i) { return 8 + i * 58; };
    [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7].forEach(function (v) { S('line', { x1: sx(v), x2: sx(v), y1: 6, y2: Hd - 36, stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, sx(v), Hd - 8, f(v, 1), { 'text-anchor': 'middle', 'font-size': 22, fill: C.ink3, 'font-family': MONO }); });
    S('line', { x1: sx(0.5), x2: sx(0.5), y1: 6, y2: Hd - 36, stroke: C.coral, 'stroke-width': 3, 'stroke-dasharray': '10 8' }, svg);
    txt(svg, sx(0.5) + 10, 30, 'desde 0.5: rechazar', { 'font-size': 22, fill: C.coral });
    function rowLab(i, a, b) { txt(svg, 316, y(i) + 26, a, { 'text-anchor': 'end', 'font-size': 27, 'font-weight': 600, fill: C.ink }); if (b) txt(svg, 316, y(i) + 50, b, { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 }); }
    rowLab(0, 'Promedio de todos', 'el punto de partida');
    var bars = [];
    var b0 = S('rect', { x: sx(0), y: y(0) + 11, height: 34, width: 0, rx: 6, fill: C.ink3 }, svg), t0 = txt(svg, 0, y(0) + 35, f(SO.base, 2), { 'font-size': 26, 'font-weight': 700, fill: C.ink2, 'font-family': MONO });
    bars.push({ r: b0, t: t0, a: 0, b: SO.base, lab: f(SO.base, 2) });
    var acc = SO.base;
    order.forEach(function (k, j) {
      var v = SO.shap[k], a = acc, b = acc + v; acc = b;
      rowLab(j + 1, NAMES[k], HERS[k]);
      var r = S('rect', { x: sx(Math.min(a, b)), y: y(j + 1) + 11, height: 34, width: 0, rx: 6, fill: v > 0 ? C.coral : C.mint }, svg);
      var t = txt(svg, 0, y(j + 1) + 35, (v > 0 ? '+' : '−') + f(Math.abs(v), 2), { 'font-size': 26, 'font-weight': 700, fill: v > 0 ? C.coral : C.mint, 'font-family': MONO });
      bars.push({ r: r, t: t, a: a, b: b, k: k });
    });
    rowLab(nR - 1, 'Su probabilidad', 'de mora · rechazada');
    var bf = S('rect', { x: sx(0), y: y(nR - 1) + 11, height: 34, width: 0, rx: 6, fill: C.coral }, svg), tf = txt(svg, 0, y(nR - 1) + 35, f(SO.prob, 2), { 'font-size': 26, 'font-weight': 700, fill: C.coral, 'font-family': MONO });
    bars.push({ r: bf, t: tf, a: 0, b: SO.prob });
    var hi1 = irows.filter(function (o) { return o.k === 'carga'; })[0].r, hi2 = S('rect', { x: 8, y: y(1) + 4, width: Wd - 16, height: 54, rx: 10, fill: 'none', stroke: C.amber, 'stroke-width': 3, opacity: 0 }, svg);
    function put(o, k) {
      var lo = Math.min(o.a, o.b), w = Math.abs(o.b - o.a) * k;
      o.r.setAttribute('x', o.b >= o.a ? sx(o.a) : sx(o.a) - (sx(o.a) - sx(o.b)) * k);
      o.r.setAttribute('width', Math.max(0, (sx(lo + w) - sx(lo))).toFixed(1));
      o.t.setAttribute('x', sx(Math.max(o.a, o.b)) + 12); o.t.style.opacity = k > 0.6 ? 1 : 0;
    }
    function set(s, still) {
      tws.forEach(function (t) { t.stop(); }); tws = [];
      var p = s0; s0 = s;
      lp.style.opacity = s >= 1 ? 1 : 0.12; rp.style.opacity = s >= 2 ? 1 : 0.12;
      if (s >= 2 && p < 2 && !still && !api.print && !RM) bars.forEach(function (o, i) { put(o, 0); setTimeout(function () { tws.push(tween(450, function (k) { put(o, k); })); }, i * 260); });
      else bars.forEach(function (o) { put(o, s >= 2 ? 1 : 0); });
      hi1.classList.toggle('hi9', s >= 3); hi2.setAttribute('opacity', s >= 3 ? 1 : 0);
    }
    set(0);
    return { step: function (s) { set(s); }, final: function () { s0 = 0; set(3, true); } };
  });

  /* ---------------- contra: the counterfactual, what would have to change for her to be approved? ----------------
     The three buttons are real NB06 results. In between, the sliders interpolate on the logit scale through those three
     points (illustrative, not the network itself): logit p = L0 + a (late payments - 2) + b (burden - her burden). */
  demo('contra', function (el, api) {
    var p0 = SO.prob, p1 = CO.sin_atrasos_prob, cf = CO.contrafactual_carga, ing = V.ingreso, c0 = V.carga;
    var lg = function (p) { return Math.log(p / (1 - p)); }, L0 = lg(p0), a = (lg(p1) - L0) / -V.atrasos, b = (lg(cf.prob) - L0) / (cf.carga - c0);
    var st = { atr: V.atrasos, carga: c0 };
    function prob() { return 1 / (1 + Math.exp(-(L0 + a * (st.atr - V.atrasos) + b * (st.carga - c0)))); }
    var root = H('div', '', el); root.style.cssText = 'display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:2.4em;height:100%;align-items:center';
    var lc = H('div', 'col', root); lc.style.gap = '1.2em';
    var pres = H('div', 'seg', lc), PR = [['Su caso', V.atrasos, c0], ['Sin los 2 atrasos', 0, c0], ['Cuota de $' + Math.round(cf.carga * ing), V.atrasos, cf.carga]];
    var pbs = PR.map(function (q, i) { var bb = H('button', 'btn', pres, q[0]); bb.type = 'button'; bb.onclick = function () { st.atr = q[1]; st.carga = q[2]; show(); }; return bb; });
    var c1 = H('div', 'ctrl', lc); c1.style.gridTemplateColumns = '9em 1fr';
    H('label', '', c1, 'atrasos');
    var sa = H('div', 'seg', c1), abs = [0, 1, 2].map(function (k) { var bb = H('button', 'btn', sa, String(k)); bb.type = 'button'; bb.onclick = function () { st.atr = k; show(); }; return bb; });
    var c2 = H('div', 'ctrl', lc); c2.style.gridTemplateColumns = '9em 1fr 5.5em';
    H('label', '', c2, 'cuota al mes');
    var inp = H('input', '', c2); inp.type = 'range'; inp.min = 100; inp.max = 165; inp.step = 1; inp.setAttribute('aria-label', 'cuota mensual en dólares');
    var oc = H('output', '', c2);
    inp.addEventListener('input', function () { st.carga = +inp.value / ing; show(); });
    var note = H('p', 'cap', lc, 'Los 3 botones son cálculos reales de la red del NB06. Los controles interpolan entre ellos: es ilustrativo.');
    var rc = H('div', 'plate', root); rc.style.cssText += ';padding:1.6em 1.8em;display:flex;flex-direction:column;gap:1em';
    H('p', 'lab3', rc, '<b>Su probabilidad de caer en mora</b>');
    var big = H('p', 'bigread', rc); big.style.fontSize = '5em';
    var tr = H('div', 'gauge9', rc), fill = H('i', '', tr), th = H('span', 'th', tr);
    H('div', 'gl9', rc, '<span>0 %</span><span>umbral: 50 %</span><span>100 %</span>');
    var ver = H('p', 'vr9', rc);
    function show() {
      var p = prob(), ok = p < 0.5;
      big.textContent = Math.round(p * 100) + '\u00a0%'; big.style.color = ok ? C.mint : C.coral;
      fill.style.width = (p * 100).toFixed(1) + '%'; fill.style.background = ok ? C.mint : C.coral;
      ver.innerHTML = ok ? '<b style="color:var(--mint)">Aprobada</b> · queda por debajo del umbral' : '<b style="color:var(--coral)">Rechazada</b> · queda por encima del umbral';
      abs.forEach(function (bb, k) { bb.classList.toggle('on', k === st.atr); });
      var cu = st.carga * ing; inp.value = Math.round(cu);
      oc.textContent = '$' + Math.round(cu);
      pbs.forEach(function (bb, i) { bb.classList.toggle('on', st.atr === PR[i][1] && Math.abs(st.carga - PR[i][2]) < 1e-6); });
    }
    show();
    return {
      step: function (s) { var q = PR[Math.min(2, s)]; st.atr = q[1]; st.carga = q[2]; show(); },
      final: function () { st.atr = V.atrasos; st.carga = c0; show(); }
    };
  });

  /* ---------------- zona: does it treat everybody alike? rural vs urban, with and without the rural column ---------------- */
  demo('zona', function (el, api) {
    var A = CO.por_zona, B = CO.sin_rural, s0 = 0, sin = false;
    var root = H('div', 'col', el); root.style.cssText += ';gap:.7em;height:100%';
    var top = H('div', 'row', root); top.style.cssText += ';justify-content:space-between';
    var seg = H('div', 'seg', top);
    var bC = H('button', 'btn', seg, 'con la columna «rural» · AUC ' + f(CO.auc, 2)), bS = H('button', 'btn', seg, 'sin la columna · AUC ' + f(B.auc, 2));
    bC.type = bS.type = 'button'; bC.onclick = function () { sin = false; draw(); }; bS.onclick = function () { sin = true; draw(); };
    H('div', 'legend', top, '<span><i style="background:var(--lilac)"></i>rural (' + A.rural.n + ' socios)</span><span><i style="background:var(--azure)"></i>urbana (' + A.urbana.n + ')</span>');
    var fg = H('div', 'fig plate', root); fg.style.flex = '1';
    var svg = svgIn(fg, 1500, 520, 'Mora real, rechazo y falsas alarmas por zona');
    var y0 = 420, sy = lin(0, 0.18, y0, 40);
    [0, 0.05, 0.1, 0.15].forEach(function (v) { S('line', { x1: 100, x2: 1460, y1: sy(v), y2: sy(v), stroke: C.grid, 'stroke-width': 2 }, svg); txt(svg, 86, sy(v) + 8, Math.round(v * 100) + '\u00a0%', { 'text-anchor': 'end', 'font-size': 21, fill: C.ink3 }); });
    var MET = [['mora_real', 'Mora real', 'cuántos sí cayeron en mora'], ['rechazo', 'Rechazados', 'a cuántos les dice «no»'], ['falsa_alarma', 'Falsas alarmas', 'rechazados que sí habrían pagado']];
    var G = MET.map(function (m, gi) {
      var g = S('g', {}, svg), gx = 200 + gi * 440, bars = [];
      [['rural', C.lilac], ['urbana', C.azure]].forEach(function (z, j) {
        var r = S('rect', { x: gx + j * 150, width: 120, rx: 10, fill: z[1], y: y0, height: 0 }, g);
        var t = txt(g, gx + j * 150 + 60, y0 - 12, '', { 'text-anchor': 'middle', 'font-size': 27, 'font-weight': 700, fill: z[1], 'font-family': MONO });
        r.style.transition = 'y .6s cubic-bezier(.16,1,.3,1), height .6s cubic-bezier(.16,1,.3,1)'; t.style.transition = 'y .6s cubic-bezier(.16,1,.3,1)';
        bars.push({ z: z[0], r: r, t: t });
      });
      txt(g, gx + 135, y0 + 44, m[1], { 'text-anchor': 'middle', 'font-size': 28, 'font-weight': 700, fill: C.ink });
      txt(g, gx + 135, y0 + 76, m[2], { 'text-anchor': 'middle', 'font-size': 21, fill: C.ink3 });
      g.style.transition = 'opacity .5s';
      return { g: g, bars: bars, k: m[0] };
    });
    function draw() {
      var D = sin ? B : A;
      bC.classList.toggle('on', !sin); bS.classList.toggle('on', sin);
      G.forEach(function (o, gi) {
        o.g.style.opacity = s0 >= (gi ? 2 : 1) ? 1 : 0.07;
        o.bars.forEach(function (b) { var v = D[b.z][o.k], yy = sy(v); b.r.setAttribute('y', yy); b.r.setAttribute('height', y0 - yy); b.t.setAttribute('y', yy - 12); b.t.textContent = f(v * 100, 1) + '\u00a0%'; });
      });
    }
    draw();
    return { step: function (s) { s0 = s; sin = s >= 3; draw(); }, final: function () { s0 = 3; sin = false; draw(); } };
  });
})();
