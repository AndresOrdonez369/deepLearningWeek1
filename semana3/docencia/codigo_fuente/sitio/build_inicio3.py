"""Week-3 home page: semana3/index.html (served by Vercel at /semana3/).

Short links also work from here (the QR codes use the root router: ?nb05 ?nb06 ?pre3 ?final3 ?guia3 ?slides3):
  .../semana3/?nb05  ?nb06   -> the notebook in Google Colab
  .../semana3/?pre   ?final  -> the Kahoot-style quiz of week 3 (?clase = projector mode)
  .../semana3/?guia  ?slides -> study guide / interactive slides

usage: python build_inicio3.py <repo_root>        (writes <repo_root>/semana3/index.html)
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit3 import CSS, WEEKS_CSS, weeks

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
OUT = ROOT / 'semana3'
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana3/proyectos/"
NB = {"nb05": "NB05_generalizar_y_robustez.ipynb", "nb06": "NB06_reutilizar_y_explicar.ipynb"}
ROUTES = {**{k: COLAB + v for k, v in NB.items()}, "pre": "quiz/index.html?pre", "final": "quiz/index.html?final", "clase": "quiz/index.html?clase",
          "guia": "guia/index.html", "slides": "docencia/slides/index.html"}
# the trend reading of the week (final version, written for the course)
PDF_SRC = pathlib.Path('/home/claude/w1/tendencias/final/Lectura_tendencia_Semana3.pdf')
PDF = 'Lectura_tendencia_Semana3.pdf'


def step(n, when, title, text, href, label, kind=''):
    """One of the four steps of the week (a big clickable card)."""
    return (f'<a class="step {kind}" href="{href}"><span class="num">{n}</span><span class="when">{when}</span>'
            f'<span class="t">{title}</span><span class="d">{text}</span><span class="go">{label} →</span></a>')


def project(tag, title, text, tasks, nb, extra=''):
    """A notebook card: what it is about, three real results and the Colab / download links."""
    return (f'<article class="proj"><span class="chip">{tag}</span><h3>{title}</h3><p>{text}</p>'
            f'<ul>{"".join(f"<li>{t}</li>" for t in tasks)}</ul>'
            f'<div class="btnrow"><a class="btn" href="{COLAB + NB[nb]}">Abrir en Colab ↗</a></div>'
            f'<p class="more"><a href="proyectos/{NB[nb]}" download>Descargar el .ipynb</a>{extra}</p></article>')


steps = ''.join([
    step(1, 'Al empezar la semana', 'Pre-quiz', '8 preguntas cortas tipo Kahoot, sin cuentas. No es nota: es tu punto de partida en la semana 3.', 'quiz/index.html?pre', 'Jugar', 'amber'),
    step(2, 'Tema 1 y Tema 2', 'Proyectos en clase', 'Un notebook por tema, en Colab y sin nota: ¿funcionará con casos nuevos? (Tema 1) y reutilizar y explicar (Tema 2). Todo el código ya está escrito y explicado.', '#proyectos', 'Ver proyectos'),
    step(3, 'Después de clase', 'Repasa', 'Las slides interactivas y la guía de estudio: recorderis de las semanas 1 y 2, sobreajuste, robustez, transfer learning y explicabilidad.', 'guia/index.html', 'Estudiar', 'purple'),
    step(4, 'Al cerrar la semana', 'Quiz final', '10 preguntas cortas. Las 5 ideas clave del pre-quiz vuelven con otra versión: mide tu avance.', 'quiz/index.html?final', 'Jugar', 'amber'),
])

projects = ''.join([
    project('Tema 1 · Generalizar y ser robusto', 'NB05 · ¿Funcionará con casos nuevos?',
            'La CNN de la semana 2 estudia con solo 1 000 fotos y se aprende el solucionario. Le pones frenos (aumento de datos, dropout y parar a tiempo), la engañas con un ruido invisible y la vacunas.',
            ['Con 1 000 fotos: <b>96.7 %</b> en entrenamiento y <b>83.0 %</b> en el simulacro: memoriza',
             'Un ruido invisible (ε = 0.05) la baja de <b>87.7 %</b> a <b>39.2 %</b>; vacunada aguanta <b>71.7 %</b>',
             '<b>Ejercicios</b> que se responden leyendo los resultados, y el <b>Experimento 5</b> (opcional)'], 'nb05'),
    project('Tema 2 · Reutilizar y explicar', 'NB06 · Reutilizar y explicar',
            'Una red que nunca vio camisetas aprende con 5 fotos por clase gracias a lo que ya sabía. Después miras dónde mira la red, pones a prueba sus explicaciones y explicas un «no» de crédito a una socia ficticia.',
            ['Con 5 fotos por clase: desde cero <b>30.6 %</b>; heredando lo aprendido, <b>45.9 %</b> (congelada) y <b>47.2 %</b> (ajuste fino)',
             'La prueba de cordura: Grad-CAM la pasa; gradiente × imagen no (<b>0.90</b>)',
             'La socia rechazada (<b>61 %</b>): sin sus 2 atrasos bajaría a <b>12 %</b>'], 'nb06'),
])

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deep Learning · Semana 3 · UIDE</title>
<meta name="description" content="Semana 3 de Neural Networks: Deep Learning (UIDE / EIG Campus): generalización, robustez, transfer learning y explicabilidad. Proyectos en Colab, guía de estudio, pre-quiz y quiz final.">
<script>
// short links: ?nb05 ?nb06 ?pre ?final ?clase ?guia ?slides
(function () {{
  var R = {json.dumps(ROUTES)};
  var q = new URLSearchParams(location.search);
  for (var k in R) if (q.has(k)) {{ location.replace(R[k]); break; }}
}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}{WEEKS_CSS}
.weeks{{padding:0;margin:0 0 14px}}
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
.pend{{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;justify-content:space-between;background:var(--amber-bg);border-radius:18px;padding:16px 20px;margin-top:18px}}
.pend p{{margin:0;max-width:720px}} .pend b{{color:var(--ink)}}
.pend .btnrow{{margin:0}}
.qs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:14px}}
.qs div{{background:var(--bg);border:1px solid var(--line);border-radius:16px;padding:14px 16px}}
.qs b{{display:block;font:700 18px 'Space Grotesk',sans-serif;color:var(--ink);margin-bottom:4px}}
</style>
</head>
<body>
<div class="wrap">
{weeks(3, '../index.html', '../semana2/index.html', 'index.html')}
<div class="hero">
<span class="chip">UIDE · Maestría en Ciencia de Datos · Semana 3</span>
<h1 style="margin-top:14px">Neural Networks: Deep Learning</h1>
<p>Robustez, transfer learning y explicabilidad. Que la red acierte en el examen no basta: tiene que funcionar con casos nuevos, aguantar cambios pequeños, aprovechar lo que ya se sabe y poder explicar por qué decide. La semana tiene dos temas: empezamos con un recorderis de las semanas 1 y 2 y cada sesión sigue donde terminó la anterior. Sigue los cuatro pasos de abajo; no necesitas instalar nada.</p>
<p style="font-size:15px">Docente: Andrés Ordóñez-Bolaños · Semana 3 · noviembre de 2026 · Microsoft Teams</p>
</div>

<nav class="steps" aria-label="Tu semana en cuatro pasos">{steps}</nav>

<div class="pend"><p><b>Empezamos con un recorderis de las semanas 1 y 2</b>: la neurona, la pérdida y el gradiente, Keras en 4 pasos y la suposición de cada arquitectura (densa, CNN, RNN y atención). Esta semana usamos otra vez la CNN de ropa del NB03; si quieres refrescarla, repasa su guía.</p>
<div class="btnrow"><a class="btn ghost" href="guia/index.html#rec">El recorderis en la guía</a><a class="btn ghost" href="../semana2/guia/index.html#b01">La CNN de la semana 2</a></div></div>

<section class="sec" id="temas">
<h2>Las dos preguntas de la semana</h2>
<div class="qs">
<div><b>Tema 1 · ¿Funcionará con casos nuevos?</b>Aprender no es memorizar. Frenos para la memoria, fotos movidas, ruidos que engañan, un mundo que cambia y cómo afinar sin hacer trampa.</div>
<div><b>Tema 2 · ¿Puedo reutilizarla y explicar lo que decide?</b>Transfer learning con pocos datos, mapas de calor, la prueba de cordura, explicar un «no» de crédito y si trata a todos por igual.</div>
<div><b>Cierre · ¿Le creerías a tu red?</b>Cinco preguntas antes de usar un modelo con personas, y cómo llevarlas a tu proyecto de titulación.</div>
</div>
</section>

<section class="sec" id="proyectos">
<h2>Proyectos en clase</h2>
<p>Se trabajan durante la clase, solos o en parejas, y <b>no tienen nota</b>. Cada notebook ya viene completo y ejecutado. En cada sección: <b>la idea → el código explicado → ¿qué crees que saldrá? → lo que deberías ver → preguntas para pensar</b>, con la respuesta desplegable. Al final hay <b>ejercicios</b> que se resuelven leyendo los resultados. Se aprende leyendo, prediciendo y explicando, no rellenando.</p>
<div class="projs">{projects}</div>
<h3 style="margin-top:26px">Cómo abrir un notebook en Colab</h3>
<div class="how">
<div><b class="n">1</b>Clic en <b>Abrir en Colab</b> y entra con tu cuenta de Google.</div>
<div><b class="n">2</b><b>Archivo → Guardar una copia en Drive.</b> Si no, tus cambios se pierden al cerrar la pestaña.</div>
<div><b class="n">3</b>Ejecuta primero la celda <b>Configuración</b>; luego en orden con <code>Shift + Enter</code>. Si algo falla, mira la sección <b>🛟 Si algo falla</b> del notebook.</div>
<div><b class="n">4</b>Antes de cada celda, apuesta un resultado en <b>🔮 Antes de ejecutar</b> y compáralo con <b>Qué deberías ver</b>.</div>
</div>
</section>

<section class="sec">
<h2>Material de apoyo</h2>
<p>Para repasar con calma. Las slides son interactivas: puedes ver cómo se separan las curvas cuando la red memoriza, subir poco a poco el ruido que la engaña y comparar dónde miró la red con cada explicación.</p>
<div class="mat">
<a class="btn" href="docencia/slides/index.html">Slides interactivas de la clase</a>
<a class="btn ghost" href="guia/index.html">Guía de estudio</a>
<a class="btn ghost" href="material/{PDF}">Lectura de tendencia «¿Puedes explicar por qué tu modelo dijo «no»?» (PDF)</a>
</div>
</section>

<p style="margin-top:22px;color:var(--muted);font-size:14px">Código y materiales: <a href="{REPO}">{REPO.replace('https://', '')}</a> · Fashion-MNIST: Xiao, Rasul y Vollgraf (2017), Zalando Research. Los socios de la cooperativa del NB06 son ficticios y se generaron solo para el curso.</p>
</div>
</body>
</html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
mat = OUT / 'material'
mat.mkdir(exist_ok=True)
if PDF_SRC.exists() and not (mat / PDF).exists():
    (mat / PDF).write_bytes(PDF_SRC.read_bytes())
print('week-3 home built')
