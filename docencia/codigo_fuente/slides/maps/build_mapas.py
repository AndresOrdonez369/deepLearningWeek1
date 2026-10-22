"""Teacher concept maps: docencia/mapas/index.html (self-contained, interactive, printable on A4).
usage: python build_mapas.py <out_dir> <slides.json>
"""
import base64, json, os, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from maps_data import MAPS  # noqa: E402

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'out')
SLIDES = json.loads(pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else HERE.parent / 'out' / 'slides.json').read_text())
NM = pathlib.Path(os.environ.get('DECK_NODE_MODULES', HERE.parent / 'fonts' / 'node_modules'))
SN = {s['id']: s['n'] for s in SLIDES}
TABS = {'semana': 'La semana', 'b01': 'IA, ML y DL', 'b02': 'La neurona', 'b03': 'Cómo aprende', 'b04': 'Error y mejora', 'b05': 'Una red',
        'b06': 'Retropropagación', 'b07': 'Entrenar bien', 'b08': 'Keras', 'b09': '¿Es bueno?'}
for m in MAPS:
    m['tab'] = TABS[m['id']]

for m in MAPS:
    ids = {n['id'] for n in m['nodes']}
    for a, b, _ in m['edges']:
        assert a in ids and b in ids, (m['id'], a, b)
    for n in m['nodes']:
        assert not n['slide'] or n['slide'] in SN, (m['id'], n['id'], n['slide'])


def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()


fs = NM / '@fontsource-variable'
FONTS = '\n'.join(f'@font-face{{font-family:"{n}";src:url(data:font/woff2;base64,{b64(p)}) format("woff2");font-weight:{w};font-display:swap}}' for n, p, w in [
    ('Unbounded', fs / 'unbounded/files/unbounded-latin-wght-normal.woff2', '200 900'),
    ('Lexend', fs / 'lexend/files/lexend-latin-wght-normal.woff2', '100 900'),
    ('JetBrains Mono', fs / 'jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2', '100 800')])

CSS = r"""
:root{--night:oklch(0.17 0.03 258);--night-2:oklch(0.215 0.035 258);--night-3:oklch(0.26 0.038 258);--line:oklch(0.34 0.035 258);--grid:oklch(0.235 0.03 258);
--ink:oklch(0.97 0.008 250);--ink-2:oklch(0.82 0.03 250);--ink-3:oklch(0.68 0.035 252);--amber:oklch(0.83 0.155 72);--azure:oklch(0.75 0.13 235);--mint:oklch(0.85 0.14 165);
--coral:oklch(0.72 0.17 28);--lilac:oklch(0.78 0.11 300);--ease:cubic-bezier(0.16,1,0.3,1);--sans:"Lexend",system-ui,sans-serif;--display:"Unbounded","Lexend",sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace;color-scheme:dark}
*{box-sizing:border-box}html,body{margin:0;background:var(--night);color:var(--ink);font-family:var(--sans)}
a{color:var(--amber)}
.app{display:grid;grid-template-columns:minmax(0,1fr) 22rem;grid-template-rows:auto auto 1fr;min-height:100vh}
header{grid-column:1/-1;display:flex;align-items:center;gap:1rem;padding:1rem 1.4rem;border-bottom:1px solid var(--line);flex-wrap:wrap}
header h1{font:700 1.35rem/1.1 var(--display);margin:0;letter-spacing:-.01em}
header .sp{flex:1}
.btn{display:inline-flex;align-items:center;gap:.4rem;font:600 .95rem/1 var(--sans);padding:.6rem 1rem;border-radius:999px;border:2px solid var(--line);background:var(--night-2);color:var(--ink);cursor:pointer;text-decoration:none}
.btn:hover{border-color:var(--ink-3)}.btn:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.btn.primary{background:var(--amber);border-color:var(--amber);color:var(--night)}
nav.maps{grid-column:1/-1;padding:.5rem .9rem;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:.15rem}
nav.maps button{display:inline-flex;align-items:center;gap:.45rem;white-space:nowrap;background:none;border:0;border-radius:999px;padding:.5rem .62rem;color:var(--ink-2);font:500 .92rem/1.1 var(--sans);cursor:pointer}
nav.maps button b{font:700 .8rem/1 var(--mono);color:var(--ink-3)}
nav.maps button:hover{background:var(--night-2);color:var(--ink)}
nav.maps button[aria-current=true]{background:var(--night-3);color:var(--ink)}
nav.maps button[aria-current=true] b{color:var(--amber)}
nav.maps button:focus-visible{outline:3px solid var(--amber);outline-offset:-3px}
main{padding:1.2rem 1.4rem;display:flex;flex-direction:column;gap:.8rem;min-width:0}
main h2{font:600 1.6rem/1.15 var(--sans);margin:0;letter-spacing:-.01em}
main .sub{color:var(--ink-2);margin:0;font-size:1.05rem}
.plate{background:var(--night-2);border:1px solid oklch(0.3 0.035 258);border-radius:1rem;position:relative;overflow:hidden}
.plate::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.6;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:44px 44px}
#map{display:block;width:100%;height:auto;position:relative}
.tour{display:flex;align-items:center;gap:.7rem;flex-wrap:wrap}
.tour .pos{font:600 .95rem/1 var(--mono);color:var(--ink-2)}
.legend{display:flex;gap:1.1rem;flex-wrap:wrap;color:var(--ink-3);font-size:.88rem}
.legend span{display:inline-flex;align-items:center;gap:.45rem}
.legend i{display:inline-block;width:1.6rem;height:.9rem;border-radius:999px;border:2px solid var(--ink-3)}
aside.det{border-left:1px solid var(--line);padding:1.2rem 1.3rem;display:flex;flex-direction:column;gap:1rem;overflow:auto}
.det h3{font:600 1.45rem/1.2 var(--sans);margin:0}
.det .empty{color:var(--ink-3);line-height:1.5}
.det dl{margin:0;display:grid;gap:.9rem}
.det dt{font:600 .78rem/1 var(--sans);letter-spacing:.04em;color:var(--ink-3);margin-bottom:.35rem}
.det dd{margin:0;font-size:1.05rem;line-height:1.48;color:var(--ink)}
.det dd.q{color:var(--mint)}
.det dd.t{color:var(--coral)}
.det .meta{display:flex;gap:.5rem;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:.35rem;font:600 .8rem/1 var(--sans);padding:.45rem .75rem;border-radius:999px;background:var(--night-3);color:var(--ink-2);text-decoration:none}
.chip.key{background:var(--amber);color:var(--night)}.chip.trend{background:var(--lilac);color:var(--night)}
a.chip:hover{color:var(--ink)}
/* svg */
.edge{fill:none;stroke:var(--ink-3);stroke-width:3;opacity:.65;transition:opacity .3s,stroke .3s}
.edge.on{stroke:var(--amber);opacity:1;stroke-width:4}
.elab{font:500 20px var(--sans);fill:var(--ink-2);transition:opacity .3s}
.elab-bg{fill:var(--night-2)}
.node{cursor:pointer;transition:opacity .3s}
.node rect{fill:var(--night);stroke:var(--ink-3);stroke-width:3;transition:stroke .2s,fill .2s}
.node text{font:600 26px var(--sans);fill:var(--ink);text-anchor:middle;pointer-events:none}
.node.key rect{stroke:var(--amber);stroke-width:4}
.node.ex rect{stroke-dasharray:8 7;stroke:var(--ink-2)}
.node.tool text{font-family:var(--mono);font-weight:600;font-size:23px}
.node.tool rect{fill:var(--night-3)}
.node.trend rect{stroke:var(--lilac)}
.node.trap rect{stroke:var(--coral)}
.node .badge{fill:var(--amber)}.node .badgen{font:700 19px var(--mono);fill:var(--night)}
.node:hover rect,.node:focus-visible rect{fill:var(--night-3)}
.node:focus{outline:none}.node:focus-visible rect{stroke:var(--ink);stroke-width:5}
.node.sel rect{fill:oklch(0.83 0.155 72 / .14);stroke:var(--amber);stroke-width:5}
svg.dim .node:not(.sel):not(.nb){opacity:.38}
svg.dim .edge:not(.on),svg.dim .elab:not(.on){opacity:.25}
.halo{fill:url(#halo);opacity:0;transition:opacity .4s}
.node.sel .halo{opacity:1}
#print{display:none}
.mlist{display:none;list-style:none;margin:0;padding:0;flex-direction:column;gap:.5rem}
.mlist button{width:100%;display:flex;flex-direction:column;align-items:flex-start;gap:.3rem;text-align:left;background:var(--night-2);color:var(--ink);border:2px solid var(--ink-3);border-radius:.9rem;padding:.8rem 1rem;font:600 1.05rem/1.3 var(--sans);cursor:pointer}
.mlist button small{font:400 .88rem/1.35 var(--sans);color:var(--ink-2)}
.mlist .key button{border-color:var(--amber)}.mlist .ex button{border-style:dashed}.mlist .tool button{background:var(--night-3);font-family:var(--mono)}
.mlist .trend button{border-color:var(--lilac)}.mlist .trap button{border-color:var(--coral)}
.mlist button.sel{background:oklch(0.83 0.155 72 / .14);border-color:var(--amber)}
.mlist .kb{font:700 .78rem/1 var(--mono);background:var(--amber);color:var(--night);border-radius:999px;padding:.2rem .45rem;margin-right:.4rem}
@media (max-width:1000px){.app{grid-template-columns:1fr}aside.det{border-left:0;border-top:1px solid var(--line)}}
@media (max-width:700px){.plate,.legend{display:none}.mlist{display:flex}header{padding:.8rem 1rem}header .btn{font-size:.85rem;padding:.5rem .8rem}main{padding:1rem}nav.maps{padding:.5rem .8rem;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
/* print: one A4 landscape page per map, light ink on paper */
@page{size:A4 landscape;margin:10mm}
@media print{
  :root{--night:#fff;--night-2:#fff;--night-3:#f1f4f8;--line:#c9d1dc;--grid:#eef1f5;--ink:#121b28;--ink-2:#2b3646;--ink-3:#5a6677;--amber:#a45e00;--lilac:#6f4fa1;--coral:#ba362e;--mint:#007653;color-scheme:light}
  html,body{background:#fff}
  .app{display:none}
  #print{display:block}
  .pmap{page-break-after:always;break-after:page;display:flex;flex-direction:column;gap:3mm}
  .pmap h2{font:600 16pt/1.1 var(--sans);margin:0}.pmap .sub{font-size:9.5pt;color:var(--ink-3);margin:0}
  .pmap svg{display:block;width:100%;height:84mm;flex:none}
  .pmap .tbl{columns:4;column-gap:5mm;font-size:7.3pt;line-height:1.3}
  .pmap .it{break-inside:avoid;margin:0 0 2.4mm}
  .pmap .it b{font-size:8pt}
  .pmap .it span{display:block;color:var(--ink-2)}
  .pmap .it .q{color:#007653}
  .node.sel rect{fill:#fff}
  .elab-bg{fill:#fff}
}
"""

JS = r"""
(function(){
var MAPS = __MAPS__, SN = __SN__, SLIDES = '../slides/index.html#';
var NS = 'http://www.w3.org/2000/svg';
function S(t, a, p){ var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
function esc(s){ return String(s).replace(/\|/g, ' ').replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
function wrap(label){
  var lines = [];
  label.split('|').forEach(function(part){
    var cur = '';
    part.split(' ').forEach(function(w){ if ((cur + ' ' + w).trim().length > 16 && cur) { lines.push(cur); cur = w; } else cur = (cur + ' ' + w).trim(); });
    if (cur) lines.push(cur);
  });
  return lines;
}
function draw(svg, m, opts){
  svg.innerHTML = '';
  var defs = S('defs', {}, svg);
  var g = S('radialGradient', {id: 'halo'}, defs);
  S('stop', {offset: '0%', 'stop-color': 'oklch(0.83 0.155 72)', 'stop-opacity': .18}, g); S('stop', {offset: '100%', 'stop-color': 'oklch(0.83 0.155 72)', 'stop-opacity': 0}, g);
  var mk = S('marker', {id: 'arr' + (opts.p || ''), viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse'}, defs);
  S('path', {d: 'M0 0 L10 5 L0 10 z', fill: 'var(--ink-3)'}, mk);
  var gE = S('g', {}, svg), gL = S('g', {}, svg), gN = S('g', {}, svg), box = {};
  m.nodes.forEach(function(n){
    var lines = wrap(n.label), w = Math.min(310, Math.max(160, Math.max.apply(null, lines.map(function(l){ return l.length; })) * (n.kind === 'tool' ? 14.4 : 14.6) + 56)), h = 34 * lines.length + 32;
    box[n.id] = {x: n.x, y: n.y, w: w, h: h};
    var el = S('g', {class: 'node ' + n.kind, tabindex: opts.print ? -1 : 0, role: 'button', 'aria-label': n.label.replace(/\|/g, ' '), 'data-id': n.id, transform: 'translate(' + n.x + ' ' + n.y + ')'}, gN);
    S('circle', {class: 'halo', r: w * 0.62}, el);
    S('rect', {x: -w / 2, y: -h / 2, width: w, height: h, rx: Math.min(h / 2, 30)}, el);
    lines.forEach(function(l, i){ var t = S('text', {y: (i - (lines.length - 1) / 2) * 34 + 9}, el); t.textContent = l; });
    if (n.key) { S('circle', {class: 'badge', cx: -w / 2 + 6, cy: -h / 2 + 4, r: 19}, el); var b = S('text', {class: 'badgen', x: -w / 2 + 6, y: -h / 2 + 11}, el); b.textContent = n.key; }
  });
  function clip(a, b){
    var dx = b.x - a.x, dy = b.y - a.y, tx = Math.abs(dx) > 1e-6 ? (a.w / 2 + 8) / Math.abs(dx) : 1e9, ty = Math.abs(dy) > 1e-6 ? (a.h / 2 + 8) / Math.abs(dy) : 1e9, t = Math.min(tx, ty);
    return {x: a.x + dx * t, y: a.y + dy * t};
  }
  m.edges.forEach(function(e, i){
    var a = box[e[0]], b = box[e[1]], p = clip(a, b), q = clip(b, a);
    var path = S('path', {class: 'edge', d: 'M' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + 'L' + q.x.toFixed(1) + ' ' + q.y.toFixed(1), 'marker-end': 'url(#arr' + (opts.p || '') + ')', 'data-a': e[0], 'data-b': e[1]}, gE);
    if (e[2]) {
      var mx = (p.x + q.x) / 2, my = (p.y + q.y) / 2, hz = Math.abs(q.y - p.y) < 30, vt = Math.abs(q.x - p.x) < 30, tg = S('g', {class: 'elab', 'data-a': e[0], 'data-b': e[1]}, gL);
      var len = e[2].length * 10.6 + 22, cand = vt ? [[mx + 14, my - 17], [mx - 14 - len, my - 17]] : hz ? [[mx - len / 2, my - 44], [mx - len / 2, my + 10]] : [[mx - len / 2, my - 17], [mx - len / 2, my - 52], [mx - len / 2, my + 18]];
      function hits(c){ if (c[0] < 4 || c[0] + len > 1396) return true; return Object.keys(box).some(function(k){ var r = box[k]; return c[0] < r.x + r.w / 2 + 6 && c[0] + len > r.x - r.w / 2 - 6 && c[1] < r.y + r.h / 2 + 4 && c[1] + 34 > r.y - r.h / 2 - 4; }); }
      var pick = cand.filter(function(c){ return !hits(c); })[0] || cand[0], lx = pick[0], ly = pick[1];
      S('rect', {class: 'elab-bg', x: lx, y: ly, width: len, height: 34, rx: 17}, tg);
      var t = S('text', {x: lx + len / 2, y: ly + 24, 'text-anchor': 'middle'}, tg); t.textContent = e[2];
    }
  });
  return svg;
}
var cur = 0, sel = null, svg = document.getElementById('map'), det = document.getElementById('det');
function select(id){
  var m = MAPS[cur]; sel = id;
  svg.classList.toggle('dim', !!id);
  [].forEach.call(svg.querySelectorAll('.node'), function(n){ n.classList.toggle('sel', n.dataset.id === id); n.classList.remove('nb'); });
  [].forEach.call(document.querySelectorAll('#mlist button'), function(b){ b.classList.toggle('sel', b.dataset.id === id); });
  [].forEach.call(svg.querySelectorAll('.edge,.elab'), function(e){
    var on = id && (e.dataset.a === id || e.dataset.b === id); e.classList.toggle('on', !!on);
    if (on) { var o = e.dataset.a === id ? e.dataset.b : e.dataset.a; var nd = svg.querySelector('.node[data-id="' + o + '"]'); if (nd) nd.classList.add('nb'); }
  });
  var i = m.nodes.findIndex(function(n){ return n.id === id; });
  document.getElementById('pos').textContent = (i >= 0 ? i + 1 : 0) + ' de ' + m.nodes.length;
  if (!id) { det.innerHTML = '<p class="empty">Haz clic en un concepto (o usa <b>Recorrido</b>) para ver qué decir, un ejemplo, una pregunta para la clase y el error más frecuente.</p>'; return; }
  var n = m.nodes[i], chips = '';
  if (n.key) chips += '<span class="chip key">Idea clave ' + n.key + '</span>';
  if (n.kind === 'trend') chips += '<span class="chip trend">Lectura de tendencia</span>';
  if (n.slide) chips += '<a class="chip" href="' + SLIDES + n.slide + '" target="_blank" rel="noopener">Lámina ' + SN[n.slide] + ' ↗</a>';
  if (n.nb && n.nb !== '—') chips += '<span class="chip">' + esc(n.nb) + '</span>';
  var rows = [['Qué decir', n.say, ''], ['Ejemplo para usar', n.ex, ''], ['Pregunta para la clase', n.ask, 'q'], ['Error frecuente', n.trap, 't']]
    .filter(function(r){ return r[1] && r[1] !== '—'; }).map(function(r){ return '<div><dt>' + r[0] + '</dt><dd class="' + r[2] + '">' + esc(r[1]) + '</dd></div>'; }).join('');
  det.innerHTML = '<h3>' + esc(n.label) + '</h3><div class="meta">' + chips + '</div><dl>' + rows + '</dl>';
  try { history.replaceState(null, '', '#' + m.id + '/' + id); } catch (e) {}
}
function show(i, nodeId){
  cur = i; var m = MAPS[i];
  document.getElementById('mt').textContent = m.title; document.getElementById('ms').textContent = m.sub;
  [].forEach.call(document.querySelectorAll('nav.maps button'), function(b, k){ b.setAttribute('aria-current', k === i ? 'true' : 'false'); });
  draw(svg, m, {});
  var byId = {}; m.nodes.forEach(function(n){ byId[n.id] = n; });
  document.getElementById('mlist').innerHTML = m.nodes.map(function(n){
    var out = m.edges.filter(function(e){ return e[0] === n.id; }).map(function(e){ return (e[2] ? esc(e[2]) + ' → ' : '→ ') + esc(byId[e[1]].label); }).join(' · ');
    return '<li class="' + n.kind + '"><button type="button" data-id="' + n.id + '">' + '<span>' + (n.key ? '<span class="kb">' + n.key + '</span>' : '') + esc(n.label) + '</span>' + (out ? '<small>' + out + '</small>' : '') + '</button></li>';
  }).join('');
  [].forEach.call(document.querySelectorAll('#mlist button'), function(b){ b.addEventListener('click', function(){ select(b.dataset.id); var d = document.getElementById('det'); if (d.scrollIntoView) d.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'}); }); });
  svg.querySelectorAll('.node').forEach(function(n){
    n.addEventListener('click', function(){ select(n.dataset.id === sel ? null : n.dataset.id); });
    n.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(n.dataset.id); } });
  });
  select(nodeId || null);
  try { if (!nodeId) history.replaceState(null, '', '#' + m.id); } catch (e) {}
}
var nav = document.querySelector('nav.maps');
MAPS.forEach(function(m, i){ var b = document.createElement('button'); b.type = 'button'; b.innerHTML = '<b>' + (m.short === 'Semana' ? '★' : m.short) + '</b><span>' + esc(m.tab || m.title) + '</span>'; b.title = m.title; b.onclick = function(){ show(i); }; nav.appendChild(b); });
function step(d){ var m = MAPS[cur], i = m.nodes.findIndex(function(n){ return n.id === sel; }); i = i < 0 ? (d > 0 ? 0 : m.nodes.length - 1) : Math.max(0, Math.min(m.nodes.length - 1, i + d)); select(m.nodes[i].id); }
document.getElementById('prev').onclick = function(){ step(-1); };
document.getElementById('next').onclick = function(){ step(1); };
document.getElementById('printb').onclick = function(){ window.print(); };
document.addEventListener('keydown', function(e){ if (e.target.closest && e.target.closest('input,textarea')) return; if (e.key === 'ArrowRight') step(1); else if (e.key === 'ArrowLeft') step(-1); else if (e.key === 'Escape') select(null); });
var h = decodeURIComponent(location.hash.slice(1)).split('/'), mi = MAPS.findIndex(function(m){ return m.id === h[0]; });
show(mi < 0 ? 0 : mi, h[1]);
window.addEventListener('hashchange', function(){ var h = decodeURIComponent(location.hash.slice(1)).split('/'), mi = MAPS.findIndex(function(m){ return m.id === h[0]; }); if (mi >= 0 && (mi !== cur || (h[1] || null) !== sel)) show(mi, h[1]); });
/* printable version: every map plus its teaching notes */
var pr = document.getElementById('print');
MAPS.forEach(function(m, i){
  var sec = document.createElement('section'); sec.className = 'pmap';
  sec.innerHTML = '<div><h2>' + esc(m.title) + '</h2><p class="sub">' + esc(m.sub) + ' · Semana 1 · Neural Networks: Deep Learning · UIDE</p></div>';
  var s = S('svg', {viewBox: '0 0 1400 800'}); sec.appendChild(s); draw(s, m, {print: true, p: 'p' + i});
  var t = document.createElement('div'); t.className = 'tbl';
  t.innerHTML = m.nodes.map(function(n){ return '<p class="it"><b>' + esc(n.label) + (n.key ? ' · idea clave ' + n.key : '') + (n.slide ? ' · lámina ' + SN[n.slide] : '') + '</b><span>' + esc(n.say) + '</span>' + (n.ex && n.ex !== '—' ? '<span>Ej.: ' + esc(n.ex) + '</span>' : '') + (n.ask && n.ask !== '—' ? '<span class="q">? ' + esc(n.ask) + '</span>' : '') + '</p>'; }).join('');
  sec.appendChild(t); pr.appendChild(sec);
});
})();
"""

HTML = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mapas conceptuales · Semana 1</title>
<meta name="description" content="Mapas conceptuales para enseñar la semana 1 de Neural Networks: Deep Learning (UIDE): qué decir, ejemplos, preguntas y errores frecuentes por concepto.">
<meta name="robots" content="noindex">
<style>{FONTS}</style>
<style>{CSS}</style>
</head>
<body>
<div class="app">
  <header><h1>Mapas conceptuales · Semana 1</h1><span class="sp"></span>
    <a class="btn" href="../slides/index.html" target="_blank" rel="noopener">Abrir las slides ↗</a>
    <a class="btn" href="../index.html">Panel del profesor</a>
    <button class="btn primary" id="printb" type="button">Imprimir en A4</button></header>
  <nav class="maps" aria-label="Mapas"></nav>
  <main>
    <h2 id="mt"></h2><p class="sub" id="ms"></p>
    <div class="plate"><svg id="map" viewBox="0 0 1400 800" role="img" aria-label="Mapa conceptual"></svg></div>
    <ol class="mlist" id="mlist" aria-label="Conceptos del mapa, en orden"></ol>
    <div class="tour"><button class="btn" id="prev" type="button">← Anterior</button><span class="pos" id="pos"></span><button class="btn" id="next" type="button">Siguiente →</button>
      <span class="legend"><span><i style="border-color:var(--amber)"></i>idea clave del quiz</span><span><i style="border-style:dashed"></i>ejemplo o analogía</span><span><i style="background:var(--night-3)"></i>código</span><span><i style="border-color:var(--lilac)"></i>lectura de tendencia</span><span><i style="border-color:var(--coral)"></i>trampa típica</span></span></div>
  </main>
  <aside class="det" id="det" aria-live="polite"></aside>
</div>
<div id="print"></div>
<script>{JS.replace('__MAPS__', json.dumps(MAPS, ensure_ascii=False)).replace('__SN__', json.dumps(SN))}</script>
</body>
</html>
"""
assert '</script' not in JS
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(HTML)
print(f'{len(MAPS)} maps · {len(HTML) / 1e3:.0f} KB → {OUT / "index.html"}')
