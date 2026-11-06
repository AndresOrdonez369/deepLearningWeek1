"""Semana 3 · Encuadre, 00 Recorderis de las semanas 1 y 2, y Tema 1 (generalizar y ser robusto).
Organized by themes, not by days: each session simply continues where the previous one stopped.
Every number comes from data/tema1.json (tools/run_tema1.py, the same code as NB05) or data/fmnist.json (week 2)."""
import json, pathlib
from kit import slide, head, key, chip, st, demo, count, qr, notes, eq, hist, code

D = pathlib.Path(__file__).parent / 'data'
T1 = json.loads((D / 'tema1.json').read_text())
FM = json.loads((D / 'fmnist.json').read_text())
RD, RC = FM['results']['densa'], FM['results']['cnn']
SOB, REG, AUM = T1['sobreajuste'], T1['regularizada'], T1['aumento']
FG, FGV, BUS = T1['fgsm'], T1['fgsm_entrenada'], T1['busqueda']
BEST = BUS['trials'][BUS['best']]


def pct(v, d=1):
    return f'{v * 100:.{d}f} %'


def miles(n):
    return f'{n:,}'.replace(',', ' ')


G0 = 'Encuadre'
GR = '00 · Recorderis: semanas 1 y 2'
G1 = 'Tema 1 · Generalizar y ser robusto'


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


# ======================================================================= encuadre
slide('portada3', 'Acertar no basta', f"""
<div class="cover">
  <div class="left">
    <h1 class="display" style="font-size:5.4em">Acertar no basta</h1>
    <p class="lede" style="font-size:1.45em">Neural Networks: Deep Learning · Robustez, transfer learning y explicabilidad</p>
    <div class="tags after">{chip('UIDE · Maestría en Ciencia de Datos')}{chip('Semana 3')}</div>
    <p class="meta"><b>Andrés Ordóñez-Bolaños, MSc</b><br>Semana 3 · noviembre de 2026 · Microsoft Teams</p>
  </div>
  <div class="right cv" style="padding:6em 4em 6em 0">{demo('adv', 'fig', mode='cover', alt='La foto de un botín y la misma foto con un ruido invisible: la red cambia de botín a zapatilla')}</div>
</div>""", notes(
    '<b>Antes de hablar:</b> verifica que la grabación está corriendo. Comparte esta ventana y abre la vista del presentador con <b>P</b>.',
    'Bienvenida: «En la semana 1 una red aprendió de una tabla; en la semana 2 aprendió a mirar fotos y a leer secuencias. Esta semana nos hacemos otra pregunta: <b>que la red acierte, ¿basta?</b>».',
    'La animación de la derecha es real (Tema 1): la misma foto del botín, con un ruido que no se ve, y la CNN de la semana 2 pasa de «botín 96 %» a «zapatilla 67 %». Es el resumen de la semana: exacto no es lo mismo que confiable.'),
    layout='L-cover', block='E', group=G0, minutes=1, blockname='Encuadre')

ROUTE = [('00', 'Recorderis', 'Las semanas 1 y 2 en una sola cadena, y tres preguntas para calentar.', 'Sin notebook', '≈ 15 min', 'az'),
         ('Tema 1', '¿Funcionará con casos nuevos?', 'Memorizar contra aprender, frenos para la memoria, la foto movida, el ruido invisible y afinar sin trampa.', 'NB05 en clase', '≈ 1 h 45', 'am'),
         ('Tema 2', 'Reutilizar y explicar', 'Transfer learning, dónde miró la red, la prueba de cordura y cómo explicarle un «no» a una socia.', 'NB06 en clase', '≈ 2 h', 'mi'),
         ('Cierre', '¿Le creerías a tu red?', 'Cinco preguntas antes de usar un modelo con personas, tu proyecto y el quiz final.', 'Quiz final', '≈ 40 min', 'li')]
slide('ruta3', 'La semana en dos temas', head('La semana en dos temas', 'Dos preguntas: <b>¿funcionará con casos nuevos?</b> y <b>¿puedo reutilizar lo que otra red aprendió y explicar lo que decide?</b> Antes, un recorderis; al final, el cierre.') +
      '<div class="route4">' + ''.join(st(i + 1, f'<div class="rt {k}"><span class="k num">{a}</span><h3>{t}</h3><p>{d}</p><div class="ft"><span class="chip">{nb}</span><span class="du num">{du}</span></div></div>')
                                       for i, (a, t, d, nb, du, k) in enumerate(ROUTE)) + '</div>' +
      st(4, '<div class="keybar" style="margin-top:1.4em"><span>Cada sesión <b>sigue donde terminó la anterior</b>: el orden importa, el reloj no. Las prácticas son en clase y <b>no tienen nota</b>.</span></div>'),
      notes('La semana tiene dos temas y no está atada a los días. Si el Tema 1 se alarga, el Tema 2 empieza en la sesión siguiente: no pasa nada.',
            'Recorderis: unos 15 minutos para conectar las semanas 1 y 2. Tema 1: sobreajuste, regularización, robustez y búsqueda de hiperparámetros (con el NB05). Tema 2: transfer learning y explicabilidad (con el NB06 y la lectura de tendencia). Cierre: ¿le creerías a tu red?, tu proyecto y el quiz final.',
            'Recalca: <b>las prácticas son en clase y no tienen nota</b>. Los notebooks traen todo el código escrito y comentado: se leen, se ejecutan y se responden preguntas para pensar.',
            'Las duraciones son aproximadas (incluyen las prácticas) y suman unas 4 h 45 de las 6 horas de la semana: hay colchón para preguntas y para lo que se alargue.'),
      block='E', group=G0, minutes=1, steps=4)

slide('prequiz3', 'Pre-quiz: ¿de dónde partimos?', head('Antes de empezar: ¿de dónde partimos?', '8 preguntas cortas tipo Kahoot. <b>No es nota</b>: es tu punto de partida para medir cuánto avanzas esta semana.') + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:1em">
  <ol class="steps-list" style="gap:1.2em">
    {st(1, '<span class="k">1</span><span>Escanea el código o abre <b>deeplearningweek1.vercel.app/?pre3</b></span>', 'li')}
    {st(2, '<span class="k">2</span><span>Escribe tu nombre (el mismo de las semanas 1 y 2) y responde rápido: <b>más rapidez, más puntos</b></span>', 'li')}
    {st(3, '<span class="k">3</span><span>Al final, copia tu código y <b>pégalo en el chat de Teams</b></span>', 'li')}
    {st(3, '<span class="k" style="background:var(--mint);color:var(--night)">✓</span><span>Si no sabes una, elige la que te parezca. Equivocarse aquí es parte del plan.</span>', 'li')}
  </ol>
  <div class="center">{qr('pre3')}</div>
</div>""", notes(
    'Dales 6 minutos. Cuando la mayoría haya pegado su código en el chat, sigue.',
    'Cinco de las ocho preguntas son las <b>ideas clave</b> de la semana 3 y vuelven en el quiz final del cierre. El panel <b>Resultados_quiz.html</b> de la semana 3 lee los códigos del chat.',
    '<span class="q">Pregunta para el chat:</span> «¿Cuál les pareció más difícil?» Anota la respuesta: suele ser la de los ejemplos adversariales o la de la prueba de cordura.'),
    block='E', group=G0, minutes=6)

IDEAS = ['Aprender no es memorizar', 'Regularizar es ponerle frenos a la memoria', 'Exacto no es robusto',
         'Transfer learning: reutilizar lo que otra red ya aprendió', 'Explicar y verificar: una explicación también tiene que pasar pruebas']
slide('metas3', 'Las 5 ideas clave de la semana', head('Al terminar la semana vas a poder explicar estas 5 ideas', 'Las medimos dos veces: en este pre-quiz y en el quiz final del cierre.') +
      '<ol class="steps-list" style="gap:1.05em;margin-top:.4em">' + ''.join(
          st(i + 1, f'<span class="k key">{i + 1}</span><span class="big" style="color:var(--ink)">{t}</span>', 'li') for i, t in enumerate(IDEAS)) + '</ol>' +
      st(5, '<p class="say" style="margin-top:1.2em">Tema 1: <b>ideas 1, 2 y 3</b>. Tema 2: <b>ideas 4 y 5</b>. Cada una tiene su lámina con la etiqueta amarilla <b>Idea clave</b>.</p>'),
      notes('Esta es la promesa de la semana. El hilo: <b>que la red acierte en el examen no basta; tiene que funcionar con casos nuevos, aguantar cambios pequeños, aprovechar lo que ya se sabe y poder explicar por qué decide</b>.',
            'Si al final alguien no puede explicar alguna con sus palabras, la guía de estudio de la semana 3 tiene una sección para cada una.'),
      block='E', group=G0, minutes=1)

# ======================================================================= 00 · recorderis de las semanas 1 y 2
section('b00', '00', 'Recorderis: semanas 1 y 2', 'Antes de preguntarnos si la red es confiable, repasemos en 15 minutos cómo aprende, qué arquitecturas vimos y qué resultados obtuvimos.',
        ['Las dos semanas en una cadena', 'Tres preguntas'], '≈ 15 minutos', GR, '00 · Recorderis: semanas 1 y 2',
        notes('Un repaso corto para conectar: todo lo de esta semana se apoya en el entrenamiento de la semana 1 (pérdida, gradiente, simulacro) y en la CNN de la semana 2.',
              'Si el grupo viene fresco, pasa más rápido; si alguien faltó, detente en los eslabones 2, 5 y 7: son los que más usamos esta semana.'))

CHAIN = [('Neurona', 'z = w·x + b', 'como la nota final: cada dato por lo que pesa · socio A: <b class="num">z = 2.81</b>', 'am'),
         ('Pérdida y gradiente', 'peso − η · pendiente', 'bajar el Cotopaxi con neblina, un paso a la vez; <b>η</b> es el largo del paso', 'co'),
         ('Retropropagación', 'repartir la culpa hacia atrás', 'los engranajes: la regla de la cadena, capa por capa', 'li'),
         ('Keras', 'Sequential · compile · fit', 'TensorFlow es el motor; Keras, el volante', 'az'),
         ('Simulacro y examen', 'estudiar · validar · probar', 'estudia unas fotos, se mide en un <b>simulacro</b> y al final en el <b>examen</b>', 'mi'),
         ('La suposición', 'densa · CNN · RNN · atención', 'cada arquitectura es una apuesta sobre cómo están organizados los datos', 'am'),
         ('La lupa de la CNN', 'filtros compartidos', f'la CNN acierta el <b class="num">{pct(RC["test"])}</b> con 8 veces menos números', 'am'),
         ('Mover la prenda', '2 píxeles a la derecha', f'densa <b class="num">{pct(RD["shift"]["2"])}</b>, CNN <b class="num">{pct(RC["shift"]["2"])}</b>; con 4 píxeles, las dos se caen', 'co'),
         ('La atención', 'buscar el dato exacto', 'con 80 pasos las recurrentes adivinan; la atención acierta el <b class="num">100 %</b>', 'mi')]
slide('recorderis3', 'Las semanas 1 y 2 en una sola cadena', head('Las semanas 1 y 2 en una sola cadena', 'Nueve eslabones: cómo aprende una red y cómo se elige su forma.') +
      '<div class="chain9">' + ''.join(st(i + 1, f'<div class="ch {k}"><span class="i num">{i + 1}</span><h3>{t}</h3><span class="f">{f}</span><p>{a}</p></div>') for i, (t, f, a, k) in enumerate(CHAIN)) + '</div>' +
      st(10, '<div class="keybar" style="margin-top:1em"><span>Ya sabemos construir redes que <b>aciertan</b>. Esta semana: ¿funcionan con <b>casos nuevos</b>? ¿Las podemos <b>reutilizar</b> y <b>explicar</b>?</span></div>'),
      notes('Un clic por eslabón. Antes de cada clic, pregunta: «¿qué venía después?». Que lo digan ellos; la lámina solo confirma.',
            '1 · La neurona multiplica cada dato por su peso, suma y añade el sesgo (la nota final del curso). 2 · La pérdida mide qué tan mal vamos y el gradiente dice hacia dónde bajar: el Cotopaxi con neblina. 3 · La retropropagación reparte la culpa hacia atrás. 4 · Keras lo hace en cuatro pasos.',
            '5 · <b>El eslabón más importante para esta semana:</b> entrenamiento (lo que estudia), validación (el simulacro, que no estudia) y prueba (el examen final). Con <code>validation_split=0.2</code> ya lo usábamos.',
            f'6 · Cada arquitectura es una suposición. 7 · La CNN comparte sus filtros: {pct(RC["test"])} con 12 810 parámetros contra {pct(RD["test"])} de la densa con 101 770. 8 · Al mover la prenda 2 píxeles, la densa cayó a {pct(RD["shift"]["2"])}; con 4 píxeles la CNN también cayó, a {pct(RC["shift"]["4"])}. 9 · La atención va a buscar el dato: 100 % con 82 parámetros.',
            'Paso 10, el puente: <span class="q">«Ya sabemos construir redes que aciertan. ¿Funcionarán con casos nuevos? ¿Las podemos reutilizar y explicar?»</span> Son el Tema 1 y el Tema 2.'),
      block='00', group=GR, minutes=8, steps=10)

QA3 = [('En <code>fit(…, validation_split=0.2)</code>, ¿qué es ese <b class="num">20 %</b>?', 'El <b>simulacro</b>: fotos que la red no estudia.', 'Sirve para ver si aprende o memoriza, y para decidir sin tocar el examen final. Lo usamos en todo el Tema 1.'),
       ('¿Por qué la CNN necesita unas <b>8 veces menos</b> parámetros que la densa?', '<b>Comparte sus filtros.</b> El mismo filtro de 9 pesos recorre toda la foto.', '12 810 contra 101 770 números, y aun así acierta más.'),
       ('La CNN acierta el <b class="num">87.7 %</b>. Si movemos cada foto <b>4 píxeles</b>, ¿cuánto acierta?', f'<b>{pct(RC["shift"]["4"])}</b>. Se cae.', 'Exacta no significa robusta: es el punto de partida del Tema 1.')]
slide('recorderis3-preguntas', 'Tres preguntas para calentar', head('Tres preguntas para calentar', 'Respondan en el chat <b>antes</b> de que aparezca la respuesta. Vienen de las semanas 1 y 2.') +
      '<div class="qa3">' + ''.join(f'<div class="qr3"><span class="n num">{i + 1}</span><p class="q">{q}</p>' + st(i + 1, f'<div class="a"><p class="ans">{a}</p><p class="why">{w}</p></div>') + '</div>' for i, (q, a, w) in enumerate(QA3)) + '</div>',
      notes('Práctica de recuerdo: es lo que mejor fija lo aprendido. Lee la pregunta, espera 20 segundos de respuestas en el chat y solo entonces avanza.',
            '1 · El simulacro. Si alguien dice «es para probar el modelo al final», aclara: ese es el examen final (la prueba), y se mira una sola vez.',
            '2 · Compartir pesos: un filtro de 3 × 3 tiene 9 pesos y 1 sesgo, y sirve en las 676 posiciones de la foto. Es la idea clave 3 de la semana 2.',
            f'3 · La sorpresa: {pct(RC["test"])} sin mover, {pct(RC["shift"]["4"])} con 4 píxeles. Lo vimos en el duelo del NB03. Esta semana aprendemos a que aguante.'),
      block='00', group=GR, minutes=6, steps=3)

# ======================================================================= Tema 1 · generalizar y ser robusto
section('b01', '01', '¿Funcionará con casos nuevos?', 'Una red que acierta lo que ya vio no garantiza nada. Hay que probarla con lo que no vio y con lo que cambia.',
        ['Memorizar', 'Por qué memoriza', 'Frenos', 'Aumento', 'Con frenos', 'En Keras', 'Mover la foto', 'Ruido invisible', 'La receta', 'Vacunar', 'El mundo cambia', 'Afinar', 'Práctica NB05'],
        'Tema 1 · ≈ 1 h 45 con el NB05', G1, 'Tema 1 · Generalizar y ser robusto',
        notes('<b>Tema 1.</b> Aquí están las <b>ideas clave 1, 2 y 3</b>. Termina con la práctica NB05 y un cierre del tema.',
              'Si la sesión se acaba en medio del tema, no pasa nada: la siguiente sigue donde quedamos.'), shown='T1')

slide('memorizar3', 'Aprender no es memorizar', head('Aprender no es memorizar', f'La CNN de la semana 2 estudia solo <b>1 000 fotos</b>, 60 épocas. Como quien memoriza el solucionario: <b>{pct(SOB["train_acc"][-1])}</b> en lo que estudió y <b>{pct(SOB["val_acc"][-1])}</b> en el simulacro.', key(1)) +
      demo('curvas', 'fill', mode='uno') +
      st(3, f'<div class="keybar" style="margin-top:.6em;flex:none"><span><b>El sobreajuste:</b> la pérdida de entrenamiento <b>sigue bajando</b> y la del simulacro <b>sube</b>. Examen final: <b class="num">{pct(SOB["test"])}</b>.</span></div>'),
      notes('<b>Idea clave 1.</b> Curvas reales del NB05 (sección 1). Paso 1: la pérdida de entrenamiento (ámbar) baja época tras época, hasta 0.14. Si solo miráramos esta curva, diríamos que la red es excelente.',
            f'Paso 2: la del simulacro (blanca punteada) baja al principio y después se queda quieta y <b>sube</b>: su mínimo es en la <b>época {SOB["best_epoch"]}</b> (0.53) y termina en 0.58. Las dos curvas se separan: eso es el <b>sobreajuste</b>.',
            f'Paso 3: el nombre, sobreajuste. Es el estudiante que se aprende de memoria el solucionario del examen pasado: saca 100 en los ejercicios que ya vio y falla los nuevos. En exactitud: {pct(SOB["train_acc"][-1])} en lo estudiado contra {pct(SOB["val_acc"][-1])} en el simulacro; en el examen final, {pct(SOB["test"])}. Mueve el deslizador para mostrar dónde empiezan a separarse.',
            '<span class="q">Pregunta:</span> «Si fueran el profesor de esta red, ¿en qué época la habrían mandado a dar el examen?» (cerca de la 33, cuando el simulacro estaba mejor).'),
      block='01', group=G1, minutes=6, steps=3)

SETS = [('Entrenamiento', 'las fotos que <b>estudia</b> · aquí 1 000', 'el cuaderno de ejercicios'),
        ('Validación', 'el <b>simulacro</b> · 2 000 fotos que no estudia', 'decide cuándo parar y qué ajustar'),
        ('Prueba', 'el <b>examen final</b> · 10 000 fotos', 'se mira una sola vez, al final')]
REASONS = [('Muchos números, pocos ejemplos', 'La CNN tiene <b>12 810</b> números que aprender y solo ve <b>1 000</b> fotos: unos 13 números por foto. Le alcanza para guardarse detalles.'),
           ('Estudiar de más', 'En 60 épocas ve <b>cada foto 60 veces</b>. Llega un momento en que ya no aprende nada general: repasa lo mismo.'),
           ('Detalles que no se repiten', 'Una arruga, una sombra o un fondo raro existen solo en <b>esas</b> fotos. Si los aprende, no le sirven para fotos nuevas.')]
slide('por-que-memoriza', '¿Por qué memoriza?', head('¿Por qué memoriza una red?', 'Memorizar no es un error de programación: es lo que pasa cuando la red puede guardarse los detalles de sus ejemplos.', key(1)) +
      '<div class="sets3">' + ''.join(st(1, f'<div class="mapi"><span>{a}</span><b>{b}</b><span style="font-weight:400">{c}</span></div>') for a, b, c in SETS) + '</div>' +
      '<div class="three9" style="margin-top:1.2em">' + ''.join(st(i + 2, f'<div class="c9 co"><h3>{t}</h3><p>{d}</p></div>') for i, (t, d) in enumerate(REASONS)) + '</div>' +
      st(4, '<div class="keybar" style="margin-top:1.1em"><span><b>El mejor remedio es tener más datos.</b> La misma red con las 60 000 fotos llega a <b class="num">87.7 %</b> en el examen; con 1 000, a <b class="num">' + pct(SOB['test']) + '</b>.</span></div>'),
      notes('Paso 1: los tres montones de fotos, con sus papeles. Es la regla de oro de la semana: <b>lo que se usa para decidir no puede ser el examen final</b>. Si afinamos mirando el examen, el examen deja de medir casos nuevos.',
            'Pasos 2 a 4: las tres causas. 12 810 parámetros para 1 000 fotos; 60 vueltas a las mismas fotos; detalles que solo existen en esas fotos. Por eso la pérdida de entrenamiento sigue bajando: la red se acomoda cada vez mejor a sus 1 000 fotos.',
            'El remedio más fuerte: más datos (80.9 % con 1 000 fotos, 87.7 % con las 60 000, con la misma red y el mismo código). Cuando no hay más datos, se usan frenos: la lámina siguiente.',
            '<span class="q">Pregunta:</span> «En su proyecto, ¿cuántos ejemplos tienen y cuántos parámetros tendría su red?»'),
      block='01', group=G1, minutes=6, steps=4)

ICSTOP = ('<svg viewBox="0 0 440 300" aria-hidden="true"><path d="M30 60 C 120 220, 200 250, 410 262" fill="none" stroke="#ffb541" stroke-width="6"/>'
          '<path d="M30 40 C 110 200, 170 210, 230 205 S 330 175, 410 150" fill="none" stroke="#f1f6fa" stroke-width="5" stroke-dasharray="12 9"/>'
          '<line x1="230" y1="20" x2="230" y2="280" stroke="#64eab7" stroke-width="5" stroke-dasharray="6 8"/>'
          '<rect x="246" y="28" width="150" height="46" rx="10" fill="#64eab7"/><text x="321" y="60" text-anchor="middle" font-size="26" font-weight="700" fill="#07101c" font-family="Lexend, sans-serif">¡para aquí!</text></svg>')
BRAKES = [('Dropout', demo('dropout', ''), 'Un equipo en el que, en cada partido, <b>puede faltar cualquiera</b>: nadie depende de un solo compañero.', 'en cada lote descansa al azar una parte de las neuronas'),
          ('Aumento de datos', demo('aumento', '', mode='mini'), '<b>Practicar con la prenda movida</b>: así no te sorprende verla corrida.', 'en cada época, versiones un poco movidas de las mismas fotos'),
          ('Parar a tiempo', ICSTOP, '<b>Dejar de estudiar</b> cuando el simulacro empieza a salir peor.', '<i>early stopping</i>: vigila el simulacro y se queda con la mejor época')]
slide('frenos', 'Regularizar: frenos para la memoria', head('Regularizar es ponerle frenos a la memoria', 'Tres frenos que se usan casi siempre: hacen que memorizar sea más difícil que aprender.', key(2)) +
      '<div class="cards3 frn3">' + ''.join(st(i + 1, f'<div class="acard"><div class="ic">{ic}</div><h3 class="am">{t}</h3><p class="sup">{a}</p><p class="ex">{e}</p></div>') for i, (t, ic, a, e) in enumerate(BRAKES)) + '</div>' +
      st(4, '<p class="say" style="margin-top:.9em">De pasada: <b>L2</b> castiga los pesos grandes. Y el freno más fuerte sigue siendo <b>tener más datos</b>.</p>'),
      notes('<b>Idea clave 2.</b> Paso 1, <b>dropout</b>: en cada lote, el 30 % de las neuronas (por ejemplo) descansa al azar; las demás tienen que aprender a jugar sin ellas. Al predecir juegan todas. La animación muestra un lote distinto cada segundo.',
            'Paso 2, <b>aumento de datos</b>: en cada época la red ve la misma prenda movida un poco hacia un lado. No son fotos nuevas, pero se parecen a lo que el mundo puede mostrar.',
            'Paso 3, <b>parar a tiempo</b> (early stopping): la red vigila el simulacro; si deja de mejorar durante varias épocas, se detiene y vuelve a la mejor. Es lo que habríamos querido en la época 33.',
            'Paso 4: L2 de pasada (suma a la pérdida el tamaño de los pesos). No lo usamos en el NB05, pero lo verán en artículos con el nombre «weight decay».',
            '<span class="q">Pregunta:</span> «¿Qué freno usarían con un historial de pagos? ¿Tiene sentido mover un historial como movemos una foto?» (no siempre: el aumento debe respetar lo que los datos significan).'),
      block='01', group=G1, minutes=6, steps=4)

slide('aumento', 'Aumento de datos: la misma prenda, movida', head('Aumento: la misma prenda, movida', 'No son fotos nuevas: son <b>versiones distintas</b> de las mismas, otras en cada época. Un botín movido sigue siendo un botín.', key(2)) +
      demo('aumento', 'fill') +
      st(1, '<div class="warnbar" style="margin-top:.6em;flex:none"><span><b>Solo cambios que no cambien la respuesta:</b> mover un poco la prenda, sí; ponerla de cabeza, no.</span></div>'),
      notes('Fotos reales de Fashion-MNIST. A la derecha, lo que estudia la red en una época: 10 copias del botín movidas al azar hasta 4 píxeles (<code>RandomTranslation(0.15)</code>: 15 % de 28). Cada dos segundos, otra época, otras copias.',
            'El borde se rellena como un espejo: es lo que hace Keras por defecto. Cambia de prenda con los botones de abajo.',
            'Paso 1: la regla. Las transformaciones tienen que ser realistas para tus datos: en radiografías no se voltea izquierda-derecha si el corazón importa; en texto se cambian palabras por sinónimos, no por cualquier cosa.',
            '<span class="q">Pregunta:</span> «¿Qué aumento tendría sentido para fotos de cultivos tomadas con un celular?» (girar un poco, cambiar el brillo, acercar).'),
      block='01', group=G1, minutes=4, steps=1)

slide('regularizada', 'Con frenos: lo que pasó', head('Con frenos: lo que pasó', 'Las mismas 1 000 fotos con <b>aumento</b>, <b>dropout</b> y <b>parar a tiempo</b>, y hasta 100 épocas.', key(2)) +
      demo('curvas', 'fill', mode='dos') +
      st(3, f'<div class="keybar" style="margin-top:.5em;flex:none"><span>Las curvas ya no se separan. Los frenos ayudan <b>un poco</b> (<b class="num">{pct(SOB["test"])} → {pct(REG["test"])}</b>); <b>más datos ayudan mucho</b>: con las 60 000 fotos, <b class="num">87.7 %</b>.</span></div>'),
      notes(f'Paso 1: la red sin frenos, la misma de hace dos láminas: se separan las curvas desde la época {SOB["best_epoch"]}.',
            f'Paso 2: con frenos. Las curvas van juntas durante muchas más épocas. EarlyStopping se detiene solo en la época {REG["epochs"]} porque el simulacro no mejoró durante 8 épocas, y vuelve a los pesos de la época <b>{REG["best_epoch"]}</b>.',
            f'Paso 3: la lección honesta. En el examen final, {pct(SOB["test"])} sin frenos y {pct(REG["test"])} con frenos: menos de un punto. Lo que cambia es que ya no memoriza: el simulacro y el examen dicen lo mismo. Y la mejora grande viene de más datos (87.7 %).',
            '<span class="q">Pregunta:</span> «Si los frenos solo ganan menos de un punto, ¿para qué usarlos?» (para que el simulacro sea confiable, para poder entrenar más tiempo sin miedo y porque con pocos datos no hay alternativa).'),
      block='01', group=G1, minutes=6, steps=3)

KCODE = code("""
model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.RandomTranslation(0.05, 0.05),  # shifts
    layers.Conv2D(16, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Flatten(),
    layers.Dropout(0.3),                   # rests
    layers.Dense(10, activation="softmax"),
])
stop = keras.callbacks.EarlyStopping(monitor="val_loss",
    patience=8, restore_best_weights=True)
model.fit(x_small, y_small, epochs=100, callbacks=[stop],
          validation_data=(x_val, y_val))
""", hl='1:3;2:9;3:12-15', cls='sm', style='line-height:1.48')
KSTEPS = [('RandomTranslation(0.05, 0.05)', 'mueve cada foto hasta un 5 % (≈ 1 píxel). Solo al entrenar.'),
          ('Dropout(0.3)', 'en cada lote apaga al azar el 30 % de los 800 números antes de la salida. Al predecir, juegan todos.'),
          ('EarlyStopping(patience=8, …)', 'un <i>callback</i>: si el simulacro no mejora en 8 épocas, para y vuelve a la mejor.')]
slide('keras-frenos', 'Los frenos en Keras', head('Los frenos en Keras: tres líneas', 'La CNN de la semana 2, con dos capas nuevas y un <i>callback</i>.') + f"""
<div class="split" style="grid-template-columns:7fr 5fr;gap:2em;align-items:start">
  {KCODE}
  <div class="col" style="gap:.9em">
    """ + ''.join(st(i + 1, f'<div class="mapi stack" style="font-size:1.12em"><span style="font-family:var(--mono)">{a}</span><b>{b}</b></div>') for i, (a, b) in enumerate(KSTEPS)) + """
    """ + st(3, f'<p class="say">Para en la <b class="num">{REG["epochs"]}</b>, se queda con la <b class="num">{REG["best_epoch"]}</b>: <b class="num">{pct(REG["test"])}</b> en el examen.</p>') + """
  </div>
</div>""", notes(
    'Es el código de la sección 2 del NB05. Un clic por freno: se ilumina la línea y su explicación.',
    '<code>RandomTranslation</code> y <code>Dropout</code> son capas que <b>solo actúan al entrenar</b>. Al llamar a <code>predict</code> o <code>evaluate</code>, la foto pasa sin moverse y todas las neuronas trabajan. Keras lo maneja solo.',
    '<code>EarlyStopping</code> no es una capa: es un <i>callback</i>. <code>patience=8</code>: cuántas épocas espera sin mejora. <code>restore_best_weights=True</code>: sin esto, se quedaría con los pesos de la última época, no con los de la mejor.',
    '<span class="q">Pregunta:</span> «¿Por qué <code>EarlyStopping</code> mira <code>val_loss</code> y no <code>loss</code>?» (la pérdida de entrenamiento casi siempre baja: solo el simulacro avisa que está memorizando).'),
    block='01', group=G1, minutes=4, steps=3)

slide('aumento-mover', 'Mover la foto: con aumento, la red aguanta', head('Mover la foto: con aumento, aguanta', '60 000 fotos y 5 épocas, como en la semana 2. Después movemos las fotos del examen de 1 a 4 píxeles.', key(3)) +
      demo('mover', 'fill') +
      st(3, f'<div class="keybar" style="margin-top:.5em;flex:none"><span>Con 4 píxeles: <b class="num">{pct(AUM["sin"]["shift"]["4"])} → {pct(AUM["con"]["shift"]["4"])}</b>. El precio: sin mover, de {pct(AUM["sin"]["test"])} a {pct(AUM["con"]["test"])}.</span></div>'),
            notes(f'Sección 3 del NB05. Paso 1: la CNN de la semana 2 (sin aumento): {pct(AUM["sin"]["test"])} sin mover; {pct(AUM["sin"]["shift"]["1"])}, {pct(AUM["sin"]["shift"]["2"])}, {pct(AUM["sin"]["shift"]["3"])} y {pct(AUM["sin"]["shift"]["4"])} al mover 1, 2, 3 y 4 píxeles. Cada píxel es un precipicio.',
            f'Paso 2: la misma red entrenada con <code>RandomTranslation(0.15)</code>: {pct(AUM["con"]["test"])}, {pct(AUM["con"]["shift"]["1"])}, {pct(AUM["con"]["shift"]["2"])}, {pct(AUM["con"]["shift"]["3"])} y {pct(AUM["con"]["shift"]["4"])}. La línea casi plana es la robustez.',
            'Paso 3: el precio. Con fotos sin mover pierde unos 5 puntos con el mismo presupuesto de 5 épocas. Con más épocas esa diferencia se achica; la robustez se queda.',
            '<span class="q">Pregunta:</span> «En su proyecto, ¿qué sería “mover la foto”?» (otra cámara, otra hora del día, otro formulario, otra sucursal).'),
      block='01', group=G1, minutes=5, steps=3)

slide('adversarial', 'Exacto no es robusto: el ruido invisible', head('Exacto no es robusto: el ruido invisible', f'La CNN acierta el <b>{pct(FG["limpia"])}</b>. Le sumamos a una foto un ruido invisible, calculado para engañarla.', key(3)) +
      demo('adv', 'fill') +
      st(3, '<div class="keybar" style="margin-top:.5em;flex:none"><span>Para nosotros es la misma foto; para la red, una <b>zapatilla</b>. Es un <b>ejemplo adversarial</b> (Goodfellow et al., 2015).</span></div>'),
            notes(f'Datos reales de la sección 4 del NB05: el primer botín del examen. Paso 1: la red dice botín con {round(T1["ejemplo_adv"]["p_orig"][9] * 100)} %.',
            'Paso 2: el ruido, aumentado para que se vea. Cada píxel se mueve como máximo 13 de 255 (ε = 0.05): ámbar si sube, azul si baja. No es al azar: cada píxel se movió justo hacia donde más le molesta a la red.',
            f'Paso 3: la foto engañosa. La red dice zapatilla con {round(T1["ejemplo_adv"]["p_adv"][7] * 100)} % y botín solo con {round(T1["ejemplo_adv"]["p_adv"][9] * 100)} %. A la vista, idénticas.',
            'Lectura de tendencia: «basta con alterar los píxeles de una imagen de forma imperceptible para que una red la clasifique mal con total seguridad». Pasa con redes pequeñas como esta y con redes gigantes.',
            '<span class="q">Pregunta:</span> «¿Dónde sería peligroso esto?» (una señal de tránsito para un auto autónomo, un documento escaneado, un filtro de contenido).'),
      block='01', group=G1, minutes=5, steps=3)

FCODE = code("""
x = tf.convert_to_tensor(photos)
with tf.GradientTape() as tape:
    tape.watch(x)                  # slope per pixel
    loss = loss_fn(labels, model(x))
grad = tape.gradient(loss, x)
x_adv = x + eps * tf.sign(grad)    # one step uphill
x_adv = tf.clip_by_value(x_adv, 0, 1)   # valid photo
""", hl='1:2-5;2:6;3:7', cls='sm')
slide('fgsm-cuenta', 'La receta: subir la montaña a propósito', head('La receta: subir la montaña a propósito', 'En la semana 1 los <b>pesos</b> bajaban para que la pérdida baje. Aquí cada <b>píxel</b> sube un poquito para que la pérdida suba.', key(3)) + f"""
<div class="split" style="grid-template-columns:7fr 4.6fr;gap:2em;align-items:start">
  <div class="col" style="gap:1em">
    """ + eq([("x'", 'la foto engañosa', 'out'), ('=', '', 'op'), ('x', 'la foto', 'x'), ('+', '', 'op'), (r'\varepsilon', 'cuánto se mueve cada píxel', 'eta'), (r'\cdot', '', 'op'), (r'\text{signo}(\nabla_x \text{pérdida})', '¿sube o baja la pérdida con cada píxel?', 'w')],
             read='la pendiente de la pérdida respecto a cada píxel dice hacia dónde «duele» más. Se toma solo su signo (+1 o −1) y se da <b>un paso de tamaño ε</b> en esa dirección.', size='.84em') + """
    """ + FCODE + """
  </div>
  """ + demo('subir', 'fig') + """
</div>""", notes(
    'Se llama <b>FGSM</b> (Fast Gradient Sign Method, Goodfellow et al., 2015). Es la sección 4 del NB05, a mano con <code>GradientTape</code>.',
    'Paso 1: la semana 1. Entrenar es mover los pesos <b>en contra</b> de la pendiente: la pérdida baja. Paso 2: atacar es mover los píxeles <b>a favor</b> de la pendiente: la pérdida sube. Los pesos quedan quietos: solo cambia la foto.',
    '<code>GradientTape</code> es la grabadora de TensorFlow: anota las cuentas para después calcular pendientes. <code>tape.watch(x)</code> le pide la pendiente respecto a los píxeles (normalmente la calcula respecto a los pesos). <code>clip_by_value</code> mantiene cada píxel entre 0 y 1.',
    'ε = 0.05 en una foto de 0 a 1 son 13 de 255 en brillo: invisible para nosotros.',
    '<span class="q">Pregunta:</span> «¿Qué información necesita el atacante?» (en esta versión, la red misma para calcular la pendiente; existen ataques que no la necesitan).'),
    block='01', group=G1, minutes=6, steps=3)

slide('fgsm-curva', '¿Cuánto ruido aguanta? La vacuna', head('¿Cuánto ruido aguanta? Y la vacuna', '<b>Entrenamiento adversarial:</b> cada lote trae las fotos limpias <b>y su versión engañosa</b>. Es vacunarse.', key(3)) +
      demo('fgsm', 'fill') +
      st(2, f'<div class="keybar" style="margin-top:.5em;flex:none"><span>Con ε = 0.05: <b class="num">{pct(FG["0.05"])} → {pct(FGV["0.05"])}</b>. La vacuna tiene un costo: con fotos limpias baja de {pct(FG["limpia"])} a {pct(FGV["limpia"])}.</span></div>'),
      notes(f'Secciones 4 y 5 del NB05, con las 10 000 fotos del examen. Paso 1: la red normal. Con ε = 0.01 baja a {pct(FG["0.01"])}; con 0.02, a {pct(FG["0.02"])}; con 0.05, a {pct(FG["0.05"])}; con 0.1, a {pct(FG["0.1"])}. Usa los botones para ver cada foto.',
            f'Paso 2: la red vacunada (5 épocas; cada lote mezcla fotos limpias y su versión FGSM con ε = 0.05, calculada con los pesos de ese momento). Con ε = 0.05, {pct(FGV["0.05"])}; con 0.1, {pct(FGV["0.1"])}.',
            'Honestidad: la vacuna protege sobre todo contra el ataque con el que se entrenó; contra ataques más fuertes, protege menos. Y cuesta unos puntos con fotos limpias. No hay robustez gratis.',
            '<span class="q">Pregunta:</span> «Con ε = 0.1 la foto ya se ve sucia. ¿Cuenta como engaño?» (sí: depende de qué cambios son razonables en tu aplicación).'),
      block='01', group=G1, minutes=5, steps=2)

CHANGE = [('Mover la foto', f'<span class="big9">{pct(AUM["sin"]["test"])} → {pct(AUM["sin"]["shift"]["4"])}</span>', 'Cuatro píxeles a la derecha. La cámara se corrió un poco.', 'NB05 · sección 3'),
          ('Ruido invisible', f'<span class="big9">{pct(FG["limpia"])} → {pct(FG["0.05"])}</span>', 'Un cambio de 13 de 255 en cada píxel, hecho a propósito para engañarla.', 'NB05 · sección 4'),
          ('El mundo cambia', '<span class="big9" style="font-size:1.6em;line-height:1.15">urbanos → rurales</span>', 'Un modelo de crédito entrenado con socios urbanos se usa con socios rurales, o antes y después de una crisis.', 'Lectura de tendencia')]
slide('mundo-cambia', 'El mundo cambia y el modelo no avisa', head('El mundo cambia y el modelo no avisa', 'Tres cambios pequeños que tumban a un modelo exacto. El tercero es el más común y el más silencioso.', key(3)) +
      '<div class="three9">' + ''.join(st(i + 1, f'<div class="c9 co"><h3>{t}</h3>{b}<p>{d}</p><span class="src">{s}</span></div>') for i, (t, b, d, s) in enumerate(CHANGE)) + '</div>' +
      st(4, '<div class="trendbar" style="margin-top:1.2em">' + chip('Lectura de tendencia', 'trend') + '<span>«El modelo no avisa: sigue respondiendo con la misma seguridad». Una explicación de un modelo que no generaliza puede ser <b>una explicación muy clara de un error</b>.</span></div>') +
      st(4, '<p class="say" style="margin-top:.8em">Por eso: probar con datos <b>parecidos a donde se va a usar</b>, y seguir midiendo después de ponerlo a trabajar.</p>'),
      notes('<b>Idea clave 3, completa.</b> Los dos primeros los medimos en el NB05. El tercero es el que más pasa en la vida real: los datos del futuro no se parecen a los de entrenamiento.',
            'Ejemplos de «el mundo cambia»: la cooperativa abre agencias en el campo; cambia la economía; el hospital compra otra máquina de rayos X; la gente empieza a escribir reclamos por WhatsApp en vez de correo.',
            'Lo peligroso: el modelo no lanza un error. Da una respuesta igual de segura. Por eso se vigila: comparar cada mes la distribución de los datos nuevos con la de entrenamiento y medir con casos revisados.',
            '<span class="q">Pregunta:</span> «En su proyecto, ¿qué cambio del mundo podría tumbar al modelo?»'),
      block='01', group=G1, minutes=5, steps=4)

slide('hiperparametros', 'Afinar sin hacer trampa', head('Afinar sin hacer trampa: búsqueda al azar', '<b>Parámetros</b>: lo que la red aprende. <b>Hiperparámetros</b>: lo que tú eliges antes. Probamos 6 combinaciones al azar y elegimos con el <b>simulacro</b>.') + f"""
<div class="split" style="grid-template-columns:9fr 3.4fr;gap:1.8em;align-items:start">
  {demo('busqueda', '')}
  <div class="col" style="gap:1em">
    <div class="analog"><span class="t">Afinar la guitarra con el simulacro</span><p>Se afina tocando en el ensayo, nunca en el concierto. Si afinas mirando el examen final, el examen deja de medir casos nuevos.</p></div>
    {st(3, '<p class="say">Tocar el examen <b>una sola vez</b>, al final, es lo que hace creíble el número.</p>')}
  </div>
</div>""", notes(
    f'Sección 6 del NB05: 10 000 fotos para estudiar, 4 épocas, un simulacro de 5 000. Paso 1: las 6 combinaciones al azar entre learning rate (0.0001, 0.001, 0.01), filtros (8, 16 o 32 en la primera capa, el doble en la segunda) y dropout (0 o 0.3).',
    f'Paso 2: la mejor en el simulacro: learning rate {BEST["lr"]}, {BEST["f1"]} filtros, dropout {BEST["drop"]} ({miles(BEST["params"])} parámetros): {pct(BEST["val"])}. Fíjense en la peor: learning rate 0.0001 aprende muy lento en 4 épocas ({pct(BUS["trials"][2]["val"])}).',
    f'Paso 3: la mejor va al examen final una sola vez: {pct(BUS["test_best"])}. Casi igual que el simulacro: señal de que no hicimos trampa.',
    'Por qué al azar y no probar todo: con 3 × 3 × 2 = 18 combinaciones ya es mucho; con 6 hiperparámetros serían miles. Probar al azar suele encontrar algo bueno con pocos intentos (Bergstra y Bengio, 2012). Hay herramientas que lo automatizan, como KerasTuner u Optuna.',
    '<span class="q">Pregunta:</span> «¿Qué pasaría si eligiéramos la combinación mirando el examen final?» (el 86.9 % sería optimista: ya no mide casos nuevos).'),
    block='01', group=G1, minutes=6, steps=3)

practice('practica-nb05', 'Práctica en clase: NB05', 'En parejas. Todo el código ya viene escrito y comentado. Antes de cada celda, apuesta qué va a salir.',
         [f'<b>1</b> · El estudiante que memoriza: <b>{pct(SOB["train_acc"][-1])}</b> estudiando, <b>{pct(SOB["val_acc"][-1])}</b> en el simulacro; el mejor en la época <b>{SOB["best_epoch"]}</b>',
          f'<b>2</b> · Con frenos: para en la <b>{REG["epochs"]}</b>, se queda con la <b>{REG["best_epoch"]}</b>, examen <b>{pct(REG["test"])}</b>',
          f'<b>3</b> · Mover 4 píxeles: sin aumento <b>{pct(AUM["sin"]["shift"]["4"])}</b>, con aumento <b>{pct(AUM["con"]["shift"]["4"])}</b>',
          f'<b>4</b> · El botín engañado: <b>zapatilla 67 %</b>; con ε = 0.05 la red acierta <b>{pct(FG["0.05"])}</b>',
          f'<b>5</b> · La red vacunada: <b>{pct(FGV["0.05"])}</b> con ε = 0.05',
          f'<b>6</b> · La mejor combinación: <b>{pct(BEST["val"])}</b> en el simulacro, <b>{pct(BUS["test_best"])}</b> en el examen'], 'nb05', 35, G1, '01',
         notes('Dinámica: 25 minutos en parejas (o salas de 3) y 10 de puesta en común. Sin nota.',
               'Prioridad si el tiempo aprieta: <b>1, 2 y 4</b>. Las secciones 3, 5 y 6 pueden quedar para casa. Activen la GPU en Colab (Entorno de ejecución → Cambiar tipo de entorno): los entrenamientos son cortos, pero la sección 5 entrena 5 épocas con el doble de fotos.',
               'No hay nada que programar: cada sección explica qué va a pasar, trae el código comentado y termina en <b>Para pensar</b> (respuesta plegada). Al final hay <b>ejercicios</b> que se responden leyendo los resultados.',
               'Problema frecuente: si sale <code>NameError</code>, se saltaron la celda de Configuración. Los números pueden variar un poco en otra máquina: lo importante es la forma de las curvas.'))

slide('cierre-tema1', 'Lo que te llevas del Tema 1', head('Lo que te llevas del Tema 1') + f"""
<div class="col" style="gap:1.1em">
  {st(1, '<div class="mapi big"><span>1 · Memorizar</span><b>si el entrenamiento mejora y el simulacro empeora, la red está memorizando</b></div>')}
  {st(2, '<div class="mapi big"><span>2 · Frenos</span><b>dropout, aumento de datos y parar a tiempo; y el mejor freno: más datos</b></div>')}
  {st(3, '<div class="mapi big"><span>3 · Robustez</span><b>4 píxeles, un ruido invisible o un mundo que cambia pueden tumbar a un modelo exacto</b></div>')}
  {st(4, '<div class="trendbar" style="margin-top:.6em">' + chip('Antes del Tema 2', 'trend') + '<span>Lee la lectura de tendencia <b>«¿Puedes explicar por qué tu modelo dijo «no»? Explicabilidad, robustez y la llegada de las reglas»</b> (5 páginas) y responde la encuesta en Canvas.</span></div>')}
  {st(4, '<p class="say" style="margin-top:.2em"><b>En el Tema 2:</b> ¿podemos aprovechar lo que otra red ya aprendió? ¿Y explicar por qué decide lo que decide?</p>')}
</div>""", notes(
    'Cierre del Tema 1, 5 minutos. Pide que alguien diga cada idea con sus palabras antes de mostrarla.',
    'La lectura de tendencia va antes del Tema 2: la explicabilidad, la robustez y las nuevas reglas (Ecuador, Brasil, la Unión Europea). No la expliques: que lleguen con una opinión.',
    'En el chat, del 1 al 5: <b>¿podrías explicarle a un colega cómo se ve el sobreajuste en las curvas?</b> Anota el promedio.',
    'Si aquí termina la sesión: <b>«Finalizar reunión para todos»</b> para que la grabación se cierre bien. Si queda tiempo, sigue directo con el Tema 2.'),
    block='01', group=G1, minutes=5)
