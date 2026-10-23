"""Saturday 24 · 08:00-12:00 · blocks 05-09 and closing."""
from kit import slide, head, key, chip, st, demo, count, qr, notes, eq, hist, code, move
from slides_viernes import section, practice, rail, RAIL_S

GS = 'Sábado · Encuadre'
G5 = 'Sábado · 05 De una neurona a una red'
G6 = 'Sábado · 06 Retropropagación'
G7 = 'Sábado · 07 Entrenar bien'
G8 = 'Sábado · 08 Keras'
G9 = 'Sábado · 09 ¿El modelo es bueno?'
GC = 'Sábado · Cierre'

slide('portada-sab', 'Sábado: de una neurona a una red', f"""
<div class="cover">
  <div class="left">
    <h1 class="display">Muchas neuronas, una&nbsp;red</h1>
    <p class="lede" style="font-size:1.45em">Hoy vencemos a XOR, repartimos la culpa y entrenamos con Keras.</p>
    <div class="tags after">{chip('Semana 1 · Sábado 24')}{chip('08:00–12:00')}</div>
  </div>
  <div class="right">{demo('net', layers='3,5,5,5,2', w=860, h=1000, gap=150, padx=120, seed=4, alt='Red neuronal de varias capas con señales')}</div>
</div>""", notes('Verifica la grabación. Comparte la ventana del deck y abre la vista del presentador (P).',
                 'Hoy tiene cuatro horas, con una pausa a las 09:40. La práctica grande es el NB02, en clase y sin nota.'),
      layout='L-cover', block='S', group=GS, minutes=1, label='Sábado')

slide('agenda-sab', 'El sábado en nueve paradas', head('El sábado en nueve paradas', 'De la red a Keras, con una práctica larga en Colab y el quiz final para cerrar.') +
      st(1, rail(RAIL_S)) +
      st(2, '<div class="legend" style="margin-top:2em"><span><i style="background:var(--amber)"></i>práctica en Colab</span><span><i style="background:var(--mint)"></i>quiz tipo Kahoot</span><span><i style="background:var(--lilac)"></i>conexión con la lectura de tendencia</span><span><i style="background:var(--line)"></i>pausa</span></div>'),
      notes('Muestra el recorrido y la hora de la pausa (09:40). La práctica del NB02 es en parejas, a las 10:45.'),
      block='S', group=GS, minutes=1, label='Sábado')

REP = [('Una neurona', 'suma con pesos y sesgo, y traza una línea', 'M10 70 L110 10'),
       ('La activación', 'dobla la línea y da probabilidades', 'M10 70 C50 70 60 10 110 10'),
       ('El perceptrón', 'aprende de sus errores… pero no puede con XOR', 'M20 20 L100 60 M20 60 L100 20'),
       ('El descenso de gradiente', 'baja la montaña paso a paso', 'M10 15 Q60 110 110 15')]
slide('repaso', 'El viernes en cuatro ideas', head('El viernes en cuatro ideas', '¿Quién explica cada una con sus palabras?') +
      '<div class="quad">' + ''.join(st(i + 1, f'<div class="panel qd"><svg viewBox="0 0 120 80" aria-hidden="true"><path d="{p}"/></svg><div><b>{a}</b><span>{b}</span></div></div>') for i, (a, b, p) in enumerate(REP)) + '</div>' +
      st(5, '<div class="keybar" style="margin-top:1.2em"><span><b>Pregunta para el chat:</b> ¿qué problema nos quedó pendiente? Pista: la luz de la escalera.</span></div>'),
      notes('Diez minutos máximo. Pasa las cuatro tarjetas pidiendo a un estudiante distinto que explique cada una (no las leas tú).',
            'Respuesta esperada en el chat: XOR; una neurona solo traza una línea; necesitamos combinar varias. Eso es exactamente el bloque 05.'),
      block='S', group=GS, minutes=8, label='Sábado · Repaso')

# ======================================================================= 05 · redes
section('b05', '05', 'De una neurona a una red', 'Una neurona no puede con XOR: ¿qué hacemos?',
        ['Capas', 'XOR resuelto', 'Pistas cada vez más ricas', 'Juega a la red', 'Contar parámetros'], 'Sábado · 40 minutos', G5, '05 · De una neurona a una red',
        notes('Aquí volvemos a la <b>idea clave 3</b>: el límite de una línea y cómo lo superan las capas.'))

slide('red', 'Una red son neuronas en capas', f"""
<div class="split" style="grid-template-columns:5fr 7fr">
  <div class="col">
    {head('Una red son neuronas organizadas en capas')}
    <ul class="steps-list">
      {st(1, '<span class="k">1</span><span><b>Entrada:</b> los datos. No calcula nada.</span>', 'li')}
      {st(2, '<span class="k">2</span><span><b>Ocultas:</b> inventan sus propias pistas a partir de los datos.</span>', 'li')}
      {st(3, '<span class="k">3</span><span><b>Salida:</b> toma la decisión final.</span>', 'li')}
    </ul>
    {st(3, '<div class="panel"><p class="say">Como una cooperativa con agencias en <b>Riobamba, Latacunga y Ambato</b>: cada agencia resume lo que ve y el comité central decide con esos resúmenes.</p></div>')}
  </div>
  {demo('net', 'fig', layers='3,4,4,1', w=900, h=700, gap=130, names='Entrada|Oculta 1|Oculta 2|Salida', hl='0|1,2|3', alt='Red con capa de entrada, dos capas ocultas y una salida')}
</div>""", notes(
    'Una red no es más que muchas neuronas como la del viernes, organizadas en capas. Las ocultas se llaman así porque no vemos lo que producen: <b>nadie les dice qué pistas inventar</b>, las aprenden solas.',
    'Nombre técnico: perceptrón multicapa (MLP). Cuando hay muchas capas ocultas hablamos de deep learning, aprendizaje profundo.'),
    block='05', group=G5, minutes=3)

slide('xor-resuelto', 'Dos neuronas vencen a XOR', f"""
<div class="split" style="grid-template-columns:5fr 6fr">
  <div class="col">
    {head('Dos neuronas vencen a la luz de la escalera', 'Cada neurona oculta traza su línea. La salida combina las dos.', key(3))}
    <ul class="steps-list">
      {st(1, '<span class="k" style="background:var(--azure);color:var(--night)">1</span><span>Una aprende: <b>¿al menos un interruptor arriba?</b></span>', 'li')}
      {st(2, '<span class="k" style="background:var(--lilac);color:var(--night)">2</span><span>Otra aprende: <b>¿los dos arriba?</b></span>', 'li')}
      {st(3, '<span class="k key">=</span><span>Luz encendida si la primera dice sí y la segunda dice no: <b>la franja del medio</b>.</span>', 'li')}
    </ul>
  </div>
  {demo('xor2', 'fig plate', style='align-self:center;height:auto;aspect-ratio:760/640')}
</div>""", notes(
    '<b>Idea clave 3, resuelta.</b> La magia de la capa oculta. Una neurona aprende «¿al menos un interruptor arriba?» (OR); otra, «¿los dos arriba?» (AND). La salida enciende la luz si la primera dice sí y la segunda no.',
    'Dos líneas rectas, combinadas, hacen lo que una sola no podía. <b>Este es el principio de todo el deep learning</b>: combinar piezas simples para formar decisiones complejas.',
    'En el NB02, Parte E, Keras encuentra una solución así por sí solo.'),
    block='05', group=G5, minutes=3)

slide('pistas', 'Cada capa arma pistas más elaboradas', head('Cada capa arma pistas más elaboradas', 'Leer un 7 escrito a mano, como el monto de una papeleta de depósito.') + demo('digit', 'fill') +
      '<p class="cap">Esquema ilustrativo: en una red real las pistas no son tan limpias.</p>',
      notes('La primera capa detecta trazos sueltos (una línea horizontal, una diagonal). La siguiente combina trazos en formas (una esquina). La salida reconoce «es un 7».',
            'Nadie programó qué buscar: cada capa lo aprendió. Por eso se llama «profundo»: muchas capas, cada una más abstracta.',
            'Con datos de tabla pasa lo mismo, pero las pistas no se pueden dibujar: combinaciones como «cuota alta respecto al ingreso».'),
      layout='', block='05', group=G5, minutes=3, steps=3)

slide('juega', 'Juega: ¿cuántas neuronas necesita?', head('Juega: ¿cuántas neuronas necesita?', 'Una red pequeña que entrena aquí mismo. Elige los datos y el número de neuronas ocultas.') + demo('playground', 'fill'),
      notes('La demo estrella del sábado: una red real entrenando en el navegador (2 entradas → neuronas ocultas tanh → 1 salida sigmoide, con Adam).',
            'Sugerencia de recorrido: <b>Círculos con 1 neurona</b> → solo puede trazar una línea; se queda en ~60 %. Luego <b>4 neuronas</b> → arma un polígono y llega a ~100 %.',
            '<b>XOR con 2 neuronas</b>: lo resuelve, como en la lámina anterior. <b>Lunas con 8</b>: frontera curva.',
            '<span class="q">Pregunta:</span> «¿Por qué con 1 neurona nunca pasa del 60 % en los círculos?» Porque una neurona = una línea.',
            'Variante en grupos (10 min): que cada uno pruebe en <b>playground.tensorflow.org</b> y comparta en el chat la red más pequeña que resuelve la espiral.'),
      block='05', group=G5, minutes=12)

slide('parametros', '¿Cuántos números aprende una red?', head('¿Cuántos números aprende una red?', 'Como las perillas de una consola de sonido: un peso por cada cable y un sesgo por cada neurona. Entrenar es girarlas todas hasta que suene bien.') + f"""
<div class="split" style="grid-template-columns:6fr 6fr">
  {demo('net', 'fig', layers='3,4,1', w=760, h=560, gap=120, quiet='1', alt='Red tres, cuatro, uno')}
  <div class="col" style="gap:1.2em">
    {st(1, '<p class="big num">3 × 4 + 4 = <b class="am">16</b></p>')}
    {st(2, '<p class="big num">4 × 1 + 1 = <b class="am">5</b></p>')}
    {st(3, '<p class="bigread">' + count(21, 0, at=3) + ' <span class="mu" style="font-size:.4em;font-family:var(--sans)">números que aprender</span></p>')}
    {st(4, '<div class="panel col" style="gap:.4em"><p class="say">La red de las lunas del NB02: <b class="num">337</b></p><p class="say">Un modelo de lenguaje actual: <b>cientos de miles de millones</b></p></div>')}
    {st(5, '<div class="two-q"><div><b>Parámetros</b><span>pesos y sesgos: los ajusta el entrenamiento</span></div><div><b>Hiperparámetros</b><span>capas, neuronas y η: los eliges tú</span></div></div>')}
  </div>
</div>""", notes(
    'Contar parámetros ayuda a entender el tamaño de una red. Regla: entradas por neuronas (una conexión, un peso) más una por neurona (el sesgo). <b>La consola de sonido:</b> cada parámetro es una perilla; entrenar es girar todas las perillas a la vez hasta que la mezcla suene bien.',
    'Red 3-4-1: 3·4 + 4 = 16 en la oculta; 4·1 + 1 = 5 en la salida; total 21. Keras lo confirma con <code>model.summary()</code>.',
    'La red de las lunas del NB02 tiene 337. Más parámetros que datos es una receta para el sobreajuste: lo vemos en la semana 3.',
    'Paso 5. <b>Parámetros</b>: las perillas que el entrenamiento ajusta (pesos y sesgos). <b>Hiperparámetros</b>: las decisiones que tomamos nosotros antes de entrenar (cuántas capas, cuántas neuronas, qué η). <span class="q">Pregunta:</span> «¿16 neuronas significa 16 categorías?» No: son 16 cuentas intermedias; la salida sigue siendo sí o no.'),
    block='05', group=G5, minutes=3)

# ======================================================================= 06 · retropropagación
section('b06', '06', 'Retropropagación', 'Entre miles de perillas, ¿cuál movemos?',
        ['Hacia adelante', 'Repartir la culpa', 'Engranajes', 'Hacia atrás', 'Actualizar', 'TensorFlow'], 'Sábado · 45 minutos', G6, '06 · Retropropagación',
        notes('El corazón teórico del sábado. Una red 2-2-1 con números: los mismos del NB02, partes A a D.'))

slide('adelante', 'Paso 1 · Hacia adelante', head('Paso 1 · Hacia adelante: la red predice', 'Un socio con antigüedad 1.0 y carga de la cuota 0.5 (datos escalados). Cada neurona hace la cuenta del viernes.') +
      demo('fwd221', 'fill', mode='forward') +
      st(4, '<div class="keybar"><span>La red dice <b>56 % de que paga</b>. El socio sí pagó: pérdida = −log(0.56) = <b class="num">0.59</b>.</span></div>'),
      notes('El forward es lo que ya sabemos hacer, capa por capa. Oculta 1: 0.5·1.0 − 0.3·0.5 + 0.1 = 0.45 → sigmoide 0.61. Oculta 2: 0.2·1.0 + 0.8·0.5 − 0.1 = 0.50 → 0.62.',
            'Salida: 0.7·0.61 − 0.4·0.62 + 0.05 = 0.23 → 0.56. No hace falta que hagan las cuentas: lo importante es ver que la información fluye de izquierda a derecha.',
            'Todo está en el NB02, Parte A.'),
      block='06', group=G6, minutes=4, steps=4)

slide('culpa', 'Paso 2 · Repartir la culpa', head('Paso 2 · Hacia atrás: repartir la culpa', 'El error se descubre al final. La culpa viaja hacia atrás, según cuánto influyó cada paso.') + demo('chain', 'fill') +
      st(3, '<div class="row" style="gap:1.4em;align-items:center"><p class="say">Eso es la <b>retropropagación</b> (backpropagation). «Culpa» es una metáfora: lo que se calcula es una <b>derivada</b>.</p>' + hist('1986', 'Rumelhart, Hinton y Williams la popularizan') + '</div>'),
      notes('Analogía de la cadena del cacao, muy nuestra. El cliente prueba la barra de chocolate y está amarga: ese es el error, y se descubre al final.',
            '¿De quién es la culpa? La chocolatería revisa cuánto influyó cada proceso: si el tostado influyó mucho, recibe mucha culpa; y el tostado reparte su parte hacia el fermentado y la cosecha.',
            'Lo bonito: con <b>una sola pasada hacia atrás</b>, cada peso de la red sabe cuánta culpa tiene y hacia dónde moverse.',
            'Aclara la palabra: «culpa» es solo una ayuda para recordar. Lo que se calcula es una <b>derivada</b>, la sensibilidad de la pérdida a ese peso; no es una culpa moral ni un porcentaje de responsabilidad.'),
      block='06', group=G6, minutes=3, steps=3)

slide('engranajes', 'La regla de la cadena: engranajes', head('La regla de la cadena: engranajes que se multiplican', 'Si A mueve a B tres veces más rápido, y B mueve a C seis veces más rápido, A mueve a C 3 × 6 = 18 veces más rápido.') +
      '<div class="split" style="grid-template-columns:7fr 5fr;gap:2em">' + demo('gears', 'fig') +
      '<div class="col" style="gap:1.2em">' + eq([('18', 'A mueve a C', 'out'), ('=', '', 'op'), ('3', 'A mueve a B', 'x'), (r'\times', '', 'op'), ('6', 'B mueve a C', 'x')],
          read='en una red, la culpa de un peso es la culpa de la salida por lo que entró por su cable: −0.44 × 0.61 = −0.27. <b>Los efectos se multiplican a lo largo de la cadena.</b>', size='.9em') +
      hist('1676', 'Leibniz escribe la regla de la cadena') + '</div></div>',
      notes('La herramienta matemática detrás de repartir la culpa es la <b>regla de la cadena</b> del cálculo, y se entiende con engranajes.',
            'Para curiosos: z = (3x)². Por dentro u = 3x cambia 3 veces más rápido que x; por fuera z = u² cambia 2u = 6 veces más rápido que u (en x = 1). Total: 18, que coincide con la derivada 18x evaluada en 1.'),
      block='06', group=G6, minutes=3)

slide('atras', 'Hacia atrás, con los números', head('Hacia atrás, con los números', 'La misma red, pero ahora los números viajan de derecha a izquierda.') + demo('fwd221', 'fill', mode='backward') +
      st(3, '<p class="say">Ojo con la oculta 2: su peso hacia la salida es negativo, así que para que la salida suba, <b>ella debe bajar</b>. Cada «culpa» es una derivada.</p>'),
      notes('(1) La culpa de la salida es simplemente ŷ − y = 0.56 − 1 = <b>−0.44</b>: negativa significa que la predicción se quedó corta.',
            '(2) La culpa de cada peso que llega a la salida es esa culpa por lo que entró por ese cable: −0.44 × 0.61 = −0.27 y −0.44 × 0.62 = −0.28.',
            '(3) La culpa sigue hacia la capa oculta: se multiplica por el peso que la conecta y por la pendiente de la sigmoide (0.24): 0.7 × (−0.44) × 0.24 = −0.07 y −0.4 × (−0.44) × 0.24 = +0.04.',
            'Valores exactos con 4 decimales en el NB02, Parte B. En el notebook la culpa de la salida se llama delta (δ): solo es el nombre de ese resultado intermedio. Recuerda que «culpa» es una metáfora: cada número es una derivada.'),
      block='06', group=G6, minutes=5, steps=3)

slide('actualizar', 'Paso 3 · Actualizar', head('Paso 3 · Actualizar: un paso cuesta abajo', 'A cada peso le restamos η por su culpa. Es el descenso de gradiente del viernes.') + f"""
<div class="split" style="grid-template-columns:2fr 1fr;gap:2em">
  {demo('fwd221', 'fig', mode='update')}
  <div class="col" style="gap:1.1em">
    {st(1, eq([('0.7', 'peso viejo', 'w'), ('-', '', 'op'), (r'0.5\times(-0.27)', 'η × su culpa', 'x'), ('=', '', 'op'), ('0.84', 'peso nuevo', 'w')], size='.78em') + '<p class="say" style="margin-top:.6em">…y lo mismo con <b>los 9 números a la vez</b> (en verde).</p>')}
    {st(2, '<p class="big">Predicción: <b class="num">56 %</b> → <b class="num mi">65 %</b></p>')}
    {st(3, '<p class="big">Pérdida: <b class="num">0.59</b> → <b class="num mi">0.42</b></p>')}
    {st(3, '<div class="keybar"><span><b>Adelante, atrás, actualizar</b>, repetido miles de veces: eso es entrenar.</span></div>')}
  </div>
</div>""", notes(
    'Cerramos el ciclo. Ejemplo con el peso 0.7 que va de la oculta 1 a la salida: su culpa era −0.27; con η = 0.5, el peso nuevo es 0.7 + 0.135 = 0.84.',
    'Se hace lo mismo con los 9 parámetros a la vez. Con un solo paso, la predicción para el socio que pagó sube de 56 % a 65 % y la pérdida baja de 0.59 a 0.42.',
    'En el NB02, Parte C, el notebook además verifica la cuenta con un gradient check.'),
    block='06', group=G6, minutes=3)

CODE_TF = '''<pre class="code" data-demo="codehl" data-hl="1:1-3;2:4"><span class="ln"><span class="kw">with</span> tf.<span class="fn">GradientTape</span>() <span class="kw">as</span> tape:</span><span class="ln">    y_hat = <span class="fn">model</span>(x)            <span class="cm"># forward: the tape records it</span></span><span class="ln">    loss = <span class="fn">bce</span>(y, y_hat)</span><span class="ln">grads = tape.<span class="fn">gradient</span>(loss, model.trainable_variables)  <span class="cm"># backward</span></span></pre>'''
slide('tensorflow', 'TensorFlow hace la cuenta por ti', head('TensorFlow hace la cuenta por ti', '<b>TensorFlow</b> es la librería de Google (2015) que hace las cuentas de las redes. Calcula todas las culpas solo: se llama <b>diferenciación automática</b>.') + f"""
<div class="col" style="gap:1.4em">
  {CODE_TF}
  <div class="split even" style="gap:1.4em">
    {st(1, '<div class="panel"><p class="say"><b>Como una grabadora:</b> graba cada operación de la ida…</p></div>')}
    {st(2, '<div class="panel"><p class="say">…y la reproduce al revés aplicando la regla de la cadena.</p></div>')}
  </div>
  {st(3, '<div class="keybar"><span>Diferencia con nuestra cuenta a mano: <b class="num">5.6 × 10⁻¹⁷</b>, es decir, cero (errores de redondeo).</span></div>')}
</div>""", notes(
    'Primero, qué es: <b>TensorFlow</b> es una librería de Python que Google publicó en 2015 para hacer las cuentas de las redes neuronales, en CPU o en GPU. En el bloque 08 la vemos con calma junto a Keras.',
    'TensorFlow (y PyTorch) hacen la retropropagación automáticamente. <code>GradientTape</code> funciona como una grabadora: graba la ida y la reproduce al revés.',
    'En el NB02, Parte D, comparamos su resultado con nuestra cuenta de la Parte B: la diferencia es 5.6 × 10⁻¹⁷.',
    'Mensaje: entender la retropropagación no es para hacerla a mano, sino <b>para saber qué pasa cuando el entrenamiento falla</b>.'),
    block='06', group=G6, minutes=3)

# ======================================================================= 07 · entrenar bien
section('b07', '07', 'Entrenar bien', '¿Qué puede salir mal al entrenar?',
        ['La señal que se apaga', 'Neuronas clonadas', 'Lotes', 'La carrera', 'La receta'], 'Sábado · 35 minutos', G7, '07 · Entrenar bien',
        notes('Después de la pausa. Bloque práctico: lo que hace que un entrenamiento funcione o falle. Incluye la conexión con la lectura de tendencia.'))

slide('apaga', 'Trampa 1: la señal que se apaga', head('Trampa 1: la culpa que se apaga en el camino', 'Como el teléfono dañado: en cada capa, la sigmoide deja pasar como mucho ¼ del mensaje y al principio ya no llega nada.') + demo('vanish', 'fill') +
      '<div class="row" style="justify-content:flex-end;margin-top:.6em">' + hist('2010', 'ReLU se vuelve la activación estándar (Nair y Hinton)') + '</div>',
      notes('Es el gradiente que se desvanece. La pendiente máxima de la sigmoide es 0.25; tras cinco capas, la culpa llega multiplicada por 0.25⁵ ≈ 0.001: la primera capa casi no aprende. Como el teléfono dañado.',
            'Cambia a <b>ReLU</b>: su pendiente es 1 cuando está activa, la culpa llega entera. Por eso en las capas ocultas usamos ReLU.',
            'También ayuda <b>escalar los datos</b>: estandarizar es restar el promedio y dividir por la desviación. Un ingreso de 1200 con promedio 1000 y desviación 200 queda (1200 − 1000) / 200 = <b>1</b>: «una desviación sobre el promedio».'),
      block='07', group=G7, minutes=3)

slide('clones', 'Trampa 2: neuronas clonadas', head('Trampa 2: si todas empiezan igual, aprenden lo mismo', 'Como cuatro estudiantes que copian la misma tarea: cuatro cuadernos, una sola idea. Con todos los pesos en cero, las neuronas quedan clonadas.') + demo('clones', 'fill') +
      '<div class="row" style="justify-content:flex-end;margin-top:.6em">' + hist('2010', 'Glorot y Bengio: cómo sortear bien los pesos iniciales') + '</div>',
      notes('Si todos los pesos empiezan en cero (o iguales), todas las neuronas ocultas calculan lo mismo, reciben la misma culpa y se actualizan igual: cuatro neuronas que piensan una sola idea.',
            'La solución: pesos al azar, bien escalados según el tamaño de la capa. Keras ya lo hace por defecto (inicialización Glorot); para ReLU se usa He.',
            'Trampa 3 la conocen del viernes: un learning rate demasiado grande.'),
      block='07', group=G7, minutes=3, steps=1)

slide('lotes', 'Aprender por lotes', head('Aprender por lotes: encuesta, no censo', 'Con 4 800 socios no calculamos la culpa de todos en cada paso. Tomamos 32 al azar, damos un paso y seguimos.') + demo('batches', 'fill'),
      notes('Un lote (mini-batch) de 32 socios al azar → culpa promedio → un paso. Cuando pasamos por todos los lotes (4 800 / 32 = 150) completamos una época.',
            'Analogía: el INEC no hace un censo cada mes para medir el empleo; hace una encuesta por muestreo, más barata y suficientemente precisa.',
            'El pequeño «ruido» de usar una muestra incluso ayuda a no quedarse atascado. En Keras: <code>batch_size=32</code>.'),
      block='07', group=G7, minutes=3, steps=1)

slide('carrera', 'La carrera de los optimizadores', head('La carrera de los optimizadores', 'Mismo valle largo y angosto, tres formas de caminar. ¿Quién llega primero a la meta?', chip('Lectura de tendencia', 'trend')) + demo('race', 'fill') +
      '<div class="trendbar" style="margin-top:.8em"><span><b style="color:var(--ink-3)">SGD</b>: pasos fijos. <b style="color:var(--ink)">Momentum</b> (1964): una bola que rueda y gana impulso. <b>Adam</b> (2014): zapatos a la medida de cada terreno. ¿Y con una carrera <b>justa</b>?</span></div>',
      notes('<b>Conexión con la lectura «Más allá de Adam».</b> El valle es largo en una dirección y angosto en la otra, como los que aparecen al entrenar redes.',
            'SGD (blanco) zigzaguea entre las paredes y avanza lento. Momentum (azul) acumula velocidad y aquí llega primero. Adam (lila) va más derecho, pero con los pasos que le dimos tarda un poco más.',
            '<b>Ese resultado es parte de la lección:</b> si cambian el learning rate de cada uno, el ganador cambia. Comparar optimizadores sin ajustarlos con el mismo cuidado es una carrera injusta.',
            '<b>Debate de 8 minutos en el chat:</b> la lectura cuenta que, con un ajuste justo para todos, la ventaja de los optimizadores nuevos baja de ~1.4× a ~1.1× en modelos grandes (Wen et al., 2025). ¿Conviene invertir en mejores algoritmos o en más cómputo y mejores datos? No hay respuesta correcta: es la misma pregunta de la encuesta.',
            'Ojo: esta carrera es una ilustración; los números de pasos dependen de cómo se ajuste cada optimizador. Esa es justamente la lección de la lectura.'),
      block='07', group=G7, minutes=10)

REC2 = [('Escala los datos', 'que todas las columnas estén en rangos parecidos'), ('ReLU en las capas ocultas', 'la culpa llega entera'),
        ('Sigmoide en la salida', 'si la respuesta es sí o no'), ('Adam con learning_rate = 0.001', 'un buen punto de partida'),
        ('Pérdida binary_crossentropy', 'la BCE del viernes'), ('Lotes de 32 y una parte para validar', 'para medir con datos que no vio')]
slide('receta-arranque', 'La receta para arrancar', head('La receta para arrancar (y que funcione)', 'Un punto de partida para casi cualquier problema con datos de tabla. Tómale foto.') +
      '<ol class="steps-list fill" style="display:grid;grid-template-columns:1fr 1fr;gap:1.6em 3em;align-content:center;font-size:1.12em">' + ''.join(
          st(i + 1 if i < 3 else 4, f'<span class="k">{i + 1}</span><span><b>{a}</b><br>{b}</span>', 'li') for i, (a, b) in enumerate(REC2)) + '</ol>',
      notes('Esta receta sirve como punto de partida para casi cualquier problema con datos de tabla. No es la única ni siempre la mejor, pero rara vez falla.',
            'El paso 1 es el más olvidado: si una columna va de 0 a 10 000 (ingreso) y otra de 0 a 5 (atrasos), la red se confunde. Ojo: el escalador se ajusta solo con los datos de entrenamiento.',
            'Ejemplo de estandarizar: promedio 1000, desviación 200. Un ingreso de 1200 queda (1200 − 1000) / 200 = <b>1</b>; uno de 800 queda −1. Así todas las columnas hablan en la misma escala.'),
      block='07', group=G7, minutes=3)

# ======================================================================= 08 · keras
section('b08', '08', 'Keras', '¿Hay que hacer todo esto a mano?',
        ['Motor y volante', 'Los datos', 'Construir', 'Compilar', 'Aprender no es memorizar', 'Entrenar', 'Predecir', 'Práctica NB02'], 'Sábado · 24 minutos y 40 de práctica', G8, '08 · Keras',
        notes('Keras desde cero: qué es, cómo se importa, cómo entran los datos y cada línea del código. Después, la práctica más larga de la semana.'))

# ---- the motor and the steering wheel
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

print(tf.__version__, keras.__version__)
""", hl='1:2-3;2:1;3:2-3;4:5', out='2.x  3.x')
slide('tf-keras', 'TensorFlow y Keras: el motor y el volante', head('TensorFlow y Keras: el motor y el volante', 'Dos librerías de Python que ya vienen en Colab. Con Keras manejas; TensorFlow hace las cuentas por debajo.') + f"""
<div class="split" style="grid-template-columns:6fr 6fr;gap:2.4em">
  {STACK}
  <div class="col" style="gap:1em">
    {IMPORTS}
    <div class="analog"><span class="t">Puedes manejar sin abrir el capó</span><p>Keras te deja armar y entrenar una red en diez líneas. Saber que existe el motor ayuda cuando algo falla: por eso hicimos las cuentas a mano.</p></div>
    {hist('2015', 'nacen Keras (François Chollet, marzo) y TensorFlow (Google, noviembre)')}
  </div>
</div>""", notes(
    '<b>No asumamos nada:</b> TensorFlow y Keras son librerías de Python, es decir, código que otros escribieron y que importamos para no reinventarlo.',
    '<b>TensorFlow</b> (Google, 2015) es el motor: guarda los números en «tensores», calcula las culpas solo (la retropropagación de esta mañana) y puede usar la GPU. <b>Keras</b> (François Chollet, 2015; hoy Keras 3) es el volante: capas listas, <code>compile</code> y <code>fit</code>.',
    'Las tres líneas de <code>import</code> son las primeras de la Parte T del NB02. <code>tf</code> es solo un apodo; <code>from keras import layers</code> nos deja escribir <code>layers.Dense</code>.',
    'Para curiosos: Keras 3 puede usar como motor a TensorFlow, a JAX o a PyTorch. En Colab usa TensorFlow por defecto.'),
    block='08', group=G8, minutes=3)

# ---- data as arrays
slide('datos-arrays', 'Los datos entran como una tabla', head('Los datos entran como una tabla de números', 'Como una hoja de cálculo: cada fila es un ejemplo y cada columna un dato. En Python se llama <b>array</b>; su <code>shape</code> dice filas × columnas.') +
      code("""
X_m, y_m = make_moons(600, noise=0.2, random_state=SEED)  # 600 rows, 2 columns
""", cls='sm') + demo('moons', 'fill', mode='arrays', style='margin-top:1em'),
      notes('Antes de construir la red, cómo le entregamos los datos. Keras recibe arrays de NumPy: <code>X</code> es la tabla de entradas y <code>y</code> la respuesta de cada fila (0 o 1).',
            'La tabla de la derecha son las primeras filas reales del NB02; el anillo blanco muestra dónde cae cada fila en el plano. Haz clic en una fila para ubicarla.',
            '<code>X.shape → (480, 2)</code>: 480 ejemplos de entrenamiento, 2 datos cada uno. <code>y.shape → (480,)</code>: una respuesta por fila. Si las formas no cuadran, Keras se queja: es el error más común al empezar.'),
      block='08', group=G8, minutes=2)

# ---- build
BUILD = code("""
model = keras.Sequential([
    keras.Input(shape=(2,)),                # 2 inputs
    layers.Dense(16, activation="relu"),    # 48
    layers.Dense(16, activation="relu"),    # 272
    layers.Dense(1, activation="sigmoid"),  # 17
])
model.summary()                             # 337
""", hl='1:1;2:2;3:3;4:4;5:5;6:8', cls='sm')
BUILD_SAY = [(1, 'Sequential', 'una pila de capas: los datos pasan en orden'),
             (2, 'Input(shape=(2,))', 'la puerta: cada ejemplo trae 2 números'),
             (3, 'Dense(16, activation="relu")', '16 neuronas conectadas con todo; ReLU, la válvula'),
             (5, 'Dense(1, activation="sigmoid")', 'la salida: una probabilidad')]
slide('keras-construir', 'Construir: apilar capas como LEGO', head('Construir: apilar capas como LEGO', 'Cada <code>Dense</code> es una capa de neuronas como las del viernes. <code>Sequential</code> las apila en orden, como piezas de LEGO.') + f"""
<div class="split" style="grid-template-columns:7fr 5fr;gap:2em">
  <div class="col" style="gap:.8em">
    {BUILD}
    <div class="col" style="gap:.35em">""" + ''.join(st(n, f'<p class="cl"><code>{c}</code> {d}</p>') for n, c, d in BUILD_SAY) + """</div>
    """ + st(6, '<div class="keybar"><span><code>model.summary()</code> cuenta las perillas: <b class="num">48 + 272 + 17 = 337</b>.</span></div>') + f"""
  </div>
  {demo('net', 'fig', layers='2,16,16,1', w=760, h=700, r=12, gap=36, padx=90, names='Entrada|Oculta 1|Oculta 2|Salida', hl='0,1,2,3|0|1|2|3|0,1,2,3', quiet='1', alt='Red de dos entradas, dos capas ocultas de 16 neuronas y una salida')}
</div>""", notes(
    'Avanza línea por línea: cada clic ilumina una línea del código y la capa que crea en el dibujo.',
    '<code>Sequential</code>: la red más simple, una capa detrás de otra. <code>Input(shape=(2,))</code>: le decimos cuántos números trae cada ejemplo. <code>Dense(16, activation="relu")</code>: 16 neuronas del viernes, cada una con su peso por cable y su sesgo, y ReLU para doblar la línea.',
    'La salida tiene <b>una</b> neurona con sigmoide porque la respuesta es sí o no: nos da una probabilidad.',
    '<code>model.summary()</code> imprime una tabla con los parámetros de cada capa: 2×16 + 16 = 48; 16×16 + 16 = 272; 16×1 + 1 = 17. Total 337, como contamos en el bloque 05.'),
    block='08', group=G8, minutes=4)

# ---- compile
COMPILE = code("""
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
""", hl='1:2;2:3;3:4')
CMP = [('optimizer', 'cómo da los pasos', 'Adam, el de la carrera, con <code>learning_rate</code> = η = 0.01: el largo del paso del viernes.'),
       ('loss', 'qué tan mal va', 'la BCE del viernes: castiga la falsa seguridad, como al meteorólogo.'),
       ('metrics', 'qué te reporta', 'la exactitud. Solo informa, no se usa para aprender. Ojo con el 87 % del bloque 09.')]
slide('keras-compile', 'Compilar: las reglas del entrenamiento', head('Compilar: las reglas del entrenamiento', '<code>compile</code> todavía no entrena. Decide cómo se corrige, qué se mide y qué te reporta, como planear el estudio antes de empezar.') + f"""
<div class="col" style="gap:1.4em">
  {COMPILE}
  <div class="cases">""" + ''.join(st(i + 1, f'<div class="case"><span class="chip">{a} · {b}</span><p>{c}</p></div>') for i, (a, b, c) in enumerate(CMP)) + """</div>
</div>""", notes(
    '<code>compile</code> es la lista de reglas antes de entrenar. Tres decisiones, y las tres ya las conocen:',
    '<b>optimizer</b>: cómo bajar la montaña. Adam (la carrera del bloque 07) con un paso de 0.01. El valor por defecto de Adam es 0.001; en el NB02 usamos 0.01 para que aprenda rápido.',
    '<b>loss</b>: qué tan mal vamos. Para sí/no, la entropía cruzada binaria (el meteorólogo del viernes). <b>metrics</b>: lo que queremos ver en la pantalla; no cambia el entrenamiento.'),
    block='08', group=G8, minutes=3)

# ---- fit: watch it learn
FIT = code("""
history = model.fit(X_train, y_train, epochs=60, batch_size=32, validation_split=0.2)
""", cls='sm')
slide('keras-fit', 'Entrenar: fit', head('Entrenar con <code>fit</code>') +
      FIT + '<p class="cl" style="margin:.6em 0 .9em"><code>fit</code> repite adelante, atrás y actualizar. <code>epochs=60</code> 60 vueltas · <code>batch_size=32</code> 12 pasos por vuelta · <code>validation_split=0.2</code> el simulacro</p>' +
      demo('moons', 'fill', mode='fit'),
      notes('La lámina más importante del bloque. Pulsa <b>Entrenar 60 épocas</b> (o avanza: arranca solo).',
            'Izquierda: la zona ámbar es donde la red dice «clase 1»; la línea blanca es su frontera (probabilidad 0.5). Al principio adivina; en pocas épocas la frontera se dobla para seguir las lunas.',
            'Derecha: la pérdida de entrenamiento (ámbar) y la de validación (blanca punteada) bajan <b>juntas</b>. Validación = <b>el simulacro</b>: 96 ejemplos que la red no estudia y que usamos para ver si entendió o memorizó. Si la blanca subiera mientras la ámbar baja, estaría memorizando (sobreajuste, semana 3).',
            '<code>fit</code> hace todo lo de esta mañana: adelante, pérdida, culpas hacia atrás y un paso de Adam, 12 veces por época durante 60 épocas: 720 pasos.'),
      block='08', group=G8, minutes=4, steps=1)

# ---- predict
PRED = code("""
p = model.predict(NUEVOS)       # 0..1
clase = (p >= 0.5).astype(int)  # 0 / 1
model.evaluate(X_test, y_test)  # exam
""", hl='1:1;2:1;3:2;4:3', out='p = [0.005 0.995 0.252]<br>        clase = [0 1 0]')
slide('keras-predict', 'Predecir: de probabilidad a decisión', head('Predecir: de probabilidad a decisión', '<code>predict</code> da una probabilidad y el umbral 0.5 la convierte en sí o no. <code>evaluate</code> toma el examen final.') + f"""
<div class="split" style="grid-template-columns:6fr 6fr;gap:2em">
  {demo('moons', 'fig', mode='predict')}
  <div class="col" style="gap:1.2em">
    {PRED}
    {st(4, '<div class="keybar"><span>Examen final: 120 ejemplos que la red nunca vio. Exactitud <b class="num">95 %</b>.</span></div>')}
    {st(4, '<p class="cap"><code>predict</code> y <code>evaluate</code> <b>no cambian los pesos</b>: solo usan lo aprendido. El umbral 0.5 no es sagrado: en el bloque 09 lo movemos.</p>')}
  </div>
</div>""", notes(
    'Tres socios nuevos, los mismos de la Tarea final 1 del NB02. Avanza para ver uno por uno.',
    'Primero: probabilidad 0.005 → clase 0. Segundo: 0.995 → clase 1. Tercero: 0.25 → clase 0, pero menos seguro; está más cerca de la frontera.',
    '<code>model.evaluate(X_test, y_test)</code> devuelve la pérdida y la exactitud en el examen final: 95 %. Separar un examen final que la red nunca ve es la forma honesta de medir.',
    'Ni <code>predict</code> ni <code>evaluate</code> entrenan: no tocan pesos ni sesgos. Solo <code>fit</code> aprende.'),
    block='08', group=G8, minutes=2)

# ---- all together
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
slide('keras', 'Todo junto: tu primera red en Keras', head('Todo junto: tu primera red en Keras') + f"""
<div class="split" style="grid-template-columns:7fr 5fr;align-items:start;gap:2em">
  {CODE_K}
  <div class="col" style="gap:1em">
    {st(1, '<div class="mapi"><span>1 · Construir</span><b>apilar capas Dense: ReLU dentro, sigmoide a la salida</b></div>')}
    {st(2, '<div class="mapi"><span>2 · Compilar</span><b>Adam + la BCE del viernes + exactitud</b></div>')}
    {st(3, '<div class="mapi"><span>3 · Entrenar</span><b>fit = adelante, atrás y actualizar, por lotes y épocas</b></div>')}
    {st(4, '<div class="mapi"><span>4 · Predecir</span><b>probabilidad → umbral → decisión</b></div>')}
    {st(4, '<p class="say">Diez líneas, <b class="num">337</b> parámetros y <b class="num">95 %</b> en el examen final.</p>')}
  </div>
</div>""", notes(
    'El resumen para tomarle foto: las diez líneas que van a escribir en la Parte F del NB02.',
    'Pregunta rápida antes de la práctica: «¿En qué línea está la retropropagación?» (dentro de <code>fit</code>: Keras y TensorFlow la hacen solos).'),
    block='08', group=G8, minutes=2)

practice('practica3', 'Práctica en clase: NB02', 'En parejas. Todo el código ya viene escrito y comentado. Las partes A a D repiten las láminas con código: los números coinciden.',
         ['<b>T</b> · Importa TensorFlow y Keras; tu primer tensor', 'A · Forward: <b>0.56</b> y pérdida <b>0.59</b> · B · culpas <b>−0.44, −0.27, −0.28</b>',
          'C · Un paso: <b>56 % → 65 %</b> · D · TensorFlow coincide con tu cuenta', 'E · Keras paso a paso: <b>XOR resuelto</b> con 33 parámetros',
          'F · Las lunas: <b>337</b> parámetros y <b>95 %</b> en el examen final', '<b>Experimento 2</b> · los círculos con más de <b>90 %</b>'], 'nb02', 40, G8, '08',
         notes('Dinámica: 30 minutos en parejas (o salas de 3) y 10 de puesta en común. Sin nota: el objetivo es que todas las parejas lleguen a la Parte F.',
               'Prioridad si el tiempo aprieta: T, A, E y F. B, C, D y la Parte G (la carrera de optimizadores) quedan para la casa.',
               'No hay nada que programar: cada parte explica qué va a pasar, trae el código comentado y termina en <b>Para pensar</b> (respuesta plegada) y <b>Experimenta</b> (cambiar un número y volver a ejecutar). Pide que digan qué esperan antes de ejecutar.',
               'Experimento 2: con dos capas de 16 y ReLU los círculos pasan del 90 % (en nuestra corrida, 98 %).',
               'Problema frecuente: «No module named…» casi nunca pasa en Colab; si pasa, abrieron el notebook fuera de Colab.'))

# ======================================================================= 09 · métricas
section('b09', '09', '¿El modelo es bueno?', '¿Cómo sabemos si el modelo es bueno de verdad?',
        ['87 % que no vale nada', 'La matriz de confusión', 'Recall, precisión y AUC'], 'Sábado · 15 minutos', G9, '09 · ¿El modelo es bueno?',
        notes('Aquí está la <b>idea clave 5</b>: por qué la exactitud engaña con datos desbalanceados.'))

slide('trampa87', '87 % de exactitud puede no valer nada', f"""
<div class="col fill">
  {head('87 % de exactitud puede no valer nada', 'Una cooperativa busca a los socios que caerán en mora: 13 de cada 100. Ahora la clase <b>positiva</b> es «cae en mora», el caso que buscamos (positiva no significa buena).', key(5))}
  {demo('trap', 'fill')}
</div>""", notes(
    '<b>Anuncia el cambio:</b> hasta ahora la clase 1 era «pagó». Desde aquí, la clase positiva es <b>la mora</b>, el caso que queremos detectar. «Positiva» no significa buena: en una prueba médica, positivo indica enfermedad.',
    '<b>Idea clave 5.</b> Paso 1: 100 socios (datos ficticios), 13 caen en mora. Un modelo que nunca avisa es como una alarma de humo que nunca suena: casi siempre «acierta».',
    'Paso 2: un «modelo» perezoso que siempre dice «está al día» acierta 87 de 100… y <b>no encuentra a ningún moroso</b>, que es justo lo que la cooperativa necesita. <b>La alarma de humo:</b> una que nunca suena «acierta» casi todos los días del año y no sirve para nada.',
    'Paso 3: una red de verdad le da a cada socio un puntaje de riesgo y marca a quien supera el umbral. Mueve el umbral: si lo bajas, encuentras más morosos pero con más falsas alarmas; si lo subes, al revés. La exactitud casi no se mueve, pero la utilidad sí.',
    '<span class="q">Pregunta:</span> «¿Qué es peor para la cooperativa: una falsa alarma o un moroso que no vimos?» Depende del negocio, y eso decide el umbral.'),
    block='09', group=G9, minutes=6, steps=3)

slide('metricas', 'Mira más allá de la exactitud', f"""
<div class="split" style="grid-template-columns:6fr 5fr">
  <div class="col">
    {head('Mira más allá de la exactitud', 'Tres preguntas mejores cuando los casos que buscas son pocos.', key(5))}
    <ul class="steps-list">
      {st(1, '<span class="k">R</span><span><b>Recall:</b> de los que caen en mora, ¿cuántos encontramos? <span class="num">10 de 13</span></span>', 'li')}
      {st(2, '<span class="k">P</span><span><b>Precisión:</b> de los que marcamos, ¿cuántos sí caen? <span class="num">10 de 18</span></span>', 'li')}
      {st(3, '<span class="k">A</span><span><b>AUC:</b> ¿qué tan bien ordena el riesgo? 0.5 es tirar una moneda; 1 es perfecto. AUC 0.5 <b>no</b> significa 50 % de exactitud.</span>', 'li')}
    </ul>
    {st(3, hist('Años 40', 'la curva ROC y el AUC nacen con el radar en la Segunda Guerra Mundial'))}
  </div>
  {st(3, demo('rank', 'fig'), cls='fig')}
</div>""", notes(
    'Recall (sensibilidad): de los morosos reales, qué porcentaje detectamos. Precisión: de los que marcamos, cuántos lo eran de verdad.',
    'AUC: si tomo un moroso y un socio al día al azar, ¿con qué probabilidad el modelo le da más riesgo al moroso? La imagen lo muestra: el buen modelo pone los morosos (amarillo) arriba; la moneda los reparte.',
    'Ojo: <b>AUC 0.5 no significa 50 % de exactitud</b>. Mide cómo ordena el riesgo, no cuántas decisiones acierta: el modelo perezoso del 87 % tiene AUC 0.5 porque a todos les da el mismo puntaje.',
    'En la semana 3 volvemos a esto cuando hablemos de explicar por qué un modelo dijo «no».'),
    block='09', group=G9, minutes=4)

# ======================================================================= cierre
slide('quizfinal', 'Quiz final: ¿cuánto avanzamos?', head('Quiz final: ¿cuánto avanzamos?', '10 preguntas tipo Kahoot. Vuelven las 5 ideas clave del pre-quiz: así vemos tu avance.', chip('No es nota', 'ok')) + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:1em">
  <ol class="steps-list" style="gap:1.2em">
    <li><span class="k">1</span><span>Abre <b>deeplearningweek1.vercel.app/?final</b></span></li>
    <li><span class="k">2</span><span>Usa <b>el mismo nombre</b> que en el pre-quiz</span></li>
    <li><span class="k">3</span><span>Pega tu código en el chat de Teams</span></li>
  </ol>
  <div class="center">{qr('final')}</div>
</div>""", notes(
    'Diez minutos. Pide que usen el mismo nombre que en el pre-quiz: el panel de resultados los empareja por nombre.',
    'Después de clase, copia todo el chat en <b>Resultados_quiz.html</b> y verás el avance del grupo en cada idea clave.'),
    block='C', group=GC, minutes=10, label='Cierre')

WEEK = [('Ejemplos', 160, 110), ('Neurona', 490, 110), ('Activación', 820, 110), ('Perceptrón', 1150, 110), ('XOR', 1480, 110),
        ('Pérdida', 1480, 330), ('Gradiente', 1150, 330), ('Red en capas', 820, 330), ('Retropropagación', 490, 330), ('Keras', 160, 330),
        ('Métricas', 160, 550)]
KEYS5 = ('Neurona', 'Activación', 'XOR', 'Gradiente', 'Métricas')
wsvg = ('<svg viewBox="0 0 1640 640" role="img" aria-label="Mapa de la semana: de los ejemplos a las métricas">'
        '<defs><marker id="wk-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#ffb541"/></marker></defs>')
def _edge(a, b):
    (x1, y1), (x2, y2) = a[1:], b[1:]
    if y1 == y2:
        d = 145 if x2 > x1 else -145
        return x1 + d, y1, x2 - d, y2
    return x1, y1 + 46, x2, y2 - 46
for i in range(len(WEEK) - 1):
    x1, y1, x2, y2 = _edge(WEEK[i], WEEK[i + 1])
    wsvg += f'<path data-draw="{i}" d="M{x1} {y1} L{x2} {y2}" stroke="#ffb541" stroke-width="5" fill="none" stroke-linecap="round" marker-end="url(#wk-arr)"/>'
for n, x, y in WEEK:
    hot = n in KEYS5
    wsvg += (f'<g><rect x="{x - 145}" y="{y - 46}" width="290" height="92" rx="46" fill="#0f1a29" stroke="{"#ffb541" if hot else "#2d394a"}" stroke-width="4"/>'
             f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-size="28" font-weight="600" fill="#f1f6fa" font-family="Lexend, sans-serif">{n}</text></g>')
route = ' L'.join(f'{x} {y}' for _, x, y in WEEK)
wsvg += (f'<circle r="13" fill="#ffb541" class="wk-pulse"><animateMotion dur="12s" repeatCount="indefinite" path="M{route}"/></circle>'
         '<text x="360" y="560" font-size="24" fill="#899aae" font-family="Lexend, sans-serif">Borde amarillo: las 5 ideas clave</text></svg>')
slide('mapa-semana', 'La semana en un mapa', head('De cero a tu primera red', 'Todo lo de la semana, en el orden en que lo vimos.') +
      f'<div class="fig fill" data-demo="draw">{wsvg}</div>',
      notes('Recorre el camino en voz alta: aprendemos de ejemplos → una neurona suma y traza una línea → la activación la dobla → el perceptrón aprende de errores → choca con XOR → medimos el error → bajamos la montaña → las capas vencen a XOR → repartimos la culpa → Keras lo hace todo → y medimos bien.',
            'Para repasar: la guía de estudio tiene un tema por cada parada.'),
      block='C', group=GC, minutes=2, label='Cierre')

HIST1 = [('1676', 'Leibniz · la regla de la cadena'), ('1805', 'Legendre · el MSE'), ('1847', 'Cauchy · bajar por la pendiente'),
         ('1943', 'McCulloch y Pitts · la neurona'), ('1958', 'Rosenblatt · el perceptrón'), ('1969', 'Minsky y Papert · XOR')]
HIST2 = [('1986', 'Rumelhart y Hinton · retropropagación'), ('2010', 'ReLU y buenos pesos iniciales'), ('2014', 'Kingma y Ba · Adam'),
         ('2015', 'TensorFlow y Keras'), ('2024', 'Muon · llega a Kimi K2'), ('2026', 'Tú · tu primera red')]


def tl(items, step):
    return st(step, '<div class="tl">' + ''.join(f'<div class="ev"><span class="y num">{y}</span><i></i><span class="d">{d}</span></div>' for y, d in items) + '</div>')


slide('historia', 'Todo lo que vimos tiene fecha', head('Todo lo que vimos tiene fecha', 'Casi todas las ideas de la semana tienen décadas, algunas siglos. Lo que cambió es cuánto cómputo y cuántos datos tenemos.') +
      '<div class="col hist-tl" style="gap:1.6em;margin-top:.2em">' + tl(HIST1, 1) + tl(HIST2, 2) + '</div>' +
      st(3, '<div class="trendbar" style="margin-top:1.4em"><span>Si las ideas son viejas, ¿qué hace avanzar al deep learning: <b>mejores algoritmos o más cómputo</b>? Es la pregunta de la lectura de la semana.</span></div>'),
      notes('Lámina para reflexionar, no para memorizar fechas. Recorre la primera fila: la regla de la cadena tiene más de 300 años; el MSE, más de 200; el descenso de gradiente, casi 180.',
            'Segunda fila: la retropropagación se populariza en 1986, pero las redes profundas despegan después de 2010, cuando llegan las GPU, los datos y trucos como ReLU. Adam es de 2014; TensorFlow y Keras, de 2015.',
            '<span class="q">Pregunta para el chat:</span> «Si casi todo es viejo, ¿por qué el deep learning explotó recién en la última década?» Respuesta esperada: datos, cómputo (GPU) y algunos algoritmos clave. Conecta con la encuesta de la lectura.'),
      block='C', group=GC, minutes=2, label='Cierre')


slide('lo-que-viene', 'Lo que viene: semanas 2 y 3', head('Lo que viene: semanas 2 y 3', 'Las próximas lecturas de tendencia salen de preguntas que hoy ya puedes hacerte.', chip('Lecturas de tendencia', 'trend')) + f"""
<div class="split even" style="gap:2em;align-items:stretch;margin-top:1.4em;flex:none">
  {st(1, '<div class="panel col" style="gap:.8em;height:100%"><span class="chip trend">Semana 2</span><h3 class="big" style="font-weight:600">¿El regreso de las redes recurrentes? Transformers, Mamba y la búsqueda de la arquitectura ideal</h3><p class="say">Hoy la red miró todos los datos a la vez. ¿Y si llegan en orden, como las palabras de una frase o las ventas de cada día?</p></div>')}
  {st(2, '<div class="panel col" style="gap:.8em;height:100%"><span class="chip trend">Semana 3</span><h3 class="big" style="font-weight:600">¿Puedes explicar por qué tu modelo dijo «no»?</h3><p class="say">El socio B del NB01 recibió un «no» (z = −3.61). En Ecuador, desde marzo de 2026, una norma de la Superintendencia de Protección de Datos permite pedir una explicación de la lógica del algoritmo.</p></div>')}
</div>""", notes(
    'Deja las dos preguntas sembradas. Semana 2: arquitecturas para datos con estructura (imágenes, secuencias); la lectura discute si las redes recurrentes modernas como Mamba vuelven a competir con los Transformers.',
    'Semana 3: explicabilidad y robustez. El gancho es el socio B del viernes (z = −3.61): si un modelo de deep learning le niega el crédito, ¿cómo se lo explicamos? La lectura cita la norma ecuatoriana de 2026 que permite pedir esa explicación.',
    '<span class="q">Pregunta para cerrar:</span> «¿Sus datos son tablas, imágenes, texto o series de tiempo?» Eso decidirá la arquitectura la próxima semana.'),
    block='C', group=GC, minutes=2, label='Cierre')

slide('recursos', 'Para repasar y profundizar', head('Para repasar y profundizar') + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:.6em">
  <ul class="checks" style="gap:1em">
    <li><b>Guía de estudio de la semana:</b> los 9 temas con ejemplos y ejercicios</li>
    <li><b>Nielsen (2015)</b>, <i>Neural networks and deep learning</i>, capítulos 1 y 2 · neuralnetworksanddeeplearning.com</li>
    <li><b>Zhang, Lipton, Li y Smola (2023)</b>, <i>Dive into deep learning</i>, «Multilayer perceptrons» · d2l.ai</li>
    <li><b>TensorFlow Playground</b>: entrena redes en el navegador · playground.tensorflow.org</li>
    <li>Los notebooks NB01 y NB02 quedan en la página para practicar cuando quieras</li>
  </ul>
  <div class="center">{qr('guia')}</div>
</div>""", notes('La guía de estudio resume todo con fórmulas explicadas; los notebooks quedan abiertos para practicar.'),
    block='C', group=GC, minutes=1, label='Cierre')

slide('gracias', 'Gracias', '<div class="col" style="justify-content:center;flex:1;gap:1.6em">' +
      '<h2 class="display" style="font-size:6em">Gracias</h2>' +
      '<p class="lede" style="font-size:1.6em;max-width:30em">En el chat, del 1 al 5: <b>¿podrías explicarle a un colega cómo aprende una red?</b></p>' +
      '<p class="say mu">Andrés Ordóñez-Bolaños · Neural Networks: Deep Learning · UIDE</p></div>',
      notes('Pide el número del 1 al 5 y compáralo con el del viernes.', 'Al terminar: <b>«Finalizar reunión para todos»</b> para que la grabación se cierre correctamente.'),
      layout='L-statement', block='C', group=GC, minutes=1, label='Cierre')


# ======================================================================= new slides (placed with move())
# --- 08 · memorizar: generalisation and the three groups of data
SPL = [(1, [(100, '600 puntos de las lunas', 'all')]),
       (2, [(80, '480 para estudiar', 'tr'), (20, '120 · prueba', 'te')]),
       (3, [(64, '384 · entrenamiento', 'tr'), (16, '96 · validación', 'va'), (20, '120 · prueba', 'te')])]
sbars = ''.join(st(n, ''.join(f'<i class="{c}" style="--w:{w}%"><span>{t}</span></i>' for w, t, c in segs), cls='sbar') for n, segs in SPL)
slide('memorizar', 'Aprender no es memorizar', head('Aprender no es memorizar', 'Queremos que la red acierte con casos <b>nuevos</b>: eso es <b>generalizar</b>. Si solo repite lo que estudió, está <b>sobreajustada</b>.') + f"""
<div class="col" style="gap:.9em;margin-top:.6em">
  {sbars}
  {st(3, '<div class="legend" style="margin-top:.3em"><span><i style="background:var(--amber)"></i>entrenamiento: los ejercicios que estudia</span><span><i style="background:var(--ink)"></i>validación: el simulacro</span><span><i style="background:var(--ink-3)"></i>prueba: el examen final</span></div>')}
  {st(4, '<p class="big num" style="margin-top:.6em">384 ÷ 32 = <b class="am">12</b> pasos por época · × 60 épocas = <b class="am">720</b> pasos</p>')}
</div>""", notes(
    'Antes de entrenar, la pregunta más importante: ¿cómo sabremos si la red <b>aprendió</b> o solo <b>memorizó</b>? Un estudiante puede memorizar diez respuestas y fallar cuando cambian los números. Funcionar con casos nuevos se llama <b>generalización</b>; adaptarse demasiado a los detalles de los ejemplos de estudio se llama <b>sobreajuste</b>.',
    'Paso 1: el NB02 genera 600 puntos. Paso 2: separa 120 para la <b>prueba</b> (el examen final, que no se mira hasta el final). Quedan 480.',
    'Paso 3: de esos 480, el 20 % (96) es <b>validación</b> (el simulacro: no ajusta pesos, pero nos dice cómo vamos). Los que de verdad ajustan pesos son <b>384</b>.',
    'Paso 4: con lotes de 32, 384 / 32 = 12 actualizaciones por época; con 60 épocas, 720. Por eso «época» y «paso» no son lo mismo.',
    'Si miramos la prueba una y otra vez para cambiar el modelo, deja de ser un examen independiente.'),
    block='08', group=G8, minutes=3)

# --- 09 · confusión: the four possible outcomes
CM = [(1, 'vp', '10', 'verdaderos positivos', 'alertó y sí cae en mora'), (2, 'fn', '3', 'falsos negativos', 'no alertó y sí cae: se nos pasó'),
      (3, 'fp', '8', 'falsos positivos', 'alertó y está al día: falsa alarma'), (4, 'vn', '79', 'verdaderos negativos', 'no alertó y está al día')]
cmc = {k: st(n, f'<b class="num">{v}</b><span class="nm">{t}</span><span class="ds">{d}</span>', cls=f'cm {k}') for n, k, v, t, d in CM}
CMAT = ('<div class="cmat"><span></span><span class="ch">El modelo <b>alertó</b></span><span class="ch">El modelo <b>no alertó</b></span>'
        '<span class="rh">Cae en mora <b class="num">13</b></span>' + cmc['vp'] + cmc['fn'] +
        '<span class="rh">Está al día <b class="num">87</b></span>' + cmc['fp'] + cmc['vn'] + '</div>')
slide('confusion', 'La matriz de confusión', f"""
<div class="split" style="grid-template-columns:7fr 5fr;gap:2.2em">
  <div class="col" style="gap:1em">
    {head('La matriz de confusión: cuatro resultados', '«Verdadero» o «falso» dice si acertó. «Positivo» o «negativo» dice si alertó.', key(5))}
    {CMAT}
  </div>
  <div class="col" style="gap:1.1em;justify-content:center">
    {st(4, '<p class="big">Exactitud: (10 + 79) / 100 = <b class="num">89 %</b></p>')}
    {st(5, eq([(r'\text{recall}', 'morosos encontrados', 'out'), ('=', '', 'op'), (r'\dfrac{10}{10+3}', 'de todos los morosos', 'x'), (r'\approx', '', 'op'), (r'76.9\,\%', '', 'num')], size='1em'))}
    {st(6, eq([(r'\text{precisión}', 'alarmas ciertas', 'out'), ('=', '', 'op'), (r'\dfrac{10}{10+8}', 'de todas las alarmas', 'x'), (r'\approx', '', 'op'), (r'55.6\,\%', '', 'num')], size='1em'))}
  </div>
</div>""", notes(
    'Una red de verdad sobre los mismos 100 socios. Cada socio cae en una de cuatro casillas; la tabla que las cuenta se llama <b>matriz de confusión</b>.',
    'Pasos 1 a 4: encontró 10 de los 13 morosos (verdaderos positivos) y se le pasaron 3 (falsos negativos). Además alertó por error sobre 8 socios al día (falsos positivos), y dejó tranquilos a los 79 restantes (verdaderos negativos). Exactitud: 89 de 100.',
    'Paso 5. <b>Recall</b> empieza por los morosos reales: 10 de 13 ≈ 76.9 %. Paso 6. <b>Precisión</b> empieza por las alarmas: de 18 alertas, 10 eran ciertas ≈ 55.6 %.',
    'Usa «exactitud» para accuracy y reserva «precisión» para esta segunda medida, así no se mezclan los nombres.',
    '<span class="q">Para decir en clase:</span> «Antes de celebrar un porcentaje, preguntémonos qué clase de errores está escondiendo».'),
    block='09', group=G9, minutes=3)

move('memorizar', 'keras-compile')
move('confusion', 'trampa87')
