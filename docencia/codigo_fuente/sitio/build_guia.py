"""Student study guide: guia/index.html"""
import pathlib, sys, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit import page, section, chip, idea, box, formula, ex, colab, fig

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
COLAB = 'https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/'
NB1, NB2, NB3 = (COLAB + 'NB01_viernes_tu_primera_neurona.ipynb', COLAB + 'NB02_sabado_tu_primera_red.ipynb',
                 COLAB + 'NB03_miniproyecto_cooperativa_starter.ipynb')
B, A, T, P, I = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--purple)', 'var(--ink)'

# ------------------------------------------------------------------ small inline figures
def svg_neuron():
    return """<svg viewBox="0 0 640 260" width="640" height="260" role="img" aria-label="Neurona: tres entradas con pesos llegan a una suma, luego a una activación y salen como una salida">
<g style="stroke:var(--blue);stroke-width:3"><line x1="70" y1="50" x2="300" y2="122"/><line x1="70" y1="130" x2="300" y2="130"/><line x1="70" y1="210" x2="300" y2="138"/></g>
<g style="fill:var(--blue-bg);stroke:var(--blue);stroke-width:3"><circle cx="60" cy="50" r="26"/><circle cx="60" cy="130" r="26"/><circle cx="60" cy="210" r="26"/></g>
<g style="fill:var(--blue-d);font:italic 20px 'STIX Two Text',Georgia,serif" text-anchor="middle"><text x="60" y="57">x₁</text><text x="60" y="137">x₂</text><text x="60" y="217">x₃</text>
<text x="170" y="70">w₁</text><text x="170" y="122">w₂</text><text x="170" y="196">w₃</text></g>
<circle cx="340" cy="130" r="44" style="fill:var(--navy)"/><text x="340" y="142" text-anchor="middle" style="fill:#fff;font:34px Georgia,serif">Σ</text>
<line x1="384" y1="130" x2="430" y2="130" style="stroke:var(--ink);stroke-width:3"/>
<rect x="430" y="96" width="76" height="68" rx="14" style="fill:var(--amber-f)"/><text x="468" y="140" text-anchor="middle" style="fill:#0B1424;font:italic 30px Georgia,serif">φ</text>
<line x1="506" y1="130" x2="590" y2="130" style="stroke:var(--ink);stroke-width:3"/><polygon points="590,120 610,130 590,140" style="fill:var(--ink)"/>
<g style="fill:var(--muted);font:600 15px 'IBM Plex Sans',sans-serif" text-anchor="middle"><text x="340" y="196">suma + sesgo b</text><text x="468" y="190">activación</text><text x="560" y="116">salida</text><text x="60" y="250">datos</text></g>
</svg>"""

def curve(fn, x0, x1, X0, X1, Y0, Y1, ymin, ymax, n=100):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = fn(x)
        pts.append(f'{X0 + (x - x0) / (x1 - x0) * (X1 - X0):.1f},{Y0 - (y - ymin) / (ymax - ymin) * (Y0 - Y1):.1f}')
    return ' '.join(pts)

def svg_acts():
    sig = lambda z: 1 / (1 + math.exp(-z))
    def panel(x, title, pts):
        return (f'<g transform="translate({x},0)"><rect x="0" y="0" width="190" height="150" rx="12" style="fill:var(--bg);stroke:var(--line)"/>'
                f'<line x1="15" y1="120" x2="175" y2="120" style="stroke:var(--line);stroke-width:2"/><line x1="95" y1="15" x2="95" y2="130" style="stroke:var(--line);stroke-width:2"/>'
                f'<polyline points="{pts}" style="fill:none;stroke:var(--blue);stroke-width:4"/>'
                f'<text x="95" y="172" text-anchor="middle" style="fill:var(--ink);font:700 16px \'Space Grotesk\',sans-serif">{title}</text></g>')
    step = '15,120 95,120 95,30 175,30'
    s = curve(sig, -6, 6, 15, 175, 120, 30, 0, 1)
    relu = '15,118 95,118 175,30'
    return (f'<svg viewBox="0 0 620 185" width="620" height="185" role="img" aria-label="Tres funciones de activación: escalón, sigmoide y ReLU">'
            + panel(0, 'Escalón', step) + panel(215, 'Sigmoide', s) + panel(430, 'ReLU', relu) + '</svg>')

def svg_gd():
    L = lambda w: (w - 3) ** 2
    X = lambda w: 40 + (w + 0.5) / 7 * 520
    Y = lambda l: 230 - l / 10 * 200
    pts = curve(L, -0.17, 6.17, X(-0.17), X(6.17), 230, 30, 0, 10)
    ws = [0, 0.6, 1.08, 1.464, 1.771]
    dots = ''.join(f'<circle cx="{X(w):.1f}" cy="{Y(L(w)):.1f}" r="7" style="fill:var(--blue)"/>' for w in ws)
    path = ' '.join(f'{X(w):.1f},{Y(L(w)):.1f}' for w in ws)
    return (f'<svg viewBox="0 0 600 260" width="600" height="260" role="img" aria-label="Parábola de pérdida y cinco pasos de descenso de gradiente que bajan hacia el mínimo en w igual a 3">'
            f'<line x1="30" y1="230" x2="580" y2="230" style="stroke:var(--line);stroke-width:2"/>'
            f'<polyline points="{pts}" style="fill:none;stroke:var(--ink);stroke-width:3"/>'
            f'<polyline points="{path}" style="fill:none;stroke:var(--amber-f);stroke-width:3;stroke-dasharray:7 5"/>{dots}'
            f'<circle cx="{X(3):.1f}" cy="{Y(0):.1f}" r="8" style="fill:var(--teal)"/>'
            f'<text x="{X(3):.1f}" y="252" text-anchor="middle" style="fill:var(--teal);font:700 15px sans-serif">mínimo: w = 3</text>'
            f'<text x="{X(0)+12:.1f}" y="{Y(9)-6:.1f}" style="fill:var(--blue);font:700 15px sans-serif">empieza en w = 0</text></svg>')

def svg_mlp():
    L1 = [(70, y) for y in (60, 130, 200)]; L2 = [(270, y) for y in (40, 100, 160, 220)]; O = (470, 130)
    s = '<svg viewBox="0 0 560 260" width="560" height="260" role="img" aria-label="Red con tres entradas, cuatro neuronas ocultas y una salida">'
    s += ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" style="stroke:var(--blue);stroke-width:1.6;opacity:.6"/>' for a in L1 for b in L2)
    s += ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{O[0]}" y2="{O[1]}" style="stroke:var(--amber-f);stroke-width:2.4"/>' for a in L2)
    s += ''.join(f'<circle cx="{x}" cy="{y}" r="20" style="fill:var(--paper);stroke:var(--blue);stroke-width:3"/>' for x, y in L1)
    s += ''.join(f'<circle cx="{x}" cy="{y}" r="20" style="fill:var(--navy)"/>' for x, y in L2)
    s += f'<circle cx="{O[0]}" cy="{O[1]}" r="24" style="fill:var(--amber-f)"/>'
    s += ''.join(f'<text x="{x}" y="252" text-anchor="middle" style="fill:var(--muted);font:600 15px sans-serif">{t}</text>' for x, t in [(70, 'entrada'), (270, 'capa oculta'), (470, 'salida')])
    return s + '</svg>'

def svg_back():
    return """<svg viewBox="0 0 640 150" width="640" height="150" role="img" aria-label="Flechas: la predicción va de izquierda a derecha y la culpa vuelve de derecha a izquierda">
<g style="font:700 16px 'Space Grotesk',sans-serif" text-anchor="middle">
<rect x="10" y="40" width="130" height="70" rx="14" style="fill:var(--blue-bg)"/><text x="75" y="81" style="fill:var(--blue-d)">datos x</text>
<rect x="250" y="40" width="140" height="70" rx="14" style="fill:var(--navy)"/><text x="320" y="81" style="fill:#fff">capa oculta</text>
<rect x="500" y="40" width="130" height="70" rx="14" style="fill:var(--amber-f)"/><text x="565" y="81" style="fill:#0B1424">predicción ŷ</text></g>
<g style="stroke:var(--blue);stroke-width:3"><line x1="145" y1="58" x2="240" y2="58"/><line x1="395" y1="58" x2="490" y2="58"/></g>
<g style="fill:var(--blue)"><polygon points="240,50 252,58 240,66"/><polygon points="490,50 502,58 490,66"/></g>
<g style="stroke:var(--amber);stroke-width:3;stroke-dasharray:6 5"><line x1="155" y1="94" x2="248" y2="94"/><line x1="405" y1="94" x2="498" y2="94"/></g>
<g style="fill:var(--amber)"><polygon points="155,86 143,94 155,102"/><polygon points="405,86 393,94 405,102"/></g>
<g style="font:600 14px sans-serif" text-anchor="middle"><text x="320" y="22" style="fill:var(--blue)">1 · hacia adelante: predecir</text><text x="320" y="140" style="fill:var(--amber)">2 · hacia atrás: repartir la culpa</text></g>
</svg>"""

# ------------------------------------------------------------------ sections
S = []

S.append(('inicio', '★', 'Cómo usar esta guía', f"""
<div class="hero">
<span class="chip">Semana 1 · Guía de estudio</span>
<h1 style="margin-top:14px">Fundamentos de redes neuronales, de cero a tu primera red</h1>
<p>Todo lo de la semana en una sola página: la idea de cada tema en palabras sencillas, la fórmula explicada término por término, un ejemplo con números y ejercicios con su respuesta.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?pre">Jugar el pre-quiz</a><a class="btn" href="#b01">Empezar a estudiar</a><a class="btn ghost" style="color:#EEF2F8;border-color:#2A3B5C" href="../material/Apuntes_teoricos_Clase1.pdf">Apuntes en PDF</a></div>
</div>
<div class="grid">
<div class="tile"><h4>1 · Lee</h4><p>Cada tema empieza con <b>la idea en una frase</b>. Si solo tienes 5 minutos, lee esas frases.</p></div>
<div class="tile"><h4>2 · Practica</h4><p>Resuelve los ejercicios en papel <b>antes</b> de abrir la respuesta. Equivocarse aquí es gratis.</p></div>
<div class="tile"><h4>3 · Programa</h4><p>Cada tema dice qué parte del notebook abrir en Colab. Las tareas se autocorrigen con ✅ o ❌.</p></div>
<div class="tile"><h4>4 · Comprueba</h4><p>Al final juega el <a href="../quiz/index.html?final">quiz final</a>: te dice qué temas repasar.</p></div>
</div>
{box('ojo', 'Mapa de la semana', '''<p><b>Viernes:</b> 01 IA, ML y DL → 02 La neurona → 03 El perceptrón y XOR → 04 Pérdida y gradiente · notebook <b>NB01</b> y su Mini-reto 1.</p>
<p><b>Sábado:</b> 05 Capas → 06 Retropropagación → 07 Entrenar bien → 08 Keras · notebook <b>NB02</b> y su Mini-reto 2 → 09 Mini-proyecto con el <b>NB03</b>.</p>''')}
<p>Marca <b>«Ya lo entendí»</b> al final de cada tema: tu avance se guarda en este navegador y aparece en el índice.</p>
"""))

S.append(('pre', '0', 'Antes de empezar: las bases que vamos a usar', f"""
{idea('Para esta semana bastan cuatro herramientas: funciones, vectores, pendientes y probabilidades. Nada más.')}
<h3>Funciones: una máquina con perillas</h3>
<p>Una función recibe un número y devuelve otro. Si \\(f(x) = 2x + 1\\), entonces \\(f(3) = 7\\). Una neurona es una función con muchas perillas (los <b>pesos</b>) que el entrenamiento ajusta.</p>
<h3>Vectores y producto punto</h3>
<p>Un vector es una lista de números: los datos de un socio, por ejemplo \\(\\mathbf{{x}} = (0.8,\\ 0.5,\\ -1.0)\\). El <b>producto punto</b> multiplica parejas y suma:</p>
{formula(r'\mathbf{w}\cdot\mathbf{x} = w_1x_1 + w_2x_2 + w_3x_3', note='<p>En Python con NumPy: <code>w @ x</code>.</p>')}
<h3>Pendiente (derivada): si me muevo un poquito, ¿cuánto cambia?</h3>
<p>La pendiente de \\(L(w) = (w-3)^2\\) es \\(L'(w) = 2(w-3)\\). En \\(w = 0\\) vale \\(-6\\): la curva baja hacia la derecha. En \\(w = 3\\) vale 0: estamos en el fondo. Esa es la idea del descenso de gradiente.</p>
<h3>Probabilidades y logaritmos</h3>
<p>Una probabilidad va de 0 a 1 (0.8 = 80 %). El logaritmo \\(-\\log p\\) es pequeño cuando \\(p\\) está cerca de 1 y enorme cuando \\(p\\) está cerca de 0: \\(-\\log(0.99) \\approx 0.01\\), \\(-\\log(0.01) \\approx 4.6\\). Con eso se construye la pérdida para clasificar.</p>
<h3>Python mínimo</h3>
<pre><code>import numpy as np
x = np.array([0.8, 0.5, -1.0])   # a vector
w = np.array([1.2, 0.7, -2.0])
z = w @ x + (-0.5)               # dot product plus bias -> 2.81
np.mean([2, 4, 9])               # average -> 5.0
1 / (1 + np.exp(-z))             # sigmoid -> 0.943</code></pre>
<h3>Practica</h3>
{ex('Si \\(f(x) = 3x - 2\\), ¿cuánto vale \\(f(4)\\)?', '<p>\\(3\\cdot 4 - 2 = 10\\).</p>')}
{ex('Calcula \\(\\mathbf{w}\\cdot\\mathbf{x}\\) con \\(\\mathbf{w} = (2, -1)\\) y \\(\\mathbf{x} = (3, 4)\\).', '<p>\\(2\\cdot3 + (-1)\\cdot 4 = 6 - 4 = 2\\).</p>')}
{ex('¿Cuál es la pendiente de \\(L(w) = w^2\\) en \\(w = 2\\)? ¿Hacia dónde conviene moverse para bajar?', '<p>\\(L\'(w) = 2w\\), así que en \\(w=2\\) vale 4 (positiva): la curva sube hacia la derecha, conviene <b>bajar</b> \\(w\\).</p>')}
"""))

S.append(('b01', '01', 'IA, machine learning y deep learning', f"""
{idea('La IA es el campo; el machine learning aprende patrones de ejemplos; el deep learning lo hace con redes neuronales de muchas capas.')}
<h3>En palabras</h3>
<ul>
<li><b>Inteligencia artificial:</b> máquinas que hacen tareas que asociamos con inteligencia, con reglas escritas o aprendiendo.</li>
<li><b>Machine learning:</b> en vez de escribir reglas, le damos <b>ejemplos con su respuesta</b> y el algoritmo encuentra las reglas.</li>
<li><b>Deep learning:</b> machine learning con <b>redes neuronales de muchas capas</b> que descubren solas qué mirar en los datos.</li>
</ul>
<p>Todo deep learning es machine learning, y todo machine learning es IA, pero no al revés: «si el monto supera 1 000 dólares, rechazar» es IA en sentido amplio, pero no aprende nada.</p>
<h3>En fórmula</h3>
<p>Aprender es buscar una función con perillas \\(\\theta\\) (los parámetros) que, dados los datos \\(\\mathbf{{x}}\\), acierte la respuesta \\(y\\):</p>
{formula(r'\text{dados ejemplos } (\mathbf{x}_i, y_i),\ \text{buscar } f_\theta \text{ tal que } f_\theta(\mathbf{x}_i) \approx y_i',
         [(r'\mathbf{x}', 'los datos de un ejemplo (la ficha del socio)', B), (r'y', 'la respuesta correcta (pagó o no)', T), (r'\theta', 'las perillas que se aprenden', A)])}
<h3>Tres formas de aprender</h3>
<table><tr><th>Tipo</th><th>Qué recibe</th><th>Ejemplo</th></tr>
<tr><td><b>Supervisado</b> (esta semana)</td><td>datos con la respuesta correcta</td><td>predecir si un socio cae en mora</td></tr>
<tr><td>No supervisado</td><td>datos sin respuesta</td><td>agrupar clientes por hábitos de compra</td></tr>
<tr><td>Por refuerzo</td><td>premios y castigos por sus acciones</td><td>un agente que aprende a jugar</td></tr></table>
{box('analogia', 'Analogía', '<p>El comerciante del mercado que con los años aprende a quién fiarle: nadie le dio un manual; aprendió de muchos casos (quién pagó y quién no).</p>')}
<h3>¿Por qué ahora?</h3>
<p>Las redes existen desde 1958, pero despegaron después de 2012 por tres cosas juntas: muchos más <b>datos</b>, procesadores gráficos (<b>GPU</b>) que hacen millones de multiplicaciones en paralelo y <b>mejores técnicas</b> de entrenamiento (ReLU, buenas inicializaciones, Adam).</p>
<h3>¿Cuándo conviene el deep learning?</h3>
<p>Brilla con <b>imágenes, texto, audio y series largas</b>, donde es difícil describir a mano qué mirar. En <b>datos de tabla</b> (como el mini-proyecto), una regresión logística o un modelo de árboles a veces lo iguala: por eso siempre se compara con una <b>línea base</b>.</p>
<h3>Practica</h3>
{ex('Un filtro marca como spam todo correo que diga «GRATIS». ¿Es machine learning?', '<p>No: es una regla escrita por una persona. Sería ML si aprendiera de miles de correos marcados como spam o no spam.</p>')}
{ex('Quieres agrupar a los socios en perfiles parecidos sin tener una etiqueta. ¿Qué tipo de aprendizaje es?', '<p>No supervisado: no hay respuesta correcta que imitar.</p>')}
"""))

S.append(('b02', '02', 'La neurona artificial', f"""
{idea('Una neurona multiplica cada dato por su peso, suma todo con un sesgo y decide con una función de activación.')}
{fig(svg_neuron(), 'Entradas × pesos → suma con sesgo → activación → salida.')}
<h3>En fórmula</h3>
{formula(r'z = w_1x_1 + w_2x_2 + w_3x_3 + b = \mathbf{w}\cdot\mathbf{x} + b \qquad a = \varphi(z)',
         [('z', 'el puntaje total', I), (r'w_i x_i', 'cada dato por su importancia', B), ('b', 'el sesgo: qué tan exigente es', A), (r'\varphi', 'la activación: convierte el puntaje en salida', T)])}
<h3>Ejemplo con números: el comité de crédito</h3>
<table><tr><th>Dato</th><th>Valor \\(x\\)</th><th>Peso \\(w\\)</th><th>Aporte \\(w\\cdot x\\)</th></tr>
<tr><td>Ingreso</td><td>0.8</td><td>1.2</td><td>+0.96</td></tr>
<tr><td>Antigüedad</td><td>0.5</td><td>0.7</td><td>+0.35</td></tr>
<tr><td>Atrasos (menos que el promedio)</td><td>−1.0</td><td>−2.0</td><td>+2.00</td></tr>
<tr><td>Sesgo \\(b\\)</td><td colspan="2"></td><td>−0.50</td></tr>
<tr><th>Puntaje \\(z\\)</th><th colspan="2"></th><th>2.81</th></tr></table>
<p>Con escalón: \\(z \\ge 0\\) → <b>aprueba</b>. Con sigmoide: \\(\\sigma(2.81) \\approx 0.94\\) → <b>94 % de probabilidad de pago</b>. Fíjate: un peso negativo por un dato negativo da un aporte positivo.</p>
{box('analogia', 'Analogía: el comité de crédito', '<p>Mira la ficha (entradas), confía más en unos datos que en otros (pesos), aplica su nivel de exigencia (sesgo) y decide (activación). <b>Aprender</b> = ajustar cuánto confía en cada dato después de ver quién pagó.</p>')}
<h3>Las tres activaciones de la semana</h3>
{fig(svg_acts(), 'De izquierda a derecha: interruptor, regulador de intensidad y válvula.')}
<table><tr><th>Activación</th><th>Fórmula</th><th>Qué hace</th><th>Dónde se usa</th></tr>
<tr><td>Escalón</td><td>\\(1\\) si \\(z\\ge0\\); si no, \\(0\\)</td><td>sí o no</td><td>perceptrón clásico</td></tr>
<tr><td>Sigmoide</td><td>\\(\\sigma(z) = \\dfrac{{1}}{{1+e^{{-z}}}}\\)</td><td>número entre 0 y 1: una probabilidad</td><td>salida «¿paga o no?»</td></tr>
<tr><td>ReLU</td><td>\\(\\max(0, z)\\)</td><td>apaga lo negativo, deja pasar lo positivo</td><td>capas ocultas</td></tr></table>
<p><b>¿Para qué sirve?</b> Sin activación, apilar neuronas sería sumar sumas: el resultado seguiría siendo una recta. La activación «dobla» el espacio.</p>
<h3>Una neurona dibuja una línea</h3>
<p>Con dos datos, cada socio es un punto del plano. La neurona aprueba de un lado y rechaza del otro; la frontera es donde \\(z = 0\\):</p>
{formula(r'w_1 x_1 + w_2 x_2 + b = 0', note='<p>Los <b>pesos</b> giran la línea; el <b>sesgo</b> la mueve. Entrenar es buscar la mejor posición.</p>')}
{box('error', 'Errores comunes', '<ul><li>Olvidar el sesgo \\(b\\) al calcular \\(z\\).</li><li>Confundir \\(z\\) (puntaje) con la salida \\(a\\) (decisión o probabilidad).</li><li>Pensar que un peso negativo «está mal»: solo dice que ese dato resta.</li></ul>')}
<h3>Practica</h3>
{ex('Socio B: ingreso 0.2, antigüedad −0.5, atrasos 1.5, con los mismos pesos y sesgo. ¿Cuánto vale \\(z\\)? ¿Qué decide?', '<p>\\(z = 1.2\\cdot0.2 + 0.7\\cdot(-0.5) + (-2)\\cdot1.5 - 0.5 = 0.24 - 0.35 - 3.0 - 0.5 = -3.61\\). Rechaza; con sigmoide, \\(\\approx 2.6\\,\\%\\) de probabilidad de pago.</p>')}
{ex('¿Cuánto vale \\(\\sigma(0)\\)? ¿Qué significa para el socio?', '<p>0.5: la neurona duda. El socio está exactamente sobre la línea frontera.</p>')}
{ex('Si el comité se vuelve más exigente, ¿qué número cambia y hacia dónde?', '<p>El sesgo \\(b\\) baja (más negativo): hace falta más puntaje para aprobar.</p>')}
{colab(NB1, '<b>NB01</b>, secciones 1 y 2 · Tareas T1 (programa tu neurona) y T2 (de puntaje a decisión).')}
"""))

S.append(('b03', '03', 'Cómo aprende una neurona: el perceptrón y XOR', f"""
{idea('El perceptrón aprende corrigiéndose solo cuando se equivoca: empuja los pesos hacia la respuesta correcta.')}
<h3>El ciclo de todo aprendizaje</h3>
<p><b>Predecir → comparar → corregir → repetir.</b> Como ajustar la sal del locro: pruebas, notas que falta, echas una pizca, vuelves a probar. Cada vuelta completa por todos los datos se llama <b>época</b>.</p>
<h3>En fórmula: la regla del perceptrón</h3>
<p>Con etiquetas \\(y = +1\\) (aprobar) y \\(y = -1\\) (rechazar), cuando se equivoca:</p>
{formula(r'\mathbf{w} \leftarrow \mathbf{w} + \eta\, y\, \mathbf{x} \qquad b \leftarrow b + \eta\, y',
         [(r'\mathbf{w}', 'los pesos actuales', I), (r'\eta', 'tamaño de la corrección (aquí 1)', A), ('y', 'la respuesta correcta: +1 o −1', T), (r'\mathbf{x}', 'el dato que clasificó mal', B)])}
<h3>Ejemplo con números</h3>
<p>Pesos \\(\\mathbf{{w}} = (0.2, -0.5)\\), \\(b = 0\\). Un socio \\(\\mathbf{{x}} = (1, 1)\\) que debía aprobarse (\\(y=+1\\)):</p>
<ol><li>Antes: \\(z = 0.2 - 0.5 + 0 = -0.30\\) → rechaza. <b>Error.</b></li>
<li>Corrige: \\(\\mathbf{{w}} = (0.2+1,\\ -0.5+1) = (1.2,\\ 0.5)\\), \\(b = 0 + 1 = 1\\).</li>
<li>Después: \\(z = 1.2 + 0.5 + 1 = +2.70\\) → aprueba. <b>Acierta.</b></li></ol>
<h3>La garantía y el límite</h3>
<p><b>Si una línea puede separar los datos</b>, el perceptrón la encuentra en un número finito de correcciones (Novikoff, 1962). Pero <b>XOR</b>, la luz de la escalera (se enciende si los interruptores están en posiciones distintas), no se puede separar con una sola línea: el perceptrón comete 4 errores en todas las épocas.</p>
<table><tr><th>\\(x_1\\)</th><th>\\(x_2\\)</th><th>XOR (luz)</th></tr><tr><td>0</td><td>0</td><td>apagada</td></tr><tr><td>0</td><td>1</td><td>encendida</td></tr><tr><td>1</td><td>0</td><td>encendida</td></tr><tr><td>1</td><td>1</td><td>apagada</td></tr></table>
<p>En el negocio, XOR aparece cuando el efecto de una variable <b>depende de otra</b> (por ejemplo, el garante ayuda solo si la cuota es baja). La solución llega el sábado: <b>más de una neurona</b>.</p>
{box('curioso', 'Para curiosos', '<p>El número de correcciones está acotado por \\((R/\\gamma)^2\\): \\(R\\) es qué tan lejos están los datos del origen y \\(\\gamma\\) el <b>margen</b>, el ancho del «pasillo» vacío entre las clases. Pasillo ancho, aprendizaje rápido.</p>')}
<h3>Practica</h3>
{ex('Con \\(\\mathbf{w} = (1.2, 0.5)\\), \\(b = 1\\), llega \\(\\mathbf{x} = (1, 0.5)\\) que NO pagó (\\(y = -1\\)). ¿Se equivoca? Aplica una corrección.', '<p>\\(z = 1.2 + 0.25 + 1 = 2.45\\) → aprueba: error. Corrige: \\(\\mathbf{w} = (1.2-1,\\ 0.5-0.5) = (0.2, 0)\\), \\(b = 0\\). Nuevo \\(z = 0.2\\): todavía aprueba. Hacen falta más vueltas.</p>')}
{ex('¿La compuerta AND (vale 1 solo si ambos valen 1) se puede aprender con un perceptrón?', '<p>Sí: una línea deja (1,1) de un lado y los otros tres del otro. Por ejemplo \\(x_1 + x_2 - 1.5 = 0\\).</p>')}
{colab(NB1, '<b>NB01</b>, secciones 3 a 5 · Tareas T3 (corrige un error al revés), T4 (compuerta AND) y T5 (¿por qué falla XOR?).')}
"""))

S.append(('b04', '04', 'Medir el error y mejorar: pérdida y descenso de gradiente', f"""
{idea('La pérdida mide qué tan mal vamos con un solo número; el descenso de gradiente mueve los pesos cuesta abajo para bajarla.')}
<h3>La pérdida: la nota al revés</h3>
<p>0 es perfecto; mientras más alta, peor. Entrenar = bajarla.</p>
{formula(r'\text{MSE} = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat y_i)^2', [('y', 'valor real', T), (r'\hat y', 'lo que predijo el modelo', B), ('N', 'número de ejemplos', I)], '<p>Para predecir <b>números</b> (precios). Elevar al cuadrado castiga mucho los errores grandes.</p>')}
<p><b>Ejemplo:</b> casas en Quito, reales (120, 95, 150, 80) y predichas (110, 100, 170, 82) miles de USD. Errores 10, −5, −20, −2 → cuadrados 100, 25, 400, 4 → MSE = 529 ÷ 4 = <b>132.25</b>.</p>
{formula(r'\text{BCE} = -\big[\,y\log\hat y + (1-y)\log(1-\hat y)\,\big]', [('y', '1 si pagó, 0 si no', T), (r'\hat y', 'probabilidad que dio el modelo', B)], '<p>Para clasificar <b>sí/no</b>. Si pagó queda \\(-\\log\\hat y\\); si no pagó, \\(-\\log(1-\\hat y)\\).</p>')}
<table><tr><th>El socio pagó; el modelo dijo…</th><th>99 %</th><th>90 %</th><th>50 %</th><th>10 %</th><th>1 %</th></tr>
<tr><td>Pérdida BCE</td><td>0.01</td><td>0.11</td><td>0.69</td><td>2.30</td><td>4.61</td></tr></table>
{box('analogia', 'Analogía: el pronóstico del clima', '<p>Decir «99 % sin lluvia» el día de un aguacero en Quito te deja muy mal; decir 50 %, no tanto. La BCE castiga la <b>falsa seguridad</b>.</p>')}
<h3>Descenso de gradiente: bajar el Cotopaxi con neblina</h3>
<p>No ves el valle, pero con el pie sientes hacia dónde baja el terreno (la <b>pendiente</b>) y das un paso hacia allá.</p>
{formula(r'w \leftarrow w - \eta \cdot \frac{\partial L}{\partial w}', [('w', 'el peso', I), (r'\eta', 'largo del paso (tasa de aprendizaje)', A), (r'\partial L/\partial w', 'la pendiente: hacia dónde sube la pérdida', B)], '<p>El <b>signo menos</b> es la clave: la pendiente apunta cuesta arriba y nosotros vamos al revés.</p>')}
{fig(svg_gd(), 'Pérdida \\((w-3)^2\\), paso η = 0.1: w = 0 → 0.6 → 1.08 → 1.464 → 1.771…')}
<table><tr><th>Paso</th><th>w</th><th>pendiente 2(w−3)</th><th>pérdida</th></tr>
<tr><td>0</td><td>0</td><td>−6</td><td>9.00</td></tr><tr><td>1</td><td>0.6</td><td>−4.8</td><td>5.76</td></tr><tr><td>2</td><td>1.08</td><td>−3.84</td><td>3.69</td></tr><tr><td>3</td><td>1.464</td><td>−3.07</td><td>2.36</td></tr><tr><td>4</td><td>1.771</td><td>−2.46</td><td>1.51</td></tr></table>
<h3>El tamaño del paso η</h3>
<ul><li><b>Muy corto</b> (η = 0.02): llega, pero tarda una eternidad.</li><li><b>Bien elegido</b> (η = 0.4): llega en pocos pasos.</li><li><b>Muy largo</b> (η = 1.02): se pasa del fondo y rebota cada vez más lejos: <b>diverge</b>.</li></ul>
{box('error', 'Errores comunes', '<ul><li>Usar \\(-\\log\\hat y\\) cuando el socio NO pagó: ahí va \\(-\\log(1-\\hat y)\\).</li><li>Olvidar el signo menos y subir la montaña.</li><li>Si la pérdida sube o aparece <code>NaN</code>: casi siempre η es demasiado grande.</li></ul>')}
<h3>Practica</h3>
{ex('El modelo dijo 0.9 y el socio NO pagó. ¿Cuánto vale la BCE?', '<p>\\(-\\log(1 - 0.9) = -\\log(0.1) \\approx 2.30\\).</p>')}
{ex('Con \\(L(w) = (w-3)^2\\), \\(\\eta = 0.1\\) y \\(w = 1\\): ¿cuánto vale \\(w\\) después de un paso?', '<p>Pendiente \\(2(1-3) = -4\\). Nuevo \\(w = 1 - 0.1\\cdot(-4) = 1.4\\).</p>')}
{ex('Con \\(L(w) = (w+2)^2\\), ¿dónde está el mínimo y hacia dónde se mueve \\(w\\) si empieza en 5?', '<p>En \\(w = -2\\). Desde 5 la pendiente es positiva, así que \\(w\\) baja hacia −2.</p>')}
{colab(NB1, '<b>NB01</b>, secciones 6 a 8 · Tareas T6 (programa MSE y BCE), T7 (baja otra montaña), T8 (¿cuáles convergen?) y el <b>Mini-reto 1</b>: tu propio comité de crédito.')}
"""))

S.append(('b05', '05', 'De una neurona a una red', f"""
{idea('Una red son neuronas organizadas en capas: cada capa arma pistas más elaboradas a partir de la anterior.')}
{fig(svg_mlp(), 'Entrada (los datos) → capa oculta (inventa pistas) → salida (decide).')}
<h3>En fórmula: cada capa</h3>
{formula(r'\mathbf{a}^{(l)} = \varphi\big(W^{(l)}\,\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}\big), \qquad \mathbf{a}^{(0)} = \mathbf{x}',
         [(r'W^{(l)}', 'pesos de la capa: cada fila es una neurona', B), (r'\mathbf{b}^{(l)}', 'un sesgo por neurona', A), (r'\mathbf{a}^{(l)}', 'lo que sale de la capa l', T)])}
{box('analogia', 'Analogía: las agencias de la cooperativa', '<p>Cada agencia (neurona oculta) resume una pista: «¿tiene capacidad de pago?», «¿es cumplido?». El comité central (salida) decide con esas pistas, no con los datos crudos.</p>')}
<h3>Dos neuronas resuelven XOR</h3>
<p>Una neurona oculta aprende «¿al menos un interruptor arriba?»; otra, «¿los dos arriba?». La salida enciende la luz si la primera dice sí y la segunda dice no. Dos líneas combinadas hacen lo que una sola no podía.</p>
<h3>¿Cuántos números aprende una red?</h3>
{formula(r'\text{parámetros de una capa} = n_{\text{entradas}} \times n_{\text{neuronas}} + n_{\text{neuronas}}')}
<table><tr><th>Red</th><th>Cuenta</th><th>Total</th></tr>
<tr><td>2 → 16 → 16 → 1 (las lunas)</td><td>(2·16+16) + (16·16+16) + (16·1+1) = 48 + 272 + 17</td><td><b>337</b></td></tr>
<tr><td>28 → 32 → 16 → 1 (mini-proyecto)</td><td>928 + 528 + 17</td><td><b>1 473</b></td></tr></table>
{box('curioso', 'Para curiosos: aproximación universal', '<p>Con suficientes neuronas, una sola capa oculta puede aproximar casi cualquier función continua (Cybenko, 1989). En la práctica, varias capas lo logran con muchas menos neuronas: eso es el «deep».</p>')}
<h3>Practica</h3>
{ex('¿Cuántos parámetros tiene una red 3 → 4 → 1?', '<p>\\((3\\cdot4 + 4) + (4\\cdot1 + 1) = 16 + 5 = 21\\).</p>')}
{ex('¿Por qué una red sin funciones de activación, aunque tenga 50 capas, no puede separar XOR?', '<p>Porque una composición de funciones lineales sigue siendo lineal: equivale a una sola neurona, una sola línea.</p>')}
{colab(NB2, '<b>NB02</b>, Parte E · XOR resuelto y las «lunas» · Tarea TE (cuenta parámetros).')}
"""))

S.append(('b06', '06', 'Retropropagación: repartir la culpa', f"""
{idea('Hacia adelante la red predice; hacia atrás reparte la culpa del error entre todos sus pesos; luego cada peso da un paso cuesta abajo.')}
{fig(svg_back(), 'La información viaja hacia adelante; la culpa, hacia atrás.')}
<h3>Ejemplo con números: una red 2 → 2 → 1</h3>
<p>Socio con antigüedad 1.0 y carga de cuota 0.5; <b>sí pagó</b> (\\(y = 1\\)). Pesos ocultos (0.5, −0.3) y (0.2, 0.8), sesgos 0.1 y −0.1; salida (0.7, −0.4), sesgo 0.05; todas con sigmoide.</p>
<ol><li><b>Adelante:</b> capa oculta \\(\\mathbf{{a}} = (0.61,\\ 0.62)\\); salida \\(\\hat y = 0.56\\). Pérdida \\(-\\log 0.56 = 0.59\\).</li>
<li><b>Culpa de la salida:</b> \\(\\delta = \\hat y - y = -0.44\\) (se quedó corta).</li>
<li><b>Culpa de cada peso de salida:</b> \\(\\delta\\) × lo que entró: \\(-0.44 \\times 0.61 = -0.27\\).</li>
<li><b>Culpa de la capa oculta:</b> peso × culpa × pendiente de la sigmoide: \\(-0.07\\) y \\(+0.04\\).</li>
<li><b>Paso</b> con η = 0.5: la predicción sube de 56 % a <b>65 %</b> y la pérdida baja de 0.59 a <b>0.42</b>.</li></ol>
<h3>Las cuatro reglas</h3>
<table><tr><th>#</th><th>En palabras</th><th>En símbolos</th></tr>
<tr><td>1</td><td>Culpa de la salida = predicción − realidad</td><td>\\(\\delta^{{(L)}} = \\hat y - y\\)</td></tr>
<tr><td>2</td><td>Culpa de una neurona oculta = culpa que le llega por sus pesos × su pendiente</td><td>\\(\\delta^{{(l)}} = (W^{{(l+1)}})^\\top \\delta^{{(l+1)}} \\odot \\varphi'(z^{{(l)}})\\)</td></tr>
<tr><td>3</td><td>Culpa de un peso = culpa de su neurona × lo que entra por ese cable</td><td>\\(\\partial L/\\partial w = \\delta \\cdot a_{{\\text{{entrada}}}}\\)</td></tr>
<tr><td>4</td><td>Actualizar: peso − η × culpa, y repetir</td><td>\\(w \\leftarrow w - \\eta\\, \\partial L/\\partial w\\)</td></tr></table>
<h3>La regla de la cadena: engranajes</h3>
<p>Si A mueve a B tres veces más rápido y B mueve a C seis veces más rápido, A mueve a C <b>18</b> veces más rápido: los efectos se <b>multiplican</b>.</p>
{formula(r'z = (3x)^2:\quad \frac{dz}{dx} = \underbrace{2(3x)}_{\text{por fuera}} \cdot \underbrace{3}_{\text{por dentro}} = 18 \text{ en } x = 1')}
{box('analogia', 'Analogía: la cadena del cacao', '<p>El cliente dice «¡salió amargo!» (el error se descubre al final). La chocolatería revisa cuánto influyó cada proceso y pasa la culpa hacia el tostado y la cosecha, según cuánto influyeron.</p>')}
{box('ojo', 'TensorFlow lo hace solo', '<p><code>tf.GradientTape</code> «graba» la pasada hacia adelante y la recorre al revés aplicando estas reglas. Nadie hace retropropagación a mano en la vida real; entenderla sirve para <b>depurar</b>.</p>')}
<h3>Practica</h3>
{ex('Otro socio NO pagó (\\(y = 0\\)) y la red dijo \\(\\hat y = 0.53\\). ¿Cuál es la culpa de la salida? ¿Subirá o bajará la predicción tras el paso?', '<p>\\(\\delta = 0.53 - 0 = 0.53\\) (positiva): los pesos se mueven para <b>bajar</b> la predicción. En el NB02 baja a ≈ 0.41.</p>')}
{ex('Una neurona ReLU tuvo \\(z < 0\\). ¿Qué culpa reciben sus pesos con ese ejemplo?', '<p>Cero: la pendiente de ReLU para \\(z<0\\) es 0. Si le pasa con todos los ejemplos, es una «neurona muerta».</p>')}
{ex('¿Cuánto vale la derivada de \\((2x+1)^2\\) en \\(x = 1\\)?', '<p>Por fuera \\(2(2x+1) = 6\\); por dentro 2. Total \\(6\\cdot 2 = 12\\).</p>')}
{colab(NB2, '<b>NB02</b>, Partes A a D · Tareas TA (otro socio hacia adelante), TB (la culpa de la salida), TC (un paso) y TD (los engranajes en TensorFlow).')}
"""))

S.append(('b07', '07', 'Entrenar bien: trampas, lotes y optimizadores', f"""
{idea('Entrenar bien es evitar tres trampas, aprender por lotes y elegir un buen optimizador: Adam es la opción segura para empezar.')}
<h3>Tres trampas y su remedio</h3>
<table><tr><th>Trampa</th><th>Síntoma</th><th>Remedio</th></tr>
<tr><td><b>La señal se apaga</b> (teléfono dañado)</td><td>las primeras capas casi no aprenden</td><td>ReLU en capas ocultas</td></tr>
<tr><td><b>Pesos iniciales malos</b> (clones)</td><td>la red no mejora o explota desde el inicio</td><td>inicialización aleatoria escalada: <code>he_normal</code> con ReLU</td></tr>
<tr><td><b>Paso η equivocado</b> (medio salero)</td><td>la pérdida sube, salta o da NaN</td><td>Adam con learning_rate 0.001; si falla, bajarlo</td></tr></table>
{box('curioso', 'Para curiosos: por qué se apaga la señal', '<p>La pendiente máxima de la sigmoide es 0.25. Al retropropagar por 10 capas, la culpa se multiplica por números ≤ 0.25: \\(0.25^{10} \\approx 10^{-6}\\). ReLU tiene pendiente 1 cuando está activa.</p>')}
<h3>Aprender por lotes: censo o encuesta</h3>
<p>No usamos los 4 800 socios en cada paso: tomamos un <b>lote</b> de 32 al azar, promediamos su culpa y damos un paso. Como el INEC, que no hace un censo cada mes: una encuesta bien hecha basta.</p>
{formula(r'\text{pasos por época} = \frac{N}{\text{batch\_size}} = \frac{4800}{32} = 150')}
<h3>Tres formas de bajar la montaña</h3>
<table><tr><th>Optimizador</th><th>Idea</th><th>Analogía</th></tr>
<tr><td>SGD</td><td>pasos fijos en la dirección de la pendiente</td><td>el caminante</td></tr>
<tr><td>Momentum</td><td>acumula impulso: acelera en las rectas, zigzaguea menos</td><td>la bicicleta en bajada</td></tr>
<tr><td>Adam</td><td>ajusta el paso de cada peso por separado</td><td>el guía con experiencia</td></tr></table>
{box('ojo', 'La receta para arrancar', '<ol><li>Escala los datos (<code>StandardScaler</code>, ajustado solo con entrenamiento).</li><li>Capas ocultas ReLU con <code>he_normal</code>; empieza con 1 o 2.</li><li>Salida según la pregunta: sí/no → 1 neurona sigmoide + BCE.</li><li>Adam con learning_rate 0.001.</li><li>batch_size 32; mira las curvas de entrenamiento y validación.</li><li>Si la pérdida sube o da NaN: baja el learning_rate.</li></ol>')}
<h3>Practica</h3>
{ex('Con 4 800 ejemplos y batch_size = 64, ¿cuántos pasos tiene una época? ¿Y 30 épocas?', '<p>4 800 ÷ 64 = 75 pasos por época; 30 épocas = 2 250 pasos.</p>')}
{ex('¿Por qué no conviene iniciar todos los pesos en cero?', '<p>Todas las neuronas de la capa calcularían lo mismo y recibirían la misma culpa: quedarían clones para siempre.</p>')}
{colab(NB2, '<b>NB02</b>, Parte G · Tarea TG (lee las curvas de los tres optimizadores).')}
"""))

S.append(('b08', '08', 'Keras en tres pasos', f"""
{idea('Construir, compilar, entrenar: Keras hace por ti el ciclo adelante → atrás → actualizar, lote a lote y época a época.')}
<pre><code>import keras

# 1) BUILD: stack layers
model = keras.Sequential([
    keras.Input(shape=(2,)),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid"),   # probability
])
model.summary()                                    # 337 parameters

# 2) COMPILE: how it learns
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
              loss="binary_crossentropy", metrics=["accuracy"])

# 3) TRAIN: repeat the cycle
history = model.fit(X_tr, y_tr, validation_data=(X_va, y_va),
                    epochs=60, batch_size=32)</code></pre>
<table><tr><th>Paso</th><th>Qué decides</th><th>Lo que ya sabes</th></tr>
<tr><td>Construir</td><td>capas, neuronas y activaciones</td><td>bloques 02 y 05</td></tr>
<tr><td>Compilar</td><td>optimizador, pérdida y métrica</td><td>bloques 04 y 07</td></tr>
<tr><td>Entrenar</td><td>épocas y tamaño del lote</td><td>bloques 06 y 07</td></tr></table>
{box('ojo', 'Lee las curvas', '<p>Si la pérdida de <b>entrenamiento</b> baja y la de <b>validación</b> también, vas bien. Si la de validación empieza a subir mientras la de entrenamiento sigue bajando, la red está memorizando (sobreajuste): lo veremos en la semana 3.</p>')}
<h3>Practica</h3>
{ex('Escribe el modelo del mini-proyecto: 28 entradas, capas de 32 y 16 con ReLU y una salida sigmoide. ¿Cuántos parámetros debe mostrar <code>summary()</code>?', '<pre><code>model = keras.Sequential([keras.Input(shape=(28,)),\n    keras.layers.Dense(32, activation="relu"),\n    keras.layers.Dense(16, activation="relu"),\n    keras.layers.Dense(1, activation="sigmoid")])</code></pre><p>928 + 528 + 17 = 1 473 parámetros.</p>')}
{ex('Una red sin capas ocultas logra 49 % en los círculos del NB02. ¿Por qué?', '<p>Sin capas ocultas es una sola neurona: traza una línea, y ninguna línea separa un círculo de su anillo. Es como adivinar.</p>')}
{colab(NB2, '<b>NB02</b>, Parte F · <b>Mini-reto 2</b>: entrena tu red para los círculos y supera el 90 %.')}
"""))

S.append(('b09', '09', 'Mini-proyecto: anticipar la mora', f"""
{idea('Con datos desbalanceados, la exactitud engaña: medimos qué tan bien ordena el riesgo (ROC-AUC) y cuántos morosos detecta el modelo.')}
<h3>El caso</h3>
<p>La Cooperativa «Valle Andino» (ficticia) quiere anticipar qué socios pueden caer en <b>mora de más de 30 días</b> para acompañarlos a tiempo. Datos: 8 000 socios, 13 variables y 12.7 % de mora (100 % sintéticos). Si tu grupo tiene los datos de su proyecto de titulación, puede usarlos.</p>
<h3>La ruta del NB03</h3>
<ol><li>Cargar y explorar los datos.</li><li><b>Partir sin trampa:</b> entrenamiento 4 800 · validación 1 600 · prueba 1 600. El escalador se ajusta <b>solo</b> con entrenamiento.</li><li>Líneas base: «siempre no mora» y regresión logística.</li><li>Perceptrón desde cero · MLP con retropropagación desde cero (gradient check) · el mismo MLP en Keras.</li><li>Experimentos de optimización (optimizador × learning rate × batch).</li><li>Evaluación final con prueba, <b>una sola vez</b>, y elección del umbral con validación.</li></ol>
<h3>Métricas en palabras sencillas</h3>
<table><tr><th>Métrica</th><th>Pregunta que responde</th></tr>
<tr><td>Exactitud (accuracy)</td><td>¿qué porcentaje acertó en total? Engaña: decir siempre «no mora» ya da 87 %.</td></tr>
<tr><td>ROC-AUC</td><td>si tomo un moroso y un cumplido al azar, ¿con qué probabilidad el modelo le da más riesgo al moroso? 0.5 = moneda al aire, 1 = perfecto.</td></tr>
<tr><td>Recall (detecta)</td><td>de los morosos reales, ¿qué porcentaje encontró?</td></tr>
<tr><td>Precisión</td><td>de los que marcó como riesgo, ¿qué porcentaje era moroso de verdad?</td></tr></table>
<table><tr><th>Modelo (validación)</th><th>Exactitud</th><th>ROC-AUC</th></tr>
<tr><td>Siempre «no mora»</td><td>87 %</td><td>0.50</td></tr><tr><td>Regresión logística</td><td>89 %</td><td>0.85</td></tr><tr><td>Perceptrón</td><td>89 %</td><td>0.84</td></tr><tr><td>Red en Keras</td><td>90 %</td><td>0.87</td></tr></table>
{box('ojo', 'Qué entregan (grupal, 70 puntos)', '<p>El notebook completo que corra en Colab y un informe PDF de 4 a 6 páginas que <b>justifique</b> cada decisión con lo visto en clase. Cierre: martes 27 de octubre (hora exacta en Canvas).</p>')}
{box('error', 'Errores comunes', '<ul><li>Ajustar el escalador con todos los datos (fuga de información).</li><li>Mirar la prueba para decidir: se usa una sola vez, al final.</li><li>Reportar solo la exactitud.</li><li>Formas que no coinciden en Keras: vector <code>(N,)</code> frente a <code>(N, 1)</code>.</li></ul>')}
<h3>Practica</h3>
{ex('En validación hay 1 600 socios y 203 morosos. ¿Qué exactitud logra «siempre no mora»?', '<p>(1 600 − 203) ÷ 1 600 ≈ 87.3 %, con recall 0 %: no encuentra a ningún moroso.</p>')}
{ex('¿Por qué el umbral de decisión se elige con validación y no con prueba?', '<p>Porque elegir algo mirando la prueba la convierte en parte del entrenamiento: el resultado final dejaría de ser una medida honesta.</p>')}
{colab(NB3, '<b>NB03</b> · mini-proyecto en grupo. Los datos se descargan solos desde GitHub; cada sección tiene un <b>Checkpoint</b> con el resultado esperado.')}
"""))

FORMULAS = r"""
<table>
<tr><th>Qué</th><th>Fórmula</th><th>En palabras</th></tr>
<tr><td>Neurona</td><td>\(z = \mathbf{w}\cdot\mathbf{x} + b,\ a = \varphi(z)\)</td><td>multiplica, suma y decide</td></tr>
<tr><td>Sigmoide</td><td>\(\sigma(z) = 1/(1+e^{-z})\)</td><td>puntaje → probabilidad</td></tr>
<tr><td>ReLU</td><td>\(\max(0, z)\)</td><td>apaga lo negativo</td></tr>
<tr><td>Frontera</td><td>\(w_1x_1 + w_2x_2 + b = 0\)</td><td>la línea donde duda</td></tr>
<tr><td>Perceptrón</td><td>\(\mathbf{w} \leftarrow \mathbf{w} + \eta\,y\,\mathbf{x}\)</td><td>corrige solo si se equivoca</td></tr>
<tr><td>MSE</td><td>\(\frac{1}{N}\sum (y-\hat y)^2\)</td><td>promedio de errores al cuadrado</td></tr>
<tr><td>BCE</td><td>\(-[y\log\hat y + (1-y)\log(1-\hat y)]\)</td><td>castiga la falsa seguridad</td></tr>
<tr><td>Gradiente</td><td>\(w \leftarrow w - \eta\,\partial L/\partial w\)</td><td>un paso cuesta abajo</td></tr>
<tr><td>Capa</td><td>\(\mathbf{a}^{(l)} = \varphi(W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)})\)</td><td>muchas neuronas a la vez</td></tr>
<tr><td>Culpa de salida</td><td>\(\delta = \hat y - y\)</td><td>predicción − realidad</td></tr>
<tr><td>Parámetros</td><td>\(n_{in}\cdot n_{out} + n_{out}\)</td><td>pesos + sesgos por capa</td></tr>
<tr><td>Pasos por época</td><td>\(N / \text{batch}\)</td><td>lotes por vuelta</td></tr>
</table>"""
S.append(('formulas', 'Σ', 'Fórmulas de bolsillo', FORMULAS))

GLOS = [
    ("Activación", "Función que convierte el puntaje z en la salida de la neurona (escalón, sigmoide, ReLU)."),
    ("Adam", "Optimizador que ajusta el tamaño del paso de cada peso por separado; buena opción por defecto."),
    ("Batch (lote)", "Grupo de ejemplos con el que se calcula un paso de aprendizaje; batch_size es su tamaño."),
    ("BCE (entropía cruzada binaria)", "Pérdida para clasificar sí/no; castiga mucho estar seguro y equivocado."),
    ("Capa oculta", "Capa entre la entrada y la salida; construye pistas a partir de los datos."),
    ("Deep learning", "Machine learning con redes neuronales de muchas capas."),
    ("Descenso de gradiente", "Método para bajar la pérdida dando pasos en contra de la pendiente."),
    ("Divergir", "Cuando la pérdida crece en vez de bajar, típicamente por un η demasiado grande."),
    ("Época", "Una vuelta completa por todos los datos de entrenamiento."),
    ("Exactitud (accuracy)", "Porcentaje de aciertos; engaña con clases desbalanceadas."),
    ("Forward", "Pasada hacia adelante: de los datos a la predicción."),
    ("Fuga de información", "Usar, sin querer, información de validación o prueba al entrenar."),
    ("Gradient check", "Verificación numérica de que los gradientes calculados a mano son correctos."),
    ("Gradiente", "La lista de pendientes de la pérdida respecto a cada peso."),
    ("Keras", "Librería de Python para construir y entrenar redes en pocas líneas (sobre TensorFlow)."),
    ("Learning rate (η)", "Tamaño del paso en el descenso de gradiente."),
    ("Línea base", "Modelo sencillo con el que se compara: si la red no lo supera, no vale la pena."),
    ("Machine learning", "Aprender patrones a partir de ejemplos con su respuesta, en vez de escribir reglas."),
    ("MLP (perceptrón multicapa)", "Red de neuronas organizadas en capas completamente conectadas."),
    ("Momentum", "Optimizador que acumula impulso, como una bicicleta en bajada."),
    ("MSE", "Error cuadrático medio: promedio de los errores al cuadrado; para predecir números."),
    ("Parámetros", "Los números que la red aprende: pesos y sesgos."),
    ("Perceptrón", "La neurona de Rosenblatt (1958) que aprende corrigiendo sus errores."),
    ("Pérdida", "Un solo número que mide qué tan mal predice el modelo; entrenar es bajarla."),
    ("Peso", "Cuánto importa un dato para la neurona; puede ser positivo o negativo."),
    ("Recall", "De los casos positivos reales, qué porcentaje encontró el modelo."),
    ("ReLU", "Activación máx(0, z); la más usada en capas ocultas."),
    ("Retropropagación", "Algoritmo que reparte la culpa del error hacia atrás con la regla de la cadena."),
    ("ROC-AUC", "Probabilidad de que el modelo le dé más riesgo a un positivo que a un negativo al azar."),
    ("Sesgo (b)", "Número que sube o baja la exigencia de la neurona; mueve la frontera."),
    ("Sigmoide", "Activación con forma de S que da un número entre 0 y 1."),
    ("Sobreajuste", "Cuando la red memoriza el entrenamiento y empeora en datos nuevos."),
    ("TensorFlow", "Librería que calcula los gradientes automáticamente (GradientTape)."),
    ("Validación", "Datos apartados para decidir (arquitectura, umbral) sin tocar la prueba."),
    ("XOR", "«Uno u otro, pero no ambos»; no se separa con una sola línea."),
]
S.append(('glosario', 'A–Z', 'Glosario', '<input id="search" class="search" type="search" placeholder="Buscar una palabra…" aria-label="Buscar en el glosario"><dl class="glos">' +
          ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS) + '</dl>'))

S.append(('cierre', '✓', '¿Listo? Comprueba lo que aprendiste', """
<p>Juega el quiz final: 12 preguntas, 30 segundos cada una. Al terminar te dice tu puntaje, qué temas repasar (con enlace a esta guía) y tu avance frente al pre-quiz.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?final">Jugar el quiz final</a><a class="btn ghost" href="../index.html">Volver al inicio</a></div>
<p>Antes del martes 27 de octubre: test individual (20 pts), encuesta de tendencia (10 pts) y entregable del mini-proyecto (70 pts). Las horas exactas están en Canvas.</p>
"""))

body = ''
toc = []
for sid, n, title, inner in S:
    kick = {'inicio': chip('Empieza aquí', 'amber'), 'pre': chip('Repaso', 'gray'), 'formulas': chip('Resumen', 'purple'),
            'glosario': chip('Referencia', 'purple'), 'cierre': chip('Autoevaluación', 'teal')}.get(sid)
    if not kick:
        day = 'Viernes' if sid in ('b01', 'b02', 'b03', 'b04') else 'Sábado'
        kick = chip(f'{day} · bloque {n}')
    if sid == 'inicio':
        body += f'<section id="inicio">{inner}</section>'
    else:
        body += section(sid, kick, title, inner)
    toc.append((sid, n, title))

html = page('Guía de estudio · Semana 1 · Deep Learning UIDE',
            'Guía de estudio de la semana 1 de Neural Networks: Deep Learning (UIDE): ideas, fórmulas explicadas, ejemplos, ejercicios con respuesta y glosario.',
            toc, body, 'dl-uide-w1-guia')
(OUT / 'guia').mkdir(parents=True, exist_ok=True)
(OUT / 'guia' / 'index.html').write_text(html)
print('guía built', len(html) // 1024, 'KB')
