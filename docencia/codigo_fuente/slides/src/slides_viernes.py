"""Friday 23 · 18:00-20:00 · blocks 00-04."""
from kit import slide, head, key, chip, st, demo, count, qr, notes

G0 = 'Viernes · Encuadre'
G1 = 'Viernes · 01 IA, machine learning y deep learning'
G2 = 'Viernes · 02 La neurona artificial'
G3 = 'Viernes · 03 Cómo aprende una neurona'
G4 = 'Viernes · 04 Medir el error y mejorar'
GV = 'Viernes · Cierre'


def section(sid, n, title, lede, items, when, group, blockname, note):
    lst = ''.join(f'<span>{i}</span>' for i in items)
    body = (f'<div class="sec"><div class="n">{n}</div><h2>{title}</h2>'
            f'<p class="lede">{lede}</p><div class="lst">{lst}</div><p class="when">{when}</p></div>')
    slide(sid, title, body, note, layout='L-section', block=n, group=group, minutes=1, blockname=blockname)


def practice(sid, title, lede, checks, keyname, minutes, group, block, note, extra=''):
    ck = ''.join(f'<li>{c}</li>' for c in checks)
    body = (head(title, lede, chip('En clase · sin nota', 'ok') + chip(f'{minutes} minutos', 'hint')) +
            f'<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:.6em">'
            f'<div class="col"><h3 class="big" style="font-weight:600">Qué deberías ver</h3><ul class="checks">{ck}</ul>{extra}</div>'
            f'<div class="col" style="align-items:center">{qr(keyname)}'
            f'<p class="txt" style="text-align:center;font-size:1em">Archivo → <b>Guardar una copia en Drive</b><br>y ejecuta primero <b>Configuración</b></p></div></div>')
    slide(sid, title, body, note, block=block, group=group, minutes=minutes)


# ======================================================================= 00 · encuadre
slide('portada', 'De una neurona a tu primera red', f"""
<div class="cover">
  <div class="left">
    <div class="tags">{chip('UIDE · Maestría en Ciencia de Datos')}{chip('Semana 1')}</div>
    <h1 class="display">De una neurona a tu primera&nbsp;red</h1>
    <p class="lede" style="font-size:1.45em">Neural Networks: Deep Learning</p>
    <p class="meta"><b>Andrés Ordóñez-Bolaños, MSc</b><br>Viernes 23 · 18:00–20:00 &nbsp;·&nbsp; Sábado 24 · 08:00–12:00<br>Octubre de 2026 · Microsoft Teams</p>
  </div>
  <div class="right">{demo('net', layers='4,6,6,3,1', w=860, h=1000, gap=140, padx=120, alt='Red neuronal con señales que viajan de izquierda a derecha')}</div>
</div>""", notes(
    '<b>Antes de hablar:</b> verifica que la grabación está corriendo. Comparte esta ventana (no toda la pantalla) y abre la vista del presentador con la tecla <b>P</b>.',
    'Bienvenida corta: «Esta semana vamos a pasar de no saber qué es una neurona artificial a entrenar nuestra primera red en Keras. Sin instalar nada: todo en el navegador».',
    'La red de la derecha está viva: cada punto que viaja es una señal y cada neurona se ilumina según cuánto se activa. Al final del sábado van a entender exactamente qué está pasando ahí.'),
    layout='L-cover', block='00', group=G0, minutes=2, blockname='Encuadre')

RAIL_V = [('18:00', 'Pre-quiz', 'q'), ('18:10', '01 · Aprender de ejemplos', ''), ('18:25', '02 · La neurona', ''), ('18:45', '03 · Cómo aprende', ''),
          ('19:00', 'Práctica NB01', 'p'), ('19:20', '04 · Error y gradiente', ''), ('19:55', 'Cierre y lectura', 't')]
RAIL_S = [('08:00', 'Repaso', ''), ('08:15', '05 · Redes', ''), ('08:55', '06 · Retro­propagación', ''), ('09:40', 'Pausa', 'b'), ('09:55', '07 · Entrenar bien', 't'),
          ('10:30', '08 · Keras', ''), ('10:45', 'Práctica NB02', 'p'), ('11:30', '09 · Métricas', ''), ('11:45', 'Quiz final', 'q')]


def rail(items):
    return '<div class="rail" style="--n:%d">' % len(items) + ''.join(
        f'<div class="stn {k}"><i></i><span class="t num">{t}</span><span class="l">{l}</span></div>' for t, l, k in items) + '</div>'


slide('ruta', 'La semana en dos sesiones', head('La semana en dos sesiones', 'Primero la idea, después la demo y al final la práctica en Colab. Las prácticas son en clase y no tienen nota.') + f"""
<div class="col" style="gap:2.2em;margin-top:.6em">
  {st(1, '<h3 class="dayh">Viernes 23 <span class="mu">18:00–20:00</span></h3>' + rail(RAIL_V))}
  {st(2, '<h3 class="dayh">Sábado 24 <span class="mu">08:00–12:00</span></h3>' + rail(RAIL_S))}
  {st(2, '<div class="legend"><span><i style="background:var(--amber)"></i>práctica en Colab</span><span><i style="background:var(--mint)"></i>quiz tipo Kahoot</span><span><i style="background:var(--lilac)"></i>lectura de tendencia</span></div>')}
</div>""", notes(
    'Dos sesiones, nueve bloques. El viernes construimos UNA neurona y vemos cómo aprende; el sábado juntamos muchas en una red y la entrenamos con Keras.',
    'Recalca: <b>las prácticas son en clase y no se califican</b>. Los notebooks se corrigen solos (✅ ❌ ⏳); la idea es equivocarse sin miedo.',
    'Lo que sí registramos es el pre-quiz y el quiz final, pero solo para ver cuánto avanzamos como grupo.'),
    block='00', group=G0, minutes=1)

slide('prequiz', 'Pre-quiz: ¿de dónde partimos?', head('Antes de empezar: ¿de dónde partimos?', '8 preguntas cortas tipo Kahoot. <b>No es nota</b>: es tu punto de partida para medir cuánto avanzas.') + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:1em">
  <ol class="steps-list" style="gap:1.2em">
    {st(1, '<span class="k">1</span><span>Escanea el código o abre <b>deeplearningweek1.vercel.app/?pre</b></span>', 'li')}
    {st(2, '<span class="k">2</span><span>Escribe tu nombre y responde rápido: <b>más rapidez, más puntos</b></span>', 'li')}
    {st(3, '<span class="k">3</span><span>Al final, copia tu código y <b>pégalo en el chat de Teams</b></span>', 'li')}
    {st(3, '<span class="k" style="background:var(--mint);color:var(--night)">✓</span><span>Si no sabes una, elige la que te parezca. Equivocarse aquí es parte del plan.</span>', 'li')}
  </ol>
  <div class="center">{qr('pre')}</div>
</div>""", notes(
    'Dales 6 minutos. Mientras juegan, mira el chat: cuando la mayoría haya pegado su código, sigue.',
    'Cinco de las ocho preguntas son las <b>ideas clave</b> que vuelven en el quiz final; así medimos el avance. El panel <b>Resultados_quiz.html</b> lee los códigos que peguen en el chat.',
    '<span class="q">Pregunta para el chat:</span> «¿Cuál les pareció más difícil?» Anota la respuesta: es el termómetro del grupo.'),
    block='00', group=G0, minutes=6)

IDEAS = ['Qué calcula una neurona', 'Para qué sirve la activación', 'Por qué una sola neurona no puede con XOR',
         'Hacia dónde camina el descenso de gradiente', 'Por qué la exactitud puede engañar']
slide('metas', 'Las 5 ideas clave de la semana', head('El sábado vas a poder explicar estas 5 ideas', 'Las medimos dos veces: en el pre-quiz de hoy y en el quiz final del sábado.') +
      '<ol class="steps-list" style="gap:1.05em;margin-top:.4em">' + ''.join(
          st(i + 1, f'<span class="k key">{i + 1}</span><span class="big" style="color:var(--ink)">{t}</span>', 'li') for i, t in enumerate(IDEAS)) + '</ol>',
      notes('Esta es la promesa de la semana. Cada idea tiene una lámina marcada con la etiqueta amarilla <b>Idea clave</b>: cuando aparezca, deténganse ahí.',
            'Si al final alguien no puede explicar alguna de las cinco con sus palabras, la guía de estudio tiene una sección para cada una.'),
      block='00', group=G0, minutes=1)

# ======================================================================= 01 · IA, ML, DL
section('b01', '01', 'IA, machine learning y deep learning', 'Qué significa que una máquina aprenda de ejemplos.',
        ['Tres círculos', 'Reglas o ejemplos', 'Dónde ya lo usas', '¿Por qué ahora?'], 'Viernes · 15 minutos', G1, '01 · IA, machine learning y deep learning',
        notes('Bloque corto y conversado. La meta es una sola: que entiendan que el machine learning <b>aprende las reglas a partir de ejemplos</b> en vez de recibirlas escritas.'))

CIRC = """
<svg viewBox="0 0 1000 800" role="img" aria-label="Tres círculos anidados: la inteligencia artificial contiene al machine learning, que contiene al deep learning">
 <g data-step="1"><circle cx="470" cy="420" r="370" fill="#0f1a29" stroke="#899aae" stroke-width="5"/>
  <text x="470" y="118" text-anchor="middle" font-size="40" font-weight="700" fill="#f1f6fa" font-family="Unbounded, Lexend, sans-serif">IA</text></g>
 <g data-step="2"><circle cx="555" cy="495" r="265" fill="#182436" stroke="#b6c6d7" stroke-width="5"/>
  <text x="555" y="322" text-anchor="middle" font-size="34" font-weight="700" fill="#f1f6fa" font-family="Unbounded, Lexend, sans-serif">Machine</text>
  <text x="555" y="364" text-anchor="middle" font-size="34" font-weight="700" fill="#f1f6fa" font-family="Unbounded, Lexend, sans-serif">learning</text></g>
 <g data-step="3"><circle cx="630" cy="575" r="150" fill="#ffb541" fill-opacity=".1" stroke="#ffb541" stroke-width="6"/>
  <text x="630" y="566" text-anchor="middle" font-size="34" font-weight="700" fill="#ffb541" font-family="Unbounded, Lexend, sans-serif">Deep</text>
  <text x="630" y="610" text-anchor="middle" font-size="34" font-weight="700" fill="#ffb541" font-family="Unbounded, Lexend, sans-serif">learning</text></g>
</svg>"""
CIRC_T = [('Inteligencia artificial', 'Máquinas que hacen tareas que parecen inteligentes, aprendan o no.', 'El GPS que calcula la ruta · el rival de un videojuego', ''),
          ('Machine learning', 'Aprende las reglas a partir de ejemplos.', 'El filtro de spam · las recomendaciones de Netflix', ''),
          ('Deep learning', 'Machine learning con redes de muchas capas.', 'Desbloquear el celular con tu cara · los subtítulos automáticos · ChatGPT', 'am')]
slide('circulos', 'Tres círculos, uno dentro de otro', f"""
<div class="split" style="grid-template-columns:6fr 5fr">
  <div class="fig">{CIRC}</div>
  <div class="col" style="gap:1.6em">
    {head('Tres círculos, uno dentro de otro')}
    """ + ''.join(st(i + 1, f'<div class="circ-t"><h3 class="{c}">{t}</h3><p class="say">{d}</p><p class="ex">{e}</p></div>') for i, (t, d, e, c) in enumerate(CIRC_T)) + """
  </div>
</div>""", notes(
    'Paso 1. <b>IA</b> es la etiqueta más amplia: cualquier sistema que haga algo que parece inteligente, aunque siga reglas escritas a mano (el GPS no «aprende» a calcular rutas: usa un algoritmo).',
    'Paso 2. <b>Machine learning</b> es la parte de la IA que aprende de datos. Nadie le escribe al filtro de spam la lista de palabras; la aprende de millones de correos marcados.',
    'Paso 3. <b>Deep learning</b> es machine learning con redes neuronales de muchas capas. Es lo que vamos a estudiar todo el curso.',
    '<span class="q">Pregunta:</span> «¿En cuál círculo pondrían a ChatGPT? ¿Y a la calculadora de su celular?» (la calculadora: ni siquiera es IA).'),
    block='01', group=G1, minutes=3)

slide('reglas', 'Programar reglas o aprender de ejemplos', head('Programar reglas o aprender de ejemplos') + f"""
<div class="col fill" style="gap:2em;justify-content:center">
  {st(1, '<div class="flow"><span class="lab">Programación clásica</span><span class="bx">Reglas</span><span class="op">+</span><span class="bx">Datos</span><span class="op">→</span><span class="bx out">Respuestas</span></div>')}
  {st(2, '<div class="flow"><span class="lab am">Machine learning</span><span class="bx">Datos</span><span class="op">+</span><span class="bx">Respuestas</span><span class="op">→</span><span class="bx out hot">Reglas</span></div>')}
  {st(3, '<div class="split even" style="gap:1.4em;margin-top:.6em"><div class="warnbar"><span><b>Regla escrita:</b> «si dice GRATIS, es spam». Y el correo de tu tienda favorita, «¡Envío gratis!», termina en spam.</span></div><div class="keybar"><span><b>Aprendida:</b> le muestras 10 000 correos ya marcados y el modelo descubre solo qué combinación de señales delata al spam.</span></div></div>')}
</div>""", notes(
    'Esta es la lámina más importante del bloque. En la programación de siempre, una persona escribe las reglas. En machine learning le damos <b>ejemplos con su respuesta</b> y la máquina encuentra las reglas.',
    'El ejemplo del spam: una regla escrita a mano falla en cuanto el mundo cambia; el modelo aprende muchas señales a la vez (remitente, enlaces, palabras, horario) y se puede reentrenar.',
    '<span class="q">Pregunta:</span> «¿Qué problema de su trabajo hoy se resuelve con reglas escritas a mano y podría aprender de ejemplos?»'),
    block='01', group=G1, minutes=3)

CAT = [('tiene orejas puntiagudas', 'un zorro también'), ('tiene bigotes', 'una foca también'),
       ('es pequeño y peludo', 'un cuy también'), ('maúlla', 'en una foto no se oye nada')]
slide('gato', 'Intenta escribir las reglas de un gato', head('Intenta escribir las reglas de un gato', 'Para que una computadora reconozca gatos en fotos, ¿qué reglas le darías?') +
      '<div class="col" style="gap:.8em">' + ''.join(
          st(i + 1, f'<div class="rule"><span>Si <b>{r}</b>, es un gato</span><span class="co">✗ {c}</span></div>') for i, (r, c) in enumerate(CAT)) +
      st(5, '<div class="keybar" style="margin-top:.6em"><span><b>Mejor:</b> muéstrale miles de fotos con su etiqueta, «gato» o «no gato», y deja que encuentre las señales. Eso es deep learning.</span></div>') + '</div>',
      notes('Hazlo como juego: pide en el chat una regla y busca juntos el contraejemplo. Siempre aparece uno.',
            'Mensaje: hay problemas donde <b>no sabemos escribir las reglas</b>, aunque nosotros mismos los resolvamos sin pensar (reconocer una cara, entender una voz). Ahí el deep learning brilla.',
            'Dato para curiosos: un niño aprende «gato» viendo unos pocos; las redes necesitan miles. Esa diferencia es un tema abierto de investigación.'),
      block='01', group=G1, minutes=2)

USES = [('Tu cara', 'desbloquea el celular'), ('Tu voz', 'el texto del mensaje'), ('Una foto', '«perro», «playa», «Quito»'),
        ('Una compra con tarjeta', '¿fraude? Alerta del banco'), ('Lo que ya viste', 'la próxima serie'), ('Tu pregunta', 'una respuesta de ChatGPT')]
slide('usos', 'Deep learning que ya usas hoy', head('Deep learning que ya usas hoy', 'Todos hacen lo mismo: convierten una <b>entrada</b> en una <b>salida</b>, después de aprender de millones de ejemplos.') +
      '<div class="pipes">' + ''.join(
          st(i // 2 + 1, f'<div class="pipe"><span class="in">{a}</span><span class="wire"><i class="pulse"></i></span><span class="nn"><b></b><b></b><b></b></span><span class="wire"><i class="pulse"></i></span><span class="out">{b}</span></div>')
          for i, (a, b) in enumerate(USES)) + '</div>',
      notes('Seis ejemplos cotidianos. La idea que deben retener: <b>una red neuronal es una función</b> que convierte una entrada (una imagen, un audio, una lista de compras) en una salida (una etiqueta, un texto, una probabilidad).',
            'Pregunta a quién le ha llegado una alerta de fraude del banco: detrás hay un modelo que aprendió cómo se ven las compras normales de esa persona.',
            'Esta forma «entrada → red → salida» la vamos a ver toda la semana.'),
      block='01', group=G1, minutes=2)

TL = [('1958', 'El perceptrón de Rosenblatt: la primera neurona artificial que aprende'), ('1969', 'Minsky y Papert muestran su límite (XOR) y llega el primer «invierno»'),
      ('1986', 'Se populariza la retropropagación: redes de varias capas'), ('2012', 'AlexNet gana ImageNet entrenada con tarjetas gráficas (GPU)'),
      ('2017', 'El Transformer, base de los modelos de lenguaje'), ('2022', 'ChatGPT llega al público')]
slide('ahora', '¿Por qué ahora?', head('Las ideas tienen 60 años. ¿Por qué despegaron ahora?') +
      '<div class="tl">' + ''.join(st(1 if i < 3 else 2, f'<div class="ev"><span class="y num">{y}</span><i></i><span class="d">{d}</span></div>') for i, (y, d) in enumerate(TL)) + '</div>' +
      st(3, '<div class="row" style="gap:1em;margin-top:1.4em"><span class="big" style="color:var(--ink)">Tres ingredientes se juntaron:</span>' + chip('muchos datos', 'hint lg') + chip('cómputo barato (GPU)', 'hint lg') + chip('mejores algoritmos', 'hint lg') + '</div>') +
      st(4, '<div class="trendbar" style="margin-top:1em">' + chip('Lectura de tendencia', 'trend') + '<span>El cómputo dedicado a la IA crece <b>más de 3 veces por año</b> (AI Index 2026). Entonces, ¿todavía importan los mejores algoritmos? Es la pregunta de la lectura de esta semana.</span></div>'),
      notes('Recorre la línea de tiempo rápido, como historia. El perceptrón de 1958 es casi lo mismo que veremos en 20 minutos.',
            '1969: Minsky y Papert demostraron que una sola neurona no puede aprender XOR (lo veremos hoy) y el financiamiento se congeló por años: el primer «invierno de la IA».',
            '2012 es el punto de quiebre: AlexNet ganó la competencia ImageNet por mucha diferencia, entrenada en GPU. Desde ahí, datos + cómputo + algoritmos se retroalimentan.',
            '<b>Puente con la lectura:</b> si el cómputo crece tanto, ¿vale la pena inventar mejores algoritmos? Que lo piensen para la encuesta (no hay respuesta correcta).'),
      block='01', group=G1, minutes=3)

# ======================================================================= 02 · la neurona
section('b02', '02', 'La neurona artificial', 'Una calculadora con opinión: recibe datos, los pesa y decide.',
        ['Un comité de crédito', 'La cuenta a mano', 'Una línea', 'La activación'], 'Viernes · 20 minutos', G2, '02 · La neurona artificial',
        notes('Aquí está la <b>idea clave 1</b> (qué calcula una neurona) y la <b>idea clave 2</b> (para qué sirve la activación).'))

NEURON = """
<svg viewBox="0 0 1090 640" role="img" aria-label="Neurona: tres datos con sus pesos llegan a una suma con sesgo, pasan por la activación y dan la decisión">
 <g data-step="1">
  <g class="flowline"><line x1="160" y1="130" x2="500" y2="320"/><line x1="160" y1="320" x2="500" y2="320"/><line x1="160" y1="510" x2="500" y2="320"/></g>
  <circle cx="120" cy="130" r="46" class="nd"/><circle cx="120" cy="320" r="46" class="nd"/><circle cx="120" cy="510" r="46" class="nd"/>
  <text x="120" y="140" class="nv">0.8</text><text x="120" y="330" class="nv">0.5</text><text x="120" y="520" class="nv">−1.0</text>
  <text x="120" y="66" class="nl">Ingreso</text><text x="120" y="256" class="nl">Antigüedad</text><text x="120" y="446" class="nl">Atrasos previos</text>
 </g>
 <g data-step="2">
  <rect x="268" y="176" width="104" height="44" rx="22" class="wchip"/><text x="320" y="206" class="wv am">× 1.2</text>
  <rect x="268" y="298" width="104" height="44" rx="22" class="wchip"/><text x="320" y="328" class="wv am">× 0.7</text>
  <rect x="262" y="420" width="116" height="44" rx="22" class="wchip"/><text x="320" y="450" class="wv az">× −2.0</text>
  <text x="320" y="592" class="nl" style="fill:var(--ink-3)">pesos: cuánto confía en cada dato</text>
 </g>
 <g data-step="3">
  <line x1="560" y1="120" x2="560" y2="232" class="arrow"/><text x="560" y="96" class="nl">sesgo b = −0.5</text>
  <circle cx="560" cy="320" r="84" class="nd big"/><text x="560" y="345" class="sum">Σ</text>
 </g>
 <g data-step="4">
  <g class="flowline"><line x1="644" y1="320" x2="726" y2="320"/><line x1="834" y1="320" x2="880" y2="320"/></g>
  <rect x="726" y="266" width="108" height="108" rx="24" class="nd"/><path d="M742 352 C770 352 772 290 818 290" class="act"/>
  <text x="780" y="410" class="nl" style="fill:var(--ink-3)">activación</text>
  <text x="930" y="312" class="nl am" style="font-size:30px">¿Aprueba?</text><text x="930" y="350" class="nl" style="fill:var(--ink-3)">sí / no</text>
 </g>
</svg>"""
slide('comite', 'Una neurona es un comité de crédito en miniatura', f"""
<div class="split wide" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('Una neurona es un comité de crédito en miniatura', 'Multiplica cada dato por su <b>peso</b>, suma todo, añade el <b>sesgo</b> y decide.', key(1))}
    <div class="formula"><m>z = w_1 x_1 + w_2 x_2 + w_3 x_3 + b</m></div>
    <p class="say"><b>Pesos</b>: cuánto confía en cada dato.<br><b>Sesgo</b>: qué tan exigente es.</p>
  </div>
  <div class="fig neuron">{NEURON}</div>
</div>""", notes(
    '<b>Idea clave 1.</b> Imaginen el comité de crédito de una cooperativa. Llega un socio con tres datos: ingreso, antigüedad y atrasos previos (ya escalados: 0 es el promedio).',
    'Paso 2: el comité no confía igual en todo. El ingreso pesa 1.2; la antigüedad 0.7; los atrasos pesan −2.0: <b>un peso negativo resta</b>, más atrasos bajan el puntaje.',
    'Paso 3: el sesgo es el «carácter» del comité. Con b = −0.5 es algo exigente: empieza restando.',
    'Paso 4: la activación convierte el puntaje en una decisión. Eso lo vemos en dos láminas.',
    '<span class="q">Pregunta:</span> «Si el comité se vuelve más exigente, ¿qué número cambia?» (el sesgo, se hace más negativo).'),
    block='02', group=G2, minutes=3)

CALC = [('Ingreso', '0.8 × 1.2', 0.96), ('Antigüedad', '0.5 × 0.7', 0.35), ('Atrasos previos', '−1.0 × −2.0', 2.00), ('Sesgo', 'b', -0.50)]


def bar(v):
    w = abs(v) / 3.0 * 50
    side = f'left:50%;width:{w:.1f}%;background:var(--amber)' if v > 0 else f'right:50%;width:{w:.1f}%;background:var(--azure)'
    return f'<span class="bt"><i style="{side}"></i></span>'


rows = ''.join(st(i + 1, f'<span class="lb">{n}</span><span class="num mu">{e}</span><span class="num {"am" if v > 0 else "az"}" style="font-weight:700">{"+" if v > 0 else "−"}{abs(v):.2f}</span>{bar(v)}', cls='calc-row') for i, (n, e, v) in enumerate(CALC))
slide('cuenta', 'Hagamos la cuenta con el socio A', head('Hagamos la cuenta con el socio A', 'Cada dato por su peso, y después se suma todo.', key(1)) + f"""
<div class="calc" style="font-size:1.5em;gap:.6em 1.4em">{rows}
  {st(5, '<span class="lb" style="color:var(--ink);font-weight:700">Puntaje z</span><span class="num mu">suma</span><span class="num" style="font-weight:700;font-size:1.5em">' + count(2.81, 2, at=5) + '</span><span class="bt"><i style="left:50%;width:46.8%;background:var(--amber);box-shadow:0 0 1em oklch(0.83 0.155 72 / .4)"></i></span>', cls='calc-row total')}
</div>
{st(6, '<div class="keybar" style="margin-top:.8em"><span>z es positivo: <b>el comité aprueba</b>. Los pocos atrasos (−1.0 por un peso de −2.0) aportaron más que el ingreso.</span></div>')}
{st(7, '<p class="say" style="margin-top:.6em">' + chip('Tu turno · NB01 §1', 'hint') + ' El <b>socio B</b>: ingreso 0.2, antigüedad −0.5 y atrasos 1.5. ¿Lo aprueba?</p>')}""",
      notes('Hagan la cuenta juntos, despacio, una fila por clic. Es exactamente la sección 1 del NB01.',
            'La fila más interesante es la de atrasos: el dato es −1.0 (menos atrasos que el promedio) y el peso es −2.0; <b>negativo por negativo da positivo</b>: tener pocos atrasos suma mucho.',
            'Total: 0.96 + 0.35 + 2.00 − 0.50 = <b>2.81</b>.',
            '<span class="q">Tu turno (está en el NB01):</span> el socio B tiene ingreso 0.2, antigüedad −0.5 y atrasos 1.5. ¿Lo aprueba? (z = −3.61: no).'),
      block='02', group=G2, minutes=3)

slide('linea', 'Una neurona dibuja una línea', f"""
<div class="split wide" style="grid-template-columns:4fr 8fr">
  <div class="col">
    {head('Una neurona dibuja una línea', 'Cada socio es un punto. La neurona parte el plano en dos con una línea recta: de un lado aprueba, del otro rechaza.')}
    <p class="say">Los <b>pesos</b> giran la línea.<br>El <b>sesgo</b> la mueve sin girarla.<br><b>Entrenar</b> es encontrar dónde ponerla.</p>
    <div class="legend"><span><i style="background:var(--amber)"></i>sí pagó</span><span><i style="background:var(--azure)"></i>no pagó</span><span><i style="background:transparent;border:3px solid var(--coral)"></i>mal clasificado</span></div>
  </div>
  {demo('line', 'fig')}
</div>""", notes(
    'Esta es la imagen que deben llevarse. Con dos datos (ingreso y atrasos) cada socio es un punto. La neurona solo sabe hacer una cosa: <b>trazar una línea recta</b>. Donde z es positivo, aprueba; donde es negativo, rechaza; justo sobre la línea, z = 0.',
    'Empieza mal a propósito: la neurona aprueba a los que más atrasos tienen. Mueve <b>w₂</b> hacia negativo y la línea gira. Luego mueve <b>b</b> y verán que se desplaza sin girar.',
    'Pide a alguien que te dicte valores por el chat hasta lograr 18 de 18. Si se tarda, usa «Buscar la mejor línea».',
    'Mensaje: entrenar una neurona = buscar automáticamente los pesos que dejan esa línea en el mejor lugar. Con 3 datos es un plano; con 28, un «hiperplano»; la idea no cambia.'),
    block='02', group=G2, minutes=4)

slide('activacion', 'La activación decide qué sale', head('La activación decide qué sale de la neurona', 'El mismo puntaje z pasa por tres funciones distintas. Mueve z y compara.', key(2)) + demo('act', 'fill'),
      notes('<b>Idea clave 2 (parte 1).</b> La activación es la última pieza: toma el puntaje z y decide qué sale.',
            '<b>Escalón</b> = un interruptor: todo o nada. Así era el perceptrón de 1958. <b>Sigmoide</b> = un regulador de luz: un valor suave entre 0 y 1, por eso sirve para probabilidades. <b>ReLU</b> = una válvula: si es negativo no pasa nada; si es positivo pasa igual. Es la más usada hoy en las capas ocultas.',
            'Con el socio A (z = 2.81): escalón 1, sigmoide 0.943, ReLU 2.81. Lleva z a −2.81 y compara.',
            'Esto es la sección 2 del NB01.'),
      block='02', group=G2, minutes=3)

slide('sigmoide', 'La sigmoide: de puntaje a probabilidad', f"""
<div class="split" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('De puntaje a probabilidad: la sigmoide')}
    <ul class="steps-list">
      {st(1, '<span class="k">1</span><span>Puntaje muy negativo → <b>casi 0 %</b></span>', 'li')}
      {st(2, '<span class="k">2</span><span>Puntaje 0 → <b>50 %</b>: la neurona duda</span>', 'li')}
      {st(3, '<span class="k key">A</span><span>El socio A, z = 2.81 → <b class="am">94 % de que paga</b></span>', 'li')}
    </ul>
    <div class="formula" style="font-size:1.2em"><m>\\sigma(z) = \\dfrac{{1}}{{1 + e^{{-z}}}}</m></div>
  </div>
  {demo('sigmoid', 'fig')}
</div>""", notes(
    'La sigmoide aplasta cualquier número a un valor entre 0 y 1, con forma de S. Léanla de izquierda a derecha: más puntaje, más probabilidad, pero nunca pasa de 0 ni de 100.',
    'z = 0 da exactamente 50 %: es la línea de la lámina anterior, el punto donde la neurona duda.',
    'Nuestro socio A queda en 94 %. La fórmula está para quien la quiera; lo importante es la forma.',
    '<span class="q">Pregunta rápida:</span> ¿qué probabilidad da z = −2.81? Por simetría, 6 %.'),
    block='02', group=G2, minutes=2, steps=3)

slide('doblar', 'Sin activación, apilar capas no sirve', head('Sin activación, apilar capas no sirve de nada', 'Una suma de sumas sigue siendo una línea. La activación <b>dobla</b> la línea, y con varios dobleces se arma cualquier curva.', key(2)) + demo('bend', 'fill') +
      '<p class="cap">Curva ilustrativa, por ejemplo la demanda de taxis a lo largo del día.</p>',
      notes('<b>Idea clave 2 (parte 2): para qué sirve la activación.</b> Sin ella, cien capas equivalen a una sola suma: solo líneas rectas. Haz clic en «Sin activación»: no importa cuánto se esfuerce, sale una recta.',
            'Ahora 2, 4, 8, 16 neuronas ReLU: cada una aporta un «doblez» (las marcas amarillas abajo) y la curva naranja se pega cada vez más a la línea punteada. Así una red aprende formas complicadas.',
            'Dato para curiosos: esto es la intuición del teorema de aproximación universal: con suficientes neuronas, una capa oculta puede aproximar cualquier función continua.',
            '<span class="q">Pregunta:</span> «Entonces, ¿para qué sirve la activación?» Respuesta esperada: para que la red pueda aprender relaciones que no son líneas rectas.'),
      block='02', group=G2, minutes=3)

# ======================================================================= 03 · cómo aprende
section('b03', '03', 'Cómo aprende una neurona', 'Equivocarse, corregir un poquito y repetir.',
        ['El ciclo', 'La regla', 'Una corrección', 'Míralo aprender', 'El límite: XOR'], 'Viernes · 15 minutos', G3, '03 · Cómo aprende una neurona',
        notes('Aquí está la <b>idea clave 3</b>: el límite de una sola línea (XOR). Cierra el bloque con la práctica 1.'))

slide('ciclo', 'Aprender = equivocarse y corregir', f"""
<div class="split even">
  <div class="col">
    {head('Aprender es equivocarse y corregir', 'Todo el machine learning, del perceptrón a ChatGPT, es este ciclo.')}
    <div class="panel"><p class="say"><b>Como sazonar un locro:</b> pruebas, notas que le falta sal, echas una pizca y vuelves a probar. Una pizca, no medio salero.</p></div>
    <p class="say">Una vuelta completa por todos los ejemplos se llama <b>época</b>.</p>
  </div>
  {demo('cycle', 'fig', labels='Predice|Compara|Corrige|Repite', sub='da una respuesta|¿acertó?|mueve los pesos|con el siguiente')}
</div>""", notes(
    'Predecir, comparar con la respuesta correcta, corregir un poquito, repetir. Eso es todo.',
    'Dos ideas que van a volver: (1) se corrige <b>poco a poco</b> (eso será la tasa de aprendizaje η); (2) una época es una vuelta completa por todos los datos.',
    '<span class="q">Pregunta:</span> «¿Qué pasa si en vez de una pizca echas medio salero?» Te pasas y tienes que corregir al revés: es un η demasiado grande, lo vemos en el bloque 04.'),
    block='03', group=G3, minutes=2, steps=4)

slide('regla', 'La regla del perceptrón', head('La regla del perceptrón: corregir solo cuando falla', 'Si se equivocó, empuja los pesos hacia la respuesta correcta. Si acertó, no toca nada.') + f"""
<div class="col" style="gap:1.6em">
  <div class="formula" style="align-self:flex-start;font-size:1.7em"><m>w \\leftarrow w + \\eta\\, y\\, x \\qquad b \\leftarrow b + \\eta\\, y</m></div>
  <div class="cases">
    {st(1, '<div class="case"><span class="chip" style="background:var(--amber);color:var(--night)">Debía decir sí · y = +1</span><p>Le <b>suma</b> el dato a los pesos: la próxima vez ese socio tendrá más puntaje.</p></div>')}
    {st(2, '<div class="case"><span class="chip" style="background:var(--azure);color:var(--night)">Debía decir no · y = −1</span><p>Le <b>resta</b> el dato: la próxima vez tendrá menos puntaje.</p></div>')}
    {st(3, '<div class="case"><span class="chip ok">Acertó</span><p>No cambia nada. Solo aprende de sus errores.</p></div>')}
  </div>
  {st(3, '<p>' + chip('η (eta) = el tamaño de la corrección', 'hint') + '</p>')}
</div>""", notes(
    'La regla de Rosenblatt (1958) cabe en una línea. Léanla como frase: «el peso nuevo es el peso viejo más un pasito en la dirección de la respuesta correcta».',
    'Si la respuesta correcta era +1 (pagaba) y la neurona dijo que no, sumamos el dato: la próxima vez ese mismo socio tendrá más puntaje. Si era −1, restamos.',
    'Siguiente lámina: la misma cuenta con números.'),
    block='03', group=G3, minutes=2)

slide('correccion', 'Una corrección, con números', head('Una corrección, con números', 'Un socio con x = (1.0, 1.0) que <b>sí pagó</b> (y = +1). La neurona empieza con w = (0.2, −0.5) y b = 0.') + f"""
<div class="three">
  {st(1, '<div class="panel col"><span class="chip bad">Antes</span><p class="num big">z = 0.2 − 0.5 + 0</p><p class="bigread co">−0.30</p><p class="say">Rechaza al socio. <b class="co">Se equivocó.</b></p></div>')}
  {st(2, '<div class="panel col"><span class="chip">Corrige (η = 1)</span><p class="num big">w₁ = 0.2 + 1 = 1.2</p><p class="num big">w₂ = −0.5 + 1 = 0.5</p><p class="num big">b = 0 + 1 = 1</p><p class="say">Le suma el dato a cada peso y 1 al sesgo.</p></div>')}
  {st(3, '<div class="panel col"><span class="chip ok">Después</span><p class="num big">z = 1.2 + 0.5 + 1</p><p class="bigread mi">+2.70</p><p class="say">Ahora aprueba. <b class="mi">Acertó.</b></p></div>')}
</div>""", notes(
    'Hagan esta cuenta despacio. Antes: z = −0.30, la neurona dice «no», pero el socio sí pagó: error.',
    'Corrección con η = 1 y y = +1: a cada peso le sumamos su dato (1) y al sesgo le sumamos 1. Pesos nuevos (1.2, 0.5), sesgo 1.',
    'Después: z = +2.70. Una sola corrección cambió la respuesta. Esto mismo está en el NB01, sección 3.',
    '<span class="q">Pregunta:</span> «¿Y si el socio NO hubiera pagado y la neurona hubiera dicho sí?» Restaríamos el dato.'),
    block='03', group=G3, minutes=2)

slide('entrenar', 'Mira cómo aprende, error por error', head('Mira cómo aprende, error por error', 'Recorre los puntos uno por uno; cada vez que se equivoca, mueve la línea. Si existe una línea que separa los datos, la encuentra.') +
      demo('perceptron', 'fill'),
      notes('Pulsa <b>Entrenar</b> (o avanza con la flecha: arranca solo). El anillo blanco marca el socio que está mirando; si se pone rojo, se equivocó y la línea salta.',
            'Al final de cada vuelta (época) anota cuántos errores tuvo. Cuando una vuelta termina con 0 errores, la línea se pone verde: aprendió.',
            'Esto es una <b>garantía matemática</b>: si los datos se pueden separar con una línea, el perceptrón deja de equivocarse después de un número finito de correcciones (Rosenblatt, 1958; Novikoff, 1962). Es la sección 4 del NB01.',
            'La pregunta que abre la siguiente lámina: ¿y si NO existe esa línea?'),
      block='03', group=G3, minutes=3, steps=1)

slide('xor', 'El primer límite: XOR', f"""
<div class="split" style="grid-template-columns:5fr 6fr">
  <div class="col">
    {head('El primer límite: la luz de la escalera', 'Con dos interruptores, la luz se enciende si están en posiciones <b>distintas</b>. Eso es XOR.', key(3))}
    <p>{chip('Arrastra los extremos de la línea', 'hint')}</p>
    {st(1, '<div class="warnbar"><span><b>No se puede.</b> Una neurona solo traza una recta, y ninguna recta separa XOR.</span></div>')}
    {st(2, '<p class="say">' + chip('1969') + ' Minsky y Papert lo demuestran: llega el primer «invierno» de la IA.</p>')}
  </div>
  {demo('xor', 'fig')}
</div>""", notes(
    '<b>Idea clave 3.</b> La luz de la escalera de cualquier casa: con dos interruptores, se enciende si están en posiciones distintas.',
    'Pide a alguien que te dicte cómo mover la línea. Luego usa «Probar 1 000 líneas al azar»: la mejor siempre separa 3 de 4.',
    'En negocio esto aparece cuando el efecto de una variable depende de otra (una interacción). Por ejemplo: ser socio nuevo es riesgoso solo si además pide un monto alto.',
    'La salida, que veremos mañana: <b>combinar varias neuronas en capas</b>. En el NB01, sección 5, el perceptrón nunca baja de 4 errores con XOR.'),
    block='03', group=G3, minutes=3, steps=2)

practice('practica1', 'Práctica en clase: NB01, secciones 1 a 5', 'Lo que acabamos de ver, ahora con código. Cada tarea te dice ✅ correcto, ❌ todavía no (con una pista) o ⏳ falta.',
         ['§1 · El socio A da <b>z = 2.81</b>', '§2 · Sigmoide ≈ <b>0.943</b>: 94 % de que paga', '§3 · Una corrección: <b>−0.30 → +2.70</b>',
          '§4 · El perceptrón aprende AND: <b>0 errores</b>', '§5 · Con XOR <b>nunca</b> deja de equivocarse'], 'nb01', 20, G3, '03',
         notes('Dinámica: 14 minutos de trabajo individual o en parejas y 6 de puesta en común. Que nadie se quede sin Colab funcionando: es el objetivo de esta práctica.',
               'Si a alguien le sale otra cosa, casi siempre se saltó una celda: <b>Entorno de ejecución → Ejecutar todo</b>.',
               'En la puesta en común pregunta por la sección 5: ¿por qué el perceptrón no aprende XOR? Porque no existe una línea que lo separe.',
               'Recuerda: no hay nota. Los ❌ son para aprender.'))

# ======================================================================= 04 · error y gradiente
section('b04', '04', 'Medir el error y mejorar', 'Bajar la montaña con neblina, paso a paso.',
        ['La pérdida', 'Castigar la falsa seguridad', 'El Cotopaxi', 'La pendiente', 'El tamaño del paso'], 'Viernes · 25 minutos', G4, '04 · Medir el error y mejorar',
        notes('Aquí está la <b>idea clave 4</b>: hacia dónde camina el descenso de gradiente.'))

slide('perdida', 'La pérdida', f"""
<div class="split" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('La pérdida: un número que dice qué tan mal vamos', 'Como una nota al revés: <b>0 es perfecto</b>.')}
    <p class="say">El modelo predice el precio de cuatro casas en Quito y se equivoca por 10, 5, 20 y 2 mil dólares.</p>
    {st(1, '<p class="say"><span class="az">■</span> el error de cada casa</p>')}
    {st(2, '<p class="say"><span class="am">■</span> el error al cuadrado: <b>la casa 3 pesa casi todo</b></p>')}
    {st(3, '<div class="formula" style="font-size:1.15em"><m>\\text{MSE} = \\dfrac{100 + 25 + 400 + 4}{4} = 132.25</m></div>')}
  </div>
  {demo('mse', 'fig plate', style='align-self:center;height:auto;aspect-ratio:1000/560')}
</div>""", notes(
    'Para aprender necesitamos medir qué tan mal lo estamos haciendo con un solo número: la <b>pérdida</b> (loss).',
    'Elevamos cada error al cuadrado (así los negativos no restan) y promediamos: 132.25. Miren las barras: la casa 3, con un error de 20, aporta 400. <b>El MSE castiga fuerte los errores grandes.</b>',
    'Este ejemplo está en el NB01, sección 6. La siguiente lámina: para clasificar (paga o no paga) usamos otra pérdida.'),
    block='04', group=G4, minutes=2, steps=3)

slide('bce', 'Para clasificar: castigar la falsa seguridad', f"""
<div class="split" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('Para clasificar: castigar la falsa seguridad', 'El socio <b>sí pagó</b>. ¿Cuánto castigamos al modelo según lo que dijo?')}
    <p class="say">Como al meteorólogo: si dijo «99 % sin lluvia» y llovió, pierde toda credibilidad.</p>
    <div class="formula" style="font-size:1.15em"><m>\\text{{pérdida}} = -\\log(p)</m></div>
    <p class="say mu" style="font-size:1em">p = la probabilidad que le dio a lo que de verdad pasó. En Keras: <code>binary_crossentropy</code>.</p>
  </div>
  {demo('bce', 'fig')}
</div>""", notes(
    'Para clasificar no usamos el MSE sino la <b>entropía cruzada binaria</b> (BCE). La idea es intuitiva: prueba los tres botones.',
    '99 % → pérdida 0.01, casi nada. 50 % → 0.69, castigo medio. 1 % (estaba «seguro» de que no pagaba) → <b>4.61</b>, el castigo se dispara.',
    'No hace falta más fórmula que esa: menos el logaritmo de la probabilidad que le dio a lo que realmente pasó. Valores exactos en el NB01, sección 6.'),
    block='04', group=G4, minutes=2)

MAP = [('La altura', 'la pérdida'), ('Dónde estás', 'los pesos'), ('La inclinación bajo tus pies', 'el gradiente'), ('El largo de tu paso', 'η, la tasa de aprendizaje')]
slide('cotopaxi', 'Bajar el Cotopaxi con neblina', head('Entrenar es bajar el Cotopaxi con neblina', 'No ves la laguna, pero sientes con el pie hacia dónde baja el terreno. Das un paso. Vuelves a tantear.') + f"""
<div class="split" style="grid-template-columns:8fr 4fr;align-items:stretch">
  {demo('mountain', 'fig')}
  <div class="col" style="justify-content:center;gap:.9em">""" + ''.join(st(i + 1, f'<div class="mapi stack"><span>{a}</span><b>= {b}</b></div>') for i, (a, b) in enumerate(MAP)) + """</div>
</div>""", notes(
    'La analogía central. Estás en la ladera del Cotopaxi con neblina y quieres llegar a la laguna de Limpiopungo, abajo. No ves el camino, pero con el pie sientes hacia dónde baja. Das un paso, vuelves a tantear, otro paso.',
    'La altura es la pérdida; tu posición son los pesos; la inclinación que sientes es el gradiente; el largo del paso es η.',
    'Lo poderoso: no hace falta conocer toda la montaña (que en una red tiene millones de dimensiones), solo la pendiente donde estás.',
    'Límite honesto: podrías quedar en un hoyo que no es el más profundo (un mínimo local); en redes grandes preocupa menos de lo que parece.'),
    block='04', group=G4, minutes=3, steps=6)

slide('pendiente', 'La pendiente dice hacia dónde bajar', f"""
<div class="split" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('La pendiente dice hacia dónde bajar', 'Siempre damos el paso <b>en contra</b> de la pendiente: así la pérdida baja.', key(4))}
    <div class="formula" style="font-size:1.25em"><m>w_{{\\text{{nuevo}}}} = w - \\eta \\cdot \\text{{pendiente}}</m></div>
    <p class="say">Arrastra el punto. Si la pendiente es negativa, el peso sube; si es positiva, baja.</p>
  </div>
  {demo('slope', 'fig')}
</div>""", notes(
    '<b>Idea clave 4.</b> La pendiente (el gradiente) apunta hacia donde la pérdida <b>sube</b>. Por eso restamos: caminamos al revés, cuesta abajo.',
    'Arrastra el punto a la izquierda del mínimo: pendiente negativa → el paso va a la derecha. A la derecha del mínimo: pendiente positiva → el paso va a la izquierda. En el fondo la pendiente es cero y ya no hay que moverse.',
    '<span class="q">Pregunta:</span> «Si la pendiente de un peso es +4, ¿el peso sube o baja?» Baja.'),
    block='04', group=G4, minutes=2)

GD = [('0', '0.00', '−6.00', '9.00'), ('1', '0.60', '−4.80', '5.76'), ('2', '1.08', '−3.84', '3.69'), ('3', '1.46', '−3.07', '2.36'), ('4', '1.77', '−2.46', '1.51')]
gdt = '<div class="gdt"><span class="h">paso</span><span class="h">w</span><span class="h">pendiente</span><span class="h">pérdida</span>' + ''.join(
    (''.join(f'<span class="num">{c}</span>' for c in r) if i == 0 else ''.join(f'<span class="num" data-step="{i}">{c}</span>' for c in r)) for i, r in enumerate(GD)) + '</div>'
slide('pasos', 'Bajando paso a paso, con números', f"""
<div class="split" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('Bajando paso a paso, con números', 'Pérdida (w − 3)², empezando en w = 0, con η = 0.1.')}
    {gdt}
    {st(4, '<div class="keybar"><span>La pérdida baja en cada paso y <b>los pasos se acortan solos</b>: cerca del fondo la pendiente es menor.</span></div>')}
  </div>
  {demo('gdsteps', 'fig plate', style='align-self:center;height:auto;aspect-ratio:900/560')}
</div>""", notes(
    'Hagamos 4 pasos a mano. Sabemos que el mejor w es 3; la gracia es ver cómo el algoritmo lo descubre solo.',
    'La pendiente de esta curva es 2·(w − 3). Paso 1: en w = 0 la pendiente es −6; w nuevo = 0 − 0.1·(−6) = 0.6. Paso 2: pendiente −4.8; w = 1.08. Y así.',
    'La pérdida baja: 9 → 5.76 → 3.69 → 2.36 → 1.51. Es la misma cuenta que hace TensorFlow con millones de pesos. Está en el NB01, sección 7.'),
    block='04', group=G4, minutes=2)

slide('eta', 'El tamaño del paso η', head('El largo del paso η: ni muy corto ni muy largo', 'Misma montaña, distintos tamaños de paso. Prueba los tres botones.') + demo('eta', 'fill'),
      notes('La lección práctica más importante de hoy; la gráfica sale del NB01, sección 8.',
            'Con η = 0.02 va bien encaminado pero necesita cientos de pasos. Con η = 0.4 llega en pocos. Con η = 1.02 se pasa del fondo, cae al otro lado más alto que antes y se va alejando: <b>la pérdida crece en vez de bajar</b>.',
            'Volviendo al locro: es echar medio salero, luego medio vaso de agua… nunca llegas al punto.',
            'En la práctica: si la pérdida sube o sale NaN, lo primero que se revisa es η. En Keras se llama <code>learning_rate</code>.'),
      block='04', group=G4, minutes=3)

REC = ['Predecir', 'Medir la pérdida', 'Calcular la pendiente', 'Dar un paso', 'Repetir']
slide('receta', 'La receta de todo el deep learning', '<div class="col" style="justify-content:center;flex:1;gap:2em">' +
      '<h2 class="display" style="font-size:3.6em;max-width:14em">La receta de todo el deep learning</h2>' +
      '<div class="loop-wrap"><div class="loop live">' + ''.join(st(i + 1, f'<span class="lp{" last" if i == 4 else ""}" style="--i:{i}"><b class="num">{i + 1}</b>{t}</span>') for i, t in enumerate(REC)) + '</div>' +
      '<div class="loop-ret" data-step="5"><span>miles de veces</span></div></div>' +
      st(5, '<p class="lede" style="font-size:1.4em">Así aprende el perceptrón, una red de tres capas y también un modelo de lenguaje con miles de millones de pesos.</p>') + '</div>',
      notes('Si se quedan con una sola lámina del viernes, que sea esta: predecir, medir el error, ver la pendiente, dar un paso, repetir.',
            'Mañana resolvemos dos preguntas: ¿cómo superar el límite de XOR? (con capas) y ¿cómo calcular la pendiente de miles de pesos a la vez? (con retropropagación).'),
      layout='L-statement', block='04', group=G4, minutes=1)

practice('practica2', 'Práctica en clase: NB01, secciones 6 a 8', 'La pérdida, el descenso de gradiente y el tamaño del paso, con código. El Mini-reto 1 queda como práctica opcional.',
         ['§6 · MSE = <b>132.25</b>; BCE: <b>0.01 · 0.69 · 4.61</b>', '§7 · Tu descenso llega a <b>w ≈ −2</b>', '§8 · Compara η: lento, bien y diverge',
          '<b>Mini-reto 1 (opcional)</b> · Tu propio comité de crédito: elige pesos a mano para separar a 6 socios'], 'nb01', 10, G4, '04',
         notes('Diez minutos en clase: que corran las secciones 6 y 7 y vean la gráfica de la 8. El resto queda como práctica opcional en casa.',
               'Respuesta del Tu turno de la sección 8: con η = 0.5 llega en UN paso (en esta parábola es el paso perfecto); con η = 1.1 diverge.',
               'Si sobra tiempo: abran TensorFlow Playground y pongan el learning rate en 3 o en 10: la pérdida «explota». Es el mejor puente hacia mañana.'))

# ======================================================================= cierre viernes
slide('tendencia1', 'Lectura de tendencia: Más allá de Adam', head('Lectura de la semana: «Más allá de Adam»', 'Hoy bajamos la montaña con pasos de tamaño fijo. Los optimizadores modernos ajustan el paso solos. ¿Vale más un mejor algoritmo o más cómputo?', chip('Lectura de tendencia', 'trend')) + f"""
<div class="three trend3">
  {st(1, '<div class="panel col"><span class="bigread li">2024→2025</span><p class="say">Muon, un optimizador nuevo, pasa de récords en competencias abiertas a entrenar <b>Kimi K2</b>, un modelo de un billón de parámetros.</p><p class="cap">Jordan (s. f.); Kimi Team (2025)</p></div>')}
  {st(2, '<div class="panel col"><span class="bigread li">1.4× → 1.1×</span><p class="say">Con una carrera justa para todos, la ventaja se encoge: grande en modelos pequeños, modesta en los grandes.</p><p class="cap">Wen, Hall, Ma y Liang (2025)</p></div>')}
  {st(3, '<div class="panel col"><span class="bigread li">&gt;3× al año</span><p class="say">Crece la capacidad mundial de cómputo dedicada a la IA. Un optimizador mejor ayuda, pero no cambia el orden de magnitud.</p><p class="cap">Stanford HAI, AI Index (2026)</p></div>')}
</div>
{st(4, '<div class="trendbar" style="margin-top:1.2em"><span>Lee la lectura y responde la encuesta en Canvas. <b>No hay respuestas correctas</b>: queremos tu opinión. Mañana, en el bloque 07, hacemos correr a los optimizadores.</span></div>')}""",
      notes('Puente con la lectura de tendencia de la semana 1. No la expliques toda: deja la pregunta abierta.',
            'Las tres cifras salen de la lectura: Muon escaló muy rápido; un estudio de Stanford con un ajuste justo para todos encontró ventajas de ~1.4× en modelos pequeños que bajan a ~1.1× en los grandes; y el cómputo para IA crece más de tres veces por año.',
            'La idea de fondo, que vale para todo el curso: <b>un resultado solo vale tanto como la comparación que lo respalda</b>.',
            'Mañana, en el bloque 07, verán correr a SGD, momentum y Adam en la misma montaña.'),
      block='V', group=GV, minutes=2, label='Cierre del viernes')

slide('cierre-viernes', 'Lo que te llevas hoy', head('Lo que te llevas hoy') + f"""
<div class="col" style="gap:1.1em">
  {st(1, '<div class="mapi big"><span>Una neurona</span><b>suma con pesos y sesgo, y traza una línea</b></div>')}
  {st(2, '<div class="mapi big"><span>La activación</span><b>dobla la línea y da probabilidades</b></div>')}
  {st(3, '<div class="mapi big"><span>Aprender</span><b>es bajar la montaña: pendiente y paso</b></div>')}
  {st(4, '<div class="keybar" style="margin-top:.8em;font-size:1.3em"><span><b>Mañana:</b> ¿cómo vencer a la luz de la escalera (XOR)? Juntando neuronas en capas.</span></div>')}
  {st(4, '<p class="say" style="margin-top:.4em">En el chat, del 1 al 5: <b>¿podrías explicar el descenso de gradiente a un colega?</b></p>')}
</div>""", notes(
    'Cierre de 5 minutos. Repasa las tres ideas pidiendo que alguien las diga con sus palabras antes de mostrar cada una.',
    'Pide el número del 1 al 5 en el chat y anótalo: si el promedio es bajo, el sábado empieza con más repaso.',
    'Logística: la lectura y su encuesta están en Canvas. Al terminar, <b>«Finalizar reunión para todos»</b> para que la grabación se cierre bien.'),
    block='V', group=GV, minutes=3, label='Cierre del viernes')
