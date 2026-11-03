"""Inline SVG figures for the week-2 study guide. They use the page colors (CSS variables of doc_kit2),
so they work in light and dark mode. Real data comes from the NB03/NB04 runs (deck/src/data/*.json)."""
import json, math, pathlib

_HERE = pathlib.Path(__file__).resolve().parent
_DATA = [_HERE / 'data',
         _HERE.parent / 'slides' / 'src' / 'data',                             # repo: semana2/docencia/codigo_fuente/slides/src/data
         pathlib.Path('/home/claude/w2/deck/src/data')]                        # build workspace
_D = next(d for d in _DATA if (d / 'fmnist.json').exists())
FM = json.loads((_D / 'fmnist.json').read_text())
SQ = json.loads((_D / 'seq.json').read_text())

B, A, T, P, I, M, L = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--purple)', 'var(--ink)', 'var(--muted)', 'var(--line)'
FONT = "font-family:'IBM Plex Sans',Arial,sans-serif"


def t(x, y, s, col=I, size=15, anchor='middle', weight=600):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="fill:{col};font:{weight} {size}px \'IBM Plex Sans\',Arial,sans-serif">{s}</text>'


def svg(w, h, label, inner):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">{inner}</svg>'


# ------------------------------------------------------------------ 01 · images
def prenda():
    """The real first test image of Fashion-MNIST (a botín), 28 x 28, and the 3 x 3 window used in NB03 §1."""
    px = FM['samples'][0]['px']
    s, c = '', 9
    for i in range(28):
        for j in range(28):
            v = px[i][j]
            s += f'<rect x="{10 + j * c}" y="{10 + i * c}" width="{c}" height="{c}" fill="rgb({v},{v},{v})"/>'
    s += f'<rect x="{10 + 13 * c}" y="{10 + 11 * c}" width="{3 * c}" height="{3 * c}" fill="none" style="stroke:{A};stroke-width:3"/>'
    s += f'<line x1="{10 + 16 * c}" y1="{10 + 11 * c}" x2="330" y2="40" style="stroke:{A};stroke-width:2"/>'
    s += f'<line x1="{10 + 16 * c}" y1="{10 + 14 * c}" x2="330" y2="212" style="stroke:{A};stroke-width:2"/>'
    W = [[px[r][k] / 255 for k in range(13, 16)] for r in range(11, 14)]
    for i, row in enumerate(W):
        for j, v in enumerate(row):
            g = round(v * 255)
            s += f'<rect x="{330 + j * 58}" y="{40 + i * 58}" width="56" height="56" rx="6" fill="rgb({g},{g},{g})" style="stroke:{L}"/>'
            s += t(358 + j * 58, 74 + i * 58, f'{v:.2f}', '#0B1424' if g > 120 else '#EEF2F8', 15)
    s += t(417, 236, 'filas 11–13 · columnas 13–15', M, 13)
    s += t(136, 278, '28 × 28 = 784 números', M, 14)
    return svg(520, 290, 'La primera foto de prueba de Fashion-MNIST, un botín, como una tabla de 28 por 28 brillos, con una ventana de 3 por 3 ampliada y sus números', s)


def suposicion():
    s = ''
    for k, (x, title, col, sub) in enumerate([(10, 'Densa', B, 'todo con todo'), (220, 'CNN', A, 'lo cercano importa'), (430, 'RNN', T, 'el orden importa')]):
        s += f'<rect x="{x}" y="10" width="190" height="170" rx="16" style="fill:var(--bg);stroke:{L}"/>'
        s += t(x + 95, 205, title, col, 17, weight=700) + t(x + 95, 226, sub, M, 14)
    Lp, Rp = [40, 75, 110, 145], [55, 95, 135]
    s += ''.join(f'<line x1="50" y1="{a}" x2="160" y2="{b}" style="stroke:{B};stroke-width:1.4;opacity:.7"/>' for a in Lp for b in Rp)
    s += ''.join(f'<circle cx="50" cy="{a}" r="8" style="fill:var(--paper);stroke:{B};stroke-width:2.5"/>' for a in Lp)
    s += ''.join(f'<circle cx="160" cy="{b}" r="9" style="fill:{B}"/>' for b in Rp)
    for i in range(6):
        for j in range(6):
            s += f'<rect x="{245 + j * 24}" y="{28 + i * 24}" width="22" height="22" rx="3" style="fill:var(--blue-bg)"/>'
    s += f'<rect x="{245 + 24 - 2}" y="{28 + 48 - 2}" width="{3 * 24 + 2}" height="{3 * 24 + 2}" rx="5" fill="none" style="stroke:{A};stroke-width:4"/>'
    for i in range(4):
        x = 448 + i * 40
        s += f'<rect x="{x}" y="72" width="30" height="40" rx="7" style="fill:var(--teal-bg);stroke:{T};stroke-width:2.5"/>'
        s += t(x + 15, 140, f'x{"₁₂₃₄"[i]}', M, 13)
        if i < 3:
            s += f'<path d="M{x + 30} 92 h10" style="stroke:{T};stroke-width:3"/>'
    return svg(630, 240, 'Tres suposiciones: la red densa conecta todo con todo; la CNN mira una ventana pequeña que recorre la imagen; la RNN lee en orden, paso por paso', s)


def conv():
    s = ''
    X = [[0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1]]
    for i in range(6):
        for j in range(6):
            g = 235 if X[i][j] else 25
            s += f'<rect x="{10 + j * 34}" y="{20 + i * 34}" width="32" height="32" rx="3" fill="rgb({g},{g},{g})" style="stroke:{L}"/>'
    s += f'<rect x="{10 + 1 * 34 - 2}" y="{20 + 1 * 34 - 2}" width="{3 * 34 + 2}" height="{3 * 34 + 2}" fill="none" style="stroke:{A};stroke-width:4"/>'
    K = [[-1, 0, 1]] * 3
    for i in range(3):
        for j in range(3):
            v = K[i][j]
            col = 'var(--blue-bg)' if v < 0 else 'var(--amber-bg)' if v > 0 else 'var(--bg)'
            s += f'<rect x="{262 + j * 40}" y="{68 + i * 40}" width="38" height="38" rx="6" style="fill:{col};stroke:{L}"/>' + t(281 + j * 40, 93 + i * 40, {-1: '−1', 0: '0', 1: '+1'}[v], I, 15)
    s += t(321, 52, 'filtro (3 × 3)', M, 13) + t(236, 133, '×', M, 26) + t(406, 133, '→', M, 26)
    out = [[0, 3, 3, 0]] * 4
    for i in range(4):
        for j in range(4):
            v = out[i][j]
            on = (i, j) == (1, 1)
            s += f'<rect x="{432 + j * 40}" y="{54 + i * 40}" width="38" height="38" rx="6" style="fill:{"var(--amber-bg)" if v else "var(--bg)"};stroke:{A if on else L};stroke-width:{3 if on else 1}"/>' + t(451 + j * 40, 79 + i * 40, v, I, 15)
    s += t(511, 40, 'mapa de activación (4 × 4)', M, 13)
    s += t(112, 238, 'foto: oscuro | claro', M, 13)
    return svg(600, 250, 'Un filtro de borde vertical recorre una foto de 6 por 6 con la mitad izquierda oscura y la derecha clara: el mapa de 4 por 4 se enciende con 3 justo en el borde y vale 0 donde todo es igual', s)


def share():
    s = f'<rect x="10" y="10" width="290" height="200" rx="16" style="fill:var(--bg);stroke:{L}"/><rect x="320" y="10" width="290" height="200" rx="16" style="fill:var(--bg);stroke:{L}"/>'
    for i in range(7):
        for j in range(7):
            s += f'<line x1="{36 + j * 22}" y1="{40 + i * 22}" x2="262" y2="106" style="stroke:{B};stroke-width:.7;opacity:.45"/>'
    for i in range(7):
        for j in range(7):
            s += f'<rect x="{30 + j * 22}" y="{34 + i * 22}" width="12" height="12" rx="2" style="fill:var(--blue-bg);stroke:{B};stroke-width:.8"/>'
    s += f'<circle cx="266" cy="106" r="14" style="fill:{B}"/>'
    for i in range(7):
        for j in range(7):
            s += f'<rect x="{352 + j * 32}" y="{30 + i * 22}" width="30" height="20" rx="2" style="fill:var(--amber-bg)"/>'
    for k, (a, b) in enumerate([(0, 0), (2, 2), (4, 4), (1, 4)]):
        s += f'<rect x="{351 + b * 32}" y="{29 + a * 22}" width="{3 * 32}" height="{3 * 22}" rx="4" fill="none" style="stroke:{A};stroke-width:3;opacity:{1 - k * .2}"/>'
    s += t(155, 236, 'densa: un peso por píxel, por neurona', B, 14) + t(465, 236, 'CNN: el mismo filtro de 10 números', A, 14)
    return svg(620, 250, 'Izquierda: una neurona densa con una línea a cada píxel. Derecha: el mismo filtro pequeño estampado en varias posiciones de la foto', s)


def pool():
    G = [[1, 3, 0, 2], [5, 2, 1, 0], [0, 1, 4, 6], [2, 0, 3, 1]]
    cols = [A, B, T, P]
    s = ''
    for i in range(4):
        for j in range(4):
            q = (i // 2) * 2 + j // 2
            blk = [G[(i // 2) * 2 + a][(j // 2) * 2 + b] for a in (0, 1) for b in (0, 1)]
            mx = G[i][j] == max(blk)
            s += f'<rect x="{10 + j * 50}" y="{10 + i * 50}" width="48" height="48" rx="6" style="fill:var(--bg);stroke:{cols[q]};stroke-width:{4 if mx else 1.5}"/>' + t(34 + j * 50, 41 + i * 50, G[i][j], cols[q] if mx else M, 18, weight=700 if mx else 500)
    s += t(250, 112, '→', M, 30)
    for i, row in enumerate([[5, 2], [2, 6]]):
        for j, v in enumerate(row):
            s += f'<rect x="{290 + j * 62}" y="{50 + i * 62}" width="58" height="58" rx="8" style="fill:var(--paper);stroke:{cols[i * 2 + j]};stroke-width:4"/>' + t(319 + j * 62, 88 + i * 62, v, cols[i * 2 + j], 22, weight=700)
    s += t(110, 232, 'mapa 4 × 4', M, 14) + t(350, 194, 'MaxPooling 2 × 2', M, 14)
    return svg(440, 245, 'MaxPooling de 2 por 2: de cada ventana de cuatro números queda el mayor; un mapa de 4 por 4 pasa a 2 por 2', s)


def shapes():
    blocks = [('foto', '28×28×1', 28, 1, M), ('Conv2D 16', '26×26×16', 26, 16, A), ('MaxPool', '13×13×16', 13, 16, B),
              ('Conv2D 32', '11×11×32', 11, 32, A), ('MaxPool', '5×5×32', 5, 32, B), ('Flatten', '800', 0, 0, M), ('Dense 10', '10', 0, 0, T)]
    s, x = '', 10
    for name, sh, side, depth, col in blocks:
        if side:
            h = 26 + side * 4.2
            d = min(6, max(1, depth // 4))
            for k in range(d, -1, -1):
                s += f'<rect x="{x + k * 5}" y="{120 - h / 2 - k * 5}" width="{h * .62}" height="{h}" rx="4" style="fill:var(--paper);stroke:{col};stroke-width:2"/>'
            w = h * .62 + d * 5
        else:
            n = 14 if name == 'Flatten' else 6
            for k in range(n):
                s += f'<rect x="{x + 6}" y="{120 - n * 6 + k * 12}" width="14" height="10" rx="2" style="fill:{col};opacity:.75"/>'
            w = 26
        s += t(x + w / 2, 222, name, I, 13, weight=700) + t(x + w / 2, 240, sh, M, 12)
        if not side:
            x += 26                                                 # room for the label under the thin vector blocks
        x += w + 22
    return svg(int(x), 250, 'Las formas dentro de la CNN del NB03: 28 por 28 por 1, 26 por 26 por 16, 13 por 13 por 16, 11 por 11 por 32, 5 por 5 por 32, 800 números y 10 salidas', s)


def softmax_bars():
    smp = next(s for s in FM['samples'] if s['label'] == 6)
    p, names = smp['cnn'], FM['clases']
    order = sorted(range(10), key=lambda k: -p[k])
    s = ''
    for r, k in enumerate(order):
        y = 14 + r * 24
        s += t(110, y + 15, names[k], I if r == 0 else M, 14, 'end', 700 if r == 0 else 500)
        s += f'<rect x="120" y="{y}" width="300" height="18" rx="4" style="fill:var(--bg)"/>'
        s += f'<rect x="120" y="{y}" width="{max(1.5, 300 * p[k]):.1f}" height="18" rx="4" style="fill:{A if r == 0 else B};opacity:{1 if r == 0 else .7}"/>'
        s += t(430, y + 15, f'{p[k] * 100:.1f} %' if p[k] >= .001 else '< 0.1 %', I if r == 0 else M, 13, 'start')
    return svg(500, 260, 'Las 10 probabilidades que da la CNN para la primera camisa de prueba: camisa 77 %, camiseta 11 %, abrigo y suéter cerca de 5 % cada uno y casi cero para el resto; suman 100 %', s)


def duelo():
    R = FM['results']
    X = lambda px: 60 + px * 95
    Y = lambda a: 210 - a * 190
    s = f'<line x1="50" y1="210" x2="450" y2="210" style="stroke:{L};stroke-width:2"/><line x1="50" y1="20" x2="50" y2="210" style="stroke:{L};stroke-width:2"/>'
    for a in (0.25, 0.5, 0.75, 1.0):
        s += f'<line x1="50" y1="{Y(a)}" x2="450" y2="{Y(a)}" style="stroke:{L};stroke-width:1;stroke-dasharray:4 5"/>' + t(42, Y(a) + 5, f'{int(a * 100)} %', M, 12, 'end')
    for name, col in (('densa', B), ('cnn', A)):
        vals = [R[name]['test']] + [R[name]['shift'][str(k)] if str(k) in R[name]['shift'] else R[name]['shift'][k] for k in (1, 2, 3, 4)]
        pts = ' '.join(f'{X(k):.1f},{Y(v):.1f}' for k, v in enumerate(vals))
        s += f'<polyline points="{pts}" fill="none" style="stroke:{col};stroke-width:4"/>'
        s += ''.join(f'<circle cx="{X(k):.1f}" cy="{Y(v):.1f}" r="6" style="fill:{col}"/>' for k, v in enumerate(vals))
        s += (t(X(2) + 10, Y(vals[2]) - 14, f'{vals[2] * 100:.1f} %', col, 14, 'start', 700) if name == 'cnn'
              else t(X(2) - 12, Y(vals[2]) + 22, f'{vals[2] * 100:.1f} %', col, 14, 'end', 700))
    for k in range(5):
        s += t(X(k), 232, f'{k} px', M, 13)
    s += t(250, 252, 'cuántos píxeles movimos la prenda a la derecha', M, 13)
    s += f'<rect x="330" y="26" width="16" height="6" style="fill:{A}"/>' + t(352, 33, 'CNN', I, 13, 'start') + f'<rect x="330" y="44" width="16" height="6" style="fill:{B}"/>' + t(352, 51, 'densa', I, 13, 'start')
    return svg(470, 262, 'Exactitud en la prueba al mover las prendas de 0 a 4 píxeles: con 2 píxeles la densa cae a 56.5 % y la CNN aguanta 75.2 %; con 4 las dos se caen', s)


# ------------------------------------------------------------------ 02 · sequences
def orden():
    ej = SQ['orden']['ejemplo']
    s = ''
    for k, (vals, col, name, x0) in enumerate([(ej, 'var(--amber-f)', 'empeora', 20), (ej[::-1], T, 'mejora (los mismos meses al revés)', 330)]):
        mean = sum(vals) / len(vals)
        for i, v in enumerate(vals):
            s += f'<rect x="{x0 + i * 22}" y="{170 - v * 5.6:.1f}" width="17" height="{v * 5.6:.1f}" rx="3" style="fill:{col}"/>'
        s += f'<line x1="{x0 - 6}" y1="{170 - mean * 5.6:.1f}" x2="{x0 + 12 * 22}" y2="{170 - mean * 5.6:.1f}" style="stroke:{I};stroke-width:2;stroke-dasharray:6 5"/>'
        s += t(x0 + 130, 196, name, col, 14, weight=700)
    s += t(310, 222, 'días de atraso de un socio en 12 meses · línea punteada: el mismo promedio (13.2 días)', M, 13)
    return svg(620, 232, 'Un socio que empeora y el mismo socio con los meses al revés: las barras son las mismas y el promedio es idéntico; solo cambia el orden', s)


def eco():
    hs = [math.tanh(1.0)]
    for _ in range(3):
        hs.append(math.tanh(0.5 * hs[-1]))
    s = f'<line x1="40" y1="190" x2="440" y2="190" style="stroke:{L};stroke-width:2"/>'
    for i, h in enumerate(hs):
        x = 70 + i * 95
        s += f'<rect x="{x}" y="{190 - h * 210:.1f}" width="60" height="{h * 210:.1f}" rx="8" style="fill:{T};opacity:{.45 + h * .7:.2f}"/>'
        s += t(x + 30, 182 - h * 210, f'{h:.2f}', I, 16, weight=700) + t(x + 30, 212, f'h{"₁₂₃₄"[i]}', M, 14) + t(x + 30, 232, f'x = {1 if i == 0 else 0}', M, 13)
    return svg(470, 242, 'La libreta a mano con w igual a 1 y u igual a 0.5: el eco del primer dato se reduce más o menos a la mitad en cada paso: 0.76, 0.36, 0.18 y 0.09', s)


def unroll():
    s = ''
    for i in range(4):
        x = 30 + i * 140
        s += f'<rect x="{x}" y="70" width="90" height="60" rx="12" style="fill:var(--teal-bg);stroke:{T};stroke-width:3"/>' + t(x + 45, 106, 'celda', T, 15, weight=700)
        s += f'<line x1="{x + 45}" y1="175" x2="{x + 45}" y2="134" style="stroke:{I};stroke-width:2.5"/><polygon points="{x + 39},{140} {x + 45},{130} {x + 51},{140}" style="fill:{I}"/>'
        s += t(x + 45, 196, ['el', 'socio', 'pagó', 'a tiempo'][i], I, 14) + t(x + 45, 214, f'x{"₁₂₃₄"[i]}', M, 13)
        if i < 3:
            s += f'<line x1="{x + 92}" y1="100" x2="{x + 136}" y2="100" style="stroke:{T};stroke-width:3"/><polygon points="{x + 130},94 {x + 140},100 {x + 130},106" style="fill:{T}"/>' + t(x + 115, 90, f'h{"₁₂₃"[i]}', T, 13)
        s += f'<path d="M{x + 80} 62 C {x + 60} 30, {x + 30} 30, {x + 10} 62" fill="none" style="stroke:{A};stroke-width:2.5;stroke-dasharray:6 5;opacity:{.35 + i * .2}"/>'
    s += t(300, 26, 'la culpa vuelve hacia atrás, paso por paso, y se debilita', A, 14)
    s += t(300, 238, 'la misma celda, con los mismos pesos, en cada paso', M, 13)
    return svg(600, 248, 'La RNN desenrollada: la misma celda en cada paso pasa su libreta h al paso siguiente; la culpa del error viaja hacia atrás y se debilita', s)


def lstm():
    s = f'<line x1="20" y1="70" x2="600" y2="70" style="stroke:{T};stroke-width:7;stroke-linecap:round"/>' + t(310, 40, 'la cinta de la memoria (c): puede llevar lo importante muy lejos', T, 14)
    for name, x, col, d in (('olvidar', 150, 'var(--amber)', 'borrador: qué se borra'), ('guardar', 310, A, 'lápiz: qué se anota'), ('mostrar', 470, B, 'ventana: qué se lee')):
        s += f'<circle cx="{x}" cy="70" r="22" style="fill:var(--paper);stroke:{col};stroke-width:4"/>' + t(x, 76, 'σ', col, 18, weight=700)
        s += f'<line x1="{x}" y1="94" x2="{x}" y2="130" style="stroke:{col};stroke-width:3"/><rect x="{x - 70}" y="130" width="140" height="56" rx="12" style="fill:var(--bg);stroke:{L}"/>'
        s += t(x, 154, name, col, 16, weight=700) + t(x, 175, d, M, 12.5)
    return svg(620, 200, 'La LSTM: una cinta de memoria con tres compuertas, olvidar, guardar y mostrar; cada una es una sigmoide que se abre entre 0 y 1', s)


def memoria():
    M_ = SQ['memoria']
    s = f'<line x1="50" y1="200" x2="610" y2="200" style="stroke:{L};stroke-width:2"/>'
    Y = lambda a: 200 - a * 170
    for a in (0.5, 1.0):
        s += f'<line x1="50" y1="{Y(a)}" x2="610" y2="{Y(a)}" style="stroke:{L};stroke-width:1;stroke-dasharray:4 5"/>' + t(42, Y(a) + 5, f'{int(a * 100)} %', M, 12, 'end')
    s += t(610, Y(0.5) - 6, 'adivinar', M, 12, 'end')
    cols = {'rnn': B, 'lstm': P, 'atencion': A}
    for g, T_ in enumerate(['10', '30', '80']):
        for k, kind in enumerate(['rnn', 'lstm', 'atencion']):
            v = M_[T_][kind]['test']
            x = 80 + g * 165 + k * 42
            s += f'<rect x="{x}" y="{Y(v):.1f}" width="34" height="{v * 170:.1f}" rx="5" style="fill:{cols[kind]}"/>' + t(x + 17, Y(v) - 6, f'{v * 100:.0f}', I, 12, weight=700)
        s += t(80 + g * 165 + 59, 222, f'{T_} pasos', I, 14, weight=700)
    for k, (kind, name) in enumerate([('rnn', 'SimpleRNN'), ('lstm', 'LSTM'), ('atencion', 'atención')]):
        s += f'<rect x="{90 + k * 140}" y="238" width="14" height="10" style="fill:{cols[kind]}"/>' + t(110 + k * 140, 247, name, I, 13, 'start')
    return svg(620, 256, 'El examen de memoria del NB04: con 10 y 30 pasos los tres aciertan; con 80 pasos la SimpleRNN y la LSTM adivinan (52 % y 50 %) y la atención llega a 100 %', s)


# ------------------------------------------------------------------ 03 · attention
def attn_words():
    W = [('el', 36), ('socio', 106), ('pagó', 180), ('la', 244), ('cuota', 312), ('porque', 396), ('él', 480)]
    wt = {'socio': .786, 'cuota': .039}
    Y0 = 170
    s = ''
    for w, x in W[:-1]:
        if w not in wt:
            continue
        k = wt[w]
        apex = Y0 - 30 - min(110, (480 - x) * .3)
        col = A if w == 'socio' else B
        s += f'<path d="M478 {Y0 - 18} Q {(480 + x) / 2} {2 * apex - (Y0 - 18)} {x + 2} {Y0 - 18}" fill="none" style="stroke:{col};stroke-width:{2 + k * 12:.1f};stroke-linecap:round;opacity:.95"/>'
        s += (f'<text x="{(480 + x) / 2}" y="{apex - 12:.0f}" text-anchor="middle" style="fill:{col};font:700 15px \'IBM Plex Sans\',Arial,sans-serif;'
              f'paint-order:stroke;stroke:var(--paper);stroke-width:6px">{k * 100:.1f} %</text>')
    for w, x in W:
        on = w in ('socio', 'él')
        s += f'<rect x="{x - 29}" y="{Y0 - 17}" width="58" height="34" rx="8" style="fill:{"var(--amber-bg)" if on else "var(--bg)"};stroke:{A if on else L};stroke-width:2"/>' + t(x, Y0 + 6, w, I, 15, weight=700 if on else 500)
    s += t(480, Y0 + 38, 'consulta', A, 12, weight=700) + t(480, Y0 + 54, '17.5 % a sí misma', M, 12)
    s += t(240, Y0 + 54, 'en el NB04: 3 palabras con vectores escritos a mano', M, 12)
    return svg(530, 232, '«Él» mira a las otras palabras: 78.6 % a socio, 3.9 % a cuota y 17.5 % a sí misma', s)


def attn_weights():
    a = SQ['atencion']
    p, mk = a['pesos'], a['marca']
    s = f'<line x1="40" y1="170" x2="560" y2="170" style="stroke:{L};stroke-width:2"/>'
    for i, v in enumerate(p):
        h = max(1.2, v * 150)
        s += f'<rect x="{44 + i * 6.4:.1f}" y="{170 - h:.1f}" width="5" height="{h:.1f}" style="fill:{A if i == mk else B}"/>'
    s += t(44 + mk * 6.4 + 12, 170 - p[mk] * 150 + 4, f'paso {mk + 1}, el marcado: {p[mk] * 100:.1f} %', A, 14, 'start', 700)
    s += t(300, 192, 'los 80 pasos de un ejemplo del examen de memoria', M, 13)
    return svg(600, 200, f'Los pesos de atención de la red del NB04 sobre los 80 pasos de un ejemplo: el {p[mk] * 100:.1f} % cae en el paso marcado', s)


def costo():
    s = ''
    for i in range(3):
        for j in range(3):
            s += f'<rect x="{30 + j * 16}" y="{60 + i * 16}" width="13" height="13" rx="2" style="fill:{B}"/>'
    for i in range(9):
        for j in range(9):
            s += f'<rect x="{170 + j * 16}" y="{12 + i * 16}" width="13" height="13" rx="2" style="fill:{A};opacity:.9"/>'
    s += t(54, 128, '3 palabras', B, 14, weight=700) + t(54, 146, '9 comparaciones', M, 13)
    s += t(242, 172, '9 palabras (3 veces más)', A, 14, weight=700) + t(242, 190, '81 comparaciones (9 veces más)', M, 13)
    s += t(470, 60, '1 000 palabras', I, 14, weight=700) + t(470, 80, '1 000 000 de comparaciones', M, 13)
    s += t(470, 120, '1 000 000 de palabras', I, 14, weight=700) + t(470, 140, '10¹² comparaciones', M, 13)
    return svg(580, 200, 'El costo de la atención crece con el cuadrado: 3 palabras son 9 comparaciones y 9 palabras son 81; mil palabras son un millón', s)


def hibrido():
    s = ''
    for i in range(8):
        on = i == 3
        s += f'<rect x="{20 + i * 62}" y="30" width="52" height="110" rx="10" style="fill:{"var(--amber-bg)" if on else "var(--blue-bg)"};stroke:{A if on else B};stroke-width:2.5"/>' + t(46 + i * 62, 92, 'A' if on else 'R', A if on else B, 22, weight=700)
    s += t(262, 170, 'R = capa recurrente barata (Mamba) · A = capa de atención completa', M, 13)
    s += t(262, 18, 'Jamba (2024): una capa de atención por cada siete de Mamba', I, 14, weight=700)
    return svg(530, 182, 'Un modelo híbrido como Jamba: siete capas recurrentes por cada capa de atención', s)
