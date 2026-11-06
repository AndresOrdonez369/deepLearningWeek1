"""Week-2 student study guide: semana2/guia/index.html
usage: python build_guia2.py <repo_root>          (slide numbers come from <repo_root>/semana2/docencia/slides/slides.json)"""
import json, pathlib, sys, unicodedata as _u
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit2 import page, section, chip, idea, box, formula, ex, colab, fig, hist, weeks
import figs_guia2 as F

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
OUT = ROOT / 'semana2'
COLAB = 'https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana2/proyectos/'
NB3, NB4 = COLAB + 'NB03_tu_primera_cnn.ipynb', COLAB + 'NB04_redes_que_recuerdan.ipynb'
NB2 = 'https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/NB02_sabado_tu_primera_red.ipynb'
B, A, T, P, I = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--purple)', 'var(--ink)'

_sj = OUT / 'docencia' / 'slides' / 'slides.json'
SL = {s['id']: s['n'] for s in json.loads(_sj.read_text())} if _sj.exists() else {}


def lam(*ids):
    """'lámina 14' or 'láminas 14 y 15' from the deck; empty if the slide is not in the deck."""
    ns = sorted({SL[i] for i in ids if i in SL})
    if not ns:
        return 'las slides'
    return f'lámina {ns[0]}' if len(ns) == 1 else 'láminas ' + ', '.join(map(str, ns[:-1])) + f' y {ns[-1]}'


S = []

# ------------------------------------------------------------------ start
S.append(('inicio', '★', 'Cómo usar esta guía', f"""
<div class="hero">
<h1>Cómo mira y cómo lee una red neuronal</h1>
<span class="chip" style="margin-top:14px">Semana 2 · Guía de estudio</span>
<p>Las arquitecturas de la semana, en palabras sencillas: primero el problema, después un ejemplo, luego el nombre y al final la cuenta, leída en voz alta («Léelo así»). Con los números reales de los notebooks NB03 y NB04 y ejercicios con su respuesta.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?pre">Jugar el pre-quiz</a><a class="btn" href="#rec">Empezar a estudiar</a><a class="btn ghost" style="color:#EEF2F8;border-color:#2A3B5C" href="../material/Lectura_tendencia_Semana2.pdf">Lectura de tendencia (PDF)</a></div>
</div>
<h2 class="sr">Cómo usar esta guía</h2>
{idea('El hilo de toda la semana: <b>cada arquitectura es una suposición sobre cómo están organizados los datos.</b> La red densa supone que todo se relaciona con todo; la convolucional, que lo cercano importa; la recurrente, que el orden importa; y la atención deja que cada parte mire a todas las demás.')}
<div class="grid">
<div class="tile"><h3>1 · Lee</h3><p>Cada tema empieza con <b>la idea en una frase</b>. Si solo tienes 5 minutos, lee esas frases.</p></div>
<div class="tile"><h3>2 · Practica</h3><p>Resuelve los ejercicios en papel <b>antes</b> de abrir la respuesta. Equivocarse aquí es gratis.</p></div>
<div class="tile"><h3>3 · Lee el código</h3><p>Los notebooks NB03 y NB04 ya vienen <b>escritos y ejecutados</b>. Se aprenden leyendo, apostando un resultado antes de cada celda y comparando con lo que sale.</p></div>
<div class="tile"><h3>4 · Comprueba</h3><p>Al final juega el <a href="../quiz/index.html?final">quiz final</a>: te dice qué temas repasar.</p></div>
</div>
{box('ojo', 'Mapa de la semana: dos temas', '''<p><b>Recorderis:</b> la semana 1 en una sola red, y Keras en 4 pasos (lo que había quedado pendiente).</p>
<p><b>Tema 1 · Cómo mira una red una imagen:</b> la suposición de cada arquitectura, el filtro que recorre la foto, compartir pesos, pooling y la CNN en Keras · notebook <b>NB03</b>.</p>
<p><b>Tema 2 · Cómo lee una red una secuencia:</b> la libreta de la RNN, el olvido y la LSTM · notebook <b>NB04</b>; después la atención, el Transformer y la tendencia de los modelos híbridos.</p>
<p><b>Cierre:</b> cómo elegir la arquitectura para tu proyecto. Cada sesión sigue donde terminó la anterior.</p>
<p>Las prácticas son <b>en clase y sin nota</b>. Las <a href="../docencia/slides/index.html">slides interactivas</a> quedan publicadas para repasar: puedes mover el filtro sobre una foto, ver cómo se llena la libreta y a qué palabra mira la atención.</p>''')}
<p>Marca <b>«Ya lo entendí»</b> al final de cada tema: tu avance se guarda en este navegador y aparece en el índice.</p>
"""))

# ------------------------------------------------------------------ 00 · recap of week 1
def cadena():
    """The week-1 chain as responsive HTML cards (readable on a phone)."""
    steps = [('Tabla', 'datos y etiqueta'), ('Neurona', 'z = w·x + b'), ('Activación', 'dobla la línea'), ('Red en capas', 'vence a XOR'),
             ('Pérdida', 'qué tan mal vamos'), ('Gradiente', 'bajar la montaña'), ('Retro&shy;propagación', 'repartir la culpa'), ('Keras', 'cuatro pasos')]
    cards = ''.join(
        f'<li style="list-style:none;background:var(--paper);border:2px solid {"var(--amber-f)" if i in (1, 5) else "var(--blue)"};border-radius:14px;padding:10px 12px">'
        f'<span style="display:block;font:700 13px \'Space Grotesk\',sans-serif;color:var(--muted)">{i + 1}</span>'
        f'<b style="display:block;font:700 16px \'Space Grotesk\',sans-serif;color:var(--ink)">{t}</b>'
        f'<span style="font-size:14px;color:var(--muted)">{d}</span></li>' for i, (t, d) in enumerate(steps))
    return (f'<ol style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;padding:0;margin:18px 0 8px">{cards}</ol>'
            '<p style="font-size:14.5px;color:var(--muted);margin:0 0 18px">En ámbar, las dos piezas que más vuelven esta semana: '
            'la <b>neurona</b> (un filtro de la CNN es una neurona que mira 9 píxeles vecinos) y el <b>gradiente</b> (todas las redes se entrenan igual).</p>')

S.append(('rec', '00', 'Recorderis de la semana 1', f"""
{idea('Todo lo de esta semana se arma con las piezas de la semana 1: una neurona que suma datos por pesos, una pérdida que dice qué tan mal vamos y el descenso de gradiente que corrige. Lo único nuevo es <b>cómo se conectan las neuronas</b>.')}
{cadena()}
<table><tr><th>Pieza</th><th>Qué es, en una frase</th><th>El ejemplo de clase</th></tr>
<tr><td><b>Datos en una tabla</b></td><td>Cada fila es un ejemplo; cada columna, una <b>característica</b>; la respuesta conocida es la <b>etiqueta</b>.</td><td>Los socios del comité de crédito: ingreso, antigüedad, atrasos → ¿paga o no paga?</td></tr>
<tr><td><b>Neurona</b></td><td>Multiplica cada dato por su <b>peso</b>, suma todo y le suma el <b>sesgo</b>: \\(z = w \\cdot x + b\\).</td><td>Tu nota final del curso: cada nota pesa distinto y la exigencia es el sesgo (−70). El socio A obtuvo <b>z = 2.81</b>.</td></tr>
<tr><td><b>Activación</b></td><td>Convierte el puntaje en la salida y <b>dobla la línea</b> para que la red aprenda curvas.</td><td>Interruptor (escalón), regulador de luz (sigmoide: z = 2.81 → 0.943, un 94 %) y válvula (ReLU).</td></tr>
<tr><td><b>Red en capas</b></td><td>Una neurona solo traza una línea recta; varias en capas combinan líneas.</td><td>La luz de la escalera (XOR): ninguna línea la separa; dos neuronas ocultas sí.</td></tr>
<tr><td><b>Error y pérdida</b></td><td>El error es <b>real − predicho</b>, uno por caso. La pérdida resume todos en <b>un solo número</b>: más pequeño es mejor.</td><td>Las casas de Quito: errores 10, −5, −20 y −2 → MSE = <b>132.25</b>. La BCE castiga al meteorólogo que dijo «1 %» y llovió.</td></tr>
<tr><td><b>Descenso de gradiente</b></td><td>La pendiente dice hacia dónde sube la pérdida; damos un paso <b>en contra</b>, de largo η.</td><td>Bajar el Cotopaxi con neblina. Peso 2, pendiente +4, η = 0.1 → peso nuevo <b>1.6</b>.</td></tr>
<tr><td><b>Retropropagación</b></td><td>Reparte la culpa del error hacia atrás, capa por capa, multiplicando efectos (regla de la cadena).</td><td>Los engranajes: si A mueve a B 3 veces y B mueve a C 2 veces, A mueve a C 6 veces.</td></tr>
<tr><td><b>Keras</b></td><td>Construir, compilar, entrenar y predecir: TensorFlow hace las cuentas por debajo.</td><td>La red de las lunas: <b>337</b> parámetros y <b>95 %</b> en el examen final.</td></tr>
<tr><td><b>Métricas</b></td><td>La exactitud puede engañar si los casos que buscas son pocos: mira la matriz de confusión.</td><td>Un modelo que dice «al día» a todos acierta el <b>87 %</b> y no encuentra ni un moroso.</td></tr></table>
{box('analogia', 'Lo que cambia esta semana', '<p>Hasta ahora los datos eran <b>tablas</b>: cualquier columna se podía relacionar con cualquier otra. ¿Y si el dato es una <b>foto</b>, donde importa qué píxel está al lado de cuál? ¿Y si es una <b>frase</b>, donde importa el orden de las palabras? Esas dos preguntas son los dos temas de la semana.</p>')}
<h3>Para comprobar</h3>
{ex('Una neurona recibe varios datos. ¿Qué hace con ellos?', '<p>Multiplica cada dato por su peso, suma todo y le suma el sesgo. Ese puntaje \\(z\\) pasa por la activación, que da la salida. Es la cuenta de la nota final del curso.</p>')}
{ex('Si la pendiente de la pérdida con respecto a un peso es +4, ¿el peso debe subir o bajar?', '<p><b>Bajar.</b> La pendiente apunta hacia donde la pérdida sube; caminamos en contra. Con η = 0.1: 2 − 0.1 × 4 = 1.6.</p>')}
{ex('Un modelo dice «al día» a todos los socios y acierta el 87 %. ¿Es un buen modelo?', '<p><b>No.</b> Acierta porque el 87 % de los socios está al día, pero no encuentra a ningún moroso: su recall es 0. Por eso, además de la exactitud, miramos la matriz de confusión.</p>')}
<p>Si alguna pieza no te queda clara, la <a href="../../guia/index.html">guía de la semana 1</a> tiene una sección para cada una.</p>
"""))

# ------------------------------------------------------------------ 00 · Keras
S.append(('b00', 'K', 'Keras en 4 pasos (lo que quedó pendiente)', f"""
{idea('Keras arma y entrena una red en cuatro pasos: construir, compilar, entrenar y predecir. Esta semana solo cambia el primero: qué capas apilamos.')}
<h3>Primero, la necesidad</h3>
<p>En la semana 1 hicimos a mano las cuentas de una red con 2 neuronas ocultas: el paso hacia adelante, la culpa hacia atrás y la actualización. Una red de verdad tiene miles o millones de pesos. Nadie hace eso a mano. Para eso existen dos librerías de Python que ya vienen en Colab.</p>
<ul>
<li><b>TensorFlow</b> (Google, 2015) es <b>el motor</b>: guarda los números en tensores, calcula las culpas solo (la retropropagación) y puede usar la GPU.</li>
<li><b>Keras</b> (François Chollet, 2015; hoy Keras 3) es <b>el volante</b>: trae capas listas y tres métodos que hacen todo el trabajo.</li>
</ul>
{box('analogia', 'Analogía', '<p>Puedes manejar un carro sin abrir el capó. Keras te deja entrenar una red sin escribir la retropropagación; saber que el motor existe ayuda cuando algo falla.</p>')}
<h3>Los datos entran como una tabla</h3>
<p>Keras recibe arrays de NumPy. <code>X</code> es la tabla de entradas: cada fila es un ejemplo y cada columna un dato. <code>y</code> trae la respuesta de cada fila. Su forma (<code>shape</code>) dice filas × columnas. En las lunas del NB02: <code>X_train.shape → (480, 2)</code>, 480 ejemplos con 2 datos cada uno.</p>
<h3>Los cuatro pasos, con las lunas</h3>
<pre><code>import keras
from keras import layers

# 1 · Build: stack layers in order
model = keras.Sequential([
    keras.Input(shape=(2,)),                 # each example brings 2 numbers
    layers.Dense(16, activation="relu"),     # 2*16 + 16 = 48 parameters
    layers.Dense(16, activation="relu"),     # 16*16 + 16 = 272
    layers.Dense(1, activation="sigmoid"),   # 16*1 + 1 = 17 -> a probability
])
# 2 · Compile: how to learn and what to report
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
              loss="binary_crossentropy", metrics=["accuracy"])
# 3 · Train: forward, backward and update, in batches, many times
history = model.fit(X_train, y_train, epochs=60, batch_size=32, validation_split=0.2)
# 4 · Predict and evaluate: use what it learned (no weight changes)
p = model.predict(X_new)                     # probabilities between 0 and 1
model.evaluate(X_test, y_test)               # loss and accuracy on unseen data</code></pre>
<p class="read"><b>Léelo así:</b> <code>Sequential</code> apila capas como piezas de LEGO. <code>Dense(16, activation="relu")</code> son 16 neuronas de la semana 1, conectadas con todo lo anterior. <code>compile</code> elige el optimizador (Adam, con paso η = 0.01), la pérdida (la entropía cruzada binaria) y lo que se reporta (la exactitud). <code>fit</code> entrena: con 384 ejemplos de entrenamiento y lotes de 32 son <b>12 pasos por época</b>; con 60 épocas, <b>720 pasos</b>. <code>validation_split=0.2</code> aparta 96 ejemplos como simulacro. Al final, 337 parámetros y cerca de <b>95 %</b> en los 120 ejemplos de prueba.</p>
<table><tr><th>Paso</th><th>Qué decides</th><th>¿Cambia esta semana?</th></tr>
<tr><td><b>1 · Construir</b> (<code>Sequential</code>)</td><td>capas, neuronas y activaciones</td><td><b>Sí:</b> aparecen <code>Conv2D</code>, <code>MaxPooling2D</code>, <code>SimpleRNN</code> y <code>LSTM</code></td></tr>
<tr><td><b>2 · Compilar</b> (<code>compile</code>)</td><td>optimizador, pérdida y métrica</td><td>Con 10 clases la pérdida es <code>sparse_categorical_crossentropy</code></td></tr>
<tr><td><b>3 · Entrenar</b> (<code>fit</code>)</td><td>épocas, tamaño del lote y validación</td><td>No: es igual</td></tr>
<tr><td><b>4 · Predecir</b> (<code>predict</code>, <code>evaluate</code>)</td><td>usar lo aprendido</td><td>Con 10 clases se elige la más probable</td></tr></table>
{box('ojo', 'Solo fit aprende', '<p><code>predict</code> y <code>evaluate</code> no cambian los pesos: solo usan lo aprendido. Y <code>summary()</code> solo muestra la tabla de capas y parámetros.</p>')}
{box('error', 'Errores comunes', '<ul><li>Que la forma de los datos no coincida con <code>keras.Input</code>: si cada ejemplo trae 6 datos, va <code>shape=(6,)</code>. Es el error más común al empezar.</li><li>Olvidar la validación y no darse cuenta de que la red memoriza.</li><li>Pensar que <code>predict</code> sigue entrenando.</li></ul>')}
<h3>Practica</h3>
{ex('Tienes 1 200 socios con 6 datos cada uno. ¿Qué forma tiene <code>X</code> y qué escribes en <code>keras.Input</code>?', '<p><code>X.shape == (1200, 6)</code>, y en la red <code>keras.Input(shape=(6,))</code>: cada ejemplo trae 6 datos.</p>')}
{ex('Con 800 ejemplos de entrenamiento y <code>batch_size=50</code>, ¿cuántos pasos de aprendizaje hay en cada época? ¿Y en 10 épocas?', '<p>800 ÷ 50 = 16 pasos por época; en 10 épocas, 160 pasos.</p>')}
{ex('¿Cuál de los cuatro pasos tienes que cambiar para probar otra arquitectura?', '<p>Solo el primero, <b>construir</b>: la lista de capas dentro de <code>Sequential</code>. Compilar, entrenar y predecir se escriben igual.</p>')}
{colab(NB2, '<b>NB02 de la semana 1</b>, partes E y F: Keras paso a paso con XOR y con las lunas, línea por línea. Si en clase no alcanzamos, es la mejor preparación para el NB03.')}
"""))

# ------------------------------------------------------------------ 01 · images and CNN
S.append(('b01', 'T1', 'Cómo mira una red una imagen: redes convolucionales', f"""
{idea('Una red convolucional (CNN) mira la foto con una lupa pequeña que recorre toda la imagen y busca el mismo patrón en todas partes. Por eso aprende más con muchos menos parámetros que una red densa.')}
<h3>Primero, la necesidad</h3>
<p>Una tienda en línea recibe miles de fotos de productos y quiere ordenarlas solas: camisetas, pantalones, zapatillas. Escribir reglas («si tiene dos mangas…») es imposible, como pasaba con el gato de la semana 1. Así que entrenamos una red con ejemplos. Usamos <b>Fashion-MNIST</b> (Zalando, 2017): <b>70 000 fotos de ropa</b> de 28 × 28 píxeles en 10 clases: camiseta, pantalón, suéter, vestido, abrigo, sandalia, camisa, zapatilla, bolso y botín. 60 000 son para estudiar y 10 000 para el examen final.</p>
<h3>Una imagen es una tabla de números</h3>
<p>Cada píxel guarda su <b>brillo</b>: 0 es negro y 255 es blanco. Una foto de 28 × 28 es una tabla de <b>784 números</b>; no hay nada más. Antes de entrenar dividimos entre 255 para que queden entre 0 y 1.</p>
{fig(F.prenda(), 'La primera foto de prueba de Fashion-MNIST, un botín, y la ventana de 3 × 3 que usamos en el NB03 para hacer la cuenta a mano.')}
<h3>Primer intento: la red densa de la semana 1</h3>
<p>Una red densa necesita una fila de números, así que <b>aplanamos</b> la foto (<code>Flatten</code>): las 28 filas, una detrás de otra, en una sola fila de 784. Una capa de 128 neuronas conectadas con todo tiene 784 × 128 + 128 = <b>100 480</b> parámetros. Con la salida, <b>101 770</b>. Funciona: cerca de <b>86.7 %</b> en el examen final.</p>
<p>Pero tiene un problema escondido. Al aplanar, <b>la red ya no sabe qué píxel está al lado de cuál</b>: cada píxel es una columna más. La prueba del NB03: si mezclamos los píxeles de todas las fotos siempre de la misma manera (para nosotros la foto se vuelve ruido), la densa da <b>87.2 %</b>, prácticamente lo mismo. Nunca usó la vecindad.</p>
<h3>Idea clave 1 · Cada arquitectura es una suposición</h3>
{fig(F.suposicion(), 'Tres formas de mirar los datos: todo con todo, lo cercano y el orden.')}
<table><tr><th>Arquitectura</th><th>Qué supone</th><th>Para qué datos</th><th>Analogía</th></tr>
<tr><td><b>Densa</b></td><td>cualquier dato puede relacionarse con cualquier otro</td><td>tablas: la ficha de un socio</td><td>un comité que mira todos los papeles a la vez</td></tr>
<tr><td><b>Convolucional (CNN)</b></td><td>lo cercano importa más que lo lejano y el mismo patrón puede aparecer en cualquier parte</td><td>imágenes</td><td>una lupa que recorre la foto</td></tr>
<tr><td><b>Recurrente (RNN)</b></td><td>el orden importa: se lee paso a paso</td><td>texto, voz, series de tiempo</td><td>leer un libro con una libreta pequeña</td></tr></table>
<p>Una suposición buena le ahorra trabajo a la red: no tiene que descubrir desde cero algo que ya sabemos de los datos.</p>
<h3>Idea clave 2 · El filtro: una lupa de 3 × 3</h3>
<p>Un <b>filtro</b> (o <i>kernel</i>) es una tablita de 3 × 3 pesos. La <b>convolución</b> lo coloca sobre cada ventana de 3 × 3 de la foto, multiplica número por número, suma los 9 productos más un sesgo y anota el resultado. Después corre la ventana un píxel y repite, hasta recorrer toda la foto.</p>
{formula(r'\text{mapa}[i,j] = \sum_{a=0}^{2}\sum_{b=0}^{2} w_{a,b}\; x_{i+a,\,j+b} \; + \; b',
         [(r'x_{i+a,\,j+b}', 'los 9 píxeles de la ventana que empieza en la fila i, columna j', B), (r'w_{a,b}', 'los 9 pesos del filtro (se aprenden)', A), (r'b', 'el sesgo del filtro', T)],
         read='para cada posición (i, j), pon la lupa encima, multiplica cada píxel de la ventana por el peso que le toca en el filtro, suma los nueve productos y agrega el sesgo. Ese número va a la casilla (i, j) del mapa.')}
{fig(F.conv(), 'Un filtro de borde vertical: −1 a la izquierda, 0 al centro y +1 a la derecha. Donde los dos lados son iguales da 0; sobre el borde, oscuro → claro, da un número grande.')}
<p><b>El ejemplo del NB03, con números.</b> En la ventana marcada del botín (filas 11 a 13, columnas 13 a 15), la columna de la izquierda vale 0, 0 y 0.35 y la de la derecha 0.54, 0.45 y 0.35. Con el filtro de borde vertical, la columna del medio se multiplica por 0 y no cuenta:</p>
{formula(r'(0.54 + 0.45 + 0.35) - (0 + 0 + 0.35) \approx +0.99', read='lo de la derecha menos lo de la izquierda. Da positivo y grande: ahí hay un borde de oscuro a claro, y el mapa lo pinta. Donde todo es fondo negro, la resta da 0.')}
<p>El resultado de recorrer toda la foto es un <b>mapa de activación</b>: una tabla nueva que se enciende donde el filtro encontró su patrón. Con un filtro de 3 × 3 sobre 28 × 28 el mapa queda de <b>26 × 26</b>, porque la ventana cabe en 26 posiciones por fila (28 − 3 + 1). En las slides ({lam('filtro')}) puedes mover la lupa y ver cómo se llena el mapa.</p>
<p><b>Muchos filtros, muchos mapas.</b> Una capa <code>Conv2D(16, 3)</code> tiene 16 filtros, cada uno con sus propios pesos, y produce 16 mapas: uno para bordes verticales, otro para horizontales, otro para zonas claras… <b>Nadie los programa</b>: salen del descenso de gradiente. En el NB03 (Parte 4) se ven los 16 filtros que aprendió la red, y varios son detectores de bordes parecidos al que escribimos a mano.</p>
<h3>Idea clave 3 · El mismo filtro en toda la imagen</h3>
<p>Un filtro de 3 × 3 tiene <b>9 pesos + 1 sesgo = 10 números</b>, y se usa en <b>todas</b> las posiciones de la foto. 16 filtros son <b>160 parámetros</b>. La primera capa densa necesitaba <b>100 480</b>, porque cada neurona tiene un peso propio para cada píxel. Esto se llama <b>compartir pesos</b>.</p>
{fig(F.share(), 'La neurona densa conecta cada píxel con un peso propio; el filtro de la CNN es un sello de 10 números que se estampa en toda la foto.')}
{box('analogia', 'Analogía: el sello', '<p>Para marcar todas las hojas de un expediente no fabricas un sello distinto para cada hoja: usas el mismo en todas. La CNN usa la misma lupa en toda la foto, y si un borde aparece arriba o abajo, la misma lupa lo encuentra.</p>')}
<h3>Pooling: quedarse con lo más fuerte</h3>
<p>Después de la convolución, una capa <code>MaxPooling2D(2)</code> resume cada mapa: de cada ventana de 2 × 2 se queda con el número más grande. El mapa queda de la mitad de alto y de ancho (26 × 26 → 13 × 13). Así la red trabaja con menos números y tolera que el patrón se mueva un poquito.</p>
{fig(F.pool(), 'MaxPooling 2 × 2: de cada cuadrito de cuatro números queda el mayor, como subrayar la frase más importante de cada párrafo.')}
<h3>La CNN completa, en Keras</h3>
<pre><code>cnn = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),           # height, width, channels (1 = grayscale)
    layers.Conv2D(16, 3, activation="relu"),  # 16 filters of 3x3 -> 16 maps of 26x26
    layers.MaxPooling2D(2),                   # keep the strongest of each 2x2 -> 13x13
    layers.Conv2D(32, 3, activation="relu"),  # 32 filters that look at the 16 maps -> 11x11
    layers.MaxPooling2D(2),                   # -> 5x5
    layers.Flatten(),                         # 5*5*32 = 800 numbers in a row
    layers.Dense(10, activation="softmax"),   # 10 probabilities, one per class
])
cnn.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
cnn.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)</code></pre>
{fig(F.shapes(), 'Las formas dentro de la red: la foto se achica y gana mapas; al final, 800 números y 10 probabilidades.')}
<table><tr><th>Capa</th><th>Sale</th><th>Parámetros</th><th>De dónde salen</th></tr>
<tr><td><code>Conv2D(16, 3)</code></td><td style="white-space:nowrap">26 × 26 × 16</td><td>160</td><td>16 filtros × (9 pesos + 1 sesgo)</td></tr>
<tr><td><code>MaxPooling2D(2)</code></td><td style="white-space:nowrap">13 × 13 × 16</td><td>0</td><td>solo elige el mayor: no aprende nada</td></tr>
<tr><td><code>Conv2D(32, 3)</code></td><td style="white-space:nowrap">11 × 11 × 32</td><td>4 640</td><td>32 filtros × (3 × 3 × 16 pesos + 1 sesgo): cada filtro mira los 16 mapas</td></tr>
<tr><td><code>MaxPooling2D(2)</code></td><td style="white-space:nowrap">5 × 5 × 32</td><td>0</td><td>—</td></tr>
<tr><td><code>Flatten</code></td><td>800</td><td>0</td><td>5 × 5 × 32 en una fila</td></tr>
<tr><td><code style="white-space:nowrap">Dense(10, softmax)</code></td><td>10</td><td>8 010</td><td>800 × 10 + 10</td></tr>
<tr><td colspan="2"><b>Total</b></td><td><b>12 810</b></td><td>cerca de <b>8 veces menos</b> que la densa (101 770)</td></tr></table>
<h3>De sí o no a 10 clases: softmax</h3>
<p>En la semana 1 la salida era una sola neurona con sigmoide: una probabilidad de «sí». Ahora hay 10 clases, así que la salida tiene <b>10 neuronas</b> y la función <b>softmax</b> convierte sus 10 puntajes en <b>10 probabilidades que suman 1</b>.</p>
{formula(r'p_k = \frac{e^{z_k}}{e^{z_1} + e^{z_2} + \dots + e^{z_{10}}}',
         [(r'z_k', 'el puntaje de la clase k', B), (r'e^{z_k}', 'lo vuelve positivo y agranda las diferencias', A), (r'p_k', 'la probabilidad de la clase k', T)],
         read='a cada puntaje le aplicamos la exponencial, para que quede positivo, y lo dividimos entre la suma de todos. Así cada probabilidad queda entre 0 y 1 y entre todas suman 1. La red elige la clase con la probabilidad más alta.')}
{fig(F.softmax_bars(), 'Lo que dice la CNN de la primera camisa de prueba: camisa cerca de 77 %, y algo para camiseta, abrigo y suéter. Duda entre prendas parecidas, como dudaría una persona.')}
<p>La pérdida para 10 clases es <code>sparse_categorical_crossentropy</code>: la misma idea de la entropía cruzada de la semana 1 (castiga estar seguro y equivocado), pero con 10 opciones. «Sparse» quiere decir que la etiqueta llega como un número de 0 a 9.</p>
<h3>Los resultados del NB03</h3>
<table><tr><th></th><th>Parámetros</th><th>Examen final</th><th>Moviendo la prenda 2 píxeles</th><th>Con los píxeles mezclados</th></tr>
<tr><td><b>Densa</b></td><td>101 770</td><td>86.7 %</td><td><b>56.5 %</b></td><td>87.2 % (igual)</td></tr>
<tr><td><b>CNN</b></td><td>12 810</td><td>87.7 %</td><td><b>75.2 %</b></td><td>85.2 % (baja)</td></tr></table>
{fig(F.duelo(), 'Si movemos la prenda unos píxeles, la densa se cae más rápido. Con 4 píxeles las dos se caen: la suposición ayuda, pero no es magia.')}
<p class="read"><b>Léelo así:</b> la CNN acierta un poco más con <b>8 veces menos</b> números. Si movemos la prenda 2 píxeles, la densa se cae a 56.5 % (aprendió «este píxel», no «este borde») y la CNN aguanta 75.2 %. Si mezclamos los píxeles, la densa ni se entera y la CNN baja, porque su suposición, «lo cercano importa», ya no se cumple. Cada red funciona mejor cuando su suposición coincide con los datos.</p>
<p><b>¿En qué se equivoca?</b> La confusión más frecuente de la CNN es <b>camisa tomada por camiseta</b>: 129 de 1 000 camisas. La camisa es la clase más difícil (63 %); pantalón, bolso, botín y sandalia pasan del 96 %. A 28 × 28 píxeles, una camisa de manga corta se parece muchísimo a una camiseta.</p>
{hist('1989', 'Yann LeCun y su equipo en los laboratorios Bell entrenaron una red convolucional con retropropagación para leer códigos postales escritos a mano. Una versión posterior, LeNet-5 (1998), leía cheques en bancos de Estados Unidos. En 2012, una CNN mucho más grande, AlexNet, ganó el concurso ImageNet y abrió la era del deep learning.')}
{box('curioso', 'Comparar con justicia', '<p>Desde 2020 los Vision Transformers parecían los sucesores de las CNN. En 2023, un equipo de Google DeepMind entrenó CNN con el mismo cómputo que los mejores ViT y obtuvo un empate técnico, con más de 90 % en ImageNet (Smith et al., 2023). Lo que más pesó fueron el cómputo y los datos. Antes de declarar un ganador, todos deben correr la misma carrera.</p>')}
{box('error', 'Errores comunes', '<ul><li>Olvidar el canal: la CNN espera fotos de forma (28, 28, <b>1</b>), no (28, 28).</li><li>No dividir entre 255: los números grandes hacen que el entrenamiento arranque mal.</li><li>Usar <code>binary_crossentropy</code> con 10 clases: es para sí o no.</li><li>Creer que la CNN es inmune a todo: con 4 píxeles de movimiento cae a 28 % (en la semana 3 veremos cómo hacerla más robusta).</li></ul>')}
<h3>Practica</h3>
{ex('Un filtro de 5 × 5 recorre una foto de 28 × 28. ¿De qué tamaño queda el mapa?', '<p>28 − 5 + 1 = <b>24</b>: un mapa de 24 × 24.</p>')}
{ex('¿Cuántos parámetros tiene <code>Conv2D(8, 3)</code> sobre una foto en blanco y negro?', '<p>Cada filtro: 3 × 3 = 9 pesos + 1 sesgo = 10. Con 8 filtros, <b>80</b> parámetros.</p>')}
{ex('Aplica MaxPooling 2 × 2 a la ventana [[1, 4], [3, 2]].', '<p>Queda <b>4</b>, el mayor de los cuatro.</p>')}
{ex('Una red densa y una CNN dan casi la misma exactitud en tus fotos. ¿Por qué podrías preferir la CNN?', '<p>Porque usa muchos menos parámetros (8 veces menos en el NB03) y aguanta mejor que la prenda se mueva un poco (75.2 % contra 56.5 % con 2 píxeles).</p>')}
{ex('Un hospital quiere detectar fracturas en radiografías. ¿Qué arquitectura pruebas primero y por qué?', '<p>Una CNN: es una imagen y una fractura es un patrón local (bordes y formas) que puede aparecer en cualquier parte de la placa.</p>')}
{colab(NB3, '<b>NB03 · Tu primera red convolucional</b>: la foto como tabla, el filtro a mano, la red densa contra la CNN, los filtros que aprendió y las dos pruebas de la suposición. En clase: partes 0, 2, 3 y 5.')}
"""))

# ------------------------------------------------------------------ 02 · sequences, RNN, LSTM
S.append(('b02', 'T2', 'Cómo lee una red una secuencia: RNN y LSTM', f"""
{idea('Una red recurrente (RNN) lee de a un paso y lleva una libreta pequeña, el estado oculto, donde resume lo que va leyendo; usa la misma celda en cada paso. Su límite: la libreta es de tamaño fijo y lo que quedó muy atrás se olvida.')}
<h3>Primero, la necesidad</h3>
<p>Muchos datos llegan <b>en orden</b>: las palabras de una frase, el audio de una llamada, las ventas de cada día, los pagos de un socio mes a mes. «El perro mordió al cartero» y «el cartero mordió al perro» tienen las mismas palabras y dicen cosas distintas.</p>
<p><b>El ejemplo del NB04.</b> Tenemos 12 meses de días de atraso de cada socio (ficticio). Unos <b>empeoran</b> y otros <b>mejoran</b>. El truco: un socio que mejora tiene <b>exactamente los mismos meses</b> que uno que empeora, solo que al revés. Su promedio es idéntico.</p>
{fig(F.orden(), 'El mismo socio con los meses en otro orden: mismo promedio, historia contraria.')}
<h3>Una secuencia es una tabla con orden</h3>
<p>Para Keras, un conjunto de secuencias tiene forma <b>(ejemplos, pasos, datos por paso)</b>. En el NB04: <code>(2000, 12, 1)</code>, 2 000 socios, 12 meses y 1 dato por mes. Una frase sería (frases, palabras, números por palabra).</p>
<p>Un modelo que solo mira el <b>promedio</b> de los meses tiene 25 parámetros y logra <b>48.4 %</b>: adivina, porque para él los dos socios son idénticos. Una RNN pequeña, con 89 parámetros, logra <b>100 %</b>. La diferencia no es el tamaño: es la suposición.</p>
<h3>Idea clave 4 · La libreta de la RNN</h3>
<p>La RNN lee un paso a la vez. En cada paso mira el dato nuevo y lo que tenía anotado, y reescribe su libreta. Esa libreta es un vector de números llamado <b>estado oculto</b>, \\(h\\).</p>
{formula(r'h_t = \tanh\big(\,w\,x_t \;+\; u\,h_{t-1} \;+\; b\,\big)',
         [(r'x_t', 'el dato que llega ahora (el mes t, la palabra t)', B), (r'h_{t-1}', 'lo que ya estaba en la libreta', T), (r'w,\ u,\ b', 'los pesos y el sesgo que se aprenden', A), (r'\tanh', 'aplasta el resultado entre −1 y 1', P)],
         read='la nueva libreta es una mezcla de lo que llega ahora (pesado por w) y de lo que ya tenía anotado (pesado por u), más un sesgo, aplastada entre −1 y 1. Los mismos w, u y b se usan en todos los pasos.')}
<p><b>La libreta a mano (NB04, parte 1).</b> Con w = 1, u = 0.5 y b = 0, leemos la secuencia x = [1, 0, 0, 0]: un dato al principio y después nada.</p>
<ul>
<li>Paso 1: \\(h_1 = \\tanh(1\\cdot 1 + 0.5\\cdot 0) = \\tanh(1) \\approx\\) <b>0.76</b></li>
<li>Paso 2: \\(h_2 = \\tanh(0 + 0.5\\cdot 0.76) = \\tanh(0.38) \\approx\\) <b>0.36</b></li>
<li>Paso 3: \\(h_3 = \\tanh(0.5\\cdot 0.36) \\approx\\) <b>0.18</b></li>
<li>Paso 4: \\(h_4 \\approx\\) <b>0.09</b></li>
</ul>
{fig(F.eco(), 'El eco del primer dato se reduce más o menos a la mitad en cada paso: la libreta se va borrando.')}
<h3>La misma celda en cada paso</h3>
<p>Si dibujamos la RNN paso por paso (la <b>desenrollamos</b>), parece una red de muchas capas, una por paso, pero todas con <b>los mismos pesos</b>. Es la misma idea de la CNN: la CNN comparte su filtro en el <b>espacio</b>; la RNN comparte su celda en el <b>tiempo</b>. Por eso puede leer secuencias de cualquier largo: 3 meses o 60.</p>
{fig(F.unroll(), 'La RNN desenrollada: cada paso le pasa su libreta al siguiente. Al entrenar, la culpa viaja hacia atrás paso por paso.')}
<h3>Por qué se olvida</h3>
<p>Para entrenar, la culpa del error viaja hacia atrás por todos los pasos (se llama <b>retropropagación a través del tiempo</b>). En cada paso se multiplica por un número que suele ser menor que 1. Si fuera 0.5, después de 10 pasos quedaría \\(0.5^{{10}} \\approx 0.001\\): casi nada. Es el <b>teléfono dañado</b> de la semana 1, ahora en el tiempo. La red casi no puede aprender relaciones lejanas.</p>
<h3>La LSTM: una libreta con compuertas</h3>
<p>En 1997, Sepp Hochreiter y Jürgen Schmidhuber propusieron la <b>LSTM</b> (<i>long short-term memory</i>). Agrega una <b>cinta de memoria</b> \\(c\\) y tres <b>compuertas</b>, cada una una sigmoide entre 0 y 1, como una válvula:</p>
<ul>
<li><b>Olvidar</b> (\\(f\\)): qué parte de la cinta se borra. Es el borrador.</li>
<li><b>Guardar</b> (\\(i\\)): qué parte de lo nuevo se anota. Es el lápiz.</li>
<li><b>Mostrar</b> (\\(o\\)): qué parte de la cinta se lee en voz alta como salida. Es la ventana.</li>
</ul>
{formula(r'c_t = f_t \cdot c_{t-1} \;+\; i_t \cdot \tilde c_t \qquad\qquad h_t = o_t \cdot \tanh(c_t)',
         read='la cinta nueva es lo que se conserva de la anterior (si f vale 1, se conserva todo) más lo nuevo que se decide anotar. La salida es la parte de la cinta que la compuerta de mostrar deja pasar. Como f puede quedarse cerca de 1, lo importante viaja lejos sin borrarse.')}
{fig(F.lstm(), 'La LSTM: una cinta que puede llevar lo importante muy lejos, con tres válvulas.')}
<p>Durante dos décadas la LSTM fue la reina de las secuencias: traducción, reconocimiento de voz, series de tiempo. En 2014 apareció la GRU, una versión con dos compuertas.</p>
<h3>El examen de memoria del NB04</h3>
<p>Cada paso trae un valor (+1 o −1) y una marca. Solo uno de los primeros 10 pasos está marcado, y la respuesta es el signo de ese valor; después vienen muchos pasos de distracción. Los tres modelos tienen el mismo presupuesto: 10 épocas.</p>
<table><tr><th>Pasos</th><th>SimpleRNN (1 153 parámetros)</th><th>LSTM (4 513)</th><th>Atención (82)</th></tr>
<tr><td>10</td><td>99.9 %</td><td>100 %</td><td>100 %</td></tr>
<tr><td>30</td><td>100 %</td><td>100 % (aprende más rápido)</td><td>100 %</td></tr>
<tr><td>80</td><td><b>52.1 %</b> (adivina)</td><td><b>50.0 %</b> (adivina)</td><td><b>100 %</b></td></tr></table>
{fig(F.memoria(), 'Cuanto más lejos está el dato importante, más difícil es recordarlo. La atención, que veremos en el tema 03, no tiene que recordar: mira directo.')}
{box('ojo', 'Una corrida no prueba nada', '<p>Con 50 pasos, la LSTM aprende con una semilla (SEED = 7: 100 % en la época 9) y no con otra (SEED = 2026: 48 %). Las compuertas ayudan, pero no hacen magia, y una sola corrida no basta para declarar un ganador. Es el Experimento 4 del NB04.</p>')}
<h3>En Keras</h3>
<pre><code>rnn = keras.Sequential([
    keras.Input(shape=(12, 1)),              # (steps, values per step): 12 months, 1 value
    layers.SimpleRNN(8),                     # the notebook: 8 numbers, updated month by month
    layers.Dense(1, activation="sigmoid"),   # probability of "gets worse"
])
# For an LSTM, change one line: layers.LSTM(8)</code></pre>
<p class="read"><b>Léelo así:</b> la entrada ya no es una fila de datos sino una tabla de pasos: 12 meses con 1 número cada uno. <code>SimpleRNN(8)</code> es una libreta de 8 números que se reescribe mes a mes con la misma celda; al final pasa su última libreta a la neurona de salida. Compilar, entrenar y predecir son iguales que siempre.</p>
{box('error', 'Errores comunes', '<ul><li>Darle a la red una forma (2000, 12) en vez de (2000, 12, 1): falta el «datos por paso».</li><li>Creer que una LSTM recuerda todo: también tiene límite.</li><li>Comparar dos modelos con una sola semilla y declarar un ganador.</li></ul>')}
<h3>Practica</h3>
{ex('Tienes las ventas diarias de 300 tiendas durante 90 días, con 2 datos por día (ventas y clientes). ¿Qué forma tiene el array?', '<p><code>(300, 90, 2)</code>: 300 ejemplos, 90 pasos y 2 datos por paso.</p>')}
{ex('Con w = 1, u = 0.5 y b = 0, ¿qué libreta queda después de leer x = [2]?', '<p>\\(h_1 = \\tanh(1\\cdot 2) = \\tanh(2) \\approx 0.96\\).</p>')}
{ex('¿Por qué el modelo del promedio no puede distinguir a un socio que empeora de uno que mejora?', '<p>Porque tienen los mismos meses al revés: el promedio es idéntico. Solo el orden los distingue, y el promedio lo borra.</p>')}
{ex('¿Qué compuerta de la LSTM tiene que quedarse cerca de 1 para recordar algo durante muchos pasos?', '<p>La de <b>olvidar</b>: si vale 1, la cinta conserva todo lo que tenía.</p>')}
{colab(NB4, '<b>NB04 · Redes que recuerdan</b>: la libreta a mano, el orden importa, el examen de memoria y la atención. En clase: partes 1, 2, 3 y 4.')}
"""))

# ------------------------------------------------------------------ 03 · attention, Transformers, trend
S.append(('b03', 'T2', 'La atención, el Transformer y la tendencia', f"""
{idea('La atención deja que cada elemento mire directamente a todos los demás y decida cuáles le importan. No necesita recordar y se calcula en paralelo, pero su costo crece con el cuadrado de la longitud. La tendencia: mezclarla con capas recurrentes baratas.')}
<h3>Primero, la necesidad</h3>
<p>La RNN tiene dos problemas. El primero ya lo vimos: <b>se olvida</b> de lo lejano. El segundo es práctico: <b>lee en fila</b>. Para procesar la palabra 100 necesita haber procesado las 99 anteriores, y las GPU, que son excelentes haciendo miles de cuentas al mismo tiempo, se quedan esperando.</p>
<h3>Idea clave 5 · Cada palabra mira a todas</h3>
<p>En 2017, un equipo de Google propuso dejar la recurrencia: en su artículo <i>Attention is all you need</i> presentó el <b>Transformer</b>. Su idea central, la <b>atención</b>: antes de interpretar una palabra, se la compara con todas las demás y se decide cuáles importan.</p>
<p>El ejemplo de la lectura de tendencia: «el socio pagó la cuota porque <b>él</b> recibió su sueldo». ¿A quién se refiere «él»: al socio o a la cuota? Una persona lo sabe sin pensar. La atención lo calcula con tres ingredientes. Piensa en una biblioteca:</p>
<ul>
<li>la <b>consulta</b> es lo que buscas («él» busca una persona);</li>
<li>cada palabra tiene una <b>clave</b>, como la ficha del catálogo que dice de qué trata;</li>
<li>y un <b>valor</b>, el libro: lo que aporta si la eliges.</li>
</ul>
{formula(r'\text{puntaje}_j = \mathbf{q}\cdot\mathbf{k}_j \qquad \alpha_j = \text{softmax}(\text{puntajes})_j \qquad \text{salida} = \sum_j \alpha_j\,\mathbf{v}_j',
         [(r'\mathbf{q}', 'la consulta de la palabra que pregunta', A), (r'\mathbf{k}_j', 'la clave de la palabra j', B), (r'\alpha_j', 'cuánto mira a la palabra j (suman 1)', T), (r'\mathbf{v}_j', 'el valor de la palabra j', P)],
         read='el puntaje de cada palabra es qué tanto coincide su clave con la consulta (el producto punto de la semana 1); softmax convierte los puntajes en pesos que suman 1; y la nueva versión de la palabra es el promedio de los valores, pesado por esos pesos.')}
<p><b>Con números (NB04, parte 5).</b> Usamos vectores de 2 números: [qué tan persona, qué tan dinero]. Las claves: socio [2, 0], cuota [0, 2], él [1, 0]. La consulta de «él» es [1.5, 0]: busca una persona.</p>
<ul>
<li>Puntajes: socio 1.5·2 = <b>3.0</b>; cuota <b>0.0</b>; él 1.5·1 = <b>1.5</b>.</li>
<li>Softmax: \\(e^{{3}} \\approx 20.1\\), \\(e^{{0}} = 1\\), \\(e^{{1.5}} \\approx 4.5\\); la suma es 25.6. Pesos: socio <b>78.6 %</b>, cuota <b>3.9 %</b>, él <b>17.5 %</b>.</li>
<li>Con los valores socio [1, 0], cuota [0, 1] y él [0.5, 0.5], el nuevo «él» pasa de [0.5, 0.5] (ambiguo) a cerca de <b>[0.87, 0.13]</b>: casi pura persona.</li>
</ul>
{fig(F.attn_words(), 'La atención de «él»: el grosor de cada arco es cuánto mira a esa palabra.')}
<p>En un Transformer real, las consultas, claves y valores no se escriben a mano: la red los <b>aprende</b>, y hay varias atenciones en paralelo («cabezas»), cada una buscando algo distinto.</p>
<h3>La atención del NB04: mirar directo al paso importante</h3>
<p>En el examen de memoria con 80 pasos, las dos redes recurrentes adivinaban. Una atención de <b>82 parámetros</b> llega a <b>100 %</b> en 4 épocas. No tuvo que recordar nada a lo largo de 80 pasos: aprendió <b>a quién mirar</b>. En un ejemplo, pone el <b>90.3 %</b> de su peso en el paso marcado.</p>
{fig(F.attn_weights(), 'Los pesos de la atención del NB04 sobre los 80 pasos: casi todo cae en el paso marcado.')}
<h3>El precio de la atención</h3>
<p>Si cada palabra mira a todas, con \\(n\\) palabras hay \\(n \\times n\\) comparaciones. Con 1 000 palabras, <b>un millón</b>. Además, al generar texto el modelo guarda en memoria una representación de cada palabra anterior (la <b>caché KV</b>), que crece con el texto. El costo de la atención <b>crece con el cuadrado</b> de la longitud.</p>
{fig(F.costo(), 'Tres veces más palabras son nueve veces más comparaciones.')}
{box('analogia', 'Analogía de la lectura', '<p>La RNN escribe una carta mirando solo su libreta de resumen. El Transformer, antes de escribir cada palabra, relee la carta completa desde el principio. Recuerda todo, pero cada palabra nueva le cuesta un poco más que la anterior.</p>')}
<h3>El Transformer en una frase</h3>
<p>Un Transformer apila bloques: en cada bloque, todas las palabras se miran entre sí (atención) y después cada una pasa por una pequeña red densa. Como todo se calcula a la vez, se entrena en paralelo con cantidades de datos antes impensables. De ahí salieron BERT, GPT y casi todos los modelos de lenguaje actuales.</p>
{hist('2017', 'Vaswani y sus colegas publicaron «Attention is all you need» y presentaron el Transformer. Hoy esa arquitectura está detrás de casi cualquier chatbot y también se usa en imágenes, audio y video.')}
<h3>La tendencia: las recurrentes vuelven, mezcladas</h3>
<p>Mientras los textos eran cortos, el precio era tolerable. Hoy los modelos trabajan con cientos de miles o un millón de palabras, y releerlo todo se volvió el cuello de botella. Entre 2023 y 2026 los laboratorios recuperaron la libreta con dos mejoras: que se pueda entrenar en paralelo y que la red decida mejor qué anotar. Así nacieron los <b>state space models</b> como <b>Mamba</b> (Gu y Dao, 2023), e incluso volvió la LSTM con <b>xLSTM</b> (Beck et al., 2025).</p>
<p>La tendencia más fuerte no fue reemplazar al Transformer, sino <b>mezclarlo</b>: los <b>modelos híbridos</b> conservan unas pocas capas de atención completa, que funcionan como un buscador preciso, y usan capas recurrentes baratas en todo lo demás.</p>
{fig(F.hibrido(), 'Un híbrido como Jamba: apuntes resumidos de casi todo y, de vez en cuando, volver al libro.')}
<table><tr><th>Cuándo</th><th>Modelo</th><th>Idea principal (según la lectura)</th></tr>
<tr><td>2024</td><td>Jamba (AI21 Labs)</td><td>una capa de atención por cada siete capas de Mamba</td></tr>
<tr><td>2025</td><td>Nemotron-H (NVIDIA)</td><td>reemplaza cerca del 92 % de las capas de atención por Mamba-2; hasta 3 veces más rápido al generar, con exactitud comparable</td></tr>
<tr><td>2025</td><td>Kimi Linear (Moonshot AI)</td><td>hasta 75 % menos memoria de caché y hasta 6 veces más rápido con textos de un millón de tokens</td></tr>
<tr><td>2026</td><td>Qwen3.5 (Alibaba)</td><td>tres capas de atención «lineal» por cada capa de atención completa</td></tr>
<tr><td>2026</td><td>Nemotron 3 Super (NVIDIA)</td><td>híbrido Mamba–atención con hasta 2.2 veces más rendimiento que un Transformer abierto parecido</td></tr></table>
{box('analogia', 'Analogía: el buen estudiante', '<p>Un modelo híbrido prepara el examen como un buen estudiante: toma apuntes resumidos de casi todo (capas recurrentes) y, de vez en cuando, vuelve al libro para buscar un dato exacto (capas de atención).</p>')}
<h3>El contrapeso: lo que la libreta no puede guardar</h3>
<ul>
<li><b>La libreta tiene un límite.</b> Jelassi y sus colegas (2024) mostraron que un Transformer pequeño copia textos largos con exactitud, mientras que un modelo con estado de tamaño fijo está limitado por lo que cabe en ese estado. Si alguien te dicta un número de teléfono larguísimo y solo puedes anotar un resumen, pierdes dígitos.</li>
<li><b>Los benchmarks pueden engañar.</b> MiniMax probó un híbrido para su modelo M2 y volvió a la atención completa: igualaba en las pruebas tradicionales, pero a mayor escala mostraba «claros déficits» en razonamiento de varios pasos.</li>
<li><b>No hay consenso.</b> A comienzos de 2026 conviven Transformers clásicos, atenciones comprimidas y varios híbridos: «ya nadie se pone de acuerdo sobre la atención».</li>
</ul>
{box('curioso', 'Una mirada desde América Latina', '<p>En la región el desafío no suele ser entrenar un modelo gigante, sino usarlo todos los días con pocas GPU: Latam-GPT (2026) se construyó sobre un Transformer abierto ya existente. Si un modelo necesita mucha menos memoria con textos largos, se pueden analizar expedientes, contratos o normativas en español con hardware que una organización sí puede pagar. Pero esa eficiencia hay que comprobarla en las tareas reales que nos importan.</p>')}
<h3>Debates abiertos (para la encuesta y la clase)</h3>
<ul>
<li><b>Eficiencia o capacidad:</b> ¿vale la pena ganar de 2 a 6 veces en velocidad si se arriesga recordar con exactitud?</li>
<li><b>Arquitectura o escala:</b> si con el mismo cómputo y los mismos datos las arquitecturas rinden parecido, ¿cuánto importa elegir la «perfecta»?</li>
<li><b>Benchmarks o uso real:</b> ¿cómo evaluar para que las pruebas reflejen tareas largas y complejas?</li>
</ul>
<h3>Practica</h3>
{ex('Si la consulta de «él» fuera [0, 1.5] (buscando dinero), ¿a qué palabra miraría más?', '<p>A <b>cuota</b>: su clave [0, 2] da el puntaje más alto (3.0) y la de socio da 0.</p>')}
{ex('Un texto pasa de 2 000 a 4 000 palabras. ¿Cuántas veces más comparaciones hace la atención?', '<p>4 veces más: el doble de palabras al cuadrado (2² = 4).</p>')}
{ex('¿Por qué un Transformer se entrena más rápido que una RNN con la misma cantidad de datos?', '<p>Porque la atención calcula todas las palabras a la vez (en paralelo); la RNN tiene que esperar el paso anterior.</p>')}
{ex('¿Qué tienen los modelos híbridos de cada uno de sus dos ingredientes?', '<p>De las capas recurrentes, el costo bajo y constante por palabra (la libreta). De las capas de atención, la capacidad de buscar con precisión un dato en cualquier parte del texto.</p>')}
<p class="btnrow"><a class="btn" href="../material/Lectura_tendencia_Semana2.pdf">Leer la lectura de tendencia completa (PDF)</a></p>
"""))

# ------------------------------------------------------------------ 04 · choosing
S.append(('b04', 'C', 'Cómo elegir la arquitectura', f"""
{idea('Elegir una arquitectura es elegir una suposición. Pregúntate qué estructura tienen tus datos, cuánto cuesta cada opción y compruébalo con una comparación justa contra una línea base sencilla.')}
<h3>Cada dato con su arquitectura</h3>
<table><tr><th>Tus datos</th><th>Arquitectura para empezar</th><th>Qué supone</th><th>Ejemplo</th></tr>
<tr><td><b>Una tabla</b></td><td>red densa (o un modelo clásico como línea base)</td><td>todo se relaciona con todo</td><td>la ficha de un socio: ingreso, antigüedad, atrasos</td></tr>
<tr><td><b>Una imagen</b></td><td>CNN (o un Vision Transformer, con mucho cómputo)</td><td>lo cercano importa; el mismo patrón en cualquier parte</td><td>fotos de productos, radiografías, cultivos desde un dron</td></tr>
<tr><td><b>Una secuencia</b></td><td>RNN o LSTM; Transformer o híbrido si es larga</td><td>el orden importa</td><td>reseñas de clientes, voz, ventas diarias, pagos mes a mes</td></tr>
<tr><td><b>Un grafo</b> (cosas conectadas)</td><td>red neuronal de grafos (GNN)</td><td>cada elemento aprende de sus vecinos</td><td>socios que se garantizan entre sí, transferencias entre cuentas, moléculas</td></tr>
<tr><td><b>Datos nuevos que crear</b></td><td>GAN o modelos de difusión</td><td>se puede aprender a imitar los datos</td><td>imágenes sintéticas, aumentar datos escasos</td></tr></table>
<h3>Dos arquitecturas de las lecturas, en una frase</h3>
<ul>
<li><b>GAN</b> (Goodfellow y colegas, 2014): dos redes que compiten. Un <b>falsificador</b> genera ejemplos falsos y un <b>detective</b> intenta distinguirlos de los reales; al competir, el falsificador se vuelve cada vez mejor.</li>
<li><b>GNN</b> (redes de grafos): cada nodo (un socio, una cuenta, un átomo) <b>escucha a sus vecinos</b>, mezcla lo que le cuentan y actualiza su resumen, varias rondas seguidas. Supone que las conexiones importan.</li>
</ul>
<h3>Tres preguntas antes de elegir</h3>
<ol>
<li><b>¿Qué estructura tienen mis datos?</b> ¿Es una tabla, una foto, algo con orden, algo conectado? La arquitectura debe suponer lo mismo que tus datos.</li>
<li><b>¿Qué cuesta?</b> Parámetros, tiempo de entrenamiento y, sobre todo, el costo de usarlo todos los días (memoria, velocidad). En la región, muchas veces manda el costo de uso.</li>
<li><b>¿Cómo lo compruebo?</b> Con una <b>línea base</b> sencilla y una <b>comparación justa</b>: los mismos datos, la misma división en entrenamiento, validación y prueba, presupuestos parecidos y más de una semilla. Se elige con validación; la prueba se usa una sola vez.</li>
</ol>
{box('ojo', 'Empieza simple', '<p>Como en el entregable de la semana 1: primero la línea base que no piensa (la clase más común) y un modelo sencillo. Si la arquitectura sofisticada no les gana con justicia, no vale la pena.</p>')}
{box('analogia', 'Analogía', '<p>Elegir arquitectura es como elegir el vehículo: para la ciudad, una moto; para una mudanza, un camión. Ninguno es «el mejor»: depende de la carga y del camino. Y antes de comprar, se hace la prueba de manejo en el mismo trayecto.</p>')}
<h3>Tu proyecto de titulación</h3>
<p>Responde en grupo: ¿qué estructura tienen sus datos? ¿Qué arquitectura supone lo mismo? ¿Cuál es su línea base? ¿Qué número les diría que la arquitectura nueva vale la pena? ¿Y qué cuesta usarla todos los días?</p>
{box('error', 'Errores comunes', '<ul><li>Elegir la arquitectura de moda sin mirar los datos.</li><li>Comparar un modelo grande entrenado mucho tiempo con uno pequeño entrenado poco: no es justo.</li><li>Declarar un ganador con una sola corrida.</li></ul>')}
<h3>Practica: ¿qué arquitectura pruebas primero?</h3>
{ex('Reseñas de clientes de una cooperativa, de 20 a 200 palabras, para saber si están satisfechos.', '<p>Una red para secuencias: el orden de las palabras importa («no fue buena» frente a «fue buena»). Si los textos son largos, un Transformer o un modelo preentrenado.</p>')}
{ex('Fotos de hojas de cacao para detectar una enfermedad.', '<p>Una CNN: es una imagen y la enfermedad deja manchas (patrones locales) en cualquier parte de la hoja.</p>')}
{ex('Transferencias entre miles de cuentas, para detectar redes de fraude.', '<p>Una GNN: lo importante son las conexiones entre cuentas (quién le transfiere a quién).</p>')}
{ex('La ficha de cada socio (ingreso, antigüedad, atrasos) para predecir la mora.', '<p>Una tabla: una red densa, comparada contra una línea base y un modelo clásico. No hay vecinos ni orden que aprovechar.</p>')}
"""))

# ------------------------------------------------------------------ reference
FORMULAS = r"""
<table>
<tr><th>Qué</th><th>Fórmula</th><th>En palabras</th></tr>
<tr><td>Convolución (una casilla del mapa)</td><td>\(\sum_{a,b} w_{a,b}\,x_{i+a,j+b} + b\)</td><td>la lupa: multiplica la ventana por el filtro y suma</td></tr>
<tr><td>Tamaño del mapa</td><td>\(n - k + 1\)</td><td>foto de n, filtro de k: 28 − 3 + 1 = 26</td></tr>
<tr><td>Parámetros de Conv2D</td><td>\(\text{filtros}\times(k\cdot k\cdot \text{canales} + 1)\)</td><td>16 × (3·3·1 + 1) = 160</td></tr>
<tr><td>Parámetros de Dense</td><td>\(n_{in}\cdot n_{out} + n_{out}\)</td><td>784 × 128 + 128 = 100 480</td></tr>
<tr><td>MaxPooling 2 × 2</td><td>\(\max\) de cada ventana</td><td>el mapa queda de la mitad</td></tr>
<tr><td>Softmax</td><td>\(p_k = e^{z_k} / \sum_j e^{z_j}\)</td><td>10 puntajes → 10 probabilidades que suman 1</td></tr>
<tr><td>Libreta de la RNN</td><td>\(h_t = \tanh(w\,x_t + u\,h_{t-1} + b)\)</td><td>lo nuevo + lo anotado, aplastado</td></tr>
<tr><td>Olvido</td><td>\(0.5^{10} \approx 0.001\)</td><td>la culpa se multiplica en cada paso hacia atrás</td></tr>
<tr><td>Cinta de la LSTM</td><td>\(c_t = f_t\,c_{t-1} + i_t\,\tilde c_t\)</td><td>lo que se conserva + lo que se anota</td></tr>
<tr><td>Atención</td><td>\(\alpha = \text{softmax}(\mathbf{q}\cdot\mathbf{k}),\ \text{salida} = \sum \alpha\,\mathbf{v}\)</td><td>a quién mirar, y cuánto</td></tr>
<tr><td>Costo de la atención</td><td>\(n \times n\)</td><td>1 000 palabras → 1 000 000 de comparaciones</td></tr>
<tr><td>Forma de una imagen</td><td>(fotos, alto, ancho, canales)</td><td>(60000, 28, 28, 1)</td></tr>
<tr><td>Forma de una secuencia</td><td>(ejemplos, pasos, datos por paso)</td><td>(2000, 12, 1)</td></tr>
</table>"""
S.append(('formulas', 'Σ', 'Fórmulas de bolsillo', FORMULAS))

GLOS = [
    ("Arquitectura", "La forma de organizar las capas de una red. Cada una supone algo sobre los datos."),
    ("Atención", "Mecanismo con el que cada elemento compara su consulta con las claves de todos y mezcla sus valores según esos pesos."),
    ("Caché KV", "La memoria donde un Transformer guarda las claves y valores de las palabras anteriores al generar texto; crece con el texto."),
    ("Canal", "Cada capa de color o de mapas de una imagen: 1 en blanco y negro, 3 en color (rojo, verde, azul)."),
    ("Clave, consulta y valor", "En la atención: la consulta es lo que busca una palabra, la clave dice de qué trata cada palabra y el valor es lo que aporta."),
    ("CNN (red convolucional)", "Red que recorre la imagen con filtros pequeños; supone que lo cercano importa y que el mismo patrón puede estar en cualquier parte."),
    ("Comparación justa", "Comparar modelos con los mismos datos, la misma división y un presupuesto parecido, con más de una semilla."),
    ("Compartir pesos", "Usar los mismos pesos en muchas posiciones: el filtro en toda la foto (CNN) o la celda en todos los pasos (RNN)."),
    ("Compuerta", "En la LSTM, una sigmoide entre 0 y 1 que decide cuánto olvidar, guardar o mostrar; funciona como una válvula."),
    ("Conv2D", "Capa de Keras que aplica varios filtros a una imagen y produce un mapa por filtro."),
    ("Convolución", "Pasar un filtro por cada ventana de la imagen, multiplicar, sumar y anotar el resultado en un mapa."),
    ("Densa (red)", "Red en la que cada neurona está conectada con todas las de la capa anterior; supone que todo se relaciona con todo."),
    ("Desenrollar", "Dibujar la RNN paso por paso: una cadena de celdas iguales que se pasan la libreta."),
    ("Estado oculto (h)", "La libreta de la RNN: un vector de números que resume lo leído hasta ahora."),
    ("Fashion-MNIST", "Conjunto de 70 000 fotos de ropa de 28 × 28 en 10 clases, publicado por Zalando en 2017."),
    ("Filtro (kernel)", "Tablita de pesos (por ejemplo 3 × 3) que detecta un patrón local, como un borde."),
    ("Flatten", "Capa de Keras que pone una tabla en una sola fila (aplanar)."),
    ("GAN", "Red generativa antagónica: un falsificador y un detective que compiten; el falsificador aprende a crear datos realistas."),
    ("GNN (red de grafos)", "Red para datos conectados: cada nodo mezcla la información de sus vecinos en varias rondas."),
    ("GRU", "Variante de la LSTM con dos compuertas (2014)."),
    ("Híbrido (modelo)", "Modelo que mezcla muchas capas recurrentes baratas con unas pocas capas de atención, como Jamba o Nemotron-H."),
    ("Línea base", "Modelo sencillo con el que se compara: si la arquitectura nueva no le gana con justicia, no vale la pena."),
    ("LSTM", "Red recurrente con una cinta de memoria y tres compuertas (Hochreiter y Schmidhuber, 1997)."),
    ("Mamba", "Modelo de espacio de estados (2023): una recurrencia moderna que se entrena en paralelo y decide qué anotar."),
    ("Mapa de activación", "La tabla que resulta de pasar un filtro por toda la imagen: se enciende donde está el patrón."),
    ("MaxPooling", "Capa que resume un mapa quedándose con el mayor de cada ventana (por ejemplo 2 × 2)."),
    ("Píxel", "Cada cuadrito de una imagen digital; guarda un número de brillo (0 negro, 255 blanco)."),
    ("Retropropagación a través del tiempo", "La retropropagación de una RNN: la culpa viaja hacia atrás paso por paso y se debilita."),
    ("RNN (red recurrente)", "Red que lee una secuencia paso a paso con la misma celda y actualiza su estado oculto."),
    ("Secuencia", "Datos en los que el orden importa: texto, voz, series de tiempo, pagos mes a mes."),
    ("SimpleRNN", "La capa recurrente más sencilla de Keras: la libreta con tanh."),
    ("Softmax", "Función que convierte varios puntajes en probabilidades que suman 1."),
    ("sparse_categorical_crossentropy", "Pérdida de Keras para varias clases cuando la etiqueta es un número (0 a 9)."),
    ("State space model (SSM)", "Familia de modelos recurrentes modernos, como Mamba, con un estado de tamaño fijo."),
    ("Suposición (sesgo inductivo)", "Lo que una arquitectura da por cierto sobre los datos antes de aprender, como «lo cercano importa»."),
    ("tanh", "Activación con forma de S que da un número entre −1 y 1."),
    ("Token", "Cada pedazo de texto (una palabra o parte de una) que procesa un modelo de lenguaje."),
    ("Transformer", "Arquitectura de 2017 hecha de bloques de atención y capas densas; base de BERT, GPT y casi todos los modelos de lenguaje."),
    ("Vision Transformer (ViT)", "Transformer para imágenes: corta la foto en pedacitos y los trata como palabras."),
]
GLOS.sort(key=lambda t: _u.normalize('NFD', t[0]).encode('ascii', 'ignore').decode().lower())
S.append(('glosario', 'A–Z', 'Glosario', '<input id="search" class="search" type="search" placeholder="Buscar una palabra…" aria-label="Buscar en el glosario"><dl class="glos">' +
          ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS) + '</dl>'))

S.append(('cierre', '✓', '¿Listo? Comprueba lo que aprendiste', """
<p>Juega el quiz final: 10 preguntas cortas, sin cuentas, 25 segundos cada una. Al terminar te dice tu puntaje, qué temas repasar (con enlace a esta guía) y tu avance frente al pre-quiz.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?final">Jugar el quiz final</a><a class="btn ghost" href="../index.html">Volver al inicio</a></div>
<h3>La semana completa en un minuto</h3>
<p class="read">Una red densa sirve para tablas, pero con una foto aplanada no sabe qué píxel es vecino de cuál. La red convolucional mira la foto con una lupa pequeña que recorre toda la imagen: el mismo filtro en todas partes, muchos menos parámetros y más tolerancia a que la prenda se mueva. El pooling resume y softmax reparte la probabilidad entre las clases.</p>
<p class="read">Cuando el orden importa, la red recurrente lee paso a paso y lleva una libreta. Usa la misma celda en cada paso, pero su libreta es pequeña y la culpa que viaja hacia atrás se debilita: lo lejano se olvida. La LSTM agrega compuertas que deciden qué olvidar, qué guardar y qué mostrar.</p>
<p class="read">La atención no recuerda: mira directo. Cada palabra compara su consulta con las claves de todas y mezcla sus valores. Se calcula en paralelo y es la base del Transformer, pero su costo crece con el cuadrado de la longitud. Por eso la tendencia son los híbridos: apuntes resumidos de casi todo y, de vez en cuando, volver al libro. Para elegir, la pregunta es siempre la misma: qué suponen mis datos, qué cuesta y cómo lo compruebo con justicia.</p>
<h3>Preguntas rápidas</h3>
""" + ''.join(ex(q, f'<p>{r}</p>') for q, r in [
    ('¿Qué supone una CNN sobre los datos?', 'Que lo cercano importa y que el mismo patrón puede aparecer en cualquier parte.'),
    ('¿Qué es un mapa de activación?', 'La tabla que resulta de pasar un filtro por toda la imagen: dónde encontró su patrón.'),
    ('¿Por qué la CNN del NB03 tiene 12 810 parámetros y la densa 101 770?', 'Porque la CNN comparte cada filtro en toda la foto; la densa tiene un peso por píxel para cada neurona.'),
    ('¿Qué hace el MaxPooling?', 'Resume cada mapa quedándose con el mayor de cada ventana; el mapa queda de la mitad.'),
    ('¿Qué guarda una RNN?', 'Un estado oculto, su libreta: un resumen de lo leído que se reescribe en cada paso.'),
    ('¿Por qué se olvida?', 'Porque la culpa que viaja hacia atrás se multiplica por un número pequeño en cada paso.'),
    ('¿Qué agrega la LSTM?', 'Una cinta de memoria y tres compuertas: olvidar, guardar y mostrar.'),
    ('¿Qué hace la atención?', 'Compara la consulta de cada palabra con las claves de todas y mezcla sus valores según esos pesos.'),
    ('¿Cuál es el precio de la atención?', 'Crece con el cuadrado de la longitud: 1 000 palabras, un millón de comparaciones.'),
    ('¿Qué es un modelo híbrido?', 'Uno que mezcla muchas capas recurrentes baratas con unas pocas de atención.'),
]) + """
<p>En Canvas te esperan el test de la semana, la lectura de tendencia con su encuesta y el entregable; las fechas exactas están allí.</p>
"""))

# ------------------------------------------------------------------ assemble
body, toc = '', []
for sid, n, title, inner in S:
    kick = {'inicio': chip('Empieza aquí', 'amber'), 'formulas': chip('Resumen', 'purple'), 'glosario': chip('Referencia', 'purple'),
            'cierre': chip('Autoevaluación', 'teal')}.get(sid)
    if not kick:
        tema = {'rec': 'Recorderis de la semana 1', 'b00': 'Recorderis · Keras', 'b01': 'Tema 1 · Imágenes', 'b02': 'Tema 2 · Secuencias',
                'b03': 'Tema 2 · La atención', 'b04': 'Cierre de la semana'}[sid]
        kick = chip(tema) + (chip('Pendiente de la semana 1', 'amber') if sid == 'b00' else '')
    body += f'<section id="inicio">{inner}</section>' if sid == 'inicio' else section(sid, kick, title, inner)
    toc.append((sid, n, title))

html = page('Guía de estudio · Semana 2 · Deep Learning UIDE',
            'Guía de estudio de la semana 2 de Neural Networks: Deep Learning (UIDE): redes convolucionales, recurrentes, LSTM, atención, Transformers y cómo elegir la arquitectura.',
            toc, body, 'dl-uide-w2-guia', topbar=weeks(2, '../../guia/index.html', 'index.html', '../../semana3/guia/index.html'))
(OUT / 'guia').mkdir(parents=True, exist_ok=True)
(OUT / 'guia' / 'index.html').write_text(html)
print('guía semana 2 built', len(html) // 1024, 'KB')
