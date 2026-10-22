"""Teacher panel: docencia/index.html (slides, concept maps, code in Colab, guide, quiz results).
usage: python build_docencia.py <docencia_folder>      (reads <docencia_folder>/slides/slides.json)"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit import CSS

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docencia')
SITE = "https://deeplearningweek1.vercel.app/"
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/"
SL = {s['id']: s['n'] for s in json.loads((OUT / 'slides' / 'slides.json').read_text())}
N_SLIDES = len(SL)
FRI_END = SL['cierre-viernes']
NB = [("NB01 · Tu primera neurona", f"Viernes · prácticas en clase (láminas {SL['practica1']} y {SL['practica2']})", "NB01_viernes_tu_primera_neurona.ipynb"),
      ("NB02 · Tu primera red", f"Sábado · práctica en clase (lámina {SL['practica3']})", "NB02_sabado_tu_primera_red.ipynb")]


def card(title, text, links):
    btns = ''.join(f'<a class="btn {k}" href="{h}">{t}</a>' for t, h, k in links)
    return f'<article class="c"><h3>{title}</h3><p>{text}</p><div class="btnrow">{btns}</div></article>'


code = ''.join(card(t, w, [('Abrir en Colab ↗', COLAB + f, ''), ('Ver en GitHub', f'{REPO}/blob/main/proyectos/{f}', 'ghost')]) for t, w, f in NB)
KEYS = [('→ · espacio · PageDown', 'avanzar un paso (los clickers de presentación funcionan)'), ('← · PageUp', 'retroceder'),
        ('P', 'vista del presentador en otra ventana: notas, reloj y lámina siguiente'), ('G', 'índice de todas las láminas'),
        ('F', 'pantalla completa'), ('L', 'puntero láser, más visible que el mouse en Teams'), ('B', 'pantalla negra'),
        ('número + Enter', 'ir a una lámina')]

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Docencia · Semana 1 · Deep Learning UIDE</title>
<meta name="description" content="Panel del profesor de la semana 1: slides interactivas, mapas conceptuales, código en Colab, guía docente y resultados de los quizzes.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}
.wrap{{max-width:1120px;margin:0 auto;padding:24px 16px 64px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:14px}}
.c{{display:flex;flex-direction:column;gap:6px;background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:18px}}
td a,.sec p a{{overflow-wrap:anywhere}} .hero h1{{overflow-wrap:anywhere}}
.c h3{{margin:0}} .c p{{margin:0;font-size:15.5px}} .c .btnrow{{margin-top:auto;padding-top:8px}}
kbd{{font-family:'JetBrains Mono',monospace;font-size:14px;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:1px 7px}}
</style></head>
<body><div class="wrap">
<div class="hero"><span class="chip">Docencia · Semana 1</span>
<h1 style="margin-top:14px">Panel del profesor</h1>
<p>Todo para dictar la semana 1: las slides interactivas, los mapas conceptuales para preparar cada bloque, el código para mostrar en Colab, tu guía y los resultados de los quizzes. Los proyectos son en clase y sin nota.</p>
<p style="font-size:15px"><a href="../index.html" style="color:#B8C4D6">← Página de los estudiantes</a></p></div>

<section class="sec"><h2>1 · Para dictar</h2>
<div class="cards">
{card('Slides interactivas', f'{N_SLIDES} láminas con demos en vivo: viernes 1–{FRI_END}, sábado {FRI_END + 1}–{N_SLIDES}. Cada lámina trae notas con el guion, la pregunta para la clase y el tiempo sugerido.', [('Abrir las slides', 'slides/index.html', ''), ('Vista del presentador', 'slides/index.html?presenter', 'ghost'), ('PDF de respaldo', 'Slides_Semana1.pdf', 'ghost')])}
{card('Mapas conceptuales', 'La semana completa y un mapa por bloque. Clic en cada concepto: qué decir, un ejemplo, una pregunta para la clase, el error frecuente y la lámina. Se imprimen en A4.', [('Abrir los mapas', 'mapas/index.html', '')])}
{card('Guía docente y apuntes', 'El orden de todo, el plan minuto a minuto, apuntes con rigor, preguntas probables y claves de los notebooks.', [('Abrir la guía', 'Guia_docente.html', '')])}
</div>
<h3 style="margin-top:22px">Cómo presentar en Teams</h3>
<p>Abre las slides en el navegador, pulsa <kbd>F</kbd> y comparte <b>esa ventana</b> (no toda la pantalla). Con <kbd>P</kbd> se abre la vista del presentador en otra ventana: déjala en tu segunda pantalla; las dos ventanas avanzan juntas. Las demos se manejan con el mouse en la ventana compartida.</p>
<table><tr><th>Tecla</th><th>Qué hace</th></tr>{''.join(f'<tr><td><kbd>{k}</kbd></td><td>{d}</td></tr>' for k, d in KEYS)}</table>
</section>

<section class="sec"><h2>2 · Mostrar el código en clase</h2>
<p>Comparte pantalla con Colab. <b>Abrir en Colab</b> abre la versión de los estudiantes directo desde GitHub: ejecútala en vivo con <b>Entorno de ejecución → Ejecutar todo</b>.</p>
<div class="cards">{code}</div>
<p style="margin-top:16px"><b>Las soluciones no están en este repo</b> (es público). Están en tu carpeta <code>Soluciones_privadas</code>. Para mostrarlas, súbelas una vez a una carpeta privada de tu Google Drive y ábrelas desde allí, o en Colab: <b>Archivo → Subir cuaderno</b>. Nunca compartas pantalla con una solución mientras los estudiantes trabajan en la tarea.</p>
</section>

<section class="sec"><h2>3 · Quizzes y resultados</h2>
<div class="cards">
{card('Pre-quiz y quiz final', '8 y 10 preguntas cortas, sin cuentas. Los estudiantes juegan en su celular y pegan su código en el chat. Modo proyector: sin puntos, con «Mostrar respuesta».', [('Pre-quiz', '../quiz/index.html?pre', ''), ('Quiz final', '../quiz/index.html?final', ''), ('Modo proyector', '../quiz/index.html?clase', 'ghost')])}
{card('Resultados', 'Pega el chat de Teams y ve el antes y el después de cada idea clave, por grupo y por estudiante.', [('Abrir resultados', 'Resultados_quiz.html', '')])}
</div></section>

<section class="sec"><h2>4 · Enlaces cortos (los de los QR)</h2>
<table><tr><th>Para</th><th>Enlace</th></tr>
{''.join(f'<tr><td>{a}</td><td><a href="{SITE}?{k}">{SITE.replace("https://", "")}?{k}</a></td></tr>' for a, k in [('Pre-quiz', 'pre'), ('Quiz final', 'final'), ('NB01 en Colab', 'nb01'), ('NB02 en Colab', 'nb02'), ('Guía de estudio', 'guia'), ('Slides', 'slides')])}
</table>
<p>Página de los estudiantes: <a href="{SITE}">{SITE}</a> · Repositorio: <a href="{REPO}">{REPO.replace('https://', '')}</a></p>
</section>
</div></body></html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
print('docencia panel built')
