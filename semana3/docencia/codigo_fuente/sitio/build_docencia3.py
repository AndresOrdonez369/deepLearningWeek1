"""Week-3 teacher panel: semana3/docencia/index.html (slides, concept maps, code in Colab, guide, quizzes, reading and survey).
usage: python build_docencia3.py <semana3/docencia folder>      (reads <folder>/slides/slides.json)
Also copies the trend survey PDF next to the panel (semana3/docencia/Encuesta_tendencia_Semana3.pdf) when the source
exists. Slide ids that are missing from slides.json are reported and printed as «?»."""
import json, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit_docencia3 import CSS, WEEKS_CSS, weeks  # noqa: E402

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docencia3')
SITE = "https://deeplearningweek1.vercel.app/"
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana3/proyectos/"
SURVEY_SRC = pathlib.Path('/home/claude/w1/tendencias/final/Encuesta_tendencia_Semana3.pdf')
SL = {s['id']: s['n'] for s in json.loads((OUT / 'slides' / 'slides.json').read_text())}
N_SLIDES = len(SL)
MISSING = set()


def L(i):
    if i not in SL:
        MISSING.add(i)
        return '?'
    return SL[i]


def R(a, b):
    return f'{L(a)}–{L(b)}'


# the deck is one sequence organized by themes (each session starts where the previous one ended)
PARTS = [('Encuadre', 'portada3', 'metas3'), ('00 · Recorderis: semanas 1 y 2', 'b00', 'recorderis3-preguntas'),
         ('Tema 1 · Generalizar y ser robusto', 'b01', 'cierre-tema1'), ('Tema 2 · Reutilizar y explicar', 'b02', 'cierre-tema2'),
         ('Cierre · ¿Le creerías a tu red?', 'b03', 'recursos3')]
NB = [("NB05 · Generalizar y ser robusto", f"Tema 1 · práctica en clase (lámina {L('practica-nb05')}) · 35 minutos · prioridad §1, §2 y §4", "NB05_generalizar_y_robustez.ipynb"),
      ("NB06 · Reutilizar y explicar", f"Tema 2 · práctica en clase (lámina {L('practica-nb06')}) · 40 minutos · prioridad §1 a §4", "NB06_reutilizar_y_explicar.ipynb")]


def card(title, text, links):
    btns = ''.join(f'<a class="btn {k}" href="{h}">{t}</a>' for t, h, k in links)
    return f'<article class="c"><h3>{title}</h3><p>{text}</p><div class="btnrow">{btns}</div></article>'


code = ''.join(card(t, w, [('Abrir en Colab ↗', COLAB + f, ''), ('Ver en GitHub', f'{REPO}/blob/main/semana3/proyectos/{f}', 'ghost')]) for t, w, f in NB)
KEYS = [('→ · espacio · PageDown', 'avanzar un paso (los clickers de presentación funcionan)'), ('← · PageUp', 'retroceder'),
        ('P', 'vista del presentador en otra ventana: notas, reloj y lámina siguiente'), ('G', 'índice de todas las láminas'),
        ('F', 'pantalla completa'), ('L', 'puntero láser, más visible que el mouse en Teams'), ('B', 'pantalla negra'),
        ('número + Enter', 'ir a una lámina')]
SHORT = [('Inicio de la semana 3', 'semana3'), ('Pre-quiz', 'pre3'), ('Quiz final', 'final3'), ('NB05 en Colab', 'nb05'), ('NB06 en Colab', 'nb06'),
         ('Guía de estudio', 'guia3'), ('Slides', 'slides3')]

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Docencia · Semana 3 · Deep Learning UIDE</title>
<meta name="description" content="Panel del profesor de la semana 3: slides interactivas, mapas conceptuales, código en Colab, guía docente, quizzes, lectura y encuesta de tendencia.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}{WEEKS_CSS}
.wrap{{max-width:1120px;margin:0 auto;padding:24px 16px 64px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:14px}}
.c{{display:flex;flex-direction:column;gap:6px;background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:18px}}
td a,.sec p a{{overflow-wrap:anywhere}} .hero h1{{overflow-wrap:anywhere}}
.c h3{{margin:0}} .c p{{margin:0;font-size:15.5px}} .c .btnrow{{margin-top:auto;padding-top:8px}}
kbd{{font-family:'JetBrains Mono',monospace;font-size:14px;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:1px 7px}}
@media (max-width:520px){{.cards{{grid-template-columns:1fr}}}}
</style></head>
<body><div class="wrap">
<div class="hero">{weeks(3, '../../docencia/index.html', '../../semana2/docencia/index.html', 'index.html')}<br><span class="chip">Docencia · Semana 3</span>
<h1 style="margin-top:14px">Panel del profesor</h1>
<p>Todo para dictar la semana 3, organizada en <b>dos temas</b> después de un recorderis de las semanas 1 y 2: <b>generalizar y ser robusto</b> (¿funcionará con casos nuevos?) y <b>reutilizar y explicar</b> (transfer learning y explicabilidad). El cierre es la pregunta del entregable de la semana 1: <b>¿le creerías a tu red?</b> Aquí están las slides, los mapas conceptuales, el código para mostrar en Colab, tu guía, los quizzes y la lectura con su encuesta. Las prácticas son en clase y sin nota.</p>
<p style="font-size:15px">Semana 3 · noviembre de 2026 · Microsoft Teams. Las láminas son una sola secuencia por temas: cada sesión empieza donde terminó la anterior.</p>
<p style="font-size:15px"><a href="../index.html" style="color:#B8C4D6">← Página de los estudiantes</a></p></div>

<section class="sec"><h2>1 · Para dictar</h2>
<div class="cards">
{card('Slides interactivas', f'{N_SLIDES} láminas con demos en vivo, por temas: ' + ' · '.join(f'{t.split(" · ")[0]} {R(a, b)}' for t, a, b in PARTS) + '. Cada lámina trae notas con el guion, la pregunta para la clase y el tiempo sugerido.', [('Abrir las slides', 'slides/index.html', ''), ('Vista del presentador', 'slides/index.html?presenter', 'ghost'), ('PDF de respaldo', 'Slides_Semana3.pdf', 'ghost')])}
{card('Mapas conceptuales', 'La semana completa y un mapa por bloque: recorderis de las semanas 1 y 2, Tema 1, Tema 2 y el cierre. Clic en cada concepto: qué decir, un ejemplo, una pregunta para la clase, el error frecuente, la lámina y la sección del notebook. Se imprimen en A4.', [('Abrir los mapas', 'mapas/index.html', '')])}
{card('Guía docente y apuntes', 'El orden de todo, el plan por temas con sus puntos de corte («Si vas atrasado»), apuntes con rigor (sobreajuste, frenos, FGSM, transfer learning, Grad-CAM, SHAP, contrafactuales, equidad por grupo y las reglas), las tablas de los notebooks, el debate de la lectura, la actividad «tu proyecto» y la clave de los quizzes.', [('Abrir la guía', 'Guia_docente.html', ''), ('Plan por temas', 'Guia_docente.html#plan', 'ghost')])}
</div>
<h3 style="margin-top:22px">La semana por temas</h3>
<table><tr><th>Parte</th><th>Láminas</th><th>Duración sugerida</th></tr>{''.join(f'<tr><td>{t}</td><td>{R(a, b)}</td><td>{d}</td></tr>' for (t, a, b), d in zip(PARTS, ['≈ 10 min', '≈ 15 min', '≈ 1 h 45 (35 min de NB05)', '≈ 2 h (40 min de NB06)', '≈ 40 min']))}</table>
<p>Puntos de corte naturales si el tiempo no alcanza: después de la lámina {L('cierre-tema1')} (fin del Tema 1), {L('cordura')} (transfer learning y los mapas de calor cerrados, con su prueba de cordura) o {L('cierre-tema2')} (fin del Tema 2: solo falta el cierre). Para retomar después del Tema 1, abre con la lámina {L('repaso-tema1')}. Detalle en la <a href="Guia_docente.html#plan">guía docente</a>.</p>
<h3 style="margin-top:22px">Cómo presentar en Teams</h3>
<p>Abre las slides en el navegador, pulsa <kbd>F</kbd> y comparte <b>esa ventana</b> (no toda la pantalla). Con <kbd>P</kbd> se abre la vista del presentador en otra ventana: déjala en tu segunda pantalla; las dos ventanas avanzan juntas. Las demos se manejan con el mouse en la ventana compartida.</p>
<table><tr><th>Tecla</th><th>Qué hace</th></tr>{''.join(f'<tr><td><kbd>{k}</kbd></td><td>{d}</td></tr>' for k, d in KEYS)}</table>
</section>

<section class="sec"><h2>2 · Mostrar el código en clase</h2>
<p>Comparte pantalla con Colab. <b>Abrir en Colab</b> abre la versión de los estudiantes directo desde GitHub: ejecútala en vivo con <b>Entorno de ejecución → Ejecutar todo</b>. Funciona con la CPU gratuita; la GPU es opcional. El NB06 instala <code>shap</code> solo si falta (tarda unos segundos).</p>
<div class="cards">{code}</div>
<p style="margin-top:16px">Los notebooks ya vienen <b>completos y ejecutados</b>: puedes mostrarlos tal cual, no hay versión con soluciones. Las tablas «Qué deberían ver» de cada sección están en la <a href="Guia_docente.html#notebooks">guía docente</a>. Lo único privado son sus generadores, que están en tu carpeta <code>Soluciones_privadas</code> y nunca se suben al repo.</p>
</section>

<section class="sec"><h2>3 · Quizzes y resultados</h2>
<div class="cards">
{card('Pre-quiz y quiz final', f'Preguntas cortas, sin cuentas, con las 5 ideas clave de la semana en los dos. Pre-quiz en la lámina {L("prequiz3")} y quiz final en la {L("quizfinal3")}. Los estudiantes juegan en su celular y pegan su código en el chat. Modo proyector: sin puntos, con «Mostrar respuesta».', [('Pre-quiz', '../quiz/index.html?pre', ''), ('Quiz final', '../quiz/index.html?final', ''), ('Modo proyector', '../quiz/index.html?clase', 'ghost')])}
{card('Resultados', 'Pega el chat de Teams y ve el antes y el después de cada idea clave, por grupo y por estudiante. La clave de las preguntas está en la guía docente.', [('Abrir resultados', 'Resultados_quiz.html', ''), ('Clave de los quizzes', 'Guia_docente.html#quizzes', 'ghost')])}
</div></section>

<section class="sec"><h2>4 · Material de la semana</h2>
<div class="cards">
{card('Lectura de tendencia', '«¿Puedes explicar por qué tu modelo dijo «no»? Explicabilidad, robustez y la llegada de las reglas». El resumen, la línea de tiempo de las reglas y los cuatro debates están en la guía docente.', [('Abrir la lectura (PDF)', '../material/Lectura_tendencia_Semana3.pdf', ''), ('Resumen y debate', 'Guia_docente.html#lectura', 'ghost')])}
{card('Encuesta de tendencia', 'Cinco preguntas de opinión, sin respuestas correctas: exactitud o comprensión · qué es una buena explicación · las explicaciones de la propia IA · regular en un campo que cambia · heredar lo que no conocemos. Sus resultados alimentan el video de conclusiones.', [('Abrir la encuesta (PDF)', 'Encuesta_tendencia_Semana3.pdf', ''), ('Cómo usarla en clase', 'Guia_docente.html#encuesta', 'ghost')])}
{card('Guía de estudio', 'Lo que ven los estudiantes para repasar: el recorderis y los dos temas, con ejemplos y ejercicios.', [('Abrir la guía de estudio', '../guia/index.html', '')])}
</div></section>

<section class="sec"><h2>5 · Enlaces cortos (los de los QR)</h2>
<table><tr><th>Para</th><th>Enlace</th></tr>
{''.join(f'<tr><td>{a}</td><td><a href="{SITE}?{k}">{SITE.replace("https://", "")}?{k}</a></td></tr>' for a, k in SHORT)}
</table>
<p>Página de los estudiantes: <a href="{SITE}semana3/">{SITE}semana3/</a> · Repositorio: <a href="{REPO}">{REPO.replace('https://', '')}</a> (carpeta <code>semana3/</code>). Los enlaces cortos de las semanas 1 y 2 siguen funcionando.</p>
</section>
</div></body></html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
if SURVEY_SRC.exists():
    shutil.copyfile(SURVEY_SRC, OUT / 'Encuesta_tendencia_Semana3.pdf')
else:
    print('warning: survey PDF not found at', SURVEY_SRC, '(keep the existing copy)')
print('docencia panel semana 3 built')
if MISSING:
    print('warning: slide ids not in slides.json:', ', '.join(sorted(MISSING)))
