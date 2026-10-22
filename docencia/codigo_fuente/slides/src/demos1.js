/* Demo helpers + generic demos (count, codehl, draw, net, cycle) */
var demo = window.DeckDemo, C = window.DeckColors, RM = window.DeckRM;
var NS = 'http://www.w3.org/2000/svg';
function S(tag, attrs, parent) {
  var e = document.createElementNS(NS, tag);
  if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function H(tag, cls, parent, html) {
  var e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  if (parent) parent.appendChild(e);
  return e;
}
function lin(d0, d1, r0, r1) { return function (v) { return r0 + (v - d0) * (r1 - r0) / (d1 - d0); }; }
function sig(z) { return 1 / (1 + Math.exp(-z)); }
function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
function f(x, d) { d = d == null ? 2 : d; var s = Math.abs(x).toFixed(d); return (x < 0 && +s !== 0 ? '−' : '') + s; }
function fs(x, d) { return (x > 0 ? '+' : '') + f(x, d); }
function easeOut(t) { return 1 - Math.pow(1 - t, 4); }
function range(n) { var a = []; for (var i = 0; i < n; i++) a.push(i); return a; }
function seeded(s) { return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }
function gauss(r) { var u = 1 - r(), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
function tween(dur, fn, done) {
  if (RM || dur <= 0) { fn(1); if (done) done(); return { stop: function () {} }; }
  var t0 = performance.now(), id = 0, alive = true;
  function tick(t) { if (!alive) return; var k = Math.max(0, Math.min(1, (t - t0) / dur)); fn(easeOut(k)); if (k < 1) id = requestAnimationFrame(tick); else if (done) done(); }
  id = requestAnimationFrame(tick);
  return { stop: function () { alive = false; cancelAnimationFrame(id); } };
}
function svgIn(el, w, h, label) {
  var s = S('svg', { viewBox: '0 0 ' + w + ' ' + h, role: 'img', 'aria-label': label || el.dataset.alt || '' }, el);
  s.style.overflow = 'visible';
  return s;
}
function pt(svg, e) {
  var p = svg.createSVGPoint(), t = e.touches ? e.touches[0] : e;
  p.x = t.clientX; p.y = t.clientY;
  return p.matrixTransform(svg.getScreenCTM().inverse());
}
function drag(svg, handle, onMove) {
  function move(e) { e.preventDefault(); onMove(pt(svg, e)); }
  function up() { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); }
  handle.addEventListener('pointerdown', function (e) { e.preventDefault(); e.stopPropagation(); window.addEventListener('pointermove', move); window.addEventListener('pointerup', up); });
  handle.style.cursor = 'grab';
  handle.setAttribute('data-drag', '1');
}
function txt(parent, x, y, s, a) {
  a = a || {};
  var t = S('text', Object.assign({ x: x, y: y, fill: C.ink2, 'font-size': 22, 'font-family': 'Lexend, system-ui, sans-serif' }, a), parent);
  t.textContent = s;
  return t;
}
function grid(g, x0, y0, x1, y1, step) {
  for (var x = x0; x <= x1 + 0.1; x += step) S('line', { x1: x, y1: y0, x2: x, y2: y1, stroke: C.grid, 'stroke-width': 2 }, g);
  for (var y = y0; y <= y1 + 0.1; y += step) S('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: C.grid, 'stroke-width': 2 }, g);
}
function axes(g, x0, y0, x1, y1) {
  S('line', { x1: x0, y1: y1, x2: x1, y2: y1, stroke: C.line, 'stroke-width': 3 }, g);
  S('line', { x1: x0, y1: y0, x2: x0, y2: y1, stroke: C.line, 'stroke-width': 3 }, g);
}
function pathOf(fn, a, b, sx, sy, n) {
  n = n || 160; var d = '';
  for (var i = 0; i <= n; i++) { var v = a + (b - a) * i / n; d += (i ? 'L' : 'M') + sx(v).toFixed(1) + ' ' + sy(fn(v)).toFixed(1); }
  return d;
}
/* clip a rectangle with the half-plane a*x + b*y + c >= 0 (Sutherland-Hodgman) */
function halfPlane(rect, a, b, c) {
  var out = [], P = rect;
  for (var i = 0; i < P.length; i++) {
    var p = P[i], q = P[(i + 1) % P.length], fp = a * p[0] + b * p[1] + c, fq = a * q[0] + b * q[1] + c;
    if (fp >= 0) out.push(p);
    if ((fp >= 0) !== (fq >= 0)) { var t = fp / (fp - fq); out.push([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]); }
  }
  return out;
}
function poly(pts) { return pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' '); }
/* segment of the line a*x + b*y + c = 0 inside a rect [x0,y0,x1,y1] */
function lineInRect(a, b, c, x0, y0, x1, y1) {
  var pts = [];
  if (Math.abs(b) > 1e-9) { [x0, x1].forEach(function (x) { var y = -(a * x + c) / b; if (y >= y0 - 1e-6 && y <= y1 + 1e-6) pts.push([x, y]); }); }
  if (Math.abs(a) > 1e-9) { [y0, y1].forEach(function (y) { var x = -(b * y + c) / a; if (x >= x0 - 1e-6 && x <= x1 + 1e-6) pts.push([x, y]); }); }
  if (pts.length < 2) return null;
  var best = [pts[0], pts[1]], dm = 0;
  for (var i = 0; i < pts.length; i++) for (var j = i + 1; j < pts.length; j++) { var d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]); if (d > dm) { dm = d; best = [pts[i], pts[j]]; } }
  return best;
}
var _gid = 0;
/* radial light for things that are active (DESIGN.md · The Activation Rule) */
function glow(svg, color) {
  var defs = svg.querySelector('defs');
  if (!defs) { defs = S('defs', {}); svg.insertBefore(defs, svg.firstChild); }
  var id = 'gl' + (++_gid) + Math.floor(Math.random() * 1e6), g = S('radialGradient', { id: id }, defs);
  S('stop', { offset: '0%', 'stop-color': color, 'stop-opacity': 0.6 }, g);
  S('stop', { offset: '50%', 'stop-color': color, 'stop-opacity': 0.2 }, g);
  S('stop', { offset: '100%', 'stop-color': color, 'stop-opacity': 0 }, g);
  return 'url(#' + id + ')';
}

/* ---------------- count: animated number when the slide reaches a step ---------------- */
demo('count', function (el, api) {
  var to = +el.dataset.to, from = +(el.dataset.from || 0), dec = +(el.dataset.dec || 0), at = +(el.dataset.at || 0), unit = el.dataset.unit || '';
  var sign = el.dataset.sign === '1', shown = null, tw = null;
  function fmt(v) {
    var s = dec ? f(v, dec) : Math.round(v).toLocaleString('es-EC');
    if (sign && v > 0) s = '+' + s;
    return s + unit;
  }
  function set(v) { el.textContent = fmt(v); }
  set(at ? from : to);
  return {
    step: function (s) {
      var on = s >= at;
      if (on === shown) return; shown = on;
      if (tw) tw.stop();
      if (!on) { set(from); return; }
      tw = tween(+(el.dataset.ms || 1100), function (k) { set(from + (to - from) * k); });
    },
    final: function () { set(to); }
  };
});

/* ---------------- codehl: highlight code lines by step  data-hl="1:1-3;2:5-6" ---------------- */
demo('codehl', function (el) {
  var lines = el.querySelectorAll('.ln'), map = {};
  (el.dataset.hl || '').split(';').forEach(function (p) {
    if (!p) return; var kv = p.split(':'), r = kv[1].split('-');
    map[+kv[0]] = [+r[0], +(r[1] || r[0])];
  });
  return {
    step: function (s) {
      var r = map[s];
      [].forEach.call(lines, function (l, i) { l.classList.toggle('hl', !!r && i + 1 >= r[0] && i + 1 <= r[1]); });
    }
  };
});

/* ---------------- draw: stroke-draw every [data-draw] path when the slide opens ---------------- */
demo('draw', function (el) {
  var ps = [].slice.call(el.querySelectorAll('[data-draw]'));
  ps.forEach(function (p) { var L = p.getTotalLength ? p.getTotalLength() : 1000; p.style.strokeDasharray = L; p.style.strokeDashoffset = L; p._L = L; });
  var tws = [];
  function run(full) {
    tws.forEach(function (t) { t.stop(); }); tws = [];
    ps.forEach(function (p, i) {
      if (full || RM) { p.style.strokeDashoffset = 0; return; }
      p.style.strokeDashoffset = p._L;
      setTimeout(function () { tws.push(tween(700, function (k) { p.style.strokeDashoffset = p._L * (1 - k); })); }, 90 * (+p.dataset.draw || i));
    });
  }
  return { enter: function () { run(false); }, final: function () { run(true); } };
});

/* ---------------- net: a network whose signals travel and light the neurons ---------------- */
demo('net', function (el, api) {
  var layers = (el.dataset.layers || '3,4,4,1').split(',').map(Number);
  var W = +(el.dataset.w || 900), Hh = +(el.dataset.h || 700), R = +(el.dataset.r || 24);
  var names = el.dataset.names ? el.dataset.names.split('|') : null;
  var hl = el.dataset.hl ? el.dataset.hl.split('|').map(function (s) { return s.split(',').map(Number); }) : null;
  var quiet = el.dataset.quiet === '1';
  var svg = svgIn(el, W, Hh);
  var padX = +(el.dataset.padx || 90), padY = names ? 70 : 40;
  var maxN = Math.max.apply(null, layers);
  var gapY = Math.min(+(el.dataset.gap || 120), (Hh - 2 * padY - (names ? 40 : 0)) / Math.max(1, maxN - 1));
  var cy = (Hh - (names ? 50 : 0)) / 2;
  var rnd = seeded(+(el.dataset.seed || 11));
  var nodes = layers.map(function (n, i) {
    var x = layers.length === 1 ? W / 2 : padX + i * (W - 2 * padX) / (layers.length - 1);
    return range(n).map(function (j) { return { x: x, y: cy + (j - (n - 1) / 2) * gapY, a: 0, l: i, out: [] }; });
  });
  var gE = S('g', {}, svg), gP = S('g', {}, svg), gN = S('g', {}, svg), gL = S('g', {}, svg), GL = glow(svg, C.amber);
  var edges = [];
  for (var l = 0; l < layers.length - 1; l++) nodes[l].forEach(function (a) {
    nodes[l + 1].forEach(function (b) {
      var w = rnd() * 2 - 1;
      var e = { a: a, b: b, w: w, el: S('line', { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: w > 0 ? C.amber : C.azure, 'stroke-opacity': (0.22 + 0.4 * Math.abs(w)).toFixed(2), 'stroke-width': (2.5 + 5 * Math.abs(w)).toFixed(1), 'stroke-linecap': 'round' }, gE) };
      a.out.push(e); edges.push(e);
    });
  });
  nodes.forEach(function (col) {
    col.forEach(function (n) {
      n.halo = S('circle', { cx: n.x, cy: n.y, r: R * 2.6, fill: GL, opacity: 0 }, gN);
      n.body = S('circle', { cx: n.x, cy: n.y, r: R, fill: C.night2, stroke: C.ink3, 'stroke-width': 4 }, gN);
      n.core = S('circle', { cx: n.x, cy: n.y, r: R - 6, fill: C.amber, opacity: 0 }, gN);
    });
  });
  var labels = [];
  if (names) names.forEach(function (s, i) {
    var col = nodes[Math.min(i, nodes.length - 1)];
    labels.push(txt(gL, col[0].x, Hh - 14, s, { 'text-anchor': 'middle', 'font-size': 26, 'font-weight': 600, fill: C.ink2 }));
  });
  var pool = [], pulses = [];
  function pulse(e) {
    var c = pool.pop() || S('circle', { r: 8, fill: C.amber }, gP);
    c.style.display = '';
    pulses.push({ e: e, t: 0, c: c });
  }
  function fire(n, k) { n.a = Math.min(1, n.a + k); n.out.forEach(function (e) { if (Math.random() < 0.55 + 0.4 * n.a) pulse(e); }); }
  function inputs() { nodes[0].forEach(function (n) { if (Math.random() < 0.8) fire(n, 0.9); }); }
  var acc = 0, loop = api.raf(function (t, dt) {
    acc += dt;
    if (acc > 1900) { acc = 0; inputs(); }
    for (var i = pulses.length - 1; i >= 0; i--) {
      var p = pulses[i]; p.t += dt / 650;
      if (p.t >= 1) { p.c.style.display = 'none'; pool.push(p.c); pulses.splice(i, 1); var b = p.e.b; var g = 0.35 * Math.abs(p.e.w); b.a = Math.min(1, b.a + g); if (b.a > 0.4 && b.out.length && !b._f) { b._f = 1; setTimeout(function (bb) { return function () { bb._f = 0; fire(bb, 0); }; }(b), 60); } continue; }
      var x = p.e.a.x + (p.e.b.x - p.e.a.x) * p.t, y = p.e.a.y + (p.e.b.y - p.e.a.y) * p.t;
      p.c.setAttribute('cx', x.toFixed(1)); p.c.setAttribute('cy', y.toFixed(1));
    }
    nodes.forEach(function (col) { col.forEach(function (n) { n.a *= 0.965; n.core.setAttribute('opacity', (n.a * 0.95).toFixed(3)); n.halo.setAttribute('opacity', (n.a * 0.9).toFixed(3)); }); });
  });
  function still() { nodes.forEach(function (col, i) { col.forEach(function (n, j) { var a = (i + j) % 3 === 0 ? 0.8 : (i + j) % 3 === 1 ? 0.35 : 0; n.core.setAttribute('opacity', a); n.halo.setAttribute('opacity', a * 0.8); }); }); }
  function highlight(s) {
    if (!hl) return;
    var on = s > 0 && hl[s - 1] ? hl[s - 1] : null;
    nodes.forEach(function (col, i) {
      var lit = !on || on.indexOf(i) >= 0;
      col.forEach(function (n) { n.body.setAttribute('stroke', on && lit ? C.ink : C.ink3); n.body.style.opacity = lit ? 1 : 0.35; });
    });
    edges.forEach(function (e) { e.el.style.opacity = !on || on.indexOf(e.a.l) >= 0 || on.indexOf(e.b.l) >= 0 ? 1 : 0.25; });
    labels.forEach(function (t, i) { t.setAttribute('fill', on && on.indexOf(i) >= 0 ? C.amber : C.ink2); });
  }
  return {
    enter: function (s) { highlight(s); if (RM || quiet) { still(); return; } acc = 1500; loop.start(); },
    leave: function () { loop.stop(); },
    step: highlight,
    final: still
  };
});

/* ---------------- cycle: predict -> compare -> correct -> repeat, with a signal orbiting ---------------- */
demo('cycle', function (el, api) {
  var W = 900, Hh = 660, cx = 450, cy = 330, R = 215;
  var svg = svgIn(el, W, Hh, 'Ciclo de aprendizaje: predecir, comparar, corregir y repetir');
  var labs = (el.dataset.labels || 'Predice|Compara|Corrige|Repite').split('|');
  var sub = (el.dataset.sub || '').split('|');
  S('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: C.line, 'stroke-width': 4, 'stroke-dasharray': '2 14', 'stroke-linecap': 'round' }, svg);
  var ang = [-90, 0, 90, 180], cols = [C.amber, C.coral, C.mint, C.azure], groups = [], off = [[0, -112, 'middle'], [96, 8, 'start'], [0, 128, 'middle'], [-96, 8, 'end']];
  ang.forEach(function (a, i) {
    var x = cx + R * Math.cos(a * Math.PI / 180), y = cy + R * Math.sin(a * Math.PI / 180);
    var g = S('g', { 'data-step': i + 1 }, svg);
    S('circle', { cx: x, cy: y, r: 76, fill: C.night2, stroke: cols[i], 'stroke-width': 5 }, g);
    txt(g, x, y + 9, labs[i], { 'text-anchor': 'middle', 'font-size': 27, 'font-weight': 600, fill: C.ink });
    if (sub[i]) txt(g, x + off[i][0], y + off[i][1], sub[i], { 'text-anchor': off[i][2], 'font-size': 24, fill: C.ink2 });
    groups.push(g);
  });
  var dot = S('circle', { r: 13, fill: C.amber, opacity: 0 }, svg), th = -Math.PI / 2;
  var loop = api.raf(function (t, dt) { th += dt / 1000 * 1.25; dot.setAttribute('cx', cx + R * Math.cos(th)); dot.setAttribute('cy', cy + R * Math.sin(th)); });
  return {
    enter: function () { if (!RM) { dot.setAttribute('opacity', 1); loop.start(); } },
    leave: function () { loop.stop(); }
  };
});
