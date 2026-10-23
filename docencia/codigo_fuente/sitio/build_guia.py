"""Student study guide: guia/index.html"""
import pathlib, sys, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit import page, section, chip, idea, box, formula, ex, colab, fig, hist

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
COLAB = 'https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/'
NB1, NB2 = COLAB + 'NB01_viernes_tu_primera_neurona.ipynb', COLAB + 'NB02_sabado_tu_primera_red.ipynb'
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
<h1>Fundamentos de redes neuronales, de cero a tu primera red</h1>
<span class="chip" style="margin-top:14px">Semana 1 · Guía de estudio</span>
<p>Todo lo de la semana en una sola página: la idea de cada tema en palabras sencillas, cada fórmula leída en voz alta («Léelo así»), analogías del día a día, un ejemplo con números, un dato histórico y ejercicios con su respuesta.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?pre">Jugar el pre-quiz</a><a class="btn" href="#b01">Empezar a estudiar</a><a class="btn ghost" style="color:#EEF2F8;border-color:#2A3B5C" href="../material/Apuntes_teoricos_Clase1.pdf">Apuntes en PDF</a></div>
</div>
<h2 class="sr">Cómo usar esta guía</h2>
<div class="grid">
<div class="tile"><h3>1 · Lee</h3><p>Cada tema empieza con <b>la idea en una frase</b>. Si solo tienes 5 minutos, lee esas frases.</p></div>
<div class="tile"><h3>2 · Practica</h3><p>Resuelve los ejercicios en papel <b>antes</b> de abrir la respuesta. Equivocarse aquí es gratis.</p></div>
<div class="tile"><h3>3 · Lee el código</h3><p>Cada tema dice qué parte del notebook abrir en Colab. Los notebooks ya vienen <b>escritos y resueltos</b>: no hay espacios en blanco. Se aprenden leyendo y ejecutando celda por celda.</p></div>
<div class="tile"><h3>4 · Comprueba</h3><p>Al final juega el <a href="../quiz/index.html?final">quiz final</a>: te dice qué temas repasar.</p></div>
</div>
{box('ojo', 'Mapa de la semana', '''<p><b>Viernes:</b> 01 IA, ML y DL → 02 La neurona (tu nota final es una) → 03 El perceptrón y XOR → 04 Pérdida y gradiente · notebook <b>NB01</b>, que empieza con un repaso exprés de Python.</p>
<p><b>Sábado:</b> 05 Capas → 06 Retropropagación → 07 Entrenar bien → 08 Keras · notebook <b>NB02</b> → 09 ¿El modelo es bueno?</p>
<p>Las prácticas son <b>en clase y sin nota</b>. Los notebooks están completos: cada celda trae el código, su explicación y el resultado esperado. Tu trabajo es <b>leer, ejecutar y entender</b>; al final hay experimentos opcionales para cambiar números y mirar qué pasa. Las <a href="../docencia/slides/index.html">slides interactivas</a> quedan publicadas para repasar.</p>''')}
<p>Marca <b>«Ya lo entendí»</b> al final de cada tema: tu avance se guarda en este navegador y aparece en el índice.</p>
"""))

S.append(('pre', '0', 'Antes de empezar: las bases que vamos a usar', f"""
{idea('Para esta semana bastan cuatro herramientas: funciones, vectores, pendientes y probabilidades. Nada más.')}
<h3>Funciones: una máquina con perillas</h3>
<p>Una función recibe un número y devuelve otro. Si \\(f(x) = 2x + 1\\), entonces \\(f(3) = 7\\). Una neurona es una función con muchas perillas (los <b>pesos</b>) que el entrenamiento ajusta.</p>
<h3>Vectores y producto punto</h3>
<p>Un vector es una lista de números: los datos de un socio, por ejemplo \\(\\mathbf{{x}} = (0.8,\\ 0.5,\\ -1.0)\\). El <b>producto punto</b> multiplica parejas y suma:</p>
{formula(r'\mathbf{w}\cdot\mathbf{x} = w_1x_1 + w_2x_2 + w_3x_3', note='<p>En Python con NumPy: <code>w @ x</code>.</p>',
         read='multiplica el primer peso por el primer dato, el segundo por el segundo y el tercero por el tercero, y suma los tres resultados. Es la misma cuenta de una nota final ponderada.')}
<h3>Pendiente (derivada): si me muevo un poquito, ¿cuánto cambia?</h3>
<p>La pendiente de \\(L(w) = (w-3)^2\\) es \\(L'(w) = 2(w-3)\\). En \\(w = 0\\) vale \\(-6\\): la curva baja hacia la derecha. En \\(w = 3\\) vale 0: estamos en el fondo. Esa es la idea del descenso de gradiente.</p>
<h3>Probabilidades y logaritmos</h3>
<p>Una probabilidad va de 0 a 1 (0.8 = 80 %). El logaritmo \\(-\\log p\\) es pequeño cuando \\(p\\) está cerca de 1 y enorme cuando \\(p\\) está cerca de 0: \\(-\\log(0.99) \\approx 0.01\\), \\(-\\log(0.01) \\approx 4.6\\). Con eso se construye la pérdida para clasificar.</p>
<h3>Python mínimo (es la Parte 0 del NB01)</h3>
<p>Si ya programas en Python, solo repasa. Si no, estas líneas son todo lo que necesitas para el viernes. Cada línea trae un comentario (en inglés, como en los notebooks) que dice qué hace.</p>
<pre><code># variables and print
name = "Ana"
s1 = 80                              # week-1 grade, out of 100
print(name, "got", s1)

# a list keeps several values in order
grades = [80, 70, 90, 60]            # S1, S2, S3, final project
print(len(grades), grades[0])        # 4 values; the first one is 80

# a function: give it inputs, it returns a result
def weighted_grade(grades, weights):
    return sum(g * w for g, w in zip(grades, weights))

# NumPy: fast arrays, math on whole lists at once
import numpy as np
x = np.array([0.8, 0.5, -1.0])       # a vector: one member's data
w = np.array([1.2, 0.7, -2.0])       # one weight per datum
z = w @ x + (-0.5)                   # dot product plus bias -> 2.81
1 / (1 + np.exp(-z))                 # sigmoid -> 0.943

# matplotlib: draw what you computed
import matplotlib.pyplot as plt
plt.bar(["S1", "S2", "S3", "Final"], grades)
plt.show()</code></pre>
<p class="read"><b>Léelo así:</b> <code>np.array</code> convierte una lista en un vector con el que se puede hacer matemática; <code>@</code> es el producto punto (multiplica parejas y suma); <code>np.exp(z)</code> es \\(e^z\\), la función exponencial.</p>
<h3>Practica</h3>
{ex('Si \\(f(x) = 3x - 2\\), ¿cuánto vale \\(f(4)\\)?', '<p>\\(3\\cdot 4 - 2 = 10\\).</p>')}
{ex('Calcula \\(\\mathbf{w}\\cdot\\mathbf{x}\\) con \\(\\mathbf{w} = (2, -1)\\) y \\(\\mathbf{x} = (3, 4)\\).', '<p>\\(2\\cdot3 + (-1)\\cdot 4 = 6 - 4 = 2\\).</p>')}
{ex('¿Cuál es la pendiente de \\(L(w) = w^2\\) en \\(w = 2\\)? ¿Hacia dónde conviene moverse para bajar?', '<p>\\(L\'(w) = 2w\\), así que en \\(w=2\\) vale 4 (positiva): la curva sube hacia la derecha, conviene <b>bajar</b> \\(w\\).</p>')}
"""))

S.append(('b01', '01', 'IA, machine learning y deep learning', f"""
{idea('La IA es el campo; el machine learning aprende patrones de ejemplos; el deep learning lo hace con redes neuronales de muchas capas.')}
<h3>Primero, la necesidad: hay tareas sin reglas fáciles</h3>
<p>Imagina que quieres un programa que reconozca gatos en fotos. Escribes una regla: «si tiene orejas puntiagudas, es un gato». Pero un zorro también las tiene. Agregas «y si tiene bigotes»: un perro también. Y un gato de espaldas no muestra la cara. <b>Cada regla nueva abre otra excepción.</b></p>
<p>Un niño, en cambio, aprende a reconocer gatos viendo muchos gatos. Nadie le da la lista de reglas. Esa es la idea del aprendizaje automático: <b>en vez de escribir las reglas, mostramos ejemplos con su respuesta</b> y dejamos que la computadora encuentre el patrón.</p>
<h3>¿Por qué importa tanto hoy?</h3>
<ul>
<li><b>Ver imágenes.</b> En el concurso ImageNet, los mejores sistemas fallaban cerca del 26 % de las veces en 2011 (contando como acierto si la respuesta correcta estaba entre sus 5 primeras opciones). En 2015 una red profunda bajó a 3.6 %.</li>
<li><b>Ciencia.</b> AlphaFold predice la forma 3D de las proteínas. Por ese trabajo, Demis Hassabis y John Jumper compartieron el <b>Nobel de Química 2024</b> con David Baker.</li>
<li><b>Las bases.</b> El <b>Nobel de Física 2024</b> fue para John Hopfield y Geoffrey Hinton, por las ideas que permiten que las redes neuronales aprendan.</li>
<li><b>La vida diaria.</b> Traductores, asistentes de voz, filtros de spam, recomendaciones y modelos de lenguaje como ChatGPT o Claude usan redes neuronales.</li>
</ul>
<h3>Cinco palabras que usaremos toda la semana</h3>
<table><tr><th>Palabra</th><th>Qué significa</th><th>En la cooperativa</th></tr>
<tr><td><b>Dato</b> o <b>característica</b></td><td>un número que describe algo</td><td>el ingreso del socio</td></tr>
<tr><td><b>Ejemplo</b></td><td>un caso completo, con todos sus datos</td><td>la ficha de un socio</td></tr>
<tr><td><b>Etiqueta</b></td><td>la respuesta correcta conocida</td><td>pagó o no pagó</td></tr>
<tr><td><b>Modelo</b></td><td>la fórmula con perillas que aprende</td><td>la red neuronal</td></tr>
<tr><td><b>Predicción</b></td><td>la respuesta que da el modelo</td><td>«creo que pagará»</td></tr></table>
<p>Un <b>conjunto de datos</b> es una tabla: cada <b>fila</b> es un ejemplo y cada <b>columna</b> es un dato. La etiqueta y la predicción <b>no son lo mismo</b>: la etiqueta es lo que de verdad pasó; la predicción es lo que el modelo cree. Aprender es hacer que se parezcan.</p>
<p><b>Aprender</b>, para una computadora, no es entender ni sentir: es <b>ajustar números para equivocarse menos</b> en los ejemplos.</p>
<h3>Dos tipos de pregunta</h3>
<ul>
<li><b>Clasificación:</b> la respuesta es una <b>clase</b> (una categoría). «¿Pagará o no?» es clasificación <b>binaria</b>: solo hay dos clases.</li>
<li><b>Regresión:</b> la respuesta es una <b>cantidad</b>. «¿Cuánto cuesta esta casa?» Aquí «regresión» no significa retroceder: es el nombre histórico de estimar un número.</li>
</ul>
<p>Cuando cada ejemplo trae su etiqueta, el aprendizaje se llama <b>supervisado</b>: es como estudiar con un solucionario. Toda esta semana es supervisada.</p>
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
         [(r'\mathbf{x}', 'los datos de un ejemplo (la ficha del socio)', B), (r'y', 'la respuesta correcta (pagó o no)', T), (r'\theta', 'las perillas que se aprenden', A)],
         read='tenemos muchos ejemplos, cada uno con sus datos x y su respuesta correcta y. Buscamos una función f, con perillas θ, que al recibir los datos de cada ejemplo dé una respuesta parecida a la correcta. Aprender es girar esas perillas.')}
<h3>Tres formas de aprender</h3>
<table><tr><th>Tipo</th><th>Qué recibe</th><th>Ejemplo</th></tr>
<tr><td><b>Supervisado</b> (esta semana)</td><td>datos con la respuesta correcta</td><td>predecir si un socio cae en mora</td></tr>
<tr><td>No supervisado</td><td>datos sin respuesta</td><td>agrupar clientes por hábitos de compra</td></tr>
<tr><td>Por refuerzo</td><td>premios y castigos por sus acciones</td><td>un agente que aprende a jugar</td></tr></table>
{box('analogia', 'Analogía', '<p>El comerciante del mercado que con los años aprende a quién fiarle: nadie le dio un manual; aprendió de muchos casos (quién pagó y quién no).</p>')}
<h3>¿Por qué ahora?</h3>
<p>Las redes existen desde 1958, pero despegaron después de 2012 por tres cosas juntas: muchos más <b>datos</b>, procesadores gráficos (<b>GPU</b>: el chip que dibuja los videojuegos, y que también sirve para hacer muchas cuentas a la vez) que hacen millones de multiplicaciones en paralelo y <b>mejores técnicas</b> de entrenamiento (ReLU, buenas inicializaciones, Adam).</p>
<h3>¿Cuándo conviene el deep learning?</h3>
<p>Brilla con <b>imágenes, texto, audio y series largas</b>, donde es difícil describir a mano qué mirar. En <b>datos de tabla</b> (como los socios de una cooperativa), una regresión logística o un modelo de árboles a veces lo iguala: por eso siempre se compara con una <b>línea base</b>.</p>
<h3>Practica</h3>
{ex('Un filtro marca como spam todo correo que diga «GRATIS». ¿Es machine learning?', '<p>No: es una regla escrita por una persona. Sería ML si aprendiera de miles de correos marcados como spam o no spam.</p>')}
{ex('Quieres agrupar a los socios en perfiles parecidos sin tener una etiqueta. ¿Qué tipo de aprendizaje es?', '<p>No supervisado: no hay respuesta correcta que imitar.</p>')}
{ex('¿Predecir el precio de un auto usado es clasificación o regresión? ¿Y decidir si un correo es spam?', '<p>El precio es una cantidad: <b>regresión</b>. Spam o no spam son dos clases: <b>clasificación binaria</b>.</p>')}
{ex('¿Todo programa que toma decisiones es IA que aprende?', '<p>No. Una calculadora o una regla fija («si llueve, enviar aviso») deciden, pero no aprenden de ejemplos.</p>')}
"""))

S.append(('b02', '02', 'La neurona artificial', f"""
{idea('Una neurona multiplica cada dato por su peso, suma todo con un sesgo y decide con una función de activación.')}
<h3>Primero: ¿qué es un peso?</h3>
<p>Una materia tiene examen y deberes. El examen vale 80 % y los deberes 20 %. Sacaste 90 en el examen y 50 en los deberes:</p>
<p style="text-align:center">\\(90 \\times 0.8 + 50 \\times 0.2 = 72 + 10 = 82\\)</p>
<p>El 0.8 y el 0.2 son <b>pesos</b>: números que multiplican cada dato y controlan <b>cuánto aporta</b>. Multiplicar por un peso puede <b>aumentar</b> un dato (peso mayor que 1), <b>reducirlo</b> (entre 0 y 1) o <b>invertirlo</b> (negativo: el dato resta). Un peso alto no significa que el dato sea «moralmente» más importante: solo que pesa más en la cuenta. En una red, los pesos <b>no tienen que sumar 1 ni ser positivos</b>. Multiplicar cada dato por su peso y sumar se llama <b>suma ponderada</b>.</p>
<h3>Tu nota final del curso ya es una neurona</h3>
<p>El sílabo de este curso calcula la nota final así (cada semana y la entrega final se califican sobre 100):</p>
{formula(r'\text{Nota final} = 0.2667\,S_1 + 0.2667\,S_2 + 0.2667\,S_3 + 0.20\,\text{Final}',
         [(r'S_1,\ S_2,\ S_3,\ \text{Final}', 'tus notas: los datos', B), (r'0.2667,\ 0.20', 'cuánto pesa cada nota: los pesos', A)],
         read='la nota de cada semana cuenta un 26.67 % y la entrega final un 20 %. Cada nota se multiplica por lo que pesa y se suma todo.')}
<p><b>Ana</b> sacó 80, 70 y 90 en las semanas y 60 en la entrega final:</p>
<table><tr><th>Nota</th><th>Dato \\(x\\)</th><th>Peso \\(w\\)</th><th>Aporte \\(w\\cdot x\\)</th></tr>
<tr><td>Semana 1</td><td>80</td><td>0.2667</td><td>21.33</td></tr>
<tr><td>Semana 2</td><td>70</td><td>0.2667</td><td>18.67</td></tr>
<tr><td>Semana 3</td><td>90</td><td>0.2667</td><td>24.00</td></tr>
<tr><td>Entrega final</td><td>60</td><td>0.20</td><td>12</td></tr>
<tr><th>Nota final</th><th colspan="2"></th><th>76</th></tr></table>
<p>Ahora la decisión. <b>Si se aprobara con 70/100</b> (es un ejemplo para hacer la cuenta, no la regla del curso), la pregunta «¿aprueba?» es una neurona completa: los <b>pesos</b> son los porcentajes, el <b>sesgo</b> es la exigencia con signo menos (\\(b = -70\\)) y la <b>activación</b> es un escalón que dice sí cuando el puntaje no es negativo.</p>
{formula(r'z = 0.2667\,S_1 + 0.2667\,S_2 + 0.2667\,S_3 + 0.20\,\text{Final} - 70',
         [('z', 'el puntaje: cuánto le sobra o le falta', I), ('-70', 'el sesgo: la exigencia', A)],
         read='suma las notas con sus pesos y réstale la exigencia. Si el resultado z es 0 o más, aprueba; si es negativo, no.')}
<ul><li><b>Ana:</b> \\(z = 76 - 70 = 6\\) → <b>aprueba</b>.</li>
<li><b>Beto</b> (60, 55, 65 y 70 en el final): \\(0.2667\\cdot 180 + 0.20\\cdot 70 = 48 + 14 = 62\\), así que \\(z = 62 - 70 = -8\\) → <b>no aprueba</b>.</li></ul>
<h3>¿Qué es el sesgo?</h3>
<p>Piensa en un marcador que no empieza en cero, sino en <b>−70</b>. Cada nota suma puntos; si al final el marcador queda en cero o más, apruebas. Ese punto de partida es el <b>sesgo</b> \\(b\\). Si la exigencia sube a 80, el marcador empieza en \\(b = -80\\) y Ana queda en \\(76 - 80 = -4\\): ya no aprueba.</p>
<p><b>El peso cambia cuánto aporta cada dato; el sesgo cambia desde dónde empezamos a contar.</b> Otro ejemplo: un taxi cobra 5 dólares al subir y 2 por hora. El 2 es el peso de las horas; el 5 es el sesgo, lo que pagas aunque el viaje dure cero. En inglés se dice <i>bias</i>, pero aquí no significa prejuicio: es solo un número de ajuste. <b>La red también aprende el sesgo.</b></p>
<p>Así, el 70 de la regla «aprobar con 70» se convirtió en una pregunta más simple: <b>¿el puntaje \\(z\\) es mayor o igual que cero?</b> El cero es el <b>umbral</b> de la neurona.</p>
<p>La gran diferencia con una neurona de verdad: estos pesos los fijó el sílabo. <b>Una red los aprende sola</b>, a partir de ejemplos con su respuesta.</p>
{hist('1943', 'Warren McCulloch y Walter Pitts publican el primer modelo matemático de una neurona: datos que entran, una suma y un umbral. Es la idea de esta página, ochenta años antes de ChatGPT.')}
{fig(svg_neuron(), 'Entradas × pesos → suma con sesgo → activación → salida.')}
<h3>En fórmula</h3>
<p>Una <b>neurona artificial</b> es una pequeña unidad de cálculo: no es una célula ni piensa. Recibe números, hace una suma ponderada y entrega un resultado. Las letras son solo nombres cortos: \\(x\\) para los datos, \\(w\\) para los pesos (de <i>weight</i>), \\(b\\) para el sesgo y \\(z\\) para el puntaje. Los subíndices (\\(x_1, x_2\\)) solo distinguen un dato de otro.</p>
{formula(r'z = w_1x_1 + w_2x_2 + w_3x_3 + b = \mathbf{w}\cdot\mathbf{x} + b \qquad a = \varphi(z)',
         [('z', 'el puntaje total', I), (r'w_i x_i', 'cada dato por su importancia', B), ('b', 'el sesgo: qué tan exigente es', A), (r'\varphi', 'la activación: convierte el puntaje en salida', T)],
         read='z es el puntaje: cada dato x por su peso w, todo sumado, más el sesgo b. Después la activación φ (la letra griega «fi») convierte ese puntaje en la salida a: un sí o no, o una probabilidad. En la nota final, las x son las notas, las w los porcentajes y b = −70.')}
<h3>Un caso aplicado: el comité de crédito</h3>
<p>La nota final solo suma cosas buenas. En la vida real algunos datos <b>restan</b>, y ahí aparecen los pesos negativos. Un comité de crédito mira tres datos de un socio. Están <b>escalados</b>: 0 es el promedio, +1 es algo por encima y −1 algo por debajo. Así, un −1 en atrasos significa «menos atrasos que el promedio», no «menos un atraso». (Es un ejemplo para aprender, no un sistema real de crédito.)</p>
<table><tr><th>Dato</th><th>Valor \\(x\\)</th><th>Peso \\(w\\)</th><th>Aporte \\(w\\cdot x\\)</th></tr>
<tr><td>Ingreso</td><td>0.8</td><td>1.2</td><td>+0.96</td></tr>
<tr><td>Antigüedad</td><td>0.5</td><td>0.7</td><td>+0.35</td></tr>
<tr><td>Atrasos (menos que el promedio)</td><td>−1.0</td><td>−2.0</td><td>+2.00</td></tr>
<tr><td>Sesgo \\(b\\)</td><td colspan="2"></td><td>−0.50</td></tr>
<tr><th>Puntaje \\(z\\)</th><th colspan="2"></th><th>2.81</th></tr></table>
<p>Con escalón: \\(z \\ge 0\\) → <b>aprueba</b>. Con sigmoide: \\(\\sigma(2.81) \\approx 0.94\\) → <b>94 % de probabilidad estimada de pago</b>. Es una estimación, no una garantía: de muchos socios parecidos, unos 94 de cada 100 pagarían. Fíjate: un peso negativo por un dato negativo da un aporte positivo.</p>
{box('analogia', 'Analogía: el comité de crédito', '<p>Mira la ficha (entradas), confía más en unos datos que en otros (pesos), aplica su nivel de exigencia (sesgo) y decide (activación). <b>Aprender</b> = ajustar cuánto confía en cada dato después de ver quién pagó.</p>')}
<h3>Las tres activaciones de la semana</h3>
<p>Una <b>función</b> es una regla que recibe un número y devuelve otro, como «multiplica por dos». La <b>función de activación</b> es la regla que la neurona aplica al final para convertir el puntaje \\(z\\) en su salida.</p>
{fig(svg_acts(), 'De izquierda a derecha: interruptor, regulador de intensidad y válvula.')}
{box('analogia', 'Analogía: tres formas de dejar pasar la señal', '<p><b>Escalón = un interruptor:</b> todo o nada, como la luz de tu cuarto. <b>Sigmoide = un regulador de luz:</b> va de apagado a encendido de forma suave; por eso sirve para dar probabilidades. <b>ReLU = una válvula:</b> si la presión es negativa no pasa nada; si es positiva, pasa tal cual.</p>')}
<table><tr><th>Activación</th><th>Fórmula</th><th>Qué hace</th><th>Dónde se usa</th></tr>
<tr><td>Escalón</td><td>\\(1\\) si \\(z\\ge0\\); si no, \\(0\\)</td><td>sí o no</td><td>perceptrón clásico</td></tr>
<tr><td>Sigmoide</td><td>\\(\\sigma(z) = \\dfrac{{1}}{{1+e^{{-z}}}}\\)</td><td>número entre 0 y 1: una probabilidad</td><td>salida «¿paga o no?»</td></tr>
<tr><td>ReLU</td><td>\\(\\max(0, z)\\)</td><td>apaga lo negativo, deja pasar lo positivo</td><td>capas ocultas</td></tr></table>
<p class="read"><b>Léelo así:</b> la sigmoide \\(\\sigma(z) = \\dfrac{{1}}{{1+e^{{-z}}}}\\) aplasta cualquier puntaje entre 0 y 1. Si z es muy negativo, \\(e^{{-z}}\\) es enorme y el resultado se acerca a 0; si z es muy positivo, \\(e^{{-z}}\\) casi desaparece y el resultado se acerca a 1; si z = 0, da exactamente 0.5. La letra \\(e\\) es un número fijo, \\(e \\approx 2.718\\). Ejemplos: \\(\\sigma(0) = 0.5\\), \\(\\sigma(2.81) \\approx 0.943\\), \\(\\sigma(-3.61) \\approx 0.026\\). \\(\\max(0, z)\\) se lee «el mayor entre 0 y z»: ReLU da 0 o el mismo z, así que <b>no es una probabilidad</b>.</p>
<p><b>¿Para qué sirve?</b> Sin activación, apilar neuronas sería sumar sumas: el resultado seguiría siendo una recta. La activación «dobla» el espacio.</p>
<h3>Una neurona dibuja una línea</h3>
<p>Con dos datos, cada socio es un punto del plano. La neurona aprueba de un lado y rechaza del otro; la frontera es donde \\(z = 0\\):</p>
{formula(r'w_1 x_1 + w_2 x_2 + b = 0', note='<p>Los <b>pesos</b> giran la línea; el <b>sesgo</b> la mueve. Entrenar es buscar la mejor posición.</p>',
         read='son todos los puntos donde el puntaje vale exactamente cero, es decir, donde la neurona duda. Esos puntos forman una línea recta: de un lado aprueba y del otro rechaza.')}
{box('error', 'Errores comunes', '<ul><li>Olvidar el sesgo \\(b\\) al calcular \\(z\\).</li><li>Confundir \\(z\\) (puntaje) con la salida \\(a\\) (decisión o probabilidad).</li><li>Pensar que un peso negativo «está mal»: solo dice que ese dato resta.</li></ul>')}
<h3>Practica</h3>
{ex('¿Cuánto necesita Ana en la entrega final para llegar justo a 70, con sus notas de 80, 70 y 90 en las semanas?', '<p>Las semanas ya le dan \\(\\approx 64\\). Necesita \\(64 + 0.20\\cdot F = 70\\): \\(0.20\\cdot F = 6\\), así que \\(F = 30\\). Con 30, \\(z = 0\\): queda justo sobre la línea.</p>')}
{ex('Socio B: ingreso 0.2, antigüedad −0.5, atrasos 1.5, con los mismos pesos y sesgo. ¿Cuánto vale \\(z\\)? ¿Qué decide?', '<p>\\(z = 1.2\\cdot0.2 + 0.7\\cdot(-0.5) + (-2)\\cdot1.5 - 0.5 = 0.24 - 0.35 - 3.0 - 0.5 = -3.61\\). Rechaza; con sigmoide, \\(\\approx 2.6\\,\\%\\) de probabilidad de pago.</p>')}
{ex('¿Cuánto vale \\(\\sigma(0)\\)? ¿Qué significa para el socio?', '<p>0.5: la neurona duda. El socio está exactamente sobre la línea frontera.</p>')}
{ex('Si el comité se vuelve más exigente, ¿qué número cambia y hacia dónde?', '<p>El sesgo \\(b\\) baja (más negativo): hace falta más puntaje para aprobar.</p>')}
{colab(NB1, '<b>NB01</b>, Parte 0 (Python exprés) y secciones 1 y 2: lee y ejecuta la nota final como neurona, el comité de crédito y las tres activaciones. Todo el código ya está escrito.')}
"""))

S.append(('b03', '03', 'Cómo aprende una neurona: el perceptrón y XOR', f"""
{idea('El perceptrón aprende corrigiéndose solo cuando se equivoca: empuja los pesos hacia la respuesta correcta.')}
<h3>El ciclo de todo aprendizaje</h3>
<p><b>Predecir → comparar → corregir → repetir.</b> Como ajustar la sal del locro: pruebas, notas que falta, echas una pizca, vuelves a probar. Cada vuelta completa por todos los datos se llama <b>época</b>.</p>
<h3>En fórmula: la regla del perceptrón</h3>
<p>Aquí usamos las etiquetas \\(y = +1\\) (aprobar) y \\(y = -1\\) (rechazar) en lugar de 1 y 0. Es solo notación: así el signo de \\(y\\) dice hacia dónde corregir. La <b>tasa de aprendizaje</b> \\(\\eta\\) es el tamaño de cada corrección, como cuánto giras la llave de la ducha. Cuando se equivoca:</p>
{formula(r'\mathbf{w} \leftarrow \mathbf{w} + \eta\, y\, \mathbf{x} \qquad b \leftarrow b + \eta\, y',
         [(r'\mathbf{w}', 'los pesos actuales', I), (r'\eta', 'tamaño de la corrección (aquí 1)', A), ('y', 'la respuesta correcta: +1 o −1', T), (r'\mathbf{x}', 'el dato que clasificó mal', B)],
         read='la flecha ← significa «se reemplaza por». El peso nuevo es el peso viejo más un pasito η (la letra griega «eta») en la dirección de la respuesta correcta: si debía decir sí (y = +1) se le suma el dato; si debía decir no (y = −1) se le resta. Con el sesgo pasa lo mismo, pero sin dato.')}
<h3>Ejemplo con números</h3>
<p>Pesos \\(\\mathbf{{w}} = (0.2, -0.5)\\), \\(b = 0\\). Un socio \\(\\mathbf{{x}} = (1, 1)\\) que debía aprobarse (\\(y=+1\\)):</p>
<ol><li>Antes: \\(z = 0.2 - 0.5 + 0 = -0.30\\) → rechaza. <b>Error.</b></li>
<li>Corrige: \\(\\mathbf{{w}} = (0.2+1,\\ -0.5+1) = (1.2,\\ 0.5)\\), \\(b = 0 + 1 = 1\\).</li>
<li>Después: \\(z = 1.2 + 0.5 + 1 = +2.70\\) → aprueba. <b>Acierta.</b></li></ol>
{hist('1958', 'Frank Rosenblatt presenta el perceptrón, la primera neurona artificial que aprende de sus errores. La prensa de la época llegó a anunciar que pronto caminaría y hablaría.')}
<h3>Una neurona dibuja una recta en el plano</h3>
<p>Con dos datos, cada socio es un punto en un <b>plano de coordenadas</b>: el primer dato va en el eje horizontal y el segundo en el vertical. La <b>frontera de decisión</b> es la línea que separa «aprueba» de «rechaza». Aunque usemos sigmoide y decidamos con 50 %, la frontera sigue siendo una <b>recta</b>: el 50 % ocurre justo donde \\(z = 0\\).</p>
<h3>La garantía y el límite</h3>
<p><b>Si una línea puede separar los datos</b>, el perceptrón la encuentra en un número finito de correcciones (Novikoff, 1962). Pero <b>XOR</b>, la luz de la escalera (se enciende si los interruptores están en posiciones distintas), no se puede separar con una sola línea. Ojo con la frase: no es que «no la encontramos»; es que <b>no existe</b> ninguna recta que deje los dos casos «encendida» de un lado y los dos «apagada» del otro. Por eso el perceptrón sigue fallando época tras época. En el NB01 verás 4 correcciones en cada época: como la línea se mueve después de cada error, en una misma vuelta puede pasar a fallar casos que antes acertaba.</p>
<table><tr><th>\\(x_1\\)</th><th>\\(x_2\\)</th><th>XOR (luz)</th></tr><tr><td>0</td><td>0</td><td>apagada</td></tr><tr><td>0</td><td>1</td><td>encendida</td></tr><tr><td>1</td><td>0</td><td>encendida</td></tr><tr><td>1</td><td>1</td><td>apagada</td></tr></table>
<p>En el negocio, XOR aparece cuando el efecto de una variable <b>depende de otra</b> (por ejemplo, el garante ayuda solo si la cuota es baja). La solución llega el sábado: <b>más de una neurona</b>.</p>
{hist('1969', 'Marvin Minsky y Seymour Papert demuestran en su libro <i>Perceptrons</i> que una sola neurona no puede con XOR. El entusiasmo y el financiamiento caen: es el primer «invierno» de la IA.')}
{box('curioso', 'Para curiosos', '<p>El número de correcciones está acotado por \\((R/\\gamma)^2\\): \\(R\\) es qué tan lejos están los datos del origen y \\(\\gamma\\) el <b>margen</b>, el ancho del «pasillo» vacío entre las clases. Pasillo ancho, aprendizaje rápido.</p>')}
<h3>Practica</h3>
{ex('Con \\(\\mathbf{w} = (1.2, 0.5)\\), \\(b = 1\\), llega \\(\\mathbf{x} = (1, 0.5)\\) que NO pagó (\\(y = -1\\)). ¿Se equivoca? Aplica una corrección.', '<p>\\(z = 1.2 + 0.25 + 1 = 2.45\\) → aprueba: error. Corrige: \\(\\mathbf{w} = (1.2-1,\\ 0.5-0.5) = (0.2, 0)\\), \\(b = 0\\). Nuevo \\(z = 0.2\\): todavía aprueba. Hacen falta más vueltas.</p>')}
{ex('¿La compuerta AND (vale 1 solo si ambos valen 1) se puede aprender con un perceptrón?', '<p>Sí: una línea deja (1,1) de un lado y los otros tres del otro. Por ejemplo \\(x_1 + x_2 - 1.5 = 0\\).</p>')}
{colab(NB1, '<b>NB01</b>, secciones 3 a 5: lee la corrección hecha paso a paso, el perceptrón que aprende AND y el que nunca aprende XOR.')}
"""))

S.append(('b04', '04', 'Medir el error y mejorar: pérdida y descenso de gradiente', f"""
{idea('La pérdida mide qué tan mal vamos con un solo número; el descenso de gradiente mueve los pesos cuesta abajo para bajarla.')}
<h3>Paso 1 · El error de un caso</h3>
<p>Una casa vale 100 mil dólares y el modelo dice 99. Se equivocó por poco. Si dice 160, se equivocó por mucho. Para medirlo restamos:</p>
<p style="text-align:center"><b>error = valor real − valor predicho</b></p>
<ul><li>Dice 99: \\(100 - 99 = 1\\).</li><li>Dice 160: \\(100 - 160 = -60\\).</li></ul>
<p>El signo solo dice hacia dónde falló (negativo = se pasó). El tamaño, 1 o 60, dice <b>cuánto</b> falló.</p>
<h3>Paso 2 · La pérdida: un solo número para todos los casos</h3>
<p>Un modelo predice muchos casos a la vez. Necesitamos <b>un solo número</b> que resuma todos los errores: eso es la <b>pérdida</b> (en inglés, <i>loss</i>). No tiene nada que ver con perder dinero. Es como una nota al revés: <b>0 es perfecto; mientras más pequeña, mejor</b>. Entrenar es bajarla.</p>
<h3>MSE en tres pasos</h3>
<p>Cuatro casas en Quito, en miles de USD: reales 120, 95, 150, 80 y predichas 110, 100, 170, 82.</p>
<ol><li><b>Resta</b> real − predicho: 10, −5, −20, −2.</li>
<li><b>Eleva al cuadrado</b> cada error: 100, 25, 400, 4.</li>
<li><b>Promedia</b>: \\((100 + 25 + 400 + 4) / 4 = 529 / 4 =\\) <b>132.25</b>.</li></ol>
<p>¿Por qué al cuadrado? Para que un error de −20 no cancele uno de +20, y para que los errores grandes pesen mucho más (20 al cuadrado es 400; 2 al cuadrado es solo 4). Ojo: el resultado queda en <b>unidades al cuadrado</b> (miles de dólares al cuadrado), así que 132.25 no se lee como dólares.</p>
{formula(r'\text{MSE} = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat y_i)^2', [('y', 'valor real', T), (r'\hat y', 'lo que predijo el modelo', B), ('N', 'número de ejemplos', I)], '<p>Para predecir <b>números</b> (precios). Elevar al cuadrado castiga mucho los errores grandes.</p>',
         read='para cada ejemplo, resta lo real menos lo predicho (el error) y elévalo al cuadrado: así los negativos no restan y los errores grandes pesan más. Suma todos (eso es la Σ) y divide para N: el promedio de los errores al cuadrado. «ŷ» se lee «y sombrero»: la predicción.')}
{hist('1805', 'Adrien-Marie Legendre publica el método de mínimos cuadrados para calcular órbitas de cometas: elegir la curva que hace mínima la suma de errores al cuadrado. Es la idea del MSE.')}
<h3>Para clasificar: la BCE</h3>
<p>Cuando la respuesta es sí o no, el modelo da una probabilidad \\(p\\) de «sí». La probabilidad de «no» es lo que falta para llegar a 1: \\(1 - p\\). Si el modelo dice \\(p = 0.9\\) de pago, le da \\(1 - p = 0.1\\) a «no paga».</p>
<p>La <b>BCE</b> (entropía cruzada binaria) mira la probabilidad que el modelo le dio a <b>lo que de verdad pasó</b> y le aplica \\(-\\log\\). No hace falta saber logaritmos; basta su efecto: si esa probabilidad es alta, la pérdida es casi cero; si es muy baja, la pérdida se dispara.</p>
{formula(r'\text{BCE} = -\big[\,y\log\hat y + (1-y)\log(1-\hat y)\,\big]', [('y', '1 si pagó, 0 si no', T), (r'\hat y', 'probabilidad que dio el modelo', B)], '<p>Para clasificar <b>sí/no</b>. Si pagó queda \\(-\\log\\hat y\\); si no pagó, \\(-\\log(1-\\hat y)\\).</p>',
         read='parece larga, pero solo una de sus dos mitades queda viva. Si el socio pagó (y = 1), la pérdida es menos el logaritmo de la probabilidad que el modelo le dio a «paga»; si no pagó (y = 0), menos el logaritmo de la probabilidad que le dio a «no paga». En corto: menos el logaritmo de la probabilidad que le dio a lo que de verdad pasó.')}
<table><tr><th>El socio pagó; el modelo dijo…</th><th>99 %</th><th>90 %</th><th>50 %</th><th>10 %</th><th>1 %</th></tr>
<tr><td>Pérdida BCE</td><td>0.01</td><td>0.11</td><td>0.69</td><td>2.30</td><td>4.61</td></tr></table>
{box('analogia', 'Analogía: el pronóstico del clima', '<p>Decir «99 % sin lluvia» el día de un aguacero en Quito te deja muy mal; decir 50 %, no tanto. La BCE castiga la <b>falsa seguridad</b>.</p>')}
{box('ojo', 'Tres palabras que no son lo mismo', '<table><tr><th>Palabra</th><th>Qué es</th><th>Ejemplo</th></tr><tr><td><b>Error</b></td><td>cuánto falló <b>un</b> caso</td><td>100 − 160 = −60</td></tr><tr><td><b>Pérdida</b></td><td><b>un número</b> que resume los errores de todos los casos</td><td>MSE = 132.25</td></tr><tr><td><b>Gradiente</b></td><td>hacia dónde y cuánto cambia la pérdida si movemos cada perilla</td><td>la lista de derivadas</td></tr></table><p>El error y la pérdida dicen <b>qué tan mal</b> vamos. El gradiente dice <b>qué mover</b> para mejorar.</p>')}
<h3>Paso 3 · La derivada: ¿qué pasa si muevo un poquito una perilla?</h3>
<p>Los pesos y sesgos son las <b>perillas</b> del modelo; su nombre técnico es <b>parámetros</b>. La <b>derivada</b> responde: si muevo un poquito esta perilla, ¿cuánto cambia la pérdida, y en qué dirección? Es un efecto <b>local</b>: vale cerca del punto donde estamos.</p>
<ul><li>Peso 2, derivada <b>+4</b>: subir el peso sube la pérdida. Hay que <b>bajarlo</b>. Con \\(\\eta = 0.1\\): \\(2 - 0.1 \\times 4 = 1.6\\).</li>
<li>Peso 2, derivada <b>−4</b>: subir el peso baja la pérdida. Hay que <b>subirlo</b>: \\(2 - 0.1 \\times (-4) = 2.4\\).</li></ul>
<p>Una red tiene muchas perillas. El <b>gradiente</b> es la lista con la derivada de cada una (en matemática, una lista así se llama <b>vector</b>).</p>
<h3>Descenso de gradiente: bajar el Cotopaxi con neblina</h3>
<p>No ves el valle, pero con el pie sientes hacia dónde baja el terreno (la <b>pendiente</b>) y das un paso hacia allá. La analogía tiene un límite: la montaña real tiene dos direcciones; la pérdida de una red puede tener miles o millones, una por perilla.</p>
{formula(r'w \leftarrow w - \eta \cdot \frac{\partial L}{\partial w}', [('w', 'el peso', I), (r'\eta', 'largo del paso (tasa de aprendizaje)', A), (r'\partial L/\partial w', 'la pendiente: hacia dónde sube la pérdida', B)], '<p>El <b>signo menos</b> es la clave: la pendiente apunta cuesta arriba y nosotros vamos al revés.</p>',
         read='el peso nuevo es el peso actual menos un paso. El paso es η (qué tan largo caminas) por la pendiente ∂L/∂w, que se lee «cuánto sube la pérdida L si muevo un poquito el peso w». Si la pendiente es negativa, restar un negativo suma: el peso sube.')}
{hist('1847', 'Augustin-Louis Cauchy propone el descenso de gradiente para resolver ecuaciones de la astronomía. Casi dos siglos después, entrena todas las redes neuronales.')}
{fig(svg_gd(), 'Pérdida \\((w-3)^2\\), paso η = 0.1: w = 0 → 0.6 → 1.08 → 1.464 → 1.771…')}
<table><tr><th>Paso</th><th>w</th><th>pendiente 2(w−3)</th><th>pérdida</th></tr>
<tr><td>0</td><td>0</td><td>−6</td><td>9.00</td></tr><tr><td>1</td><td>0.6</td><td>−4.8</td><td>5.76</td></tr><tr><td>2</td><td>1.08</td><td>−3.84</td><td>3.69</td></tr><tr><td>3</td><td>1.464</td><td>−3.07</td><td>2.36</td></tr><tr><td>4</td><td>1.771</td><td>−2.46</td><td>1.51</td></tr></table>
<p class="read"><b>Ejemplo paso a paso:</b> la pérdida es \\(L(w) = (w-3)^2\\) y su derivada es \\(2(w-3)\\). Empezamos en \\(w = 0\\): la pérdida vale 9 y la derivada −6. El paso es \\(0 - 0.1 \\times (-6) = 0.6\\), y la pérdida baja a 5.76. Desde 0.6 la derivada es −4.8 y llegamos a 1.08, con pérdida 3.69. Cada paso nos acerca al fondo, en \\(w = 3\\).</p>
<h3>El tamaño del paso η</h3>
<ul><li><b>Muy corto</b> (η = 0.02): llega, pero tarda una eternidad.</li><li><b>Bien elegido</b> (η = 0.4): llega en pocos pasos. En esta curva en particular, η = 0.5 llega al fondo en un solo paso; no es una regla para todas las curvas.</li><li><b>Muy largo</b> (η = 1.02): se pasa del fondo y rebota cada vez más lejos: <b>diverge</b>.</li></ul>
<p><b>Converger</b> es acercarse cada vez más al fondo; <b>divergir</b> es alejarse cada vez más.</p>
{box('analogia', 'Analogía: la ducha', '<p>Quieres el agua tibia. Si giras la llave del agua caliente un poquito y esperas, llegas, aunque despacio (η pequeño). Si la giras de golpe, te quemas; la cierras de golpe y te congelas; cada corrección es más brusca que la anterior. Eso es un η demasiado grande: <b>diverge</b>.</p>')}
{box('error', 'Errores comunes', '<ul><li>Usar \\(-\\log\\hat y\\) cuando el socio NO pagó: ahí va \\(-\\log(1-\\hat y)\\).</li><li>Olvidar el signo menos y subir la montaña.</li><li>Si la pérdida sube o aparece <code>NaN</code>: casi siempre η es demasiado grande.</li></ul>')}
<h3>Practica</h3>
{ex('El modelo dijo 0.9 y el socio NO pagó. ¿Cuánto vale la BCE?', '<p>\\(-\\log(1 - 0.9) = -\\log(0.1) \\approx 2.30\\).</p>')}
{ex('Con \\(L(w) = (w-3)^2\\), \\(\\eta = 0.1\\) y \\(w = 1\\): ¿cuánto vale \\(w\\) después de un paso?', '<p>Pendiente \\(2(1-3) = -4\\). Nuevo \\(w = 1 - 0.1\\cdot(-4) = 1.4\\).</p>')}
{ex('Con \\(L(w) = (w+2)^2\\), ¿dónde está el mínimo y hacia dónde se mueve \\(w\\) si empieza en 5?', '<p>En \\(w = -2\\). Desde 5 la pendiente es positiva, así que \\(w\\) baja hacia −2.</p>')}
{colab(NB1, '<b>NB01</b>, secciones 6 a 8 y las tareas finales: lee cómo se calculan MSE y BCE, cómo se baja otra montaña, \\(L = (w+2)^2\\) con mínimo en −2, y la comparación de tamaños de paso. Al final, un experimento opcional: tu propio comité de crédito.')}
"""))

S.append(('b05', '05', 'De una neurona a una red', f"""
{idea('Una red son neuronas organizadas en capas: cada capa arma pistas más elaboradas a partir de la anterior.')}
<h3>Primero, las palabras</h3>
<p>Una <b>red neuronal</b> son varias neuronas conectadas, organizadas en <b>capas</b>: grupos de neuronas que trabajan al mismo tiempo. Funciona como una cadena de trabajo: cada capa recibe lo que hizo la anterior y lo pasa a la siguiente.</p>
<ul><li><b>Capa de entrada:</b> los datos tal como llegan. No calcula nada.</li>
<li><b>Capa oculta:</b> las capas del medio. «Oculta» no significa secreta: solo que no vemos su resultado directamente, ni en la entrada ni en la salida.</li>
<li><b>Capa de salida:</b> da la respuesta final.</li></ul>
<p>Una <b>capa densa</b> (<code>Dense</code> en Keras) es una capa donde cada neurona está conectada con todo lo que sale de la capa anterior.</p>
{fig(svg_mlp(), 'Entrada (los datos) → capa oculta (inventa pistas) → salida (decide).')}
<h3>En fórmula: cada capa</h3>
{formula(r'\mathbf{a}^{(l)} = \varphi\big(W^{(l)}\,\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}\big), \qquad \mathbf{a}^{(0)} = \mathbf{x}',
         [(r'W^{(l)}', 'pesos de la capa: cada fila es una neurona', B), (r'\mathbf{b}^{(l)}', 'un sesgo por neurona', A), (r'\mathbf{a}^{(l)}', 'lo que sale de la capa l', T)],
         read='lo que sale de una capa es lo que salió de la capa anterior, multiplicado por la tabla de pesos W de esta capa, más sus sesgos b, y todo pasado por la activación φ. El (l) de arriba solo dice de qué capa hablamos; la primera capa recibe los datos: a⁽⁰⁾ = x.')}
{box('analogia', 'Analogía: las agencias de la cooperativa', '<p>Cada agencia (neurona oculta) resume una pista: «¿tiene capacidad de pago?», «¿es cumplido?». El comité central (salida) decide con esas pistas, no con los datos crudos.</p>')}
<h3>Dos neuronas resuelven XOR</h3>
<p>Una neurona oculta aprende «¿al menos un interruptor arriba?»; otra, «¿los dos arriba?». La salida enciende la luz si la primera dice sí y la segunda dice no. Dos líneas combinadas hacen lo que una sola no podía. En pocas palabras: <b>XOR = OR, pero no AND</b>.</p>
<table><tr><th>Entrada</th><th>OR (¿al menos uno?)</th><th>AND (¿los dos?)</th><th>Salida: OR y no AND</th></tr>
<tr><td>(0, 0)</td><td>no</td><td>no</td><td>apagada</td></tr>
<tr><td>(0, 1)</td><td>sí</td><td>no</td><td>encendida</td></tr>
<tr><td>(1, 0)</td><td>sí</td><td>no</td><td>encendida</td></tr>
<tr><td>(1, 1)</td><td>sí</td><td>sí</td><td>apagada</td></tr></table>
<p>Esta es una forma de resolverlo. Cuando Keras entrena la red, puede encontrar <b>otra combinación</b> de pesos que también funcione.</p>
<h3>¿Por qué hace falta la activación?</h3>
<p>Una operación <b>lineal</b> solo multiplica y suma. Si multiplicas por 2 y luego por 3, es lo mismo que multiplicar por 6: dos pasos lineales equivalen a uno solo. Por eso apilar capas que solo suman no sirve: toda la torre seguiría dibujando una sola recta. La activación es <b>no lineal</b> (dobla la línea); no lineal no significa aleatorio, solo que no es una recta.</p>
<h3>¿Cuántos números aprende una red?</h3>
{formula(r'\text{parámetros de una capa} = n_{\text{entradas}} \times n_{\text{neuronas}} + n_{\text{neuronas}}',
         read='cada neurona tiene un peso por cada cosa que le llega (entradas × neuronas) y además un sesgo propio (+ neuronas).')}
<table><tr><th>Red</th><th>Cuenta</th><th>Total</th></tr>
<tr><td>2 → 2 → 1 (la de XOR)</td><td>(2·2+2) + (2·1+1) = 6 + 3</td><td><b>9</b></td></tr>
<tr><td>3 → 4 → 1 (la de la lámina)</td><td>(3·4+4) + (4·1+1) = 16 + 5</td><td><b>21</b></td></tr>
<tr><td>2 → 16 → 16 → 1 (las lunas)</td><td>(2·16+16) + (16·16+16) + (16·1+1) = 48 + 272 + 17</td><td><b>337</b></td></tr></table>
{box('analogia', 'Analogía: la consola de sonido', '<p>Cada parámetro es una perilla de una consola de sonido. La red de las lunas tiene 337 perillas; un modelo de lenguaje, cientos de miles de millones. Nadie las gira a mano: <b>entrenar es girar todas las perillas a la vez</b>, un poquito, en la dirección que baja la pérdida.</p>')}
<h3>Parámetros e hiperparámetros</h3>
<p>Los <b>parámetros</b> (pesos y sesgos) los aprende la red. Los <b>hiperparámetros</b> los decides tú antes de entrenar: cuántas capas, cuántas neuronas, la tasa de aprendizaje, el número de épocas. La <b>anchura</b> es cuántas neuronas tiene una capa; la <b>profundidad</b>, cuántas capas hay. Ojo: una capa de 16 neuronas no significa 16 categorías; son 16 pistas intermedias.</p>
{box('curioso', 'Para curiosos: aproximación universal', '<p>Con suficientes neuronas, una sola capa oculta puede aproximar casi cualquier función continua (Cybenko, 1989). En la práctica, varias capas lo logran con muchas menos neuronas: eso es el «deep».</p>')}
<h3>Practica</h3>
{ex('¿Cuántos parámetros tiene una red 3 → 4 → 1?', '<p>\\((3\\cdot4 + 4) + (4\\cdot1 + 1) = 16 + 5 = 21\\).</p>')}
{ex('¿Por qué una red sin funciones de activación, aunque tenga 50 capas, no puede separar XOR?', '<p>Porque una composición de funciones lineales sigue siendo lineal: equivale a una sola neurona, una sola línea.</p>')}
{colab(NB2, '<b>NB02</b>, Parte E: una capa oculta resuelve XOR y las «lunas». Antes de leer la tabla de Keras, intenta contar los parámetros en papel.')}
"""))

S.append(('b06', '06', 'Retropropagación: repartir la culpa', f"""
{idea('Hacia adelante la red predice; hacia atrás reparte la culpa del error entre todos sus pesos; luego cada peso da un paso cuesta abajo.')}
{fig(svg_back(), 'La información viaja hacia adelante; la culpa, hacia atrás.')}
<h3>Ejemplo con números: una red 2 → 2 → 1</h3>
<p>Socio con antigüedad 1.0 y carga de cuota 0.5; <b>sí pagó</b> (\\(y = 1\\)). Pesos ocultos (0.5, −0.3) y (0.2, 0.8), sesgos 0.1 y −0.1; salida (0.7, −0.4), sesgo 0.05; todas con sigmoide.</p>
<p><b>Ida (hacia adelante, <i>forward</i>):</b></p>
<ol><li>Neurona oculta 1: \\(0.5 \\times 1 - 0.3 \\times 0.5 + 0.1 = 0.45\\) → sigmoide → <b>0.6106</b>.</li>
<li>Neurona oculta 2: \\(0.2 \\times 1 + 0.8 \\times 0.5 - 0.1 = 0.5\\) → sigmoide → <b>0.6225</b>.</li>
<li>Salida: \\(0.7 \\times 0.6106 - 0.4 \\times 0.6225 + 0.05 \\approx 0.2284\\) → sigmoide → \\(\\hat y = \\) <b>0.5569</b> (55.69 % de pago).</li>
<li>Pérdida BCE: \\(-\\log 0.5569 \\approx\\) <b>0.5854</b>.</li></ol>
<p><b>Predecir no es aprender:</b> hasta aquí ningún peso cambió. Y aunque 55.69 % ya dice «sí paga» con umbral 0.5, la red sigue entrenando porque la pérdida no es cero: quiere estar <b>más segura</b> de la respuesta correcta.</p>
<p><b>Vuelta (hacia atrás):</b></p>
<ol><li><b>Culpa de la salida:</b> \\(\\delta = \\hat y - y = 0.5569 - 1 = -0.4431\\). Negativa: la predicción se quedó corta.</li>
<li><b>Culpa del peso que viene de la neurona oculta 1:</b> \\(\\delta\\) × lo que entró por ese cable: \\(-0.4431 \\times 0.6106 \\approx -0.2706\\).</li>
<li><b>Culpa de la capa oculta:</b> peso × culpa × pendiente de la sigmoide: \\(-0.07\\) y \\(+0.04\\).</li>
<li><b>Paso</b> con η = 0.5: ese peso pasa de 0.7 a \\(0.7 - 0.5 \\times (-0.2706) = 0.8353\\). Los <b>9 parámetros</b> se actualizan a la vez, todos calculados con el mismo estado de antes.</li>
<li><b>Resultado:</b> la predicción sube de 55.69 % a <b>65.42 %</b> y la pérdida baja de 0.5854 a <b>0.4243</b>.</li></ol>
<p>Aquí «culpa» es solo una palabra cómoda para la <b>derivada</b>: cuánto influye cada peso en la pérdida (su sensibilidad). No es culpa moral.</p>
<h3>¿Qué es la retropropagación?</h3>
<p><b>Retro</b> significa «hacia atrás» y <b>propagación</b>, «ir pasando». La <b>retropropagación</b> (<i>backpropagation</i>) es el método que calcula la derivada de la pérdida respecto a cada peso, empezando por el final y pasando hacia atrás capa por capa. Reutiliza los números de la ida, así que no repite cuentas. Ojo: la retropropagación <b>calcula</b> las derivadas; quien <b>actualiza</b> los pesos es el <b>optimizador</b>.</p>
<h3>Las cuatro reglas</h3>
<table><tr><th>#</th><th>En palabras</th><th>En símbolos</th></tr>
<tr><td>1</td><td>Culpa de la salida = predicción − realidad</td><td>\\(\\delta^{{(L)}} = \\hat y - y\\)</td></tr>
<tr><td>2</td><td>Culpa de una neurona oculta = culpa que le llega por sus pesos × su pendiente</td><td>\\(\\delta^{{(l)}} = (W^{{(l+1)}})^\\top \\delta^{{(l+1)}} \\odot \\varphi'(z^{{(l)}})\\)</td></tr>
<tr><td>3</td><td>Culpa de un peso = culpa de su neurona × lo que entra por ese cable</td><td>\\(\\partial L/\\partial w = \\delta \\cdot a_{{\\text{{entrada}}}}\\)</td></tr>
<tr><td>4</td><td>Actualizar: peso − η × culpa, y repetir</td><td>\\(w \\leftarrow w - \\eta\\, \\partial L/\\partial w\\)</td></tr></table>
<h3>La regla de la cadena: engranajes</h3>
<p>Si A mueve a B tres veces más rápido y B mueve a C seis veces más rápido, A mueve a C <b>18</b> veces más rápido: los efectos se <b>multiplican</b>: \\(3 \\times 6 = 18\\). Eso es la <b>regla de la cadena</b>. En la fórmula de abajo, llamamos \\(u = 3x\\) a lo de adentro y \\(u^2\\) a lo de afuera.</p>
{formula(r'z = (3x)^2:\quad \frac{dz}{dx} = \underbrace{2(3x)}_{\text{por fuera}} \cdot \underbrace{3}_{\text{por dentro}} = 18 \text{ en } x = 1',
         read='dz/dx es «cuánto cambia z si muevo x un poquito». Por dentro, 3x cambia 3 veces más rápido que x; por fuera, elevar al cuadrado cambia 2·(3x) = 6 veces más rápido que lo de adentro (en x = 1). Los dos efectos se multiplican: 6 × 3 = 18.')}
{hist('1986', 'David Rumelhart, Geoffrey Hinton y Ronald Williams publican en <i>Nature</i> cómo entrenar redes de varias capas con retropropagación. La idea tenía antecedentes, pero ese artículo la volvió popular y ayudó a terminar el primer invierno.')}
{box('analogia', 'Analogía: la cadena del cacao', '<p>El cliente dice «¡salió amargo!» (el error se descubre al final). La chocolatería revisa cuánto influyó cada proceso y pasa la culpa hacia el tostado y la cosecha, según cuánto influyeron.</p>')}
{box('ojo', 'TensorFlow lo hace solo', '<p><code>tf.GradientTape</code> «graba» la pasada hacia adelante y la recorre al revés aplicando estas reglas. Nadie hace retropropagación a mano en la vida real; entenderla sirve para <b>depurar</b>.</p>')}
<h3>Practica</h3>
{ex('Otro socio NO pagó (\\(y = 0\\)) y la red dijo \\(\\hat y = 0.53\\). ¿Cuál es la culpa de la salida? ¿Subirá o bajará la predicción tras el paso?', '<p>\\(\\delta = 0.53 - 0 = 0.53\\) (positiva): los pesos se mueven para <b>bajar</b> la predicción. En el NB02 baja a ≈ 0.41.</p>')}
{ex('Una neurona ReLU tuvo \\(z < 0\\). ¿Qué culpa reciben sus pesos con ese ejemplo?', '<p>Cero: la pendiente de ReLU para \\(z<0\\) es 0. Si le pasa con todos los ejemplos, es una «neurona muerta».</p>')}
{ex('¿Cuánto vale la derivada de \\((2x+1)^2\\) en \\(x = 1\\)?', '<p>Por fuera \\(2(2x+1) = 6\\); por dentro 2. Total \\(6\\cdot 2 = 12\\).</p>')}
{colab(NB2, '<b>NB02</b>, Partes A a D: la red 2 → 2 → 1 hacia adelante, la culpa hacia atrás, un paso de aprendizaje y TensorFlow comprobando tu cuenta.')}
"""))

S.append(('b07', '07', 'Entrenar bien: trampas, lotes y optimizadores', f"""
{idea('Entrenar bien es evitar tres trampas, aprender por lotes y elegir un buen optimizador: Adam es la opción segura para empezar.')}
<h3>Antes de entrenar: escalar los datos</h3>
<p>Si un dato va de 0 a 3 (atrasos) y otro de 300 a 5 000 (ingreso), el grande domina las cuentas. <b>Escalar</b> es llevar todos los datos a una medida parecida. La forma más común es <b>estandarizar</b>: restar el promedio y dividir para la desviación estándar.</p>
<p>La <b>desviación estándar</b> mide cuánto se alejan los datos de su promedio, en general. Ejemplo: ingresos con promedio 1 000 y desviación 200. Un ingreso de 1 200 queda en \\((1200 - 1000)/200 = 1\\): una desviación por encima. Uno de 800 queda en −1.</p>
<h3>Inicializar: ¿con qué pesos empezamos?</h3>
<p><b>Inicializar</b> es elegir los pesos del inicio. Si todas las neuronas empiezan iguales, calculan lo mismo y reciben la misma corrección, como estudiantes que copian el mismo cuaderno: nunca se diferencian. Por eso los pesos empiezan <b>al azar</b> (con una escala cuidada). Los sesgos sí pueden empezar en 0.</p>
<h3>Tres trampas y su remedio</h3>
<table><tr><th>Trampa</th><th>Síntoma</th><th>Remedio</th></tr>
<tr><td><b>La señal se apaga</b> (teléfono dañado)</td><td>las primeras capas casi no aprenden</td><td>ReLU en capas ocultas</td></tr>
<tr><td><b>Pesos iniciales malos</b> (clones)</td><td>la red no mejora o explota desde el inicio</td><td>inicialización aleatoria escalada: <code>he_normal</code> con ReLU</td></tr>
<tr><td><b>Paso η equivocado</b> (medio salero)</td><td>la pérdida sube, salta o da NaN</td><td>Adam con learning_rate 0.001; si falla, bajarlo</td></tr></table>
{box('analogia', 'Analogía: el teléfono dañado', '<p>En el juego del teléfono dañado el mensaje se deforma un poco en cada persona; al final de una fila larga ya no queda nada del original. Con la sigmoide pasa algo parecido: en cada capa la culpa se multiplica por 0.25 como máximo y a las primeras capas casi no llega. Con solo 5 capas: \\(0.25^5 \\approx 0.001\\). A esto se le llama <b>desvanecimiento del gradiente</b>. ReLU tiene derivada 1 para valores positivos, así que deja pasar la culpa entera cuando la neurona está activa. Ayuda mucho, pero no es magia: una neurona ReLU con z negativo no deja pasar nada.</p>')}
{hist('2010', 'Vinod Nair y Geoffrey Hinton muestran las ventajas de ReLU, y Xavier Glorot y Yoshua Bengio explican cómo iniciar los pesos al azar con la escala correcta: la inicialización Glorot que Keras usa por defecto.')}
{box('curioso', 'Para curiosos: por qué se apaga la señal', '<p>La pendiente máxima de la sigmoide es 0.25. Al retropropagar por 10 capas, la culpa se multiplica por números ≤ 0.25: \\(0.25^{10} \\approx 10^{-6}\\). ReLU tiene pendiente 1 cuando está activa.</p>')}
<h3>Aprender por lotes: censo o encuesta</h3>
<p>Un <b>lote</b> (<i>batch</i>) es un grupo pequeño de ejemplos con el que se da un paso de aprendizaje. Con 100 ejemplos y lotes de 20, una <b>época</b> (una vuelta por todos los datos) tiene 100 ÷ 20 = <b>5 actualizaciones</b>. Más épocas no crean datos nuevos: la red vuelve a mirar los mismos ejemplos.</p>
<p>No usamos los 4 800 socios en cada paso: tomamos un <b>lote</b> de 32 al azar, promediamos su culpa y damos un paso. Como el INEC, que no hace un censo cada mes: una encuesta bien hecha basta.</p>
{formula(r'\text{pasos por época} = \frac{N}{\text{batch\_size}} = \frac{4800}{32} = 150',
         read='una época es una vuelta por todos los datos. Si en cada paso usamos un lote de 32 socios, una vuelta por los 4 800 socios toma 4 800 ÷ 32 = 150 pasos.')}
<h3>Tres formas de bajar la montaña</h3>
<p>El <b>optimizador</b> es la regla que usa el gradiente para cambiar los pesos. <b>SGD</b> da un paso que depende solo del gradiente de ahora. <b>Momentum</b> recuerda los pasos anteriores, como una pelota que rueda con impulso. <b>Adam</b> adapta el tamaño del paso para cada parámetro por separado; aun así, sigue necesitando una tasa de aprendizaje. Para compararlos de forma <b>justa</b> hay que usar los mismos datos, la misma red, los mismos pesos iniciales y el mismo número de pasos.</p>
<table><tr><th>Optimizador</th><th>Idea</th><th>Analogía</th></tr>
<tr><td>SGD</td><td>pasos fijos en la dirección de la pendiente</td><td>el caminante</td></tr>
<tr><td>Momentum</td><td>acumula impulso: acelera en las rectas, zigzaguea menos</td><td>la bicicleta en bajada</td></tr>
<tr><td>Adam</td><td>ajusta el paso de cada peso por separado</td><td>el guía con experiencia</td></tr></table>
{hist('1964 · 2014', 'Boris Polyak propone el momentum («el método de la bola pesada») en 1964. Diederik Kingma y Jimmy Ba publican Adam en 2014; hoy es el optimizador por defecto en muchos proyectos. La lectura de tendencia de la semana discute si los optimizadores nuevos, como Muon, cambian esa historia.')}
{box('ojo', 'La receta para arrancar', '<ol><li>Escala los datos (<code>StandardScaler</code>, ajustado solo con entrenamiento).</li><li>Capas ocultas ReLU con <code>he_normal</code>; empieza con 1 o 2.</li><li>Salida según la pregunta: sí/no → 1 neurona sigmoide + BCE.</li><li>Adam con learning_rate 0.001.</li><li>batch_size 32; mira las curvas de entrenamiento y validación.</li><li>Si la pérdida sube o da NaN: baja el learning_rate.</li></ol>')}
<h3>Practica</h3>
{ex('Con 4 800 ejemplos y batch_size = 64, ¿cuántos pasos tiene una época? ¿Y 30 épocas?', '<p>4 800 ÷ 64 = 75 pasos por época; 30 épocas = 2 250 pasos.</p>')}
{ex('¿Por qué no conviene iniciar todos los pesos en cero?', '<p>Todas las neuronas de la capa calcularían lo mismo y recibirían la misma culpa: quedarían clones para siempre.</p>')}
{colab(NB2, '<b>NB02</b>, Parte G (en casa): lee la comparación de las curvas de SGD, Momentum y Adam en el mismo problema.')}
"""))

S.append(('b08', '08', 'Keras desde cero: construir, compilar, entrenar', f"""
{idea('TensorFlow hace las cuentas; Keras es la forma corta de pedírselas. Con tres pasos (construir, compilar, entrenar) Keras repite por ti el ciclo adelante → atrás → actualizar, lote a lote y época a época.')}
<h3>Aprender no es memorizar</h3>
<p>Un estudiante puede memorizar la hoja de práctica y sacar 100 en ella sin entender nada; en el examen con preguntas nuevas, falla. A una red le pasa igual. <b>Generalizar</b> es acertar con datos nuevos. <b>Sobreajustar</b> es memorizar los datos de entrenamiento y fallar con los nuevos.</p>
<p>Por eso los datos se dividen en tres grupos con trabajos distintos:</p>
<table><tr><th>Grupo</th><th>Para qué sirve</th><th>Como en el colegio</th></tr>
<tr><td><b>Entrenamiento</b></td><td>ajustar los pesos</td><td>estudiar</td></tr>
<tr><td><b>Validación</b></td><td>decidir y vigilar durante el entrenamiento</td><td>el simulacro</td></tr>
<tr><td><b>Prueba</b></td><td>medir una sola vez, al final</td><td>el examen final</td></tr></table>
<p><b>Los números del NB02:</b> 600 puntos → 120 para prueba y 480 para entrenar. De esos 480, 96 van a validación y <b>384 ajustan los pesos</b>. Con lotes de 32: 384 ÷ 32 = <b>12 pasos por época</b>; 60 épocas = <b>720 pasos</b>.</p>
<p><b>Cómo leer las curvas:</b> si las pérdidas de entrenamiento y de validación bajan juntas, vamos bien. Si la de validación sube mientras la de entrenamiento sigue bajando, la red está memorizando.</p>
{box('error', 'Fuga de información', '<p>Al escalar, el promedio y la desviación se calculan <b>solo con los datos de entrenamiento</b>, y luego se aplican a validación y prueba. Si los calculas con todo, la prueba «se filtra» al entrenamiento y el resultado final deja de ser honesto.</p>')}
<h3>Las palabras de Colab y Python</h3>
<table><tr><th>Palabra</th><th>Qué es</th></tr>
<tr><td><b>Colab</b></td><td>un cuaderno de Python en el navegador, de Google; no hay que instalar nada</td></tr>
<tr><td><b>Celda</b></td><td>un bloque de código o de texto que se ejecuta por separado. <b>El orden importa</b>: ejecútalas de arriba hacia abajo</td></tr>
<tr><td><b>Variable</b></td><td>un nombre que guarda un valor: <code>s1 = 80</code></td></tr>
<tr><td><b>Lista</b></td><td>varios valores en orden: <code>[80, 70, 90]</code></td></tr>
<tr><td><b>Función</b></td><td>un bloque con nombre que recibe datos y devuelve un resultado</td></tr>
<tr><td><b><code>print</code></b></td><td>muestra un valor en pantalla</td></tr>
<tr><td><b>Librería</b> e <b><code>import</code></b></td><td>una librería es código ya escrito por otros; <code>import</code> la trae a tu cuaderno</td></tr></table>
<h3>¿Qué son TensorFlow y Keras?</h3>
<p><b>TensorFlow</b> es una librería de Python que Google liberó como código abierto en noviembre de 2015. Hace las cuentas pesadas de una red (multiplicar tablas enormes de números, en el procesador o en la tarjeta gráfica) y calcula sola las pendientes de la retropropagación.</p>
<p><b>Keras</b> es una librería que François Chollet publicó en marzo de 2015 para describir y entrenar redes en pocas líneas. Hoy va por <b>Keras 3</b>, que puede funcionar sobre TensorFlow, JAX o PyTorch; en el curso la usamos sobre TensorFlow.</p>
{box('analogia', 'Analogía: el motor y el volante', '<p>TensorFlow es el <b>motor</b> del carro: potente y lleno de piezas. Keras es el <b>volante y los pedales</b>: no necesitas abrir el capó para manejar. Cuando algo falla (la pérdida no baja), saber cómo funciona el motor, la retropropagación del bloque 06, te ayuda a encontrar el problema.</p>')}
{hist('2015', 'En marzo François Chollet publica Keras, y en noviembre Google libera TensorFlow como código abierto. Las dos librerías de esta página tienen apenas diez años.')}
<h3>Importar las librerías</h3>
<p>En Google Colab ya vienen instaladas: no hay que instalar nada, solo importarlas al inicio del notebook.</p>
<pre><code>import numpy as np               # arrays: tables of numbers
import tensorflow as tf          # the engine: math and gradients
import keras                     # the steering wheel: build and train networks
print(tf.__version__, keras.__version__)   # check the versions</code></pre>
<p class="read"><b>Léelo así:</b> <code>import tensorflow as tf</code> significa «trae la librería TensorFlow y llámala <code>tf</code> en este notebook». Los apodos son una convención: todo el mundo escribe <code>np</code>, <code>tf</code> y <code>keras</code>.</p>
<h3>Los datos: arrays de NumPy y su forma</h3>
<p>Una red no recibe una hoja de Excel: recibe un <b>array</b> de NumPy, una tabla de números. Cada <b>fila</b> es un ejemplo (un socio) y cada <b>columna</b> es un dato (antigüedad, carga de la cuota). Las respuestas van en otro array, una por fila.</p>
<pre><code>X = np.array([[1.0, 0.5],    # member 1: seniority, installment load
              [0.2, 0.9],    # member 2
              [0.7, 0.1]])   # member 3
y = np.array([1, 0, 1])      # 1 = paid, 0 = did not pay
print(X.shape)               # (3, 2): 3 rows (members), 2 columns (data)
print(y.shape)               # (3,): one answer per member</code></pre>
<p class="read"><b>Léelo así:</b> <code>X.shape</code> es la forma de la tabla: <code>(3, 2)</code> se lee «3 filas por 2 columnas». En el NB02, las lunas son 600 puntos con 2 datos cada uno; después de apartar el 20 % para la prueba, <code>X_train.shape</code> es <code>(480, 2)</code> y <code>y_train.shape</code> es <code>(480,)</code>: una etiqueta por fila.</p>
<p>Un <b>vector</b> es una lista de números (una fila); una <b>matriz</b> es una tabla (filas y columnas). En NumPy, <code>@</code> hace el producto punto o de matrices (multiplica parejas y suma), mientras que <code>*</code> solo multiplica elemento por elemento, sin sumar.</p>
<p>En TensorFlow, las tablas de números se llaman <b>tensores</b>. Un <code>tf.Variable</code> es un tensor que puede cambiar: ahí se guardan los pesos. <code>tf.GradientTape</code> «graba» las cuentas y luego calcula las derivadas solo: eso se llama <b>diferenciación automática</b>.</p>
<p><b>Las lunas</b> son puntos inventados por la computadora (<code>make_moons</code>) que forman dos medias lunas entrelazadas: ninguna recta las separa. El <b>ruido</b> los desordena un poco para que se parezcan a datos reales, y la <b>semilla</b> (<i>seed</i>) hace que el azar salga igual cada vez que ejecutas.</p>
<h3>Paso 1 · Construir: apilar capas</h3>
<pre><code>model = keras.Sequential([
    keras.Input(shape=(2,)),                      # each example has 2 data
    keras.layers.Dense(16, activation="relu"),    # hidden layer: 16 neurons
    keras.layers.Dense(16, activation="relu"),    # another hidden layer
    keras.layers.Dense(1, activation="sigmoid"),  # output: a probability
])
model.summary()                                   # 337 parameters</code></pre>
<table class="codeexp"><tr><th>Línea</th><th>Qué hace</th></tr>
<tr><td><code>keras.Sequential([...])</code></td><td>Una red donde las capas van una detrás de otra, en el orden de la lista.</td></tr>
<tr><td><code>keras.Input(shape=(2,))</code></td><td>Le dice a la red cuántos datos trae cada ejemplo: 2 <b>características</b>, las columnas de X (no 2 ejemplos). No tiene neuronas ni pesos.</td></tr>
<tr><td><code>Dense(16, activation="relu")</code></td><td>Una capa de 16 neuronas, cada una conectada con todo lo de la capa anterior (por eso «densa»). Cada neurona hace la cuenta del viernes y pasa el resultado por ReLU.</td></tr>
<tr><td><code>Dense(1, activation="sigmoid")</code></td><td>La salida: una sola neurona con sigmoide, que da la probabilidad de «sí».</td></tr>
<tr><td><code>model.summary()</code></td><td>Imprime una tabla con cada capa, la forma de lo que sale de ella y cuántos parámetros tiene.</td></tr></table>
{box('analogia', 'Analogía: piezas de LEGO', '<p><code>Sequential</code> es la base de LEGO y cada <code>Dense</code> es una pieza que apilas encima. Cambiar la red es quitar o poner piezas: más neuronas en una capa (16 → 32) o una capa más.</p>')}
<p><b>¿De dónde salen los 337 parámetros?</b> Con la regla del bloque 05 (entradas × neuronas + neuronas):</p>
<table><tr><th>Capa</th><th>Cuenta</th><th>Parámetros</th></tr>
<tr><td>Dense(16) · recibe 2 datos</td><td>2·16 + 16</td><td>48</td></tr>
<tr><td>Dense(16) · recibe 16</td><td>16·16 + 16</td><td>272</td></tr>
<tr><td>Dense(1) · recibe 16</td><td>16·1 + 1</td><td>17</td></tr>
<tr><th>Total</th><th></th><th>337</th></tr></table>
<h3>Paso 2 · Compilar: decidir cómo va a aprender</h3>
<pre><code>model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),  # how to take each step
              loss="binary_crossentropy",     # what to minimize (the BCE)
              metrics=["accuracy"])           # what to report while training</code></pre>
<p class="read"><b>Léelo así:</b> compilar no entrena nada: deja configuradas tres decisiones. El <b>optimizador</b> decide cómo dar cada paso cuesta abajo (Adam, el del bloque 07, con learning_rate = 0.01 como en el NB02; si escribes solo <code>"adam"</code>, usa 0.001). La <b>pérdida</b> es lo que se quiere bajar: la BCE del viernes, porque la respuesta es sí o no. Las <b>métricas</b> solo se reportan para que tú las veas: la red aprende bajando la <b>pérdida</b>, no la métrica; la exactitud sirve aquí, pero en el bloque 09 verás cuándo engaña.</p>
<p>Si quieres otro tamaño de paso, cambia el número: <code>Adam(learning_rate=0.001)</code> da pasos más cortos.</p>
<h3>Paso 3 · Entrenar: fit</h3>
<pre><code>history = model.fit(X_train, y_train,
                    epochs=60,              # 60 full passes over the data
                    batch_size=32,          # one step every 32 examples
                    validation_split=0.2)   # keep 20 % aside to check</code></pre>
<table class="codeexp"><tr><th>Argumento</th><th>Qué significa</th></tr>
<tr><td><code>epochs=60</code></td><td>60 vueltas completas por los datos de entrenamiento.</td></tr>
<tr><td><code>batch_size=32</code></td><td>En cada paso usa un lote de 32 ejemplos: la encuesta, no el censo.</td></tr>
<tr><td><code>validation_split=0.2</code></td><td>Aparta el <b>último</b> 20 % de las filas de entrenamiento (sin mezclar ni equilibrar clases): la red no aprende de ellas, solo se usan para medir. De 480 filas quedan 96 para validar y 384 para ajustar los pesos.</td></tr>
<tr><td><code>history</code></td><td>Lo que devuelve <code>fit</code>: guarda la pérdida y la exactitud de cada época en <code>history.history</code>.</td></tr></table>
{box('analogia', 'Analogía: el simulacro de examen', '<p>Los datos de validación son un simulacro con preguntas que el estudiante no ha visto. Si solo practicara con las mismas preguntas, podría memorizarlas y sacar 100 sin entender nada. El simulacro dice si de verdad aprendió.</p>')}
<pre><code>import matplotlib.pyplot as plt
plt.plot(history.history["loss"], label="training")       # loss on the data it learns from
plt.plot(history.history["val_loss"], label="validation") # loss on the practice exam
plt.xlabel("epoch"); plt.ylabel("loss"); plt.legend(); plt.show()</code></pre>
{box('ojo', 'Lee las curvas', '<p>Si la pérdida de <b>entrenamiento</b> baja y la de <b>validación</b> también, vas bien. Si la de validación empieza a subir mientras la de entrenamiento sigue bajando, la red está memorizando (sobreajuste): lo veremos en la semana 3.</p>')}
<h3>Usar el modelo: predict y evaluate</h3>
<pre><code>p = model.predict(X_new)                     # probabilities, shape (n, 1)
decision = (p > 0.5).astype(int)             # 1 = yes, 0 = no, threshold 0.5
loss, acc = model.evaluate(X_test, y_test)   # loss and accuracy on unseen data</code></pre>
<p class="read"><b>Léelo así:</b> <code>predict</code> devuelve, para cada fila, la probabilidad que da la sigmoide de salida. Para decidir se compara con un <b>umbral</b> (0.5 por defecto; en el bloque 09 verás por qué a veces conviene otro). <code>evaluate</code> mide la pérdida y la métrica con datos que la red no usó para entrenar. Ni <code>predict</code> ni <code>evaluate</code> cambian los pesos: solo <code>fit</code> entrena. Si <code>predict</code> da 0.8, con umbral 0.5 la decisión es clase 1. En el NB02 la red llega a cerca de 95 % en prueba; tómalo como referencia de una ejecución, no como un número exacto.</p>
<table><tr><th>Paso</th><th>Qué decides</th><th>Lo que ya sabes</th></tr>
<tr><td>Construir</td><td>capas, neuronas y activaciones</td><td>bloques 02 y 05</td></tr>
<tr><td>Compilar</td><td>optimizador, pérdida y métrica</td><td>bloques 04 y 07</td></tr>
<tr><td>Entrenar</td><td>épocas, tamaño del lote y validación</td><td>bloques 06 y 07</td></tr></table>
<h3>Practica</h3>
{ex('¿Qué forma tiene X si tienes 1 200 socios con 6 datos cada uno? ¿Qué pones en <code>keras.Input</code>?', '<p><code>X.shape == (1200, 6)</code>: 1 200 filas y 6 columnas. En la red: <code>keras.Input(shape=(6,))</code>, porque cada ejemplo trae 6 datos.</p>')}
{ex('Escribe una red para datos con 10 columnas: dos capas de 8 con ReLU y una salida sigmoide. ¿Cuántos parámetros debe mostrar <code>summary()</code>?', '<pre><code>model = keras.Sequential([keras.Input(shape=(10,)),\n    keras.layers.Dense(8, activation="relu"),\n    keras.layers.Dense(8, activation="relu"),\n    keras.layers.Dense(1, activation="sigmoid")])</code></pre><p>(10·8 + 8) + (8·8 + 8) + (8 + 1) = 88 + 72 + 9 = 169 parámetros.</p>')}
{ex('<code>model.predict</code> devuelve 0.82, 0.31 y 0.64 para tres socios. Con umbral 0.5, ¿qué decide para cada uno?', '<p>Sí, no y sí: 0.82 y 0.64 superan 0.5; 0.31 no.</p>')}
{ex('Una red sin capas ocultas logra 49 % en los círculos del NB02. ¿Por qué?', '<p>Sin capas ocultas es una sola neurona: traza una línea, y ninguna línea separa un círculo de su anillo. Es como adivinar.</p>')}
{colab(NB2, '<b>NB02</b>, Partes E y F: lee cómo Keras resuelve XOR y las lunas, línea por línea. Al final, un experimento opcional: cambia la red de los círculos y mira si supera el 90 %.')}
"""))

S.append(('b09', '09', '¿El modelo es bueno? Cuando la exactitud engaña', f"""
{idea('Cuando los casos que buscas son pocos, la exactitud engaña: mira cuántos casos encuentra el modelo (recall), cuántas de sus alarmas son ciertas (precisión) y qué tan bien ordena el riesgo (AUC).')}
<h3>El ejemplo de clase</h3>
<p>Una cooperativa (ficticia) quiere encontrar a los socios que caerán en <b>mora</b>. De cada 100 socios, solo 13 caen. Un «modelo» perezoso que dice siempre «está al día» acierta 87 de 100… y no encuentra a ninguno de los 13. En las slides (lámina «87 % de exactitud puede no valer nada») puedes mover el umbral de una red de verdad y ver cómo cambian los aciertos y las falsas alarmas.</p>
{box('ojo', 'Cambia la clase positiva', '<p>Hasta ahora, «1» era «sí pagó». Aquí cambiamos: la clase <b>positiva</b> es <b>mora</b>, porque es lo que queremos encontrar. «Positivo» no significa bueno; es como en una prueba médica: positivo = se encontró lo que se buscaba.</p>')}
<p>Cuando una clase es mucho más rara que la otra (13 contra 87), decimos que las clases están <b>desbalanceadas</b>.</p>
<h3>La matriz de confusión: cuatro resultados posibles</h3>
<table><tr><th></th><th>El modelo dice «mora»</th><th>El modelo dice «al día»</th></tr>
<tr><th>De verdad cayó en mora</th><td><b>VP</b> verdadero positivo: <b>10</b></td><td><b>FN</b> falso negativo: <b>3</b></td></tr>
<tr><th>De verdad está al día</th><td><b>FP</b> falso positivo: <b>8</b></td><td><b>VN</b> verdadero negativo: <b>79</b></td></tr></table>
<p><b>VP:</b> alarma correcta. <b>FN:</b> un moroso que se escapó. <b>FP:</b> falsa alarma. <b>VN:</b> un cumplido bien reconocido. Con esos números:</p>
<ul><li><b>Exactitud</b> = aciertos ÷ total = \\((10 + 79)/100 =\\) <b>89 %</b>.</li>
<li><b>Recall</b> (o sensibilidad) = VP ÷ casos reales de mora = \\(10/13 \\approx\\) <b>76.9 %</b>. El denominador son los morosos reales.</li>
<li><b>Precisión</b> = VP ÷ alarmas = \\(10/18 \\approx\\) <b>55.6 %</b>. Ojo: en español «exactitud» y «precisión» suenan parecido, pero aquí son métricas distintas.</li></ul>
<h3>El umbral y el costo de cada error</h3>
<p>Si bajas el umbral, el modelo da más alarmas: encuentra más morosos (sube el recall), pero también molesta a más cumplidos (baja la precisión). ¿Qué conviene? Depende del costo: si la alarma solo envía un recordatorio amable, una falsa alarma cuesta poco; si significa negar un servicio, cuesta mucho.</p>
<p>El <b>AUC</b> no mira un umbral: mide qué tan bien el modelo <b>ordena el riesgo</b>. 1 es perfecto; 0.5 es como lanzar una moneda (y no significa 50 % de exactitud). La <b>calibración</b>, en una línea: un modelo está calibrado si, cuando dice 30 %, de verdad pasa cerca de 30 de cada 100 veces.</p>
<h3>Métricas en palabras sencillas</h3>
<table><tr><th>Métrica</th><th>Pregunta que responde</th></tr>
<tr><td>Exactitud (accuracy)</td><td>¿qué porcentaje acertó en total? Engaña: decir siempre «no mora» ya da 87 %.</td></tr>
<tr><td>Recall (detecta)</td><td>de los morosos reales, ¿qué porcentaje encontró?</td></tr>
<tr><td>Precisión</td><td>de los que marcó como riesgo, ¿qué porcentaje era moroso de verdad?</td></tr>
<tr><td>ROC-AUC</td><td>si tomo un moroso y un cumplido al azar, ¿con qué probabilidad el modelo le da más riesgo al moroso? 0.5 = moneda al aire, 1 = perfecto.</td></tr></table>
{box('analogia', 'Analogía: la alarma de humo que nunca suena', '<p>Una alarma de humo que nunca suena «acierta» el 99 % de los días en una casa donde casi nunca hay fuego, y no sirve para nada. Una muy sensible suena con cada tostada (muchas falsas alarmas). El <b>umbral</b> decide el punto medio, y depende de qué cuesta más: una falsa alarma o un incendio que no viste.</p>')}
{hist('1940s', 'La curva ROC, de donde sale el AUC, nació con el radar en la Segunda Guerra Mundial: había que distinguir un avión enemigo del ruido sin dar demasiadas falsas alarmas. Por eso su nombre en inglés habla de un «receptor».')}
{box('error', 'Errores comunes', '<ul><li>Reportar solo la exactitud con clases desbalanceadas.</li><li>Dejar el umbral en 0.5 sin pensar en el costo de cada error.</li><li>Elegir el umbral mirando los datos de prueba: se elige con validación.</li></ul>')}
<h3>Practica</h3>
{ex('En un grupo de 1 000 compras con tarjeta hay 20 fraudes. ¿Qué exactitud logra el modelo que siempre dice «no es fraude»? ¿Y qué recall?', '<p>Exactitud: 980 ÷ 1 000 = 98 %. Recall: 0 %, no encuentra ningún fraude.</p>')}
{ex('Un modelo marca 50 socios como riesgo y 30 de ellos caen en mora. ¿Cuál es su precisión?', '<p>30 ÷ 50 = 60 %: 6 de cada 10 alarmas eran ciertas.</p>')}
{ex('¿Por qué el umbral de decisión se elige con validación y no con prueba?', '<p>Porque elegir algo mirando la prueba la convierte en parte del entrenamiento: el resultado final dejaría de ser una medida honesta.</p>')}
"""))

FORMULAS = r"""
<table>
<tr><th>Qué</th><th>Fórmula</th><th>En palabras</th></tr>
<tr><td>Nota final (ejemplo)</td><td>\(0.2667\,S_1 + 0.2667\,S_2 + 0.2667\,S_3 + 0.20\,F\)</td><td>cada nota por lo que pesa, y se suma</td></tr>
<tr><td>Neurona</td><td>\(z = \mathbf{w}\cdot\mathbf{x} + b,\ a = \varphi(z)\)</td><td>multiplica, suma y decide</td></tr>
<tr><td>Sigmoide</td><td>\(\sigma(z) = 1/(1+e^{-z})\)</td><td>puntaje → probabilidad</td></tr>
<tr><td>ReLU</td><td>\(\max(0, z)\)</td><td>apaga lo negativo</td></tr>
<tr><td>Frontera</td><td>\(w_1x_1 + w_2x_2 + b = 0\)</td><td>la línea donde duda</td></tr>
<tr><td>Perceptrón</td><td>\(\mathbf{w} \leftarrow \mathbf{w} + \eta\,y\,\mathbf{x}\)</td><td>corrige solo si se equivoca</td></tr>
<tr><td>Error de un caso</td><td>\(y - \hat y\)</td><td>real − predicho</td></tr>
<tr><td>MSE</td><td>\(\frac{1}{N}\sum (y-\hat y)^2\)</td><td>promedio de errores al cuadrado</td></tr>
<tr><td>BCE</td><td>\(-[y\log\hat y + (1-y)\log(1-\hat y)]\)</td><td>castiga la falsa seguridad</td></tr>
<tr><td>Gradiente</td><td>\(w \leftarrow w - \eta\,\partial L/\partial w\)</td><td>un paso cuesta abajo</td></tr>
<tr><td>Capa</td><td>\(\mathbf{a}^{(l)} = \varphi(W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)})\)</td><td>muchas neuronas a la vez</td></tr>
<tr><td>Culpa de salida</td><td>\(\delta = \hat y - y\)</td><td>predicción − realidad</td></tr>
<tr><td>Parámetros</td><td>\(n_{in}\cdot n_{out} + n_{out}\)</td><td>pesos + sesgos por capa</td></tr>
<tr><td>Pasos por época</td><td>\(N / \text{batch}\)</td><td>lotes por vuelta</td></tr>
<tr><td>Estandarizar</td><td>\((x - \text{promedio})/\text{desviación}\)</td><td>todos los datos en una escala parecida</td></tr>
<tr><td>Recall</td><td>\(VP/(VP+FN)\)</td><td>de los casos reales, cuántos encontró</td></tr>
<tr><td>Precisión</td><td>\(VP/(VP+FP)\)</td><td>de las alarmas, cuántas eran ciertas</td></tr>
</table>"""
S.append(('formulas', 'Σ', 'Fórmulas de bolsillo', FORMULAS))

GLOS = [
    ("Activación", "Función que convierte el puntaje z en la salida de la neurona (escalón, sigmoide, ReLU)."),
    ("Adam", "Optimizador que ajusta el tamaño del paso de cada peso por separado; buena opción por defecto."),
    ("Batch (lote)", "Grupo de ejemplos con el que se calcula un paso de aprendizaje; batch_size es su tamaño."),
    ("compile / fit / predict", "En Keras: compile elige optimizador, pérdida y métricas; fit entrena; predict da probabilidades para datos nuevos."),
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
    ("Keras", "Librería de Python para construir y entrenar redes en pocas líneas (François Chollet, 2015; hoy Keras 3). El volante; TensorFlow es el motor."),
    ("History", "Lo que devuelve model.fit: la pérdida y las métricas de cada época, para graficar las curvas."),
    ("Learning rate (η)", "Tamaño del paso en el descenso de gradiente."),
    ("Línea base", "Modelo sencillo con el que se compara: si la red no lo supera, no vale la pena."),
    ("Machine learning", "Aprender patrones a partir de ejemplos con su respuesta, en vez de escribir reglas."),
    ("MLP (perceptrón multicapa)", "Red de neuronas organizadas en capas completamente conectadas."),
    ("Momentum", "Optimizador que acumula impulso, como una bicicleta en bajada."),
    ("MSE", "Error cuadrático medio: promedio de los errores al cuadrado; para predecir números."),
    ("NumPy (array)", "Librería de Python para tablas de números; un array tiene una forma (shape): filas = ejemplos, columnas = datos."),
    ("Parámetros", "Los números que la red aprende: pesos y sesgos."),
    ("Perceptrón", "La neurona de Rosenblatt (1958) que aprende corrigiendo sus errores."),
    ("Pérdida", "Un solo número que mide qué tan mal predice el modelo; entrenar es bajarla."),
    ("Peso", "Cuánto importa un dato para la neurona; puede ser positivo o negativo."),
    ("Recall", "De los casos positivos reales, qué porcentaje encontró el modelo."),
    ("ReLU", "Activación máx(0, z); la más usada en capas ocultas."),
    ("Retropropagación", "Algoritmo que reparte la culpa del error hacia atrás con la regla de la cadena."),
    ("ROC-AUC", "Probabilidad de que el modelo le dé más riesgo a un positivo que a un negativo al azar."),
    ("Sequential, Dense", "En Keras: Sequential apila capas en orden; Dense es una capa de neuronas conectadas con todo lo anterior."),
    ("Sesgo (b)", "Número que sube o baja la exigencia de la neurona; mueve la frontera. En la nota final, −70 si se aprobara con 70."),
    ("Sigmoide", "Activación con forma de S que da un número entre 0 y 1."),
    ("Sobreajuste", "Cuando la red memoriza el entrenamiento y empeora en datos nuevos."),
    ("TensorFlow", "Librería de Google (código abierto desde 2015) que hace las cuentas de las redes y calcula los gradientes automáticamente (GradientTape)."),
    ("Umbral", "Probabilidad a partir de la cual el modelo dice «sí»; 0.5 por defecto, pero se elige según el costo de cada error."),
    ("Validación", "Datos apartados para decidir (arquitectura, umbral) sin tocar la prueba."),
    ("XOR", "«Uno u otro, pero no ambos»; no se separa con una sola línea."),
    ("Dato (característica)", "Un número que describe algo del ejemplo, como el ingreso de un socio; es una columna de la tabla."),
    ("Ejemplo", "Un caso completo con todos sus datos; es una fila de la tabla."),
    ("Etiqueta", "La respuesta correcta conocida de un ejemplo (pagó o no). No es lo mismo que la predicción."),
    ("Predicción", "La respuesta que da el modelo; entrenar es hacer que se parezca a la etiqueta."),
    ("Modelo", "La fórmula con perillas (parámetros) que aprende de los ejemplos."),
    ("Clasificación", "Pregunta cuya respuesta es una clase; binaria si solo hay dos (paga / no paga)."),
    ("Regresión", "Pregunta cuya respuesta es una cantidad (el precio de una casa); no significa retroceder."),
    ("Supervisado", "Aprendizaje con ejemplos que traen su etiqueta, como estudiar con un solucionario."),
    ("Derivada", "Cuánto cambia la pérdida, y en qué dirección, si se mueve un poquito una perilla."),
    ("Hiperparámetros", "Lo que decides tú antes de entrenar: capas, neuronas, tasa de aprendizaje, épocas."),
    ("Generalización", "Acertar con datos nuevos, no solo con los de entrenamiento."),
    ("Matriz de confusión", "Tabla con los cuatro resultados posibles: VP, FP, FN y VN."),
    ("Precisión", "De las alarmas del modelo, qué porcentaje era cierto. No es lo mismo que exactitud."),
    ("Calibración", "Un modelo calibrado que dice 30 % acierta cerca de 30 de cada 100 veces."),
    ("Estandarizar", "Restar el promedio y dividir para la desviación estándar, para que los datos tengan una escala parecida."),
    ("Tensor", "Tabla de números en TensorFlow; tf.Variable es un tensor que puede cambiar (los pesos)."),
    ("Celda", "Bloque de código o texto de Colab que se ejecuta por separado; el orden importa."),
    ("Error (de un caso)", "Valor real menos valor predicho en un solo ejemplo."),
    ("Optimizador", "La regla que usa el gradiente para actualizar los pesos (SGD, Momentum, Adam)."),
    ("Prueba", "Datos guardados para medir una sola vez, al final, como el examen final."),
]
import unicodedata as _u
GLOS.sort(key=lambda t: _u.normalize('NFD', t[0]).encode('ascii', 'ignore').decode().lower())
S.append(('glosario', 'A–Z', 'Glosario', '<input id="search" class="search" type="search" placeholder="Buscar una palabra…" aria-label="Buscar en el glosario"><dl class="glos">' +
          ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS) + '</dl>'))

S.append(('cierre', '✓', '¿Listo? Comprueba lo que aprendiste', """
<p>Juega el quiz final: 10 preguntas cortas, sin cuentas, 25 segundos cada una. Al terminar te dice tu puntaje, qué temas repasar (con enlace a esta guía) y tu avance frente al pre-quiz.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?final">Jugar el quiz final</a><a class="btn ghost" href="../index.html">Volver al inicio</a></div>
<h3>La historia completa en un minuto</h3>
<p class="read">Hay tareas para las que es difícil escribir todas las reglas. En lugar de hacerlo, mostramos ejemplos con sus respuestas. Construimos un modelo que combina datos: los pesos controlan cuánto aporta cada uno y el sesgo añade un ajuste al puntaje. La activación transforma ese puntaje en una salida.</p>
<p class="read">Una sola neurona tiene límites. Al conectar varias en capas, podemos construir respuestas más complejas. Para aprender, comparamos la predicción con la respuesta correcta mediante una pérdida. Las derivadas indican cómo afectaría cada pequeño cambio a esa pérdida; la retropropagación permite calcularlas para toda la red. El optimizador usa esa información para ajustar los pesos y sesgos.</p>
<p class="read">Repetimos ese proceso con grupos de ejemplos. Keras automatiza las cuentas. Al final comprobamos si lo aprendido funciona con datos reservados y si los errores son aceptables para el problema. Un porcentaje alto no basta por sí solo.</p>
<h3>Preguntas rápidas</h3>
""" + ''.join(ex(q, f'<p>{r}</p>') for q, r in [
    ('¿Qué es un peso?', 'Un número que multiplica un dato y controla cuánto aporta.'),
    ('¿Qué es un sesgo?', 'Un número adicional que desplaza el puntaje, incluso si todas las entradas valen cero.'),
    ('¿Qué es una activación?', 'Una regla que convierte el puntaje en la salida de la neurona.'),
    ('¿Qué cambia al entrenar?', 'Los pesos y los sesgos.'),
    ('¿Qué es una época? ¿Y un lote?', 'Una época es una vuelta por todos los ejemplos de entrenamiento. Un lote es el grupo de ejemplos que se usa en una actualización.'),
    ('¿Pérdida y gradiente son lo mismo?', 'No. La pérdida mide qué tan mal vamos; el gradiente dice cómo cambia esa pérdida al mover cada parámetro.'),
    ('¿Retropropagación y optimizador son lo mismo?', 'No. La retropropagación calcula las derivadas; el optimizador las usa para actualizar los pesos.'),
    ('¿Por qué falla XOR con una neurona?', 'Porque no existe una recta que separe sus clases con las dos entradas originales.'),
    ('¿Más neuronas garantizan el éxito?', 'No: también influyen los datos y el entrenamiento.'),
    ('¿Predecir sigue entrenando?', 'No: <code>predict</code> y <code>evaluate</code> no cambian los pesos; solo <code>fit</code> entrena.'),
]) + """
<p>En Canvas te esperan el test de la semana y la lectura de tendencia con su encuesta; las fechas exactas están allí.</p>
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
