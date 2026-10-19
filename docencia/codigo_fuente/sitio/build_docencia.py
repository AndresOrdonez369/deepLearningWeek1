"""Teacher panel: docencia/index.html (slides, code in Colab, guides, quiz results, tracking).
usage: python build_docencia.py <docencia_folder>"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit import CSS

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out_docencia')
SITE = "https://deeplearningweek1.vercel.app/"
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/"
DECK = "https://claude.ai/artifact/8HALFp7SJwd1UmDc8iT37h"
NB = [("NB01 · Tu primera neurona", "Viernes · prácticas 1 y 2 (láminas 32 y 40)", "NB01_viernes_tu_primera_neurona.ipynb"),
      ("NB02 · Tu primera red", "Sábado · práctica 3 (lámina 66)", "NB02_sabado_tu_primera_red.ipynb"),
      ("NB03 · Mini-proyecto", "Sábado · salas (lámina 73) · entrega martes 27", "NB03_miniproyecto_cooperativa_starter.ipynb")]

def card(title, text, links):
    btns = ''.join(f'<a class="btn {k}" href="{h}">{t}</a>' for t, h, k in links)
    return f'<article class="c"><h3>{title}</h3><p>{text}</p><div class="btnrow">{btns}</div></article>'

code = ''.join(card(t, w, [('Abrir en Colab ↗', COLAB + f, ''), ('Ver en GitHub', f'{REPO}/blob/main/proyectos/{f}', 'ghost')]) for t, w, f in NB)

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Docencia · Semana 1 · Deep Learning UIDE</title>
<meta name="description" content="Panel del profesor de la semana 1: slides, código en Colab, guía docente, resultados de los quizzes y seguimiento.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}
.wrap{{max-width:1120px;margin:0 auto;padding:24px 16px 64px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:14px}}
.c{{display:flex;flex-direction:column;gap:6px;background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:18px}}
td a,.sec p a{{overflow-wrap:anywhere}} .hero h1{{overflow-wrap:anywhere}}
.c h3{{margin:0}} .c p{{margin:0;font-size:15.5px}} .c .btnrow{{margin-top:auto;padding-top:8px}}
</style></head>
<body><div class="wrap">
<div class="hero"><span class="chip">Docencia · Semana 1</span>
<h1 style="margin-top:14px">Panel del profesor</h1>
<p>Todo lo que necesitas para dictar la semana 1: las slides, el código para mostrar en Colab, tu guía y las herramientas para ver cómo van los estudiantes.</p>
<p style="font-size:15px"><a href="../index.html" style="color:#B8C4D6">← Página de los estudiantes</a></p></div>

<section class="sec"><h2>1 · Para dictar</h2>
<div class="cards">
{card('Slides de la Clase 1', '78 láminas: viernes 1–41, sábado 42–78. Las notas de cada lámina traen el guion.', [('Slides (PDF)', 'Slides_Clase1.pdf', ''), ('Editar en claude.ai ↗', DECK, 'ghost')])}
{card('Guía docente y apuntes', 'El orden de todo, el plan minuto a minuto, apuntes con rigor, preguntas probables y claves.', [('Abrir la guía', 'Guia_docente.html', '')])}
{card('Logística y encuesta', 'Checklist, encuesta de tendencia con su clave y pendientes con la tutora.', [('Abrir (PDF)', 'Logistica_y_encuesta.pdf', 'ghost')])}
</div></section>

<section class="sec"><h2>2 · Mostrar el código en clase</h2>
<p>Comparte pantalla con Colab. <b>Abrir en Colab</b> abre la versión de los estudiantes directo desde GitHub: ejecútala en vivo con <b>Entorno de ejecución → Ejecutar todo</b>.</p>
<div class="cards">{code}</div>
<p style="margin-top:16px"><b>Las soluciones no están en este repo</b> (es público). Están en tu carpeta <code>Soluciones_privadas</code>. Para mostrarlas, súbelas una vez a una carpeta privada de tu Google Drive y ábrelas desde allí con doble clic, o en Colab: <b>Archivo → Subir cuaderno</b>. Nunca compartas pantalla con una solución mientras los estudiantes trabajan en la tarea.</p>
</section>

<section class="sec"><h2>3 · Quizzes y resultados</h2>
<div class="cards">
{card('Pre-quiz y quiz final', 'Los estudiantes juegan en su celular y pegan su código en el chat. Modo proyector: sin puntos, con «Mostrar respuesta».', [('Pre-quiz', '../quiz/index.html?pre', ''), ('Quiz final', '../quiz/index.html?final', ''), ('Modo proyector', '../quiz/index.html?clase', 'ghost')])}
{card('Resultados', 'Pega el chat de Teams y ve el antes y el después de cada idea clave, por grupo y por estudiante.', [('Abrir resultados', 'Resultados_quiz.html', '')])}
{card('Seguimiento de grupos', 'Avance del NB03 sección por sección, rúbrica de 70 pts y notas de sala. Descárgalo y llénalo en tu computador.', [('Descargar Excel', 'Seguimiento_grupos.xlsx', 'ghost')])}
</div></section>

<section class="sec"><h2>4 · Enlaces cortos (los de los QR)</h2>
<table><tr><th>Para</th><th>Enlace</th></tr>
{''.join(f'<tr><td>{a}</td><td><a href="{SITE}?{k}">{SITE.replace("https://", "")}?{k}</a></td></tr>' for a, k in [('Pre-quiz', 'pre'), ('Quiz final', 'final'), ('NB01 en Colab', 'nb01'), ('NB02 en Colab', 'nb02'), ('NB03 en Colab', 'nb03'), ('Guía de estudio', 'guia')])}
</table>
<p>Página de los estudiantes: <a href="{SITE}">{SITE}</a> · Repositorio: <a href="{REPO}">{REPO.replace('https://', '')}</a></p>
</section>
</div></body></html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
print('docencia panel built')
