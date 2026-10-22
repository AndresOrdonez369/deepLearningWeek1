"""Concept maps for teaching week 1. Coordinates on a 1400 x 800 canvas.
kind: core | key | ex (example/analogy) | tool (code) | trend | trap
Each node: say (what to say in one sentence), ex (example to use), ask (question for the class),
trap (frequent mistake), slide (deck slide id), nb (notebook section)."""


def N(id, label, x, y, kind='core', key=None, say='', ex='', ask='', trap='', slide='', nb=''):
    return dict(id=id, label=label, x=x, y=y, kind=kind, key=key, say=say, ex=ex, ask=ask, trap=trap, slide=slide, nb=nb)


MAPS = []

# ------------------------------------------------------------------ the whole week
MAPS.append(dict(id='semana', short='Semana', title='La semana completa', sub='El hilo de las dos sesiones: cada parada es un bloque de slides.',
  nodes=[
    N('ejemplos', 'Aprender de ejemplos', 230, 110, say='El machine learning encuentra las reglas a partir de ejemplos con su respuesta, en vez de recibirlas escritas.', ex='El filtro de spam aprendió de millones de correos marcados.', ask='¿Qué problema de tu trabajo se resuelve hoy con reglas escritas a mano?', trap='Creer que «IA» siempre significa que aprende: el GPS es IA y no aprende.', slide='reglas', nb='—'),
    N('neurona', 'Neurona|z = w·x + b', 700, 110, 'key', 1, say='Multiplica cada dato por su peso, suma todo y añade el sesgo.', ex='Tu nota final del curso: Ana llega a 76 y, con una exigencia de ejemplo de 70, z = +6. Aplicado: el comité de crédito, socio A con z = 2.81.', ask='Si el comité se vuelve más exigente, ¿qué número cambia?', trap='Olvidar el sesgo o el signo de un peso negativo.', slide='nota', nb='NB01 §1'),
    N('activacion', 'Activación', 1170, 110, 'key', 2, say='Convierte el puntaje en la salida y, sobre todo, dobla la línea para que la red aprenda curvas.', ex='Interruptor (escalón), regulador de luz (sigmoide), válvula (ReLU).', ask='Sin activación, ¿qué forma puede aprender una red de 100 capas?', trap='Pensar que la activación solo sirve para dar probabilidades.', slide='doblar', nb='NB01 §2'),
    N('perceptron', 'Perceptrón|aprende de errores', 1170, 310, say='Si se equivoca, empuja los pesos hacia la respuesta correcta; si acierta, no toca nada.', ex='La corrección −0.30 → +2.70 con un solo socio.', ask='¿Qué hace el perceptrón cuando acierta?', trap='Creer que corrige aunque acierte.', slide='entrenar', nb='NB01 §3–4'),
    N('xor', 'El límite: XOR', 700, 310, 'key', 3, say='Una neurona solo traza una recta, y ninguna recta separa XOR.', ex='La luz de la escalera: dos interruptores en posiciones distintas.', ask='¿Alguien puede trazar una línea que separe las dos luces encendidas?', trap='Pensar que con más épocas el perceptrón terminará aprendiendo XOR.', slide='xor', nb='NB01 §5'),
    N('red', 'Red en capas', 230, 310, say='Cada neurona oculta traza su línea y la salida las combina: así nacen fronteras curvas.', ex='Dos neuronas vencen a XOR; las agencias de Riobamba, Latacunga y Ambato y el comité central.', ask='¿Cuántas neuronas ocultas necesitas, como mínimo, para XOR?', trap='Creer que más capas siempre es mejor.', slide='xor-resuelto', nb='NB02 E'),
    N('perdida', 'Pérdida', 230, 510, say='Un solo número que dice qué tan mal vamos; 0 es perfecto.', ex='Casas de Quito (MSE = 132.25) y el meteorólogo «seguro» (BCE).', ask='¿Por qué la BCE castiga tanto decir 1 % cuando el socio sí pagó?', trap='Usar MSE para clasificar sí/no.', slide='perdida', nb='NB01 §6'),
    N('gradiente', 'Descenso de gradiente', 700, 510, 'key', 4, say='Damos cada paso en contra de la pendiente: así la pérdida baja.', ex='Bajar el Cotopaxi con neblina, tanteando con el pie; y la ducha: si giras la llave de golpe te quemas.', ask='Si la pendiente de un peso es +4, ¿el peso sube o baja?', trap='Restar o sumar al revés: la pendiente apunta cuesta arriba.', slide='pendiente', nb='NB01 §7–8'),
    N('retro', 'Retropropagación', 1170, 510, say='Reparte la culpa del error hacia atrás, multiplicando efectos con la regla de la cadena.', ex='La barra de chocolate amarga y la cadena del cacao; los engranajes.', ask='Si una neurona ReLU está apagada, ¿qué culpa reciben sus pesos?', trap='Creer que hay que hacerla a mano: TensorFlow la calcula.', slide='culpa', nb='NB02 A–D'),
    N('entrenar', 'Entrenar bien', 1170, 710, say='ReLU en las ocultas, pesos al azar bien escalados, un learning rate sensato y lotes.', ex='La encuesta del INEC en vez del censo; la carrera de los optimizadores.', ask='¿Por qué no empezar con todos los pesos en cero?', trap='Subir el learning rate para «ir más rápido».', slide='carrera', nb='NB02 G'),
    N('keras', 'Keras en 3 pasos', 700, 710, 'tool', say='Tres pasos que hacen todo lo de la semana: capas Dense, compile y fit.', ex='TensorFlow es el motor y Keras el volante; las capas se apilan como LEGO; la red de las lunas: 337 parámetros y 95 % en el examen final.', ask='¿Qué hace fit() por dentro?', trap='Olvidar separar datos de validación.', slide='tf-keras', nb='NB02 F'),
    N('metricas', 'Métricas|más allá de la exactitud', 230, 710, 'key', 5, say='Cuando los casos que buscas son pocos, la exactitud engaña: mira recall, precisión y AUC.', ex='Una alarma de humo que nunca suena «acierta» casi siempre. 87 % de exactitud sin encontrar a ningún moroso.', ask='¿Qué es peor para la cooperativa: una falsa alarma o un moroso que no vimos?', trap='Celebrar un 95 % sin mirar cuántos casos positivos hay.', slide='trampa87', nb='—'),
  ],
  edges=[('ejemplos', 'neurona', 'su base es'), ('neurona', 'activacion', 'decide con'), ('activacion', 'perceptron', 'con escalón'),
         ('perceptron', 'xor', 'choca con'), ('xor', 'red', 'lo resuelve la'), ('red', 'perdida', 'se mide con'), ('perdida', 'gradiente', 'se baja con'),
         ('gradiente', 'retro', 'la pendiente sale de'), ('retro', 'entrenar', 'y para'), ('entrenar', 'keras', 'en código'), ('keras', 'metricas', 'se juzga con'),
         ]))

# ------------------------------------------------------------------ 01
MAPS.append(dict(id='b01', short='01', title='01 · IA, machine learning y deep learning', sub='Qué significa que una máquina aprenda de ejemplos.',
  nodes=[
    N('ia', 'Inteligencia artificial', 220, 160, say='Sistemas que hacen tareas que parecen inteligentes, aprendan o no.', ex='El GPS que calcula la ruta; el rival de un videojuego.', ask='¿La calculadora del celular es IA?', trap='Usar «IA» como sinónimo de ChatGPT.', slide='circulos'),
    N('ml', 'Machine learning', 620, 160, say='La parte de la IA que aprende las reglas a partir de datos.', ex='Filtro de spam, recomendaciones de Netflix.', ask='¿Qué necesita un sistema de ML que un programa clásico no?', trap='Creer que aprende solo, sin ejemplos con respuesta.', slide='circulos'),
    N('dl', 'Deep learning', 1020, 160, 'key', None, say='Machine learning con redes neuronales de muchas capas.', ex='Desbloqueo facial, subtítulos automáticos, ChatGPT.', ask='¿Por qué se llama «profundo»?', trap='Pensar que siempre es la mejor opción para datos de tabla.', slide='usos'),
    N('reglas', 'Reglas escritas a mano', 220, 470, 'trap', say='Funcionan cuando sabemos escribirlas, y fallan cuando el mundo cambia.', ex='«Si dice GRATIS, es spam» manda a spam el «¡Envío gratis!» de tu tienda.', ask='Escribe una regla para reconocer un gato. ¿Cuál es su contraejemplo?', trap='—', slide='gato'),
    N('ejemplos', 'Ejemplos con su respuesta', 620, 470, 'ex', say='Datos + respuestas → el modelo encuentra las reglas.', ex='10 000 correos marcados como spam o no spam.', ask='¿De dónde sacarías los ejemplos en tu trabajo?', trap='Olvidar que la calidad de las respuestas limita al modelo.', slide='reglas'),
    N('ingredientes', 'Datos + cómputo + algoritmos', 1020, 470, 'trend', say='Las ideas son de 1958; despegaron cuando se juntaron muchos datos, GPU y mejores algoritmos.', ex='AlexNet (2012), el Transformer (2017), ChatGPT (2022).', ask='Si el cómputo crece más de 3× por año, ¿importan todavía los algoritmos? (lectura)', trap='—', slide='ahora'),
  ],
  edges=[('ia', 'ml', 'contiene a'), ('ml', 'dl', 'contiene a'), ('ia', 'reglas', 'puede usar'), ('ml', 'ejemplos', 'aprende de'), ('dl', 'ingredientes', 'despegó por'), ('reglas', 'ejemplos', 'frente a')]))

# ------------------------------------------------------------------ 02
MAPS.append(dict(id='b02', short='02', title='02 · La neurona artificial', sub='Una calculadora con opinión.',
  nodes=[
    N('x', 'Datos x', 150, 140, say='Lo que sabemos del caso, ya escalado (0 = el promedio).', ex='Ingreso 0.8, antigüedad 0.5, atrasos −1.0.', ask='¿Qué significa un dato de −1.0?', trap='Usar datos sin escalar.', slide='comite', nb='NB01 §1'),
    N('w', 'Pesos w', 150, 400, say='Cuánto confía la neurona en cada dato; un peso negativo resta.', ex='Atrasos con peso −2.0: más atrasos, menos puntaje.', ask='¿Qué pasa si un peso vale 0?', trap='Olvidar que negativo × negativo suma.', slide='comite'),
    N('b', 'Sesgo b', 150, 650, say='La disposición general: qué tan exigente es el comité.', ex='b = −0.5: el comité empieza restando.', ask='¿Qué número cambia si el comité se vuelve más exigente?', trap='Olvidar sumarlo.', slide='comite'),
    N('z', 'Puntaje|z = w·x + b', 560, 400, 'key', 1, say='Multiplica, suma y añade el sesgo.', ex='Tu nota final del curso: cada nota por lo que pesa, menos la exigencia (Ana: 76 − 70 = +6). El comité: socio A, z = 2.81.', ask='¿El socio B (0.2, −0.5, 1.5) es aprobado?', trap='Confundir z (puntaje) con la probabilidad.', slide='nota', nb='NB01 §1'),
    N('linea', 'Una línea de decisión', 560, 140, 'ex', say='Donde z = 0 la neurona duda; de un lado aprueba, del otro rechaza.', ex='Mueve los pesos en la lámina: la línea gira; el sesgo la desplaza.', ask='¿Qué pasa con un socio justo sobre la línea?', trap='Creer que una neurona puede trazar curvas.', slide='linea'),
    N('act', 'Activación', 900, 400, 'key', 2, say='Escalón, sigmoide o ReLU deciden qué sale; sin ellas, apilar capas no sirve.', ex='Interruptor, regulador de luz, válvula.', ask='¿Para qué sirve la activación?', trap='Decir «solo para dar probabilidades».', slide='activacion', nb='NB01 §2'),
    N('prob', 'Probabilidad|0 a 1', 1200, 210, say='La sigmoide aplasta el puntaje entre 0 y 1.', ex='z = 2.81 → 94 %; z = 0 → 50 %.', ask='¿Qué da z = −2.81?', trap='Leer 0.94 como «94 % de acierto del modelo».', slide='sigmoide'),
    N('curvas', 'Curvas (dobleces)', 1200, 600, say='Cada ReLU aporta un doblez; con varios se arma cualquier curva.', ex='La curva de demanda de taxis con 2, 4 u 8 neuronas.', ask='¿Cuántas capas sin activación equivalen a una sola?', trap='—', slide='doblar'),
  ],
  edges=[('x', 'z', 'entran a'), ('w', 'z', 'ponderan'), ('b', 'z', 'se suma a'), ('z', 'linea', 'z = 0 es'), ('z', 'act', 'pasa por'), ('act', 'prob', 'la sigmoide da'), ('act', 'curvas', 'la ReLU permite')]))

# ------------------------------------------------------------------ 03
MAPS.append(dict(id='b03', short='03', title='03 · Cómo aprende una neurona', sub='Equivocarse, corregir un poquito y repetir.',
  nodes=[
    N('pred', 'Predice', 200, 160, say='Calcula z y decide con su activación.', ex='El socio de la lámina 21 obtiene z = −0.30: rechaza.', ask='—', trap='—', slide='ciclo'),
    N('comp', 'Compara', 560, 160, say='Mira la respuesta correcta y y nota si se equivocó.', ex='El socio sí pagó (y = +1).', ask='¿Qué hace si acierta?', trap='—', slide='ciclo'),
    N('regla', 'Regla|w ← w + η·y·x', 920, 160, 'key', None, say='Si debía decir sí, suma el dato; si debía decir no, lo resta.', ex='w = (0.2, −0.5) → (1.2, 0.5); z pasa a +2.70.', ask='¿Y si el socio NO hubiera pagado y la neurona dijo sí?', trap='Corregir también cuando acierta.', slide='correccion', nb='NB01 §3'),
    N('epoca', 'Época', 1240, 400, say='Una vuelta completa por todos los ejemplos.', ex='Vuelta 1: 5 errores; vuelta 3: 0.', ask='¿Cuántas épocas necesitó en la demo?', trap='—', slide='entrenar', nb='NB01 §4'),
    N('conv', 'Si hay una línea, la encuentra', 940, 640, 'ex', say='Garantía de Rosenblatt (1958) y Novikoff (1962) para datos separables.', ex='La línea se pone verde: 0 errores.', ask='¿Qué pasa si no existe esa línea?', trap='—', slide='entrenar'),
    N('xor3', 'XOR: el límite', 520, 640, 'key', 3, say='Ninguna recta separa la luz de la escalera: el perceptrón nunca baja de los errores.', ex='Minsky y Papert (1969) y el primer invierno de la IA.', ask='¿Dónde aparece algo así en un negocio? (interacciones)', trap='Pensar que más épocas lo arreglan.', slide='xor', nb='NB01 §5'),
    N('locro', 'Sazonar un locro', 200, 520, 'ex', say='Pruebas, le falta sal, una pizca, vuelves a probar.', ex='Medio salero = un η demasiado grande.', ask='¿Qué pasa si echas medio salero?', trap='—', slide='ciclo'),
  ],
  edges=[('pred', 'comp', 'luego'), ('comp', 'regla', 'si falló, aplica'), ('regla', 'epoca', 'se repite durante'), ('epoca', 'conv', 'con datos separables'), ('conv', 'xor3', 'pero no con'), ('locro', 'pred', 'es como')]))

# ------------------------------------------------------------------ 04
MAPS.append(dict(id='b04', short='04', title='04 · Medir el error y mejorar', sub='Bajar la montaña con neblina.',
  nodes=[
    N('loss', 'Pérdida', 200, 400, say='Un número que dice qué tan mal vamos.', ex='Una nota al revés: 0 es perfecto.', ask='—', trap='—', slide='perdida', nb='NB01 §6'),
    N('mse', 'MSE (regresión)', 520, 170, say='Promedio de errores al cuadrado: castiga fuerte los grandes.', ex='Casas de Quito: 10, 5, 20 y 2 → 132.25.', ask='¿Qué casa pesa más en el total?', trap='Olvidar elevar al cuadrado.', slide='perdida'),
    N('bce', 'BCE (sí/no)', 520, 630, say='−log de la probabilidad que le dio a lo que pasó: castiga la falsa seguridad.', ex='99 % → 0.01; 50 % → 0.69; 1 % → 4.61.', ask='¿Qué meteorólogo pierde más credibilidad?', trap='Usar MSE para clasificar.', slide='bce'),
    N('pend', 'Pendiente (gradiente)', 860, 400, 'key', 4, say='Apunta cuesta arriba; por eso caminamos al revés.', ex='En w = 0 la pendiente es −6: el peso sube.', ask='Pendiente +4: ¿el peso sube o baja?', trap='Sumar la pendiente en vez de restarla.', slide='pendiente', nb='NB01 §7'),
    N('eta', 'Tamaño del paso η', 1200, 170, say='Muy corto: lento. Muy largo: se pasa y diverge.', ex='La ducha: giras la llave de golpe y pasas de helada a hirviendo. En la demo, η = 1.02 se aleja del fondo.', ask='¿Qué revisas primero si la pérdida sale NaN?', trap='Subir η para ir más rápido.', slide='eta', nb='NB01 §8'),
    N('gd', 'w ← w − η · pendiente', 1200, 630, 'key', 4, say='Un paso cuesta abajo, repetido hasta el fondo.', ex='w: 0 → 0.6 → 1.08 → 1.46; pérdida 9 → 1.51.', ask='¿Por qué los pasos se acortan solos?', trap='—', slide='pasos'),
    N('coto', 'Cotopaxi con neblina', 860, 120, 'ex', say='Altura = pérdida; posición = pesos; inclinación = gradiente; paso = η.', ex='Bajar hacia la laguna de Limpiopungo.', ask='¿Necesitas ver toda la montaña?', trap='Olvidar los mínimos locales (límite de la analogía).', slide='cotopaxi'),
  ],
  edges=[('loss', 'mse', 'para números:'), ('loss', 'bce', 'para sí/no:'), ('loss', 'pend', 'su inclinación es la'), ('pend', 'gd', 'se resta en'), ('eta', 'gd', 'escala el paso de'), ('coto', 'pend', 'se siente como')]))

# ------------------------------------------------------------------ 05
MAPS.append(dict(id='b05', short='05', title='05 · De una neurona a una red', sub='Muchas líneas simples forman decisiones complejas.',
  nodes=[
    N('ent', 'Entrada', 180, 400, say='Los datos; no calcula nada.', ex='Antigüedad y carga de la cuota.', ask='—', trap='Contarla como capa que aprende.', slide='red'),
    N('ocu', 'Capas ocultas', 540, 400, say='Inventan sus propias pistas a partir de los datos.', ex='Las agencias que resumen lo que ven.', ask='¿Quién les dice qué pistas inventar?', trap='—', slide='red'),
    N('sal', 'Salida', 900, 400, say='Toma la decisión final con las pistas.', ex='El comité central.', ask='—', trap='—', slide='red'),
    N('xor5', 'XOR resuelto', 260, 150, 'key', 3, say='Una neurona aprende «al menos uno», otra «los dos»; la salida combina.', ex='La franja entre dos líneas.', ask='¿Cuál es la red más pequeña que resuelve XOR?', trap='—', slide='xor-resuelto', nb='NB02 E'),
    N('pistas', 'Pistas cada vez más ricas', 900, 150, 'ex', say='Trazos → formas → «es un 7».', ex='El monto de una papeleta de depósito.', ask='En datos de tabla, ¿qué sería una «pista»?', trap='—', slide='pistas'),
    N('par', 'Parámetros', 1240, 400, 'tool', say='Un peso por conexión y un sesgo por neurona.', ex='Las perillas de una consola de sonido: 3·4 + 4 = 16 y 4·1 + 1 = 5, total 21. Las lunas del NB02: 337.', ask='¿Cuántos parámetros tiene una red 2-8-1?', trap='Olvidar los sesgos.', slide='parametros'),
    N('juega', 'Juega: 1, 2, 4, 8 neuronas', 560, 680, 'ex', say='Con 1 neurona solo hay línea; con 4 ya hay polígonos y curvas.', ex='Círculos: 1 neurona ~60 %, 4 neuronas ~100 %.', ask='¿Por qué 1 neurona no pasa del 60 % en los círculos?', trap='—', slide='juega'),
  ],
  edges=[('ent', 'ocu', 'alimenta a'), ('ocu', 'sal', 'alimentan a'), ('ocu', 'xor5', 'dos resuelven'), ('ocu', 'pistas', 'construyen'), ('sal', 'par', 'se cuenta en'), ('ocu', 'juega', 'se prueba en')]))

# ------------------------------------------------------------------ 06
MAPS.append(dict(id='b06', short='06', title='06 · Retropropagación', sub='Cómo se reparte la culpa del error.',
  nodes=[
    N('fwd', '1 · Hacia adelante', 190, 160, say='Cada capa hace la cuenta del viernes y pasa el resultado.', ex='0.45 → 0.61; 0.50 → 0.62; salida 0.56.', ask='—', trap='—', slide='adelante', nb='NB02 A'),
    N('err', 'Pérdida 0.59', 560, 160, say='La red dijo 56 % y el socio sí pagó.', ex='−log(0.56) = 0.59.', ask='¿Qué pérdida tendría si dijera 99 %?', trap='—', slide='adelante'),
    N('culpa', '2 · Culpa hacia atrás', 980, 160, 'key', None, say='La culpa de la salida es ŷ − y y viaja hacia atrás según cuánto influyó cada peso.', ex='La barra amarga y la cadena del cacao.', ask='Si la culpa de un peso es negativa, ¿sube o baja?', trap='Creer que todos los pesos tienen la misma culpa.', slide='culpa', nb='NB02 B'),
    N('cadena', 'Regla de la cadena', 980, 540, 'ex', say='Los efectos se multiplican a lo largo del camino.', ex='Engranajes: 3 × 6 = 18.', ask='Derivada de (3x)² en x = 1 por engranajes: ¿cuánto da?', trap='—', slide='engranajes'),
    N('num', 'Las culpas con números', 1250, 340, say='−0.44 en la salida; −0.27 y −0.28 en sus pesos; −0.07 y +0.04 en las ocultas.', ex='La oculta 2 debe bajar porque su peso es negativo.', ask='¿Por qué el signo de la oculta 2 es positivo?', trap='—', slide='atras', nb='NB02 B'),
    N('upd', '3 · Actualizar', 540, 540, 'key', 4, say='A cada peso se le resta η por su culpa: el descenso de gradiente del viernes.', ex='0.7 → 0.84; 56 % → 65 %; pérdida 0.59 → 0.42.', ask='¿Qué se repite miles de veces al entrenar?', trap='—', slide='actualizar', nb='NB02 C'),
    N('tape', 'GradientTape', 540, 720, 'tool', say='TensorFlow graba la ida y la recorre al revés: diferenciación automática.', ex='Diferencia con la cuenta a mano: 5.6 × 10⁻¹⁷.', ask='Entonces, ¿para qué entender la retropropagación?', trap='—', slide='tensorflow', nb='NB02 D'),
  ],
  edges=[('fwd', 'err', 'termina en'), ('err', 'culpa', 'se reparte'), ('culpa', 'cadena', 'se calcula con'), ('culpa', 'num', 'en el ejemplo'), ('cadena', 'upd', 'da la pendiente'), ('upd', 'tape', 'lo calcula'), ('upd', 'fwd', 'y se repite')]))

# ------------------------------------------------------------------ 07
MAPS.append(dict(id='b07', short='07', title='07 · Entrenar bien', sub='Tres trampas, los lotes y la carrera de los optimizadores.',
  nodes=[
    N('van', 'La culpa se apaga', 170, 170, 'trap', say='Cada sigmoide deja pasar como mucho ¼ de la culpa; tras 5 capas llega 0.001.', ex='El teléfono dañado: la sigmoide deja pasar como mucho ¼ en cada capa; tras cinco capas llega 0.001.', ask='¿Qué activación evita esto en las ocultas?', trap='—', slide='apaga'),
    N('relu', 'ReLU en las ocultas', 520, 170, say='Su pendiente es 1 cuando está activa: la culpa llega entera.', ex='Cambia a ReLU en la demo.', ask='—', trap='—', slide='apaga'),
    N('clon', 'Neuronas clonadas', 170, 460, 'trap', say='Si todos los pesos empiezan iguales, aprenden lo mismo.', ex='Cuatro estudiantes que copian la misma tarea: cuatro cuadernos, una sola idea.', ask='¿Por qué no iniciar en cero?', trap='—', slide='clones'),
    N('glorot', 'Pesos al azar bien escalados', 520, 460, say='Glorot (por defecto en Keras) o He para ReLU.', ex='4 neuronas, 4 ideas distintas.', ask='—', trap='—', slide='clones'),
    N('lotes', 'Lotes y épocas', 880, 460, say='Un lote de 32 = un paso; 150 lotes = una época.', ex='La encuesta del INEC en vez del censo.', ask='Con 4 800 socios y lotes de 32, ¿cuántos pasos por época?', trap='Confundir época con paso.', slide='lotes'),
    N('opt', 'SGD · Momentum · Adam', 880, 170, 'trend', say='Tres formas de caminar por el mismo valle.', ex='La carrera: el ganador depende de cómo se ajusta cada uno.', ask='¿Mejor algoritmo o más cómputo? (encuesta)', trap='Comparar sin ajustar a todos con el mismo cuidado.', slide='carrera'),
    N('lectura', 'Lectura: Más allá de Adam', 1230, 170, 'trend', say='Con una carrera justa, la ventaja de los nuevos se encoge (~1.4× → ~1.1×).', ex='Muon, Kimi K2, AlgoPerf.', ask='¿Qué harías con un presupuesto limitado de GPU?', trap='—', slide='tendencia1'),
    N('receta', 'La receta para arrancar', 1230, 460, 'tool', say='Escalar, ReLU, sigmoide, Adam 0.001, BCE, lotes de 32 y validación.', ex='Tómale foto.', ask='¿Cuál paso es el más olvidado?', trap='Ajustar el escalador con datos de validación.', slide='receta-arranque'),
  ],
  edges=[('van', 'relu', 'solución'), ('clon', 'glorot', 'solución'), ('relu', 'opt', 'y'), ('glorot', 'lotes', ''), ('opt', 'lectura', 'debate'), ('lotes', 'receta', ''), ('opt', 'receta', 'Adam en')]))

# ------------------------------------------------------------------ 08
MAPS.append(dict(id='b08', short='08', title='08 · Keras', sub='Tu primera red en tres pasos.',
  nodes=[
    N('build', '1 · Construir', 220, 220, 'tool', say='Sequential apila capas Dense: ReLU en las ocultas, sigmoide en la salida.', ex='Piezas de LEGO: Input(shape=(2,)), Dense(16, "relu") dos veces y Dense(1, "sigmoid").', ask='¿Por qué sigmoide en la salida?', trap='Olvidar Input(shape=...).', slide='keras-construir', nb='NB02 F'),
    N('comp', '2 · Compilar', 620, 220, 'tool', say='Elige optimizador, pérdida y métrica.', ex='Planear el estudio antes de empezar: Adam (cómo corrige), la BCE (qué mide) y la exactitud (qué reporta).', ask='¿Dónde viste antes la binary_crossentropy?', trap='Usar mse para sí/no.', slide='keras-compile'),
    N('fit', '3 · Entrenar', 1020, 220, 'tool', say='fit hace adelante, atrás y actualizar por lotes y épocas.', ex='Las lunas en vivo: 60 épocas de 12 pasos; la frontera se dobla y las dos curvas bajan juntas. Validación = el simulacro.', ask='¿Qué hace fit() por dentro?', trap='No separar validación.', slide='keras-fit'),
    N('summary', 'model.summary()', 420, 560, say='Cuenta los parámetros por capa.', ex='Lunas: 337.', ask='—', trap='—', slide='keras-construir'),
    N('curvas', 'Curvas de pérdida', 820, 560, say='Si la validación sube mientras el entrenamiento baja, se está memorizando.', ex='Semana 3: sobreajuste.', ask='¿Qué harías si la pérdida sube desde la época 1?', trap='—', slide='keras-fit'),
    N('reto', 'Mini-reto 2: círculos > 90 %', 1220, 560, 'ex', say='Práctica en clase y sin nota: diseña la red y entrénala.', ex='Prueba Dense(4) vs Dense(16).', ask='¿Qué red más pequeña logra 90 %?', trap='—', slide='practica3', nb='NB02 F'),
  ],
  edges=[('build', 'comp', 'luego'), ('comp', 'fit', 'luego'), ('build', 'summary', 'se revisa con'), ('fit', 'curvas', 'devuelve'), ('fit', 'reto', 'se practica en')]))

# ------------------------------------------------------------------ 09
MAPS.append(dict(id='b09', short='09', title='09 · ¿El modelo es bueno?', sub='Cuando la exactitud engaña.',
  nodes=[
    N('acc', 'Exactitud', 220, 250, say='Porcentaje de aciertos sobre el total.', ex='Una alarma de humo que nunca suena «acierta» casi todos los días. El modelo que siempre dice «al día» acierta 87 de 100.', ask='—', trap='Usarla sola con clases desbalanceadas.', slide='trampa87'),
    N('desb', 'Datos desbalanceados', 220, 560, 'key', 5, say='Si los casos que buscas son pocos, decir siempre «no» ya da una exactitud alta.', ex='13 morosos de 100: el modelo perezoso tiene 87 % y no encuentra a nadie.', ask='¿Qué otros problemas son así? (fraude, enfermedades raras)', trap='Celebrar un 95 % sin mirar la proporción.', slide='trampa87'),
    N('recall', 'Recall', 620, 160, say='De los que caen en mora, ¿cuántos encontramos?', ex='12 de 13 con umbral 0.5.', ask='—', trap='—', slide='metricas'),
    N('prec', 'Precisión', 620, 400, say='De los que marcamos, ¿cuántos sí caen?', ex='12 aciertos y 12 falsas alarmas.', ask='—', trap='—', slide='metricas'),
    N('umbral', 'Umbral', 1000, 280, say='Bajarlo encuentra más casos pero con más falsas alarmas.', ex='Mueve el umbral en la lámina 62.', ask='¿Qué es peor para la cooperativa: una falsa alarma o un moroso no visto?', trap='Dejar 0.5 por defecto sin pensar en el negocio.', slide='trampa87'),
    N('auc', 'AUC', 620, 640, say='Qué tan bien ordena el riesgo: 0.5 es una moneda, 1 es perfecto.', ex='El buen modelo pone a los morosos arriba.', ask='—', trap='—', slide='metricas'),
    N('s3', 'Semana 3: ¿por qué dijo «no»?', 1000, 600, 'trend', say='Explicar las decisiones del modelo; en Ecuador ya se puede pedir esa explicación.', ex='El socio B rechazado (z = −3.61).', ask='¿Cómo le explicarías la decisión al socio B?', trap='—', slide='lo-que-viene'),
  ],
  edges=[('acc', 'desb', 'engaña con'), ('desb', 'recall', 'mira'), ('desb', 'prec', 'mira'), ('desb', 'auc', 'mira'), ('recall', 'umbral', 'depende del'), ('prec', 'umbral', 'depende del'), ('auc', 's3', 'y luego')]))
