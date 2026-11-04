"""Week-2 teacher panel: semana2/docencia/index.html (slides, concept maps, code in Colab, guide, quiz results).
usage: python build_docencia2.py <semana2/docencia folder>      (reads <folder>/slides/slides.json)"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit_docencia2 import CSS, WEEKS_CSS, weeks

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docencia2')
SITE = "https://deeplearningweek1.vercel.app/"
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana2/proyectos/"
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
PARTS = [('Encuadre', 'portada2', 'metas2'), ('00 · Recorderis de la semana 1 y Keras', 'b00', 'nb02-casa'),
         ('Tema 1 · Cómo mira una red una imagen', 'b01', 'cierre-tema1'), ('Tema 2 · Cómo lee una red una secuencia', 'b02', 'contrapeso'),
         ('Cierre · Elegir la arquitectura', 'b04', 'recursos2')]
NB = [("NB03 · Tu primera CNN", f"Tema 1 · práctica en clase (lámina {L('practica-nb03')}) · unos 2 minutos de cómputo", "NB03_tu_primera_cnn.ipynb"),
      ("NB04 · Redes que recuerdan", f"Tema 2 · práctica en clase (lámina {L('practica-nb04')}) · 1–2 minutos de cómputo", "NB04_redes_que_recuerdan.ipynb")]


def card(title, text, links):
    btns = ''.join(f'<a class="btn {k}" href="{h}">{t}</a>' for t, h, k in links)
    return f'<article class="c"><h3>{title}</h3><p>{text}</p><div class="btnrow">{btns}</div></article>'


code = ''.join(card(t, w, [('Abrir en Colab ↗', COLAB + f, ''), ('Ver en GitHub', f'{REPO}/blob/main/semana2/proyectos/{f}', 'ghost')]) for t, w, f in NB)
KEYS = [('→ · espacio · PageDown', 'avanzar un paso (los clickers de presentación funcionan)'), ('← · PageUp', 'retroceder'),
        ('P', 'vista del presentador en otra ventana: notas, reloj y lámina siguiente'), ('G', 'índice de todas las láminas'),
        ('F', 'pantalla completa'), ('L', 'puntero láser, más visible que el mouse en Teams'), ('B', 'pantalla negra'),
        ('número + Enter', 'ir a una lámina')]
SHORT = [('Inicio de la semana 2', 'semana2'), ('Pre-quiz', 'pre2'), ('Quiz final', 'final2'), ('NB03 en Colab', 'nb03'), ('NB04 en Colab', 'nb04'),
         ('Guía de estudio', 'guia2'), ('Slides', 'slides2')]

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Docencia · Semana 2 · Deep Learning UIDE</title>
<meta name="description" content="Panel del profesor de la semana 2: slides interactivas, mapas conceptuales, código en Colab, guía docente y resultados de los quizzes.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}{WEEKS_CSS}
.wrap{{max-width:1120px;margin:0 auto;padding:24px 16px 64px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:14px}}
.c{{display:flex;flex-direction:column;gap:6px;background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:18px}}
td a,.sec p a{{overflow-wrap:anywhere}} .hero h1{{overflow-wrap:anywhere}}
.c h3{{margin:0}} .c p{{margin:0;font-size:15.5px}} .c .btnrow{{margin-top:auto;padding-top:8px}}
kbd{{font-family:'JetBrains Mono',monospace;font-size:14px;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:1px 7px}}
</style></head>
<body><div class="wrap">
<div class="hero">{weeks(2, '../../docencia/index.html', 'index.html')}<br><span class="chip">Docencia · Semana 2</span>
<h1 style="margin-top:14px">Panel del profesor</h1>
<p>Todo para dictar la semana 2, organizada en <b>dos temas</b> (imágenes y secuencias) después de un recorderis de la semana 1: las slides interactivas, los mapas conceptuales para preparar cada tema, el código para mostrar en Colab, tu guía y los resultados de los quizzes. Los proyectos son en clase y sin nota.</p>
<p style="font-size:15px">Sesiones por Teams: viernes 6 y sábado 7 de noviembre de 2026. Las láminas son una sola secuencia: cada sesión empieza donde terminó la anterior.</p>
<p style="font-size:15px"><a href="../index.html" style="color:#B8C4D6">← Página de los estudiantes</a></p></div>

<section class="sec"><h2>1 · Para dictar</h2>
<div class="cards">
{card('Slides interactivas', f'{N_SLIDES} láminas con demos en vivo, por temas: ' + ' · '.join(f'{t.split(" · ")[0]} {R(a, b)}' for t, a, b in PARTS) + '. Cada lámina trae notas con el guion, la pregunta para la clase y el tiempo sugerido.', [('Abrir las slides', 'slides/index.html', ''), ('Vista del presentador', 'slides/index.html?presenter', 'ghost'), ('PDF de respaldo', 'Slides_Semana2.pdf', 'ghost')])}
{card('Mapas conceptuales', 'La semana completa, el recorderis de la semana 1 y un mapa por tema (Tema 1, Tema 2 en dos partes y el cierre). Clic en cada concepto: qué decir, un ejemplo, una pregunta para la clase, el error frecuente y la lámina. Se imprimen en A4.', [('Abrir los mapas', 'mapas/index.html', '')])}
{card('Guía docente y apuntes', 'El orden de todo, el plan por temas con sus puntos de corte («Si vas atrasado»), apuntes con rigor (recorderis, CNN, RNN, LSTM, atención, GNN y GAN), claves de los notebooks, el debate de la lectura y la actividad «tu proyecto».', [('Abrir la guía', 'Guia_docente.html', '')])}
</div>
<h3 style="margin-top:22px">La semana por temas</h3>
<table><tr><th>Parte</th><th>Láminas</th></tr>{''.join(f'<tr><td>{t}</td><td>{R(a, b)}</td></tr>' for t, a, b in PARTS)}</table>
<p>Puntos de corte naturales si el tiempo no alcanza: después de la lámina {L('cierre-tema1')} (fin del Tema 1), {L('examen-memoria')} (RNN y LSTM cerradas) o {L('contrapeso')} (atención y tendencia cerradas). Para retomar, abre con la lámina {L('repaso-tema1')}. Detalle en la <a href="Guia_docente.html#plan">guía docente</a>.</p>
<h3 style="margin-top:22px">Cómo presentar en Teams</h3>
<p>Abre las slides en el navegador, pulsa <kbd>F</kbd> y comparte <b>esa ventana</b> (no toda la pantalla). Con <kbd>P</kbd> se abre la vista del presentador en otra ventana: déjala en tu segunda pantalla; las dos ventanas avanzan juntas. Las demos se manejan con el mouse en la ventana compartida.</p>
<table><tr><th>Tecla</th><th>Qué hace</th></tr>{''.join(f'<tr><td><kbd>{k}</kbd></td><td>{d}</td></tr>' for k, d in KEYS)}</table>
</section>

<section class="sec"><h2>2 · Mostrar el código en clase</h2>
<p>Comparte pantalla con Colab. <b>Abrir en Colab</b> abre la versión de los estudiantes directo desde GitHub: ejecútala en vivo con <b>Entorno de ejecución → Ejecutar todo</b>. Funciona con la CPU gratuita; la GPU es opcional.</p>
<div class="cards">{code}</div>
<p style="margin-top:16px">Los notebooks ya vienen <b>completos y ejecutados</b>: puedes mostrarlos tal cual, no hay versión con soluciones. Lo único privado son sus generadores, que están en tu carpeta <code>Soluciones_privadas</code> y nunca se suben al repo.</p>
</section>

<section class="sec"><h2>3 · Quizzes y resultados</h2>
<div class="cards">
{card('Pre-quiz y quiz final', 'Preguntas cortas, sin cuentas, con las 5 ideas clave de la semana en los dos. Los estudiantes juegan en su celular y pegan su código en el chat. Modo proyector: sin puntos, con «Mostrar respuesta».', [('Pre-quiz', '../quiz/index.html?pre', ''), ('Quiz final', '../quiz/index.html?final', ''), ('Modo proyector', '../quiz/index.html?clase', 'ghost')])}
{card('Resultados', 'Pega el chat de Teams y ve el antes y el después de cada idea clave, por grupo y por estudiante.', [('Abrir resultados', 'Resultados_quiz.html', '')])}
</div></section>

<section class="sec"><h2>4 · Material de la semana</h2>
<div class="cards">
{card('Lectura de tendencia', '«¿El regreso de las redes recurrentes? Transformers, Mamba y la búsqueda de la arquitectura ideal». El debate en clase y el guion del video de conclusiones están en la guía docente.', [('Abrir la lectura (PDF)', '../material/Lectura_tendencia_Semana2.pdf', ''), ('Debate y video', 'Guia_docente.html#lectura', 'ghost')])}
{card('Guía de estudio', 'Lo que ven los estudiantes para repasar: el recorderis y los dos temas, con ejemplos y ejercicios.', [('Abrir la guía de estudio', '../guia/index.html', '')])}
</div></section>

<section class="sec"><h2>5 · Enlaces cortos (los de los QR)</h2>
<table><tr><th>Para</th><th>Enlace</th></tr>
{''.join(f'<tr><td>{a}</td><td><a href="{SITE}?{k}">{SITE.replace("https://", "")}?{k}</a></td></tr>' for a, k in SHORT)}
</table>
<p>Página de los estudiantes: <a href="{SITE}semana2/">{SITE}semana2/</a> · Repositorio: <a href="{REPO}">{REPO.replace('https://', '')}</a> (carpeta <code>semana2/</code>)</p>
</section>
</div></body></html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
print('docencia panel semana 2 built')
if MISSING:
    print('warning: slide ids not in slides.json:', ', '.join(sorted(MISSING)))
