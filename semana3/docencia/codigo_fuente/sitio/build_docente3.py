"""Week-3 teacher guide and notes (only for the teacher): semana3/docencia/Guia_docente.html
usage: python build_docente3.py <semana3/docencia folder>
Slide numbers come from <folder>/slides/slides.json at build time; slide ids that are missing are reported and
printed as «?» so the build never breaks while the deck is still changing. Weeks 1 and 2 slide numbers (recap notes)
come from <repo>/docencia/slides/slides.json and <repo>/semana2/docencia/slides/slides.json. The quiz key is read from
banco3.py (written by the student-site builder) when it exists. All results are the real ones of DISENO3.md
(SEED = 2026), the same numbers NB05 and NB06 print. No days and no session dates: the week is organized by themes."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from kit_docencia3 import page, section, chip, idea, box, formula, weeks  # noqa: E402

try:
    from banco3 import PRE, FINAL, TEMAS, CLAVES  # noqa: E402
    HAVE_BANK = True
except Exception:  # the student-site fork writes banco3.py; rebuild this guide when it exists
    PRE, FINAL, TEMAS, CLAVES, HAVE_BANK = [], [], {}, {}, False

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docente3')
KATEX = 'inline'
SITE = 'https://deeplearningweek1.vercel.app/'
W3 = SITE + 'semana3/'
B, A, T, I, P = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--ink)', 'var(--purple)'
SL = {s['id']: s['n'] for s in json.loads((OUT / 'slides' / 'slides.json').read_text())}
REPO_ROOT = OUT.parent.parent
_W1 = REPO_ROOT / 'docencia' / 'slides' / 'slides.json'
_W2 = REPO_ROOT / 'semana2' / 'docencia' / 'slides' / 'slides.json'
SL1 = {s['id']: s['n'] for s in json.loads(_W1.read_text())} if _W1.exists() else {}
SL2 = {s['id']: s['n'] for s in json.loads(_W2.read_text())} if _W2.exists() else {}
MISSING = set()


def L(i):
    if i not in SL:
        MISSING.add(i)
        return '?'
    return SL[i]


def R(a, b):
    return f'{L(a)}–{L(b)}'


def _links(base, table, ids):
    out = [f'<a href="{base}#{i}">{table.get(i, "?")}</a>' for i in ids]
    return ('lámina ' if len(out) == 1 else 'láminas ') + ', '.join(out)


def W1(*ids):
    """Week-1 slide numbers with a link to that slide of the week-1 deck."""
    return 'S1 · ' + _links('../../docencia/slides/index.html', SL1, ids)


def W2(*ids):
    """Week-2 slide numbers with a link to that slide of the week-2 deck."""
    return 'S2 · ' + _links('../../semana2/docencia/slides/index.html', SL2, ids)


def G1(anchor, label):
    return f'<a href="../../guia/index.html#{anchor}">{label}</a>'


def G2(anchor, label):
    return f'<a href="../../semana2/guia/index.html#{anchor}">{label}</a>'


def qa(q, a):
    return f'<details class="qa" data-search><summary>{q}</summary><div>{a}</div></details>'


def table(head, rows):
    h = ''.join(f'<th>{x}</th>' for x in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table><tr>{h}</tr>{r}</table>'


def qcol(*temas):
    """Quiz items of these banco3 tema keys (rec = recap, b01/b02 = Tema 1, b03/b04 = Tema 2, b05 = closing)."""
    if not HAVE_BANK:
        return '—'
    pre = [str(i + 1) + ('*' if q.get('clave') else '') for i, q in enumerate(PRE) if q.get('tema') in temas]
    fin = [str(i + 1) + ('*' if q.get('clave') else '') for i, q in enumerate(FINAL) if q.get('tema') in temas]
    parts = ([('bases ' if temas == ('rec',) else 'pre ') + ', '.join(pre)] if pre else []) + (['final ' + ', '.join(fin)] if fin else [])
    return ' · '.join(parts) or '—'


S = []

# ------------------------------------------------------------------ 0 · how to use
S.append(('uso', '★', 'Cómo usar esta guía', f"""
<div class="hero">{weeks(3, '../../docencia/Guia_docente.html', '../../semana2/docencia/Guia_docente.html', 'Guia_docente.html')}<br><span class="chip">Solo docente</span>
<h1 style="margin-top:14px">Guía docente y apuntes · Semana 3</h1>
<p>Robustez, transfer learning, optimización y explicabilidad: que la red funcione con casos nuevos, aguante cambios pequeños, aproveche lo que otra red ya aprendió y pueda explicar por qué decide. Aquí está el orden de todo, el plan por temas (con sus puntos de corte), los apuntes con el rigor que hay detrás de cada lámina, las preguntas que te pueden hacer, las tablas de los notebooks, la lectura con su encuesta y la clave de los quizzes.</p>
<p style="font-size:15px">Semana 3 · noviembre de 2026 · Microsoft Teams. Las láminas son una sola secuencia por temas: cada sesión empieza donde terminó la anterior.</p></div>
<div class="grid">
<div class="tile"><h4>Antes de la semana</h4><p>Lee <a href="#orden">El orden de todo</a> y haz el <a href="#checklist">checklist</a>. Recorre las <a href="slides/index.html">slides</a> con la tecla <b>P</b> para ver tus notas.</p></div>
<div class="tile"><h4>Para preparar un tema</h4><p>Abre su <a href="mapas/index.html">mapa conceptual</a> (qué decir, ejemplo, pregunta y error frecuente por concepto) y luego sus apuntes: <a href="#b00">recorderis</a>, <a href="#b01">Tema 1</a>, <a href="#b02">Tema 2 · reutilizar</a>, <a href="#b02e">Tema 2 · explicar</a>, <a href="#b03">cierre</a>.</p></div>
<div class="tile"><h4>En clase</h4><p>El <a href="#plan">plan por temas</a> y su recuadro <b>Si vas atrasado</b>: dónde cortar sin dejar ideas a medias, qué mandar a la casa y cómo retomar. El plan usa unas 5 de las 6 horas: el colchón es para preguntas, no para más contenido.</p></div>
<div class="tile"><h4>Después</h4><p>Las <a href="#notebooks">tablas de los notebooks</a>, la <a href="#lectura">lectura</a> y la <a href="#encuesta">encuesta</a> para el video de conclusiones y la <a href="#quizzes">clave de los quizzes</a>.</p></div>
</div>
<h3>El hilo de la semana en una frase</h3>
{idea('Que la red acierte en el examen no basta: tiene que funcionar con casos nuevos, aguantar cambios pequeños, aprovechar lo que ya se sabe y poder explicar por qué decide.')}
<p>Primero, un <b>recorderis de las semanas 1 y 2</b>: lo nuevo se cuelga de lo que ya saben. Pregunta del <b>Tema 1</b>: <b>¿funcionará con casos nuevos?</b> (generalizar y ser robusto). Pregunta del <b>Tema 2</b>: <b>¿puedo reutilizar lo que otra red aprendió y explicar lo que decide?</b> El cierre retoma el título del entregable de la semana 1: <b>¿le creerías a tu red?</b> La lectura de tendencia pone el contexto: en Ecuador, desde marzo de 2026, una persona afectada por una decisión automatizada puede pedir una explicación de la lógica del algoritmo.</p>
<h3>Las 5 ideas clave (las mide el quiz)</h3>
<ol>
<li><b>Aprender no es memorizar:</b> el sobreajuste se ve cuando la pérdida de entrenamiento sigue bajando y la de validación sube.</li>
<li><b>Regularizar es ponerle frenos a la memoria:</b> dropout, aumento de datos y parar a tiempo.</li>
<li><b>Exacto no es robusto:</b> un cambio pequeño (mover la foto, un ruido invisible, el mundo que cambia) puede tumbar a un modelo muy exacto.</li>
<li><b>Transfer learning:</b> reutilizar lo que una red ya aprendió (congelar y ajustar); ayuda sobre todo cuando hay pocos datos.</li>
<li><b>Explicar y verificar:</b> Grad-CAM, la oclusión o SHAP son interpretaciones del modelo; una explicación también tiene que pasar pruebas.</li>
</ol>
<h3>Dónde está cada cosa en el repositorio</h3>
<pre><code>deepLearningWeek1/                ← el mismo repo público y el mismo sitio de Vercel
├── index.html ... docencia/        la semana 1
├── semana2/                        la semana 2
└── semana3/
    ├── index.html                  inicio de la semana 3 (con el selector Semana 1 · Semana 2 · Semana 3)
    ├── proyectos/                  NB05 (Tema 1) y NB06 (Tema 2), completos y ejecutados
    ├── guia/                       guía de estudio
    ├── quiz/                       pre-quiz y quiz final
    ├── material/                   la lectura de tendencia (PDF)
    └── docencia/                   lo tuyo
        ├── index.html              tu panel
        ├── slides/                 las {len(SL)} slides interactivas (notas con la tecla P)
        ├── mapas/                  mapas conceptuales para enseñar (se imprimen en A4)
        ├── Guia_docente.html       esta guía
        ├── Slides_Semana3.pdf      las slides en PDF, de respaldo
        ├── Encuesta_tendencia_Semana3.pdf   la encuesta de tendencia
        ├── Resultados_quiz.html    pegas los códigos del chat y ves el antes y el después
        └── codigo_fuente/          el código que genera las slides, los mapas y el sitio

Soluciones_privadas/              ← solo en tu computador y tu Drive: nunca al repo
    codigo_notebooks/               los generadores de NB05 y NB06</code></pre>
"""))

# ------------------------------------------------------------------ publish
S.append(('publicar', '0', 'Publicar la semana 3 (5 minutos)', f"""
{idea('La semana 3 vive en la carpeta semana3/ del mismo repositorio. Vercel ya está conectado: al subir los cambios a GitHub, el sitio se republica solo en segundos.')}
<ol>
<li>En tu carpeta <code>deepLearningWeek1</code> (Git Bash): <code>git add -A</code> → <code>git commit -m "Semana 3"</code> → <code>git push</code>. No hagas <code>git pull</code> desde otra copia: traería la historia vieja.</li>
<li>Abre <a href="{W3}">{W3}</a>: debe aparecer el inicio de la semana 3 con el selector <b>Semana 1 · Semana 2 · Semana 3</b> arriba. Tu panel está en <a href="{W3}docencia/">{W3}docencia/</a>; los paneles y las guías docentes de las semanas 1 y 2 también tienen ya el selector de tres semanas.</li>
<li>Los enlaces cortos de esta semana pasan por la raíz del sitio: <code>?nb05</code>, <code>?nb06</code>, <code>?pre3</code>, <code>?final3</code>, <code>?guia3</code>, <code>?slides3</code> y <code>?semana3</code>. Los de las semanas 1 y 2 siguen funcionando.</li>
<li>Las páginas de <code>semana3/docencia/</code> no aparecen en buscadores (<code>noindex</code> en <code>vercel.json</code> y en cada página), pero cualquiera con el enlace puede abrirlas: no las compartas en el chat.</li>
</ol>
<h3>Comprueba</h3>
<ul>
<li>Escanea con el celular los QR de las láminas {L('prequiz3')} (pre-quiz), {L('practica-nb05')} (NB05), {L('practica-nb06')} (NB06), {L('quizfinal3')} (quiz final) y {L('recursos3')} (guía de estudio).</li>
<li>Abre <a href="{W3}docencia/slides/">las slides</a>: pulsa <b>P</b> y se abre tu vista del presentador.</li>
<li>En el repo no hay generadores de notebooks: viven en <code>Soluciones_privadas</code> (y <code>semana3/docencia/codigo_fuente/notebooks/</code> está en <code>.gitignore</code>).</li>
</ul>
"""))

# ------------------------------------------------------------------ order
S.append(('orden', '1', 'El orden de todo: cómo se conecta la semana', f"""
{idea('Cada bloque de láminas tiene su sección del notebook, su mapa conceptual y sus preguntas en el quiz. Si un estudiante falla una pregunta, sabes a qué lámina y a qué celda mandarlo.')}
{table(['Momento', 'Qué pasa', 'Material'], [
    ['Antes de la semana', 'Publica en Canvas el enlace de la semana 3, la lectura de tendencia «¿Puedes explicar por qué tu modelo dijo «no»?» y la encuesta. Pide que lean antes de la segunda mitad del Tema 2 (explicar un «no» y las reglas) y que respondan la encuesta después de leer.', f'<a href="{W3}">Página de la semana 3</a> · <a href="../material/Lectura_tendencia_Semana3.pdf">lectura (PDF)</a> · <a href="Encuesta_tendencia_Semana3.pdf">encuesta (PDF)</a>'],
    ['Encuadre', f'La semana en dos temas, pre-quiz y las 5 ideas clave (láminas {R("portada3", "metas3")})', f'<a href="{W3}quiz/?pre">Pre-quiz</a> (QR en la lámina {L("prequiz3")})'],
    ['00 · Recorderis', f'Las semanas 1 y 2 en una sola cadena y tres preguntas para calentar (láminas {R("b00", "recorderis3-preguntas")})', 'Guías de estudio de las semanas 1 y 2'],
    ['Tema 1 · Generalizar y ser robusto', f'Memorizar, frenos, mover la foto, engañar y vacunar a la red, el mundo que cambia y afinar con el simulacro (láminas {R("b01", "cierre-tema1")})', f'NB05 en clase (lámina {L("practica-nb05")})'],
    ['Tema 2 · Reutilizar', f'Transfer learning: congelar y ajuste fino, 5/20/100 fotos por clase, ImageNet y LoRA (láminas {R("b02", "transfer-vida-real")})', 'NB06 §1'],
    ['Tema 2 · Explicar', f'Por qué explicar, dónde miró la red, la prueba de cordura, explicar un «no» de crédito, el contrafactual, por zona, la IA que se explica y las reglas (láminas {R("por-que-explicar", "cierre-tema2")})', f'NB06 en clase (lámina {L("practica-nb06")}) · debate de la lectura'],
    ['Cierre', f'¿Le creerías a tu red?: las cinco preguntas, la actividad «tu proyecto», quiz final y lo que viene (láminas {R("b03", "recursos3")})', f'<a href="{W3}quiz/?final">Quiz final</a> · <a href="#quizzes">Resultados</a>'],
    ['Después', 'Repaso con las slides y la guía de estudio; video de conclusiones con los resultados de la encuesta; entrega de la semana en Canvas (con su apartado de análisis crítico ético)', 'Guía de estudio · slides · Canvas'],
])}
<h3>Parte por parte</h3>
{table(['Parte', 'Láminas', 'Notebook', 'Quiz'], [
    ['Encuadre', R('portada3', 'metas3'), '—', f"el pre-quiz completo (lámina {L('prequiz3')})"],
    ['00 · Recorderis de las semanas 1 y 2', R('b00', 'recorderis3-preguntas'), '—', qcol('rec')],
    ['Tema 1 · Generalizar y ser robusto', R('b01', 'cierre-tema1'), 'NB05 §0–6 · Experimento 5', qcol('b01', 'b02')],
    ['Tema 2 · Reutilizar y explicar', R('b02', 'cierre-tema2'), 'NB06 §0–6 · Experimento 6', qcol('b03', 'b04')],
    ['Cierre · ¿Le creerías a tu red?', R('b03', 'recursos3'), '—', qcol('b05')],
])}
<p class="note">{'* = idea clave: aparece en los dos quizzes para medir el avance.' if HAVE_BANK else 'La columna Quiz se llena al reconstruir esta guía cuando exista el banco de preguntas (banco3.py).'}</p>
<p>Los dos notebooks son <b>prácticas en clase, sin nota</b>: el NB05 cierra el Tema 1 y el NB06 cierra el Tema 2. Todo el código ya viene escrito y explicado; se leen, se ejecutan, se predice antes de ejecutar y se responden los <b>ejercicios</b> leyendo los resultados (respuesta plegada). Los experimentos 5 y 6 son opcionales.</p>
"""))

# ------------------------------------------------------------------ checklist
S.append(('checklist', '2', 'Checklist antes de clase', f"""
<h3>Una vez (antes de la primera sesión de la semana)</h3>
<ul>
<li><a href="#publicar">Publicar la semana 3</a> y probar los QR desde tu celular (láminas {L('prequiz3')}, {L('practica-nb05')}, {L('practica-nb06')}, {L('quizfinal3')} y {L('recursos3')}).</li>
<li>Abrir NB05 y NB06 desde la página y hacer <b>Entorno de ejecución → Ejecutar todo</b> con la CPU gratuita de Colab, sin errores. El NB05 entrena varias redes (es el más largo); el NB06 instala <code>shap</code> si falta. Si tarda, la GPU es opcional: <b>Entorno de ejecución → Cambiar tipo de entorno</b>.</li>
<li>Recorrer las slides con la vista del presentador (<b>P</b>) y probar las demos con datos reales: las curvas del estudiante que memoriza ({L('memorizar3')}), mover la foto ({L('aumento-mover')}), el ejemplo adversarial ({L('adversarial')}), la curva de ε ({L('fgsm-curva')}), el transfer learning ({L('transfer-resultado')}), los mapas de calor ({L('donde-miro')}), la prueba de cordura ({L('cordura')}), la socia ({L('explicar-credito')}, {L('contrafactual')}) y por zona ({L('por-zona')}).</li>
<li>Publicar en Canvas el enlace de la semana 3, la lectura de tendencia y la encuesta.</li>
<li>Mirar los resultados del quiz final de la semana 2 (<a href="../../semana2/docencia/Resultados_quiz.html">Resultados_quiz de la semana 2</a>): si una idea clave subió menos de 20 puntos, retómala en el recorderis (3 minutos).</li>
<li>Preparar las salas de grupos en Teams para la actividad de la lámina {L('tu-proyecto3')} (los mismos grupos del proyecto de titulación).</li>
<li>Jugar tú el pre-quiz y abrir <code>Resultados_quiz.html</code> → <b>Ver un ejemplo</b>.</li>
</ul>
<h3>Antes de cada sesión, 15 minutos antes</h3>
<ul>
<li>Teams con el correo institucional; iniciar la grabación y verificar que graba.</li>
<li>Slides en el navegador con <b>F</b> y la vista del presentador (<b>P</b>) en la segunda pantalla. Comparte <b>la ventana de las slides</b>.</li>
<li>El notebook del tema que toca (NB05 o NB06) abierto en otra pestaña y ya ejecutado una vez, para mostrar resultados aunque la conexión falle.</li>
<li>Anota en qué lámina terminaste la sesión anterior: la siguiente empieza ahí (si es el Tema 2, con la lámina {L('repaso-tema1')}).</li>
<li>El enlace de la página listo para pegar en el chat: <code>{W3}</code>.</li>
<li>Al terminar: «Finalizar reunión para todos», para que la grabación se cierre bien.</li>
</ul>
"""))

# ------------------------------------------------------------------ plan
PLAN = [
    ['Encuadre', R('portada3', 'metas3'), '≈ 10 min', 'La semana en dos temas; pre-quiz jugado (6 min); las 5 ideas clave', '¿Le prestarían dinero a alguien solo porque una red acierta 87 %?'],
    ['00 · Recorderis de las semanas 1 y 2', R('b00', 'recorderis3-preguntas'), '≈ 15 min', 'Las dos semanas en una cadena: neurona → pérdida y gradiente → Keras → la suposición de cada arquitectura → lo que vimos (CNN 87.7 % con 8 veces menos parámetros; mover 2 px: densa 56.5 %, CNN 75.2 %; 80 pasos: atención 100 %); tres preguntas para calentar', '¿Qué supone una CNN sobre una foto?'],
    ['Tema 1 · memorizar y frenar', R('b01', 'keras-frenos'), '≈ 30 min', 'Curvas reales con 1 000 fotos: 96.7 % frente a 83.0 % y la época 33; más perillas que fotos; dropout, aumento y parar a tiempo (L2 de pasada); 81.6 % con frenos y 87.7 % con las 60 000 fotos; las tres líneas de Keras', '¿En qué época habrían parado?'],
    ['Tema 1 · exacto no es robusto', R('aumento-mover', 'mundo-cambia'), '≈ 25 min', 'Mover 4 px: 28.2 % sin aumento y 76.4 % con aumento; el botín que pasa a «zapatilla»; FGSM, subir la montaña a propósito; ε = 0.05: 39.2 % y 71.7 % vacunada; el mundo que cambia', 'Si a la vista es la misma foto, ¿por qué la red cambia de opinión?'],
    ['Tema 1 · afinar sin trampa', str(L('hiperparametros')), '≈ 10 min', 'Búsqueda al azar con el simulacro; la mejor da 86.8 % en validación y 86.9 % en el examen final, medido una sola vez', '¿Qué pasa si afinan con el examen final?'],
    ['Tema 1 · práctica NB05', str(L('practica-nb05')), '35 min', 'Colab funcionando en todos; prioridad §1, §2 y §4; el resto queda para la casa', '¿Cuánto creen que baja con ε = 0.05?'],
    ['Tema 1 · cierre', str(L('cierre-tema1')), '≈ 5 min', 'Las tres ideas del tema (1, 2 y 3)', 'Del 1 al 5, ¿podrían explicarle el sobreajuste a un colega?'],
    ['Tema 2 · reutilizar', R('b02', 'transfer-vida-real'), '≈ 25 min', 'El Tema 1 en tres ideas (puente, 5 min); el profesional con experiencia; congelar frente a ajuste fino (3 204 de 8 004 parámetros); 5/20/100 fotos por clase; ImageNet, keras.applications y LoRA', '¿Con cuántas fotos por clase deja de ayudar?'],
    ['Tema 2 · explicar una foto', R('por-que-explicar', 'cordura'), '≈ 15 min', 'La socia y la norma de Ecuador; oclusión y Grad-CAM sobre el botín, la camisa y el bolso; la prueba de cordura (−0.12, −0.05 y 0.90)', '¿Un mapa de calor bonito es una buena explicación?'],
    ['Tema 2 · explicar un «no»', R('explicar-credito', 'por-zona'), '≈ 20 min', 'Lo importante en general (la carga, 0.125) frente a lo que pesó en la socia (los atrasos, +0.30); el contrafactual de la cuota (61 % → 48 %); por zona: rechazo 8.9 % frente a 3.7 %, y sin la columna rural', '¿Qué explicación le sirve a ella y cuál al científico de datos?'],
    ['Tema 2 · la tendencia', R('ia-se-explica', 'reglas'), '≈ 15 min', 'Lo que la IA dice de sí misma (36 + 59; la pista mencionada 25 % y 39 % de las veces); Brasil, Ecuador y la UE; el debate de la lectura (10 min)', '¿Regular ahora o esperar?'],
    ['Tema 2 · práctica NB06', str(L('practica-nb06')), '40 min', 'Parejas o salas de 3; prioridad §1, §2, §3 y §4', '¿Los tres mapas cuentan la misma historia?'],
    ['Tema 2 · cierre', str(L('cierre-tema2')), '≈ 5 min', 'Las dos ideas del tema (4 y 5) y las preguntas que quedan abiertas', 'Del 1 al 5, ¿podrían explicarle un «no» a una socia?'],
    ['Cierre · ¿Le creerías a tu red?', R('b03', 'tu-proyecto3'), '≈ 28 min', 'Las cinco preguntas antes de usar un modelo con personas; la actividad en salas (20 min) con la plantilla en el chat', '¿Cuál de las cinco no pueden responder todavía?'],
    ['Cierre · quiz final y lo que viene', R('quizfinal3', 'recursos3'), '≈ 12 min', 'Todos jugaron y pegaron su código; las tres semanas en un mapa; la entrega final y el video de conclusiones', '¿Qué pregunta aplicarán primero en su proyecto?'],
]
S.append(('plan', '3', 'Plan por temas (no por días)', f"""
{idea('La semana es una sola secuencia de láminas en cinco partes: encuadre, recorderis, Tema 1, Tema 2 y cierre. Cada sesión empieza donde terminó la anterior. Duraciones: recorderis ≈ 15 min · Tema 1 ≈ 1 h 45 (con 35 min de NB05) · Tema 2 ≈ 2 h (con 40 min de NB06) · cierre ≈ 40 min. El plan suma unas 5 horas de las 6: el colchón es para preguntas, no para más contenido.')}
{table(['Parte', 'Láminas', 'Duración sugerida', 'Qué debe quedar', 'Pregunta para lanzar'], PLAN)}
{box('ojo', 'Si vas atrasado', f"""<p><b>Puntos de corte naturales.</b> Corta en uno de estos tres lugares y ninguna idea queda a medias:</p>
<ul>
<li>después de la lámina <b>{L('cierre-tema1')}</b>: el Tema 1 completo (ideas 1, 2 y 3, con el NB05);</li>
<li>después de la lámina <b>{L('cordura')}</b>: el transfer learning y los mapas de calor cerrados con su prueba de cordura (ideas 4 y 5); falta explicar el «no» de crédito, la tendencia y el NB06;</li>
<li>después de la lámina <b>{L('cierre-tema2')}</b>: el Tema 2 completo; solo falta el cierre.</li>
</ul>
<p><b>Para la casa, sin perder nada:</b> del NB05, la §3 (mover la foto), la §5 (vacunar) y la §6 (afinar), que también están en las láminas {L('aumento-mover')}, {L('fgsm-curva')} y {L('hiperparametros')}; del NB06, la §5 (contrafactual) y la §6 (por zona), que están en las láminas {L('contrafactual')} y {L('por-zona')}; los ejercicios y los experimentos 5 y 6; la lectura y la encuesta.</p>
<p><b>Para retomar en otra sesión:</b> si cortaste al final del Tema 1, empieza con la sección del Tema 2 y la lámina <b>{L('repaso-tema1')}</b> (el Tema 1 en tres ideas, 5 minutos). Si cortaste después de la prueba de cordura, abre con esa lámina ({L('cordura')}) como resumen en 2 minutos («una explicación también se verifica») y sigue en la {L('explicar-credito')}. Si cortaste al final del Tema 2, abre con la lámina {L('cierre-tema2')} y pasa al cierre.</p>
<p><b>Se pueden decir en un minuto:</b> las tres líneas de Keras ({L('keras-frenos')}), el transfer learning en la vida real ({L('transfer-vida-real')}), la IA que se explica ({L('ia-se-explica')}) y el mapa del curso ({L('mapa-curso')}). En el recorderis, si las tres preguntas salen bien, pasa rápido por la cadena.</p>
<p><b>No recortes:</b> las dos prácticas ({L('practica-nb05')} y {L('practica-nb06')}), la prueba de cordura ({L('cordura')}: es la mitad de la idea clave 5) y la actividad «tu proyecto» ({L('tu-proyecto3')}), que conecta la semana con la entrega y su análisis crítico ético. Si el quiz final no cabe, deja el enlace <code>…/semana3/quiz/?final</code> en el chat y pide el código.</p>""")}
"""))


# ------------------------------------------------------------------ notes per block
def bloque(sid, n, title, esencial, rigor, explicar, preguntas, errores):
    inner = (idea(esencial) + '<h3>Con más rigor (para ti)</h3>' + rigor +
             '<h3>Cómo explicarlo</h3>' + explicar +
             '<h3>Preguntas que te pueden hacer</h3>' + ''.join(qa(q, a) for q, a in preguntas) +
             box('error', 'Errores típicos de los estudiantes', '<ul>' + ''.join(f'<li>{e}</li>' for e in errores) + '</ul>'))
    part = {'00': 'Recorderis', '01': 'Tema 1', '02': 'Tema 2 · reutilizar', '02e': 'Tema 2 · explicar', '03': 'Cierre'}.get(n, n)
    return (sid, n, title, inner, chip(f'Apuntes · {part}'))


AP = []

# ---- 00 · recap of weeks 1 and 2
RECAP = [
    ['Neurona: z = w·x + b', 'Multiplica cada dato por su peso, suma todo y añade el sesgo; la activación decide.', 'Tu nota final del curso: cada nota por lo que pesa.', W1('nota', 'comite'), G1('b02', 'Guía S1 · 02')],
    ['Pérdida y gradiente', 'La pérdida resume el error en un número; el gradiente dice hacia dónde sube y damos el paso al revés.', 'Bajar el Cotopaxi con neblina, tanteando con el pie.', W1('perdida', 'cotopaxi'), G1('b04', 'Guía S1 · 04')],
    ['Keras y el simulacro', 'Construir, compilar, entrenar y predecir; <code>validation_split</code> separa el simulacro que se mira en cada época.', 'El motor y el volante. Esta semana el simulacro es el protagonista.', W1('keras') + '<br>' + W2('keras-4pasos'), G1('b08', 'Guía S1 · 08') + ' · ' + G2('b00', 'S2 · 00')],
    ['Densa: todo con todo', 'Cada neurona mira cada dato; con una foto aplanada no sabe quién es vecino de quién.', 'La primera capa con una foto de 28 × 28: 100 480 pesos.', W2('aplanar'), G2('b01', 'Guía S2 · 01')],
    ['CNN: lo cercano importa', 'Un filtro pequeño recorre la foto con los mismos pesos.', 'La lupa. 12 810 parámetros y 87.7 %, 8 veces menos que la densa.', W2('filtro', 'compartir', 'duelo'), G2('b01', 'Guía S2 · 01')],
    ['RNN y atención: el orden importa', 'La RNN lleva una libreta de tamaño fijo y se olvida; la atención mira directo a todos los pasos.', 'La libreta. Examen de memoria con 80 pasos: SimpleRNN 52 %, LSTM 50 %, atención 100 %.', W2('libreta', 'examen-memoria', 'atencion'), G2('b02', 'Guía S2 · 02') + ' · ' + G2('b03', '03')],
    ['Cada arquitectura es una suposición', 'Se elige por la estructura de los datos y se compara con justicia.', 'Mover la prenda 2 px: densa 56.5 %, CNN 75.2 %; con 4 px la CNN cae a 28.2 %. Es el gancho del Tema 1.', W2('suposicion', 'elegir'), G2('b04', 'Guía S2 · 04')],
]
WARM = [
    # Same three questions, same order, as the deck slide «recorderis3-preguntas» (QA3 in slides_tema1.py).
    ['1 · En <code>fit(…, validation_split=0.2)</code>, ¿qué es ese 20 %?', 'El simulacro (validación): fotos que la red no estudia. Sirve para ver si aprende o memoriza y para decidir (cuándo parar, qué hiperparámetros) sin tocar el examen final. Lo usamos en todo el Tema 1.', f"Repite la analogía del simulacro ({W1('memorizar', 'keras-fit')}) y manda a la {G1('b08', 'sección 08 de la guía de la semana 1')}."],
    ['2 · ¿Por qué la CNN necesita unas 8 veces menos parámetros que la red densa?', 'Comparte sus filtros: el mismo filtro de 3 × 3 (9 pesos y 1 sesgo) recorre las 676 posiciones de la foto. 12 810 parámetros contra 101 770, y aun así acierta más.', f"Repite la lupa en 3 minutos ({W2('filtro', 'compartir')}) y manda a la {G2('b01', 'sección 01 de la guía de la semana 2')}."],
    ['3 · La CNN acierta el 87.7 %. Si movemos cada foto 4 píxeles, ¿cuánto acierta?', '28.2 %: se cae. Exacta no significa robusta. (Con 2 píxeles, 75.2 % frente a 56.5 % de la densa: aguanta un poco, no mucho.) Es el punto de partida del Tema 1.', f"Muestra el duelo ({W2('duelo')}) y anuncia que en el Tema 1 lo arreglamos con aumento de datos."],
]
AP.append(bloque('b00', '00', 'Recorderis de las semanas 1 y 2',
    'El recorderis no repite las semanas 1 y 2: pone en una sola cadena lo que ya saben para que la pregunta nueva se cuelgue de ahí. Hasta ahora la pregunta fue «¿qué tan exacta es la red en el examen final?». Esta semana se suman otras: ¿funcionará con casos nuevos?, ¿aguanta cambios pequeños?, ¿puedo reutilizarla?, ¿puedo explicar lo que decide? Todas se apoyan en dos cosas que ya conocen: el simulacro (la validación) y el gradiente.',
    '<p><b>Por qué estos eslabones.</b> El Tema 1 usa tres ideas de las semanas anteriores: el <b>simulacro</b> (<code>validation_split</code>, semana 1) para detectar la memorización y para afinar hiperparámetros; el <b>gradiente</b> (semana 1), que en FGSM se calcula respecto a la foto en vez de respecto a los pesos; y la <b>CNN</b> de la semana 2, que es exactamente la red de los dos notebooks (Conv2D(16, 3) → MaxPooling2D → Conv2D(32, 3) → MaxPooling2D → Flatten → Dense(10), 12 810 parámetros, 87.7 % con las 60 000 fotos y 5 épocas). El Tema 2 reutiliza las capas convolucionales de esa misma red (transfer learning) y mira adentro de ellas (Grad-CAM usa su última capa convolucional, de 11 × 11 × 32).</p>'
    '<p><b>La continuidad de los números.</b> La fila «sin aumento» del NB05 (87.7 %; mover 1/2/3/4 px: 84.4 / 75.2 / 50.9 / 28.2 %) es la misma CNN de la semana 2 con la misma semilla: por eso coincide con el duelo. Si alguien lo nota, es buena señal: el experimento es reproducible.</p>',
    f"<h4>La cadena (lámina {L('recorderis3')}, un eslabón por clic, unos 8 minutos)</h4>"
    + table(['Eslabón', 'Qué decir (una frase)', 'La analogía o el número', 'Dónde estaba', 'Para repasar'], RECAP)
    + "<p>Ve rápido: es memoria, no clase nueva. Pregunta antes de revelar cada eslabón («¿qué venía después de la neurona?») y deja que lo digan ellos. Cierra con la pregunta de la semana: «hasta ahora medimos qué tan exacta es la red; ¿le prestarían dinero a alguien solo por eso?».</p>"
    + f"<h4>Tres preguntas para calentar (lámina {L('recorderis3-preguntas')}, unos 5 minutos)</h4>"
    + "<p>Lanza cada pregunta, pide la respuesta en el chat (una letra o una palabra) y revela. Son un termómetro: dicen si la base de las semanas 1 y 2 aguanta el peso de esta semana.</p>"
    + table(['Pregunta', 'Respuesta', 'Si más de un tercio falla'], WARM)
    + "<p>Si en los resultados del quiz de la semana 2 alguna idea clave subió poco, este es su lugar: 3 minutos, con su lámina de la semana 2, antes de seguir. Es mejor llegar más tarde al Tema 1 que hablar de robustez sobre una CNN que no se entiende.</p>",
    [('¿Por qué otra vez Fashion-MNIST y la misma CNN?', 'Para que lo único que cambie sea la técnica de esta semana. Si cambiáramos de datos y de red a la vez, no sabríamos qué explica la diferencia: es la misma lección de «comparar con justicia» de la semana 2.'),
     ('¿Qué diferencia hay entre el simulacro y el examen final?', 'El simulacro (validación) se mira todas las veces que haga falta para decidir: cuándo parar, qué hiperparámetros usar. El examen final (prueba) se mira una sola vez, al final, para reportar. Si se usa el examen para decidir, deja de medir casos nuevos.'),
     ('¿Hay que saber las cuentas de la semana 1 para seguir?', 'No las cuentas a mano, sí la idea: el gradiente dice hacia dónde sube la pérdida. En FGSM se usa esa misma idea al revés: se sube a propósito, moviendo la foto.')],
    ['Confundir el simulacro (validación) con el examen final (prueba).', 'Creer que una exactitud alta en el examen final responde todas las preguntas sobre un modelo.', 'Olvidar que la CNN de esta semana es la misma de la semana 2.']))

# ---- 01 · generalize and be robust
AP.append(bloque('b01', '01', 'Generalizar y ser robusto',
    'Una red generaliza si le va bien con casos que no vio. Con pocos datos y muchos parámetros, memoriza: la pérdida de entrenamiento sigue bajando mientras la de validación sube. Los frenos (dropout, aumento de datos, parar a tiempo, L2) ayudan un poco; más datos ayudan mucho. Y ser exacto no es ser robusto: mover la foto, un ruido calculado o un mundo que cambia pueden tumbar a un modelo exacto.',
    formula(r'\underbrace{\mathbb{E}\big[(y-\hat f(x))^2\big]}_{\text{error en casos nuevos}} \;=\; \underbrace{\big(\mathbb{E}[\hat f(x)]-f(x)\big)^2}_{\text{sesgo}^2} \;+\; \underbrace{\mathbb{E}\big[(\hat f(x)-\mathbb{E}[\hat f(x)])^2\big]}_{\text{varianza}} \;+\; \underbrace{\sigma^2}_{\text{ruido}}',
            note='<p><b>La intuición de sesgo y varianza.</b> El <b>sesgo</b> es equivocarse por ser demasiado simple: con cualquier muestra el modelo comete el mismo error. La <b>varianza</b> es cambiar mucho según qué ejemplos tocaron: el estudiante que memoriza el solucionario. La descomposición exacta es para el error cuadrático; en clasificación se usa como intuición. Con 1 000 fotos y 12 810 parámetros, manda la varianza: hay más perillas que ejemplos para estudiar. En redes muy grandes la curva clásica en U no siempre se cumple (doble descenso; Belkin et al., 2019), pero la regla práctica no cambia: se decide con el simulacro.</p>'
                 '<p><b>El NB05 §1.</b> 1 000 fotos para estudiar, 2 000 de simulacro, 60 épocas, sin frenos: al final 96.7 % en entrenamiento y 83.0 % en validación; la pérdida de validación es mínima en la época 33 y después sube aunque la exactitud de validación casi no cambie (la red se vuelve cada vez más segura en sus errores, y la pérdida castiga la seguridad equivocada). Examen final con 10 000 fotos: 80.9 %.</p>',
            read='el error con casos nuevos se reparte en tres: equivocarse por simple (sesgo), cambiar según la muestra (varianza) y el ruido que nadie puede predecir.') +
    formula(r'\begin{gathered}\tilde{\mathbf h} = \frac{\mathbf m \odot \mathbf h}{1-p}, \quad m_j \sim \text{Bernoulli}(1-p) \\[8pt] \mathcal L_{\text{reg}} = \mathcal L + \lambda \sum_i w_i^2 \;\Rightarrow\; w \leftarrow w - \eta\,(\nabla_w \mathcal L + 2\lambda w)\end{gathered}',
            [(r'p', 'probabilidad de apagar cada neurona (0.3)', A), (r'\mathbf m', 'la máscara al azar de cada paso', B), (r'\lambda', 'cuánto se castigan los pesos grandes', I)],
            '<p><b>Dropout</b> (Srivastava et al., 2014): en cada paso de entrenamiento se apaga al azar el 30 % de las neuronas y las demás se escalan por 1/(1 − p), para que al predecir no haya que cambiar nada. Keras lo aplica solo al entrenar (<code>fit</code>) y lo apaga en <code>predict</code> y <code>evaluate</code>. Se puede ver como entrenar a la vez muchísimas subredes que comparten pesos y promediarlas. <b>L2</b> (<i>weight decay</i>): cada paso encoge los pesos un factor (1 − 2ηλ); en Keras, <code>kernel_regularizer=keras.regularizers.l2(1e-4)</code>; con Adam se prefiere <code>keras.optimizers.AdamW</code>, que aplica el encogimiento por separado.</p>'
            '<p><b>Parar a tiempo</b>: <code>EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True)</code> mira la pérdida del simulacro; si no mejora en 8 épocas, para y devuelve los pesos de la mejor. En el NB05 se detiene en la época 79 y se queda con la 71 (79 = 71 + 8). <b>Aumento de datos</b>: <code>RandomTranslation(0.05, 0.05)</code> mueve cada foto al azar hasta un 5 % (≈ 1.4 px) en cada paso; como el dropout, solo actúa al entrenar. Con los tres frenos: 81.6 % en el examen final (sin frenos, 80.9 %) y las curvas ya no se separan. Con las 60 000 fotos, la misma red llega a 87.7 %: más datos es el mejor freno.</p>') +
    '<p><b>Aumento contra fotos movidas (NB05 §3, 60 000 fotos, 5 épocas).</b> El aumento le enseña a la red una invariancia que la arquitectura no garantiza: <code>RandomTranslation(0.15)</code> mueve hasta 0.15 × 28 ≈ 4 px, justo el rango de la prueba.</p>'
    + table(['', 'Sin mover', '1 px', '2 px', '3 px', '4 px'], [
        ['Sin aumento (la CNN de la semana 2)', '87.7 %', '84.4 %', '75.2 %', '50.9 %', '28.2 %'],
        ['Con RandomTranslation(0.15)', '82.6 %', '82.6 %', '82.3 %', '81.1 %', '76.4 %']])
    + '<p>Compra robustez a cambio de unos puntos con las mismas 5 épocas (con más épocas la diferencia sin mover se achica). Solo se aumenta con cambios que no cambian la etiqueta: mover una prenda sí; voltear un 6 lo convierte en 9.</p>'
    + formula(r"\begin{gathered}x' = \operatorname{clip}_{[0,1]}\!\Big(x + \varepsilon \cdot \operatorname{signo}\big(\nabla_x\, \mathcal L(\theta, x, y)\big)\Big) \\[8pt] \max_{\|\delta\|_\infty \le \varepsilon} \nabla_x \mathcal L^\top \delta = \varepsilon\,\|\nabla_x \mathcal L\|_1\end{gathered}",
              [(r'\varepsilon', 'el tamaño del cambio por píxel (0.05 ≈ 13 de 255 tonos)', A), (r'\nabla_x \mathcal L', 'cuánto sube la pérdida al cambiar cada píxel', B), (r'\theta', 'los pesos: aquí no se tocan', I)],
              '<p><b>FGSM</b> (<i>fast gradient sign method</i>; Goodfellow, Shlens y Szegedy, 2015). Es el descenso de gradiente de la semana 1 con dos cambios: se deriva respecto a la <b>foto</b> (no a los pesos) y se da el paso <b>cuesta arriba</b> (+, no −). La segunda fórmula dice por qué el signo: si cada píxel solo puede moverse ε, el cambio que más sube la pérdida (en primera aproximación) es mover cada píxel ε en la dirección de su gradiente. <b>Por qué funciona con un cambio invisible:</b> la explicación «lineal» del artículo. Para un puntaje lineal wᵀx, el cambio δ = ε·signo(w) sube el puntaje en ε‖w‖₁: cada píxel aporta muy poco, pero son 784 píxeles empujando en la misma dirección. Las redes con ReLU son casi lineales a trozos, y eso basta.</p>'
              '<p><b>En código</b> (NB05 §4): <code>with tf.GradientTape() as tape: tape.watch(x); loss = loss_fn(y, model(x))</code> → <code>g = tape.gradient(loss, x)</code> → <code>x_adv = tf.clip_by_value(x + eps * tf.sign(g), 0, 1)</code>. <b>Resultados</b> sobre la CNN normal (87.7 %): ε 0.01 → 79.1 % · 0.02 → 69.1 % · 0.05 → 39.2 % · 0.1 → 13.0 %. El primer botín de prueba: 96 % «botín»; con ε = 0.05, «zapatilla» con 67 %. Es un ataque de «caja blanca»: usa los gradientes del propio modelo.</p>',
              'a cada píxel se le suma o se le resta ε, según hacia dónde suba la pérdida; luego se recorta para que siga siendo una foto válida.')
    + formula(r'\min_\theta\; \mathbb{E}_{(x,y)}\Big[\max_{\|\delta\|_\infty \le \varepsilon} \mathcal L(\theta,\, x+\delta,\, y)\Big]',
              note='<p><b>Entrenamiento adversarial</b> (Madry et al., 2018): entrenar contra el peor cambio permitido. El NB05 aproxima el máximo de adentro con un solo paso de FGSM: cada lote son las fotos limpias más su versión FGSM con ε = 0.05, durante 5 épocas. Resultados: limpia 84.1 % · ε 0.01 → 81.6 % · 0.02 → 79.1 % · 0.05 → 71.7 % · 0.1 → 57.2 %. <b>El costo:</b> unos 3.6 puntos con fotos limpias (87.7 → 84.1) y casi el doble de cómputo por época (cada lote necesita un paso extra adelante y atrás para fabricar sus ejemplos). <b>Los límites:</b> protege contra el tipo de cambio con el que se entrenó (cada píxel ±0.05), no contra cualquiera; entrenar solo con FGSM puede dar una robustez aparente que un ataque más fuerte, de varios pasos pequeños (PGD), rompe. Para afirmar robustez hay que evaluar con ataques más fuertes que el del entrenamiento.</p>')
    + '<p><b>El mundo cambia</b> (lámina, sin notebook): los datos de uso dejan de parecerse a los de entrenamiento. Tres formas: cambian los casos, p(x) (socios rurales en un modelo entrenado con urbanos: <i>covariate shift</i>); cambia la proporción de clases, p(y) (sube la mora en una crisis); o cambia la relación, p(y | x) (el mismo perfil se comporta distinto después de la crisis). El modelo no avisa: su softmax sigue saliendo segura. Se detecta comparando la distribución de las entradas con la de entrenamiento, midiendo el desempeño por segmento cuando llegan las etiquetas y reentrenando o recalibrando cuando hace falta.</p>'
    + '<p><b>Afinar sin hacer trampa (NB05 §6).</b> Tres conjuntos: entrenamiento (para aprender los pesos), simulacro (para elegir hiperparámetros) y examen final (para reportar, una vez). Búsqueda al azar (Bergstra y Bengio, 2012) con 10 000 fotos, 4 épocas y un simulacro de 5 000: 6 combinaciones de learning rate {0.0001, 0.001, 0.01}, filtros {8, 16, 32} y dropout {0, 0.3}; en el simulacro: 85.2 · 81.0 · 69.3 · 82.2 · 86.8 · 72.6 %. La mejor (lr 0.01, 32 filtros, dropout 0.3, 34 826 parámetros) da 86.9 % en el examen final. Por qué al azar: con el mismo presupuesto prueba más valores distintos de cada hiperparámetro que una grilla, y suele haber pocos que importan. Por qué el examen una sola vez: el máximo de muchas notas con ruido está inflado (la «maldición del ganador»); si se elige mirando el examen, el examen deja de medir casos nuevos. Aquí 86.8 y 86.9 casi coinciden porque el simulacro es grande (5 000 fotos) y se probaron solo 6 combinaciones. El learning rate se busca en escala logarítmica.</p>',
    f"<p>Abre con la idea clave 1 (lámina {L('memorizar3')}): las curvas reales; pregunta en qué época pararían antes de mostrar la 33. La analogía del solucionario: 100 en los ejercicios que ya vio y falla los nuevos; validación = simulacro, prueba = examen final. Por qué memoriza ({L('por-que-memoriza')}): 12 810 perillas para 1 000 fotos. Los frenos, idea clave 2 ({L('frenos')}): el equipo que entrena sabiendo que puede faltar cualquiera (dropout), practicar con la prenda movida (aumento, {L('aumento')}) y dejar de estudiar cuando el simulacro empeora; la L2 de pasada. El resultado honesto ({L('regularizada')}): los frenos ayudan un poco (80.9 → 81.6 %) y más datos ayudan mucho (87.7 %). Las tres líneas de Keras ({L('keras-frenos')}).</p>"
    f"<p>Luego la robustez. Mover la foto ({L('aumento-mover')}): retoma el 28.2 % del recorderis y muestra el 76.4 %. La idea clave 3 ({L('adversarial')}): el botín que a la vista es el mismo y la red llama «zapatilla»; deja que adivinen qué cambió. La cuenta ({L('fgsm-cuenta')}): subir la montaña a propósito, con el Cotopaxi de la semana 1 al revés. La curva de ε y la vacuna ({L('fgsm-curva')}): 39.2 % frente a 71.7 % con ε = 0.05, y el precio con fotos limpias. El mundo cambia ({L('mundo-cambia')}): socios urbanos y rurales; «el modelo no avisa». Afinar la guitarra con el simulacro, nunca con el examen final ({L('hiperparametros')}). Después la práctica ({L('practica-nb05')}) y el cierre del tema ({L('cierre-tema1')}).</p>",
    [('¿Cuánto dropout pongo?', 'Entre 0.2 y 0.5 es lo habitual, y lo decide el simulacro. Va sobre todo antes de las capas densas; en las convolucionales se usa menos. Si la red no aprende ni en entrenamiento, sobra freno.'),
     ('¿Por qué la exactitud de validación casi no cambia pero la pérdida sube?', 'Porque la red sigue acertando más o menos lo mismo, pero se vuelve cada vez más segura, también cuando se equivoca; la entropía cruzada castiga mucho decir 99 % y fallar (el meteorólogo «seguro» de la semana 1). Por eso <code>EarlyStopping</code> mira <code>val_loss</code>.'),
     ('¿Los ejemplos adversariales son un riesgo real o un truco de laboratorio?', 'Las dos cosas. Hay ataques físicos (calcomanías en señales de tránsito, gafas que confunden el reconocimiento facial) y ataques para evadir filtros de spam o de fraude. Pero en la práctica el riesgo más común es el silencioso: el mundo cambia. La lectura lo dice: una explicación clara de un modelo que no generaliza puede ser la explicación muy clara de un error.'),
     ('¿El entrenamiento adversarial deja a la red inmune?', 'No. La protege contra el tipo y el tamaño de cambio con el que se entrenó (aquí, cada píxel ±0.05). Contra cambios más grandes, de otro tipo (girar, cambiar el brillo) o contra ataques más fuertes, puede caer. Y cuesta: 84.1 % frente a 87.7 % con fotos limpias y casi el doble de cómputo.'),
     ('¿Por qué búsqueda al azar y no probar todas las combinaciones?', 'Porque con 3 learning rates, 3 tamaños y 2 dropouts ya son 18 combinaciones, y cada hiperparámetro más las multiplica. Al azar, con el mismo presupuesto, se prueban más valores distintos de los hiperparámetros que importan (Bergstra y Bengio, 2012). Para presupuestos grandes hay métodos que aprenden de las pruebas anteriores (búsqueda bayesiana, KerasTuner).'),
     ('¿Cómo hago aumento de datos con mis propias imágenes?', 'Con capas de Keras al inicio del modelo: <code>RandomFlip</code>, <code>RandomRotation</code>, <code>RandomZoom</code>, <code>RandomTranslation</code>, <code>RandomContrast</code>. Solo las que no cambian la etiqueta: voltear una radiografía puede estar bien; voltear un texto, no.')],
    ['Celebrar la exactitud de entrenamiento.', 'Elegir hiperparámetros o la época mirando el examen final.', 'Dejar <code>restore_best_weights</code> en <code>False</code> y quedarse con la última época.', 'Creer que el ruido adversarial es al azar: está calculado con el gradiente.', 'Derivar respecto a los pesos en vez de respecto a la foto.', 'Creer que una red robusta a un ataque lo es a todo.']))

# ---- 02 · transfer learning
AP.append(bloque('b02', '02', 'Reutilizar: transfer learning',
    'Transfer learning es partir de una red que ya aprendió algo parecido y ajustarla a la tarea nueva: congelar sus capas y entrenar solo la salida, o dejar que todo se mueva un poco (ajuste fino, con un learning rate pequeño). Ayuda sobre todo cuando hay pocos datos; con suficientes, entrenar desde cero empata. Y hereda lo que la red base aprendió, incluido lo que no conocemos.',
    '<p><b>El experimento del NB06 §1.</b> Red base: la CNN de siempre entrenada 5 épocas con 6 clases que <b>no</b> son prendas de arriba (pantalón, vestido, sandalia, zapatilla, bolso, botín): 96.8 % en esas 6 clases. Tarea nueva: 4 prendas de arriba muy parecidas entre sí (camiseta, suéter, abrigo, camisa); adivinar al azar da 25 %. Examen final de 4 000 fotos; simulacro de 200.</p>'
    '<p><b>Las cuentas de los parámetros.</b> Capas convolucionales: 3·3·1·16 + 16 = 160 y 3·3·16·32 + 32 = 4 640, en total 4 800. Salida nueva: 800·4 + 4 = 3 204. Desde cero se entrenan los 8 004; congelada, solo los 3 204 de la salida (<code>base.trainable = False</code>).</p>'
    + table(['Fotos por clase para estudiar', 'Desde cero (8 004 parámetros)', 'Congelada (se entrenan 3 204)', 'Ajuste fino (lr 0.0001)'], [
        ['5 (20 fotos)', '<b>30.6 %</b>', '<b>45.9 %</b>', '<b>47.2 %</b>'],
        ['20 (80 fotos)', '61.2 %', '62.7 %', '62.7 %'],
        ['100 (400 fotos)', '<b>68.8 %</b>', '66.7 %', '68.0 %']])
    + '<p><b>Cómo leerla.</b> Con 5 fotos por clase, la experiencia heredada vale unos 15 puntos (30.6 → 45.9 %); con 20 casi nada; con 100, desde cero empata o gana. La congelada pierde con 100 porque sus filtros quedaron fijos y aprendieron de zapatos, bolsos y pantalones, no de cuellos y mangas; el ajuste fino los adapta un poco. Si la tarea de origen y la nueva se parecen poco, la herencia puede incluso estorbar (transferencia negativa). Yosinski et al. (2014) mostraron que las primeras capas aprenden cosas generales (bordes, texturas) que se transfieren bien y las últimas, cosas específicas de su tarea. En la vida real la base aprendió de millones de fotos y la ventaja es mucho mayor.</p>'
    + formula(r'\begin{gathered}\textbf{congelar: } \min_{\theta_{\text{salida}}} \mathcal L\big(\theta_{\text{base}}^{\star},\, \theta_{\text{salida}}\big) \\[8pt] \textbf{ajuste fino: } \min_{\theta_{\text{base}},\,\theta_{\text{salida}}} \mathcal L \ \text{ desde } \theta_{\text{base}}^{\star},\ \eta \text{ pequeño}\end{gathered}',
              note='<p><b>Por qué un learning rate pequeño.</b> Al empezar, la salida nueva está al azar y produce gradientes grandes; con pasos grandes esos gradientes destrozan los filtros heredados antes de que sirvan (olvido catastrófico). La receta habitual tiene dos etapas: (1) congelar la base y entrenar la salida; (2) descongelar la base (o sus últimas capas) y seguir con un learning rate 10 a 100 veces menor (1e-4 o 1e-5). En Keras, después de cambiar <code>trainable</code> hay que volver a llamar a <code>compile</code> para que el cambio cuente. Con modelos de <code>keras.applications</code> que tienen BatchNormalization, se llama a la base con <code>base(x, training=False)</code> para que esas capas no cambien sus estadísticas durante el ajuste fino.</p>')
    + '<p><b>En la vida real.</b> ImageNet (Deng et al., 2009): el subconjunto de la competencia tiene unos 1.2 millones de fotos de 1 000 clases. <code>keras.applications</code> trae redes ya entrenadas con ImageNet:</p>'
    '<pre><code>base = keras.applications.MobileNetV2(include_top=False, weights="imagenet",\n                                      input_shape=(224, 224, 3), pooling="avg")\nbase.trainable = False                       # stage 1: freeze the pretrained features\ninputs = keras.Input(shape=(224, 224, 3))\nx = keras.applications.mobilenet_v2.preprocess_input(inputs)\nx = base(x, training=False)                  # keep BatchNorm in inference mode\noutputs = keras.layers.Dense(n_classes, activation="softmax")(x)\nmodel = keras.Model(inputs, outputs)</code></pre>'
    + formula(r'W = W_0 + B A, \qquad B \in \mathbb{R}^{d \times r},\ A \in \mathbb{R}^{r \times k},\ r \ll \min(d, k)',
              [(r'W_0', 'los pesos del modelo preentrenado: congelados', B), (r'BA', 'el ajuste: dos matrices delgadas que sí se entrenan', A), (r'r', 'el rango: 4, 8 o 16', I)],
              '<p><b>LoRA</b> (Hu et al., 2022), la técnica que menciona la lectura para los modelos de lenguaje. En vez de ajustar una matriz de d × k pesos, se aprende una corrección de bajo rango: r(d + k) números. Con d = k = 4 096 y r = 8: 65 536 frente a 16 777 216, el 0.4 %. B empieza en ceros, así que al inicio el modelo es exactamente el preentrenado. Por eso se puede ajustar un modelo grande en una sola GPU y guardar muchos ajustes pequeños para un mismo modelo base.</p>',
              'el peso final es el original más una corrección hecha con dos matrices delgadas; solo se entrena la corrección.')
    + '<p><b>Lo que se hereda.</b> La lectura lo dice con la analogía del profesional con experiencia: aprende rápido, pero trae hábitos de trabajos anteriores que no conoces del todo. Un modelo preentrenado puede traer sesgos o puntos ciegos de datos que nunca vimos. Es la pregunta 5 de la encuesta («Heredar lo que no conocemos») y la pregunta 3 del checklist del cierre.</p>',
    f"<p>Abre con el repaso del Tema 1 ({L('repaso-tema1')}, 5 minutos): memorizar, frenos, exacto no es robusto. La idea clave 4 ({L('transfer')}): el profesional con experiencia y la inducción corta; pregunta qué partes de una red que conoce zapatos podrían servir para camisas. Congelar o ajuste fino ({L('congelar')}): usar su experiencia tal cual y enseñarle solo la última parte, o dejar que también ajuste un poco sus hábitos, con pasos pequeños; señala <code>base.trainable = False</code> y el learning rate de 0.0001. El resultado ({L('transfer-resultado')}): pide que apuesten antes de revelar la fila de 5 fotos y la de 100; la lección honesta es que ayuda mucho con muy pocos datos y casi nada con suficientes. En la vida real ({L('transfer-vida-real')}): ImageNet, <code>keras.applications</code> y LoRA, en un minuto.</p>",
    [('¿Qué modelo preentrenado uso para mi proyecto?', 'Para imágenes, una red de <code>keras.applications</code> (MobileNetV2 o EfficientNetB0 son livianas y funcionan en Colab). Para textos en español, un modelo de lenguaje preentrenado en español (por ejemplo, de la familia BERT) o un modelo grande ajustado con LoRA. Para tablas, el transfer learning casi no se usa: compara con boosting.'),
     ('¿Congelar o ajuste fino?', 'Con muy pocos datos, congelar (menos parámetros que aprender, menos riesgo de memorizar). Con más datos o una tarea más distinta a la original, ajuste fino con un learning rate pequeño. Lo decide el simulacro, como cualquier hiperparámetro.'),
     ('¿Por qué con 100 fotos por clase la congelada pierde contra desde cero?', 'Porque sus filtros quedaron fijos y aprendieron de prendas que no son de arriba; con suficientes datos, una red que aprende sus propios filtros los hace a la medida. El ajuste fino recupera casi todo (68.0 %).'),
     ('¿Mis fotos tienen que ser de 224 × 224 y a color?', 'Para las redes de ImageNet, sí: se redimensionan con <code>image_dataset_from_directory(..., image_size=(224, 224))</code> y, si son en escala de grises, se repite el canal tres veces. Cada red trae su función <code>preprocess_input</code>.'),
     ('¿Se puede usar un modelo preentrenado sin saber con qué datos se entrenó?', 'Técnicamente sí, y es lo más común; por eso hay que evaluarlo con datos locales, pedir la documentación del proveedor (qué datos, qué pruebas) y revisar cómo le va con cada grupo antes de usarlo con personas.')],
    ['Ajustar todo con un learning rate grande y borrar lo aprendido.', 'Cambiar <code>trainable</code> y olvidar volver a compilar.', 'Concluir que el transfer learning «no sirve» porque con 100 fotos por clase no ganó.', 'Asumir que lo preentrenado ya fue evaluado para su población.']))

# ---- 02e · explain and verify, fairness
AP.append(bloque('b02e', '02e', 'Explicar y verificar · ¿trata a todos por igual?',
    'Como nadie puede leer las reglas repartidas en miles de pesos, usamos explicaciones post hoc: mapas de calor en imágenes (oclusión, Grad-CAM) y repartos del resultado en tablas (importancia por permutación, SHAP). Son interpretaciones del modelo, no el modelo: también se verifican. Una explicación tiene dos destinatarios (el científico de datos y la persona afectada), y un modelo puede tratar distinto a dos grupos aunque no use la columna del grupo.',
    '<p><b>La red que explicamos (NB06 §2).</b> La CNN de 10 clases (87.7 %). Prendas: el primer botín (96 %), la primera camisa (77 %) y el primer bolso (99 %). Tres mapas sobre cada una.</p>'
    + formula(r'S_{ij} = p_c(x) - p_c\big(x^{\,\setminus ij}\big)',
              note='<p><b>Oclusión</b> (Zeiler y Fergus, 2014): tapar un cuadro de 6 × 6 alrededor de cada posición y medir cuánto baja la probabilidad de la clase. No necesita mirar adentro de la red (sirve para cualquier modelo) y se entiende sin fórmulas; cuesta una predicción por posición (si el cuadro avanza de a un píxel, (28 − 6 + 1)² = 529 predicciones por foto) y depende del tamaño del cuadro y del color con que se tapa.</p>',
              read='lo que pierde la clase cuando tapo esa zona; si baja mucho, esa zona importaba.')
    + formula(r'\begin{gathered}\alpha_k^c = \frac{1}{Z}\sum_{i}\sum_{j} \frac{\partial y^c}{\partial A^k_{ij}} \\[8pt] L^c_{\text{Grad-CAM}} = \operatorname{ReLU}\Big(\sum_k \alpha_k^c\, A^k\Big)\end{gathered}',
              [(r'A^k', 'el mapa k de la última capa convolucional (11 × 11; hay 32)', B), (r'y^c', 'el puntaje de la clase c', A), (r'\alpha_k^c', 'cuánto importa el mapa k para la clase c', T)],
              '<p><b>Grad-CAM</b> (Selvaraju et al., 2017): promedia el gradiente de cada mapa (cuánto empuja ese mapa hacia la clase), pondera los mapas con esos pesos y se queda con la parte positiva (ReLU: lo que empuja <i>a favor</i>). Sale un mapa de 11 × 11 que se amplía a 28 × 28: por eso se ve borroso. El artículo usa el puntaje antes de softmax. Funciona porque la última capa convolucional todavía sabe <i>dónde</i> están las cosas y ya sabe <i>qué</i> son.</p>',
              'cada mapa de la última capa vale según cuánto empuja hacia la clase; se suman los mapas con esos pesos y se queda solo lo que empuja a favor.')
    + formula(r'S = x \odot \nabla_x\, y^c',
              note='<p><b>Gradiente × imagen</b>: cuánto cambiaría el puntaje si cambia cada píxel, multiplicado por el píxel. Es barato y se ve nítido, pero al multiplicar por x el mapa se parece a la foto misma, y eso lo delata en la prueba de cordura.</p>')
    + '<p><b>La prueba de cordura</b> (Adebayo et al., 2018), prueba de aleatorización de los parámetros: misma arquitectura con pesos al azar (la red ya no sabe nada) y se vuelve a calcular cada mapa. Se compara con la correlación de Spearman (ordena los píxeles por importancia y compara los dos órdenes: 1 = idénticos, 0 = nada que ver), en 30 fotos:</p>'
    + table(['Método', 'Correlación con la red al azar', 'Veredicto'], [
        ['Grad-CAM', '−0.12', 'pasa: el mapa cambia cuando la red ya no sabe'],
        ['Oclusión', '−0.05', 'pasa'],
        ['Gradiente × imagen', '0.90', 'no pasa: casi el mismo mapa aunque la red no sepa nada; se parece a la foto, como un filtro de bordes']])
    + '<p>Coincide con el artículo: varios métodos populares de mapas de saliencia se comportan como detectores de bordes. La lección no es tirar las herramientas: es verificarlas antes de presentarlas como verdad (el traductor que sigue el tono de voz y no las palabras). El artículo propone una segunda prueba: entrenar con las etiquetas barajadas.</p>'
    '<p><b>La cooperativa ficticia (NB06 §4).</b> 6 000 socios inventados, 7 datos (ingreso, carga = cuota/ingreso, antigüedad en meses, atrasos en 12 meses, garante, ahorro en meses de ingreso, zona rural) y 12.5 % de mora. Red densa 16-8-1 (30 épocas): AUC 0.80, exactitud 89.2 %, rechaza (p ≥ 0.5) al 5.7 %.</p>'
    + formula(r'I_j = \operatorname{AUC}(f, X, y) - \operatorname{AUC}\big(f, X^{\pi_j}, y\big)',
              note='<p><b>Importancia por permutación</b> (Breiman, 2001): mezclar al azar la columna j en los datos de prueba y medir cuánto baja el AUC. Es <b>global</b>: habla del modelo con todos los socios. Resultados: carga 0.125 · atrasos 0.051 · garante 0.049 · antigüedad 0.017 · rural 0.003 · ingreso 0.003 · ahorro −0.002 (≈ 0: ruido de la mezcla). Ojo con columnas correlacionadas: la mezcla crea socios imposibles y la importancia se reparte entre las columnas que dicen lo mismo.</p>')
    + formula(r'\begin{gathered}\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!\,(|F|-|S|-1)!}{|F|!}\,\big[v(S \cup \{i\}) - v(S)\big] \\[8pt] \phi_0 + \sum_i \phi_i = f(x)\end{gathered}',
              [(r'F', 'los 7 datos de la socia', B), (r'v(S)', 'la predicción si solo se conocen los datos de S', A), (r'\phi_0', 'la base: la predicción promedio (0.13)', I)],
              '<p><b>SHAP</b> (Lundberg y Lee, 2017), basado en el valor de Shapley (1953) de la teoría de juegos. <b>En palabras simples:</b> imagina que los datos de la socia «entran» a la jugada uno por uno, en todos los órdenes posibles; el mérito de cada dato es el promedio de cuánto cambia la predicción cuando entra. Es repartir el mérito de un gol entre los jugadores que participaron en la jugada. Cumple que las contribuciones suman exactamente la diferencia entre su predicción y la base (eficiencia), que dos datos que aportan igual reciben lo mismo y que un dato que nunca cambia nada recibe cero. «No conocer» un dato se simula reemplazándolo por valores de otros socios (datos de fondo), y eso supone que los datos son independientes. Con 7 datos hay 2⁷ = 128 coaliciones por caso; con muchos datos, la librería <code>shap</code> aproxima.</p>'
              '<p><b>La socia</b> (la primera de prueba con probabilidad entre 0.6 y 0.8): ingreso $506, carga 0.29 (cuota ≈ $144), 1 mes de antigüedad, 2 atrasos, sin garante, ahorro de 1.5 meses, zona rural → probabilidad de mora 61 %: rechazada. SHAP: base 0.13 · atrasos +0.30 · rural +0.08 · sin garante +0.04 · antigüedad +0.04 · ingreso +0.02 · ahorro +0.02 · carga −0.02 → 0.13 + 0.48 = 0.61. <b>La lección:</b> lo importante en general (la carga) no es lo que más pesó en su caso (los atrasos). Explicar a una persona con la importancia global es un error.</p>',
              'el mérito de un dato es lo que cambia la predicción cuando entra, promediado sobre todos los órdenes en que pudieron entrar los demás.')
    + formula(r"x^{\star} = \arg\min_{x'} \; d(x, x') \quad \text{sujeto a} \quad f(x') < 0.5",
              note='<p><b>El contrafactual</b> (Wachter, Mittelstadt y Russell, 2018): el cambio más pequeño que daría otra decisión. Es la explicación que le sirve a la persona afectada: «¿qué tendría que cambiar para que me aprueben?». En el NB06 §5: sin los 2 atrasos su probabilidad baja a 12 %; o con una cuota de ≈ $124 en vez de $144 (carga 0.245, unos $20 menos al mes, por ejemplo con un plazo más largo) baja a 48 % y la aprobarían. <b>Solo cuentan los cambios que ella puede hacer:</b> sus atrasos pasados no se borran (ese contrafactual le sirve al científico de datos para entender el modelo), y la zona no debería ser una palanca; la cuota sí. Nota fina: la carga casi no empujó en su caso según SHAP (−0.02), pero es la palanca que ella puede mover. SHAP dice qué empujó; el contrafactual, qué cambiaría la decisión. Y el umbral de 0.5 es una decisión de la cooperativa, no del modelo.</p>')
    + '<p><b>¿Trata a todos por igual? (NB06 §6).</b> Mora real: rural 15.5 %, urbana 9.5 %. «Falsas alarmas» son socios que sí habrían pagado y el modelo rechaza.</p>'
    + table(['', 'Rechazo rural', 'Rechazo urbano', 'Falsas alarmas rural', 'Falsas alarmas urbana', 'AUC'], [
        ['Con la columna rural', '8.9 %', '3.7 %', '3.4 %', '2.2 %', '0.80'],
        ['Sin la columna rural', '6.4 %', '5.6 %', '1.6 %', '3.4 %', '0.79']])
    + '<p><b>Por qué quitar la columna no basta.</b> (1) Las otras columnas pueden delatar la zona (ingreso, ahorro, garante o antigüedad se distribuyen distinto en cada zona: variables <i>proxy</i>); a eso se le llama «equidad por desconocimiento» y casi nunca funciona sola. (2) Quitarla movió los errores: la brecha de rechazo bajó de 5.2 a 0.8 puntos, pero las falsas alarmas pasaron a la zona urbana (2.2 → 3.4 %). (3) Hay varias definiciones de «trato igual» y no se pueden cumplir todas a la vez: igual tasa de rechazo (paridad), igual tasa de falsas alarmas y de casos detectados (Hardt, Price y Srebro, 2016), o puntajes igual de calibrados en cada grupo. Cuando la mora real es distinta entre grupos (15.5 frente a 9.5 %), un puntaje calibrado no puede igualar a la vez las falsas alarmas y los casos no detectados (Kleinberg, Mullainathan y Raghavan, 2017; Chouldechova, 2017). (4) La pregunta de fondo no es solo técnica: ¿por qué la mora real es distinta? (acceso, ingresos que varían, distancia a la agencia). Qué error es más grave lo decide la institución, con las personas afectadas y la norma; el científico de datos pone los números sobre la mesa.</p>'
    + '<p><b>La IA que se explica (lectura).</b> Lindsey et al. (2025) analizaron por dentro un modelo de lenguaje: ante «¿cuál es la capital del estado donde está Dallas?» representaba Texas como paso intermedio antes de decir «Austin», y al cambiar esa representación por la de otro estado cambiaba la respuesta; al rimar, parecía elegir antes la palabra final. Los propios autores dicen que su método dio una comprensión satisfactoria en cerca de una cuarta parte de los casos. Al preguntarle cómo sumó 36 + 59 respondió con el «llevar uno» escolar, pero por dentro combinaba una estimación aproximada con el cálculo exacto de la última cifra. Con una pista escondida en la pregunta, Claude 3.7 Sonnet la mencionó en su razonamiento el 25 % de las veces que la usó y DeepSeek R1 el 39 % (Anthropic, 2025); 41 investigadores de varios laboratorios llamaron a leer ese razonamiento una oportunidad valiosa pero «frágil» (Korbak et al., 2025). Lo que un modelo dice de sí mismo es texto generado: sirve para supervisar, no es prueba.</p>',
    f"<p>Empieza por la necesidad (lámina {L('por-que-explicar')}): la socia que recibe un «no» y pregunta por qué; en Ecuador, desde marzo de 2026, puede pedir la lógica del algoritmo. La idea clave 5 ({L('donde-miro')}): tapar partes con la mano (oclusión) y el mapa de calor (Grad-CAM) sobre el botín, la camisa y el bolso; pregunta qué esperarían ver en una radiografía con «neumonía» (el pulmón, no la etiqueta del hospital). La prueba de cordura ({L('cordura')}): borra lo aprendido y vuelve a explicar; deja que adivinen cuál método no pasa antes de revelar el 0.90, y cierra con el traductor que sigue el tono de voz.</p>"
    f"<p>Luego las tablas. Explicar el crédito ({L('explicar-credito')}): primero lo importante en general (la carga) y después la socia (los atrasos, +0.30), con el gol repartido entre los jugadores; pregunta por qué no coinciden. El contrafactual ({L('contrafactual')}): pregunta cuál de los dos le sirve a ella hoy. Por zona ({L('por-zona')}): muestra la tabla con la columna, pregunta qué pasaría al quitarla y revela; termina con la pregunta que no es técnica. La IA que se explica ({L('ia-se-explica')}) y las reglas ({L('reglas')}), que abren el debate de la lectura (10 minutos, ver <a href=\"#lectura\">Lectura de tendencia</a>). Después la práctica ({L('practica-nb06')}) y el cierre del tema ({L('cierre-tema2')}).</p>",
    [('¿Cuál método de explicación uso en mi proyecto?', 'En imágenes, Grad-CAM (pasó la prueba de cordura) y la oclusión para confirmar. En tablas, la importancia por permutación para el modelo en general y SHAP para cada caso; para las personas afectadas, un contrafactual con cambios que puedan hacer. Y siempre una verificación: prueba de cordura, o comprobar que la explicación cambia cuando cambia el modelo.'),
     ('¿SHAP sirve para redes de imágenes?', 'Sí (hay versiones para redes profundas), pero con 784 píxeles es caro y los píxeles sueltos no son «jugadores» con significado. En imágenes se usa más Grad-CAM; SHAP brilla en tablas con columnas que significan algo.'),
     ('¿Qué diferencia hay entre un modelo interpretable y uno explicado?', 'Interpretable por diseño: se lee directamente (una regresión logística con pocas variables, una tabla de puntajes, un árbol pequeño). Explicado: una caja negra a la que se le aplica una explicación post hoc. Rudin (2019) sostiene que en decisiones de alto impacto conviene lo primero. Es la pregunta 1 de la encuesta.'),
     ('Si quito la columna de zona, ¿el modelo ya no discrimina?', 'No necesariamente: otras columnas pueden delatar la zona, y quitarla puede mover los errores a otro grupo (en el NB06, las falsas alarmas pasan a la zona urbana). Hay que medir por grupo, con y sin la columna, y decidir qué igualdad importa.'),
     ('¿Los pesos de atención de un Transformer son una explicación?', 'Son una pista sobre a qué miró una capa, no una explicación de toda la decisión (Jain y Wallace, 2019, en la semana 2). Igual que los mapas de calor, tendrían que pasar pruebas.'),
     ('¿Qué exige la norma de Ecuador?', 'Según la lectura: evaluaciones de impacto antes de usar sistemas de IA riesgosos, revisión humana de decisiones automatizadas con efectos jurídicos y derecho a pedir una explicación de la lógica aplicada por el algoritmo (Resolución SPDP-SPD-2026-0009-R, Registro Oficial n.º 240, 10 de marzo de 2026). Para un caso real, hay que leer la norma completa y consultar a un abogado.')],
    ['Tomar el mapa de calor como la «razón» de la red.', 'Presentar una explicación sin verificarla.', 'Explicar a una persona con la importancia global.', 'Proponer contrafactuales que la persona no puede cumplir (borrar sus atrasos, cambiar de zona).', 'Creer que borrar la columna sensible elimina el problema.', 'Tomar la «cadena de pensamiento» de un modelo de lenguaje como prueba de cómo decidió.']))

# ---- 03 · closing
AP.append(bloque('b03', '03', '¿Le creerías a tu red?',
    'El cierre convierte la semana en cinco preguntas que se hacen antes de usar un modelo con personas. No son un trámite: cada una se responde con evidencia (una curva, una prueba, una tabla por grupo) o con un plan para conseguirla. Son el esqueleto del análisis crítico ético que pide la entrega de la semana.',
    # Same five questions, same order and wording, as the deck slide «checklist» (CHK in slides_tema2.py).
    table(['Pregunta', 'Con qué se responde', 'Idea clave', 'Dónde lo vimos'], [
        ['1 · ¿Generaliza? <br><small>¿Lo medí con datos que no vio, y miré el examen final una sola vez?</small>', 'Entrenamiento, simulacro y examen final separados; curvas que no se separan; el examen final medido una vez', '1', f'láminas {L("memorizar3")}, {L("hiperparametros")} · NB05 §1, §2, §6'],
        ['2 · ¿Aguanta cambios? <br><small>Fotos movidas, ruido, otra sucursal, otra época</small>', 'Probar con fotos movidas, con ruido calculado y con datos de otra zona u otra época; vigilar los datos de uso', '3', f'láminas {L("aumento-mover")}, {L("fgsm-curva")}, {L("mundo-cambia")} · NB05 §3–5'],
        ['3 · ¿De dónde viene lo que sabe? <br><small>Si partí de una red ya entrenada, ¿sé con qué datos se formó?</small>', 'Si parte de un modelo preentrenado: con qué datos aprendió, quién lo hizo y cómo le va con datos locales', '4', f'láminas {L("transfer-resultado")}, {L("transfer-vida-real")} · NB06 §1'],
        ['4 · ¿La explicación pasa pruebas? <br><small>¿Cambia si borro lo aprendido? ¿Mira lo que debe?</small>', 'Una explicación para el equipo (¿es correcto?) y otra para la persona afectada (¿qué puedo hacer?); la prueba de cordura', '5', f'láminas {L("donde-miro")}, {L("cordura")}, {L("contrafactual")} · NB06 §2–5'],
        ['5 · ¿Trata a todos por igual y le sirve a la persona? <br><small>¿Cómo le va a cada grupo? ¿Puedo decirle qué tendría que cambiar?</small>', 'Rechazos y falsas alarmas por grupo; un contrafactual que la persona pueda usar; una persona responsable que revisa y corrige', '5', f'láminas {L("por-zona")}, {L("reglas")} · NB06 §6'],
    ]) +
    '<p><b>De dónde viene esto.</b> Las cinco preguntas son una versión corta de lo que la industria documenta en las <i>model cards</i> (Mitchell et al., 2019: para qué sirve el modelo, cómo se evaluó, cómo le va por grupo, qué limitaciones tiene) y en las <i>datasheets</i> de los datos (Gebru et al., 2021). También son lo que la norma de Ecuador empieza a exigir: evaluar el impacto, permitir la revisión humana y explicar la lógica del algoritmo.</p>'
    '<p><b>El título.</b> «¿Le creerías a tu red?» es el título del entregable de la semana 1. Entonces la pregunta era si la red acertaba; ahora es si acierta con casos nuevos, si aguanta, de dónde viene y si se puede explicar. Vale la pena decirlo en voz alta: el curso cierra el círculo.</p>',
    f"<p>Las cinco preguntas (lámina {L('checklist')}): una por clic, cada una con su número de la semana. Luego la actividad ({L('tu-proyecto3')}, ver la sección <a href=\"#proyecto\">Tu proyecto</a>), el quiz final ({L('quizfinal3')}), las tres semanas en un mapa ({L('mapa-curso')}: cómo aprende una red, qué arquitectura según los datos, ¿le creerías?), lo que viene ({L('lo-que-viene3')}: la entrega final y el video de conclusiones) y los recursos ({L('recursos3')}, QR de la guía de estudio).</p>",
    [('¿Qué tiene que llevar el análisis crítico ético de la entrega?', 'Las cinco preguntas aplicadas a su modelo, con evidencia o con un plan: cómo partieron los datos, qué cambio podría tumbarlo, qué heredó, cómo explicarían una decisión y a quién, y qué grupos compararon. El sílabo pide análisis crítico de robustez, explicabilidad, generalización y ética.'),
     ('Mi proyecto no decide sobre personas, ¿igual aplica?', 'Las preguntas 1 a 4, sí: un modelo que clasifica cultivos o piezas también tiene que funcionar con casos nuevos, aguantar cambios (otra cámara, otra temporada) y poder explicarse. La 5 se adapta: ¿le va igual en todas las regiones, cámaras o temporadas?'),
     ('¿Cómo se relaciona esto con la entrega final?', 'La entrega final es el proyecto completo; esta semana aporta la parte de generalización, optimización de hiperparámetros, transfer learning y explicación del modelo, y la reflexión sobre su uso en el contexto local.')],
    ['Responder «sí» a las cinco sin evidencia.', 'Tratar el checklist como un formulario al final del proyecto, en vez de una guía desde el principio.', 'Olvidar la revisión humana: un modelo con buenos números también necesita a alguien que responda por sus decisiones.']))

# ------------------------------------------------------------------ notebooks (tables)
NBK = f"""
{idea('Los notebooks vienen completos y ejecutados: no hay espacios para rellenar. El estudiante lee, apuesta qué saldrá, ejecuta y compara con «Qué deberías ver»; al final hay ejercicios que se responden leyendo los resultados (respuesta plegada) y 10 preguntas «Para comprobar que entendiste». Lo que cuenta es poder explicar lo que se ve, y eso no se le puede pedir a una IA.')}
<h3>Cómo correr la práctica</h3>
<ul>
<li><b>Dinámica:</b> parejas o salas de 3 en Teams. NB05: 35 minutos (30 en salas y 5 de puesta en común). NB06: 40 minutos (35 y 5).</li>
<li><b>Prioridades:</b> NB05 §1, §2 y §4 (la §3, la §5 y la §6 quedan para la casa si el tiempo aprieta: también están en las láminas). NB06 §1, §2, §3 y §4 (la §5 y la §6 están en las láminas {L('contrafactual')} y {L('por-zona')}).</li>
<li><b>Tiempo de cómputo:</b> el NB05 entrena varias redes (la que memoriza, la que tiene frenos, la aumentada, la vacunada y las 6 de la búsqueda): es el más largo. Pide que ejecuten primero la celda <b>Configuración</b> y luego <b>Ejecutar todo</b> mientras leen. El NB06 instala <code>shap</code> si falta (unos segundos).</li>
<li><b>Los números:</b> salen con <code>SEED = 2026</code>. En Colab pueden variar en el último decimal (por eso el notebook dice «alrededor de»); las conclusiones no cambian.</li>
<li><b>Si algo falla:</b> casi siempre es una celda saltada (<code>NameError</code>): <b>Entorno de ejecución → Ejecutar anteriores</b>. Cada notebook trae su recuadro «Si algo falla».</li>
</ul>
<h3>NB05 · Generalizar y ser robusto (Tema 1) · <code>NB05_generalizar_y_robustez.ipynb</code></h3>
{table(['Sección', 'Qué deberían ver', 'Pregunta para el grupo'], [
    ['§0 Los datos y la CNN de siempre', 'Fashion-MNIST (60 000 fotos para estudiar y 10 000 de examen final) y la CNN de la semana 2: Conv2D(16, 3) → MaxPooling2D → Conv2D(32, 3) → MaxPooling2D → Flatten → Dense(10), 12 810 parámetros', '¿Por qué conviene usar la misma red de la semana 2?'],
    ['§1 El estudiante que memoriza', '1 000 fotos, simulacro de 2 000, 60 épocas sin frenos: entrenamiento 96.7 %, validación 83.0 %; la pérdida de validación es mínima en la época 33 y después sube; examen final 80.9 %', '¿En qué época habrían parado y por qué?'],
    ['§2 Frenos para la memoria', 'RandomTranslation(0.05) + Dropout(0.3) + EarlyStopping(patience=8): se detiene en la época 79 y se queda con la 71; examen final 81.6 %; las curvas ya no se separan. Con las 60 000 fotos: 87.7 %', '¿Qué ayudó más: los frenos o los datos?'],
    ['§3 Mover la foto: aumento de datos', 'sin aumento 87.7 % y al mover 1/2/3/4 px 84.4 / 75.2 / 50.9 / 28.2 %; con RandomTranslation(0.15) 82.6 % y 82.6 / 82.3 / 81.1 / 76.4 %', '¿Vale la pena perder 5 puntos sin mover para aguantar 4 px?'],
    ['§4 Engañar a la red (FGSM)', 'ε 0.01 → 79.1 % · 0.02 → 69.1 % · 0.05 → 39.2 % · 0.1 → 13.0 %; el primer botín: 96 % «botín» y, con ε = 0.05, «zapatilla» con 67 %; la foto engañosa se ve igual', '¿Por qué el ruido no es al azar?'],
    ['§5 Vacunar a la red', 'entrenamiento adversarial (5 épocas, limpias + FGSM con ε = 0.05): limpia 84.1 % · ε 0.01 → 81.6 % · 0.02 → 79.1 % · 0.05 → 71.7 % · 0.1 → 57.2 %', '¿Qué se paga por la vacuna?'],
    ['§6 Afinar sin hacer trampa', '6 combinaciones al azar (10 000 fotos, 4 épocas, simulacro de 5 000): 85.2 · 81.0 · 69.3 · 82.2 · 86.8 · 72.6 %; la mejor (lr 0.01, 32 filtros, dropout 0.3, 34 826 parámetros) da 86.9 % en el examen final', '¿Por qué el examen final se mide una sola vez?'],
    ['Resumen, ejercicios y «Para comprobar» (10)', 'las ideas 1, 2 y 3 con sus números; ejercicios que se responden leyendo los resultados', '¿Qué número los sorprendió más?'],
    ['Experimento 5 (opcional)', 'cambiar un freno o un ε y comparar con el simulacro', '¿Qué conclusión sale de una sola corrida?'],
])}
<h3>NB06 · Reutilizar y explicar (Tema 2) · <code>NB06_reutilizar_y_explicar.ipynb</code></h3>
{table(['Sección', 'Qué deberían ver', 'Pregunta para el grupo'], [
    ['§0 Configuración y datos', 'Fashion-MNIST, la cooperativa ficticia (6 000 socios, 7 datos, 12.5 % de mora) y <code>shap</code> instalado', '¿Qué datos de la cooperativa usarían ustedes para decidir un crédito?'],
    ['§1 Transfer learning', 'red base con 6 clases que no son prendas de arriba: 96.8 %; 4 prendas de arriba (azar 25 %); 5 fotos por clase: 30.6 / 45.9 / 47.2 %; 20: 61.2 / 62.7 / 62.7 %; 100: 68.8 / 66.7 / 68.0 % (desde cero / congelada / ajuste fino); 8 004 parámetros desde cero y 3 204 entrenables congelada', '¿Con cuántas fotos por clase deja de valer la pena?'],
    ['§2 ¿Dónde miró la red?', 'CNN de 10 clases (87.7 %); el botín 96 %, la camisa 77 %, el bolso 99 %; tres mapas: oclusión (cuadro de 6 × 6), Grad-CAM (11 × 11, última capa convolucional) y gradiente × imagen', '¿Los tres mapas cuentan la misma historia?'],
    ['§3 La prueba de cordura', 'correlación de Spearman con la red al azar, en 30 fotos: Grad-CAM −0.12 (pasa) · oclusión −0.05 (pasa) · gradiente × imagen 0.90 (no pasa)', '¿Por qué el mapa de gradiente × imagen se parece a la foto?'],
    ['§4 Explicar una decisión de crédito', 'red 16-8-1: AUC 0.80, exactitud 89.2 %, rechaza al 5.7 %; permutación: carga 0.125 · atrasos 0.051 · garante 0.049 · antigüedad 0.017 · rural 0.003 · ingreso 0.003 · ahorro −0.002; la socia: 61 % y SHAP con base 0.13, atrasos +0.30, rural +0.08, garante +0.04, antigüedad +0.04, ingreso +0.02, ahorro +0.02, carga −0.02', '¿Por qué lo más importante en general no es lo que más pesó en ella?'],
    ['§5 Lo que le sirve a la socia', 'sin los 2 atrasos: 12 %; con una cuota de ≈ $124 en vez de $144 (unos $20 menos al mes): 48 %, aprobada', '¿Cuál de los dos contrafactuales puede usar ella hoy?'],
    ['§6 ¿Trata a todos por igual?', 'mora real rural 15.5 % y urbana 9.5 %; con la columna rural: rechazo 8.9 / 3.7 %, falsas alarmas 3.4 / 2.2 %; sin ella (AUC 0.79): rechazo 6.4 / 5.6 %, falsas alarmas 1.6 / 3.4 %', '¿Quitar la columna resolvió el problema?'],
    ['Resumen, ejercicios y «Para comprobar» (10)', 'las ideas 4 y 5 con sus números', '¿A quién le darían cada explicación?'],
    ['Experimento 6 (opcional)', 'cambiar el tamaño del cuadro de oclusión o la cantidad de fotos y comparar', '¿Qué conclusión sale de una sola corrida?'],
])}
"""

# ------------------------------------------------------------------ trend reading
LECT = f"""
{idea('La lectura «¿Puedes explicar por qué tu modelo dijo «no»? Explicabilidad, robustez y la llegada de las reglas» cierra el hilo de la semana: las redes aprenden reglas que nadie escribió, las explicamos después con herramientas que también se equivocan, un modelo exacto puede ser frágil, y las leyes empiezan a exigir explicaciones. La pregunta de fondo: cuando explicamos un modelo, ¿decimos la verdad sobre lo que hace o contamos una historia convincente?')}
<h3>La lectura en siete puntos</h3>
<ol>
<li><b>Modelos que aprendemos, no que programamos:</b> las reglas quedan repartidas en millones de números; nadie puede leerlas directamente. Y casi nadie entrena desde cero: se parte de modelos ajenos (transfer learning, LoRA), con la experiencia y los hábitos que traen.</li>
<li><b>Explicar después de entrenar:</b> Grad-CAM en imágenes (el mapa debería iluminar el pulmón, no la etiqueta del hospital) y SHAP en tablas (el mérito del gol). Son una interpretación del modelo, no el modelo.</li>
<li><b>Cuando la explicación no explica:</b> la prueba de cordura de Adebayo et al. (2018); algunos mapas casi no cambian con la red al azar. Hay que verificarlos.</li>
<li><b>Mirar adentro:</b> la interpretabilidad mecanicista (Dallas → Texas → Austin; la rima planeada), con una comprensión satisfactoria en cerca de una cuarta parte de los casos (Lindsey et al., 2025).</li>
<li><b>¿Y si le preguntamos al modelo?</b> 36 + 59 explicado con «llevar uno» aunque por dentro hizo otra cosa; la pista mencionada el 25 % y el 39 % de las veces (Anthropic, 2025); una oportunidad «frágil» (Korbak et al., 2025).</li>
<li><b>Exacto no es robusto:</b> ejemplos adversariales (Goodfellow et al., 2015) y, más común, el mundo que cambia: el modelo no avisa.</li>
<li><b>Llegan las reglas:</b> quien use IA para decidir sobre personas deberá explicar, documentar y permitir la revisión humana; lo que no está claro es si sabemos hacerlo bien.</li>
</ol>
<h3>La línea de tiempo de las reglas (lámina {L('reglas')})</h3>
{table(['Cuándo', 'Dónde', 'Qué pasó'], [
    ['diciembre de 2024', 'Brasil', 'El Senado aprobó el proyecto de ley 2338/2023, que clasifica los sistemas de IA según su riesgo. En octubre de 2026 seguía pendiente en la Cámara de Diputados (Bairo Gonzalez, 2026).'],
    ['marzo de 2026', 'Ecuador', 'La Superintendencia de Protección de Datos Personales publicó una norma para el uso de IA: evaluaciones de impacto antes de usar sistemas riesgosos, revisión humana de decisiones automatizadas con efectos jurídicos y derecho a pedir una explicación de la lógica del algoritmo (Lexis, 2026; Resolución SPDP-SPD-2026-0009-R, Registro Oficial n.º 240, 10 de marzo de 2026).'],
    ['julio de 2026', 'Unión Europea', 'El paquete «Digital Omnibus» aplazó las obligaciones del AI Act para la IA de alto riesgo, del 2 de agosto de 2026 al 2 de diciembre de 2027 (Orrick, 2026).'],
    ['octubre de 2026', 'Ecuador', 'La Asamblea Nacional tramitaba 12 proyectos de ley sobre IA; uno propone una ley orgánica de gobernanza con el derecho a recibir explicaciones (El Diario, 2026).'],
])}
<p>Cómo contarla: la dirección es clara (explicar, documentar, revisión humana), y el aplazamiento europeo muestra lo difícil que es convertir «transparencia» en requisitos técnicos verificables. Conecta con la semana: la prueba de cordura es exactamente un requisito técnico verificable para una explicación.</p>
<h3>El debate en clase (10 minutos, al terminar la lámina {L('reglas')})</h3>
<p>Elige uno de los cuatro debates abiertos de la lectura (o deja que voten en el chat). Pide una respuesta de una línea por grupo, con un número de la semana como argumento.</p>
{table(['Debate de la lectura', 'Pregunta para lanzar', 'Lo que debería salir'], [
    ['Interpretable o explicado', '¿Cuánta exactitud estarías dispuesto a sacrificar por entender un modelo que decide créditos?', 'Rudin (2019): en decisiones de alto impacto, modelos interpretables por diseño. El otro lado: los profundos son más exactos y basta con explicarlos bien. Con números: depende de cuánto se pierda y de quién se afecta; y «explicarlo bien» incluye verificar la explicación.'],
    ['Explicación o verdad', 'Si una explicación es clara pero no refleja lo que el modelo calcula, ¿es mejor que nada?', 'Genera confianza falsa. La prueba de cordura (gradiente × imagen: 0.90) y el 36 + 59 son los ejemplos: suena razonable y no es verdad.'],
    ['Regular ahora o esperar', 'Si la ciencia de explicar todavía es inmadura, ¿corremos el riesgo de que explicar se vuelva un trámite sin contenido?', 'Los derechos no esperan, pero una norma sin capacidad técnica se cumple en el papel. Lo que haría falta: explicaciones verificables, auditores, revisión humana real.'],
    ['Reutilizar o entender', 'El transfer learning ahorra datos y cómputo, pero heredamos lo que no podemos auditar: ¿dónde está el límite?', 'Con 5 fotos por clase la herencia vale 15 puntos; a cambio, hay que evaluar con datos locales y revisar por grupo antes de usarla con personas.'],
])}
<p>La lectura está en <a href="../material/Lectura_tendencia_Semana3.pdf">semana3/material/Lectura_tendencia_Semana3.pdf</a>. Para profundizar, la propia lectura recomienda las figuras interactivas de Lindsey et al. (2025), el artículo de Rudin (2019) y la figura principal de Adebayo et al. (2018).</p>
"""

# ------------------------------------------------------------------ trend survey + video
ENC = f"""
{idea('La encuesta tiene 5 preguntas de opinión, de opción múltiple y sin respuestas correctas: cada opción es una postura razonable. Sirve dos veces: en clase, como disparador de discusión, y después, como el insumo del video de conclusiones.')}
<p>Se responde <b>después de leer</b> la lectura (Canvas). El PDF está en <a href="Encuesta_tendencia_Semana3.pdf">Encuesta_tendencia_Semana3.pdf</a>.</p>
<h3>Las 5 preguntas como disparadores de discusión</h3>
{table(['Pregunta de la encuesta', 'Las cuatro posturas, en corto', 'Para lanzar en clase', 'Con qué conectarla'], [
    ['1 · Exactitud o comprensión', 'A: entender vale más que unos puntos · B: el más exacto, con explicaciones verificadas · C: depende de cuánto se pierda · D: que decidan también los afectados', '«Si un modelo que se lee directamente acierta 2 puntos menos que la red, ¿cuál usarían para decidir créditos?»', f'Rudin (2019); la red de la cooperativa (AUC 0.80); lámina {L("explicar-credito")}'],
    ['2 · ¿Qué es una buena explicación?', 'A: qué tendría que cambiar · B: qué variables pesaron (SHAP) · C: lenguaje sencillo y una persona que revise · D: cómo se construyó y se evalúa el modelo', '«A la socia, ¿qué le dirían: sus valores SHAP o qué tendría que cambiar?»', f'los dos destinatarios; el contrafactual de la cuota (61 % → 48 %); lámina {L("contrafactual")}'],
    ['3 · Las explicaciones de la propia IA', 'A: útiles para supervisar, nunca como prueba · B: escepticismo · C: punto de partida que se contrasta · D: mejorará si los laboratorios invierten', '«Si un asistente explica cómo llegó a su respuesta, ¿eso prueba cómo la obtuvo?»', f'36 + 59; 25 % y 39 %; «frágil»; lámina {L("ia-se-explica")} y la prueba de cordura'],
    ['4 · Regular en un campo que cambia', 'A: regular pronto · B: gradual, por riesgo · C: más capacidades que leyes · D: construirla con la región', '«¿Hizo bien Ecuador en regular antes que la Unión Europea?»', f'la línea de tiempo; el debate «regular ahora o esperar»; lámina {L("reglas")}'],
    ['5 · Heredar lo que no conocemos', 'A: evaluarlo con datos locales · B: exigir información al proveedor · C: revisar sesgos contra grupos · D: una persona responsable que revise', '«Si su proyecto parte de un modelo preentrenado, ¿qué le pedirían antes de usarlo con datos ecuatorianos?»', f'la tabla 5/20/100; por zona; la pregunta 3 del checklist; láminas {L("transfer-resultado")} y {L("por-zona")}'],
])}
<p><b>Cómo usarla:</b> si ya hay respuestas, muestra la distribución de una o dos preguntas y pide a alguien de la opción menos votada que la defienda en 30 segundos. Si todavía no, lanza la pregunta tal cual y pide la letra en el chat. Ninguna opción es la correcta: lo que se evalúa es el argumento, y el mejor argumento usa un número de la semana.</p>
<h3>Cómo alimenta el video de conclusiones</h3>
<p>El video (1 a 3 minutos) lo grabas con los resultados de la encuesta y se sube en Canvas debajo de ella. Un guion que funciona:</p>
<ol>
<li><b>[0:00–0:15] Contexto:</b> «Esta semana leímos sobre explicabilidad, robustez y la llegada de las reglas; respondieron N estudiantes».</li>
<li><b>[0:15–1:30] Tres hallazgos:</b> dato → interpretación → conexión con la clase. Por ejemplo: la pregunta más dividida (con sus porcentajes) y el argumento de cada lado; la pregunta con más consenso; y una cifra de la semana que lo ilumina (gradiente × imagen 0.90 en la prueba de cordura, la pista mencionada el 25 % de las veces, la herencia que vale 15 puntos con 5 fotos por clase).</li>
<li><b>[1:30–2:15] Para sus proyectos:</b> la pregunta del checklist que más les cuesta y qué evidencia la respondería.</li>
<li><b>[2:15–2:45] Cierre y puente:</b> la entrega final.</li>
</ol>
<p>Tono oral y frases cortas (unas 130 a 150 palabras por minuto). Los porcentajes salen solo de los resultados reales de la encuesta: si faltan, no se estiman.</p>
"""

# ------------------------------------------------------------------ project activity
PROY = f"""
{idea('La actividad conecta la semana con el proyecto de titulación: cada grupo aplica las cinco preguntas de «¿Le creerías a tu red?» a su propio modelo, con la evidencia que ya tiene o con el plan para conseguirla.')}
<h3>Cómo correrla (20 minutos, lámina {L('tu-proyecto3')})</h3>
<ol>
<li><b>2 minutos:</b> recuerda las cinco preguntas (lámina {L('checklist')}) y muestra la plantilla.</li>
<li><b>13 minutos en salas</b> con los grupos del proyecto. Pasa por las salas y pregunta siempre lo mismo: «¿qué evidencia tienen para esa respuesta?».</li>
<li><b>5 minutos de puesta en común:</b> cada grupo pega su plantilla en el chat; comenta dos o tres en voz alta, sobre todo las que respondieron «sí» sin evidencia y las que encontraron una pregunta que no pueden responder.</li>
</ol>
<h3>La plantilla (para pegar en el chat)</h3>
<pre><code>Grupo: …        Modelo y datos: …
1. Casos nuevos: ¿cómo partimos entrenamiento, simulacro y examen final? ¿qué muestran las curvas? …
2. Cambios: ¿qué cambio pequeño o del mundo podría tumbarlo? ¿cómo lo vamos a probar? …
3. Herencia: ¿partimos de un modelo preentrenado? ¿de quién, con qué datos? …
4. Explicación: ¿a quién se la daríamos, con qué método, y cómo la vamos a verificar? …
5. Trato igual: ¿qué grupos vamos a comparar? ¿quién revisa las decisiones? …
En cada una: «sí, con esta evidencia» o «todavía no: lo comprobaremos así».</code></pre>
<h3>Qué buscar en las respuestas</h3>
<ul>
<li>Que haya un examen final que no se usó para decidir nada (pregunta 1).</li>
<li>Que la prueba de robustez tenga sentido para sus datos: otra cámara, otra temporada, otra región, otro año (pregunta 2).</li>
<li>Que, si usan un modelo preentrenado, sepan de dónde viene y lo evalúen con datos locales (pregunta 3).</li>
<li>Que distingan la explicación para el equipo de la explicación para la persona afectada, y que piensen cómo verificarla (pregunta 4).</li>
<li>Que nombren al menos un grupo para comparar y una persona responsable (pregunta 5).</li>
</ul>
<p>La entrega de la semana (componente práctico del sílabo: generalización, optimización de hiperparámetros, transfer learning y explicación de modelos, sobre el proyecto) sale de esta plantilla, y sus cinco respuestas son el esqueleto del apartado de <b>análisis crítico ético</b> que pide la semana 3.</p>
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


QZ_USE = f"""<h3>Cómo se usa</h3>
<ol>
<li><b>Al empezar la semana, lámina {L('prequiz3')}:</b> escanean el QR (o abren <a href="{W3}quiz/?pre">el pre-quiz</a>), escriben nombre y apellido y juegan.</li>
<li>Al final la página les da un código para pegar en el chat de Teams.</li>
<li><b>Al cerrar la semana, lámina {L('quizfinal3')}:</b> lo mismo con <a href="{W3}quiz/?final">el quiz final</a>, con el mismo nombre.</li>
<li>Después de clase: copia el chat y pégalo en <a href="Resultados_quiz.html">Resultados_quiz.html</a> → <b>Analizar</b>: promedio de cada quiz, antes y después de cada idea clave y preguntas a reforzar.</li>
</ol>
<p>Para jugarlo proyectado: <a href="{W3}quiz/?clase">modo proyector</a> (sin puntos, con «Mostrar respuesta»).</p>"""

if HAVE_BANK:
    QZ = f"""
{idea('Los quizzes son formativos y miden avance: cinco ideas clave aparecen en los dos con otra versión. El pre-quiz dice de dónde parte el grupo; el quiz final, cuánto se movió en cada idea.')}
{QZ_USE}
<h3>Las 5 ideas clave (pre ↔ final)</h3>
{table(['Idea clave', 'Pre-quiz', 'Quiz final'], [[f"{c[1:]}. {CLAVES[c]}", ', '.join(str(i + 1) for i, q in enumerate(PRE) if q.get('clave') == c) or '—', ', '.join(str(i + 1) for i, q in enumerate(FINAL) if q.get('clave') == c) or '—'] for c in CLAVES])}
<h3>Pre-quiz ({len(PRE)} preguntas)</h3>
{table(['#', 'Pregunta', 'Respuesta', 'Tema', 'Qué mide'], qrows(PRE))}
<h3>Quiz final ({len(FINAL)} preguntas)</h3>
{table(['#', 'Pregunta', 'Respuesta', 'Tema', 'Qué mide'], qrows(FINAL))}
<p><b>Cómo leerlo:</b> en las ideas clave esperas un salto claro desde el pre-quiz; una ganancia normalizada de 0.3 a 0.7 es lo habitual. Si una idea sube menos de 20 puntos, retómala en la sesión de cierre del curso, antes de la entrega final.</p>
"""
else:
    QZ = f"""
{idea('Los quizzes son formativos y miden avance: cinco ideas clave aparecen en los dos con otra versión.')}
{QZ_USE}
<p>La clave del pre-quiz y del quiz final aparece aquí al reconstruir esta guía cuando exista el banco de preguntas (<code>banco3.py</code>). Las ideas clave que miden son las cinco de la <a href="#uso">primera sección</a>.</p>
"""

# ------------------------------------------------------------------ FAQ
FAQ = [
    ('¿Por qué el notebook dice «alrededor de»?', 'Porque Colab puede usar otro procesador y los cálculos en coma flotante cambian en el último decimal. Con SEED = 2026 las conclusiones son las mismas.'),
    ('¿Las prácticas tienen nota?', 'No. NB05 y NB06 son prácticas en clase ya resueltas y explicadas: se aprenden leyendo, prediciendo y explicando lo que se ve. Lo que se registra son el pre-quiz y el quiz final, y solo para medir el avance.'),
    ('No me corre el notebook en Colab, ¿qué hago?', '1) Entorno de ejecución → Reiniciar y ejecutar todo. 2) Verifica que ejecutaste la celda Configuración. 3) Si falla la instalación de <code>shap</code> en el NB06, ejecuta de nuevo esa celda. 4) Copia el error en el chat de Teams.'),
    ('¿Necesito GPU?', 'No: los dos corren con la CPU gratuita de Colab. El NB05 es el más largo porque entrena varias redes; con GPU (Entorno de ejecución → Cambiar tipo de entorno) va bastante más rápido.'),
    ('¿Qué es «generalizar»?', 'Que le vaya bien con casos que no vio al aprender. Se mide con datos que la red nunca usó: el simulacro para decidir y el examen final para reportar.'),
    ('¿Cuál es la diferencia entre robustez y generalización?', 'Generalizar es funcionar con casos nuevos parecidos a los de entrenamiento; robustez es seguir funcionando cuando los casos cambian un poco (una foto movida, un ruido, otra zona). Un modelo puede generalizar bien y ser frágil: 87.7 % en el examen final y 39.2 % con un ruido invisible.'),
    ('¿Y la «optimización» del sílabo?', 'Es la optimización de hiperparámetros: elegir learning rate, filtros, dropout o épocas con el simulacro (NB05 §6). La optimización de los pesos (Adam, descenso de gradiente) se vio en las semanas 1 y 2.'),
    ('¿Puedo usar SHAP con cualquier modelo?', 'Sí: la librería <code>shap</code> tiene versiones para modelos de árboles, redes y cualquier función (más lenta). Para tablas con muchas filas, se usa una muestra de fondo de unos cientos de casos.'),
    ('¿La cooperativa del NB06 es real?', 'No: son 6 000 socios inventados con reglas plausibles, para poder hablar de crédito sin datos personales. Las conclusiones sobre métodos valen; las cifras de mora no describen a ninguna cooperativa real.'),
    ('¿Dónde aprendo más de explicabilidad?', 'El libro gratuito <i>Interpretable Machine Learning</i> de Christoph Molnar y las tres lecturas que recomienda la lectura de tendencia: Lindsey et al. (2025), Rudin (2019) y Adebayo et al. (2018).'),
]

GLOS_D = [
    ('Ajuste fino', 'Seguir entrenando toda la red preentrenada (o parte) con la tarea nueva y un learning rate pequeño.'),
    ('Aumento de datos', 'Transformar las fotos al azar al entrenar (moverlas, girarlas) sin cambiar su etiqueta.'),
    ('Cambio de distribución', 'Cuando los datos de uso dejan de parecerse a los de entrenamiento (data shift).'),
    ('Congelar', 'Fijar los pesos de una parte de la red (<code>trainable = False</code>) y entrenar solo el resto.'),
    ('Contrafactual', 'El cambio más pequeño en los datos de un caso que daría otra decisión.'),
    ('Dropout', 'Apagar al azar una fracción de las neuronas en cada paso de entrenamiento.'),
    ('Early stopping', 'Parar el entrenamiento cuando la pérdida del simulacro deja de mejorar y quedarse con la mejor época.'),
    ('Ejemplo adversarial', 'Una entrada con un cambio pequeño, calculado a propósito, que hace fallar al modelo.'),
    ('Entrenamiento adversarial', 'Entrenar también con ejemplos adversariales para que el modelo los aguante.'),
    ('Épsilon (ε)', 'El tamaño máximo del cambio por píxel en un ataque.'),
    ('Falsa alarma', 'Un caso que el modelo marca como riesgoso y no lo era (aquí, un socio que habría pagado y se rechaza).'),
    ('FGSM', 'Fast gradient sign method: mover cada píxel ε en la dirección del signo del gradiente de la pérdida.'),
    ('Grad-CAM', 'Mapa de calor con los mapas de la última capa convolucional ponderados por su gradiente.'),
    ('Gradiente × imagen', 'Mapa de saliencia: el gradiente del puntaje respecto a cada píxel multiplicado por el píxel.'),
    ('Hiperparámetro', 'Lo que se elige antes de entrenar (learning rate, filtros, dropout, épocas), no lo que aprende la red.'),
    ('Importancia por permutación', 'Cuánto empeora el modelo si se mezcla al azar una columna; es una medida global.'),
    ('Interpretabilidad mecanicista', 'Estudiar los mecanismos internos de una red, como un biólogo estudia los órganos.'),
    ('L2 (weight decay)', 'Castigar la suma de los pesos al cuadrado para que no crezcan.'),
    ('LoRA', 'Ajustar un modelo grande aprendiendo solo una corrección de bajo rango de sus matrices.'),
    ('Oclusión', 'Tapar partes de la entrada y medir cuánto baja la predicción.'),
    ('Post hoc', 'Una explicación que se calcula después de entrenar, mirando al modelo desde afuera.'),
    ('Proxy', 'Una variable que delata a otra que se quitó (la zona a partir del ingreso o del ahorro).'),
    ('Prueba de cordura', 'Comprobar que una explicación cambia cuando se borra lo que aprendió la red.'),
    ('Regularización', 'Todo lo que frena la memorización: dropout, aumento, early stopping, L2, más datos.'),
    ('SHAP', 'Reparto de una predicción entre los datos del caso según los valores de Shapley.'),
    ('Sobreajuste', 'Memorizar los ejemplos de entrenamiento y fallar con casos nuevos.'),
    ('Transfer learning', 'Reutilizar lo que una red aprendió en una tarea para otra tarea.'),
]

REFS = """
<h3>Referencias de la lectura de tendencia</h3>
<ul>
<li>Adebayo, J., Gilmer, J., Muelly, M., Goodfellow, I., Hardt, M. y Kim, B. (2018). Sanity checks for saliency maps. En <i>Advances in Neural Information Processing Systems 31</i> (pp. 9505–9515). https://papers.nips.cc/paper/8160-sanity-checks-for-saliency-maps</li>
<li>Anthropic. (2025, 3 de abril). <i>Reasoning models don't always say what they think</i>. https://www.anthropic.com/research/reasoning-models-dont-say-think</li>
<li>Bairo Gonzalez. (2026, 4 de octubre). <i>Bill 2338/2023: Where Brazil's AI legal framework stands in 2026</i>. https://bairogonzalez.com/en/in-the-world/ia/pl-2338-brazil-ai-legal-framework-2026/</li>
<li>El Diario. (2026, 11 de octubre). <i>Ecuador busca definir reglas para el uso de la inteligencia artificial: estas son las propuestas de ley</i>. https://www.eldiario.ec/ecuador/ecuador-reglas-leyes-inteligencia-artificial-11102026/</li>
<li>Goodfellow, I. J., Shlens, J. y Szegedy, C. (2015). Explaining and harnessing adversarial examples. En <i>International Conference on Learning Representations (ICLR 2015)</i>. https://arxiv.org/abs/1412.6572</li>
<li>Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L. y Chen, W. (2022). LoRA: Low-rank adaptation of large language models. En <i>International Conference on Learning Representations (ICLR 2022)</i>. https://arxiv.org/abs/2106.09685</li>
<li>Korbak, T., Balesni, M., Barnes, E., Bengio, Y. y otros. (2025). <i>Chain of thought monitorability: A new and fragile opportunity for AI safety</i> [Preprint]. arXiv. https://arxiv.org/abs/2507.11473</li>
<li>Lexis. (2026). <i>Registro Oficial del día: Superintendencia de Protección de Datos expide norma para el uso de inteligencia artificial</i>. https://www.lexis.com.ec/noticias/registro-oficial-del-dia-superintendencia-de-proteccion-de-datos-expide-norma-para-el-uso-de-inteligencia-artificial</li>
<li>Lindsey, J., Gurnee, W., Ameisen, E., Chen, B., Pearce, A. y otros. (2025, 27 de marzo). On the biology of a large language model. <i>Transformer Circuits Thread</i>. https://transformer-circuits.pub/2025/attribution-graphs/biology.html</li>
<li>Lundberg, S. M. y Lee, S.-I. (2017). A unified approach to interpreting model predictions. En <i>Advances in Neural Information Processing Systems 30</i> (pp. 4765–4774). https://arxiv.org/abs/1705.07874</li>
<li>Orrick. (2026, 29 de julio). <i>EU AI Act update: Digital Omnibus finalizes 8 compliance changes</i>. https://www.orrick.com/en/Insights/2026/07/EU-AI-Act-Update-Digital-Omnibus-Finalizes-8-Compliance-Changes</li>
<li>Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. <i>Nature Machine Intelligence, 1</i>(5), 206–215. https://doi.org/10.1038/s42256-019-0048-x</li>
<li>Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D. y Batra, D. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. En <i>Proceedings of the IEEE International Conference on Computer Vision (ICCV)</i> (pp. 618–626). https://arxiv.org/abs/1610.02391</li>
<li>Superintendencia de Protección de Datos Personales. (2026). <i>Norma general para la garantía del derecho de protección de datos personales en el uso de sistemas de inteligencia artificial</i> (Resolución SPDP-SPD-2026-0009-R). Registro Oficial n.º 240, 10 de marzo de 2026.</li>
</ul>
<h3>Referencias complementarias de los apuntes (trabajos clásicos)</h3>
<ul>
<li>Belkin, M., Hsu, D., Ma, S. y Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. <i>Proceedings of the National Academy of Sciences, 116</i>(32), 15849–15854. https://doi.org/10.1073/pnas.1903070116</li>
<li>Bergstra, J. y Bengio, Y. (2012). Random search for hyper-parameter optimization. <i>Journal of Machine Learning Research, 13</i>, 281–305.</li>
<li>Breiman, L. (2001). Random forests. <i>Machine Learning, 45</i>(1), 5–32. https://doi.org/10.1023/A:1010933404324</li>
<li>Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. <i>Big Data, 5</i>(2), 153–163. https://doi.org/10.1089/big.2016.0047</li>
<li>Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K. y Fei-Fei, L. (2009). ImageNet: A large-scale hierarchical image database. En <i>2009 IEEE Conference on Computer Vision and Pattern Recognition</i> (pp. 248–255).</li>
<li>Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H. y Crawford, K. (2021). Datasheets for datasets. <i>Communications of the ACM, 64</i>(12), 86–92. https://doi.org/10.1145/3458723</li>
<li>Hardt, M., Price, E. y Srebro, N. (2016). Equality of opportunity in supervised learning. En <i>Advances in Neural Information Processing Systems 29</i> (pp. 3315–3323).</li>
<li>Kleinberg, J., Mullainathan, S. y Raghavan, M. (2017). Inherent trade-offs in the fair determination of risk scores. En <i>8th Innovations in Theoretical Computer Science Conference (ITCS 2017)</i> (LIPIcs 67, 43:1–43:23).</li>
<li>Madry, A., Makelov, A., Schmidt, L., Tsipras, D. y Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. En <i>International Conference on Learning Representations (ICLR 2018)</i>. https://arxiv.org/abs/1706.06083</li>
<li>Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D. y Gebru, T. (2019). Model cards for model reporting. En <i>Proceedings of the Conference on Fairness, Accountability, and Transparency</i> (pp. 220–229). https://doi.org/10.1145/3287560.3287596</li>
<li>Shapley, L. S. (1953). A value for n-person games. En H. W. Kuhn y A. W. Tucker (Eds.), <i>Contributions to the theory of games II</i> (pp. 307–317). Princeton University Press.</li>
<li>Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I. y Salakhutdinov, R. (2014). Dropout: A simple way to prevent neural networks from overfitting. <i>Journal of Machine Learning Research, 15</i>(56), 1929–1958.</li>
<li>Wachter, S., Mittelstadt, B. y Russell, C. (2018). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. <i>Harvard Journal of Law &amp; Technology, 31</i>(2), 841–887.</li>
<li>Xiao, H., Rasul, K. y Vollgraf, R. (2017). <i>Fashion-MNIST: A novel image dataset for benchmarking machine learning algorithms</i> [Preprint]. arXiv. https://arxiv.org/abs/1708.07747</li>
<li>Yosinski, J., Clune, J., Bengio, Y. y Lipson, H. (2014). How transferable are features in deep neural networks? En <i>Advances in Neural Information Processing Systems 27</i> (pp. 3320–3328).</li>
<li>Zeiler, M. D. y Fergus, R. (2014). Visualizing and understanding convolutional networks. En <i>Computer Vision – ECCV 2014</i> (LNCS 8689, pp. 818–833). Springer.</li>
</ul>
<p>Jain y Wallace (2019), citado en una pregunta, está en las referencias de la guía docente de la semana 2.</p>
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
for sid, n, title, inner in [('notebooks', '4', 'Los notebooks: qué deberían ver y cómo correr la práctica', NBK),
                             ('lectura', '5', 'Lectura de tendencia: resumen, reglas y debate', LECT),
                             ('encuesta', '6', 'Encuesta de tendencia y video de conclusiones', ENC),
                             ('proyecto', '7', 'Actividad «tu proyecto»', PROY),
                             ('quizzes', '8', 'Clave de los quizzes', QZ),
                             ('faq', '9', 'Preguntas generales que te pueden hacer',
                              '<input id="search" class="search" type="search" placeholder="Buscar en las preguntas y el glosario…" aria-label="Buscar">' + ''.join(qa(q, a) for q, a in FAQ)),
                             ('glosario', '10', 'Glosario docente', '<dl class="glos">' + ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS_D) + '</dl><p>El glosario básico de los estudiantes está en la guía de estudio.</p>'),
                             ('refs', '11', 'Referencias', REFS)]:
    body += section(sid, chip('Docente', 'amber'), title, inner, 'Revisado')
    toc.append((sid, n, title))

extra = ('<p style="margin:14px 0 0;font-size:14px"><a href="index.html">← Panel del profesor</a><br>'
         '<a href="../../docencia/Guia_docente.html">Guía docente de la semana 1</a><br>'
         '<a href="../../semana2/docencia/Guia_docente.html">Guía docente de la semana 2</a></p>')
html = page('Guía docente y apuntes · Semana 3 · Deep Learning UIDE',
            'Material solo para el docente: plan, apuntes con rigor y claves de la semana 3 (generalizar, robustez, transfer learning y explicabilidad).',
            toc, body, 'dl-uide-w3-docente', extra_toc=extra, katex=KATEX, week=3)
html = html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'Guia_docente.html').write_text(html)
print('docente semana 3 built', len(html) // 1024, 'KB', '| quiz key:', 'yes' if HAVE_BANK else 'pending (no banco3.py)',
      '| week-1/2 slides:', 'yes' if SL1 and SL2 else 'missing')
if MISSING:
    print('warning: slide ids not in slides.json:', ', '.join(sorted(MISSING)))
