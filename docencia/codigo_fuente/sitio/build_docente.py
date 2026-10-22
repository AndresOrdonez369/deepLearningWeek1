"""Teacher guide and notes (only for the teacher): docencia/Guia_docente.html
usage: python build_docente.py <teacher_folder>"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit import page, section, chip, idea, box, formula
from banco import PRE, FINAL, TEMAS, CLAVES
import json

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docente')
KATEX = 'inline'   # formulas work offline, wherever the file is
PAGES = 'https://deeplearningweek1.vercel.app/'
B, A, T, I = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--ink)'
SL = {s['id']: s['n'] for s in json.loads((OUT / 'slides' / 'slides.json').read_text())}
def L(i): return SL[i]
def R(a, b): return f'{SL[a]}–{SL[b]}'

def qa(q, a):
    return f'<details class="qa" data-search><summary>{q}</summary><div>{a}</div></details>'

def table(head, rows):
    h = ''.join(f'<th>{x}</th>' for x in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table><tr>{h}</tr>{r}</table>'

S = []

# ------------------------------------------------------------------ 0
S.append(('uso', '★', 'Cómo usar esta guía', f"""
<div class="hero"><span class="chip">Solo docente</span>
<h1 style="margin-top:14px">Guía docente y apuntes · Semana 1</h1>
<p>Todo lo que necesitas para dictar, estudiar y anticiparte: el orden de todo, el plan minuto a minuto, los apuntes con el rigor que hay detrás de cada lámina, las preguntas que te pueden hacer (con respuesta) y las claves de las tareas y los quizzes. Los proyectos de la semana son prácticas en clase, sin nota.</p></div>
<div class="grid">
<div class="tile"><h4>Antes de la semana</h4><p>Lee <a href="#orden">El orden de todo</a> y haz el <a href="#checklist">checklist</a>. Recorre las <a href="slides/index.html">slides</a> con la tecla <b>P</b> para ver tus notas.</p></div>
<div class="tile"><h4>Para preparar un bloque</h4><p>Abre su <a href="mapas/index.html">mapa conceptual</a> (qué decir, ejemplo, pregunta y error frecuente por concepto) y luego sus <a href="#b01">apuntes</a>.</p></div>
<div class="tile"><h4>En clase</h4><p>El <a href="#viernes">plan del viernes</a> y el <a href="#sabado">del sábado</a>. Las notas de cada lámina traen el guion y el tiempo sugerido.</p></div>
<div class="tile"><h4>Después</h4><p>Las <a href="#notebooks">claves de los notebooks</a> y la <a href="#quizzes">clave de los quizzes</a> con el panel de resultados.</p></div>
</div>
<h3>Mapa del repositorio deepLearningWeek1</h3>
<pre><code>deepLearningWeek1/              ← repo público en GitHub, publicado en Vercel
├── index.html                    inicio: Pre-quiz · Proyectos · Repasa · Quiz final
├── proyectos/                    NB01 y NB02 (versión estudiante)
├── guia/                         guía de estudio
├── quiz/                         pre-quiz y quiz final (tipo Kahoot)
├── material/                     apuntes y lectura de tendencia (PDF)
└── docencia/                     lo tuyo (público pero sin enlace desde el inicio)
    ├── index.html                tu panel
    ├── slides/                   las {len(SL)} slides interactivas (notas con la tecla P)
    ├── mapas/                    mapas conceptuales para enseñar (se imprimen en A4)
    ├── Guia_docente.html         esta guía
    ├── Slides_Semana1.pdf        las slides en PDF, de respaldo
    ├── Resultados_quiz.html      pegas los códigos del chat y ves el antes y el después
    └── codigo_fuente/            el código que genera todo (para la semana 2)

Soluciones_privadas/            ← SOLO en tu computador y tu Drive: nunca al repo
    NB01 y NB02 resueltos y ejecutados</code></pre>
"""))

# ------------------------------------------------------------------ quiz helpers
def qcol(tema):
    pre = [str(i + 1) + ('*' if 'clave' in q else '') for i, q in enumerate(PRE) if q['tema'] == tema]
    fin = [str(i + 1) + ('*' if 'clave' in q else '') for i, q in enumerate(FINAL) if q['tema'] == tema]
    parts = ([('bases ' if tema == 'pre' else 'pre ') + ', '.join(pre)] if pre else []) + (['final ' + ', '.join(fin)] if fin else [])
    return ' · '.join(parts) or '—'

# ------------------------------------------------------------------ publish
S.append(('publicar', '0', 'Publicar en GitHub y Vercel (10 minutos, una vez)', f"""
{idea('El repositorio deepLearningWeek1 es la página: su raíz es el sitio de los estudiantes y docencia/ es tu panel. Vercel publica el repo con una dirección fija; los QR de las slides apuntan ahí, y Colab abre los notebooks directamente desde GitHub.')}
<ol>
<li><b>GitHub:</b> en <code>AndresOrdonez369/deepLearningWeek1</code> (público, rama <code>main</code>) → <b>uploading an existing file</b> → arrastra <b>el contenido</b> de la carpeta <code>deepLearningWeek1</code> (index.html, README.md, vercel.json y las carpetas proyectos, guia, quiz, material y docencia) → <b>Commit changes</b>.</li>
<li><b>Vercel:</b> <b>Add New → Project</b> → importa <code>deepLearningWeek1</code>. En <i>Project Name</i> escribe <code>deeplearningweek1</code>; <i>Framework Preset</i>: <b>Other</b>; sin comando de build; carpeta raíz <code>./</code> → <b>Deploy</b>.</li>
<li>Abre <a href="{PAGES}">{PAGES}</a>: debe aparecer la página de inicio. Tu panel está en <a href="{PAGES}docencia/">{PAGES}docencia/</a>.</li>
</ol>
<p>Si Vercel te da otra dirección (porque <code>deeplearningweek1</code> ya estaba tomado), los QR de las slides no funcionarán: pásale la dirección nueva a Claude y regenera los QR, o en Vercel → Settings → Domains agrega <code>deeplearningweek1.vercel.app</code> si está libre.</p>
<h3>Comprueba</h3>
<ul>
<li>Escanea el QR de la lámina {L('practica1')}: abre el NB01 en Colab. El de la lámina {L('prequiz')} abre el pre-quiz.</li>
<li>Abre <a href="{PAGES}docencia/slides/">{PAGES}docencia/slides/</a>: pulsa <b>P</b> y se abre tu vista del presentador.</li>
<li>En el repo no aparece ninguna solución: esas viven solo en <code>Soluciones_privadas</code>, en tu computador.</li>
</ul>
<p>Cada vez que subas un cambio a GitHub, Vercel republica solo en segundos. No cambies el nombre del repo durante el curso: cambiarían los enlaces de Colab.</p>
"""))

# ------------------------------------------------------------------ orden
S.append(('orden', '1', 'El orden de todo: cómo se conecta la semana', f"""
{idea('Cada bloque de láminas tiene su sección del notebook, su tema en la guía de estudio, su mapa conceptual y sus preguntas en el quiz. Si un estudiante falla una pregunta, sabes exactamente a qué lámina y a qué celda mandarlo.')}
{table(['Momento', 'Qué pasa', 'Material'], [
    ['Lun 19 – Mié 21', 'Lectura y encuesta de tendencia en Canvas; abre la Clase 1. Comparte la página de la semana.', f'<a href="{PAGES}">Página</a> · lectura · encuesta'],
    ['Vie 23 · 18:00', f'Encuadre y pre-quiz (lámina {L("prequiz")})', f'<a href="{PAGES}quiz/?pre">Pre-quiz</a> (QR en la lámina)'],
    ['Vie 23 · bloques 01–04', f'De la IA a la neurona, el perceptrón, la pérdida y el gradiente (láminas {R("b01", "cierre-viernes")})', f'NB01 en clase (láminas {L("practica1")} y {L("practica2")})'],
    ['Sáb 24 · bloques 05–08', f'Capas, retropropagación, entrenar bien y Keras (láminas {R("portada-sab", "practica3")})', f'NB02 en clase (lámina {L("practica3")})'],
    ['Sáb 24 · bloque 09 y cierre', f'La trampa del 87 %, quiz final y lo que viene (láminas {R("b09", "gracias")})', f'<a href="{PAGES}quiz/?final">Quiz final</a> · <a href="#quizzes">Resultados</a>'],
    ['Dom 25 en adelante', 'Repaso autónomo con las slides y la guía; mini-retos opcionales; test y encuesta de tendencia en Canvas', 'Guía de estudio · slides · Canvas'],
])}
<h3>Bloque por bloque</h3>
{table(['Bloque', 'Láminas', 'Notebook · tareas', 'Guía', 'Quiz'], [
    ['00 Encuadre', R('portada', 'metas'), '—', '<a href="#">inicio</a>', qcol('pre')],
    ['01 IA, ML y DL', R('b01', 'ahora'), '—', 'b01', qcol('b01')],
    ['02 La neurona', R('b02', 'doblar'), 'NB01 §1–2 · T1, T2', 'b02', qcol('b02')],
    ['03 Perceptrón y XOR', R('b03', 'practica1'), 'NB01 §3–5 · T3, T4, T5', 'b03', qcol('b03')],
    ['04 Pérdida y gradiente', R('b04', 'cierre-viernes'), 'NB01 §6–8 · T6, T7, T8 · Mini-reto 1 (opcional)', 'b04', qcol('b04')],
    ['05 Capas', R('portada-sab', 'parametros'), 'NB02 E · TE', 'b05', qcol('b05')],
    ['06 Retropropagación', R('b06', 'tensorflow'), 'NB02 A–D · TA, TB, TC, TD', 'b06', qcol('b06')],
    ['07 Entrenar bien', R('b07', 'receta-arranque'), 'NB02 G · TG', 'b07', qcol('b07')],
    ['08 Keras', R('b08', 'practica3'), 'NB02 F · Mini-reto 2', 'b08', qcol('b08')],
    ['09 ¿El modelo es bueno?', R('b09', 'gracias'), '—', 'b09', qcol('b09')],
])}
<p class="note">* = idea clave: aparece en los dos quizzes para medir el avance.</p>
<p>Los proyectos de la semana son <b>prácticas en clase, sin nota</b>: el <b>NB01</b> el viernes y el <b>NB02</b> el sábado, cada uno con tareas que se corrigen solas. Los <b>mini-retos</b> son el extra: el Mini-reto 1 (diseñar a mano un comité de crédito) queda opcional; el Mini-reto 2 (los círculos con más de 90 %) se intenta en clase.</p>
"""))

# ------------------------------------------------------------------ checklist
S.append(('checklist', '2', 'Checklist antes de clase', f"""
<h3>Una vez (antes del miércoles 21)</h3>
<ul>
<li><a href="#publicar">Publicar en GitHub y Vercel</a> (10 minutos).</li>
<li>Probar los QR desde tu celular (láminas {L('prequiz')}, {L('practica1')}, {L('practica2')}, {L('practica3')}, {L('quizfinal')} y {L('recursos')}): cada uno abre el quiz, el notebook o la guía.</li>
<li>Abrir NB01 y NB02 desde la página y hacer <b>Ejecutar todo</b>: deben terminar sin errores (las tareas muestran ⏳).</li>
<li>Recorrer las slides con la vista del presentador (<b>P</b>) y probar las demos de las láminas {L('linea')}, {L('entrenar')}, {L('juega')} y {L('trampa87')}.</li>
<li>Publicar en Canvas el enlace de la página, la lectura y la encuesta de tendencia.</li>
<li>Jugar tú el pre-quiz y abrir <code>docencia/Resultados_quiz.html</code> → <b>Ver un ejemplo</b>, para saber qué verás después.</li>
</ul>
<h3>Cada sesión, 15 minutos antes</h3>
<ul>
<li>Entrar a Teams con el correo institucional; iniciar la grabación y verificar que está grabando.</li>
<li>Slides en el navegador con <b>F</b> (pantalla completa) y la vista del presentador (<b>P</b>) en tu segunda pantalla. En Teams, comparte <b>la ventana de las slides</b>.</li>
<li>NB01 (viernes) o NB02 (sábado) abiertos en otra pestaña; la solución, solo en tu pantalla privada.</li>
<li>Tener el enlace de la página listo para pegar en el chat.</li>
<li>Al terminar: «Finalizar reunión para todos», para que la grabación se cierre bien.</li>
</ul>
"""))

# ------------------------------------------------------------------ plans
VIE = [
    ['18:00–18:10', 'Encuadre y pre-quiz', R('portada', 'metas'), 'Grabación verificada; la ruta; pre-quiz jugado; las 5 ideas clave', '¿Qué pregunta les pareció más difícil?'],
    ['18:10–18:25', '01 · IA, ML y DL', R('b01', 'ahora'), 'IA ⊃ ML ⊃ DL; reglas vs. ejemplos; por qué ahora (puente a la lectura)', '¿Qué problema de su trabajo se resuelve con reglas escritas a mano?'],
    ['18:25–18:45', '02 · La neurona', R('b02', 'doblar'), 'z = 2.81 a mano; la línea con deslizadores; activaciones; sin activación no hay curvas', 'Si el comité se vuelve más exigente, ¿qué número cambia?'],
    ['18:45–19:00', '03 · Cómo aprende', R('b03', 'xor'), 'Ciclo; regla; −0.30 → +2.70; míralo aprender; XOR imposible', '¿Alguien logra separar XOR con una línea?'],
    ['19:00–19:20', 'Práctica en clase · NB01 §1–5', str(L('practica1')), 'Colab funcionando en todos; T1–T5', '¿Por qué el perceptrón no aprende XOR?'],
    ['19:20–19:45', '04 · Error y gradiente', R('b04', 'receta'), 'MSE, BCE, el Cotopaxi, la pendiente, los pasos, η', 'Pendiente +4: ¿el peso sube o baja?'],
    ['19:45–19:55', 'Práctica en clase · NB01 §6–8', str(L('practica2')), 'T6–T7 en clase; T8 y Mini-reto 1 opcionales', '¿Qué pasa con η = 1.1?'],
    ['19:55–20:00', 'Lectura y cierre', R('tendencia1', 'cierre-viernes'), 'La pregunta de la lectura; las tres ideas del día', 'Del 1 al 5, ¿podrían explicar el descenso de gradiente?'],
]
SAB = [
    ['08:00–08:15', 'Apertura y repaso', R('portada-sab', 'repaso'), 'El viernes explicado por ellos', '¿Qué problema nos quedó pendiente?'],
    ['08:15–08:55', '05 · De una neurona a una red', R('b05', 'parametros'), 'Capas; XOR con dos neuronas; pistas; juega con 1 a 8 neuronas; parámetros', '¿Por qué 1 neurona no pasa del 60 % en los círculos?'],
    ['08:55–09:40', '06 · Retropropagación', R('b06', 'tensorflow'), 'Forward 2-2-1; la culpa; engranajes; backward; un paso 56 % → 65 %; GradientTape', 'Si la culpa de un peso es negativa, ¿sube o baja?'],
    ['09:40–09:55', 'Pausa', '—', '—', '—'],
    ['09:55–10:30', '07 · Entrenar bien', R('b07', 'receta-arranque'), 'La culpa que se apaga; clones; lotes; carrera de optimizadores y debate de la lectura (8 min)', '¿Mejor algoritmo o más cómputo?'],
    ['10:30–10:45', '08 · Keras', R('b08', 'keras'), 'Construir, compilar, entrenar', '¿Qué hace fit() por dentro?'],
    ['10:45–11:30', 'Práctica en clase · NB02', str(L('practica3')), 'Parejas o salas de 3; A, B, E y F con el Mini-reto 2; sin nota', '¿Qué red más pequeña pasa el 90 %?'],
    ['11:30–11:45', '09 · ¿El modelo es bueno?', R('b09', 'metricas'), 'La trampa del 87 %; mover el umbral; recall, precisión y AUC', '¿Qué es peor: una falsa alarma o un moroso no visto?'],
    ['11:45–11:55', 'Quiz final', str(L('quizfinal')), 'Todos jugaron y pegaron su código', '¿Qué pregunta les costó más?'],
    ['11:55–12:00', 'Cierre', R('mapa-semana', 'gracias'), 'El mapa de la semana; semanas 2 y 3 (lecturas); guía de estudio', 'Del 1 al 5, ¿podrían explicar cómo aprende una red?'],
]
S.append(('viernes', '3', 'Plan del viernes 23 · 18:00–20:00', f"""
{idea('Objetivo del viernes: que todos salgan sabiendo qué calcula una neurona, por qué una sola no resuelve XOR y qué hace el descenso de gradiente, con Colab funcionando.')}
{table(['Hora', 'Bloque', 'Láminas', 'Qué debe quedar', 'Pregunta para lanzar'], VIE)}
{box('ojo', 'Si el tiempo aprieta', f'<p>Recorta las láminas {L("gato")} (el gato) y {L("ahora")} (por qué ahora) a un minuto cada una; deja la T8 y el Mini-reto 1 como práctica opcional. <b>Nunca recortes la práctica de la lámina {L("practica1")}</b>: es donde todos dejan Colab funcionando.</p>')}
"""))
S.append(('sabado', '4', 'Plan del sábado 24 · 08:00–12:00', f"""
{idea(f'Objetivo del sábado: que todos entrenen su primera red en Keras y entiendan por qué la exactitud puede engañar. El ejemplo 2-2-1 con números (láminas {R("adelante", "actualizar")}) es el corazón teórico.')}
{table(['Hora', 'Bloque', 'Láminas', 'Qué debe quedar', 'Pregunta para lanzar'], SAB)}
{box('ojo', 'Si el tiempo aprieta', f'<p>Acorta el debate del bloque 07 (déjalo en el chat). En el NB02 la prioridad es A, B, E y F; C, D y G quedan como práctica opcional. Si el quiz final no cabe, déjalo con el enlace <code>…/?final</code> y pide el código en el chat.</p>')}
"""))

# ------------------------------------------------------------------ apuntes por bloque
def bloque(sid, n, title, esencial, rigor, explicar, preguntas, errores):
    inner = (idea(esencial) + '<h3>Con más rigor (para ti)</h3>' + rigor +
             '<h3>Cómo explicarlo</h3>' + explicar +
             '<h3>Preguntas que te pueden hacer</h3>' + ''.join(qa(q, a) for q, a in preguntas) +
             box('error', 'Errores típicos de los estudiantes', '<ul>' + ''.join(f'<li>{e}</li>' for e in errores) + '</ul>'))
    day = 'Viernes' if n in ('01', '02', '03', '04') else 'Sábado'
    return (sid, n, title, inner, chip(f'Apuntes · {day} · bloque {n}'))

AP = []
AP.append(bloque('b01', '01', 'IA, machine learning y deep learning',
    'El ML aprende una función a partir de ejemplos; el DL es ML con redes de muchas capas que aprenden sus propias representaciones.',
    formula(r'\hat\theta = \arg\min_\theta \frac{1}{N}\sum_{i=1}^N \ell\big(f_\theta(\mathbf{x}_i),\, y_i\big)',
            [(r'f_\theta', 'el modelo con parámetros θ', B), (r'\ell', 'la pérdida por ejemplo', A), ('N', 'ejemplos de entrenamiento', I)],
            '<p>Todo el curso es esta línea: elegir \\(f_\\theta\\) (arquitectura), \\(\\ell\\) (pérdida) y cómo minimizar (optimizador). La diferencia del DL es que \\(f_\\theta\\) es una composición de muchas capas que aprende las características, en lugar de recibirlas hechas (<i>feature engineering</i>).</p>'),
    f"<p>Abre con la pregunta «¿cuántas veces usaron IA hoy?». Los tres círculos (lámina {L('circulos')}) se revelan uno por clic; luego reglas vs. ejemplos ({L('reglas')}) con el spam, el juego de las reglas del gato ({L('gato')}), los usos cotidianos ({L('usos')}) y la línea de tiempo ({L('ahora')}), que termina en la pregunta de la lectura de tendencia. Cierra con honestidad: en datos de tabla, compara siempre con una línea base.</p>",
    [('¿Un modelo de lenguaje como ChatGPT es deep learning?', 'Sí. Es una red neuronal muy profunda (un <i>Transformer</i>) con cientos de miles de millones de parámetros, entrenada con la misma receta que veremos: pérdida, gradientes y un optimizador de la familia de Adam. Los Transformers se ven en la semana 2.'),
     ('¿Las redes neuronales funcionan como el cerebro?', 'Solo como inspiración. Una neurona artificial es una suma ponderada y una función; no hay química, tiempo ni aprendizaje local como en las sinapsis. Decir que «piensa» es una metáfora.'),
     ('¿Por qué no usar siempre deep learning?', 'Porque en datos de tabla medianos un modelo clásico (regresión logística, árboles con boosting) suele igualarlo o superarlo, es más barato y más fácil de explicar. El DL brilla cuando hay que aprender la representación: imágenes, texto, audio.'),
     ('¿Qué diferencia hay entre IA generativa y lo que vemos?', 'La de esta semana es discriminativa: predice una etiqueta (paga o no). La generativa aprende a producir datos nuevos (texto, imágenes). Las piezas (neuronas, pérdida, gradiente) son las mismas.')],
    ['Creer que toda IA aprende de datos (los sistemas de reglas también son IA).', 'Confundir «más datos» con «mejor modelo» sin una línea base.']))

AP.append(bloque('b02', '02', 'La neurona artificial',
    'z = w·x + b es un puntaje lineal; la activación lo convierte en decisión o probabilidad; geométricamente, la neurona es un hiperplano.',
    formula(r'z = \mathbf{w}^\top\mathbf{x} + b,\qquad \sigma(z) = \frac{1}{1+e^{-z}},\qquad \sigma\'(z) = \sigma(z)\,(1-\sigma(z)) \le \tfrac14') +
    '<p><b>Geometría.</b> El conjunto \\(\\{\\mathbf{x} : \\mathbf{w}^\\top\\mathbf{x} + b = 0\\}\\) es un hiperplano; \\(\\mathbf{w}\\) es perpendicular a él y la distancia con signo de un punto es \\((\\mathbf{w}^\\top\\mathbf{x}+b)/\\|\\mathbf{w}\\|\\). Multiplicar \\((\\mathbf{w}, b)\\) por una constante positiva no cambia la frontera, solo la «seguridad» del puntaje.</p>'
    '<p><b>Sin activación no hay profundidad.</b> \\(W_2(W_1\\mathbf{x}+\\mathbf{b}_1)+\\mathbf{b}_2 = (W_2W_1)\\mathbf{x} + (W_2\\mathbf{b}_1+\\mathbf{b}_2)\\): cualquier pila de capas lineales es una sola capa lineal.</p>'
    '<p><b>La sigmoide como probabilidad.</b> Con salida sigmoide y BCE, el modelo es exactamente una regresión logística: \\(\\log\\frac{p}{1-p} = z\\). Por eso «una neurona sigmoide = regresión logística».</p>',
    f"<p>Secuencia: el comité (lámina {L('comite')}), con la neurona que se arma por pasos; la cuenta con barras ({L('cuenta')}) en voz alta; la línea ({L('linea')}): empieza mal a propósito y pide valores por el chat; las tres activaciones con el mismo z ({L('activacion')}); la sigmoide ({L('sigmoide')}); y los dobleces ({L('doblar')}): primero «Sin activación», luego 2, 4 y 8 neuronas.</p>",
    [('¿Por qué el sesgo se llama sesgo si no es un sesgo estadístico?', 'Es un nombre heredado (<i>bias</i>): es el intercepto de la recta. Desplaza la frontera sin girarla. Equivale a un peso cuya entrada vale siempre 1.'),
     ('¿Cómo se eligen los pesos iniciales?', 'Al azar, con una escala que depende del tamaño de la capa (Glorot o He, bloque 07). Nunca todos iguales: las neuronas quedarían idénticas.'),
     ('¿Por qué ReLU en capas ocultas y sigmoide en la salida?', 'ReLU no satura para z > 0 (pendiente 1), así el gradiente fluye bien entre capas. En la salida necesitamos un número entre 0 y 1 para leerlo como probabilidad: ahí va la sigmoide.'),
     ('¿Qué significa un peso negativo?', 'Que ese dato resta puntaje. En el ejemplo, más atrasos bajan la probabilidad de aprobar. Con datos escalados, el signo y el tamaño del peso dan una idea de la importancia (con cuidado si las variables están correlacionadas).'),
     ('¿Por qué escalar los datos?', 'Si el ingreso va de 0 a 3 000 y los atrasos de 0 a 4, los pesos tendrían escalas muy distintas y el gradiente se movería mal. Escalar (media 0, desviación 1) pone todo en rangos comparables.')],
    ['Olvidar el sesgo b.', 'Confundir z con la salida.', 'Leer la sigmoide como «certeza»: es una probabilidad del modelo, que puede estar mal calibrada.']))

AP.append(bloque('b03', '03', 'El perceptrón y XOR',
    'El perceptrón corrige solo los errores: w ← w + η·y·x. Converge si los datos son linealmente separables y falla en XOR porque no lo son.',
    formula(r'\text{si } y_i(\mathbf{w}^\top\mathbf{x}_i + b) \le 0:\quad \mathbf{w} \leftarrow \mathbf{w} + \eta\,y_i\mathbf{x}_i,\ \ b \leftarrow b + \eta\,y_i') +
    '<p><b>Por qué la regla mejora.</b> Tras la corrección, \\(y_i\\,\\mathbf{w}\'^\\top\\tilde{\\mathbf{x}}_i = y_i\\,\\mathbf{w}^\\top\\tilde{\\mathbf{x}}_i + \\eta\\|\\tilde{\\mathbf{x}}_i\\|^2\\): el margen de ese ejemplo sube (aunque puede no bastar en un paso, como en la T3).</p>'
    '<p><b>Teorema de Novikoff (1962).</b> Si existe \\(\\mathbf{w}^*\\) unitario con \\(y_i\\,\\mathbf{w}^{*\\top}\\tilde{\\mathbf{x}}_i \\ge \\gamma > 0\\) y \\(\\|\\tilde{\\mathbf{x}}_i\\| \\le R\\), el número de correcciones es \\(k \\le (R/\\gamma)^2\\). Prueba en dos líneas: cada corrección aumenta \\(\\mathbf{w}_k^\\top\\mathbf{w}^*\\) en al menos \\(\\gamma\\) (así \\(\\ge k\\gamma\\)) y \\(\\|\\mathbf{w}_k\\|^2\\) en a lo sumo \\(R^2\\) (así \\(\\le kR^2\\)); por Cauchy–Schwarz \\(k\\gamma \\le \\sqrt{k}R\\).</p>'
    '<p><b>XOR no es separable.</b> Con salida 1 si \\(z\\ge0\\): (0,0)→0 exige \\(b<0\\); (0,1)→1 exige \\(w_2+b\\ge0\\); (1,0)→1 exige \\(w_1+b\\ge0\\). Sumando, \\(w_1+w_2+2b\\ge0\\), luego \\(w_1+w_2+b \\ge -b > 0\\); pero (1,1)→0 exige \\(w_1+w_2+b<0\\). Contradicción.</p>',
    f"<p>El ciclo con el locro (lámina {L('ciclo')}); la regla leída como frase ({L('regla')}); la corrección con números ({L('correccion')}); «míralo aprender» ({L('entrenar')}): al avanzar arranca sola; XOR con la luz de la escalera ({L('xor')}): pide a alguien que arrastre la línea y luego «Probar 1 000 líneas». Después, la práctica en clase ({L('practica1')}).</p>",
    [('Si el perceptrón garantiza encontrar la línea, ¿por qué no lo usamos más?', 'Porque solo garantiza algo cuando los datos son separables, cosa rara en la vida real; con ruido oscila sin converger. Además no da probabilidades. La versión «pocket» guarda el mejor w visto.'),
     ('¿Qué pasó históricamente con XOR?', 'Minsky y Papert (1969) formalizaron los límites del perceptrón de una capa; contribuyó al primer «invierno» de las redes. Ya se sabía que con capas ocultas se resolvía; faltaba un algoritmo eficiente para entrenarlas: la retropropagación (Rumelhart, Hinton y Williams, 1986).'),
     ('¿El orden de los datos importa en el perceptrón?', 'Sí, cambia el camino y la solución final (no la garantía). Por eso se barajan los datos en cada época.'),
     ('¿XOR existe en problemas reales?', 'Sí, como interacciones: «el garante reduce el riesgo solo si la cuota es baja», o dos medicamentos que solo juntos causan un efecto. Un modelo lineal sin la variable de interacción no las captura.')],
    ['Aplicar la regla aunque la neurona acierte.', 'Olvidar que con y = −1 la regla resta.', 'Creer que más épocas resuelven XOR.']))

AP.append(bloque('b04', '04', 'Pérdida y descenso de gradiente',
    'La BCE es la log-verosimilitud negativa de una Bernoulli; con sigmoide su gradiente es ŷ − y. El descenso de gradiente da pasos contra la pendiente y η decide si converge.',
    formula(r'\ell = -\big[y\log\hat y + (1-y)\log(1-\hat y)\big],\quad \hat y = \sigma(z)\ \Rightarrow\ \frac{\partial \ell}{\partial z} = \hat y - y') +
    '<p><b>Derivación.</b> \\(\\partial\\ell/\\partial\\hat y = -y/\\hat y + (1-y)/(1-\\hat y)\\) y \\(\\partial\\hat y/\\partial z = \\hat y(1-\\hat y)\\); al multiplicar se cancela todo y queda \\(\\hat y - y\\).</p>'
    '<p><b>Por qué no MSE para clasificar.</b> Con MSE, \\(\\partial\\ell/\\partial z = (\\hat y - y)\\,\\sigma\'(z)\\): si la neurona está saturada y equivocada (\\(z=-6\\), \\(y=1\\)), \\(\\sigma\'\\approx0.0025\\) y casi no aprende; con BCE el gradiente es ≈ −1.</p>'
    '<p><b>Cuándo converge η en la parábola del NB01.</b> Con \\(L=(w-3)^2\\): \\(w_{t+1}-3 = (1-2\\eta)(w_t-3)\\). Converge si \\(|1-2\\eta|<1\\), es decir \\(0<\\eta<1\\); con \\(\\eta=0.5\\) llega en un paso; con \\(\\eta>1\\) diverge. En general, en una cuadrática con curvatura máxima \\(\\lambda_{\\max}\\), hace falta \\(\\eta < 2/\\lambda_{\\max}\\).</p>'
    '<p><b>Por qué el gradiente.</b> Por Taylor, \\(L(\\mathbf{w}+\\Delta) \\approx L(\\mathbf{w}) + \\nabla L^\\top\\Delta\\); entre todas las direcciones de igual largo, \\(-\\nabla L\\) es la que más baja la pérdida.</p>',
    f"<p>La pérdida como «nota al revés» con las casas (lámina {L('perdida')}); la BCE con el meteorólogo ({L('bce')}): prueba los tres botones; el Cotopaxi ({L('cotopaxi')}), un clic por paso; la pendiente ({L('pendiente')}): arrastra el punto a ambos lados del mínimo e insiste en el signo menos; la tabla de cuatro pasos ({L('pasos')}); los tres η ({L('eta')}); la receta ({L('receta')}).</p>",
    [('¿Por qué se usa el logaritmo en la BCE?', 'Porque maximizar la probabilidad de los datos (un producto) equivale a minimizar la suma de −log; convierte productos en sumas y castiga fuertemente las probabilidades cercanas a 0 asignadas a lo que sí pasó.'),
     ('¿Qué es una época y qué es una iteración?', 'Una iteración es un paso (un lote). Una época es pasar por todos los datos una vez: N ÷ batch_size iteraciones.'),
     ('¿El descenso de gradiente siempre encuentra el mínimo global?', 'En una parábola sí. En redes, la pérdida no es convexa: puede llegar a mínimos locales o mesetas. En redes grandes muchos mínimos son igual de buenos; el ruido de los mini-lotes ayuda a escapar de puntos silla.'),
     ('¿Cómo elijo η en la práctica?', 'Empieza con el valor por defecto de Adam (0.001). Si la pérdida no baja, súbelo ×3; si salta o da NaN, bájalo ÷10. Hay técnicas más finas (búsqueda de learning rate, schedules) para las semanas siguientes.'),
     ('¿Por qué MSE eleva al cuadrado y no usa el valor absoluto?', 'Ambas son válidas (MAE es la del valor absoluto). El cuadrado es derivable en todas partes y castiga más los errores grandes; MAE es más robusta a valores atípicos.')],
    ['Usar −log(ŷ) cuando el socio no pagó.', 'Olvidar el signo menos del paso.', 'Creer que un η más grande siempre aprende más rápido.']))

AP.append(bloque('b05', '05', 'De una neurona a una red',
    'Cada capa es una transformación afín seguida de una no linealidad; las capas ocultas construyen representaciones donde el problema se vuelve separable.',
    formula(r'\mathbf{a}^{(l)} = \varphi^{(l)}\!\big(W^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}\big),\quad W^{(l)} \in \mathbb{R}^{n_l\times n_{l-1}},\quad \#\text{param} = \sum_l (n_{l-1}n_l + n_l)') +
    '<p><b>Convención de código.</b> En NumPy y Keras las filas son ejemplos: \\(Z = AW + \\mathbf{b}\\) con \\(W\\) de tamaño \\(n_{l-1}\\times n_l\\). Es la misma cuenta, transpuesta; Keras muestra el «kernel» como entradas × salidas.</p>'
    '<p><b>XOR con dos neuronas ReLU.</b> \\(h_1 = \\max(0, x_1+x_2)\\), \\(h_2 = \\max(0, x_1+x_2-1)\\), \\(\\hat y = h_1 - 2h_2\\) da 0, 1, 1, 0. Con escalones: \\(h_1\\) = OR, \\(h_2\\) = AND, salida = OR y no AND.</p>'
    '<p><b>Aproximación universal</b> (Cybenko, 1989; Hornik, 1991): una capa oculta suficientemente ancha con activación no polinomial aproxima cualquier función continua en un compacto. No dice cuántas neuronas ni cómo encontrarlas: la profundidad logra lo mismo con muchas menos.</p>',
    f"<p>Las agencias de la cooperativa (lámina {L('red')}), con la red que resalta cada capa por clic; XOR con dos líneas ({L('xor-resuelto')}); pistas por capa con el «7» ({L('pistas')}); la demo «Juega» ({L('juega')}): Círculos con 1 neurona y luego con 4; contar parámetros ({L('parametros')}): haz la primera fila con ellos y pide la segunda en el chat.</p>",
    [('¿Cuántas capas y neuronas debo usar?', 'No hay fórmula. Para tablas medianas, 1–2 capas de 16–64 neuronas suelen bastar; se decide con validación. Más parámetros que datos de entrenamiento es señal de alerta de sobreajuste (semana 3).'),
     ('¿Qué «ve» una neurona oculta en datos de tabla?', 'Una combinación de variables, por ejemplo «cuota alta respecto al ingreso». No siempre es interpretable; en la semana 3 vemos herramientas de explicabilidad (SHAP, gradientes).'),
     ('¿Por qué se llama «perceptrón multicapa» si no usa la regla del perceptrón?', 'Por historia: las neuronas son como el perceptrón (suma + activación), pero se entrenan con retropropagación y activaciones suaves.')],
    ['Confundir capas con neuronas.', 'Contar parámetros sin los sesgos.', 'Pensar que la capa de entrada «calcula» algo.']))

AP.append(bloque('b06', '06', 'Retropropagación',
    'La retropropagación es la regla de la cadena organizada capa por capa: un forward guarda las activaciones y un backward calcula todos los gradientes en un costo similar al forward.',
    formula(r'\begin{aligned}&\delta^{(L)} = \hat{\mathbf{y}} - \mathbf{y} &&\text{(BP1, con sigmoide + BCE)}\\ &\delta^{(l)} = \big(W^{(l+1)}\big)^{\!\top}\delta^{(l+1)} \odot \varphi^{\prime}\big(\mathbf{z}^{(l)}\big) &&\text{(BP2)}\\ &\partial L/\partial W^{(l)} = \delta^{(l)}\,\mathbf{a}^{(l-1)\top} &&\text{(BP3)}\\ &\partial L/\partial \mathbf{b}^{(l)} = \delta^{(l)} &&\text{(BP4)}\end{aligned}') +
    '<p><b>Por qué la transpuesta en BP2.</b> En el forward, la fila \\(j\\) de \\(W^{(l+1)}\\) reúne lo que <i>entra</i> a la neurona \\(j\\). Hacia atrás necesitamos todo lo que <i>sale</i> de la neurona \\(k\\) de la capa \\(l\\): la columna \\(k\\) de \\(W^{(l+1)}\\), es decir, la fila \\(k\\) de su transpuesta.</p>'
    '<p><b>Por lotes</b> (filas = ejemplos): \\(\\Delta^{(L)} = (\\hat Y - Y)/B\\), \\(\\nabla W^{(l)} = A^{(l-1)\\top}\\Delta^{(l)}\\), \\(\\Delta^{(l-1)} = (\\Delta^{(l)}W^{(l)\\top})\\odot\\varphi\'(Z^{(l-1)})\\). Es lo que hace Keras por dentro.</p>'
    '<p><b>Costo.</b> Con diferencias finitas harían falta 2 forwards por parámetro (337 × 2 en la red de las lunas); el backward cuesta del orden de un forward. El <i>gradient check</i> usa diferencias finitas solo para verificar: error relativo &lt; 1e-6 (en NB02 da ~1e-11).</p>'
    '<p><b>Números del ejemplo 2-2-1</b> (NB02): a = (0.6106, 0.6225); ŷ = 0.5569; pérdida 0.5854; δ₂ = −0.4431; ∂L/∂W₂ = (−0.2706, −0.2758); δ₁ = (−0.0738, 0.0417); tras un paso con η = 0.5: ŷ = 0.6542, pérdida 0.4243.</p>',
    f"<p>Forward con números (lámina {L('adelante')}) sin hacer cuentas en vivo: mira cómo viaja la señal; la cadena del cacao ({L('culpa')}); engranajes ({L('engranajes')}); el backward ({L('atras')}) explicando el signo de la oculta 2; el paso ({L('actualizar')}); GradientTape ({L('tensorflow')}).</p>",
    [('¿La red «sabe» qué peso tiene la culpa?', 'Sí, en el sentido preciso de la derivada: cuánto cambiaría la pérdida si ese peso cambiara un poquito. Eso es la «culpa».'),
     ('¿Por qué la culpa de la oculta 2 es positiva si la salida necesitaba subir?', 'Porque su peso hacia la salida es negativo (−0.4): para que la salida suba, esa neurona debe bajar. El signo del peso invierte el mensaje.'),
     ('¿TensorFlow hace exactamente esto?', 'Sí: diferenciación automática en modo reverso. GradientTape graba las operaciones del forward y aplica la regla de la cadena hacia atrás. La diferencia con nuestra cuenta en el NB02 es ~1e-17 (redondeo).'),
     ('¿Qué es el gradiente que se desvanece?', 'Al retropropagar se multiplica por φ\'(z) en cada capa; con sigmoide (≤ 0.25) la culpa decae exponencialmente con la profundidad. ReLU, buenas inicializaciones y, más adelante, normalización y conexiones residuales lo mitigan.'),
     ('¿Por qué δ de salida queda tan simple?', 'Por la combinación sigmoide + BCE (o softmax + entropía cruzada): las derivadas se cancelan. Es una razón práctica para usar esa pareja.')],
    ['Olvidar multiplicar por la pendiente de la activación en BP2.', 'Mezclar el orden de las dimensiones (np.outer).', 'Actualizar los pesos antes de terminar de calcular todos los gradientes.']))

AP.append(bloque('b07', '07', 'Entrenar bien',
    'La escala de la inicialización, el tamaño del lote y el optimizador deciden si la red es entrenable; Adam con 1e-3 es un buen punto de partida.',
    formula(r'\text{He: } \operatorname{Var}(w) = \frac{2}{n_{in}} \qquad \text{Glorot: } \operatorname{Var}(w) = \frac{2}{n_{in}+n_{out}}') +
    formula(r'\text{Momentum: } \mathbf{v} \leftarrow \beta\mathbf{v} + \mathbf{g},\ \ \mathbf{w} \leftarrow \mathbf{w} - \eta\mathbf{v} \qquad \text{Adam: } \mathbf{w} \leftarrow \mathbf{w} - \eta\,\frac{\hat{\mathbf{m}}}{\sqrt{\hat{\mathbf{v}}}+\epsilon}') +
    '<p><b>Mini-lotes.</b> \\(\\hat{\\mathbf{g}} = \\frac1B\\sum_{i\\in\\mathcal B}\\nabla\\ell_i\\) es insesgado y su varianza baja como \\(1/B\\) (el error típico como \\(1/\\sqrt B\\)). Lotes chicos: más ruido, más pasos por época; lotes grandes: gradiente más preciso, más memoria.</p>'
    '<p><b>Adam</b> lleva \\(\\mathbf{m}\\) (media móvil del gradiente, β₁ = 0.9) y \\(\\mathbf{v}\\) (de su cuadrado, β₂ = 0.999), con corrección de sesgo; el paso efectivo de cada peso se normaliza por su propia escala. AdamW separa el <i>weight decay</i> del paso adaptativo (Loshchilov y Hutter, 2019).</p>'
    '<p><b>Conexión con la lectura de tendencia.</b> Con ajuste justo de hiperparámetros para todos, las ganancias de optimizadores nuevos sobre AdamW se reducen bastante (estudios de 2025). Útil para el video de conclusiones.</p>',
    f"<p>La culpa que se apaga (lámina {L('apaga')}): cambia a ReLU en vivo; las neuronas clonadas ({L('clones')}); censo vs. encuesta ({L('lotes')}); la carrera de optimizadores ({L('carrera')}) con el debate de la lectura; la receta ({L('receta-arranque')}): sugiere tomarle foto.</p>",
    [('¿Por qué no iniciar todo en cero?', 'Simetría: todas las neuronas de la capa calculan lo mismo, reciben el mismo gradiente y siguen idénticas. Los sesgos sí pueden empezar en cero.'),
     ('¿Qué batch_size uso?', '32 o 64 es un buen inicio en tablas. Si cambias el batch mucho, quizá debas reajustar el learning rate.'),
     ('¿Adam siempre gana?', 'No siempre: SGD con momentum bien ajustado a veces generaliza mejor. Adam es más robusto con poco ajuste; por eso es la opción por defecto en el curso.'),
     ('¿Qué es el learning rate schedule?', 'Cambiar η durante el entrenamiento (por ejemplo, bajarlo cuando la pérdida se estanca). Se ve con más detalle en la semana 3.')],
    ['Escalar con todos los datos (fuga).', 'Comparar optimizadores con distinta semilla o distinto ajuste.', 'Subir epochs para «arreglar» un learning rate malo.']))

AP.append(bloque('b08', '08', 'Keras en tres pasos',
    'Sequential define la arquitectura, compile fija optimizador, pérdida y métricas, y fit ejecuta el ciclo forward–backward–update por lotes y épocas.',
    '<pre><code>for epoch in range(epochs):\n    for X_b, y_b in batches(X_tr, y_tr, batch_size):\n        with tf.GradientTape() as tape:\n            loss = loss_fn(y_b, model(X_b, training=True))\n        grads = tape.gradient(loss, model.trainable_variables)\n        optimizer.apply_gradients(zip(grads, model.trainable_variables))\n    # then: validation metrics, callbacks (EarlyStopping, ...)</code></pre>'
    '<p>Eso es lo que hace <code>fit()</code> por dentro. Keras 3 puede correr sobre TensorFlow, JAX o PyTorch; en el curso usamos TensorFlow (por defecto en Colab).</p>',
    f"<p>Conecta cada línea del código (lámina {L('keras')}) con un bloque ya visto: arquitectura (02, 05), pérdida y optimizador (04, 07), lotes y épocas (07). Luego la práctica en clase ({L('practica3')}).</p>",
    [('¿Qué diferencia hay entre loss y metrics?', 'La pérdida es lo que se optimiza (debe ser derivable). Las métricas solo se reportan (accuracy, AUC); no guían el gradiente.'),
     ('¿Por qué validation_data?', 'Para ver en cada época cómo le va a la red con datos que no usa para aprender: detecta sobreajuste y permite elegir épocas, arquitectura y umbral.'),
     ('Me sale un error de shapes, ¿qué reviso?', 'Que Input(shape=(n_features,)) coincida con X.shape[1] y que y sea 0/1 de forma (N,) o (N,1) según la pérdida. El error típico es pasar X sin escalar o con columnas categóricas sin codificar.')],
    ['Olvidar keras.Input o poner mal su shape.', 'Usar softmax con una sola neurona de salida.', 'Leer solo la última época sin mirar las curvas.']))

AP.append(bloque('b09', '09', '¿El modelo es bueno? Métricas',
    'Con pocos positivos la exactitud engaña: se mira recall, precisión y ROC-AUC, y el umbral se elige con validación según el costo de cada error.',
    '<p><b>Matriz de confusión.</b> Exactitud = (VP + VN)/N; recall = VP/(VP + FN); precisión = VP/(VP + FP). Con prevalencia π, el clasificador constante «negativo» tiene exactitud 1 − π y recall 0.</p>'
    '<p><b>ROC-AUC</b> = probabilidad de que un positivo al azar reciba mayor puntaje que un negativo al azar (equivale al estadístico de Mann–Whitney normalizado); no depende del umbral. <b>PR-AUC</b> tiene como línea base la prevalencia: es más exigente con clases raras.</p>'
    '<p><b>Umbral.</b> Si un falso negativo cuesta c<sub>FN</sub> y un falso positivo c<sub>FP</sub>, con probabilidades bien calibradas el umbral que minimiza el costo esperado es c<sub>FP</sub> / (c<sub>FP</sub> + c<sub>FN</sub>).</p>'
    f'<p><b>La demo de la lámina {L("trampa87")}</b> usa 100 socios ficticios (13 en mora) con puntajes simulados: con umbral 0.5 la red tiene la misma exactitud que el modelo perezoso (87 %) pero encuentra 12 de 13 morosos, con 12 falsas alarmas. Es el mejor argumento de que la exactitud no basta.</p>',
    f"<p>La trampa (lámina {L('trampa87')}) en tres clics: los 100 socios, el modelo perezoso y la red con umbral; mueve el umbral en vivo y pregunta qué es peor para la cooperativa. Luego las tres preguntas ({L('metricas')}) con la imagen de las dos listas ordenadas para explicar el AUC.</p>",
    [('¿Qué umbral usamos?', 'El que responda a una decisión de negocio, elegido con validación: por ejemplo, encontrar al menos 70 % de los morosos. Bajar el umbral sube el recall y baja la precisión.'),
     ('¿Por qué no balanceamos las clases?', 'Se puede (pesos de clase, sobremuestreo), pero cambia la calibración de las probabilidades. Primero conviene elegir bien la métrica y el umbral.'),
     ('¿Un AUC de 0.87 es bueno?', 'Depende de la alternativa: compáralo con una línea base (regresión logística) y con el costo de los errores. Un AUC alto con un umbral mal elegido puede ser inútil.'),
     ('¿Esto conecta con la semana 3?', 'Sí: explicar por qué el modelo dijo «no» a un socio y si el modelo es robusto son los temas de la lectura de la semana 3.')],
    ['Reportar solo la exactitud.', 'Elegir el umbral mirando los datos de prueba.', 'Confundir recall con precisión.']))

# ------------------------------------------------------------------ notebooks (keys)
NBK = f"""
{idea('Los notebooks de los estudiantes tienen ejemplos resueltos y tareas que se autocorrigen. Las versiones resueltas están en Soluciones_privadas (en tu computador, fuera del repo).')}
<h3>Cómo abrir las soluciones en Colab</h3>
<ol><li>Entra a <a href="https://colab.research.google.com">colab.research.google.com</a> → <b>Archivo → Subir cuaderno</b> → elige el archivo de <code>Soluciones_privadas (en tu computador, fuera del repo)</code>.</li>
<li>O súbelos una vez a una carpeta privada de tu Google Drive y ábrelos con doble clic. <b>Nunca</b> los subas al repo público.</li>
<li>Ya vienen ejecutados: puedes ver todos los resultados sin correrlos.</li></ol>
<h3>NB01 · Tu primera neurona (viernes)</h3>
{table(['Tarea', 'Qué piden', 'Respuesta', 'Dónde se traban'], [
    ['T1', 'función neurona(x, w, b) y z del socio B', 'w @ x + b; z_b = −3.61', 'olvidar b; escribir números a mano'],
    ['T2', 'probabilidad y decisión del socio B', 'p ≈ 0.026; «rechaza»', 'usar z en vez de sigmoid(z)'],
    ['T3', 'corregir con y = −1', 'w = (0.2, 0.0), b = 0; todavía se equivoca (z = 0.2)', 'sumar en vez de restar'],
    ['T4', 'perceptrón para AND', 'X_and con 4 filas, y_and = [−1, −1, −1, 1]; aprende (p. ej. w = (3, 2), b = −4)', 'usar 0/1 en vez de −1/+1'],
    ['T5', '¿por qué falla XOR?', '«b»', '—'],
    ['T6', 'funciones mse y bce', 'mse = 132.25; bce(1, 0.9) = 0.105; bce(0, 0.9) = 2.303', 'usar solo −log(p)'],
    ['T7', 'descenso en (w + 2)²', 'mínimo −2; w_final ≈ −2.0000', 'pendiente con signo equivocado'],
    ['T8', '¿qué η convergen?', '0.05, 0.5, 0.9 → True; 1.1 → False', 'creer que 0.9 diverge porque rebota'],
    ['Mini-reto 1', 'pesos a mano para 6 socios', 'p. ej. w = (1.0, −1.5), b = −0.2 (hay muchas)', 'peso positivo para atrasos'],
])}
<h3>NB02 · Tu primera red (sábado)</h3>
{table(['Tarea', 'Qué piden', 'Respuesta', 'Dónde se traban'], [
    ['TA', 'forward del socio 2 (y = 0)', 'a ≈ (0.475, 0.677); ŷ ≈ 0.528; pérdida −log(1 − ŷ) ≈ 0.751', 'usar −log(ŷ)'],
    ['TB', 'culpa de la salida y dW2', 'δ = 0.528; dW2 ≈ (0.251, 0.357)', 'invertir ŷ − y'],
    ['TC', 'un paso completo', 'ŷ baja a ≈ 0.413', 'actualizar solo W2'],
    ['TD', 'GradientTape de (3x)²', '18', 'no usar tf.Variable'],
    ['TE', 'contar_parametros', '337 · 1 473 · 21', 'olvidar los sesgos'],
    ['Mini-reto 2', 'círculos ≥ 90 %', 'dos capas de 16 ReLU, Adam 0.01, 60 épocas ≈ 98 %; sin ocultas ≈ 49 %', 'olvidar keras.Input o la activación'],
    ['TG', 'peor optimizador', '«SGD» (val_loss ≈ 0.28 vs ≈ 0.12)', '—'],
])}
"""

# ------------------------------------------------------------------ quizzes key
def qrows(bank):
    return [[str(i + 1) + (' *' if 'clave' in q else ''), q['q'], f"{'ABCD'[q['ok']]} · {q['options'][q['ok']]}", TEMAS[q['tema']],
             (f"Idea clave {q['clave'][1:]} · " if 'clave' in q else '') + q['mide']] for i, q in enumerate(bank)]
QZ = f"""
{idea('Los quizzes son formativos y miden avance: cinco ideas clave aparecen en los dos con otra versión. El pre-quiz dice de dónde parte el grupo; el quiz final, cuánto se movió en cada idea.')}
<h3>Cómo se usa (sin Kahoot ni Excel)</h3>
<ol>
<li><b>Viernes, lámina {L('prequiz')}:</b> los estudiantes escanean el QR (o abren <a href="{PAGES}quiz/?pre">el pre-quiz</a>), escriben nombre y apellido y juegan: tiempo, puntos, racha y explicación de cada respuesta.</li>
<li>Al final la página les da un código como <code>[DL1|PRE|Ana Pérez|5/8|10110110|i1]</code>. Lo pegan en el chat de Teams.</li>
<li><b>Sábado, lámina {L('quizfinal')}:</b> lo mismo con <a href="{PAGES}quiz/?final">el quiz final</a>, con el mismo nombre.</li>
<li>Después de clase: selecciona el chat, cópialo y pégalo en <code>docencia/Resultados_quiz.html</code> → <b>Analizar</b>. Verás el promedio de cada quiz, el antes y el después de cada idea clave, la ganancia del grupo, las preguntas a reforzar y una tabla por estudiante (que puedes copiar a Excel o Sheets).</li>
</ol>
<p>Para jugarlo proyectado, todos juntos: abre <a href="{PAGES}quiz/?clase">el modo proyector</a> (sin puntos, con botón «Mostrar respuesta») y que respondan en el chat con el color o el número. El código cuenta solo el primer intento de cada estudiante.</p>
<h3>Las 5 ideas clave (pre ↔ final)</h3>
{table(['Idea clave', 'Pre-quiz', 'Quiz final'], [[f"{c[1:]}. {CLAVES[c]}", str([i + 1 for i, q in enumerate(PRE) if q.get('clave') == c][0]), str([i + 1 for i, q in enumerate(FINAL) if q.get('clave') == c][0])] for c in CLAVES])}
<h3>Pre-quiz (8 preguntas cortas, sin cuentas · 3 de calentamiento + 5 ideas clave)</h3>
{table(['#', 'Pregunta', 'Respuesta', 'Tema', 'Qué mide'], qrows(PRE))}
<p><b>Cómo leerlo:</b> las de calentamiento (1, 2 y 6) deberían salir altas; si falla la 6 (probabilidad), ve más despacio en la sigmoide (lámina {L('sigmoide')}). Las ideas clave (3, 4, 5, 7 y 8) es normal fallarlas el viernes: son la línea base. Si la 8 sale baja, la lámina {L('trampa87')} será una revelación: úsala.</p>
<h3>Quiz final (10 preguntas cortas, sin cuentas · toda la semana)</h3>
{table(['#', 'Pregunta', 'Respuesta', 'Tema', 'Qué mide'], qrows(FINAL))}
<p><b>Cómo leerlo:</b> en las ideas clave esperas un salto claro desde el pre-quiz. Una ganancia normalizada g de 0.3 a 0.7 es lo habitual en una semana bien dada; si una idea sube menos de 20 puntos, retómala en los primeros 10 minutos de la semana 2.</p>
"""

# ------------------------------------------------------------------ FAQ general
FAQ = [
    ('¿Necesito GPU para el curso?', 'No para esta semana: todo corre en la CPU gratuita de Colab en 1–2 minutos. Para imágenes (semana 2) conviene activar GPU en Colab: Entorno de ejecución → Cambiar tipo de entorno.'),
    ('¿Qué es un tensor?', 'Un arreglo de números con cualquier número de dimensiones: un número (0D), un vector (1D), una matriz (2D), un lote de imágenes (4D). TensorFlow se llama así porque opera con tensores.'),
    ('¿Qué es el sobreajuste y cómo se ve?', 'Cuando la red memoriza el entrenamiento: la pérdida de entrenamiento sigue bajando mientras la de validación sube. Se combate con más datos, regularización, dropout o early stopping (semana 3).'),
    ('¿Por qué la semilla cambia los resultados?', 'Porque fija los pesos iniciales, el orden de los lotes y la partición. Con otra semilla los números cambian un poco; por eso se reporta la semilla y, para comparar en serio, se promedian varias.'),
    ('¿Cuál es la diferencia entre parámetros e hiperparámetros?', 'Los parámetros (pesos, sesgos) se aprenden con el gradiente. Los hiperparámetros (η, capas, neuronas, batch, épocas) los elegimos nosotros con validación.'),
    ('¿Puedo usar PyTorch en vez de Keras?', 'Sí, si el grupo lo domina; el sílabo pide Keras/TensorFlow como mínimo técnico en la parte C. Las ideas son idénticas.'),
    ('¿Por qué los notebooks tienen el código en inglés y las explicaciones en español?', 'Porque el código, las librerías y la documentación técnica están en inglés: es la convención de la industria. Lo que hay que entender está en español.'),
    ('¿Las redes neuronales son cajas negras?', 'Más difíciles de interpretar que un modelo lineal, pero no del todo: hay técnicas de explicabilidad (importancia por permutación, SHAP, gradientes) que vemos en la semana 3.'),
    ('¿Cuánto se tarda en entrenar un modelo como ChatGPT?', 'Meses en miles de GPU, con costos de decenas a cientos de millones de dólares. La receta es la misma de esta semana; cambian la escala, la arquitectura (Transformer) y los datos.'),
    ('¿Las prácticas tienen nota?', 'No. NB01 y NB02 son prácticas en clase que se corrigen solas; sirven para aprender equivocándose. Lo que se registra son el pre-quiz y el quiz final, y solo para medir el avance del grupo.'),
    ('No me corre el notebook en Colab, ¿qué hago?', '1) Entorno de ejecución → Reiniciar y ejecutar todo. 2) Verifica que ejecutaste la celda Configuración. 3) Copia el mensaje de error en el chat de Teams.'),
]

GLOS_D = [
    ('Afín (transformación)', 'Wx + b: lineal más un desplazamiento. Una capa sin activación es afín.'),
    ('Autodiff (modo reverso)', 'Cálculo automático de gradientes recorriendo hacia atrás el grafo de operaciones; GradientTape lo implementa.'),
    ('Calibración', 'Qué tan bien las probabilidades del modelo coinciden con las frecuencias reales.'),
    ('Convexa (función)', 'Con un solo valle: cualquier mínimo local es global. La pérdida de una red no lo es.'),
    ('Diferencias finitas', 'Aproximar una derivada con (f(x+ε) − f(x−ε)) / 2ε; base del gradient check.'),
    ('Early stopping', 'Detener el entrenamiento cuando la métrica de validación deja de mejorar.'),
    ('Hiperplano', 'Generalización de la recta a muchas dimensiones: w·x + b = 0.'),
    ('Linealmente separable', 'Que existe un hiperplano que deja cada clase de un lado.'),
    ('Log-verosimilitud negativa', '−log de la probabilidad que el modelo asigna a los datos observados; la BCE es su versión Bernoulli.'),
    ('Margen (γ)', 'Distancia mínima de los datos a la frontera; controla la cota de Novikoff.'),
    ('One-hot', 'Codificar una categoría con columnas 0/1, una por valor posible.'),
    ('Pocket (perceptrón)', 'Variante que guarda el mejor vector de pesos visto; útil con datos no separables.'),
    ('PR-AUC', 'Área bajo la curva precisión–recall; su línea base es la prevalencia.'),
    ('Prevalencia', 'Proporción de positivos en los datos (13 % de mora en el ejemplo de clase).'),
    ('Punto silla', 'Punto con pendiente cero que no es mínimo: baja en una dirección y sube en otra.'),
    ('Regla de la cadena', 'La derivada de una composición es el producto de las derivadas: (f∘g)\' = f\'(g)·g\'.'),
    ('Umbral', 'Valor de probabilidad a partir del cual se predice la clase positiva (0.5 por defecto).'),
]

FUT = """
<p>Para que cada semana se sienta igual de ordenada, repite exactamente la misma forma:</p>
<pre><code>GitHub
├── deepLearningWeek1   (esta: raíz = página de estudiantes, docencia/ = tu panel)
├── deepLearningWeek2   (misma forma)
└── deepLearningWeek3   …
Tu computador
└── Soluciones_privadas de cada semana</code></pre>
<ul>
<li>Nombres de notebooks: <code>NB0x_dia_tema.ipynb</code> (estudiante) y <code>NB0x_..._SOLUCION.ipynb</code> (profesor).</li>
<li>Cada notebook: celda Configuración (oculta) con la autocorrección, luego «Ejemplo resuelto → Tarea → Revisar», y un Mini-reto al final.</li>
<li>Cada práctica en las slides: lámina con QR al notebook y lo que deberían ver; prácticas en clase y sin nota.</li>
<li>Slides en HTML con demos y notas del presentador (<code>codigo_fuente/slides/src</code>) y mapas conceptuales por bloque (<code>codigo_fuente/slides/maps</code>).</li>
<li>Pre-quiz y quiz final con cinco ideas clave pareadas y el mismo panel de resultados.</li>
</ul>
<p>Cuando quieras preparar la semana 2, pide «prepara la semana 2 con la misma estructura de la semana 1»: el código de <code>docencia/codigo_fuente</code> es el esqueleto.</p>
"""

REFS = """
<ul>
<li>Nielsen, M. A. (2015). <i>Neural networks and deep learning</i>. Determination Press. http://neuralnetworksanddeeplearning.com</li>
<li>Zhang, A., Lipton, Z. C., Li, M. y Smola, A. J. (2023). <i>Dive into deep learning</i>. Cambridge University Press. https://d2l.ai</li>
<li>Rosenblatt, F. (1958). The perceptron. <i>Psychological Review, 65</i>(6), 386–408.</li>
<li>Novikoff, A. B. J. (1962). On convergence proofs on perceptrons. <i>Symposium on the Mathematical Theory of Automata, 12</i>, 615–622.</li>
<li>Minsky, M. y Papert, S. (1969). <i>Perceptrons</i>. MIT Press.</li>
<li>Rumelhart, D. E., Hinton, G. E. y Williams, R. J. (1986). Learning representations by back-propagating errors. <i>Nature, 323</i>(6088), 533–536.</li>
<li>Cybenko, G. (1989). Approximation by superpositions of a sigmoidal function. <i>Mathematics of Control, Signals and Systems, 2</i>(4), 303–314.</li>
<li>Glorot, X. y Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. <i>AISTATS</i>, 249–256.</li>
<li>He, K., Zhang, X., Ren, S. y Sun, J. (2015). Delving deep into rectifiers. <i>ICCV</i>, 1026–1034.</li>
<li>Kingma, D. P. y Ba, J. (2015). Adam: A method for stochastic optimization. <i>ICLR</i>.</li>
<li>Loshchilov, I. y Hutter, F. (2019). Decoupled weight decay regularization. <i>ICLR</i>.</li>
</ul>
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
for sid, n, title, inner in [('notebooks', '5', 'Los notebooks: claves y dónde se traban', NBK),
                             ('quizzes', '6', 'Clave de los quizzes', QZ),
                             ('faq', '7', 'Preguntas generales que te pueden hacer',
                              '<input id="search" class="search" type="search" placeholder="Buscar en las preguntas y el glosario…" aria-label="Buscar">' + ''.join(qa(q, a) for q, a in FAQ)),
                             ('glosario', '8', 'Glosario docente', '<dl class="glos">' + ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS_D) + '</dl><p>El glosario básico de los estudiantes está en la guía de estudio.</p>'),
                             ('futuro', '9', 'Para las próximas semanas', FUT),
                             ('refs', '10', 'Referencias', REFS)]:
    body += section(sid, chip('Docente', 'amber'), title, inner, 'Revisado')
    toc.append((sid, n, title))

html = page('Guía docente y apuntes · Semana 1 · Deep Learning UIDE', 'Material solo para el docente.', toc, body, 'dl-uide-w1-docente', katex=KATEX)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'Guia_docente.html').write_text(html)
print('docente built', len(html) // 1024, 'KB')
