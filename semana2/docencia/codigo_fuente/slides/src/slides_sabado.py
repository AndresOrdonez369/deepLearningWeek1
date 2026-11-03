"""Semana 2 · sábado 7 de noviembre · 08:00-12:00 · bloques 02 (secuencias), 03 (atención) y 04 (elegir)."""
import json, pathlib
from kit import slide, head, key, chip, st, demo, count, qr, notes, eq, hist, code
from slides_viernes import section, practice, rail, RAIL_S, pct

SQ = json.loads((pathlib.Path(__file__).parent / 'data' / 'seq.json').read_text())
OR, MEM, ATW = SQ['orden']['res'], SQ['memoria'], SQ['atencion']
MEAN = sum(SQ['orden']['ejemplo']) / 12

G0 = 'Sábado · Encuadre'
G2 = 'Sábado · 02 Cómo lee una red una secuencia'
G3 = 'Sábado · 03 Atención y Transformers'
G4 = 'Sábado · 04 Elegir la arquitectura'
GC = 'Sábado · Cierre'

# ======================================================================= encuadre
slide('portada-sab2', 'Sábado: redes que leen en orden', f"""
<div class="cover">
  <div class="left">
    <h1 class="display" style="font-size:5.2em">Redes que leen en orden</h1>
    <p class="lede" style="font-size:1.45em">Secuencias, memoria y atención</p>
    <div class="tags after">{chip('UIDE · Maestría en Ciencia de Datos')}{chip('Semana 2 · Sábado')}</div>
    <p class="meta"><b>Andrés Ordóñez-Bolaños, MSc</b><br>Sábado 7 de noviembre · 08:00–12:00<br>Microsoft Teams</p>
  </div>
  <div class="right" style="padding:4em 4em 4em 0">{demo('rnnread', 'fig', mode='cover', alt='Una red recurrente lee una frase palabra por palabra')}</div>
</div>""", notes(
    'Bienvenida. Verifica la grabación y abre la vista del presentador (<b>P</b>).',
    'La animación: una red recurrente lee «el servicio no fue bueno» palabra por palabra y va actualizando su libreta. Al final decide: opinión negativa. Después lee «el servicio fue muy bueno» y decide lo contrario.',
    'Hoy: cómo lee una red una secuencia, por qué se olvida, cómo la atención mira directo y qué dice la lectura de tendencia sobre la mezcla de las dos.'),
    layout='L-cover', block='00', group=G0, minutes=1, blockname='Encuadre')

slide('agenda-sab2', 'El sábado en cuatro paradas', head('El sábado en cuatro paradas', 'Secuencias y la libreta, práctica, atención y la tendencia, y elegir la arquitectura de tu proyecto.') + f"""
<div class="col" style="gap:2em;margin-top:1em">
  {rail(RAIL_S)}
  <div class="legend"><span><i style="background:var(--amber)"></i>práctica en Colab</span><span><i style="background:var(--mint)"></i>quiz tipo Kahoot</span><span><i style="background:var(--lilac)"></i>lectura de tendencia</span></div>
</div>""", notes('Cuatro horas con pausa a las 09:30 y una actividad en salas sobre el proyecto de titulación. Hay unos 45 minutos de colchón: úsalos en la práctica si hace falta.'),
    block='00', group=G0, minutes=1)

slide('repaso-vie2', 'El viernes en tres ideas', head('El viernes en tres ideas', '¿Quién explica cada una con sus palabras, antes de que aparezca?') + f"""
<div class="col" style="gap:1.1em;margin-top:.4em">
  {st(1, '<div class="mapi big"><span>1 · La suposición</span><b>la densa supone que todo se relaciona con todo; la CNN, que lo cercano importa</b></div>')}
  {st(2, '<div class="mapi big"><span>2 · La lupa</span><b>un filtro de 3 × 3 recorre la foto: 9 píxeles por 9 pesos, sumados</b></div>')}
  {st(3, '<div class="mapi big"><span>3 · Compartir</span><b>el mismo filtro en toda la foto: 12 810 parámetros contra 101 770</b></div>')}
  {st(4, '<div class="keybar" style="margin-top:.6em"><span>La prueba: al mover la prenda 2 píxeles, la densa cayó a <b class="num">56.5 %</b> y la CNN aguantó <b class="num">75.2 %</b>. Hoy la pregunta cambia: <b>¿y si importa el orden?</b></span></div>')}
</div>""", notes('Cinco minutos. Pide voluntarios por el chat para cada idea antes de mostrarla.',
                 'Si alguien no hizo el NB03 completo, recuérdale las secciones 0, 2, 3 y 5 para casa.'),
    block='00', group=G0, minutes=5)

# ======================================================================= 02 · secuencias
section('b02', '02', 'Cómo lee una red una secuencia', 'En una frase, en un historial de pagos o en una canción, el orden cambia el significado.',
        ['Datos en orden', 'El orden importa', 'La libreta', 'La cuenta', 'Desenrollar', 'El olvido', 'LSTM', 'En Keras', 'Práctica NB04'], 'Sábado · 35 minutos y 40 de práctica', G2, '02 · Cómo lee una red una secuencia',
        notes('Aquí está la <b>idea clave 4</b>: qué guarda una RNN y por qué se olvida.'))

SEQS = [('Texto', ['el', 'socio', 'pagó', 'la', 'cuota'], '(5, 1)', 'palabra tras palabra'),
        ('Historial de pagos', ['3', '5', '3', '12', '7', '…', '24'], '(12, 1)', 'días de atraso de cada mes'),
        ('Ventas de una agencia', ['lun', 'mar', 'mié', 'jue', 'vie'], '(365, 1)', 'un número por día'),
        ('Voz', ['0.01', '−0.2', '0.4', '…'], '(16 000, 1)', '16 000 números por segundo de audio'),
        ('Sensores', ['temp', 'presión', '…'], '(1 440, 2)', 'cada minuto, 2 datos: pasos × datos por paso'),
        ('Video', ['foto 1', 'foto 2', 'foto 3', '…'], '(30, 28, 28)', '30 fotos por segundo, en orden')]
slide('secuencias', 'Datos que llegan en orden', head('Datos que llegan en orden', 'Una <b>secuencia</b> es una tabla en la que el orden de las filas importa. Su forma: <b>(pasos, datos por paso)</b>.') +
      '<div class="seqs">' + ''.join(st(i // 2 + 1, f'<div class="sq"><h3>{t}</h3><div class="tok">{"".join(f"<i>{w}</i>" for w in ws)}</div><span class="shape">{sh}</span><p>{d}</p></div>') for i, (t, ws, sh, d) in enumerate(SEQS)) + '</div>',
      notes('Seis ejemplos cotidianos. Lo común: si cambias el orden, cambia el significado. La forma que recibe Keras es (pasos, datos por paso); con muchos ejemplos, (ejemplos, pasos, datos por paso).',
            'El historial de pagos es el ejemplo del NB04: 12 meses, 1 número por mes (días de atraso). Forma: (12, 1).',
            '<span class="q">Pregunta:</span> «¿Qué secuencias hay en sus trabajos?» (ventas diarias, transacciones, lecturas de sensores, textos de reclamos…).'),
      block='02', group=G2, minutes=2)

slide('orden', 'El orden importa', head('El orden importa', 'Dos socios con <b>exactamente los mismos 12 números</b>, en orden contrario. Uno empeora; el otro mejora. Su promedio es idéntico.', key(1)) +
      demo('orden', 'fill') +
      st(4, f'<div class="split even" style="gap:1.4em;flex:none;margin-top:.4em"><div class="warnbar"><span>Un modelo que solo mira el <b>promedio</b> de los meses ({OR["promedio"]["params"]} parámetros): <b class="num">{pct(OR["promedio"]["test"])}</b>. Lo mismo que lanzar una moneda.</span></div>'
            f'<div class="keybar"><span>Una <b>RNN</b> que lee mes por mes ({OR["rnn"]["params"]} parámetros): <b class="num">{pct(OR["rnn"]["test"], 0)}</b>.</span></div></div>'),
      notes('<b>Idea clave 1, ahora en el tiempo.</b> Paso 1: el socio A, un historial real del NB04 (sección 2): los atrasos suben mes a mes. Paso 2: el socio B tiene los mismos 12 números al revés: mejora.',
            f'Paso 3: el promedio es el mismo ({MEAN:.1f} días). Cualquier modelo que solo mire el promedio, o que ignore el orden, no puede distinguirlos.',
            f'Paso 4: resultados reales con 2 000 socios. El modelo del promedio: {pct(OR["promedio"]["test"])} (adivina). La RNN: 100 %. Lo mismo pasa con «el perro mordió al niño» y «el niño mordió al perro»: mismas palabras, otra noticia.',
            '<span class="q">Pregunta:</span> «¿Qué socio le preocupa más a la cooperativa?» (el A: va empeorando, aunque su promedio sea igual).'),
      block='02', group=G2, minutes=4)

slide('libreta', 'La RNN lee de a uno y anota en su libreta', head('Una RNN lee de a uno y anota en su libreta', 'La misma celda recibe la palabra de ahora <b>y lo que ya tenía anotado</b>. La libreta (el <b>estado oculto h</b>) es pequeña y de tamaño fijo.', key(4)) +
      demo('rnnread', 'fill'),
      notes('<b>Idea clave 4 (parte 1).</b> Pulsa «Leer la siguiente palabra» una por vez. La celda es <b>la misma</b> en cada paso (los mismos pesos), como la CNN usaba el mismo filtro en toda la foto: ahora se comparte en el tiempo.',
            'La libreta tiene 3 casillas con nombres para explicarla (<b>ilustrativo</b>: en una red real son números sin nombre, y suelen ser 8, 32 o 128). Con «no», la casilla «¿hubo un no?» se enciende; con «bueno» al final, la opinión queda negativa.',
            'Cambia a «el servicio fue muy bueno»: la libreta termina positiva. Mismo «bueno», distinto contexto: la libreta lo lleva.',
            'Analogía de la lectura: <b>una RNN lee un libro con una libreta pequeña en la que va resumiendo lo que lleva leído</b>.',
            '<span class="q">Pregunta:</span> «¿Qué ventaja tiene una libreta de tamaño fijo?» (leer cada palabra nueva cuesta siempre lo mismo, no importa cuán largo sea el texto).'),
      block='02', group=G2, minutes=4)

ROWS = [('1', '1', '0', 'tanh(1·1 + 0.5·0)', '0.76'), ('2', '0', '0.76', 'tanh(1·0 + 0.5·0.76)', '0.36'),
        ('3', '0', '0.36', 'tanh(0.5·0.36)', '0.18'), ('4', '0', '0.18', 'tanh(0.5·0.18)', '0.09')]
slide('rnn-cuenta', 'La cuenta de la libreta', head('La cuenta de la libreta, con números', 'Es una neurona de la semana 1 con una entrada extra: su propia libreta del paso anterior.', key(4)) + f"""
<div class="split" style="grid-template-columns:6fr 6fr;gap:2.4em">
  <div class="col" style="gap:1.2em">
    """ + eq([('h_t', 'la libreta nueva', 'out'), ('=', '', 'op'), (r'\tanh(', '', 'op'), (r'w\,x_t', 'lo que llega ahora', 'x'), ('+', '', 'op'), (r'u\,h_{t-1}', 'lo que ya tenía', 'w'), ('+', '', 'op'), ('b)', '', 'op')],
             read='mezcla la palabra de ahora con lo anotado y aplasta el resultado entre −1 y 1. <b>w</b>, <b>u</b> y <b>b</b> se aprenden y son <b>los mismos en todos los pasos</b>.', size='.82em') + """
    <p class="say">Ejemplo del NB04: <b>w = 1, u = 0.5, b = 0</b> y una secuencia que solo trae algo en el primer paso: <span class="num">x = [1, 0, 0, 0]</span>.</p>
  </div>
  <div class="col" style="gap:.6em">
    <div class="etab"><span class="h">paso</span><span class="h">x</span><span class="h">la cuenta</span><span class="h">h</span>""" +
    ''.join(st(i + 1, f'<span class="num">{a}</span><span class="num">{b}</span><span class="num">{d}</span><span class="v">{e}</span>', cls='row3') for i, (a, b, c, d, e) in enumerate(ROWS)) + """</div>
    """ + st(4, '<div class="keybar" style="margin-top:.8em"><span>Cada paso, la huella del primer dato <b>se reduce a la mitad</b>. Diez pasos después queda <b class="num">0.001</b>.</span></div>') + """
  </div>
</div>""", notes(
    '<b>Idea clave 4 (parte 2): la cuenta.</b> Es la neurona de la semana 1 (pesos, suma y activación) con una entrada extra: h del paso anterior. <code>tanh</code> es como la sigmoide pero entre −1 y 1.',
    'Paso 1: h₁ = tanh(1) = 0.76. Paso 2: no llega nada nuevo (x = 0) y queda la mitad de lo anotado: tanh(0.38) = 0.36. Pasos 3 y 4: 0.18 y 0.09.',
    'Es la sección 1 del NB04. Con u = 0.5, a los 10 pasos queda 0.001: la libreta ya casi no recuerda el primer dato. Con u = 0.9 dura más (0.19), pero también se apaga.',
    '<span class="q">Pregunta:</span> «¿Qué pasaría con u = 0?» (la libreta no recuerda nada: solo ve la palabra de ahora).'),
    block='02', group=G2, minutes=4)

slide('desenrollar', 'Desenrollar: la misma celda en cada paso', head('Desenrollar: la misma celda en cada paso', 'Leer una frase de 6 palabras es como pasar por una red de 6 capas que <b>comparten los mismos pesos</b>. Al entrenar, la culpa viaja hacia atrás por todos los pasos.') +
      demo('unroll', 'fill'),
      notes('Paso 1: dibujamos la RNN «desenrollada»: una copia de la celda por palabra. Las 6 copias usan los mismos w, u y b (las etiquetas verdes): compartir pesos en el tiempo.',
            'Paso 2: el error se mide al final. Para corregir w y u, la culpa viaja hacia atrás paso a paso (retropropagación en el tiempo) y en cada paso se multiplica por un número menor que 1. A la primera palabra llega 0.03.',
            'Es el «teléfono dañado» de la semana 1, ahora en el tiempo: si el dato importante está muy atrás, casi no llega señal para aprender esa relación.',
            '<span class="q">Pregunta:</span> «Si la frase tiene 80 palabras, ¿cuánto llega a la primera con un factor de 0.5?» (0.5⁷⁹: prácticamente nada).'),
      block='02', group=G2, minutes=3, steps=2)

slide('olvido', 'La libreta se olvida', head('La libreta se olvida', 'Cuánto queda del primer dato en la libreta, paso a paso. Mueve <b>u</b>: cuánto conserva la libreta de un paso al siguiente.', key(4)) +
      demo('eco', 'fill') +
      st(2, '<div class="warnbar" style="margin-top:.6em"><span><b>El doble problema:</b> la huella del pasado se apaga al leer, y la culpa se apaga al entrenar. Por eso una RNN simple <b>no aprende relaciones lejanas</b>.</span></div>'),
      notes('<b>Idea clave 4 (parte 3).</b> Las barras son la huella del primer dato en la libreta: la cuenta de la lámina anterior, extendida a 20 pasos. Con u = 0.5, a los 10 pasos queda 0.001.',
            'Paso 2: la lámina mueve u a 0.9: dura más (0.19 a los 10 pasos), pero se sigue apagando. Prueben ustedes con el deslizador. Con u cerca de 1 se apaga despacio, pero la libreta se satura y pierde la capacidad de anotar cosas nuevas.',
            'La lectura lo dice así: «al entrenar con secuencias largas, la señal de error que viaja hacia atrás se debilita en cada paso y la red no aprende relaciones lejanas».',
            '<span class="q">Pregunta:</span> «¿Qué le pasaría a un modelo que lee contratos de 50 páginas con esta libreta?»'),
      block='02', group=G2, minutes=4, steps=2)

slide('lstm', 'LSTM: una libreta con compuertas', head('LSTM: una libreta con tres compuertas', 'La LSTM añade una <b>cinta de memoria</b> que pasa de un paso al siguiente casi sin cambios, y tres <b>válvulas</b> que la red aprende a abrir y cerrar.') +
      demo('lstm', 'fill') +
      '<div class="row" style="gap:1.4em;margin-top:.4em">' + hist('1997', 'Hochreiter y Schmidhuber inventan la LSTM') +
      st(4, '<span class="say">Si «olvidar» queda casi abierta (≈ 1), el dato viaja muchos pasos <b>sin apagarse</b>. Fue la reina de las secuencias durante dos décadas: traducción, voz, series de tiempo.</span>') + '</div>',
      notes('Paso 1, <b>olvidar</b> (el borrador): decide qué parte de la cinta se borra. Paso 2, <b>guardar</b> (el lápiz): decide qué de lo nuevo se anota. Paso 3, <b>mostrar</b> (la ventana): decide qué parte de la cinta sale como h para la palabra siguiente y para la predicción.',
            'Cada válvula es una sigmoide de la semana 1: 0 cierra, 1 abre. La red aprende cuándo abrir cada una a partir de la palabra de ahora y de lo que mostró el paso anterior.',
            'Por qué ayuda: en la cinta, el dato no pasa por una tanh en cada paso; si la válvula de olvidar está cerca de 1, la huella (y la culpa al entrenar) viaja lejos.',
            'Lectura: «La LSTM (Hochreiter y Schmidhuber, 1997) mitigó el problema con compuertas que deciden qué guardar, qué olvidar y qué mostrar». En 2025 volvió como xLSTM 7B.',
            '<span class="q">Pregunta:</span> «¿Qué válvula cerrarían al terminar una frase y empezar otra?» (olvidar: borrar lo anterior).'),
      block='02', group=G2, minutes=4, steps=4)

RNNCODE = code("""
model = keras.Sequential([
    keras.Input(shape=(12, 1)),   # 12 months
    layers.SimpleRNN(8),          # notebook: 8 numbers
    layers.Dense(1, activation="sigmoid"),
])
# with gates: layers.LSTM(32)
""", hl='1:2;2:3;3:4;4:6', cls='sm')
slide('rnn-keras', 'Las secuencias en Keras', head('Las secuencias en Keras', 'Los mismos 4 pasos de siempre. Lo nuevo: la forma <b>(pasos, datos por paso)</b> y una capa que lee en orden.') + f"""
<div class="split" style="grid-template-columns:6fr 5fr;gap:2em;align-items:start">
  {RNNCODE}
  <div class="col" style="gap:.9em">
    {st(1, '<div class="mapi stack" style="font-size:1.12em"><span>Input(shape=(12, 1))</span><b>12 meses, 1 dato por mes · X.shape → (2000, 12, 1)</b></div>')}
    {st(2, '<div class="mapi stack" style="font-size:1.12em"><span>SimpleRNN(8)</span><b>lee los 12 meses en orden; entrega su libreta final</b></div>')}
    {st(3, '<div class="mapi stack" style="font-size:1.12em"><span>Dense(1, sigmoid)</span><b>con esa libreta decide: ¿empeora?</b></div>')}
    {st(4, '<div class="mapi stack" style="font-size:1.12em"><span>LSTM(32)</span><b>se cambia una línea: cinta y válvulas</b></div>')}
    {st(4, f'<p class="say">Esta red tiene <b class="num">{OR["rnn"]["params"]}</b> parámetros y acierta el <b class="num">100 %</b> del orden de los socios.</p>')}
  </div>
</div>""", notes(
    'El código de la sección 2 del NB04. <code>Input(shape=(12, 1))</code>: 12 pasos y 1 dato por paso. Keras recibe arrays de forma (ejemplos, pasos, datos por paso): (2000, 12, 1).',
    '<code>SimpleRNN(8)</code>: una libreta de 8 números. Parámetros: 8 × 1 (w) + 8 × 8 (u) + 8 (b) = 80, más la salida: 8 + 1 = 9. Total 89.',
    'Para usar LSTM basta cambiar la capa. Con 32 unidades tiene 4 × (32 × 32 + 32 × 2 + 32) = 4 480 parámetros en el examen de memoria (4 513 con la salida): 4 veces más que una SimpleRNN del mismo tamaño, por sus tres válvulas.',
    '<span class="q">Pregunta:</span> «Si quisieran usar 3 datos por mes (atraso, monto, saldo), ¿qué cambia en el código?» (<code>shape=(12, 3)</code>).'),
    block='02', group=G2, minutes=3)

M80 = MEM['80']
practice('practica-nb04', 'Práctica en clase: NB04', 'En parejas. Todo el código ya viene escrito. Antes de cada celda, apuesta qué va a salir: en la sección 3 casi todos se equivocan.',
         ['<b>1</b> · La libreta a mano: <b>0.76 · 0.36 · 0.18 · 0.09</b>', f'<b>2</b> · El orden importa: promedio <b>{pct(OR["promedio"]["test"])}</b>, RNN <b>100 %</b>',
          f'<b>3</b> · Examen de memoria con 80 pasos: SimpleRNN <b>{pct(M80["rnn"]["test"])}</b>, LSTM <b>{pct(M80["lstm"]["test"])}</b>',
          f'<b>4</b> · La atención: <b>100 %</b> con solo <b>{M80["atencion"]["params"]}</b> parámetros', '<b>5</b> · A mano: «él» mira a «socio» el <b>79 %</b>'], 'nb04', 40, G2, '02',
         notes('Dinámica: 30 minutos en parejas y 10 de puesta en común. Sin nota.',
               'Prioridad: <b>1, 2, 3 y 4</b>. La sección 5 (atención a mano) la vemos juntos después de la pausa. Todo el notebook corre en 1 a 2 minutos.',
               'En la sección 3 pide que apuesten antes de ejecutar: casi todos esperan que la LSTM gane con 80 pasos. Con este presupuesto (10 épocas), las dos recurrentes adivinan. Es la mejor sorpresa del día.',
               'Experimento 4 (opcional): con 50 pasos, la LSTM aprende con una semilla y no con otra. Lección: una sola corrida no prueba nada.'))

slide('examen-memoria', 'El examen de memoria: lo que vimos', head('El examen de memoria: lo que vimos en el NB04', 'Cada secuencia trae una <b>marca</b> en uno de los 10 primeros pasos; la respuesta es el valor marcado. Después vienen muchos pasos de distracción. Mismo presupuesto para todos: 10 épocas.') +
      demo('memtest', 'fill') +
      st(3, f'<div class="keybar" style="margin-top:.4em"><span>Con 80 pasos, las recurrentes <b>adivinan</b> ({pct(M80["rnn"]["test"], 0)} y {pct(M80["lstm"]["test"], 0)}). La atención acierta el <b>100 %</b> con {M80["atencion"]["params"]} parámetros: no carga el dato en la libreta, <b>va a buscarlo</b>.</span></div>'),
      notes('Puesta en común de la sección 3 y 4 del NB04, con los números reales. Paso 1: 10 pasos: las tres aprenden. Paso 2: 30 pasos: las tres aprenden; la LSTM llega al 99 % en la época 3, la SimpleRNN en la 6.',
            f'Paso 3: 80 pasos: SimpleRNN {pct(M80["rnn"]["test"])} y LSTM {pct(M80["lstm"]["test"])} (lanzar una moneda). La atención: 100 % desde la época 4, con 82 parámetros y en menos de 3 segundos.',
            'Honestidad: la LSTM sí recuerda más que la SimpleRNN en muchos problemas reales (texto, voz) y con más entrenamiento. Con 50 pasos depende de la semilla (Experimento 4). Lo robusto es la lección: <b>cuanto más lejos el dato, más le cuesta a la libreta</b>.',
            '<span class="q">Pregunta:</span> «¿Por qué a la atención no le importa la distancia?» Respuesta: lo vemos en el bloque 03.'),
      block='02', group=G2, minutes=5, steps=3)

# ======================================================================= 03 · atención
section('b03', '03', 'Atención y Transformers', '¿Y si en vez de cargar todo en una libreta, cada palabra pudiera mirar directamente a las demás?',
        ['En fila', 'Cada palabra mira a todas', 'Consulta, clave y valor', 'Lo que miró la red', 'El precio', 'El Transformer', 'Los híbridos', 'El contrapeso'], 'Sábado · 40 minutos', G3, '03 · Atención y Transformers',
        notes('Aquí está la <b>idea clave 5</b> y la lectura de tendencia de la semana.'))

slide('en-fila', 'La RNN lee en fila', head('La RNN lee en fila: no se puede paralelizar', 'Para leer la palabra 100 necesita haber leído las 99 anteriores. La atención procesa todas a la vez.') +
      demo('serial', 'fill'),
      notes('El segundo problema de la RNN, de la lectura: «la RNN no se puede paralelizar. Para procesar la palabra cien necesita haber procesado las noventa y nueve anteriores. Las GPU, que son excelentes haciendo miles de operaciones al mismo tiempo, quedan subutilizadas».',
            'Arriba, la RNN: una palabra por paso, 8 pasos. Abajo, la atención: todas las palabras se comparan con todas en un solo paso (64 comparaciones).',
            'Por eso el Transformer permitió entrenar con cantidades de datos antes impensables: todo se calcula en paralelo.',
            '<span class="q">Pregunta:</span> «¿Qué pasa con el tiempo de entrenamiento de una RNN si los textos son 10 veces más largos?» (10 veces más pasos en fila).'),
      block='03', group=G3, minutes=2)

slide('atencion', 'Cada palabra mira a todas', head('La atención: cada palabra mira a todas las demás', 'Y decide cuáles son importantes para entenderla. En la frase de la lectura, «él» mira a «socio», no a «cuota».', key(5)) +
      demo('attn', 'fill'),
      notes('<b>Idea clave 5 (parte 1).</b> La frase viene de la lectura: «el socio pagó la cuota porque él recibió su sueldo». ¿A quién se refiere «él»? Una persona lo sabe sin pensar; la RNN tendría que haberlo cargado en su libreta.',
            'Los arcos son los pesos de atención (<b>ilustrativos</b>, para explicar): «él» pone el 62 % en «socio». Paso 1: «su» también mira a «socio». Paso 2: «sueldo» mira a «recibió». Haz clic en «pagó» o «cuota».',
            'Lo nuevo: no hay libreta que se llene. Cada palabra puede consultar cualquier parte del texto con precisión, sin importar la distancia.',
            '<span class="q">Pregunta:</span> «En “la cuota que el socio pagó ayer estaba vencida”, ¿a qué palabra mira “vencida”?»'),
      block='03', group=G3, minutes=4, steps=2)

TBL = ('<table class="wtab" style="font-size:1.15em"><thead><tr><th>palabra</th><th>clave</th><th>valor</th><th data-step="2">puntaje</th><th data-step="3">peso</th></tr></thead><tbody>'
       '<tr><td><b>socio</b></td><td class="num">[2, 0]</td><td class="num">[1, 0]</td><td class="num" data-step="2">3.0</td><td class="num am" data-step="3"><b>79 %</b></td></tr>'
       '<tr><td><b>cuota</b></td><td class="num">[0, 2]</td><td class="num">[0, 1]</td><td class="num" data-step="2">0.0</td><td class="num" data-step="3">4 %</td></tr>'
       '<tr><td><b>él</b></td><td class="num">[1, 0]</td><td class="num">[0.5, 0.5]</td><td class="num" data-step="2">1.5</td><td class="num" data-step="3">17.5 %</td></tr>'
       '</tbody></table>')
slide('atencion-cuenta', 'Consulta, claves y valores', head('Cómo decide a quién mirar: consulta, claves y valores', 'Como en una biblioteca: la <b>consulta</b> es lo que buscas, las <b>claves</b> son las fichas del catálogo y los <b>valores</b> son los libros que te llevas.', key(5)) + f"""
<div class="split" style="grid-template-columns:6fr 6fr;gap:2.4em;align-items:start">
  <div class="col" style="gap:1em">
    {st(1, '<p class="say">Vectores de 2 números: <b>[qué tan persona, qué tan dinero]</b>. La consulta de «él» es <b class="num">[1.5, 0]</b>: busca una persona.</p>')}
    {TBL}
    {st(4, '<div class="keybar"><span>El nuevo «él» = 0.79·[1, 0] + 0.04·[0, 1] + 0.175·[0.5, 0.5] ≈ <b class="num">[0.87, 0.13]</b>: casi pura persona.</span></div>')}
  </div>
  <div class="col" style="gap:1.2em">
    """ + st(2, eq([(r'\text{puntaje}', 'qué tanto coincide', 'out'), ('=', '', 'op'), (r'\text{consulta}\cdot\text{clave}', 'el producto punto de la semana 1', 'x')], size='.82em')) + """
    """ + st(3, eq([(r'\alpha', 'pesos que suman 1', 'out'), ('=', '', 'op'), (r'\text{softmax}(\text{puntajes})', 'el softmax del viernes', 'x')], size='.82em')) + """
    """ + st(4, eq([(r'\text{nuevo}', 'lo que entiende ahora', 'out'), ('=', '', 'op'), (r'\textstyle\sum \alpha\cdot\text{valor}', 'promedio ponderado', 'x')], size='.82em')) + """
  </div>
</div>""", notes(
    '<b>Idea clave 5 (parte 2).</b> Es la sección 5 del NB04, con los mismos números. Los vectores los escribimos a mano para entender; en un Transformer real se <b>aprenden</b>.',
    'Paso 2: puntaje = consulta · clave. Socio: 1.5 × 2 + 0 × 0 = 3.0. Cuota: 0. Él: 1.5. Paso 3: softmax (el de las 10 prendas del viernes): 79 %, 4 % y 17.5 %.',
    'Paso 4: el nuevo significado de «él» es el promedio de los valores ponderado por esos pesos: [0.87, 0.13]. La atención resolvió a quién se refiere.',
    'Con n palabras, todas miran a todas: n × n puntajes. Aquí 3 × 3 = 9; en un texto de mil palabras, un millón. Ese es el precio (dos láminas más).',
    '<span class="q">Pregunta:</span> «Si la consulta fuera [0, 1.5], ¿a quién miraría?» (a «cuota»: buscaría dinero).'),
    block='03', group=G3, minutes=4)

slide('atencion-real', 'Lo que miró la red del NB04', head('Lo que miró la red del NB04', 'La red de atención del examen de memoria, con 80 pasos. Nadie le dijo dónde mirar: aprendió a poner casi todo su peso en el paso marcado.') +
      demo('attnw', 'fill') +
      st(2, '<p class="say" style="margin-top:.4em">Por eso la distancia no le importa: no carga el dato 80 pasos en una libreta, <b>lo va a buscar</b>. Es el «buscador preciso» de la lectura.</p>'),
      notes(f'Pesos reales de la sección 4 del NB04 para una secuencia del examen. Paso 1: el {ATW["pesos"][ATW["marca"]] * 100:.1f} % del peso cae en un solo paso, el marcado (el segundo). Paso 2: los otros 79 pasos se reparten el resto.',
            'La red es la atención más simple posible: a cada paso le da un puntaje, softmax los vuelve pesos que suman 1 y hace un promedio ponderado. 82 parámetros.',
            '<span class="q">Pregunta:</span> «¿Qué tendría que hacer una RNN para acertar aquí?» (guardar el valor marcado en su libreta y protegerlo durante 80 pasos).'),
      block='03', group=G3, minutes=3, steps=2)

slide('costo', 'El precio: comparar con todas', head('El precio: comparar con todas', 'Para generar cada palabra nueva, el Transformer la compara con <b>todas</b> las anteriores y guarda una nota de cada una (la <b>caché KV</b>). El costo crece con el cuadrado de la longitud.', key(5)) +
      demo('cost', 'fill'),
      notes('<b>Idea clave 5 (parte 3): el precio.</b> A la izquierda, cada cuadrito es una comparación: con 8 palabras, 64; con 16, 256. El doble de palabras, cuatro veces más cuentas. Mueve el deslizador.',
            'Pasos 1 a 4, a la derecha: los tamaños reales de hoy. Un millón de palabras (tokens) son un billón de comparaciones. Los agentes de IA trabajan horas sobre la misma tarea: el costo de releerlo todo se volvió el cuello de botella (lectura).',
            'La libreta de la RNN, en cambio, cuesta lo mismo por palabra, sin importar cuán largo sea el texto. Analogía de la lectura: el Transformer, antes de escribir cada palabra, <b>relee la carta completa</b>; la RNN solo mira su libreta.',
            '<span class="q">Pregunta:</span> «Si la atención es tan buena, ¿por qué no usarla siempre?» (por el costo con textos largos: eso abre la tendencia).'),
      block='03', group=G3, minutes=3, steps=4)

TF_SVG = """
<svg viewBox="0 0 1000 620" role="img" aria-label="Un bloque Transformer: atención y una capa densa, repetidos muchas veces">
 <g data-step="1"><rect x="90" y="470" width="820" height="90" rx="20" fill="#0f1a29" stroke="#2d394a" stroke-width="3"/>
  <text x="500" y="525" text-anchor="middle" font-size="30" fill="#b6c6d7" font-family="Lexend, sans-serif">las palabras, cada una como un vector</text></g>
 <g data-step="2"><rect x="90" y="320" width="820" height="110" rx="20" fill="#ffb541" fill-opacity=".14" stroke="#ffb541" stroke-width="4"/>
  <text x="500" y="368" text-anchor="middle" font-size="34" font-weight="700" fill="#ffb541" font-family="Lexend, sans-serif">Atención</text>
  <text x="500" y="408" text-anchor="middle" font-size="25" fill="#f1f6fa" font-family="Lexend, sans-serif">cada palabra mira a todas</text></g>
 <g data-step="3"><rect x="90" y="170" width="820" height="110" rx="20" fill="#4abaf4" fill-opacity=".14" stroke="#4abaf4" stroke-width="4"/>
  <text x="500" y="218" text-anchor="middle" font-size="34" font-weight="700" fill="#4abaf4" font-family="Lexend, sans-serif">Capa densa</text>
  <text x="500" y="258" text-anchor="middle" font-size="25" fill="#f1f6fa" font-family="Lexend, sans-serif">la de la semana 1, palabra por palabra</text></g>
 <g data-step="4"><path d="M940 450 C990 400 990 200 940 150" stroke="#c2a7f4" stroke-width="5" fill="none"/><polygon points="928,160 944,140 952,166" fill="#c2a7f4"/>
  <text x="500" y="110" text-anchor="middle" font-size="30" font-weight="700" fill="#c2a7f4" font-family="Lexend, sans-serif">× N bloques apilados (12, 32, 96…)</text>
  <text x="500" y="60" text-anchor="middle" font-size="26" fill="#b6c6d7" font-family="Lexend, sans-serif">al final: la siguiente palabra</text></g>
</svg>"""
slide('transformer', 'El Transformer: atención apilada', head('El Transformer: atención apilada', 'En 2017, un equipo de Google propuso abandonar la recurrencia por completo. Su idea central: la atención.') + f"""
<div class="split" style="grid-template-columns:6fr 5fr;gap:2.4em">
  <div class="fig">{TF_SVG}</div>
  <div class="col" style="gap:1.1em">
    {hist('2017', 'Vaswani et al. · «Attention is all you need»')}
    {st(5, '<div class="mapi stack"><span>Ventaja 1</span><b>no hay libreta que se llene: puede consultar cualquier parte del texto con precisión</b></div>')}
    {st(5, '<div class="mapi stack"><span>Ventaja 2</span><b>todo se calcula en paralelo: se pudo entrenar con cantidades de datos antes impensables</b></div>')}
    {st(5, '<p class="say">De ahí salieron <b>BERT</b>, <b>GPT</b> y prácticamente todos los modelos de lenguaje actuales.</p>')}
  </div>
</div>""", notes(
    'Pasos 1 a 4: un Transformer es una pila de bloques iguales. Cada bloque: atención (cada palabra mira a todas) y una capa densa (la de la semana 1) aplicada a cada palabra. Se repite N veces.',
    'Detalle para curiosos (en el NB04): los puntajes se dividen entre la raíz del tamaño de los vectores y hay varias «cabezas» de atención en paralelo, cada una buscando relaciones distintas.',
    'Paso 5, las dos ventajas que cita la lectura. Si hoy le preguntas cualquier cosa a un chatbot, la respuesta la produce casi con seguridad un Transformer.',
    '<span class="q">Pregunta:</span> «¿Qué parte del Transformer ya conocían de la semana 1?» (la capa densa, la softmax, el producto punto).'),
    block='03', group=G3, minutes=3, steps=5)

HYB = [('2024', 'Jamba', 'AI21 Labs', 'Una capa de atención por cada siete de Mamba'),
       ('2025', 'Nemotron-H', 'NVIDIA', 'Cambia ~92 % de las capas de atención por Mamba-2: hasta 3 veces más rápido'),
       ('2025', 'Kimi Linear', 'Moonshot AI', 'Hasta 75 % menos memoria de caché y 6 veces más rápido con un millón de tokens'),
       ('2026', 'Qwen3.5', 'Alibaba', 'Tres capas de atención «lineal» por cada capa de atención completa'),
       ('2026', 'Nemotron 3 Super', 'NVIDIA', 'Híbrido Mamba–atención: hasta 2.2 veces más rendimiento')]
STK = [('Transformer', 'todas las capas son de atención', 8), ('Jamba (2024)', '1 de cada 8 capas es de atención', 1), ('Qwen3.5 (2026)', '1 de cada 4 es atención completa', 2)]
slide('hibridos', 'Las recurrentes vuelven, mezcladas', head('Tendencia: las recurrentes vuelven, mezcladas', 'Libretas modernas que se entrenan en paralelo (<b>Mamba</b>, 2023; <b>xLSTM 7B</b>, 2025). La tendencia más fuerte no fue reemplazar al Transformer, sino <b>mezclarlo</b>.', chip('Lectura de tendencia', 'trend')) +
      '<div class="tl5" style="margin-top:.2em">' + ''.join(st(1, f'<div class="ev"><span class="y num">{y}</span><i></i><span class="m">{m} <span class="mu" style="font-weight:400">· {w}</span></span><span class="d">{d}</span></div>') for y, m, w, d in HYB) + '</div>' +
      '<div class="split" style="grid-template-columns:7fr 4fr;gap:2em;margin-top:1em;align-items:end;flex:none">' +
      st(2, '<div class="stacks">' + ''.join(
          f'<div class="stk">{"".join("<i class=a></i>" if (j % (8 // max(1, a)) == 0 if a < 8 else True) else "<i></i>" for j in range(8))}<h3>{t}</h3><p>{d}</p></div>' for t, d, a in STK) + '</div>') +
      st(3, '<div class="analog"><span class="t">Como un buen estudiante preparando un examen</span><p>Apuntes resumidos de casi todo (capas recurrentes, azul) y, de vez en cuando, vuelve al libro por un dato exacto (atención, ámbar).</p></div>') + '</div>',
      notes('<b>La lectura de tendencia de la semana.</b> Paso 1: la línea de tiempo, con las cifras tal como las reporta la lectura (son reportes de los propios laboratorios).',
            'Paso 2: las pilas. Ámbar = capa de atención completa («un buscador preciso dentro del texto»); azul = capa recurrente barata. Jamba: 1 de cada 8. Qwen3.5: 3 de atención lineal por cada una completa.',
            'Paso 3: la analogía de la lectura. Conecta con el NB04: la recurrente resume, la atención busca el dato exacto (el 90 % del peso en el paso marcado).',
            'Mamba (Gu y Dao, 2023) es un «state space model»: una libreta que decide mejor qué anotar y se entrena en paralelo. Mamba-2 mostró que estos modelos y la atención son primos matemáticos (Dao y Gu, 2024).',
            '<span class="q">Pregunta:</span> «¿Por qué conservar unas pocas capas de atención y no ninguna?»'),
      block='03', group=G3, minutes=4, steps=3)

WARN = [('La libreta tiene un límite', 'Un Transformer pequeño puede copiar textos muy largos de forma exacta; un modelo con estado de tamaño fijo está limitado por lo que cabe en ese estado. Si te dictan un teléfono largo y solo anotas un resumen, pierdes dígitos.', 'Jelassi et al., 2024'),
        ('Los benchmarks pueden engañar', 'MiniMax volvió a la atención completa en su modelo M2: su híbrido igualaba en las pruebas tradicionales, pero a mayor escala mostró «claros déficits» en razonamiento complejo de varios pasos.', 'MiniMax, 2025'),
        ('No hay consenso', 'A comienzos de 2026 conviven Transformers clásicos, atención comprimida o dispersa y diversos híbridos: «ya nadie se pone de acuerdo sobre la atención».', 'Labonne, 2026')]
slide('contrapeso', 'Lo que la libreta no puede guardar', head('El contrapeso: lo que la libreta no puede guardar', 'Que algo sea más barato no significa que sea igual de bueno.', chip('Lectura de tendencia', 'trend')) +
      '<div class="warn3">' + ''.join(st(i + 1, f'<div class="wcard"><h3>{t}</h3><p>{d}</p><span class="src">{s}</span></div>') for i, (t, d, s) in enumerate(WARN)) + '</div>' +
      st(4, '<div class="trendbar" style="margin-top:1.3em">' + chip('Debate en el chat', 'trend') + '<span><b>¿Vale la pena ganar de 2 a 6 veces en velocidad si se arriesga la capacidad de recordar con exactitud y razonar en varios pasos?</b> Para un hospital o una cooperativa con pocas GPU, ¿qué elegirían?</span></div>'),
      notes('Tres advertencias de la lectura. 1: Jelassi, Brandfonbrener, Kakade y Malach (2024): los Transformers fueron claramente mejores para copiar y recuperar información precisa del contexto. Es lo que vimos en el NB04 con el paso marcado.',
            '2: MiniMax (2025), una publicación inusualmente honesta: verificar alternativas en tareas difíciles exige un cómputo que «crece astronómicamente».',
            '3: Labonne (2026): no hay ganador. Es la misma lección que Smith et al. (2023) con CNN y ViT: comparar con justicia y en las tareas que importan.',
            'Paso 4: abre el debate en el chat 3 minutos. La lectura lo conecta con América Latina: usar modelos todos los días en hardware que una organización de la región sí puede pagar, por ejemplo para leer expedientes o contratos en español.'),
      block='03', group=G3, minutes=4)

# ======================================================================= 04 · elegir
section('b04', '04', 'Elegir la arquitectura', 'No gana la arquitectura de moda: gana la que hace la suposición correcta sobre tus datos, y se comprueba con una comparación justa.',
        ['El mapa', 'Tres preguntas', 'Tu proyecto'], 'Sábado · 30 minutos con la actividad', G4, '04 · Elegir la arquitectura',
        notes('Cierra la semana aplicando todo al proyecto de titulación.'))

ZOO = [('Tabla', 'Densa (MLP)', 'Todo se relaciona con todo.', 'Socios de una cooperativa, ventas por cliente.', 'az'),
       ('Imagen', 'CNN · o ViT', 'Lo cercano importa; el patrón puede estar en cualquier parte.', 'Rayos X, cultivos fotografiados con dron.', 'am'),
       ('Secuencia corta', 'RNN · LSTM', 'El orden importa; basta un resumen.', 'Pagos de cada mes, lecturas de sensores.', 'mi'),
       ('Texto largo', 'Transformer · o híbrido', 'Cada palabra puede necesitar a cualquier otra.', 'Contratos, expedientes, chatbots.', 'am'),
       ('Grafo', 'GNN', 'Importan las conexiones entre elementos.', 'Transferencias entre cuentas, moléculas, redes de socios.', 'li'),
       ('Crear datos', 'GAN · difusión', 'Aprender a generar ejemplos nuevos que parezcan reales.', 'Imágenes sintéticas, datos para entrenar.', 'co')]
slide('zoologico', 'Cada dato con su arquitectura', head('Cada dato con su arquitectura', 'Cada una es una suposición distinta. Las lecturas del sílabo amplían las tres últimas: Transformers, GNN y GAN.') +
      '<div class="zoo">' + ''.join(st(i // 2 + 1, f'<div class="zc {k}"><span class="d">{d}</span><h3>{a}</h3><span class="s">{s}</span><span class="e">{e}</span></div>') for i, (d, a, s, e, k) in enumerate(ZOO)) + '</div>' +
      st(4, '<p class="say" style="margin-top:1em">Y se mezclan: una CNN puede leer cada foto de un video y una RNN el orden de las fotos; los híbridos mezclan libreta y atención.</p>'),
      notes('El mapa de la semana, ampliado con lo que viene en las lecturas del sílabo. Paso 1: tabla y imagen (lo del viernes). Paso 2: secuencia y texto largo (hoy). Paso 3: grafos y generación.',
            '<b>GNN</b> (redes neuronales de grafos): cuando los datos son nodos y conexiones, por ejemplo cuentas que se transfieren dinero (detección de fraude) o átomos de una molécula. Suponen que un nodo se parece a sus vecinos.',
            '<b>GAN</b> (Goodfellow et al., 2014): dos redes compiten, una genera y otra juzga si es real. Hoy los modelos de difusión dominan la generación de imágenes.',
            '<span class="q">Pregunta:</span> «¿Qué arquitectura usarían para detectar fraude en una red de transferencias?» (GNN, o una tabla de características con una densa como línea base).'),
      block='04', group=G4, minutes=4)

Q3 = [('1', '¿Qué estructura tienen mis datos?', 'Tabla, imagen, secuencia, texto largo o grafo. La forma <code>.shape</code> ya da una pista.'),
      ('2', '¿Qué cuesta?', 'Datos para entrenar, parámetros, tiempo de entrenamiento y memoria al usarlo todos los días.'),
      ('3', '¿Cómo lo compruebo?', 'Contra una línea base simple y con una comparación justa: mismos datos, mismo presupuesto, varias semillas.')]
slide('elegir', 'Tres preguntas antes de elegir', head('Tres preguntas antes de elegir', 'La habilidad más valiosa no es conocer la arquitectura de moda, sino saber qué suposición hace cada una, qué cuesta y cómo comprobar si es la adecuada.') +
      '<ol class="steps-list" style="gap:1.2em;margin-top:.4em">' + ''.join(st(i + 1, f'<span class="k key">{n}</span><span><b>{t}</b><br>{d}</span>', 'li') for i, (n, t, d) in enumerate(Q3)) + '</ol>' +
      st(4, '<div class="keybar" style="margin-top:1.3em"><span><b>Empieza simple.</b> Si una densa ya resuelve tu tabla, no necesitas un Transformer. En el NB04, una sola corrida de la LSTM con 50 pasos ganaba o perdía según la semilla.</span></div>'),
      notes('La frase del encabezado cierra la lectura de tendencia. Las tres preguntas son la receta para el proyecto.',
            'Pregunta 3 conecta con la semana 1 (el entregable «¿Le creerías a tu red?»): línea base, comparación justa y varias semillas. Y con Smith et al. (2023): con el mismo presupuesto, las CNN empataron con los ViT.',
            '<span class="q">Pregunta:</span> «¿Cuál es la línea base más simple para su proyecto?»'),
      block='04', group=G4, minutes=3)

ACT = [('1 · Sus datos', '¿Qué forma tienen? Escriban su <code>.shape</code>: (ejemplos, …).'),
       ('2 · La suposición', '¿Qué arquitectura hace la suposición correcta, y por qué?'),
       ('3 · La línea base', '¿Contra qué modelo simple la van a comparar?'),
       ('4 · La comparación justa', '¿Qué dejarían igual para que la comparación sea justa?')]
slide('tu-proyecto', 'La arquitectura de tu proyecto', head('Actividad: la arquitectura de tu proyecto', 'En salas, con tu grupo de titulación. Al final, cada grupo pega <b>4 líneas</b> en el chat, una por pregunta.', chip('15 minutos en salas', 'ok') + chip('5 de puesta en común', 'hint')) +
      '<div class="act4">' + ''.join(st(i + 1, f'<div class="case"><span class="chip">{a}</span><p>{b}</p></div>') for i, (a, b) in enumerate(ACT)) + '</div>' +
      st(4, '<p class="say" style="margin-top:1em">Ejemplo: «(5 000, 12, 3): 12 meses de pagos con 3 datos por mes → LSTM, porque importa la tendencia; línea base: una densa con el promedio; justo: mismos meses de prueba y 3 semillas».</p>'),
      notes('Abre salas de 3 o 4 personas (los grupos de titulación). 15 minutos.',
            'Pasa por las salas: la pregunta más difícil suele ser la 1 (la forma de sus datos). Si un grupo tiene imágenes, la respuesta es una CNN; si tiene texto largo, un Transformer ya entrenado (transfer learning, semana 3).',
            'Puesta en común: lee dos o tres respuestas del chat y corrige con cariño las suposiciones que no encajan con los datos.',
            'Esto alimenta la entrega de la semana aplicada al proyecto.'),
      block='04', group=G4, minutes=20)

# ======================================================================= cierre
slide('quizfinal2', 'Quiz final: ¿cuánto avanzamos?', head('Quiz final: ¿cuánto avanzamos?', '10 preguntas tipo Kahoot. Vuelven las 5 ideas clave del pre-quiz: así vemos tu avance.', chip('No es nota', 'ok')) + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:1em">
  <ol class="steps-list" style="gap:1.2em">
    <li><span class="k">1</span><span>Abre <b>deeplearningweek1.vercel.app/?final2</b></span></li>
    <li><span class="k">2</span><span>Usa <b>el mismo nombre</b> que en el pre-quiz del viernes</span></li>
    <li><span class="k">3</span><span>Pega tu código en el chat de Teams</span></li>
  </ol>
  <div class="center">{qr('final2')}</div>
</div>""", notes(
    'Ocho minutos. El mismo nombre que en el pre-quiz: el panel de resultados de la semana 2 los empareja por nombre.',
    'Después de clase, copia el chat en <b>Resultados_quiz.html</b> de la semana 2 y verás el avance en cada idea clave.'),
    block='C', group=GC, minutes=8, label='Cierre')

WM = [('Viernes', 'Una foto es una tabla de 784 números', ''), ('Idea 1', 'cada arquitectura es una suposición', 'am'), ('Idea 2', 'la lupa: un filtro de 3 × 3 recorre la foto', 'am'), ('Idea 3', 'compartir el filtro: 8 veces menos parámetros', 'am'),
      ('Sábado', 'en una secuencia el orden importa', ''), ('Idea 4', 'la libreta resume… y se olvida', 'mi'), ('LSTM', 'una cinta con tres válvulas', 'mi'), ('Idea 5', 'la atención mira a todas, a un precio n²', 'am'),
      ('Tendencia', 'híbridos: apuntes y libro', 'li'), ('Contrapeso', 'la libreta no lo guarda todo', 'li'), ('Elegir', 'suposición, costo y comparación justa', 'az'), ('Semana 3', 'robustez, transfer learning y explicabilidad', 'az')]
slide('mapa-semana2', 'La semana en un mapa', head('La semana en un mapa', 'Todo lo de la semana, en el orden en que lo vimos. Borde amarillo: las 5 ideas clave.') +
      '<div class="wmap">' + ''.join(st(i // 4 + 1, f'<div class="wm {k}"><span>{a}</span><b>{b}</b></div>') for i, (a, b, k) in enumerate(WM)) + '</div>',
      notes('Recorre el camino en voz alta, fila por fila. Si alguien quiere repasar, la guía de estudio de la semana 2 tiene una sección por bloque.'),
      block='C', group=GC, minutes=2, label='Cierre')

NEXT = [('Robustez', 'Al mover la prenda 4 píxeles, las dos redes se cayeron. ¿Cómo se entrena una red que aguante? Aumento de datos y regularización.'),
        ('Transfer learning', 'Usar una CNN o un Transformer ya entrenado con millones de ejemplos y ajustarlo a tus pocos datos.'),
        ('Explicabilidad', '¿Qué miró la red para decidir? Ya vimos los mapas de los filtros y los pesos de atención: es el comienzo.')]
slide('lo-que-viene2', 'Lo que viene: semana 3', head('Lo que viene: semana 3', 'Robustez, transfer learning, optimización y explicabilidad.', chip('Semana 3', 'trend')) +
      '<div class="cases" style="margin-top:.4em">' + ''.join(st(i + 1, f'<div class="case"><span class="chip">{a}</span><p>{b}</p></div>') for i, (a, b) in enumerate(NEXT)) + '</div>',
      notes('Deja tres preguntas sembradas, todas con algo que ya vieron: el desplazamiento de 4 píxeles (robustez), entrenar desde cero (transfer learning) y los mapas y pesos de atención (explicabilidad).',
            '<span class="q">Pregunta para cerrar:</span> «Si su proyecto tiene pocos datos, ¿entrenarían una CNN desde cero o partirían de una ya entrenada?»'),
      block='C', group=GC, minutes=2, label='Cierre')

slide('recursos2', 'Para repasar y gracias', head('Para repasar, y gracias') + f"""
<div class="split" style="grid-template-columns:7fr 4fr;gap:2.4em;align-items:start">
  <div class="col" style="gap:.9em">
    <div class="mapi"><span>Guía de estudio</span><b>los 4 bloques con ejemplos, figuras y ejercicios resueltos</b></div>
    <div class="mapi"><span>Slides</span><b>estas mismas, interactivas: mueve los deslizadores en casa</b></div>
    <div class="mapi"><span>NB03 y NB04</span><b>CNN y secuencias: todo escrito, para leer y experimentar</b></div>
    <div class="mapi"><span>Lectura</span><b>«¿El regreso de las redes recurrentes?» y su encuesta en Canvas</b></div>
    <p class="display" style="font-size:3em;margin-top:.6em">Gracias</p>
  </div>
  <div class="center">{qr('guia2')}</div>
</div>""", notes('Todo está en la página de la semana 2 (el código QR abre la guía de estudio). Al terminar, <b>«Finalizar reunión para todos»</b>.'),
    block='C', group=GC, minutes=1, label='Cierre')
