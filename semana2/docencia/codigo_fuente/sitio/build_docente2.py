"""Week-2 teacher guide and notes (only for the teacher): semana2/docencia/Guia_docente.html
usage: python build_docente2.py <semana2/docencia folder>
Slide numbers come from <folder>/slides/slides.json at build time; slide ids that are missing are reported and
printed as «?» so the build never breaks while the deck is still changing. The quiz key is read from banco2.py
(written by the student-site builder) when it exists."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit_docencia2 import page, section, chip, idea, box, formula  # noqa: E402

try:
    from banco2 import PRE, FINAL, TEMAS, CLAVES  # noqa: E402
    HAVE_BANK = True
except Exception:  # the student-site fork writes banco2.py; rebuild when it exists
    PRE, FINAL, TEMAS, CLAVES, HAVE_BANK = [], [], {}, {}, False

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docente2')
KATEX = 'inline'
SITE = 'https://deeplearningweek1.vercel.app/'
W2 = SITE + 'semana2/'
B, A, T, I, P = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--ink)', 'var(--purple)'
SL = {s['id']: s['n'] for s in json.loads((OUT / 'slides' / 'slides.json').read_text())}
# week 1 lives at the repo root: <repo>/docencia/slides/slides.json (used by the recap notes)
_W1 = OUT.parent.parent / 'docencia' / 'slides' / 'slides.json'
SL1 = {s['id']: s['n'] for s in json.loads(_W1.read_text())} if _W1.exists() else {}
MISSING = set()


def L(i):
    if i not in SL:
        MISSING.add(i)
        return '?'
    return SL[i]


def R(a, b):
    return f'{L(a)}–{L(b)}'


def W1(*ids):
    """Week-1 slide numbers with a link to that slide of the week-1 deck."""
    out = [f'<a href="../../docencia/slides/index.html#{i}">{SL1.get(i, "?")}</a>' for i in ids]
    return ('lámina ' if len(out) == 1 else 'láminas ') + ', '.join(out)


def G1(anchor, label):
    """Link to a section of the week-1 study guide."""
    return f'<a href="../../guia/index.html#{anchor}">{label}</a>'


def qa(q, a):
    return f'<details class="qa" data-search><summary>{q}</summary><div>{a}</div></details>'


def table(head, rows):
    h = ''.join(f'<th>{x}</th>' for x in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table><tr>{h}</tr>{r}</table>'


def qcol(tema):
    if not HAVE_BANK:
        return '—'
    pre = [str(i + 1) + ('*' if q.get('clave') else '') for i, q in enumerate(PRE) if q.get('tema') == tema]
    fin = [str(i + 1) + ('*' if q.get('clave') else '') for i, q in enumerate(FINAL) if q.get('tema') == tema]
    parts = ([('bases ' if tema == 'pre' else 'pre ') + ', '.join(pre)] if pre else []) + (['final ' + ', '.join(fin)] if fin else [])
    return ' · '.join(parts) or '—'


S = []

# ------------------------------------------------------------------ 0 · how to use
S.append(('uso', '★', 'Cómo usar esta guía', f"""
<div class="hero"><span class="chip">Solo docente</span>
<h1 style="margin-top:14px">Guía docente y apuntes · Semana 2</h1>
<p>Arquitecturas para problemas complejos: cómo mira una red una imagen (CNN), cómo lee una secuencia (RNN y LSTM), qué cambió con la atención y los Transformers, y cómo elegir la arquitectura. Aquí está el orden de todo, el plan por temas (con sus puntos de corte), los apuntes con el rigor que hay detrás de cada lámina, las preguntas que te pueden hacer y las claves de los notebooks y los quizzes.</p>
<p style="font-size:15px">Sesiones por Teams: viernes 6 y sábado 7 de noviembre de 2026. Las láminas son una sola secuencia por temas: cada sesión empieza donde terminó la anterior.</p></div>
<div class="grid">
<div class="tile"><h4>Antes de la semana</h4><p>Lee <a href="#orden">El orden de todo</a> y haz el <a href="#checklist">checklist</a>. Recorre las <a href="slides/index.html">slides</a> con la tecla <b>P</b> para ver tus notas.</p></div>
<div class="tile"><h4>Para preparar un tema</h4><p>Abre su <a href="mapas/index.html">mapa conceptual</a> (qué decir, ejemplo, pregunta y error frecuente por concepto) y luego sus apuntes: <a href="#b00">recorderis</a>, <a href="#b01">Tema 1</a>, <a href="#b02">Tema 2</a>, <a href="#b04">cierre</a>.</p></div>
<div class="tile"><h4>En clase</h4><p>El <a href="#plan">plan por temas</a> y su recuadro <b>Si vas atrasado</b>: dónde cortar sin dejar ideas a medias, qué mandar a la casa y cómo retomar. El plan usa unas 5 de las 6 horas: el colchón es para preguntas, no para más contenido.</p></div>
<div class="tile"><h4>Después</h4><p>Las <a href="#notebooks">claves de los notebooks</a>, la <a href="#lectura">lectura de tendencia</a> para el video de conclusiones y la <a href="#quizzes">clave de los quizzes</a>.</p></div>
</div>
<h3>El hilo de la semana en una frase</h3>
{idea('Cada arquitectura es una suposición sobre cómo están organizados los datos. La densa supone «todo con todo»; la CNN, «lo cercano importa y el mismo patrón puede estar en cualquier parte»; la RNN, «el orden importa»; la atención deja que cada elemento mire directamente a todos los demás, a un precio que crece con el cuadrado de la longitud.')}
<p>Primero, un <b>recorderis de la semana 1</b>: lo nuevo se cuelga de lo que ya saben. Pregunta del <b>Tema 1</b>: <b>¿cómo mira una red una imagen?</b> Pregunta del <b>Tema 2</b>: <b>¿cómo lee una red una secuencia y qué hace cuando la secuencia es muy larga?</b> Las dos preguntas se cierran con la lectura de tendencia: las redes recurrentes vuelven, mezcladas con atención.</p>
<h3>Dónde está cada cosa en el repositorio</h3>
<pre><code>deepLearningWeek1/                ← el mismo repo público y el mismo sitio de Vercel
├── index.html ... docencia/        la semana 1, sin cambios (los QR ya impresos siguen sirviendo)
└── semana2/
    ├── index.html                  inicio de la semana 2 (con el selector Semana 1 · Semana 2)
    ├── proyectos/                  NB03 (Tema 1) y NB04 (Tema 2), completos y ejecutados
    ├── guia/                       guía de estudio
    ├── quiz/                       pre-quiz y quiz final
    ├── material/                   la lectura de tendencia (PDF)
    └── docencia/                   lo tuyo
        ├── index.html              tu panel
        ├── slides/                 las {len(SL)} slides interactivas (notas con la tecla P)
        ├── mapas/                  mapas conceptuales para enseñar (se imprimen en A4)
        ├── Guia_docente.html       esta guía
        ├── Slides_Semana2.pdf      las slides en PDF, de respaldo
        ├── Resultados_quiz.html    pegas los códigos del chat y ves el antes y el después
        └── codigo_fuente/          el código que genera las slides, los mapas y el sitio

Soluciones_privadas/              ← solo en tu computador y tu Drive: nunca al repo
    codigo_notebooks/               los generadores de NB03 y NB04</code></pre>
"""))

# ------------------------------------------------------------------ publish
S.append(('publicar', '0', 'Publicar la semana 2 (5 minutos)', f"""
{idea('La semana 2 vive en la carpeta semana2/ del mismo repositorio. Vercel ya está conectado: al subir los cambios a GitHub, el sitio se republica solo en segundos.')}
<ol>
<li>En tu carpeta <code>deepLearningWeek1</code> (Git Bash): <code>git add -A</code> → <code>git commit -m "Semana 2"</code> → <code>git push</code>. No hagas <code>git pull</code> desde otra copia: traería la historia vieja.</li>
<li>Abre <a href="{W2}">{W2}</a>: debe aparecer el inicio de la semana 2, con el selector <b>Semana 1 · Semana 2</b> arriba. Tu panel está en <a href="{W2}docencia/">{W2}docencia/</a>.</li>
<li><b>Los notebooks cambiaron de nombre</b> (ya no dicen viernes ni sábado): <code>NB03_viernes_tu_primera_cnn.ipynb</code> → <code>NB03_tu_primera_cnn.ipynb</code> y <code>NB04_sabado_redes_que_recuerdan.ipynb</code> → <code>NB04_redes_que_recuerdan.ipynb</code>. Los archivos viejos <b>desaparecen</b> del repo con el próximo push (<code>git add -A</code> registra el borrado). Los enlaces cortos <code>?nb03</code> y <code>?nb04</code> y los QR de las láminas siguen funcionando; si alguien guardó el enlace viejo de Colab, que entre de nuevo desde la página de la semana.</li>
<li>Los enlaces cortos de esta semana pasan por la raíz del sitio: <code>?nb03</code>, <code>?nb04</code>, <code>?pre2</code>, <code>?final2</code>, <code>?guia2</code>, <code>?slides2</code>. Los de la semana 1 (<code>?nb01</code>, <code>?pre</code>…) siguen funcionando.</li>
</ol>
<h3>Comprueba</h3>
<ul>
<li>Escanea con el celular los QR de las láminas {L('prequiz2')} (pre-quiz), {L('practica-nb03')} (NB03), {L('practica-nb04')} (NB04) y {L('quizfinal2')} (quiz final).</li>
<li>Abre <a href="{W2}docencia/slides/">las slides</a>: pulsa <b>P</b> y se abre tu vista del presentador.</li>
<li>En el repo no hay generadores de notebooks: viven en <code>Soluciones_privadas</code>.</li>
</ul>
"""))

# ------------------------------------------------------------------ order
S.append(('orden', '1', 'El orden de todo: cómo se conecta la semana', f"""
{idea('Cada bloque de láminas tiene su sección del notebook, su mapa conceptual y sus preguntas en el quiz. Si un estudiante falla una pregunta, sabes a qué lámina y a qué celda mandarlo.')}
{table(['Momento', 'Qué pasa', 'Material'], [
    ['Antes de la semana', 'Publica en Canvas el enlace de la semana 2 y la lectura de tendencia «¿El regreso de las redes recurrentes?». Pide que la lean antes de la segunda parte del Tema 2 (la atención).', f'<a href="{W2}">Página de la semana 2</a> · <a href="../material/Lectura_tendencia_Semana2.pdf">lectura (PDF)</a>'],
    ['Encuadre', f'La semana en dos temas, pre-quiz y las 5 ideas clave (láminas {R("portada2", "metas2")})', f'<a href="{W2}quiz/?pre">Pre-quiz</a> (QR en la lámina {L("prequiz2")})'],
    ['00 · Recorderis', f'La semana 1 en una sola red, tres preguntas para calentar y Keras en 4 pasos con las lunas, lo que quedó pendiente (láminas {R("b00", "nb02-casa")})', 'NB02 partes E y F, para la casa'],
    ['Tema 1 · Imágenes', f'Cómo mira una red una imagen: de la densa a la CNN (láminas {R("b01", "cierre-tema1")})', f'NB03 en clase (lámina {L("practica-nb03")}) y el duelo densa contra CNN ({L("duelo")})'],
    ['Tema 2 · Secuencias', f'Cómo lee una red una secuencia: RNN, el olvido y la LSTM (láminas {R("b02", "examen-memoria")})', f'NB04 en clase (lámina {L("practica-nb04")}) y el examen de memoria ({L("examen-memoria")})'],
    ['Tema 2 · La atención', f'Atención, Transformers y la tendencia de los híbridos (láminas {R("b03", "contrapeso")})', 'Debate de la lectura de tendencia'],
    ['Cierre', f'Elegir la arquitectura, la actividad «tu proyecto», quiz final y lo que viene (láminas {R("b04", "recursos2")})', f'<a href="{W2}quiz/?final">Quiz final</a> · <a href="#quizzes">Resultados</a>'],
    ['Después', 'Repaso con las slides y la guía de estudio; video de conclusiones de la lectura con los resultados de la encuesta; entrega de la semana en Canvas', 'Guía de estudio · slides · Canvas'],
])}
<h3>Parte por parte</h3>
{table(['Parte', 'Láminas', 'Notebook', 'Quiz'], [
    ['Encuadre', R('portada2', 'metas2'), '—', qcol('pre')],
    ['00 · Recorderis de la semana 1 y Keras', R('b00', 'nb02-casa'), 'NB02 E–F (casa)', qcol('b00')],
    ['Tema 1 · Imágenes y CNN', R('b01', 'cierre-tema1'), 'NB03 §0–6 · Experimento 3', qcol('b01')],
    ['Tema 2 · Secuencias, RNN y LSTM', R('b02', 'examen-memoria'), 'NB04 §0–3', qcol('b02')],
    ['Tema 2 · Atención y Transformers', R('b03', 'contrapeso'), 'NB04 §4–5 · Experimento 4', qcol('b03')],
    ['Cierre · Elegir la arquitectura', R('b04', 'recursos2'), '—', qcol('b04')],
])}
<p class="note">{'* = idea clave: aparece en los dos quizzes para medir el avance.' if HAVE_BANK else 'La columna Quiz se llena al reconstruir esta guía cuando exista el banco de preguntas (banco2.py).'}</p>
<p>Los dos notebooks son <b>prácticas en clase, sin nota</b>: el NB03 cierra el Tema 1 y el NB04 está en el centro del Tema 2. Todo el código ya viene escrito y explicado; se leen, se ejecutan, se predice antes de ejecutar y se responden las preguntas <b>Para pensar</b> (respuesta plegada). Los experimentos 3 y 4 son opcionales.</p>
"""))

# ------------------------------------------------------------------ checklist
S.append(('checklist', '2', 'Checklist antes de clase', f"""
<h3>Una vez (antes de la primera sesión)</h3>
<ul>
<li><a href="#publicar">Publicar la semana 2</a> y probar los QR desde tu celular (láminas {L('prequiz2')}, {L('practica-nb03')}, {L('practica-nb04')}, {L('quizfinal2')} y {L('recursos2')}).</li>
<li>Abrir NB03 y NB04 desde la página y hacer <b>Entorno de ejecución → Ejecutar todo</b>: cada uno termina en unos 2 minutos con la CPU gratuita de Colab, sin errores. (La GPU es opcional: <b>Entorno de ejecución → Cambiar tipo de entorno</b>.)</li>
<li>Recorrer las slides con la vista del presentador (<b>P</b>) y probar las demos de las láminas {L('recorderis')} (el recorderis), {L('keras-fit2')} (las lunas), {L('filtro')} (la lupa), {L('mapas')} (los filtros aprendidos), {L('orden')}, {L('libreta')}, {L('olvido')}, {L('atencion')} y {L('costo')}.</li>
<li>Publicar en Canvas el enlace de la semana 2 y la lectura de tendencia.</li>
<li>Preparar las salas de grupos en Teams para la actividad de la lámina {L('tu-proyecto')} (los mismos grupos del proyecto de titulación).</li>
<li>Jugar tú el pre-quiz y abrir <code>Resultados_quiz.html</code> → <b>Ver un ejemplo</b>.</li>
</ul>
<h3>Cada sesión, 15 minutos antes</h3>
<ul>
<li>Teams con el correo institucional; iniciar la grabación y verificar que graba.</li>
<li>Slides en el navegador con <b>F</b> y la vista del presentador (<b>P</b>) en la segunda pantalla. Comparte <b>la ventana de las slides</b>.</li>
<li>El notebook del tema que toca (NB03 o NB04) abierto en otra pestaña y ya ejecutado una vez, para mostrar resultados aunque la conexión falle.</li>
<li>Anota en qué lámina terminaste la sesión anterior: la siguiente empieza ahí (si es el Tema 2, con la lámina {L('repaso-tema1')}).</li>
<li>El enlace de la página listo para pegar en el chat: <code>{W2}</code>.</li>
<li>Al terminar: «Finalizar reunión para todos», para que la grabación se cierre bien.</li>
</ul>
"""))

# ------------------------------------------------------------------ plans
PLAN = [
    ['Encuadre', R('portada2', 'metas2'), '≈ 10 min', 'La semana en dos temas; pre-quiz jugado (6 min); las 5 ideas clave', '¿Qué pregunta les pareció más difícil?'],
    ['00 · Recorderis de la semana 1', R('b00', 'recorderis-preguntas'), '≈ 12 min', 'La semana 1 en una sola red, un eslabón por clic con su analogía; las tres preguntas para calentar', '¿Qué hace una neurona con sus datos?'],
    ['00 · Keras en 4 pasos', R('motor-volante', 'nb02-casa'), '≈ 13 min', 'El motor y el volante; los 4 pasos con las lunas (337 parámetros, 95 %); la red aprendiendo en vivo; NB02 E y F para la casa', '¿En qué línea está la retropropagación?'],
    ['Tema 1 · la idea', R('b01', 'softmax'), '≈ 45 min', 'Una foto son 784 números; la densa aplana y no sabe quién es vecino; cada arquitectura es una suposición; la lupa de 3 × 3 (+0.99 en el borde); los filtros aprendidos; compartir pesos (160 frente a 100 480); pooling; la CNN en Keras; softmax', 'Si mezclamos los píxeles, ¿a la red densa le importa?'],
    ['Tema 1 · práctica NB03', str(L('practica-nb03')), '35 min', 'Colab funcionando en todos; prioridad §0, §2, §3 y §5; el resto queda para la casa', '¿Por qué la densa cae al mover la prenda 2 píxeles?'],
    ['Tema 1 · lo que vimos', R('duelo', 'cierre-tema1'), '≈ 15 min', '12 810 frente a 101 770 parámetros; 87.7 % frente a 86.7 %; mover 2 px: 75.2 % frente a 56.5 %; mezclar: la densa igual, la CNN baja; LeNet, AlexNet y Smith et al. (2023); las tres ideas del tema', 'Del 1 al 5, ¿podrían explicar qué hace un filtro?'],
    ['Tema 2 · secuencias y RNN', R('b02', 'rnn-keras'), '≈ 35 min', 'El Tema 1 en tres ideas (puente); datos en orden; el orden importa (48 % frente a 100 %); la libreta (0.76, 0.36, 0.18, 0.09); desenrollar; el olvido (0.5¹⁰ ≈ 0.001); la LSTM y sus compuertas; las secuencias en Keras', 'Si el modelo solo ve el promedio, ¿puede saber si el socio empeora?'],
    ['Tema 2 · práctica NB04', str(L('practica-nb04')), '40 min', 'Parejas o salas de 3; prioridad §1, §2, §3 y §4', '¿Qué cambia entre 30 y 80 pasos?'],
    ['Tema 2 · el examen de memoria', str(L('examen-memoria')), '≈ 5 min', '10 y 30 pasos: aprueban todos; 80 pasos: SimpleRNN 52 %, LSTM 50 %, atención 100 % con 82 parámetros', '¿Qué hizo distinto la atención?'],
    ['Tema 2 · la atención', R('b03', 'contrapeso'), '≈ 40 min', 'La fila que no se paraleliza; cada palabra mira a todas («él» → «socio», 79 %); consulta, claves y valores; lo que miró la red (90 % en el paso marcado); el precio n²; el Transformer; los híbridos; el contrapeso y el debate de la lectura (10 min)', '¿Eficiencia o capacidad?'],
    ['Cierre · elegir y tu proyecto', R('b04', 'tu-proyecto'), '≈ 30 min', '¿Qué arquitectura le pondrías? (los casos se revelan uno a uno); tres preguntas; la actividad en salas (20 min) con la plantilla en el chat', '¿Qué suposición hace su arquitectura sobre sus datos?'],
    ['Cierre · quiz final y lo que viene', R('quizfinal2', 'recursos2'), '≈ 13 min', 'Todos jugaron y pegaron su código; el mapa de la semana; la semana 3 (robustez, transfer learning y explicabilidad)', 'Del 1 al 5, ¿podrían elegir la arquitectura de su proyecto?'],
]
S.append(('plan', '3', 'Plan por temas (no por días)', f"""
{idea('La semana es una sola secuencia de láminas en cinco partes: encuadre, recorderis, Tema 1, Tema 2 y cierre. Cada sesión empieza donde terminó la anterior. El plan suma unas 5 horas de las 6 disponibles: el colchón es para preguntas, no para más contenido.')}
{table(['Parte', 'Láminas', 'Duración sugerida', 'Qué debe quedar', 'Pregunta para lanzar'], PLAN)}
{box('ojo', 'Si vas atrasado', f"""<p><b>Puntos de corte naturales.</b> Corta en uno de estos tres lugares y ninguna idea queda a medias:</p>
<ul>
<li>después de la lámina <b>{L('cierre-tema1')}</b>: el Tema 1 completo (CNN y NB03);</li>
<li>después de la lámina <b>{L('examen-memoria')}</b>: la RNN, la LSTM y el examen de memoria cerrados;</li>
<li>después de la lámina <b>{L('contrapeso')}</b>: la atención y la tendencia cerradas; solo falta el cierre.</li>
</ul>
<p><b>Para la casa, sin perder nada:</b> el NB02 partes E y F (Keras con XOR y las lunas), la §6 del NB03 (¿en qué se equivoca?) y la §5 del NB04 (la atención a mano, que también está en la lámina {L('atencion-cuenta')}).</p>
<p><b>Para retomar en otra sesión:</b> si cortaste al final del Tema 1, empieza con la sección del Tema 2 y la lámina <b>{L('repaso-tema1')}</b> (el Tema 1 en tres ideas, 5 minutos). Si cortaste dentro del Tema 2, abre con la lámina {L('examen-memoria')} como resumen y sigue en la {L('b03')}.</p>
<p><b>Se pueden decir en un minuto:</b> pooling ({L('pooling')}), softmax ({L('softmax')}), la historia de las CNN ({L('historia-cnn')}) y el Transformer ({L('transformer')}). En el recorderis, si las tres preguntas salen bien, pasa rápido por la cadena.</p>
<p><b>No recortes:</b> las dos prácticas ({L('practica-nb03')} y {L('practica-nb04')}) y la actividad «tu proyecto» ({L('tu-proyecto')}), que conecta la semana con la entrega. Si el quiz final no cabe, deja el enlace <code>…/semana2/quiz/?final</code> en el chat y pide el código.</p>""")}
"""))

# ------------------------------------------------------------------ notes per block
def bloque(sid, n, title, esencial, rigor, explicar, preguntas, errores):
    inner = (idea(esencial) + '<h3>Con más rigor (para ti)</h3>' + rigor +
             '<h3>Cómo explicarlo</h3>' + explicar +
             '<h3>Preguntas que te pueden hacer</h3>' + ''.join(qa(q, a) for q, a in preguntas) +
             box('error', 'Errores típicos de los estudiantes', '<ul>' + ''.join(f'<li>{e}</li>' for e in errores) + '</ul>'))
    part = {'00': 'Recorderis', '01': 'Tema 1', '02': 'Tema 2', '03': 'Tema 2 · segunda parte', '04': 'Cierre'}.get(n, n)
    return (sid, n, title, inner, chip(f'Apuntes · {part}'))


AP = []
RECAP = [
    ['Datos en una tabla', 'Cada fila es un ejemplo, cada columna una característica y la etiqueta es la respuesta que queremos aprender.', 'El comité de crédito: los datos de cada socio y si pagó.', W1('palabras'), G1('b01', 'Guía 01')],
    ['Neurona: z = w·x + b', 'Multiplica cada dato por su peso, suma todo y añade el sesgo: un puntaje.', 'Tu nota final del curso: cada nota por lo que pesa, menos la exigencia. El socio A: z = 2.81.', W1('nota', 'comite'), G1('b02', 'Guía 02')],
    ['Activación', 'Convierte el puntaje en la salida y dobla la línea para que la red aprenda curvas.', 'Interruptor (escalón), regulador de luz (sigmoide: una probabilidad) y válvula (ReLU).', W1('activacion', 'doblar'), G1('b02', 'Guía 02')],
    ['Red en capas', 'Una neurona traza una sola línea; con capas, cada neurona traza la suya y la salida las combina.', 'XOR, la luz de la escalera: ninguna línea la separa; dos neuronas sí.', W1('xor', 'xor-resuelto'), G1('b03', 'Guía 03') + ' · ' + G1('b05', '05')],
    ['Error y pérdida', 'Error = real − predicho, uno por caso; la pérdida resume todos en un solo número: más pequeño es mejor.', 'Las casas de Quito (MSE = 132.25); el meteorólogo «seguro» que falla, castigado por la BCE.', W1('error', 'perdida', 'bce'), G1('b04', 'Guía 04')],
    ['Descenso de gradiente', 'La pendiente dice hacia dónde sube la pérdida; damos el paso al revés. η es el largo del paso.', 'Bajar el Cotopaxi con neblina, tanteando con el pie; la ducha: si giras la llave de golpe, te quemas.', W1('cotopaxi', 'pendiente', 'eta'), G1('b04', 'Guía 04')],
    ['Retropropagación', 'Reparte la culpa del error hacia atrás, capa por capa, multiplicando efectos.', 'Los engranajes: si A mueve a B tres veces y B a C dos veces, A mueve a C seis veces.', W1('culpa', 'engranajes'), G1('b06', 'Guía 06')],
    ['Keras', 'Construir, compilar, entrenar y predecir; TensorFlow hace la retropropagación por dentro.', 'El motor y el volante; las piezas de LEGO.', W1('keras'), G1('b08', 'Guía 08')],
    ['Métricas', 'Si los casos que buscamos son pocos, la exactitud engaña: mira la matriz de confusión.', 'Decir «al día» a todos acierta 87 % y no encuentra ningún moroso.', W1('trampa87', 'confusion'), G1('b09', 'Guía 09')],
]
WARM = [
    ['1 · ¿Qué hace una neurona con sus datos?', 'Multiplica cada dato por su peso, suma todo y añade el sesgo; la activación decide.', f"Repite el ejemplo de la nota final en 3 minutos ({W1('nota')} de la semana 1) y manda a la {G1('b02', 'sección 02 de la guía de la semana 1')}."],
    ['2 · Si la pendiente de un peso es +4, ¿el peso sube o baja?', 'Baja: se camina en contra de la pendiente. Con η = 0.1 y el peso en 2: 2 − 0.1 · 4 = 1.6.', f"Vuelve al Cotopaxi ({W1('cotopaxi', 'pendiente')} de la semana 1) y a la {G1('b04', 'sección 04 de la guía')}."],
    ['3 · Un modelo dice «al día» a todos y acierta 87 %: ¿es bueno?', 'No: no encuentra a ningún moroso. Hay que mirar la matriz de confusión, el recall y la precisión.', f"Muestra la matriz 10/3/8/79 ({W1('confusion')} de la semana 1) y manda a la {G1('b09', 'sección 09 de la guía')}."],
]
AP.append(bloque('b00', '00', 'Recorderis de la semana 1 y Keras en 4 pasos',
    'El recorderis no es repetir la semana 1: es poner en una sola cadena lo que ya saben para que lo nuevo se cuelgue de ahí. Una CNN y una RNN siguen siendo neuronas con pesos, una pérdida y descenso de gradiente; lo único que cambia es cómo se conectan las neuronas, es decir, la suposición sobre los datos. Keras, lo que quedó pendiente, es el código de esa cadena: Sequential define la arquitectura, compile fija optimizador, pérdida y métricas, fit repite adelante–atrás–actualizar, y predict/evaluate solo usan lo aprendido.',
    '<pre><code>for epoch in range(epochs):\n    for X_b, y_b in batches(X_tr, y_tr, batch_size):\n        with tf.GradientTape() as tape:\n            loss = loss_fn(y_b, model(X_b, training=True))\n        grads = tape.gradient(loss, model.trainable_variables)\n        optimizer.apply_gradients(zip(grads, model.trainable_variables))\n    # then: validation metrics, callbacks (EarlyStopping, ...)</code></pre>'
    '<p>Eso es <code>fit()</code> por dentro: exactamente la retropropagación de la semana 1, que TensorFlow calcula solo. <b>Las cuentas de las lunas:</b> 600 puntos → 120 de prueba y 480 para estudiar; <code>validation_split=0.2</code> separa 96 (las <b>últimas</b> filas, antes de barajar) y quedan 384 de entrenamiento: 384 / 32 = 12 pasos por época × 60 épocas = 720 pasos. Parámetros: 2·16 + 16 = 48; 16·16 + 16 = 272; 16·1 + 1 = 17; total 337.</p>'
    '<p><b>Por qué abrir con esto.</b> El NB03 y el NB04 usan los mismos cuatro pasos; solo cambian las capas (<code>Conv2D</code>, <code>SimpleRNN</code>, <code>LSTM</code>) y, en el NB03, la salida (softmax con 10 clases). Si los cuatro pasos quedan claros al terminar el recorderis, el resto de la semana se lee igual.</p>',
    f"<h4>La cadena de la semana 1 (lámina {L('recorderis')}, un eslabón por clic, unos 8 minutos)</h4>"
    + table(['Eslabón', 'Qué decir (una frase)', 'La analogía de la semana 1', 'Dónde estaba (semana 1)', 'Para repasar'], RECAP)
    + f"<p>Ve rápido: es memoria, no clase nueva. Pregunta antes de revelar cada eslabón («¿qué venía después de la neurona?») y deja que lo digan ellos. Cierra con la frase de la lámina: «hasta ahora los datos eran tablas; ¿y si son fotos? ¿y si son frases?».</p>"
    + f"<h4>Tres preguntas para calentar (lámina {L('recorderis-preguntas')}, unos 4 minutos)</h4>"
    + "<p>Lanza cada pregunta, pide la respuesta en el chat (una letra o un número) y revela. Son preguntas del quiz de la semana 1: sirven de termómetro.</p>"
    + table(['Pregunta', 'Respuesta', 'Si más de un tercio falla'], WARM)
    + "<p>Si fallan las tres, no sigas de largo: dedica 10 minutos a la cadena con calma y deja el NB02 para la casa. Es mejor llegar más tarde al Tema 1 que construir CNN sobre una neurona que no se entiende.</p>"
    + f"<h4>Keras en 4 pasos (unos 13 minutos)</h4><p>Sin cuentas. El motor y el volante (lámina {L('motor-volante')}): TensorFlow hace las cuentas, Keras es lo que manejas. Los cuatro pasos (lámina {L('keras-4pasos')}): un clic por paso, cada uno con su línea de código. La red aprendiendo en vivo (lámina {L('keras-fit2')}): pulsa entrenar y comenta cómo se dobla la frontera mientras bajan juntas las dos curvas (entrenamiento y simulacro). Cierra con el NB02 para la casa (lámina {L('nb02-casa')}): partes E (XOR con 33 parámetros) y F (las lunas). El puente al Tema 1: «las lunas son una tabla de 2 columnas; ¿y si la entrada es una foto de 28 × 28?».</p>",
    [('¿Qué diferencia hay entre loss y metrics?', 'La pérdida es lo que se optimiza (debe ser derivable). Las métricas solo se reportan (accuracy, AUC); no guían el gradiente.'),
     ('¿Por qué validation_split?', 'Para mirar en cada época cómo le va a la red con datos que no usa para aprender: es el simulacro. Detecta sobreajuste y sirve para elegir épocas y arquitectura. Ojo: toma las últimas filas antes de barajar; si los datos vienen ordenados por clase, hay que barajarlos antes.'),
     ('¿Keras o PyTorch?', 'Las ideas son idénticas. Keras 3 puede correr sobre TensorFlow, JAX o PyTorch; en el curso usamos TensorFlow, que viene en Colab. Si un grupo domina PyTorch, puede usarlo en su proyecto.'),
     ('¿Por qué repasar la semana 1 si vamos atrasados?', 'Porque la semana 2 no trae una teoría nueva de aprendizaje: la CNN y la RNN aprenden igual que la red de las lunas (pérdida, gradiente, retropropagación). Lo único nuevo es cómo se conectan las neuronas. Diez minutos de recorderis ahorran media hora de dudas en el NB03.'),
     ('Me sale un error de shapes, ¿qué reviso?', 'Que <code>Input(shape=...)</code> coincida con la forma de cada ejemplo: (2,) en las lunas, (28, 28, 1) en Fashion-MNIST, (12, 1) en el historial del NB04.')],
    ['Creer que la CNN o la RNN aprenden «distinto»: aprenden igual, con pérdida y gradiente.', 'Sumar la pendiente en vez de restarla.', 'Creer que <code>compile</code> entrena.', 'Olvidar <code>keras.Input</code> o poner mal su shape.', 'Leer solo la última época sin mirar las curvas.']))

AP.append(bloque('b01', '01', 'Cómo mira una red una imagen: CNN',
    'Una capa convolucional aplica el mismo filtro pequeño en todas las posiciones: pesos compartidos, equivarianza a la traslación y muchísimos menos parámetros. El pooling resume y da una tolerancia pequeña a los corrimientos.',
    formula(r'(I \star K)(i,j) = \sum_{m=0}^{k-1}\sum_{n=0}^{k-1} I(i+m,\,j+n)\,K(m,n) + b',
            [(r'I', 'la imagen (o el mapa anterior)', B), (r'K', 'el filtro de k × k: se aprende', A), (r'b', 'el sesgo del filtro', I)],
            '<p>En deep learning se le dice «convolución», pero es una <b>correlación cruzada</b>: el filtro no se voltea. Como el filtro se aprende, da igual.</p>',
            'cada número del mapa es la ventana de la imagen multiplicada casilla por casilla por el filtro, todo sumado, más el sesgo.') +
    formula(r'o = \left\lfloor \frac{n + 2p - k}{s} \right\rfloor + 1 \qquad \#\text{param}_{\text{conv}} = k \cdot k \cdot c_{in} \cdot c_{out} + c_{out}',
            [(r'n', 'tamaño de entrada (28)', B), (r'k', 'tamaño del filtro (3)', A), (r'p', 'relleno (padding: 0 en el curso)', I), (r's', 'paso (stride: 1)', I)],
            read='con 28 píxeles, filtro de 3, sin relleno y paso 1 salen 26; con <code>padding="same"</code> saldrían 28.') +
    '<p><b>Las cuentas del NB03.</b> Formas: 28×28×1 → Conv2D(16, 3) 26×26×16 → MaxPooling2D(2) 13×13×16 → Conv2D(32, 3) 11×11×32 → MaxPooling2D(2) 5×5×32 (⌊11/2⌋ = 5) → Flatten 800 → Dense(10). '
    'Parámetros: 3·3·1·16 + 16 = <b>160</b>; 3·3·16·32 + 32 = <b>4 640</b>; 800·10 + 10 = <b>8 010</b>; total <b>12 810</b>. La densa: 784·128 + 128 = <b>100 480</b> y 128·10 + 10 = 1 290; total <b>101 770</b> (≈ 8 veces más). Con imágenes a color hay 3 canales y un filtro de 3 × 3 tiene 27 pesos.</p>'
    '<p><b>Campo receptivo.</b> Una neurona de la primera capa mira 3 × 3 píxeles; después del pooling, 4 × 4; en la segunda convolución, 8 × 8; después del segundo pooling, 10 × 10. Así se construye la jerarquía: bordes → partes → prenda.</p>'
    '<p><b>Equivarianza e invariancia.</b> La convolución es <i>equivariante</i> a la traslación: si mueves la prenda, el mapa se mueve igual. El pooling agrega una <i>invariancia</i> local pequeña. Pero el <code>Flatten</code> + <code>Dense</code> final vuelve a depender de la posición: por eso con 1–2 píxeles la CNN aguanta (84.4 % y 75.2 %) y con 4 píxeles también se cae (28.2 %). Se arregla con aumento de datos o con <i>global average pooling</i> (semana 3, robustez).</p>'
    '<p><b>Por qué mezclar píxeles no le importa a la densa.</b> Una permutación fija de las entradas es una simetría exacta de la familia de redes densas: la red con los pesos permutados del mismo modo calcula lo mismo, y la inicialización es igual en distribución. Por eso 87.2 % frente a 86.7 % es solo ruido. La CNN baja a 85.2 % porque su suposición (vecindad) se rompe.</p>'
    + formula(r'p_k = \frac{e^{z_k}}{\sum_{j=1}^{10} e^{z_j}} \qquad \ell = -\log p_{y}',
              [(r'z_k', 'el puntaje de la clase k', B), (r'p_k', 'su probabilidad: suman 1', A)],
              '<p>Es la pérdida <code>sparse_categorical_crossentropy</code> (las etiquetas son enteros 0–9). Adivinar al azar da 10 % de exactitud y una pérdida inicial cercana a ln 10 ≈ 2.30. Con 2 clases, softmax equivale a la sigmoide de la semana 1.</p>',
              'cada puntaje se vuelve positivo con la exponencial y se divide entre la suma: diez probabilidades que suman 1.'),
    f"<p>Parte de la necesidad (lámina {L('imagen-numeros')}): una foto son 784 números entre 0 y 255; pasa el mouse por el botín. Luego la densa que aplana ({L('aplanar')}): pregunta qué pasa si mezclamos los píxeles y deja la respuesta en suspenso hasta el duelo. La idea clave 1 ({L('suposicion')}): lupa y libreta, como en la lectura. La lupa ({L('filtro')}): deja que el filtro recorra el botín y cambia de filtro; la cuenta con números ({L('filtro-cuenta')}): +0.99 en el borde. Los filtros que aprendió la red ({L('mapas')}): «nadie se los enseñó». Compartir pesos ({L('compartir')}): 160 frente a 100 480. Pooling ({L('pooling')}), la CNN en Keras ({L('cnn-keras')}, un clic por línea) y softmax ({L('softmax')}). Después la práctica ({L('practica-nb03')}) y el duelo con los resultados ({L('duelo')}). Cierra con la historia ({L('historia-cnn')}): LeNet leyendo cheques, AlexNet en 2012 y la moraleja de Smith et al. (2023): comparar con justicia.</p>",
    [('¿Por qué filtros de 3 × 3 y no más grandes?', 'Dos capas de 3 × 3 ven lo mismo que una de 5 × 5 (campo receptivo 5) con menos parámetros (2·9 = 18 frente a 25 por canal) y con una no linealidad más en el medio. Es la lección de VGG (2014); por eso 3 × 3 es el estándar.'),
     ('¿Qué son el stride y el padding?', 'El stride es cuántos píxeles salta la lupa entre posiciones (1 en el curso; 2 reduce el mapa a la mitad). El padding rellena el borde con ceros para que el mapa conserve el tamaño (<code>padding="same"</code>) y para que los bordes de la foto también se miren con la ventana completa.'),
     ('¿Las CNN sirven para algo que no sean fotos?', 'Sí, para cualquier dato donde lo cercano importa: audio (espectrogramas), series de tiempo con <code>Conv1D</code>, texto (n-gramas), imágenes médicas o satelitales. La suposición es la misma: patrones locales que pueden aparecer en cualquier parte.'),
     ('¿Qué es un Vision Transformer (ViT)?', 'Corta la imagen en parches de 16 × 16, trata cada parche como una «palabra» y usa atención (Dosovitskiy et al., 2021). Supone menos que la CNN y por eso necesita más datos. Smith et al. (2023) mostraron que, con el mismo cómputo, las CNN empatan con los ViT en ImageNet.'),
     ('¿Necesito GPU para el NB03?', 'No: con la CPU gratuita de Colab entrena las dos redes en unos 2 minutos. Con GPU es más rápido; para imágenes grandes o propias del proyecto, sí conviene activarla.'),
     ('¿Cuántos filtros pongo?', 'Lo deciden la validación y el presupuesto. En el Experimento 3 del NB03: 4 filtros → 2 346 parámetros y 82.8 %; 8 → 5 258 y 86.2 %; 16 → 12 810 y 87.7 %; 32 → 34 826 y 88.1 %. Duplicar de 16 a 32 casi triplica los parámetros por 0.4 puntos.')],
    ['Olvidar el canal: <code>Input(shape=(28, 28, 1))</code>.', 'Usar sigmoide o <code>binary_crossentropy</code> con 10 clases.', 'Confundir el filtro (los pesos) con el mapa (el resultado).', 'Creer que la CNN es inmune a mover la imagen: con 4 píxeles también se cae.', 'Contar los parámetros de un filtro por cada posición.']))

AP.append(bloque('b02', '02', 'Cómo lee una red una secuencia: RNN y LSTM',
    'Una RNN aplica la misma celda en cada paso y lleva un estado de tamaño fijo. Entrenarla es retropropagar a través del tiempo, y el producto de muchos factores hace que la señal de los pasos lejanos se desvanezca (o explote). Las compuertas de la LSTM ayudan, sin magia.',
    formula(r'\mathbf{h}_t = \tanh\!\big(W_x\,\mathbf{x}_t + W_h\,\mathbf{h}_{t-1} + \mathbf{b}\big) \qquad \hat y = \sigma(\mathbf{w}_o^\top \mathbf{h}_T + b_o)',
            [(r'\mathbf{h}_t', 'la libreta después del paso t', A), (r'W_x', 'pesos para lo que llega', B), (r'W_h', 'pesos para lo anotado', B)],
            read='lo que llega ahora más lo que ya estaba anotado, aplastado por tanh; los mismos pesos en todos los pasos.') +
    '<p><b>Parámetros.</b> Con n neuronas y d datos por paso: n·d + n·n + n. SimpleRNN(8) con d = 1: 8 + 64 + 8 = 80, más Dense(1) = 9 → <b>89</b>. SimpleRNN(32) con d = 2: 64 + 1 024 + 32 = 1 120, más 33 → <b>1 153</b>. La LSTM tiene cuatro bloques así: 4 · 1 120 + 33 = <b>4 513</b>. Leer un paso más no agrega parámetros: es la misma celda.</p>'
    + formula(r'\frac{\partial \mathbf{h}_T}{\partial \mathbf{h}_k} = \prod_{t=k+1}^{T} \operatorname{diag}\!\big(1-\mathbf{h}_t^{2}\big)\,W_h \qquad \Big\|\frac{\partial \mathbf{h}_T}{\partial \mathbf{h}_k}\Big\| \le \|W_h\|^{\,T-k}',
              note='<p><b>Retropropagación a través del tiempo (BPTT).</b> Desenrollada, la RNN es una red de T capas con los mismos pesos; la culpa de un paso lejano se multiplica T − k veces. Como tanh\' ≤ 1, si el mayor valor singular de \\(W_h\\) es menor que 1 la culpa se desvanece exponencialmente; si es mayor puede explotar (Bengio, Simard y Frasconi, 1994; Pascanu, Mikolov y Bengio, 2013). Lo de explotar se controla recortando el gradiente (<i>gradient clipping</i>); lo de desvanecer, con compuertas.</p>'
                   '<p><b>El ejemplo de la lámina.</b> Con w = 1, u = 0.5, b = 0 y x = [1, 0, 0, 0]: h₁ = tanh(1) = 0.76; h₂ = tanh(0.38) = 0.36; h₃ = tanh(0.18) = 0.18; h₄ = 0.09. El eco se reduce aproximadamente a la mitad por paso: 0.5¹⁰ ≈ 0.001. Con u = 0.9 queda ≈ 0.19 a los 10 pasos: se apaga más despacio, pero se apaga.</p>') +
    formula(r'\begin{aligned}&\mathbf{f}_t = \sigma(W_f[\mathbf{h}_{t-1},\mathbf{x}_t] + \mathbf{b}_f) &&\text{olvidar}\\ &\mathbf{i}_t = \sigma(W_i[\mathbf{h}_{t-1},\mathbf{x}_t] + \mathbf{b}_i),\ \ \mathbf{g}_t = \tanh(W_g[\mathbf{h}_{t-1},\mathbf{x}_t] + \mathbf{b}_g) &&\text{guardar}\\ &\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \mathbf{g}_t &&\text{la libreta}\\ &\mathbf{o}_t = \sigma(W_o[\mathbf{h}_{t-1},\mathbf{x}_t] + \mathbf{b}_o),\ \ \mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t) &&\text{mostrar}\end{aligned}',
            note='<p><b>Por qué ayuda.</b> En la celda \\(\\mathbf{c}_t\\) lo anotado pasa sumado, multiplicado solo por \\(\\mathbf{f}_t\\): si la red aprende \\(\\mathbf{f}_t \\approx 1\\), la culpa viaja hacia atrás casi intacta (el «carrusel de error constante» de Hochreiter y Schmidhuber, 1997). Keras inicia el sesgo de olvido en 1 (<code>unit_forget_bias=True</code>): al empezar, \\(\\sigma(1) \\approx 0.73\\), así que la LSTM también olvida hasta que aprende a no hacerlo. Eso explica el examen de memoria: con 80 pasos y 10 épocas no le alcanza; con 50 pasos depende de la semilla. La GRU (Cho et al., 2014) usa dos compuertas y unas 3/4 de los parámetros de la LSTM.</p>') +
    '<p><b>Formas en Keras.</b> (ejemplos, pasos, datos por paso): el historial es (2000, 12, 1); el examen de memoria (3000, T, 2), con el valor ±1 y la marca 0/1 en cada paso. La capa recurrente devuelve solo la última libreta (<code>return_sequences=False</code>), que pasa a la salida.</p>',
    f"<p>Parte de la necesidad con datos de su mundo (lámina {L('secuencias')}): texto, voz, ventas diarias, pagos mensuales. El orden importa ({L('orden')}): los mismos 12 meses al revés tienen el mismo promedio; pregunta qué modelo puede distinguirlos antes de mostrar 48 % y 100 %. La libreta ({L('libreta')}): deja que la frase entre palabra por palabra. La cuenta ({L('rnn-cuenta')}): 0.76, 0.36, 0.18, 0.09, en voz alta. Desenrollar ({L('desenrollar')}): «la misma celda en cada paso, como la CNN usa el mismo filtro en cada lugar». El olvido ({L('olvido')}): mueve u y conecta con el teléfono dañado de la semana 1. La LSTM ({L('lstm')}): borrador, lápiz y ventana. Las secuencias en Keras ({L('rnn-keras')}) y la práctica ({L('practica-nb04')}). Al volver, el examen de memoria ({L('examen-memoria')}) abre el bloque 03.</p>",
    [('¿Por qué no usar una red densa con los 12 meses en fila?', 'Para una longitud fija también funciona (la densa ve las posiciones). La RNN aporta dos cosas: acepta secuencias de cualquier largo y comparte los pesos en el tiempo, así que un patrón aprendido en enero sirve en julio. El modelo del promedio del NB04 es otra cosa: ignora el orden a propósito.'),
     ('¿Por qué tanh y no ReLU en la RNN?', 'Porque la libreta se multiplica por los mismos pesos en cada paso: con ReLU (sin techo) puede crecer sin control y explotar. tanh la mantiene entre −1 y 1.'),
     ('¿LSTM o GRU?', 'Rinden parecido en la mayoría de los problemas; la GRU es un poco más liviana. Se decide con validación, con el mismo presupuesto para las dos.'),
     ('¿Para series de tiempo de mi trabajo uso una LSTM?', 'Compárala primero con una línea base sencilla (el último valor, un promedio móvil, un modelo clásico o boosting con rezagos). En pronóstico muchas veces gana lo simple; la LSTM suma cuando hay patrones largos y muchos datos.'),
     ('¿Qué es una RNN bidireccional?', 'Dos libretas: una lee de izquierda a derecha y otra al revés, y se combinan. Sirve cuando tienes la secuencia completa (clasificar un texto), no cuando hay que predecir el futuro paso a paso.'),
     ('Con 50 pasos la LSTM a veces aprende y a veces no: ¿entonces cuál es mejor?', 'Ninguna conclusión sale de una corrida. Con SEED = 7 la LSTM aprende en la época 9; con 2026 se queda en 48 %. Para comparar en serio: varias semillas, el mismo presupuesto y reportar la variación. Es la misma lección de «comparar con justicia».')],
    ['Pasar los datos sin el eje de los pasos: (ejemplos, pasos, datos por paso).', 'Barajar los pasos de una secuencia o resumirla con su promedio.', 'Creer que la LSTM nunca olvida.', 'Confundir «olvidar al leer» con «no poder aprender» (el problema es la culpa que se debilita al entrenar).', 'Sacar conclusiones de una sola semilla.']))

AP.append(bloque('b03', '03', 'Atención, Transformers y la tendencia',
    'La atención calcula, para cada posición, un promedio de todas las demás ponderado por similitud: softmax(QKᵀ/√d)V. Conecta cualquier par de posiciones en un solo paso y se paraleliza, a un costo de n² comparaciones y con una caché que crece con el contexto.',
    formula(r'\operatorname{Atención}(Q,K,V) = \operatorname{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)\,V \qquad Q = XW_Q,\ K = XW_K,\ V = XW_V',
            [(r'Q', 'consultas: qué busca cada palabra', B), (r'K', 'claves: cómo se ofrece cada palabra', A), (r'V', 'valores: lo que aporta', T), (r'\sqrt{d_k}', 'escala para que softmax no se sature', I)],
            read='cada palabra compara su consulta con la clave de todas, convierte los puntajes en pesos que suman 1 y se queda con el promedio ponderado de los valores.') +
    '<p><b>El ejemplo del NB04 a mano.</b> La consulta de «él» da puntajes 3.0 (socio), 0.0 (cuota) y 1.5 (él). Softmax: e³ = 20.09, e⁰ = 1, e¹·⁵ = 4.48, suma 25.57 → <b>78.6 %, 3.9 % y 17.5 %</b>. El nuevo «él» pasa de [0.5, 0.5] (ambiguo) a ≈ [0.87, 0.13]. En un Transformer, W<sub>Q</sub>, W<sub>K</sub> y W<sub>V</sub> se aprenden; varias «cabezas» hacen esto en paralelo con matrices distintas y se concatenan (<i>multi-head</i>).</p>'
    '<p><b>La posición.</b> La atención por sí sola no sabe el orden (es equivariante a permutaciones): hay que sumarle información de posición (codificación sinusoidal, aprendida o rotatoria, RoPE). En la red del NB04, la marca de cada paso cumple ese papel: el puntaje detecta el paso marcado y por eso pone ahí el 90 % del peso.</p>'
    '<p><b>El costo.</b> QKᵀ es una matriz n × n: O(n² d) operaciones y, de forma ingenua, O(n²) memoria (FlashAttention reduce la memoria, no las operaciones). Al generar texto, cada palabra nueva se compara con las n anteriores y se guarda su clave y su valor: la <b>caché KV</b> crece de forma lineal con el contexto (por capa y por cabeza). Con 1 000 tokens son 10⁶ puntajes por capa y cabeza; con un millón, 10¹². Una RNN o un <i>state space model</i> (SSM) cuesta lo mismo por paso y guarda un estado de tamaño fijo.</p>'
    '<p><b>El bloque Transformer</b> (Vaswani et al., 2017): x + Atención(Norm(x)) y luego x + Densa(Norm(x)), con conexiones residuales, repetido decenas de veces. BERT usa el codificador (mira toda la frase); GPT usa el decodificador con máscara causal (cada palabra mira solo hacia atrás) y aprende a predecir la siguiente palabra.</p>'
    '<p><b>La tendencia (lectura).</b> Mamba (Gu y Dao, 2023) es una «libreta» selectiva que se entrena en paralelo; Mamba-2 mostró que estos modelos y la atención son primos matemáticos (Dao y Gu, 2024). Los híbridos conservan pocas capas de atención: Jamba (1 de cada 8), Nemotron-H (≈ 92 % de las capas de atención reemplazadas, hasta 3 veces más rápido), Kimi Linear (75 % menos caché, hasta 6 veces más rápido con un millón de tokens), Qwen3.5 (3 lineales por 1 completa), Nemotron 3 Super (hasta 2.2 veces el rendimiento). El contrapeso: Jelassi et al. (2024) muestran que un estado fijo no puede copiar textos largos con exactitud, y MiniMax (2025) volvió a la atención completa en su modelo M2 por déficits en razonamiento de varios pasos.</p>',
    f"<p>Empieza por la limitación práctica (lámina {L('en-fila')}): la RNN lee en fila y la GPU espera. La idea clave 5 ({L('atencion')}): la frase de la lectura; haz clic en «él» y luego en «su». La cuenta ({L('atencion-cuenta')}) con la biblioteca: consulta, fichas y libros. Lo que miró la red del NB04 ({L('atencion-real')}): «no tuvo que recordar nada: aprendió a quién mirar». El precio ({L('costo')}): mueve el deslizador hasta un millón de tokens. El Transformer en un minuto ({L('transformer')}). Luego la tendencia ({L('hibridos')}) con la analogía del estudiante que toma apuntes y vuelve al libro, y el contrapeso ({L('contrapeso')}), que abre el debate de la lectura (10 minutos, ver la sección <a href=\"#lectura\">Lectura de tendencia</a>).</p>",
    [('¿Qué es un token?', 'El pedazo de texto que el modelo procesa como una unidad: una palabra, parte de una palabra o un signo. En español, una palabra son en promedio algo más de un token. Un «contexto de un millón de tokens» son varios libros.'),
     ('¿Los pesos de atención explican lo que hace el modelo?', 'No del todo. Muestran a qué posiciones mira una capa, pero hay muchas capas y cabezas, y distintos patrones de atención pueden dar la misma respuesta (Jain y Wallace, 2019). Sirven como pista, no como explicación; la explicabilidad es tema de la semana 3.'),
     ('¿Qué es Mamba en palabras simples?', 'Una red recurrente moderna: una libreta de tamaño fijo que decide qué anotar según lo que lee (por eso «selectiva») y que, gracias a su forma matemática, se puede entrenar en paralelo como un Transformer.'),
     ('Entonces, ¿los híbridos son mejores?', 'No hay consenso. Son más baratos al generar textos largos y en muchas pruebas igualan a la atención completa, pero MiniMax encontró déficits en razonamiento complejo a gran escala. La pregunta honesta es: ¿para qué tarea y con qué evaluación?'),
     ('¿ChatGPT entiende lo que dice?', 'Calcula, con atención, qué palabra sigue con mayor probabilidad dado todo lo anterior, entrenado con muchísimo texto. Si eso es «entender» es una discusión abierta; lo seguro es que puede equivocarse con total seguridad, por eso se evalúa.'),
     ('¿Por qué dividir entre √d?', 'Porque el producto punto de vectores de d componentes crece con d; sin la escala, los puntajes serían grandes, softmax se volvería casi un escalón y los gradientes serían diminutos.')],
    ['Creer que la atención es memoria ilimitada y gratis: su costo crece con el cuadrado.', 'Olvidar que la atención sola no sabe el orden.', 'Leer las cifras de velocidad de los híbridos como cifras de calidad.', 'Decir que el modelo «entiende» porque «mira».']))

AP.append(bloque('b04', '04', 'Elegir la arquitectura',
    'La arquitectura es un sesgo inductivo: una suposición sobre la estructura de los datos. Se elige por esa estructura y por el costo, y se valida contra una línea base con una comparación justa.',
    table(['Datos', 'Suposición', 'Arquitectura', 'Simetría que aprovecha'], [
        ['Tabla', 'cualquier columna con cualquier otra', 'Densa (o boosting)', 'ninguna en particular'],
        ['Imagen', 'lo cercano importa; el patrón puede estar en cualquier parte', 'CNN (o ViT con muchos datos)', 'traslación'],
        ['Secuencia', 'el orden importa', 'RNN/LSTM, Transformer o híbrido', 'el tiempo (mismos pesos en cada paso)'],
        ['Grafo', 'las relaciones importan', 'GNN', 'reordenar los nodos no cambia nada'],
        ['Generar datos', 'aprender la distribución', 'GAN, difusión, Transformer generativo', '—'],
    ]) +
    formula(r'\mathbf{h}_v^{\,(l+1)} = \varphi\Big(\mathbf{h}_v^{\,(l)},\ \bigoplus_{u \in \mathcal{N}(v)} \psi\big(\mathbf{h}_u^{\,(l)}, \mathbf{h}_v^{\,(l)}\big)\Big)',
            note='<p><b>Redes neuronales de grafos (GNN).</b> Cada nodo (un socio, una cuenta, un átomo) actualiza su representación con los «mensajes» de sus vecinos; ⊕ es una suma, promedio o máximo, así que el resultado no depende del orden de los vecinos. Apilando capas, cada nodo «ve» a los vecinos de sus vecinos. La GCN de Kipf y Welling (2017) es la versión clásica. Usos: detección de fraude en redes de transacciones, garantes cruzados en una cooperativa, moléculas y fármacos, recomendaciones.</p>') +
    formula(r'\min_G \max_D\ \ \mathbb{E}_{x\sim\text{datos}}\big[\log D(x)\big] + \mathbb{E}_{z}\big[\log\big(1 - D(G(z))\big)\big]',
            note='<p><b>Redes generativas adversarias (GAN).</b> Un generador G convierte ruido en datos falsos y un discriminador D intenta distinguirlos de los reales; entrenan uno contra otro, como un falsificador y un detective, hasta que lo falso parece real (Goodfellow et al., 2014). Son difíciles de entrenar (colapso de modo); hoy los modelos de difusión dominan la generación de imágenes. Abren preguntas éticas (caras falsas, <i>deepfakes</i>) que vuelven en la semana 3.</p>') +
    '<p><b>Comparar con justicia.</b> Mismos datos y misma partición; el mismo presupuesto (épocas o cómputo); los hiperparámetros ajustados para todos, no solo para el modelo favorito; varias semillas y reportar la variación. Smith et al. (2023) y el examen de memoria con 50 pasos son los dos ejemplos de la semana.</p>',
    f"<p>El zoológico (lámina {L('zoologico')}): una tarjeta por tipo de dato, con su suposición; pide ejemplos de su trabajo para cada una. Las tres preguntas ({L('elegir')}): estructura, costo y comparación justa, empezando por una línea base. Luego la actividad ({L('tu-proyecto')}, ver la sección <a href=\"#proyecto\">Tu proyecto</a>) y el quiz final ({L('quizfinal2')}).</p>",
    [('¿Qué es un sesgo inductivo?', 'Lo que el modelo supone antes de ver los datos y que lo hace preferir ciertas soluciones. La CNN supone localidad y traslación; por eso aprende con menos datos en imágenes, y por eso falla cuando la suposición no se cumple (los píxeles mezclados).'),
     ('¿Y si mis datos son tabla + texto + imágenes?', 'Se arma una red con varias ramas (una por tipo de dato) que se juntan antes de la salida; en Keras se hace con la API funcional (<code>keras.Model(entradas, salida)</code>), como el modelo de atención del NB04.'),
     ('¿Cuándo no usar deep learning?', 'Con tablas medianas y columnas ya informativas, un modelo clásico (regresión logística, boosting) suele igualarlo, es más barato y se explica mejor. Siempre compáralo como línea base.'),
     ('¿Tengo que entrenar desde cero?', 'Casi nunca. Lo normal es partir de un modelo preentrenado y ajustarlo (transfer learning, semana 3): una CNN preentrenada en ImageNet para tus imágenes, o un Transformer de lenguaje para tus textos. Latam-GPT, por ejemplo, partió de Llama 3.1.')],
    ['Elegir la arquitectura de moda sin una línea base.', 'Comparar modelos con distinto presupuesto o con una sola semilla.', 'Aplanar un grafo en una tabla y perder los vínculos.', 'Confundir «más parámetros» con «mejor modelo».']))

# ------------------------------------------------------------------ notebooks (keys)
NBK = f"""
{idea('Los notebooks vienen completos y ejecutados: no hay espacios para rellenar. El estudiante lee, apuesta qué saldrá (🔮), ejecuta y compara con «Qué deberías ver»; cada sección cierra con «Para pensar» (respuesta plegada). Lo que cuenta es poder explicar lo que se ve, y eso no se le puede pedir a una IA.')}
<h3>Cómo correr la práctica</h3>
<ul>
<li><b>Dinámica:</b> parejas o salas de 3 en Teams. NB03: 35 minutos (30 en salas y 5 de puesta en común). NB04: 40 minutos (35 y 5).</li>
<li><b>Prioridades:</b> NB03 §0, §2, §3 y §5 (la §1, la §4 y la §6 quedan para la casa si el tiempo aprieta). NB04 §1, §2, §3 y §4 (la §5 se ve en la lámina {L('atencion-cuenta')}).</li>
<li><b>Tiempo de cómputo:</b> el NB03 entrena cuatro redes (densa y CNN, normales y con píxeles mezclados) y tarda unos 2 minutos con la CPU de Colab; el NB04, entre 1 y 2 minutos. Pide que ejecuten primero la celda <b>Configuración</b> y luego <b>Ejecutar todo</b> mientras leen.</li>
<li><b>Los números:</b> salen con <code>SEED = 2026</code>. En Colab pueden variar en el último decimal (por eso el notebook dice «alrededor de»); las conclusiones no cambian.</li>
<li><b>Si algo falla:</b> casi siempre es una celda saltada (<code>NameError</code>): <b>Entorno de ejecución → Ejecutar anteriores</b>. Fashion-MNIST se descarga solo la primera vez (unos 30 MB).</li>
</ul>
<h3>NB03 · Tu primera CNN (Tema 1) · <code>NB03_tu_primera_cnn.ipynb</code></h3>
{table(['Sección', 'Qué deberían ver', 'Pregunta para el grupo'], [
    ['§0 Una imagen es una tabla', '<code>x_train: (60000, 28, 28)</code>; el botín como números: 0 en el fondo, más de 150 en la prenda; después de preparar: (60000, 28, 28, 1) con máximo 1.0', '¿Qué significa cada número de la tabla?'],
    ['§1 La lupa a mano', 'mapas de 26 × 26: el vertical se enciende en los lados del botín y el horizontal arriba y abajo; la ventana de las filas 11–13 y columnas 13–15 da ≈ +0.99', '¿Por qué en el fondo el filtro da 0?'],
    ['§2 La línea base densa', '101 770 parámetros (100 480 en la primera capa); validación ≈ 88 %; examen final ≈ 86.7 %', '¿Dónde están casi todos los parámetros?'],
    ['§3 La CNN', 'formas 26×26×16 → 13×13×16 → 11×11×32 → 5×5×32 → 800 → 10; 12 810 parámetros; examen final ≈ 87.7 %', '¿Por qué 8 veces menos parámetros?'],
    ['§4 Mirar adentro', '16 filtros aprendidos, varios con una mitad roja y otra azul (bordes); la primera camisa: densa ≈ 75 %, CNN ≈ 77 % (camiseta 11 %, suéter 5 %, abrigo 5 %)', '¿Quién le enseñó a la red a detectar bordes?'],
    ['§5 Poner a prueba la suposición', 'mover 2 px: densa 56.5 %, CNN 75.2 %; con 4 px las dos se caen (22 % y 28 %). Píxeles mezclados: densa 87.2 % (igual), CNN 85.2 % (baja)', '¿Por qué a la densa no le importa mezclar los píxeles?'],
    ['§6 ¿En qué se equivoca?', 'camisa tomada por camiseta: 129 de 1 000; camisa es la clase más difícil (63 %); pantalón, bolso, botín y sandalia pasan del 96 %', '¿Una persona distinguiría esas camisas a 28 × 28?'],
    ['Experimento 3', '4 filtros → 2 346 parámetros, 82.8 %; 8 → 5 258, 86.2 %; 32 → 34 826, 88.1 %', '¿Vale la pena triplicar los parámetros por 0.4 puntos?'],
])}
<h3>NB04 · Redes que recuerdan (Tema 2) · <code>NB04_redes_que_recuerdan.ipynb</code></h3>
{table(['Sección', 'Qué deberían ver', 'Pregunta para el grupo'], [
    ['§0 Una secuencia es una tabla con orden', '<code>X: (2000, 12, 1)</code>: 2 000 socios, 12 meses, 1 dato por mes; el promedio de atraso es el mismo en las dos clases (≈ 13.6 días)', 'Si el promedio es igual, ¿qué las distingue?'],
    ['§1 La libreta a mano', 'con u = 0.5: 0.76, 0.36, 0.18, 0.09 y ≈ 0.001 a los 10 pasos; con u = 0.9 queda ≈ 0.19', '¿Qué le pasa a la culpa que viaja hacia atrás?'],
    ['§2 El orden importa', 'modelo del promedio: 25 parámetros, ≈ 48 % (adivina); SimpleRNN(8): 89 parámetros, 100 %', '¿Qué ve la RNN que el promedio no ve?'],
    ['§3 El examen de memoria', '10 y 30 pasos: los tres aprueban (la LSTM llega a 99 % en la época 3, la SimpleRNN en la 6); 80 pasos: SimpleRNN ≈ 52 %, LSTM ≈ 50 %, atención 100 %', '¿Por qué 80 pasos es más difícil que 30?'],
    ['§4 La atención', '82 parámetros; ≈ 90 % del peso en el paso marcado; los 80 pesos suman 1', '¿Tuvo que recordar algo la atención?'],
    ['§5 La atención a mano', 'puntajes 3.0, 0.0 y 1.5 → socio ≈ 79 %, cuota ≈ 4 %, él ≈ 17.5 %; el nuevo «él» ≈ [0.87, 0.13]', '¿Qué hace softmax con los puntajes?'],
    ['Experimento 4 (50 pasos)', 'SEED = 2026: SimpleRNN ≈ 59 %, LSTM ≈ 48 %, atención 100 %; SEED = 7: la LSTM aprende (≈ 100 %, época 9)', '¿Qué conclusión sale de una sola corrida?'],
])}
"""

# ------------------------------------------------------------------ trend reading
LECT = f"""
{idea('La lectura «¿El regreso de las redes recurrentes? Transformers, Mamba y la búsqueda de la arquitectura ideal» cierra el hilo de la semana: cada arquitectura es una apuesta sobre qué estructura tienen los datos y qué recursos tenemos, y la tendencia de 2024–2026 fue mezclar la libreta de las recurrentes con la atención.')}
<h3>La lectura en seis puntos</h3>
<ol>
<li><b>Cada arquitectura es una forma de mirar los datos:</b> densa para tablas, CNN para imágenes («una lupa»), RNN para secuencias («una libreta»).</li>
<li><b>La libreta tiene límites:</b> se olvida (la señal de error se debilita; la LSTM de 1997 lo mitigó) y no se puede paralelizar.</li>
<li><b>La atención (2017)</b> deja que cada palabra mire a todas y se calcula en paralelo; su precio crece con el cuadrado de la longitud y con la caché KV.</li>
<li><b>La tendencia:</b> libretas modernas (Mamba, xLSTM) e híbridos que conservan pocas capas de atención: Jamba (2024), Nemotron-H (2025), Kimi Linear (2025), Qwen3.5 (2026), Nemotron 3 Super (2026).</li>
<li><b>El contrapeso:</b> un estado fijo no puede copiar con exactitud textos largos (Jelassi et al., 2024); MiniMax volvió a la atención completa en M2 (2025); no hay consenso. En visión, CNN y ViT empatan con el mismo cómputo (Smith et al., 2023).</li>
<li><b>Desde América Latina:</b> el desafío es usar modelos a diario con pocas GPU; arquitecturas más eficientes podrían permitir analizar documentos largos en español en hardware asequible, siempre que se comprueben en las tareas reales.</li>
</ol>
<h3>El debate en clase (10 minutos, lámina {L('contrapeso')})</h3>
<p>Elige uno de los cuatro debates abiertos de la lectura (o deja que voten en el chat). Pide una respuesta de una línea por grupo, con un argumento de la semana.</p>
{table(['Debate de la lectura', 'Pregunta para lanzar', 'Lo que debería salir'], [
    ['Eficiencia o capacidad', '¿Vale la pena ganar 2 a 6 veces en velocidad si se arriesga la capacidad de recordar con exactitud y razonar en varios pasos?', 'Depende de la tarea: para resumir documentos largos, sí; para copiar cifras de un contrato o razonar en varios pasos, hay que comprobarlo. El examen de memoria del NB04 es una versión pequeña de este dilema.'],
    ['Arquitectura o escala', 'Si con el mismo cómputo y los mismos datos las arquitecturas bien diseñadas rinden parecido, ¿cuánto debemos preocuparnos por la arquitectura «perfecta»?', 'Smith et al. (2023): CNN = ViT con el mismo presupuesto. Importa elegir una arquitectura cuya suposición encaje con los datos; después pesan más los datos, el cómputo y la evaluación.'],
    ['Benchmarks o uso real', '¿Cómo evaluar un modelo para que las pruebas reflejen las tareas largas y complejas del mundo real?', 'MiniMax: el híbrido igualaba en las pruebas tradicionales y fallaba en tareas largas. Evaluar con tareas parecidas a las reales, con varias semillas y con comparaciones justas.'],
    ['Abierto o cerrado', 'Si no sabemos qué usan los modelos cerrados más potentes, ¿qué tan completo es este debate?', 'Solo conocemos lo que publican los laboratorios abiertos; las conclusiones son provisionales.'],
])}
<h3>Para el video de conclusiones</h3>
<p>Con los resultados de la encuesta de tendencia, un guion de 1 a 3 minutos puede seguir este orden: qué respondió el grupo en el debate más votado; la cifra que más sorprendió (por ejemplo, Kimi Linear: hasta 75 % menos caché); el contrapeso (MiniMax y la copia exacta); y la idea para su proyecto: elegir por la estructura de los datos y comparar con justicia.</p>
<p>La lectura está en <a href="../material/Lectura_tendencia_Semana2.pdf">semana2/material/Lectura_tendencia_Semana2.pdf</a>.</p>
"""

# ------------------------------------------------------------------ project activity
PROY = f"""
{idea('La actividad conecta la semana con el proyecto de titulación: cada grupo decide qué estructura tienen sus datos, qué arquitectura le conviene, qué supone esa arquitectura y contra qué línea base la va a comparar.')}
<h3>Cómo correrla (20 minutos, lámina {L('tu-proyecto')})</h3>
<ol>
<li><b>2 minutos:</b> explica las cuatro preguntas y muestra la plantilla.</li>
<li><b>13 minutos en salas</b> con los grupos del proyecto. Pasa por las salas y pregunta siempre lo mismo: «¿qué supone su arquitectura sobre sus datos?».</li>
<li><b>5 minutos de puesta en común:</b> cada grupo pega su plantilla en el chat; comenta dos o tres en voz alta, sobre todo las que eligieron sin línea base.</li>
</ol>
<h3>La plantilla (para pegar en el chat)</h3>
<pre><code>Grupo: …
1. Nuestros datos son: tabla / imagen / secuencia / texto / grafo (tamaño aproximado: …)
2. Arquitectura candidata: …   Supone que: …
3. Línea base para comparar: …
4. Para que la comparación sea justa vamos a fijar: (datos, partición, épocas, semillas…)</code></pre>
<h3>Qué buscar en las respuestas</h3>
<ul>
<li>Que la suposición encaje con los datos (una CNN para una tabla de socios es una señal de alerta).</li>
<li>Que haya una línea base simple: la red densa de la semana 1 o un modelo clásico.</li>
<li>Que la comparación fije el presupuesto y use más de una semilla.</li>
<li>Si un grupo aún no tiene datos, que elija un dataset público parecido al de su tema.</li>
</ul>
<p>La entrega de la semana (componente práctico del sílabo: modelos CNN y RNN aplicados a tareas de clasificación, sobre el proyecto) sale de esta plantilla.</p>
"""

# ------------------------------------------------------------------ quizzes key
def qrows(bank):
    rows = []
    for i, q in enumerate(bank):
        ok = q.get('ok', 0)
        opts = q.get('options', [])
        rows.append([str(i + 1) + (' *' if q.get('clave') else ''), q.get('q', ''), f"{'ABCD'[ok]} · {opts[ok] if ok < len(opts) else ''}",
                     TEMAS.get(q.get('tema', ''), q.get('tema', '')),
                     (f"Idea clave {q['clave'][1:]} · " if q.get('clave') and not q.get('mide', '').startswith('Idea clave') else '') + q.get('mide', '')])
    return rows


if HAVE_BANK:
    QZ = f"""
{idea('Los quizzes son formativos y miden avance: cinco ideas clave aparecen en los dos con otra versión. El pre-quiz dice de dónde parte el grupo; el quiz final, cuánto se movió en cada idea.')}
<h3>Cómo se usa</h3>
<ol>
<li><b>Al empezar la semana, lámina {L('prequiz2')}:</b> escanean el QR (o abren <a href="{W2}quiz/?pre">el pre-quiz</a>), escriben nombre y apellido y juegan.</li>
<li>Al final la página les da un código para pegar en el chat de Teams.</li>
<li><b>Al cerrar la semana, lámina {L('quizfinal2')}:</b> lo mismo con <a href="{W2}quiz/?final">el quiz final</a>, con el mismo nombre.</li>
<li>Después de clase: copia el chat y pégalo en <a href="Resultados_quiz.html">Resultados_quiz.html</a> → <b>Analizar</b>: promedio de cada quiz, antes y después de cada idea clave y preguntas a reforzar.</li>
</ol>
<p>Para jugarlo proyectado: <a href="{W2}quiz/?clase">modo proyector</a> (sin puntos, con «Mostrar respuesta»).</p>
<h3>Las 5 ideas clave (pre ↔ final)</h3>
{table(['Idea clave', 'Pre-quiz', 'Quiz final'], [[f"{c[1:]}. {CLAVES[c]}", ', '.join(str(i + 1) for i, q in enumerate(PRE) if q.get('clave') == c) or '—', ', '.join(str(i + 1) for i, q in enumerate(FINAL) if q.get('clave') == c) or '—'] for c in CLAVES])}
<h3>Pre-quiz ({len(PRE)} preguntas)</h3>
{table(['#', 'Pregunta', 'Respuesta', 'Tema', 'Qué mide'], qrows(PRE))}
<h3>Quiz final ({len(FINAL)} preguntas)</h3>
{table(['#', 'Pregunta', 'Respuesta', 'Tema', 'Qué mide'], qrows(FINAL))}
<p><b>Cómo leerlo:</b> en las ideas clave esperas un salto claro desde el pre-quiz; una ganancia normalizada de 0.3 a 0.7 es lo habitual. Si una idea sube menos de 20 puntos, retómala en los primeros 10 minutos de la semana 3.</p>
"""
else:
    QZ = f"""
{idea('Los quizzes son formativos y miden avance: cinco ideas clave aparecen en los dos con otra versión.')}
<p>La clave del pre-quiz y del quiz final aparece aquí al reconstruir esta guía cuando exista el banco de preguntas (<code>banco2.py</code>). Mientras tanto: pre-quiz en la lámina {L('prequiz2')} (<a href="{W2}quiz/?pre">enlace</a>), quiz final en la lámina {L('quizfinal2')} (<a href="{W2}quiz/?final">enlace</a>) y resultados en <a href="Resultados_quiz.html">Resultados_quiz.html</a>.</p>
"""

# ------------------------------------------------------------------ FAQ
FAQ = [
    ('¿Por qué Fashion-MNIST y no los dígitos de MNIST?', 'Porque los dígitos ya son demasiado fáciles (una red densa pasa del 97 %) y no se nota la diferencia entre arquitecturas. Con ropa hay clases que se parecen (camisa y camiseta) y la CNN muestra su ventaja en robustez. Tiene la misma forma (28 × 28, 10 clases) y se descarga en una línea.'),
    ('¿Cómo cargo mis propias imágenes para el proyecto?', 'Con carpetas por clase y <code>keras.utils.image_dataset_from_directory("carpeta", image_size=(128, 128))</code>. Para imágenes reales conviene partir de una CNN preentrenada (transfer learning, semana 3) y activar la GPU de Colab.'),
    ('¿Cómo trabajo con textos en español?', 'Se convierten en números con <code>keras.layers.TextVectorization</code> (cada palabra un entero) y una capa <code>Embedding</code> (cada entero un vector que se aprende); después una LSTM o un Transformer. Para proyectos reales, un modelo de lenguaje preentrenado suele rendir mucho más.'),
    ('¿Qué es un embedding?', 'Un vector de números que representa una palabra (o un producto, o un usuario) y que se aprende: palabras que se usan parecido quedan cerca. En la §5 del NB04, «socio», «cuota» y «él» tienen vectores de 2 números hechos a mano para mostrar la idea.'),
    ('¿Las series de tiempo se trabajan con RNN?', 'Pueden. Se arman ventanas: los últimos k pasos como entrada y el siguiente como respuesta, con forma (ejemplos, k, datos por paso). Compáralo siempre con una línea base simple; en pronóstico muchas veces gana lo simple.'),
    ('¿Por qué el notebook dice «alrededor de»?', 'Porque Colab puede usar otro procesador y los cálculos en coma flotante cambian en el último decimal. Con SEED = 2026 las conclusiones son las mismas.'),
    ('¿Las prácticas tienen nota?', 'No. NB03 y NB04 son prácticas en clase ya resueltas y explicadas: se aprenden leyendo, prediciendo y explicando lo que se ve. Lo que se registra son el pre-quiz y el quiz final, y solo para medir el avance.'),
    ('No me corre el notebook en Colab, ¿qué hago?', '1) Entorno de ejecución → Reiniciar y ejecutar todo. 2) Verifica que ejecutaste la celda Configuración. 3) Si dice que no puede descargar Fashion-MNIST, espera un minuto y vuelve a ejecutar. 4) Copia el error en el chat de Teams.'),
    ('¿Qué es un Transformer en una frase?', 'Una pila de bloques de atención y capas densas, con conexiones residuales, que procesa toda la secuencia en paralelo; es la arquitectura de casi todos los modelos de lenguaje actuales.'),
    ('¿Por qué la LSTM perdió con 80 pasos si dicen que recuerda?', 'Porque con 10 épocas no alcanzó a aprender a mantener su compuerta de olvido abierta; con más épocas, otra tasa de aprendizaje u otra semilla puede lograrlo. La atención no necesita aprender eso: mira directo al paso marcado.'),
]

GLOS_D = [
    ('Atención', 'Promedio ponderado de los valores de todas las posiciones; los pesos salen de comparar consultas con claves (softmax(QKᵀ/√d)V).'),
    ('BPTT', 'Retropropagación a través del tiempo: el backward de una RNN desenrollada.'),
    ('Caché KV', 'Las claves y valores de las palabras ya procesadas que un Transformer guarda al generar texto; crece con el contexto.'),
    ('Campo receptivo', 'La región de la imagen original que influye en una neurona; crece con cada capa convolucional y de pooling.'),
    ('Canal', 'La tercera dimensión de una imagen o un mapa: 1 en escala de grises, 3 en color, 16 o 32 después de una capa con esos filtros.'),
    ('Codificación posicional', 'Información de posición que se suma a cada token, porque la atención sola no sabe el orden.'),
    ('Compuerta', 'Una sigmoide entre 0 y 1 que regula cuánto pasa (olvidar, guardar, mostrar en la LSTM).'),
    ('Convolución (en deep learning)', 'Correlación cruzada: el filtro recorre la entrada multiplicando y sumando, sin voltearse.'),
    ('Embedding', 'Vector aprendido que representa un símbolo (una palabra, un producto).'),
    ('Equivarianza a la traslación', 'Si la entrada se mueve, la salida se mueve igual: propiedad de la convolución.'),
    ('Estado oculto', 'La libreta de la RNN: el vector h que resume lo leído.'),
    ('Gradient clipping', 'Recortar la norma del gradiente para evitar que explote en las RNN.'),
    ('Híbrido', 'Modelo que combina capas de atención completa con capas recurrentes o de atención lineal.'),
    ('Mapa de activación', 'La salida de un filtro sobre toda la imagen: dónde encontró su patrón.'),
    ('Mensajes (GNN)', 'La información que cada nodo recibe de sus vecinos para actualizarse.'),
    ('Multi-cabeza', 'Varias atenciones en paralelo, cada una con sus matrices, que se concatenan.'),
    ('Padding', 'Relleno de ceros en el borde para conservar el tamaño del mapa.'),
    ('Pooling', 'Resumir cada ventana (máximo o promedio); reduce el tamaño y tolera corrimientos pequeños.'),
    ('Sesgo inductivo', 'Lo que una arquitectura supone sobre los datos antes de verlos.'),
    ('Softmax', 'Convierte puntajes en probabilidades positivas que suman 1.'),
    ('SSM (state space model)', 'Familia de modelos recurrentes modernos con estado de tamaño fijo que se entrenan en paralelo (Mamba).'),
    ('Stride', 'Cuántas posiciones salta el filtro entre una ventana y la siguiente.'),
    ('Token', 'La unidad de texto que procesa un modelo de lenguaje: una palabra o parte de ella.'),
]

REFS = """
<ul>
<li>Bengio, Y., Simard, P. y Frasconi, P. (1994). Learning long-term dependencies with gradient descent is difficult. <i>IEEE Transactions on Neural Networks, 5</i>(2), 157–166.</li>
<li>Cho, K., van Merriënboer, B., Gulcehre, C., Bahdanau, D., Bougares, F., Schwenk, H. y Bengio, Y. (2014). Learning phrase representations using RNN encoder–decoder for statistical machine translation. En <i>Proceedings of EMNLP 2014</i> (pp. 1724–1734).</li>
<li>Dao, T. y Gu, A. (2024). Transformers are SSMs: Generalized models and efficient algorithms through structured state space duality. En <i>Proceedings of the 41st International Conference on Machine Learning</i> (PMLR 235). https://arxiv.org/abs/2405.21060</li>
<li>Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., … Houlsby, N. (2021). An image is worth 16x16 words: Transformers for image recognition at scale. <i>ICLR 2021</i>.</li>
<li>Elman, J. L. (1990). Finding structure in time. <i>Cognitive Science, 14</i>(2), 179–211.</li>
<li>Fukushima, K. (1980). Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position. <i>Biological Cybernetics, 36</i>(4), 193–202.</li>
<li>Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A. y Bengio, Y. (2014). Generative adversarial nets. En <i>Advances in Neural Information Processing Systems 27</i> (pp. 2672–2680).</li>
<li>Gu, A. y Dao, T. (2023). <i>Mamba: Linear-time sequence modeling with selective state spaces</i> [Preprint]. arXiv. https://arxiv.org/abs/2312.00752</li>
<li>Hochreiter, S. y Schmidhuber, J. (1997). Long short-term memory. <i>Neural Computation, 9</i>(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735</li>
<li>Jain, S. y Wallace, B. C. (2019). Attention is not explanation. En <i>Proceedings of NAACL-HLT 2019</i> (pp. 3543–3556).</li>
<li>Jelassi, S., Brandfonbrener, D., Kakade, S. M. y Malach, E. (2024). Repeat after me: Transformers are better than state space models at copying. En <i>Proceedings of the 41st International Conference on Machine Learning</i> (PMLR 235, pp. 21502–21521).</li>
<li>Kipf, T. N. y Welling, M. (2017). Semi-supervised classification with graph convolutional networks. <i>ICLR 2017</i>.</li>
<li>Krizhevsky, A., Sutskever, I. y Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. En <i>Advances in Neural Information Processing Systems 25</i> (pp. 1097–1105).</li>
<li>LeCun, Y., Bottou, L., Bengio, Y. y Haffner, P. (1998). Gradient-based learning applied to document recognition. <i>Proceedings of the IEEE, 86</i>(11), 2278–2324.</li>
<li>MiniMax. (2025, 30 de octubre). <i>Why did M2 end up as a full attention model?</i> Hugging Face Blog. https://huggingface.co/blog/MiniMax-AI/why-did-m2-end-up-as-a-full-attention-model</li>
<li>Pascanu, R., Mikolov, T. y Bengio, Y. (2013). On the difficulty of training recurrent neural networks. En <i>Proceedings of the 30th International Conference on Machine Learning</i> (PMLR 28, pp. 1310–1318).</li>
<li>Smith, S. L., Brock, A., Berrada, L. y De, S. (2023). <i>ConvNets match vision transformers at scale</i> [Preprint]. arXiv. https://arxiv.org/abs/2310.16764</li>
<li>Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. y Polosukhin, I. (2017). Attention is all you need. En <i>Advances in Neural Information Processing Systems 30</i> (pp. 5998–6008).</li>
<li>Xiao, H., Rasul, K. y Vollgraf, R. (2017). <i>Fashion-MNIST: A novel image dataset for benchmarking machine learning algorithms</i> [Preprint]. arXiv. https://arxiv.org/abs/1708.07747</li>
<li>Zhang, A., Lipton, Z. C., Li, M. y Smola, A. J. (2023). <i>Dive into deep learning</i>. Cambridge University Press. https://d2l.ai (capítulos 7 a 11: CNN, RNN modernas y atención).</li>
</ul>
<p>Las demás referencias de la tendencia (Jamba, Nemotron-H, Kimi Linear, Qwen3.5, Nemotron 3 Super, xLSTM, Latam-GPT) están en la lectura de tendencia.</p>
"""

# ------------------------------------------------------------------ assemble
body, toc = '', []
for sid, n, title, inner in S:
    if sid == 'uso':
        body += f'<section id="uso">{inner}</section>'
    else:
        body += section(sid, chip('Docente', 'amber'), title, inner, 'Revisado')
    toc.append((sid, n, title))
for sid, n, title, inner, kick in AP:
    body += section(sid, kick, title, inner, 'Lo estudié')
    toc.append((sid, n, 'Apuntes · ' + title))
for sid, n, title, inner in [('notebooks', '4', 'Los notebooks: claves y cómo correr la práctica', NBK),
                             ('lectura', '5', 'Lectura de tendencia: resumen y debate', LECT),
                             ('proyecto', '6', 'Actividad «tu proyecto»', PROY),
                             ('quizzes', '7', 'Clave de los quizzes', QZ),
                             ('faq', '8', 'Preguntas generales que te pueden hacer',
                              '<input id="search" class="search" type="search" placeholder="Buscar en las preguntas y el glosario…" aria-label="Buscar">' + ''.join(qa(q, a) for q, a in FAQ)),
                             ('glosario', '9', 'Glosario docente', '<dl class="glos">' + ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS_D) + '</dl><p>El glosario básico de los estudiantes está en la guía de estudio.</p>'),
                             ('refs', '10', 'Referencias', REFS)]:
    body += section(sid, chip('Docente', 'amber'), title, inner, 'Revisado')
    toc.append((sid, n, title))

extra = '<p style="margin:14px 0 0;font-size:14px"><a href="index.html">← Panel del profesor</a><br><a href="../../docencia/Guia_docente.html">Guía docente de la semana 1</a></p>'
html = page('Guía docente y apuntes · Semana 2 · Deep Learning UIDE', 'Material solo para el docente: plan, apuntes con rigor y claves de la semana 2 (CNN, RNN, atención).',
            toc, body, 'dl-uide-w2-docente', extra_toc=extra, katex=KATEX, week=2)
html = html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'Guia_docente.html').write_text(html)
print('docente semana 2 built', len(html) // 1024, 'KB', '| quiz key:', 'yes' if HAVE_BANK else 'pending (no banco2.py)')
if MISSING:
    print('warning: slide ids not in slides.json:', ', '.join(sorted(MISSING)))
