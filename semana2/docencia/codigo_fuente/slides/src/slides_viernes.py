"""Semana 2 · Encuadre, 00 Recorderis de la semana 1 (con Keras) y Tema 1 (imágenes y CNN).
Organized by themes, not by days: each session simply continues where the previous one stopped."""
import json, pathlib
from kit import slide, head, key, chip, st, demo, count, qr, notes, eq, hist, code

FM = json.loads((pathlib.Path(__file__).parent / 'data' / 'fmnist.json').read_text())
RD, RC = FM['results']['densa'], FM['results']['cnn']


def pct(v, d=1):
    return f'{v * 100:.{d}f}'.replace('.', '.') + ' %'


G0 = 'Encuadre'
GR = '00 · Recorderis: la semana 1'
G1 = 'Tema 1 · Imágenes y CNN'


def section(sid, n, title, lede, items, when, group, blockname, note, shown=None):
    lst = ''.join(f'<span>{i}</span>' for i in items)
    body = (f'<div class="sec"><div class="n">{shown or n}</div><h2>{title}</h2>'
            f'<p class="lede">{lede}</p><div class="lst">{lst}</div><p class="when">{when}</p></div>')
    slide(sid, title, body, note, layout='L-section', block=n, group=group, minutes=0.5, blockname=blockname)


def practice(sid, title, lede, checks, keyname, minutes, group, block, note, extra='', tag='En clase · sin nota', slot=None):
    ck = ''.join(f'<li>{c}</li>' for c in checks)
    body = (head(title, lede, chip(tag, 'ok') + chip(f'{minutes} minutos', 'hint')) +
            f'<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:.4em">'
            f'<div class="col"><h3 class="big" style="font-weight:600">Qué deberías ver</h3><ul class="checks">{ck}</ul>{extra}</div>'
            f'<div class="col" style="align-items:center">{qr(keyname)}'
            f'<p class="txt" style="text-align:center;font-size:1em">Archivo → <b>Guardar una copia en Drive</b><br>y ejecuta primero <b>Configuración</b></p></div></div>')
    slide(sid, title, body, note, block=block, group=group, minutes=slot or minutes)


def rail(items):
    return '<div class="rail" style="--n:%d">' % len(items) + ''.join(
        f'<div class="stn {k}"><i></i><span class="t num">{t}</span><span class="l">{l}</span></div>' for t, l, k in items) + '</div>'


# ======================================================================= 00 · encuadre
slide('portada2', 'De mirar imágenes a leer secuencias', f"""
<div class="cover">
  <div class="left">
    <h1 class="display" style="font-size:4.9em">De mirar imágenes a leer secuencias</h1>
    <p class="lede" style="font-size:1.45em">Neural Networks: Deep Learning · Arquitecturas</p>
    <div class="tags after">{chip('UIDE · Maestría en Ciencia de Datos')}{chip('Semana 2')}</div>
    <p class="meta"><b>Andrés Ordóñez-Bolaños, MSc</b><br>6 y 7 de noviembre de 2026 · Microsoft Teams</p>
  </div>
  <div class="right cv" style="padding:8em 4em 8em 0">{demo('conv', 'fig', mode='cover', img=0, k='vertical', alt='Una lupa de 3 por 3 recorre la foto de un botín y dibuja sus bordes')}</div>
</div>""", notes(
    '<b>Antes de hablar:</b> verifica que la grabación está corriendo. Comparte esta ventana y abre la vista del presentador con <b>P</b>.',
    'Bienvenida: «La semana pasada construimos una neurona y una red para datos de tabla. Esta semana le enseñamos a la red a <b>mirar imágenes</b> (Tema 1) y a <b>leer secuencias</b> (Tema 2)».',
    'La animación de la derecha es lo que vamos a entender en el Tema 1: una lupa de 3 × 3 recorre la foto de un botín y, a la derecha, va dibujando dónde encontró bordes. Es una red convolucional en acción.'),
    layout='L-cover', block='E', group=G0, minutes=1, blockname='Encuadre')

ROUTE = [('00', 'Recorderis', 'La semana 1 en una sola red y Keras en 4 pasos, lo que quedó pendiente.', 'NB02 en casa', '≈ 25 min', 'az'),
         ('Tema 1', 'Cómo mira una red una imagen', 'La lupa de 3 × 3, los filtros, compartir pesos y la CNN contra la densa.', 'NB03 en clase', '≈ 1 h 20', 'am'),
         ('Tema 2', 'Cómo lee una red una secuencia', 'La libreta de la RNN, el olvido, la LSTM, la atención y la tendencia.', 'NB04 en clase', '≈ 1 h 50', 'mi'),
         ('Cierre', 'Elegir la arquitectura', '¿Qué arquitectura le pondrías?, tu proyecto y el quiz final.', 'Quiz final', '≈ 45 min', 'li')]
slide('ruta2', 'La semana en dos temas', head('La semana en dos temas', 'Dos preguntas: <b>¿cómo mira una red una imagen?</b> y <b>¿cómo lee una red una secuencia?</b> Antes, un recorderis; al final, cómo elegir.') +
      '<div class="route4">' + ''.join(st(i + 1, f'<div class="rt {k}"><span class="k num">{a}</span><h3>{t}</h3><p>{d}</p><div class="ft"><span class="chip">{nb}</span><span class="du num">{du}</span></div></div>')
                                       for i, (a, t, d, nb, du, k) in enumerate(ROUTE)) + '</div>' +
      st(4, '<div class="keybar" style="margin-top:1.4em"><span>Cada sesión <b>sigue donde terminó la anterior</b>: el orden importa, el reloj no. Las prácticas son en clase y <b>no tienen nota</b>.</span></div>'),
      notes('La semana tiene dos temas y no está atada a los días. Si el Tema 1 se alarga, el Tema 2 empieza en la sesión siguiente: no pasa nada.',
            'Recorderis: 10 minutos de la semana 1 y lo que quedó pendiente, Keras. Tema 1: la red convolucional (con el NB03). Tema 2: la red recurrente, su olvido y la atención (con el NB04 y la lectura de tendencia). Cierre: elegir la arquitectura y el quiz final.',
            'Recalca: <b>las prácticas son en clase y no tienen nota</b>. Los notebooks traen todo el código escrito: se leen, se ejecutan y se responden preguntas para pensar.',
            'Las duraciones son aproximadas (incluyen las prácticas) y suman unas 4 h 20 de las 6 horas de la semana: hay colchón a propósito, para preguntas y para lo que se alargue.'),
      block='E', group=G0, minutes=1, steps=4)

slide('prequiz2', 'Pre-quiz: ¿de dónde partimos?', head('Antes de empezar: ¿de dónde partimos?', '8 preguntas cortas tipo Kahoot. <b>No es nota</b>: es tu punto de partida para medir cuánto avanzas esta semana.') + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:1em">
  <ol class="steps-list" style="gap:1.2em">
    {st(1, '<span class="k">1</span><span>Escanea el código o abre <b>deeplearningweek1.vercel.app/?pre2</b></span>', 'li')}
    {st(2, '<span class="k">2</span><span>Escribe tu nombre (el mismo de la semana 1) y responde rápido: <b>más rapidez, más puntos</b></span>', 'li')}
    {st(3, '<span class="k">3</span><span>Al final, copia tu código y <b>pégalo en el chat de Teams</b></span>', 'li')}
    {st(3, '<span class="k" style="background:var(--mint);color:var(--night)">✓</span><span>Si no sabes una, elige la que te parezca. Equivocarse aquí es parte del plan.</span>', 'li')}
  </ol>
  <div class="center">{qr('pre2')}</div>
</div>""", notes(
    'Dales 6 minutos. Cuando la mayoría haya pegado su código en el chat, sigue.',
    'Cinco de las ocho preguntas son las <b>ideas clave</b> de la semana 2 y vuelven en el quiz final del cierre. El panel <b>Resultados_quiz.html</b> de la semana 2 lee los códigos del chat.',
    '<span class="q">Pregunta para el chat:</span> «¿Cuál les pareció más difícil?» Anota la respuesta.'),
    block='E', group=G0, minutes=6)

IDEAS = ['Cada arquitectura es una suposición sobre los datos', 'Qué hace un filtro: una lupa que recorre la imagen',
         'Por qué una CNN necesita muchos menos parámetros', 'Qué guarda una RNN y por qué se olvida', 'Qué hace la atención y cuál es su precio']
slide('metas2', 'Las 5 ideas clave de la semana', head('Al terminar la semana vas a poder explicar estas 5 ideas', 'Las medimos dos veces: en este pre-quiz y en el quiz final del cierre.') +
      '<ol class="steps-list" style="gap:1.05em;margin-top:.4em">' + ''.join(
          st(i + 1, f'<span class="k key">{i + 1}</span><span class="big" style="color:var(--ink)">{t}</span>', 'li') for i, t in enumerate(IDEAS)) + '</ol>' +
      st(5, '<p class="say" style="margin-top:1.2em">Tema 1: <b>ideas 1, 2 y 3</b>. Tema 2: <b>ideas 4 y 5</b>. Cada una tiene su lámina con la etiqueta amarilla <b>Idea clave</b>.</p>'),
      notes('Esta es la promesa de la semana. La primera es el hilo de todo: <b>cada arquitectura es una suposición sobre cómo están organizados los datos</b>. Las demás son consecuencias.',
            'Si al final alguien no puede explicar alguna con sus palabras, la guía de estudio de la semana 2 tiene una sección para cada una.'),
      block='E', group=G0, minutes=1)

# ======================================================================= 00 · recorderis de la semana 1 (con Keras, lo que quedó pendiente)
section('b00', '00', 'Recorderis: la semana 1', 'Antes de mirar imágenes, repasemos en 10 minutos cómo aprende una red. Y terminamos lo que quedó pendiente: Keras.',
        ['La semana 1 en una red', 'Tres preguntas', 'Motor y volante', 'Los 4 pasos', 'Mírala aprender', 'El NB02 en casa'], '≈ 25 minutos', GR, '00 · Recorderis: la semana 1',
        notes('Un repaso corto para conectar: todo lo de esta semana se apoya en la neurona, la pérdida y el gradiente de la semana 1.',
              'Después del repaso viene lo que no alcanzamos: Keras en 4 pasos. Es corto a propósito: en el NB03 usamos los mismos 4 pasos con capas nuevas.'))

# ---- the week 1 in one chain (each node with its week-1 analogy and number)
CHAIN = [('Datos en una tabla', 'cada fila, un socio; cada columna, un dato', 'la <b>etiqueta</b> es la respuesta conocida: el comité de crédito', 'az'),
         ('Neurona', 'z = w·x + b', 'tu nota final: cada nota por lo que pesa, menos la exigencia · socio A: <b class="num">z = 2.81</b>', 'am'),
         ('Activación', 'interruptor · regulador · válvula', 'la sigmoide da una probabilidad; la ReLU <b>dobla la línea</b>', 'am'),
         ('Red en capas', 'una neurona = una línea', 'XOR necesita <b>dos</b> neuronas ocultas', 'mi'),
         ('Error y pérdida', 'error = real − predicho', 'la pérdida es un solo número: casas de Quito <b class="num">MSE = 132.25</b>; la BCE del meteorólogo «seguro»', 'co'),
         ('Descenso de gradiente', 'peso nuevo = peso − η · pendiente', 'bajar el Cotopaxi con neblina; <b>η</b> es el largo del paso', 'co'),
         ('Retropropagación', 'repartir la culpa hacia atrás', 'los engranajes: la regla de la cadena', 'li'),
         ('Keras', 'construir · compilar · entrenar · predecir', 'TensorFlow es el motor; Keras, el volante (lo vemos ahora)', 'az'),
         ('Métricas', '87 % puede no valer nada', 'no encontró a ningún moroso: mira la <b>matriz de confusión</b>', 'mi')]
slide('recorderis', 'La semana 1 en una sola red', head('La semana 1 en una sola red', 'Nueve ideas en cadena: cada una resuelve el problema que dejó la anterior.') +
      '<div class="chain9">' + ''.join(st(i + 1, f'<div class="ch {k}"><span class="i num">{i + 1}</span><h3>{t}</h3><span class="f">{f}</span><p>{a}</p></div>') for i, (t, f, a, k) in enumerate(CHAIN)) + '</div>' +
      st(10, '<div class="keybar" style="margin-top:1em"><span>Hasta ahora los datos eran <b>tablas</b>. ¿Y si son <b>fotos</b>? ¿Y si son <b>frases</b>?</span></div>'),
      notes('Un clic por idea. Antes de cada clic, pregunta a la clase: «¿qué venía después?». Que lo digan ellos; la lámina solo confirma.',
            '1 · Los datos: una tabla con características y la etiqueta (la respuesta conocida). 2 · La neurona: multiplica cada dato por su peso, suma y añade el sesgo; como la nota final del curso. 3 · La activación decide la salida y dobla la línea. 4 · Una neurona solo traza una línea: para XOR hacen falta capas.',
            '5 · El error es real − predicho, uno por caso; la pérdida resume todos en un número. 6 · El gradiente dice hacia dónde bajar; η es el largo del paso. 7 · La retropropagación reparte la culpa hacia atrás, capa por capa. 8 · Keras hace todo eso en diez líneas (lo vemos en dos minutos). 9 · Y la exactitud sola engaña: el modelo del 87 % no encontraba morosos.',
            'Paso 10, el puente de la semana: <span class="q">«Hasta ahora los datos eran tablas. ¿Y si son fotos? ¿Y si son frases?»</span> Esa pregunta abre el Tema 1 y el Tema 2.'),
      block='00', group=GR, minutes=6, steps=10)

QA3 = [('¿Qué hace una neurona con sus datos?', 'Multiplica cada dato por su peso, suma todo y añade el sesgo: <b class="num">z = w·x + b</b>.', 'Como tu nota final: cada nota pesa distinto y al final se compara con la exigencia.'),
       ('Si la pendiente de un peso es <b class="num">+4</b>, ¿el peso sube o baja?', '<b>Baja.</b> Caminamos en contra de la pendiente.', 'Con η = 0.1, el peso 2 pasa a 2 − 0.1 · 4 = <b class="num">1.6</b>. La pendiente apunta cuesta arriba.'),
       ('Un modelo dice «al día» a todos los socios y acierta el <b class="num">87 %</b>. ¿Es bueno?', '<b>No.</b> No encuentra a ningún moroso.', 'La exactitud engaña cuando lo que buscas es poco frecuente: mira la matriz de confusión y el recall.')]
slide('recorderis-preguntas', 'Tres preguntas para calentar', head('Tres preguntas para calentar', 'Respondan en el chat <b>antes</b> de que aparezca la respuesta. Vienen del quiz de la semana 1.') +
      '<div class="qa3">' + ''.join(f'<div class="qr3"><span class="n num">{i + 1}</span><p class="q">{q}</p>' + st(i + 1, f'<div class="a"><p class="ans">{a}</p><p class="why">{w}</p></div>') + '</div>' for i, (q, a, w) in enumerate(QA3)) + '</div>',
      notes('Práctica de recuerdo: es lo que mejor fija lo aprendido. Lee la pregunta, espera 20 segundos de respuestas en el chat y solo entonces avanza.',
            '1 · La neurona: suma con pesos más el sesgo. Si alguien dice «elige el dato más grande», es el error típico del pre-quiz de la semana 1.',
            '2 · La pendiente +4 dice que si el peso sube, la pérdida sube: por eso el paso va al revés, hacia abajo. Con η = 0.1: 2 − 0.4 = 1.6.',
            '3 · El 87 % de la trampa del comité: 87 de cada 100 socios estaban al día, así que decir siempre «al día» acierta 87 % sin encontrar un solo moroso.'),
      block='00', group=GR, minutes=4, steps=3)

ICON = {
    'py': '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M14 12 L5 20 L14 28 M26 12 L35 20 L26 28 M22 9 L18 31"/></svg>',
    'wheel': '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="15"/><circle cx="20" cy="20" r="4"/><path d="M5.5 17 L16 19 M24 19 L34.5 17 M20 24 L20 35"/></svg>',
    'engine': '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="6"/><path d="M20 4 L20 9 M20 31 L20 36 M4 20 L9 20 M31 20 L36 20 M8.7 8.7 L12.2 12.2 M27.8 27.8 L31.3 31.3 M8.7 31.3 L12.2 27.8 M27.8 12.2 L31.3 8.7"/><circle cx="20" cy="20" r="12"/></svg>',
    'chip': '<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="10" y="10" width="20" height="20" rx="3"/><path d="M15 10 L15 5 M20 10 L20 5 M25 10 L25 5 M15 30 L15 35 M20 30 L20 35 M25 30 L25 35 M10 15 L5 15 M10 20 L5 20 M10 25 L5 25 M30 15 L35 15 M30 20 L35 20 M30 25 L35 25"/></svg>',
}
LEVELS = [('py', 'Tú · Python', 'escribes qué quieres en Colab', ''),
          ('wheel', 'Keras', '<b>el volante</b>: capas, pérdidas y <code>fit</code>', 'hot'),
          ('engine', 'TensorFlow', '<b>el motor</b>: tensores y culpas calculadas solas', ''),
          ('chip', 'La máquina', 'la CPU o GPU hace las multiplicaciones', '')]
STACK = '<div class="stackx">' + '<span class="dn" aria-hidden="true">↓</span>'.join(
    st(i + 1, f'<div class="lv {k}">{ICON[ic]}<b>{t}</b><span>{d}</span></div>') for i, (ic, t, d, k) in enumerate(LEVELS)) + '</div>'
IMPORTS = code("""
import tensorflow as tf   # the engine
import keras              # the wheel
from keras import layers  # the pieces
""", hl='1:2-3;2:1;3:2-3;4:1-3')
slide('motor-volante', 'TensorFlow y Keras: el motor y el volante', head('TensorFlow y Keras: el motor y el volante', 'Dos librerías de Python que ya vienen en Colab. Con Keras manejas; TensorFlow hace las cuentas por debajo, incluida la retropropagación.') + f"""
<div class="split" style="grid-template-columns:6fr 6fr;gap:2.4em">
  {STACK}
  <div class="col" style="gap:1em">
    {IMPORTS}
    <div class="analog"><span class="t">Puedes manejar sin abrir el capó</span><p>Keras arma y entrena una red en diez líneas. Saber que existe el motor ayuda cuando algo falla: por eso la semana pasada hicimos las cuentas a mano.</p></div>
    {hist('2015', 'nacen Keras (François Chollet, marzo) y TensorFlow (Google, noviembre)')}
  </div>
</div>""", notes(
    '<b>Esto quedó pendiente de la semana 1.</b> TensorFlow y Keras son librerías de Python: código que otros escribieron y que importamos para no reinventarlo.',
    '<b>TensorFlow</b> (Google, 2015) es el motor: guarda los números en «tensores», calcula las culpas solo (la retropropagación) y puede usar la GPU. <b>Keras</b> (François Chollet, 2015; actualmente Keras 3) es el volante: capas listas, <code>compile</code> y <code>fit</code>.',
    'Las tres líneas de <code>import</code> abren el NB02 y también el NB03 del Tema 1.'),
    block='00', group=GR, minutes=2)

CODE_K = code("""
model = keras.Sequential([
    keras.Input(shape=(2,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")])
model.compile(optimizer=keras.optimizers.Adam(0.01),
              loss="binary_crossentropy",
              metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=60,
                    batch_size=32, validation_split=0.2)
p = model.predict(NUEVOS)
""", hl='1:1-5;2:6-8;3:9-10;4:11', cls='sm')
STEPS4 = [('1 · Construir', 'apilar capas como LEGO: ReLU dentro, sigmoide a la salida'),
          ('2 · Compilar', 'Adam baja la montaña; la BCE mide qué tan mal vamos'),
          ('3 · Entrenar', '<code>fit</code>: adelante, culpa hacia atrás y un paso, 60 vueltas'),
          ('4 · Predecir', 'una probabilidad; con el umbral 0.5, sí o no')]
slide('keras-4pasos', 'Keras en 4 pasos', head('Keras en 4 pasos: construir, compilar, entrenar y predecir', 'El problema de las lunas: 600 puntos de dos clases, cada uno con 2 datos. La misma receta sirve para fotos (Tema 1) y para secuencias (Tema 2).') + f"""
<div class="split" style="grid-template-columns:7fr 6fr;align-items:start;gap:2em">
  {CODE_K}
  <div class="col" style="gap:.8em">
    """ + ''.join(st(i + 1, f'<div class="mapi" style="font-size:1.08em"><span>{a}</span><b>{b}</b></div>') for i, (a, b) in enumerate(STEPS4)) + """
    """ + st(4, '<p class="say">Diez líneas, <b class="num">337</b> parámetros y <b class="num">95 %</b> en el examen final.</p>') + """
  </div>
</div>""", notes(
    'Avanza un paso por clic: se ilumina el bloque de código y su explicación.',
    '<b>Construir</b>: <code>Sequential</code> apila capas en orden. <code>Input(shape=(2,))</code>: cada ejemplo trae 2 números. <code>Dense(16, activation="relu")</code>: 16 neuronas, cada una con un peso por cable y su sesgo. Salida: 1 neurona con sigmoide (sí o no). Parámetros: 48 + 272 + 17 = 337.',
    '<b>Compilar</b> no entrena todavía: decide cómo se corrige (Adam, paso 0.01), qué se mide (la BCE de la semana 1) y qué se reporta (exactitud).',
    '<b>Entrenar</b>: <code>fit</code> hace todo lo de la semana 1 solo: adelante, pérdida, culpas hacia atrás y un paso. 480 ejemplos de entrenamiento; con <code>validation_split=0.2</code> se reservan 96 para el simulacro y quedan 384: 12 lotes de 32 por época, 720 pasos en 60 épocas.',
    '<b>Predecir</b>: probabilidad → umbral → decisión. <span class="q">Pregunta:</span> «¿En qué línea está la retropropagación?» (dentro de <code>fit</code>).'),
    block='00', group=GR, minutes=4)

slide('keras-fit2', 'Mira a la red aprender', head('Mira a la red aprender: <code>fit</code> en vivo') +
      code("""
history = model.fit(X_train, y_train, epochs=60, batch_size=32, validation_split=0.2)
""", cls='sm') + '<p class="cl" style="margin:.6em 0 .9em"><code>epochs=60</code> 60 vueltas · <code>batch_size=32</code> lotes de 32 · <code>validation_split=0.2</code> el simulacro que la red no estudia</p>' +
      demo('moons', 'fill', mode='fit'),
      notes('Datos reales de la Parte F del NB02. Pulsa <b>Entrenar 60 épocas</b> (o avanza: arranca solo).',
            'Izquierda: la zona ámbar es donde la red dice «clase 1»; la línea blanca es su frontera (probabilidad 0.5). Al principio adivina; en pocas épocas la frontera se dobla para seguir las lunas.',
            'Derecha: la pérdida de entrenamiento (ámbar) y la de validación (blanca punteada) bajan <b>juntas</b>: aprendió, no memorizó. Si la blanca subiera mientras la ámbar baja, estaría memorizando (sobreajuste, semana 3).',
            '<span class="q">Pregunta:</span> «¿Qué le pasaría a la frontera si la red no tuviera ReLU?» (sería una línea recta: la semana 1).'),
      block='00', group=GR, minutes=4, steps=1)

practice('nb02-casa', 'El NB02 queda para casa', 'Si en la semana 1 no alcanzaste, empieza por las partes <b>E</b> y <b>F</b>: son las de esta lámina y la anterior.',
         ['<b>E</b> · Keras paso a paso: <b>XOR resuelto</b> con 33 parámetros', '<b>F</b> · Las lunas: <b>337</b> parámetros y <b>95 %</b> en el examen final',
          '<b>Experimento 2</b> · los círculos con más de <b>90 %</b>'], 'nb02', 30, GR, '00',
         notes('No lo hacemos en clase: queda para casa. Las partes A a D (las cuentas a mano) son opcionales si ya entendieron la retropropagación.',
               '<b>Puente al Tema 1:</b> las lunas eran una tabla de 2 columnas. ¿Qué pasa si la entrada es una foto de 784 números? La receta de Keras es la misma; cambian las capas.'),
         extra=st(1, '<div class="keybar" style="margin-top:1em"><span><b>Puente:</b> las lunas eran una tabla de <b>2 columnas</b>. ¿Y si la entrada es una foto de <b>784 números</b>?</span></div>'),
         tag='En casa · sin nota', slot=2)

# ======================================================================= 01 · imágenes
section('b01', '01', 'Cómo mira una red una imagen', 'Una foto pequeña ya tiene 784 números. ¿Conectamos todos con todos, o miramos de cerca?',
        ['Una foto son números', 'La densa aplana', 'La suposición', 'La lupa', 'Mapas', 'Compartir', 'Pooling', 'En Keras', 'Softmax', 'Práctica NB03'], 'Tema 1 · ≈ 1 h 20 con el NB03', G1, 'Tema 1 · Imágenes y CNN',
        notes('<b>Tema 1.</b> Aquí están las <b>ideas clave 1, 2 y 3</b>. Termina con la práctica NB03, el duelo densa contra CNN y un cierre del tema.',
              'Si la sesión se acaba en medio del tema, no pasa nada: la siguiente sigue donde quedamos.'), shown='T1')

slide('imagen-numeros', 'Una imagen es una tabla de números', head('Una imagen es una tabla de números', '<b>Fashion-MNIST</b> (Zalando, 2017): 70 000 fotos de ropa de 28 × 28 píxeles en 10 clases. Cada píxel es un brillo: <b>0 es negro y 255 es blanco</b>.') +
      demo('pixels', 'fill') +
      st(2, '<div class="keybar" style="margin-top:.6em"><span>28 × 28 = <b class="num">784</b> números por foto. La foto <b>es</b> esa tabla: no hay nada más.</span></div>'),
      notes('Empieza con la foto real: es la primera foto del examen del NB03, un botín. Paso 1: aparece el recuadro y, a la derecha, sus números. Pasa el mouse por la foto para mover el recuadro: en el fondo hay ceros; en la prenda, números grandes.',
            'Los botones de abajo cambian de prenda: camiseta, bolso, zapatilla, pantalón, vestido, camisa. Son las 10 clases de Fashion-MNIST.',
            'Paso 2: la conclusión. Para la red, una foto es una tabla de 28 × 28 = 784 números. En el NB03: <code>x_train.shape → (60000, 28, 28)</code>.',
            '<span class="q">Pregunta:</span> «¿Cuántos números tendría una foto de su celular de 12 megapíxeles, a color?» (12 millones × 3 colores = 36 millones). Por eso importa cómo la miramos.'),
      block='01', group=G1, minutes=2)

slide('aplanar', 'La red densa aplana la foto', head('La red densa aplana la foto y pierde la vecindad', 'Una <code>Dense</code> conecta <b>cada</b> píxel con <b>cada</b> neurona. Funciona, pero no sabe qué píxel está al lado de cuál.') +
      demo('flatten', 'fill'),
      notes('Paso 1: la animación aplana la foto fila por fila: así la recibe una capa densa (<code>layers.Flatten()</code>). 784 números en fila.',
            f'Paso 2: el experimento más revelador del NB03. Mezclamos los píxeles de todas las fotos con la misma regla. Para nosotros es ruido; para la densa es <b>el mismo problema</b>: acierta {pct(RD["mezclada"])} (sin mezclar, {pct(RD["test"])}). Nunca usó la vecindad.',
            'Paso 3: cada neurona tiene 784 pesos, uno por píxel. Con 128 neuronas: 784 × 128 + 128 = <b>100 480</b> parámetros solo en la primera capa.',
            '<span class="q">Pregunta:</span> «Si la red no sabe quién es vecino de quién, ¿cómo reconoce un borde?» Esa pregunta nos lleva a la idea clave 1.'),
      block='01', group=G1, minutes=3, steps=3)

ICDENSE = ('<svg viewBox="0 0 200 160" aria-hidden="true">' + ''.join(f'<line x1="30" y1="{20 + i * 30}" x2="170" y2="{20 + j * 40}" stroke="#4abaf4" stroke-width="2" opacity=".5"/>' for i in range(5) for j in range(4)) +
           ''.join(f'<circle cx="30" cy="{20 + i * 30}" r="9" fill="#0f1a29" stroke="#4abaf4" stroke-width="3"/>' for i in range(5)) +
           ''.join(f'<circle cx="170" cy="{20 + j * 40}" r="11" fill="#4abaf4"/>' for j in range(4)) + '</svg>')
ICCNN = ('<svg viewBox="0 0 200 160" aria-hidden="true">' + ''.join(f'<rect x="{20 + c * 20}" y="{10 + r * 20}" width="18" height="18" rx="3" fill="#182436"/>' for r in range(7) for c in range(8)) +
         '<rect x="78" y="48" width="62" height="62" rx="6" fill="#ffb541" fill-opacity=".2" stroke="#ffb541" stroke-width="4"/>'
         '<circle cx="109" cy="79" r="40" fill="none" stroke="#f1f6fa" stroke-width="5"/><line x1="138" y1="108" x2="170" y2="140" stroke="#f1f6fa" stroke-width="9" stroke-linecap="round"/></svg>')
ICRNN = ('<svg viewBox="0 0 200 160" aria-hidden="true"><rect x="40" y="16" width="120" height="128" rx="10" fill="#0f1a29" stroke="#64eab7" stroke-width="4"/>' +
         ''.join(f'<line x1="58" y1="{44 + i * 22}" x2="{142 - (i % 2) * 24}" y2="{44 + i * 22}" stroke="#64eab7" stroke-width="4" stroke-linecap="round" opacity=".7"/>' for i in range(5)) +
         '<path d="M10 150 L190 150" stroke="#b6c6d7" stroke-width="3"/><path d="M178 142 L192 150 L178 158" fill="none" stroke="#b6c6d7" stroke-width="3"/></svg>')
CARDS = [('Densa', ICDENSE, 'Supone que <b>todo se relaciona con todo</b>.', 'Tablas: los socios de una cooperativa, cada columna un dato.', 'az'),
         ('Convolucional · CNN', ICCNN, 'Supone que <b>lo cercano importa</b> y que el mismo patrón puede estar <b>en cualquier parte</b>.', 'Imágenes: una lupa que recorre la foto.', 'am'),
         ('Recurrente · RNN', ICRNN, 'Supone que <b>el orden importa</b> y resume lo leído en una libreta.', 'Secuencias: frases, pagos de cada mes. En el Tema 2.', 'mi')]
slide('suposicion', 'Cada arquitectura es una suposición', head('Cada arquitectura es una suposición sobre los datos', 'Una arquitectura no es solo una lista de capas: es una apuesta sobre <b>cómo están organizados</b> los datos.', key(1)) +
      '<div class="cards3">' + ''.join(st(i + 1, f'<div class="acard{" hot" if k == "am" else ""}"><div class="ic">{ic}</div><h3 class="{k}">{t}</h3><p class="sup">{s}</p><p class="ex">{e}</p></div>') for i, (t, ic, s, e, k) in enumerate(CARDS)) + '</div>' +
      st(4, '<div class="keybar" style="margin-top:.8em"><span>Si la suposición es cierta, la red <b>aprende más con menos</b>. Si no lo es, le estorba. Elegir arquitectura = elegir qué suponemos.</span></div>'),
      notes('<b>Idea clave 1: el hilo de toda la semana.</b> La frase viene de la lectura de tendencia: «una arquitectura no es solo una lista de capas: es una suposición sobre cómo están organizados los datos».',
            'Densa: cualquier dato puede relacionarse con cualquier otro. Perfecto para una tabla, donde el orden de las columnas no significa nada.',
            'CNN: un borde, una esquina o una textura se reconocen mirando una ventana pequeña, y el mismo detector sirve en cualquier parte de la foto. Analogía de la lectura: <b>una lupa que recorre toda la imagen</b>.',
            'RNN: lee elemento por elemento y va guardando lo leído en una <b>libreta pequeña</b>. Es el Tema 2.',
            '<span class="q">Pregunta:</span> «Los datos de su proyecto de titulación, ¿son tabla, imagen o secuencia? ¿Qué suposición tendría sentido?»'),
      block='01', group=G1, minutes=3)

slide('filtro', 'La lupa: un filtro recorre la imagen', head('La lupa: un filtro de 3 × 3 recorre la imagen', 'En cada lugar multiplica <b>9 píxeles por 9 pesos</b> y suma. Donde encuentra su patrón, el resultado es grande. Eso es una <b>convolución</b>.', key(2)) +
      demo('conv', 'fill', img=0, k='vertical'),
      notes('<b>Idea clave 2.</b> Arranca solo: la lupa (el recuadro ámbar) recorre el botín fila por fila. En el centro: los 9 píxeles bajo la lupa, los 9 pesos del filtro y la suma. A la derecha se va llenando el <b>mapa</b>: un número por posición.',
            'Filtro de <b>borde vertical</b>: −1 a la izquierda, 0 al centro, +1 a la derecha. Si a la izquierda está oscuro y a la derecha claro, la suma es positiva (ámbar); al revés, negativa (azul). En el fondo negro o dentro de la prenda (todo parejo) da casi 0.',
            'Cambia a <b>borde horizontal</b>: se encienden la suela y la parte de arriba. <b>Desenfoque</b>: promedia los 9 vecinos y el botín sale borroso.',
            'La foto es de 28 × 28 y el mapa de <b>26 × 26</b>: la lupa de 3 × 3 no puede salirse del borde.',
            '<span class="q">Pregunta:</span> «¿Dónde esperan que se encienda un filtro de borde vertical en una foto de un pantalón?» (en los costados de cada pierna).'),
      block='01', group=G1, minutes=4)

# ---- the hand count with the real window (rows 11-13, cols 13-15 of the boot)
PX = FM['samples'][0]['px']
WIN = [[PX[r][c] / 255 for c in range(13, 16)] for r in range(11, 14)]
KV = [[-1, 0, 1]] * 3
PROD = [[WIN[r][c] * KV[r][c] for c in range(3)] for r in range(3)]
SUMV = sum(sum(r) for r in PROD)


def m3(vals, fmt, color=None, bg=None):
    cells = ''
    for r in vals:
        for v in r:
            sty = ''
            if bg:
                g = int(15 + (241 - 15) * v)
                sty = f'background:rgb({g},{int(26 + (246 - 26) * v)},{int(41 + (250 - 41) * v)});color:{"#07101c" if v > .55 else "#b6c6d7"}'
            elif color:
                sty = f'color:{color(v)}'
            cells += f'<span style="{sty}">{fmt(v)}</span>'
    return f'<div class="m3{" k" if not bg else ""}">{cells}</div>'


sgn = lambda v: ('+' if v > 0 else '−' if v < 0 else '') + f'{abs(v):g}'
col = lambda v: 'var(--amber)' if v > 0 else 'var(--azure)' if v < 0 else 'var(--ink-3)'
HC = (f'<div class="hc">'
      + st(1, f'<div class="blk">{m3(WIN, lambda v: f"{v:.2f}", bg=True)}<span class="cap3">9 píxeles del botín<br>(filas 11–13, columnas 13–15)</span></div>')
      + st(2, '<span class="op">×</span>') + st(2, f'<div class="blk">{m3(KV, sgn, color=col)}<span class="cap3">filtro de borde vertical</span></div>')
      + st(3, '<span class="op">=</span>') + st(3, f'<div class="blk">{m3(PROD, lambda v: (("+" if v > 0 else "−") + f"{abs(v):.2f}") if abs(v) > 1e-9 else "0", color=col)}<span class="cap3">casilla por casilla</span></div>')
      + st(4, '<span class="op">→</span>') + st(4, f'<div class="blk"><span class="bigread am">+{SUMV:.2f}</span><span class="cap3">la suma: un número del mapa</span></div>')
      + '</div>')
slide('filtro-cuenta', 'Un filtro, con números', head('Un filtro, con números', 'La misma cuenta de la neurona de la semana 1: cada dato por su peso, y todo sumado. Solo que ahora los datos son <b>9 píxeles vecinos</b>.', key(2)) + HC +
      st(4, eq([('z', 'un número del mapa', 'out'), ('=', '', 'op'), (r'\textstyle\sum_{9}\ \text{píxel}\cdot\text{peso}', '9 productos sumados', 'x'), ('+', '', 'op'), ('b', 'sesgo', 'w')],
               read=f'la columna de la izquierda (oscura: 0, 0 y 0.35) resta; la de la derecha (clara: 0.54, 0.45 y 0.35) suma. Queda <b>+{SUMV:.2f}</b>: ahí hay un borde «oscuro → claro».', size='.8em')),
      notes('Es exactamente la sección 1 del NB03, con la misma ventana del botín. Avanza un paso por clic.',
            'Paso 1: 9 píxeles ya divididos entre 255 (de 0 a 1). Paso 2: el filtro: −1, 0, +1 en cada fila. Paso 3: casilla por casilla. La columna del medio se multiplica por 0 y no cuenta.',
            f'Paso 4: (0.54 + 0.45 + 0.35) − (0 + 0 + 0.35) ≈ <b>+{SUMV:.2f}</b>. Positivo: el mapa vertical pinta esa posición de ámbar.',
            'Conexión con la semana 1: <b>es una neurona</b> que solo mira 9 píxeles. Lo nuevo es que la misma neurona se pasea por toda la foto.',
            '<span class="q">Pregunta:</span> «Si la ventana estuviera en el fondo negro, ¿cuánto daría la suma?» (0: no hay borde).'),
      block='01', group=G1, minutes=3)

slide('mapas', 'Lo que aprendió la red', head('Muchos filtros, muchos mapas: lo que aprendió la red', 'La primera capa de la CNN del NB03 tiene <b>16 filtros</b>. Nadie se los dio: los aprendió de 54 000 fotos. Cada mapa dice <b>dónde</b> encontró su filtro el patrón.') +
      demo('fmaps', 'fill'),
      notes('Filtros reales, sacados de la CNN entrenada con el mismo código del NB03 (sección 4). Paso 1: los 16 filtros de 3 × 3 (ámbar positivo, azul negativo). Paso 2: sus 16 mapas sobre el botín y, a la derecha, el filtro elegido en grande; la lámina los recorre uno por uno. Haz clic en un filtro o en un mapa para elegir.', 'Cada filtro es un <b>detector</b> y cada mapa dice dónde encontró su patrón. Las capas siguientes combinan bordes en partes (suela, caña) y las partes en prendas.',
            'Busquen los que tienen una mitad ámbar y otra azul: son <b>detectores de bordes</b>, como el que hicimos a mano. Otros responden a las zonas claras de la prenda o al fondo.',
            'La gran idea: la semana pasada los pesos de una neurona se aprendían; ahora <b>los filtros se aprenden</b>. La red descubre sola qué patrones le sirven.',
            '<span class="q">Pregunta:</span> «¿Por qué creen que la red aprendió detectores de bordes y no, por ejemplo, de colores?» (las fotos son en gris y los bordes separan prenda y fondo).'),
      block='01', group=G1, minutes=3, steps=2)

slide('compartir', 'El mismo filtro en toda la imagen', head('El mismo filtro en toda la imagen', 'Un filtro de 3 × 3 tiene <b>9 pesos y 1 sesgo</b>, y sirve para las 676 posiciones de la foto. Es como un sello que se usa en toda la hoja.', key(3)) + f"""
<div class="cmp" style="margin-top:.4em">
  {st(1, '<div class="cmpc"><span class="chip">Primera capa densa · 128 neuronas</span><span class="bigread az">' + count(100480, at=1) + '</span><span class="how">784 × 128 + 128</span><p>Cada neurona tiene un peso para <b>cada</b> píxel.</p></div>')}
  {st(2, '<div class="cmpc"><span class="chip key">Primera capa convolucional · 16 filtros</span><span class="bigread am">' + count(160, at=2) + '</span><span class="how">16 × (3 × 3 + 1)</span><p>Cada filtro tiene 10 números y <b>recorre toda la foto</b>.</p></div>')}
</div>
{st(3, '<div class="keybar" style="margin-top:1.4em"><span>Red completa: la densa aprende <b class="num">101 770</b> números; la CNN, <b class="num">12 810</b>. <b>Unas 8 veces menos</b>, porque comparte sus filtros.</span></div>')}
{st(3, '<p class="say" style="margin-top:.6em">Además, si el borde se mueve de lugar, <b>el mismo filtro lo encuentra</b>. Eso lo vamos a probar en el NB03.</p>')}""",
      notes('<b>Idea clave 3: compartir pesos.</b> Paso 1: la densa necesita un peso por píxel para cada neurona: 784 × 128 + 128 = 100 480 solo en la primera capa.',
            'Paso 2: la convolucional usa 16 filtros de 3 × 3: 16 × 10 = <b>160</b> parámetros, y cada uno se aplica en las 676 posiciones. Es el mismo inspector con la misma lupa revisando toda la foto.',
            'Paso 3: en la red completa del NB03, 101 770 contra 12 810: unas 8 veces menos. Menos números que aprender = menos datos necesarios y menos memorización.',
            '<span class="q">Pregunta:</span> «¿Por qué tiene sentido usar el mismo detector de bordes arriba y abajo de la foto?» (un borde es un borde en cualquier parte: esa es la suposición de la CNN).'),
      block='01', group=G1, minutes=3)

slide('pooling', 'Pooling: quedarse con lo más fuerte', head('Pooling: quedarse con lo más fuerte', '<code>MaxPooling2D(2)</code>: de cada ventana de 2 × 2 se queda con el <b>número mayor</b>. El mapa queda 4 veces más chico y tolera que la prenda se mueva un poco.') +
      demo('pool', 'fill'),
      notes('Pasos 1 a 4: una ventana por clic; de cada una sobrevive el máximo (5, 2, 2 y 6). Es como resumir un párrafo en su frase más importante.',
            'Paso 5: con un mapa real del borde vertical del botín: de 26 × 26 = 676 números a 13 × 13 = 169. El borde sigue ahí.',
            'Para qué sirve: (1) achica el mapa y la cuenta de las capas siguientes, (2) si el borde se corre un píxel, el máximo de la ventana casi no cambia. <b>Pooling no tiene parámetros</b>: no aprende nada.',
            '<span class="q">Pregunta:</span> «¿Cuántos parámetros tiene una capa MaxPooling?» (cero).'),
      block='01', group=G1, minutes=2, steps=5)

CNNCODE = code("""
model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),  # gray photo
    layers.Conv2D(16, 3, activation="relu"),
    layers.MaxPooling2D(2),          # max of 2x2
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Flatten(),                # 800 numbers
    layers.Dense(10, activation="softmax"),
])
""", hl='1:2;2:3;3:4;4:5;5:6;6:7;7:8;8:1-9', cls='sm')
slide('cnn-keras', 'La CNN en Keras', head('La CNN en Keras: los mismos 4 pasos, capas nuevas', 'Cada <code>Conv2D</code> es un juego de filtros; cada <code>MaxPooling2D</code>, un resumen. Al final, la densa de siempre decide entre 10 prendas.') + f"""
<div class="split" style="grid-template-columns:6.2fr 5.8fr;gap:1.6em;align-items:start">
  {CNNCODE}
  {demo('shapes', '')}
</div>""", notes(
    'Un clic por línea: se ilumina la línea y la capa que crea en el dibujo, con su forma y sus parámetros (lo que imprime <code>model.summary()</code> en el NB03).',
    '<code>Input(shape=(28, 28, 1))</code>: alto, ancho y canales (1 porque es gris; a color serían 3). <code>Conv2D(16, 3)</code>: 16 filtros de 3 × 3 → 16 mapas de 26 × 26 (160 parámetros). <code>MaxPooling2D(2)</code> → 13 × 13.',
    'La segunda <code>Conv2D(32, 3)</code> mira los 16 mapas a la vez: cada filtro tiene 3 × 3 × 16 pesos + 1 → 32 × 145 = 4 640. Después, pooling → 5 × 5 × 32 = 800 números, <code>Flatten</code> y la salida <code>Dense(10)</code>: 8 010.',
    'Total: 160 + 4 640 + 8 010 = <b>12 810</b>. compile y fit son los mismos de siempre, con una sola diferencia: la pérdida para 10 clases (siguiente lámina).'),
    block='01', group=G1, minutes=4, steps=8)

slide('softmax', 'De sí o no a 10 clases', head('De sí o no a 10 clases: softmax', 'La sigmoide de la semana 1 daba una probabilidad (sí o no). <b>Softmax</b> da 10, una por prenda, y <b>suman 1</b>. La red elige la más alta.') + f"""
<div class="split" style="grid-template-columns:8fr 4fr;gap:2em">
  {demo('softmax', 'fig', start=0)}
  <div class="col" style="gap:1em">
    """ + eq([('p_k', 'probabilidad de la prenda k', 'out'), ('=', '', 'op'), (r'\dfrac{e^{z_k}}{\sum_j e^{z_j}}', 'su puntaje entre todos', 'x')],
             read='cada puntaje se vuelve positivo con e<sup>z</sup> y se divide entre la suma de todos: quedan 10 porciones de una torta.', size='.76em') + """
    """ + st(1, '<p class="say">La camisa: la CNN duda entre <b>camisa 77 %</b> y camiseta 11 %. Duda entre prendas que se parecen, como una persona.</p>') + """
    <p class="cap">En <code>compile</code>: <code>loss="sparse_categorical_crossentropy"</code>, la BCE de la semana 1 para muchas clases.</p>
  </div>
</div>""", notes(
    'Probabilidades reales de las dos redes del NB03 para siete fotos del examen. Empieza con el botín: la CNN le da 96 %.',
    'Paso 1: la camisa, la prenda más difícil. La CNN reparte: camisa 77 %, camiseta 11 %, abrigo 5 %, suéter 5 %. Cambia a la densa con el botón: 75 % camisa.',
    'La fórmula es para quien la quiera; lo importante: 10 números positivos que suman 1. La pérdida <code>sparse_categorical_crossentropy</code> castiga, como la BCE, la falsa seguridad en la prenda equivocada.',
    '<span class="q">Pregunta:</span> «¿Qué prendas creen que la red confunde más?» (camisa con camiseta: lo vemos en la sección 6 del NB03).'),
    block='01', group=G1, minutes=2, steps=1)

practice('practica-nb03', 'Práctica en clase: NB03', 'En parejas. Todo el código ya viene escrito y comentado. Antes de cada celda, apuesta qué va a salir.',
         ['<b>0</b> · La foto es una tabla: <code>(60000, 28, 28)</code>, de 0 a 255', '<b>1</b> · Tu lupa a mano: la suma da <b>+0.99</b>',
          f'<b>2</b> · La densa: <b>101 770</b> parámetros y <b>{pct(RD["test"])}</b>', f'<b>3</b> · La CNN: <b>12 810</b> parámetros y <b>{pct(RC["test"])}</b>',
          f'<b>5</b> · Mover 2 píxeles: densa <b>{pct(RD["shift"]["2"])}</b>, CNN <b>{pct(RC["shift"]["2"])}</b>', '<b>6</b> · Lo que más confunde: <b>camisa ↔ camiseta</b>'], 'nb03', 35, G1, '01',
         notes('Dinámica: 25 minutos en parejas (o salas de 3) y 10 de puesta en común. Sin nota.',
               'Prioridad si el tiempo aprieta: <b>0, 2, 3 y 5</b>. Las secciones 1, 4 y 6 pueden quedar para casa. Cada entrenamiento tarda menos de un minuto en Colab (los dos, unos 2 minutos).',
               'No hay nada que programar: cada sección explica qué va a pasar, trae el código comentado y termina en <b>Para pensar</b> (respuesta plegada) y <b>Experimenta</b> (cambiar un número). Pide que digan qué esperan antes de ejecutar.',
               'Problema frecuente: «la descarga de Fashion-MNIST tarda»: son 30 MB, la primera vez toma unos segundos. Si sale <code>NameError</code>, se saltaron la celda de Configuración.'))

slide('duelo', 'Densa contra CNN: lo que vimos', head('Densa contra CNN: lo que vimos en el NB03', 'Mismas fotos, mismos 5 épocas, mismo optimizador. Solo cambia la suposición.') +
      demo('duel', 'fill') +
      st(5, '<div class="keybar" style="margin-top:.8em"><span>La CNN gana porque <b>su suposición es cierta</b> para las fotos. Con 4 píxeles las dos se caen: no es magia. La semana 3 trata de <b>robustez</b>.</span></div>'),
      notes('Puesta en común de la práctica, con los números reales del NB03. Pide que alguien diga cada número antes de mostrarlo.',
            f'1 · Parámetros: 101 770 contra 12 810. 2 · Examen final: {pct(RD["test"])} contra {pct(RC["test"])}: la CNN gana con 8 veces menos números.',
            f'3 · Mover la prenda: con 1 px, {pct(RD["shift"]["1"])} contra {pct(RC["shift"]["1"])}; con 2 px la densa se desploma a {pct(RD["shift"]["2"])} y la CNN aguanta {pct(RC["shift"]["2"])}. Con 4 px, {pct(RD["shift"]["4"])} y {pct(RC["shift"]["4"])}: las dos fallan.',
            f'4 · Mezclar los píxeles: la densa da lo mismo ({pct(RD["mezclada"])}); la CNN baja a {pct(RC["mezclada"])}. Es la prueba de la idea clave 1: la CNN aprovecha la vecindad; si la rompes, pierde su ventaja.',
            '<span class="q">Pregunta:</span> «¿Cómo harían que la CNN aguante prendas movidas 4 píxeles?» (entrenar con fotos movidas: aumento de datos, semana 3).'),
      block='01', group=G1, minutes=6, steps=5)

HCNN = [('1980', 'Fukushima · el neocognitrón: capas que detectan rasgos'), ('1989', 'LeCun · una CNN lee códigos postales escritos a mano'),
        ('1998', 'LeNet-5 · lee cheques en los bancos'), ('2012', 'AlexNet · gana ImageNet con GPU: el error cae de 26 % a 15 %'),
        ('2015', 'ResNet · 152 capas, 3.6 % de error'), ('2020', 'Vision Transformer · la atención llega a las imágenes')]
slide('historia-cnn', 'De los cheques a ImageNet', head('De los cheques a ImageNet', 'Las CNN tienen más de 40 años. Dominaron la visión desde 2012 y siguen vivas.') +
      '<div class="tl hist-tl" style="margin-top:.4em">' + ''.join(st(1 if i < 3 else 2, f'<div class="ev"><span class="y num">{y}</span><i></i><span class="d">{d}</span></div>') for i, (y, d) in enumerate(HCNN)) + '</div>' +
      st(3, '<div class="trendbar" style="margin-top:1.6em">' + chip('Lectura de tendencia', 'trend') + '<span>En 2023, Google DeepMind entrenó CNN con <b>el mismo presupuesto de cómputo</b> que los Vision Transformers más fuertes: empate técnico, más de 90 % en ImageNet. «No hay evidencia fuerte de que los ViT superen a las CNN cuando se evalúan con justicia» (Smith et al., 2023).</span></div>'),
      notes('Recorrido rápido. Lo importante: la CNN no es nueva. LeCun la usó en 1989 para leer códigos postales y en 1998 LeNet-5 leía cheques. En 2012 AlexNet, entrenada en GPU, ganó ImageNet por mucha diferencia (la misma historia de la semana 1).',
            'En 2020 llegó el Vision Transformer: la atención (Tema 2) aplicada a pedazos de imagen. Muchos dieron por muertas a las CNN.',
            '<b>Puente con la lectura:</b> con una comparación justa (mismo cómputo y datos), las CNN empataron. Es la misma moraleja de los optimizadores de la semana 1: antes de declarar un ganador, que todos corran la misma carrera.',
            '<span class="q">Pregunta:</span> «¿Qué significa comparar con justicia en su proyecto?» (mismos datos, mismo presupuesto, misma métrica).'),
      block='01', group=G1, minutes=4)

slide('cierre-tema1', 'Lo que te llevas del Tema 1', head('Lo que te llevas del Tema 1') + f"""
<div class="col" style="gap:1.1em">
  {st(1, '<div class="mapi big"><span>La suposición</span><b>cada arquitectura apuesta por cómo están organizados los datos</b></div>')}
  {st(2, '<div class="mapi big"><span>La lupa</span><b>un filtro de 3 × 3 recorre la foto y responde donde está su patrón</b></div>')}
  {st(3, '<div class="mapi big"><span>Compartir</span><b>el mismo filtro en toda la foto: 8 veces menos parámetros</b></div>')}
  {st(4, '<div class="trendbar" style="margin-top:.6em">' + chip('Antes del Tema 2', 'trend') + '<span>Lee la lectura de tendencia <b>«¿El regreso de las redes recurrentes? Transformers, Mamba y la búsqueda de la arquitectura ideal»</b> (5 páginas) y responde la encuesta en Canvas.</span></div>')}
  {st(4, '<p class="say" style="margin-top:.2em"><b>En el Tema 2:</b> si los datos llegan <b>en orden</b>, como las palabras de una frase, ¿cómo los lee una red?</p>')}
</div>""", notes(
    'Cierre del Tema 1, 5 minutos. Pide que alguien diga cada idea con sus palabras antes de mostrarla.',
    'La lectura de tendencia va antes del Tema 2: cada arquitectura es una suposición y las redes recurrentes vuelven en modelos híbridos. No la expliques: que lleguen con una opinión.',
    'En el chat, del 1 al 5: <b>¿podrías explicar qué hace un filtro convolucional a un colega?</b> Anota el promedio.',
    'Si aquí termina la sesión: <b>«Finalizar reunión para todos»</b> para que la grabación se cierre bien. Si queda tiempo, sigue directo con el Tema 2.'),
    block='01', group=G1, minutes=5)
