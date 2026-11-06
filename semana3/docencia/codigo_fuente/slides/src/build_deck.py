"""Builds the self-contained week-3 deck: semana3/docencia/slides/index.html (+ slides.json index).

usage: python build_deck.py <out_dir>
needs: Python 3.12+, segno, Node with the packages in ../fonts (katex, @fontsource-variable/*)
"""
import base64, json, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import kit                      # noqa: E402
import slides_tema1            # noqa: E402,F401  (Encuadre, 00 Recorderis, Tema 1)
import slides_tema2            # noqa: E402,F401  (Tema 2, Cierre)

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / 'out')
NM = pathlib.Path(os.environ.get('DECK_NODE_MODULES', HERE.parent / 'fonts' / 'node_modules'))

CONTRACT = """<!--
THESIS (week 3): the same keynote system as weeks 1 and 2. Being accurate is not enough: the network must work on new
  cases, survive small changes, reuse what it knows and explain its decisions. Real curves, a real adversarial boot, real
  occlusion and Grad-CAM maps and a fictional cooperative make every idea visible before it is named.
OWN-WORLD: "Sala de señales". Night blue-graphite ground, white Lexend, Unbounded for covers and big
  numbers; amber = sí/positive, azure = no/negative, mint = learned, coral = error/blame, lilac = trend
  thread. Live figure plates on a faint coordinate grid, chips.
STORY: two themes, not days (each session continues where the previous one stopped): a recorderis of weeks 1 and 2,
  Tema 1 (generalizar y ser robusto, NB05), Tema 2 (reutilizar y explicar, NB06) and the closing "¿Le creerías a tu red?".
FIRST VIEWPORT: Cover. Left: course chips, huge Unbounded title, teacher. Right: the real boot photo flipping between the
  original (botín 96 %) and its adversarial twin (zapatilla 67 %).
FORM: Classic presentation chosen by the teacher (canon), staged presenter-driven step by step.
-->"""


def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def fonts_css():
    fs = NM / '@fontsource-variable'
    rules = [
        ('Unbounded', fs / 'unbounded/files/unbounded-latin-wght-normal.woff2', '200 900'),
        ('Lexend', fs / 'lexend/files/lexend-latin-wght-normal.woff2', '100 900'),
        ('JetBrains Mono', fs / 'jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2', '100 800'),
    ]
    return '\n'.join(f'@font-face{{font-family:"{n}";src:url(data:font/woff2;base64,{b64(p)}) format("woff2");font-weight:{w};font-style:normal;font-display:swap}}'
                     for n, p, w in rules)


KEEP = {'KaTeX_Main-Regular', 'KaTeX_Main-Bold', 'KaTeX_Main-Italic', 'KaTeX_Math-Italic', 'KaTeX_Size1-Regular',
        'KaTeX_Size2-Regular', 'KaTeX_AMS-Regular'}


def katex_css():
    d = NM / 'katex' / 'dist'
    css = (d / 'katex.min.css').read_text()

    def face(m):
        block = m.group(0)
        name = re.search(r'url\(fonts/(KaTeX_[A-Za-z0-9_-]+)\.woff2\)', block)
        if not name or name.group(1) not in KEEP:
            return ''
        src = f'src:url(data:font/woff2;base64,{b64(d / "fonts" / (name.group(1) + ".woff2"))}) format("woff2")'
        return re.sub(r'src:[^;}]*', src, block)
    css = re.sub(r'@font-face\{[^}]*\}', face, css)
    assert 'url(fonts/' not in css
    return css


def render_math(html):
    texs = re.findall(r'<m>(.*?)</m>', html, flags=re.S)
    if not texs:
        return html
    r = subprocess.run(['node', str(HERE.parent / 'tools' / 'katex_render.js')], input=json.dumps(texs), capture_output=True, text=True,
                       env={**os.environ, 'KATEX_PATH': str(NM / 'katex')}, check=True)
    out = iter(json.loads(r.stdout))
    return re.sub(r'<m>(.*?)</m>', lambda m: next(out), html, flags=re.S)


def build():
    slides = kit.SLIDES
    ids = [s['id'] for s in slides]
    assert len(ids) == len(set(ids)), 'duplicate slide id'
    body = render_math('\n'.join(s['html'] for s in slides))
    css = (HERE / 'deck.css').read_text() + '\n' + (HERE / 'components.css').read_text() + '\n' + (HERE / 'w2.css').read_text() + '\n' + (HERE / 'w3.css').read_text()
    data = {k: json.loads((HERE / 'data' / f).read_text()) for k, f in [('FMNIST', 'fmnist.json'),   # week 2 (NB03): photos + results
                                                                          ('FMX', 'fm_extra.json'),    # 3 more photos (tools/extra_samples.py)
                                                                          ('T1', 'tema1.json'),        # NB05 (tools/run_tema1.py)
                                                                          ('T2', 'tema2.json')]}       # NB06 (tools/run_tema2.py)
    js = (''.join(f'window.{k} = ' + json.dumps(v, separators=(',', ':'), ensure_ascii=False) + ';\n' for k, v in data.items()) +
          (HERE / 'deck.js').read_text() + '\n' +
          ''.join((HERE / f).read_text() + '\n' for f in ['demos1.js', 'demos6.js', 'demos8.js', 'demos9.js']))
    assert '</script' not in js
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semana 3 · Slides</title>
<meta name="description" content="Slides interactivas de la semana 3 de Neural Networks: Deep Learning (UIDE): generalización, robustez, transfer learning y explicabilidad.">
<meta name="robots" content="noindex">
{CONTRACT}
<style>{fonts_css()}</style>
<style>{katex_css()}</style>
<style>{css}</style>
</head>
<body>
<div id="viewport"><div id="stage">
{body}
</div></div>
<nav id="chrome" aria-label="Controles de la presentación">
  <span class="sec-l"></span>
  <button type="button" data-a="prev" aria-label="Lámina anterior">←</button>
  <span class="cnt num"></span>
  <button type="button" data-a="next" aria-label="Lámina siguiente">→</button>
  <button type="button" data-a="index" title="Índice (G)">Índice</button>
  <button type="button" data-a="presenter" title="Vista del presentador (P)">Notas</button>
  <button type="button" data-a="full" title="Pantalla completa (F)" aria-label="Pantalla completa">⛶</button>
  <span class="bar"><i></i></span>
</nav>
<div id="laser"></div><div id="blank"></div><div id="index" role="dialog" aria-label="Índice"></div><div id="pv"></div>
<script>
{js}
</script>
</body>
</html>
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'index.html').write_text(html)
    idx = [{'n': i + 1, 'id': s['id'], 'title': s['title'], 'block': s['block'], 'group': s['group'], 'minutes': s['minutes']} for i, s in enumerate(slides)]
    (OUT / 'slides.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1))
    print(f'{len(slides)} slides · {len(html) / 1e6:.2f} MB → {OUT / "index.html"}')


if __name__ == '__main__':
    build()
