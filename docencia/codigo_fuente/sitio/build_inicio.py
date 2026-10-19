"""Home page of the website (index.html at the repo root, served by Vercel).

It also works as the router for the short links printed as QR codes on the slides:
  .../deepLearningWeek1/?nb01  ?nb02  ?nb03   -> the notebook in Google Colab
  .../deepLearningWeek1/?pre   ?final         -> the Kahoot-style quiz
  .../deepLearningWeek1/?guia                 -> the study guide

usage: python build_inicio.py <site_folder>
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit import CSS

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/"
NB = {"nb01": "NB01_viernes_tu_primera_neurona.ipynb", "nb02": "NB02_sabado_tu_primera_red.ipynb",
      "nb03": "NB03_miniproyecto_cooperativa_starter.ipynb"}
ROUTES = {**{k: COLAB + v for k, v in NB.items()}, "pre": "quiz/index.html?pre", "final": "quiz/index.html?final", "guia": "guia/index.html"}

def step(n, when, title, text, href, label, kind=''):
    return (f'<a class="step {kind}" href="{href}"><span class="num">{n}</span><span class="when">{when}</span>'
            f'<span class="t">{title}</span><span class="d">{text}</span><span class="go">{label} →</span></a>')

def project(tag, kind, title, text, tasks, nb, extra=''):
    return (f'<article class="proj"><span class="chip {kind}">{tag}</span><h3>{title}</h3><p>{text}</p>'
            f'<ul>{"".join(f"<li>{t}</li>" for t in tasks)}</ul>'
            f'<div class="btnrow"><a class="btn" href="{COLAB + NB[nb]}">Abrir en Colab ↗</a></div>'
            f'<p class="more"><a href="proyectos/{NB[nb]}" download>Descargar el .ipynb</a>{extra}</p></article>')

steps = ''.join([
    step(1, 'Viernes, al empezar', 'Pre-quiz', '10 preguntas tipo Kahoot. No es nota: es tu punto de partida.', 'quiz/index.html?pre', 'Jugar', 'amber'),
    step(2, 'Viernes y sábado', 'Proyectos', 'Tres notebooks en Colab: ejemplos resueltos y tareas que se corrigen solas.', '#proyectos', 'Ver proyectos'),
    step(3, 'Después de clase', 'Guía de estudio', 'Los 9 temas con la idea, la fórmula, ejemplos y ejercicios.', 'guia/index.html', 'Estudiar', 'purple'),
    step(4, 'Sábado, al cerrar', 'Quiz final', '12 preguntas. Las 5 ideas clave del pre-quiz vuelven: mide tu avance.', 'quiz/index.html?final', 'Jugar', 'amber'),
])

projects = ''.join([
    project('Viernes 23', '', 'NB01 · Tu primera neurona',
            'Calcula una neurona a mano, entrena un perceptrón, descubre su límite (XOR) y baja la montaña con descenso de gradiente.',
            ['8 tareas cortas que se corrigen solas', '<b>Mini-reto 1:</b> tu propio comité de crédito'], 'nb01'),
    project('Sábado 24', '', 'NB02 · Tu primera red',
            'Forward y backward de una red pequeña con números, TensorFlow calculando lo mismo y Keras en tres pasos.',
            ['6 tareas cortas que se corrigen solas', '<b>Mini-reto 2:</b> los círculos, con más de 90 %'], 'nb02'),
    project('En grupo · martes 27', 'teal', 'NB03 · Mini-proyecto',
            'Un modelo de riesgo de mora para la Cooperativa «Valle Andino» (datos ficticios). Los datos se descargan solos.',
            ['Perceptrón, red desde cero y la misma red en Keras', 'Cada sección tiene un checkpoint con el resultado esperado'], 'nb03',
            ' · <a href="material/Enunciado_miniproyecto_Clase1.pdf">Enunciado (PDF)</a>'),
])

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deep Learning · Semana 1 · UIDE</title>
<meta name="description" content="Semana 1 de Neural Networks: Deep Learning (UIDE / EIG Campus): proyectos en Colab, guía de estudio, pre-quiz y quiz final.">
<script>
// short links used by the QR codes on the slides: ?nb01 ?nb02 ?nb03 ?pre ?final ?guia
(function () {{
  var R = {json.dumps(ROUTES)};
  var q = new URLSearchParams(location.search);
  for (var k in R) if (q.has(k)) {{ location.replace(R[k]); break; }}
}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}
.wrap{{max-width:1120px;margin:0 auto;padding:24px 16px 64px}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:22px}}
.step{{display:flex;flex-direction:column;gap:6px;background:var(--paper);border:2px solid var(--line);border-radius:20px;padding:20px;text-decoration:none;color:var(--txt);transition:transform .12s,border-color .12s}}
.step:hover,.step:focus-visible{{transform:translateY(-2px);border-color:var(--blue);outline:none}}
.step .num{{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--blue);color:#fff;font:700 20px 'Space Grotesk',sans-serif}}
.step.amber .num{{background:var(--amber-f)}} .step.purple .num{{background:#7C3AED}}
.step .when{{font-size:13px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin-top:6px}}
.step .t{{font:700 24px 'Space Grotesk',sans-serif;color:var(--ink)}}
.step .d{{font-size:15.5px;line-height:1.45}}
.step .go{{margin-top:auto;padding-top:8px;font-weight:700;color:var(--blue)}}
.projs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:16px}}
.proj{{display:flex;flex-direction:column;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:22px}}
.proj h3{{margin:4px 0 0}} .proj p{{margin:0}} .proj .chip{{align-self:flex-start}}
.proj ul{{margin:4px 0 6px;padding-left:20px;font-size:15.5px}}
.proj .btnrow{{margin-top:auto}}
.proj .more{{font-size:14.5px;color:var(--muted)}}
.how{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:14px}}
.how div{{background:var(--bg);border:1px solid var(--line);border-radius:16px;padding:14px 16px;font-size:15.5px}}
.how b.n{{font:700 22px 'Space Grotesk',sans-serif;color:var(--blue);margin-right:6px}}
.mat{{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}}
</style>
</head>
<body>
<div class="wrap">
<div class="hero">
<span class="chip">UIDE · Maestría en Ciencia de Datos · Semana 1</span>
<h1 style="margin-top:14px">Neural Networks: Deep Learning</h1>
<p>Fundamentos de redes neuronales: de qué es la inteligencia artificial a entrenar tu primera red en Keras. Sigue los cuatro pasos de abajo; no necesitas instalar nada.</p>
<p style="font-size:15px">Docente: Andrés Ordóñez-Bolaños · Sesiones: viernes 23 (18:00–20:00) y sábado 24 de octubre de 2026 (08:00–12:00) · Entrega del mini-proyecto: martes 27 de octubre</p>
</div>

<nav class="steps" aria-label="Tu semana en cuatro pasos">{steps}</nav>

<section class="sec" id="proyectos">
<h2>Proyectos de la semana</h2>
<p>Cada notebook tiene la misma forma: <b>Ejemplo resuelto → Tu tarea → Revisar</b>. La revisión te dice ✅ correcto, ❌ todavía no (con una pista) o ⏳ falta completar. Las tareas no tienen nota; el mini-proyecto sí (70 puntos).</p>
<div class="projs">{projects}</div>
<h3 style="margin-top:26px">Cómo abrir un notebook en Colab</h3>
<div class="how">
<div><b class="n">1</b>Clic en <b>Abrir en Colab</b> y entra con tu cuenta de Google.</div>
<div><b class="n">2</b><b>Archivo → Guardar una copia en Drive.</b> Si no, tus cambios se pierden al cerrar la pestaña.</div>
<div><b class="n">3</b>Ejecuta primero la celda <b>Configuración</b>; luego en orden con <code>Shift + Enter</code>.</div>
<div><b class="n">4</b>En cada tarea, reemplaza los <code>None</code> y ejecuta <b>Revisar</b>.</div>
</div>
</section>

<section class="sec">
<h2>Material de apoyo</h2>
<p>Para leer con calma. La guía de estudio resume todo; estos PDF amplían.</p>
<div class="mat">
<a class="btn ghost" href="material/Apuntes_teoricos_Clase1.pdf">Apuntes teóricos (PDF)</a>
<a class="btn ghost" href="material/Enunciado_miniproyecto_Clase1.pdf">Enunciado del mini-proyecto (PDF)</a>
<a class="btn ghost" href="material/Lectura_tendencia_Mas_alla_de_Adam.pdf">Lectura de tendencia «Más allá de Adam» (PDF)</a>
</div>
</section>

<p style="margin-top:22px;color:var(--muted);font-size:14px">Código y materiales: <a href="{REPO}">{REPO.replace('https://', '')}</a> · Los datos de la cooperativa son ficticios y se generaron solo para el curso.</p>
</div>
</body>
</html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
print('home page built')
