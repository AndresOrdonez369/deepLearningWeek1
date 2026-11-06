"""Inline SVG figures for the week-3 study guide. They use the page colors (CSS variables of doc_kit3),
so they work in light and dark mode. Real data comes from the NB05/NB06 runs (deck/src/data/tema1.json, tema2.json)
and the Fashion-MNIST samples of week 2 (fmnist.json)."""
import json, math, pathlib

_HERE = pathlib.Path(__file__).resolve().parent
_DATA = [_HERE / 'data',
         _HERE.parent / 'slides' / 'src' / 'data',                             # repo: semana3/docencia/codigo_fuente/slides/src/data
         pathlib.Path('/home/claude/w3/deck/src/data')]                        # build workspace
_D = next(d for d in _DATA if (d / 'tema1.json').exists())
T1 = json.loads((_D / 'tema1.json').read_text())
T2 = json.loads((_D / 'tema2.json').read_text())
FM = json.loads((_D / 'fmnist.json').read_text())
PX = {s['i']: s['px'] for s in FM['samples']}          # test photos by index (0 botín, 4 camisa, 18 bolso ...)
CLASES = FM['clases']

B, A, T, P, I, M, L = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--purple)', 'var(--ink)', 'var(--muted)', 'var(--line)'
CO = '#E4572E'     # coral: "error / falla" (readable on light and dark paper)


def t(x, y, s, col=I, size=15, anchor='middle', weight=600):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="fill:{col};font:{weight} {size}px \'IBM Plex Sans\',Arial,sans-serif">{s}</text>'


def svg(w, h, label, inner):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">{inner}</svg>'


def num(v, d=1):
    """0.8086 -> '80.9'. Rounds the stored float32 value to 4 decimals first, then half-even:
    the same numbers as DISENO3.md, the slides and the notebooks (0.8415 -> 84.1 (as NB05 prints it), 0.6885 -> 68.8)."""
    from decimal import Decimal, ROUND_HALF_EVEN
    return str((Decimal(str(round(v, 4))) * 100).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_EVEN))


def pct(v, d=1):
    """0.8086 -> '80.9 %' (Spanish style used in the whole course: point as decimal mark, space before %)."""
    return f'{num(v, d)} %'


# ------------------------------------------------------------------ small chart helpers
def axes(x0, y0, x1, y1, yticks, ymap, fmt=lambda v: f'{v:g}'):
    s = f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" style="stroke:{L};stroke-width:1.5"/>'
    for v in yticks:
        y = ymap(v)
        s += f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" style="stroke:{L};stroke-width:1;stroke-dasharray:3 4"/>' + t(x0 - 6, y + 4, fmt(v), M, 12, 'end', 500)
    return s


def poly(pts, col, w=3, dash=''):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polyline points="{d}" fill="none" style="stroke:{col};stroke-width:{w};stroke-linejoin:round{";stroke-dasharray:" + dash if dash else ""}"/>'


def _png(rows):
    """Tiny PNG encoder (RGBA rows of 0..255 tuples) -> data URI. Keeps the 28 x 28 pictures at ~1 KB each."""
    import base64, struct, zlib
    h, w = len(rows), len(rows[0])
    raw = b''.join(b'\x00' + bytes(v for px in r for v in px) for r in rows)
    chunk = lambda tag, data: struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    return 'data:image/png;base64,' + base64.b64encode(png).decode()


def _img(uri, x, y, c, n=28):
    return f'<image href="{uri}" x="{x}" y="{y}" width="{n * c}" height="{n * c}" preserveAspectRatio="none" style="image-rendering:pixelated"/>'


def gray(px, x, y, c, dim=1.0):
    """A 28 x 28 photo (0..255) drawn at c px per cell (an embedded PNG, sharp pixels)."""
    return _img(_png([[(round(v * dim),) * 3 + (255,) for v in r] for r in px]), x, y, c)


HEAT_RGB = {'amber': (245, 158, 11), 'blue': (91, 140, 255), 'coral': (228, 87, 46)}


def heat(m, x, y, c, col='amber', under=None, gamma=1.0):
    """A 28 x 28 map (0..1): colored cells with opacity = value, over a dark tile or over a dimmed photo."""
    mx = max(max(r) for r in m) or 1
    r0, g0, b0 = HEAT_RGB[col]
    base = gray(under, x, y, c, .55) if under else f'<rect x="{x}" y="{y}" width="{28 * c}" height="{28 * c}" fill="#0B1424"/>'
    over = [[(r0, g0, b0, round(255 * min(1, max(0.0, v / mx) ** gamma * .9))) for v in row] for row in m]
    return base + _img(_png(over), x, y, c)


# ------------------------------------------------------------------ Tema 1 · memorizing and brakes
def curvas():
    """Real loss curves of NB05: 1 000 photos without brakes (60 epochs) and with brakes (early stopping at 79)."""
    s = ''
    for k, (key, title) in enumerate([('sobreajuste', 'Sin frenos · 1 000 fotos'), ('regularizada', 'Con frenos · las mismas 1 000 fotos')]):
        d = T1[key]; n = len(d['train_loss']); x0 = 60 + k * 330; W = 260
        X = lambda e: x0 + (e - 1) / 99 * W if key == 'regularizada' else x0 + (e - 1) / 59 * W
        Y = lambda v: 200 - (min(v, 1.0) - 0.1) / 0.9 * 160
        s += axes(x0, 40, x0 + W, 200, [0.2, 0.4, 0.6, 0.8, 1.0], Y, lambda v: f'{v:.1f}')
        s += t(x0 + W / 2, 24, title, I, 15, weight=700)
        be = d['best_epoch']
        s += f'<line x1="{X(be):.1f}" y1="40" x2="{X(be):.1f}" y2="200" style="stroke:{A};stroke-width:2;stroke-dasharray:5 4"/>'
        s += poly([(X(e + 1), Y(v)) for e, v in enumerate(d['train_loss'])], B)
        s += poly([(X(e + 1), Y(v)) for e, v in enumerate(d['val_loss'])], CO)
        s += f'<circle cx="{X(be):.1f}" cy="{Y(d["val_loss"][be - 1]):.1f}" r="5" style="fill:{A}"/>'
        s += t(X(be), 222, f'mejor época: {be}', A, 13)
        last = 60 if key == 'sobreajuste' else 100
        s += t(x0, 240, '1', M, 12, 'middle', 500) + t(x0 + W, 240, f'{last} épocas', M, 12, 'end', 500)
        if key == 'regularizada':
            s += t(X(n) - 4, 56, f'se detiene en la {n}', M, 12, 'end', 500)
            s += f'<line x1="{X(n):.1f}" y1="44" x2="{X(n):.1f}" y2="200" style="stroke:{M};stroke-width:1.5"/>'
    s += t(80, 268, '— entrenamiento', B, 14, 'start') + t(250, 268, '— validación (el simulacro)', CO, 14, 'start') + t(470, 268, 'eje vertical: pérdida', M, 13, 'start', 500)
    return svg(660, 280, 'Curvas reales de pérdida del NB05. Sin frenos, la pérdida de entrenamiento baja hasta el final y la de validación es mínima en la época 33 y después sube. Con frenos, las dos curvas bajan juntas y el entrenamiento se detiene en la época 79', s)


def dropout():
    """Two training steps with different neurons switched off, and prediction with all of them."""
    s = ''
    layers_ = [[50, 90, 130, 170], [40, 75, 110, 145, 180], [70, 110, 150], [110]]
    for k, (off, title) in enumerate([({(1, 1), (1, 3), (2, 0)}, 'paso 1 (entrenando)'), ({(1, 0), (1, 4), (2, 2)}, 'paso 2 (entrenando)'), (set(), 'al predecir: todas')]):
        x0 = 20 + k * 215; xs = [x0 + 10, x0 + 70, x0 + 130, x0 + 175]
        for l in range(3):
            for i, a in enumerate(layers_[l]):
                for j, b in enumerate(layers_[l + 1]):
                    dead = (l, i) in off or (l + 1, j) in off
                    s += f'<line x1="{xs[l]}" y1="{a}" x2="{xs[l + 1]}" y2="{b}" style="stroke:{B};stroke-width:1.2;opacity:{.08 if dead else .55}"/>'
        for l, ys in enumerate(layers_):
            for i, y in enumerate(ys):
                dead = (l, i) in off
                s += f'<circle cx="{xs[l]}" cy="{y}" r="9" style="fill:{"var(--paper)" if dead else (A if l == 3 else B)};stroke:{M if dead else "none"};stroke-width:1.5"/>'
                if dead:
                    s += f'<path d="M{xs[l] - 6} {y - 6} L{xs[l] + 6} {y + 6} M{xs[l] + 6} {y - 6} L{xs[l] - 6} {y + 6}" style="stroke:{CO};stroke-width:2.5"/>'
        s += t(x0 + 92, 214, title, I if k < 2 else T, 14, weight=700)
    return svg(660, 230, 'Dropout: en cada paso de entrenamiento se apagan al azar neuronas distintas; al predecir trabajan todas', s)


# ------------------------------------------------------------------ Tema 1 · robustness
def mover():
    """Accuracy when the photo is moved 0..4 px: the CNN of week 2 vs the same CNN trained with RandomTranslation(0.15)."""
    a = T1['aumento']; sin = [a['sin']['test']] + [a['sin']['shift'][str(k)] for k in range(1, 5)]
    con = [a['con']['test']] + [a['con']['shift'][str(k)] for k in range(1, 5)]
    X = lambda k: 90 + k * 115; Y = lambda v: 210 - v * 180
    s = axes(70, 30, 570, 210, [0.25, 0.5, 0.75, 1.0], Y, lambda v: f'{int(v * 100)} %')
    for vals, other, col in ((sin, con, CO), (con, sin, T)):
        s += poly([(X(k), Y(v)) for k, v in enumerate(vals)], col, 3.5)
        for k, v in enumerate(vals):
            dy = -12 if v >= other[k] else 20
            s += f'<circle cx="{X(k)}" cy="{Y(v):.1f}" r="5" style="fill:{col}"/>' + t(X(k), Y(v) + dy, pct(v), col, 13)
    s += ''.join(t(X(k), 234, f'{k} px', M, 13, weight=500) for k in range(5))
    s += t(90, 262, '— sin aumento (la CNN de la semana 2)', CO, 14, 'start') + t(380, 262, '— con aumento de datos', T, 14, 'start')
    return svg(600, 272, 'Exactitud real del NB05 al mover la prenda de 0 a 4 píxeles: sin aumento cae de 87.7 a 28.2 por ciento; con aumento de datos va de 82.6 a 76.4 por ciento', s)


def adversarial():
    """The real first botín of the test set, the FGSM noise (sign), the adversarial photo and both answers."""
    e = T1['ejemplo_adv']; c = 5
    s = gray(e['orig'], 20, 30, c)
    # noise: + (amber) / - (blue) where the adversarial photo differs from the original
    s += f'<rect x="190" y="30" width="{28 * c}" height="{28 * c}" style="fill:var(--bg);stroke:{L}"/>'
    noise = [[(245, 158, 11, 255) if e['adv'][i][j] > e['orig'][i][j] else (91, 140, 255, 255) if e['adv'][i][j] < e['orig'][i][j] else (0, 0, 0, 0)
              for j in range(28)] for i in range(28)]
    s += _img(_png(noise), 190, 30, c)
    s += gray(e['adv'], 360, 30, c)
    s += t(175, 105, '+', I, 30) + t(345, 105, '=', I, 30)
    s += t(90, 194, 'la foto original', M, 13, weight=500) + t(260, 194, 'ruido: ± 0.05 por píxel', M, 13, weight=500) + t(430, 194, 'la foto adversarial', M, 13, weight=500)
    po, pa = e['p_orig'], e['p_adv']
    s += t(90, 218, f'{CLASES[9]} {round(100 * po[9])} %', T, 16, weight=700) + t(430, 218, f'{CLASES[7]} {round(100 * pa[7])} %', CO, 16, weight=700)
    s += t(260, 218, '(el ruido se ve aquí exagerado)', M, 12, weight=500)
    # probability bars of the two answers (original vs adversarial)
    s += t(560, 46, 'Lo que dice la red', I, 14, 'start', 700)
    for r, (lab, idx) in enumerate([('botín', 9), ('zapatilla', 7), ('sandalia', 5)]):
        y = 66 + r * 42
        s += t(560, y + 4, lab, M, 13, 'start', 500)
        s += f'<rect x="630" y="{y - 8}" width="{po[idx] * 110:.1f}" height="11" rx="3" style="fill:{T}"/>'
        s += f'<rect x="630" y="{y + 6}" width="{pa[idx] * 110:.1f}" height="11" rx="3" style="fill:{CO}"/>'
    s += t(560, 200, '■ original   ', T, 12, 'start') + t(640, 200, '■ adversarial', CO, 12, 'start')
    return svg(760, 232, 'El primer botín de prueba: la red dice botín con 96 por ciento. Sumando un ruido de más o menos 0.05 en cada píxel, invisible a la vista, la red dice zapatilla con 67 por ciento', s)


def fgsm_curva():
    """Accuracy vs epsilon: the normal CNN and the CNN with adversarial training."""
    eps = ['limpia', '0.01', '0.02', '0.05', '0.1']
    n, v = T1['fgsm'], T1['fgsm_entrenada']
    X = lambda k: 90 + k * 115; Y = lambda p: 210 - p * 180
    s = axes(70, 30, 570, 210, [0.25, 0.5, 0.75, 1.0], Y, lambda p: f'{int(p * 100)} %')
    for d, o, col in ((n, v, CO), (v, n, T)):
        pts = [(X(k), Y(d[e])) for k, e in enumerate(eps)]
        s += poly(pts, col, 3.5)
        for (x, y), e in zip(pts, eps):
            dy = -12 if d[e] >= o[e] else 20
            s += f'<circle cx="{x}" cy="{y:.1f}" r="5" style="fill:{col}"/>' + t(x, y + dy, pct(d[e]), col, 13)
    s += ''.join(t(X(k), 234, 'ε = 0' if e == 'limpia' else f'ε = {e}', M, 13, weight=500) for k, e in enumerate(eps))
    s += t(90, 262, '— la CNN normal', CO, 14, 'start') + t(300, 262, '— vacunada (entrenamiento adversarial)', T, 14, 'start')
    return svg(600, 272, 'Exactitud real del NB05 frente a ejemplos adversariales de tamaño épsilon: la CNN normal cae de 87.7 a 13 por ciento; la vacunada empieza en 84.1 y aguanta 71.7 por ciento con épsilon 0.05', s)


def busqueda():
    """The six random trials of NB05 on the mock exam (validation); the best one, measured once on the final exam."""
    tr = T1['busqueda']['trials']; best = T1['busqueda']['best']
    s = t(20, 22, 'learning rate · filtros · dropout', M, 13, 'start', 500) + t(600, 22, 'en el simulacro', M, 13, 'end', 500)
    for k, c in enumerate(tr):
        y = 44 + k * 30; on = k == best; w = (c['val'] - 0.6) / 0.3 * 300
        s += t(20, y + 13, f"{c['lr']:g} · {c['f1']} · {c['drop']:g}", I if on else M, 14, 'start', 700 if on else 500)
        s += f'<rect x="230" y="{y}" width="{w:.1f}" height="20" rx="5" style="fill:{A if on else B};opacity:{1 if on else .55}"/>'
        s += t(236 + w, y + 15, pct(c['val']), I, 13, 'start', 700 if on else 500)
    s += t(20, 238, f"La mejor en el simulacro, medida una sola vez en el examen final: {pct(T1['busqueda']['test_best'])}", A, 14, 'start', 700)
    return svg(620, 250, 'Las seis combinaciones al azar del NB05 en el simulacro: la mejor, learning rate 0.01, 32 filtros y dropout 0.3, logra 86.8 por ciento y 86.9 en el examen final', s)


# ------------------------------------------------------------------ Tema 2 · transfer learning
def congelar():
    """Frozen base (what it already knew) + a new output layer; fine-tuning unlocks everything with small steps."""
    s = ''
    for k, (title, locked, note) in enumerate([('Congelar', True, 'solo se entrena la salida nueva (3 204 de 8 004 números)'), ('Ajuste fino', False, 'después se ajusta todo, con pasos pequeños (learning rate 0.0001)')]):
        y0 = 20 + k * 92
        s += t(20, y0 + 40, title, I, 16, 'start', 700)
        for i, n in enumerate(['Conv2D(16)', 'MaxPool', 'Conv2D(32)', 'MaxPool', 'Flatten']):
            x = 140 + i * 86
            s += f'<rect x="{x}" y="{y0 + 8}" width="78" height="46" rx="9" style="fill:{"var(--blue-bg)" if locked else "var(--amber-bg)"};stroke:{B if locked else A};stroke-width:2"/>' + t(x + 39, y0 + 36, n, I, 12.5)
        s += f'<rect x="572" y="{y0 + 8}" width="78" height="46" rx="9" style="fill:var(--amber-bg);stroke:{A};stroke-width:3"/>' + t(611, y0 + 30, 'Dense(4)', I, 12.5) + t(611, y0 + 46, 'nueva', A, 11.5)
        s += t(140, y0 + 74, ('🔒 ya saben ver · ' if locked else '') + note, M, 13, 'start', 500)
    return svg(670, 200, 'Transfer learning: congelar las capas que ya saben ver y entrenar solo una salida nueva; en el ajuste fino se ajusta todo con pasos pequeños', s)


def transfer():
    """Real NB06 results: 4 kinds of tops with 5, 20 and 100 photos per class."""
    d = T2['transfer']; cols = [('desde_cero', 'desde cero', CO), ('congelada', 'congelada', B), ('ajuste_fino', 'ajuste fino', A)]
    Y = lambda v: 220 - v * 260
    s = axes(60, 30, 620, 220, [0.25, 0.5, 0.75], Y, lambda v: f'{int(v * 100)} %')
    s += f'<line x1="60" y1="{Y(.25):.1f}" x2="620" y2="{Y(.25):.1f}" style="stroke:{M};stroke-width:1.5"/>' + t(64, Y(.25) - 6, 'azar', M, 12, 'start', 500)
    for g, n in enumerate(('5', '20', '100')):
        x0 = 100 + g * 180
        for k, (key, lab, col) in enumerate(cols):
            v = d[n][key]; x = x0 + k * 44
            s += f'<rect x="{x}" y="{Y(v):.1f}" width="38" height="{220 - Y(v):.1f}" rx="4" style="fill:{col}"/>' + t(x + 19, Y(v) - 6, num(v), I, 12.5)
        s += t(x0 + 63, 242, f'{n} fotos por clase', I, 14)
    s += ''.join(t(110 + k * 170, 270, f'■ {lab}', col, 14, 'start') for k, (_, lab, col) in enumerate(cols))
    return svg(640, 280, 'Resultados reales del NB06 con 4 prendas de arriba: con 5 fotos por clase, desde cero 30.6, congelada 45.9 y ajuste fino 47.2 por ciento; con 100 fotos por clase, 68.8, 66.7 y 68.0', s)


# ------------------------------------------------------------------ Tema 2 · explaining images
def mapas():
    """Real maps of NB06 for three test photos: photo, occlusion, Grad-CAM and gradient x image."""
    c = 3.2; s = ''
    heads = ['la foto', 'oclusión', 'Grad-CAM', 'gradiente × imagen']
    for j, h in enumerate(heads):
        s += t(150 + j * 104, 22, h, I, 13, weight=700)
    for r, m in enumerate(T2['mapas']):
        y = 34 + r * 104; px = PX[m['i']]
        s += t(14, y + 40, CLASES[m['label']], I, 14, 'start', 700) + t(14, y + 60, f"{round(100 * m['p'])} %", M, 13, 'start', 500)
        s += gray(px, 105, y, c)
        s += heat(m['oclusion'], 209, y, c, 'amber', under=px)
        s += heat(m['gradcam'], 313, y, c, 'amber', under=px)
        s += heat(m['gradx'], 417, y, c, 'amber', under=px, gamma=.6)
    return svg(540, 350, 'Mapas reales del NB06 para un botín, una camisa y un bolso: la foto, la oclusión, Grad-CAM y gradiente por imagen; el color muestra dónde influyó más en la decisión', s)


def cordura():
    """Sanity check: maps of the trained network vs the same architecture with random weights, and the average Spearman correlation (30 photos)."""
    c = 3.0; m0 = T2['mapas'][0]; rnd = T2['cordura_mapas']; px = PX[m0['i']]; s = ''
    for k, (key, name, col, hc) in enumerate([('gradcam', 'Grad-CAM', A, 'amber'), ('gradx', 'gradiente × imagen', B, 'blue')]):
        x0 = 20 + k * 200
        s += t(x0 + 88, 20, name, col, 14, weight=700)
        s += heat(m0[key], x0, 30, c, hc, under=px, gamma=1 if key == 'gradcam' else .6)
        s += heat(rnd[key], x0 + 92, 30, c, hc, under=px, gamma=1 if key == 'gradcam' else .6)
        s += t(x0 + 42, 135, 'entrenada', M, 12, weight=500) + t(x0 + 134, 135, 'pesos al azar', M, 12, weight=500)
    # Spearman bars: 1 = identical maps, 0 = nothing to do with each other
    s += t(440, 30, 'Parecido entre los dos mapas', I, 14, 'start', 700) + t(440, 48, '(promedio de 30 fotos · 1 = idénticos)', M, 12, 'start', 500)
    for r, (key, name) in enumerate([('gradcam', 'Grad-CAM'), ('oclusion', 'oclusión'), ('gradx', 'gradiente × imagen')]):
        v = T2['cordura'][key]; y = 68 + r * 30; ok = v < 0.5
        s += t(440, y + 13, name, M, 13, 'start', 500)
        x0 = 580; w = abs(v) * 90
        s += f'<line x1="{x0}" y1="{y - 4}" x2="{x0}" y2="{y + 22}" style="stroke:{L};stroke-width:1.5"/>'
        s += f'<rect x="{x0 if v >= 0 else x0 - w:.1f}" y="{y}" width="{w:.1f}" height="16" rx="3" style="fill:{T if ok else CO}"/>'
        s += t(x0 + (w if v >= 0 else 0) + 6, y + 13, f"{v:.2f}".replace('-', '−') + (' ✓ pasa' if ok else ' ✗ no pasa'), T if ok else CO, 12.5, 'start', 700)
    s += t(20, 162, 'Si la red ya no sabe nada, un mapa fiel debe cambiar: Grad-CAM y la oclusión cambian; gradiente × imagen casi no.', M, 13, 'start', 500)
    return svg(780, 175, 'Prueba de cordura real del NB06: con pesos al azar el mapa de Grad-CAM cambia por completo, el de gradiente por imagen casi no cambia; correlaciones promedio menos 0.12, menos 0.05 y 0.90', s)


# ------------------------------------------------------------------ Tema 2 · explaining a credit decision
NOMBRES = {'carga': 'carga (cuota / ingreso)', 'atrasos': 'atrasos en 12 meses', 'garante': 'garante', 'antiguedad': 'antigüedad',
           'rural': 'zona rural', 'ingreso': 'ingreso', 'ahorro': 'ahorro'}


def importancia():
    """Permutation importance: how much the AUC drops if a column is shuffled."""
    imp = sorted(T2['coop']['importancia'].items(), key=lambda kv: -kv[1]); s = ''
    for r, (k, v) in enumerate(imp):
        y = 16 + r * 30; w = max(v, 0) / 0.13 * 330
        s += t(200, y + 14, NOMBRES[k], I if r == 0 else M, 14, 'end', 700 if r == 0 else 500)
        s += f'<rect x="212" y="{y}" width="{max(w, 1.5):.1f}" height="20" rx="4" style="fill:{A if r == 0 else B};opacity:{1 if r == 0 else .6}"/>'
        s += t(220 + w, y + 15, f'{v:.3f}'.replace('-', '−'), I, 13, 'start', 600)
    s += t(212, 236, 'cuánto baja el AUC si se mezcla esa columna (más = pesa más en el modelo)', M, 13, 'start', 500)
    return svg(720, 248, 'Importancia por permutación en la cooperativa ficticia: la carga es lo que más pesa en general (0.125), después los atrasos (0.051) y el garante (0.049)', s)


def shap_socia():
    """SHAP waterfall of the fictitious member: from the average (0.13) to her probability (0.61)."""
    c = T2['coop']['socia']; base = c['base']; sv = sorted(c['shap'].items(), key=lambda kv: -abs(kv[1]))
    X = lambda p: 210 + p * 560; s = ''
    s += f'<line x1="{X(.5):.1f}" y1="10" x2="{X(.5):.1f}" y2="{30 + 30 * (len(sv) + 1)}" style="stroke:{M};stroke-width:1.5;stroke-dasharray:5 4"/>' + t(X(.5), 22, 'se rechaza desde 0.50', M, 12, 'middle', 500)
    s += t(200, 48, 'promedio de todos', M, 13.5, 'end', 500) + f'<rect x="{X(0)}" y="34" width="{X(base) - X(0):.1f}" height="20" rx="4" style="fill:{M};opacity:.5"/>' + t(X(base) + 6, 49, f'{base:.2f}', I, 13, 'start')
    acc = base
    for r, (k, v) in enumerate(sv):
        y = 64 + r * 30; a, b = (acc, acc + v) if v >= 0 else (acc + v, acc)
        col = CO if v > 0 else T
        s += t(200, y + 14, NOMBRES[k], I if r == 0 else M, 13.5, 'end', 700 if r == 0 else 500)
        s += f'<rect x="{X(a):.1f}" y="{y}" width="{max(X(b) - X(a), 2):.1f}" height="20" rx="4" style="fill:{col}"/>'
        s += t(X(b) + 6 if v >= 0 else X(a) - 6, y + 15, f'{v:+.2f}'.replace('-', '−'), col, 13, 'start' if v >= 0 else 'end', 700)
        acc += v
    y = 64 + len(sv) * 30
    s += t(200, y + 14, 'su probabilidad', I, 14, 'end', 700) + f'<rect x="{X(0)}" y="{y}" width="{X(acc) - X(0):.1f}" height="20" rx="4" style="fill:{CO}"/>' + t(X(acc) + 6, y + 15, f'{c["prob"]:.2f}', CO, 14, 'start', 700)
    s += t(210, y + 46, '■ empuja hacia rechazar', CO, 13, 'start') + t(420, y + 46, '■ empuja hacia aprobar', T, 13, 'start')
    return svg(660, y + 58, 'SHAP de la socia ficticia: desde el promedio 0.13, sus 2 atrasos suman 0.30, la zona rural 0.08, no tener garante y la antigüedad 0.04 cada uno; la carga resta 0.02; su probabilidad de mora es 0.61', s)


def zona():
    """Rejection rate and false alarms by zone, with and without the column 'rural'."""
    c = T2['coop']; Y = lambda v: 190 - v * 1500; s = axes(60, 30, 620, 190, [0.03, 0.06, 0.09], Y, lambda v: f'{round(v * 100)} %')
    groups = [('Con la columna «rural»', c['por_zona']), ('Sin la columna «rural»', c['sin_rural'])]
    for g, (title, d) in enumerate(groups):
        x0 = 90 + g * 280
        for k, (key, lab) in enumerate([('rechazo', 'rechazados'), ('falsa_alarma', 'falsas alarmas')]):
            for z, (zz, col) in enumerate([('rural', A), ('urbana', B)]):
                v = d[zz][key]; x = x0 + k * 120 + z * 46
                s += f'<rect x="{x}" y="{Y(v):.1f}" width="40" height="{190 - Y(v):.1f}" rx="4" style="fill:{col};opacity:{1 if k == 0 else .6}"/>' + t(x + 20, Y(v) - 6, pct(v), I, 12)
            s += t(x0 + k * 120 + 43, 208, lab, M, 12.5, weight=500)
        s += t(x0 + 103, 232, title, I, 14, weight=700)
    s += t(90, 262, '■ rural', A, 14, 'start') + t(170, 262, '■ urbana', B, 14, 'start') + t(270, 262, 'falsa alarma: rechazar a alguien que sí habría pagado', M, 13, 'start', 500)
    return svg(640, 272, 'Por zona en la cooperativa ficticia: con la columna rural se rechaza al 8.9 por ciento de los rurales y al 3.7 de los urbanos; sin la columna, 6.4 y 5.6 por ciento', s)
