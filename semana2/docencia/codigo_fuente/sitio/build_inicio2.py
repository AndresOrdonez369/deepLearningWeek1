"""Week-2 home page: semana2/index.html (served by Vercel at /semana2/).

Short links also work from here (the QR codes use the root router: ?nb03 ?nb04 ?pre2 ?final2 ?guia2 ?slides2):
  .../semana2/?nb03  ?nb04   -> the notebook in Google Colab
  .../semana2/?pre   ?final  -> the Kahoot-style quiz of week 2
  .../semana2/?guia  ?slides -> study guide / interactive slides

usage: python build_inicio2.py <repo_root>        (writes <repo_root>/semana2/index.html)
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit2 import CSS, WEEKS_CSS, weeks

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
OUT = ROOT / 'semana2'
REPO = "https://github.com/AndresOrdonez369/deepLearningWeek1"
COLAB = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana2/proyectos/"
COLAB_W1 = "https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/"
NB = {"nb03": "NB03_viernes_tu_primera_cnn.ipynb", "nb04": "NB04_sabado_redes_que_recuerdan.ipynb"}
ROUTES = {**{k: COLAB + v for k, v in NB.items()}, "pre": "quiz/index.html?pre", "final": "quiz/index.html?final", "clase": "quiz/index.html?clase",
          "guia": "guia/index.html", "slides": "docencia/slides/index.html"}


def step(n, when, title, text, href, label, kind=''):
    return (f'<a class="step {kind}" href="{href}"><span class="num">{n}</span><span class="when">{when}</span>'
            f'<span class="t">{title}</span><span class="d">{text}</span><span class="go">{label} →</span></a>')


def project(tag, title, text, tasks, nb, extra=''):
    return (f'<article class="proj"><span class="chip">{tag}</span><h3>{title}</h3><p>{text}</p>'
            f'<ul>{"".join(f"<li>{t}</li>" for t in tasks)}</ul>'
            f'<div class="btnrow"><a class="btn" href="{COLAB + NB[nb]}">Abrir en Colab ↗</a></div>'
            f'<p class="more"><a href="proyectos/{NB[nb]}" download>Descargar el .ipynb</a>{extra}</p></article>')


steps = ''.join([
    step(1, 'Viernes, al empezar', 'Pre-quiz', '8 preguntas cortas tipo Kahoot, sin cuentas. No es nota: es tu punto de partida en la semana 2.', 'quiz/index.html?pre', 'Jugar', 'amber'),
    step(2, 'Viernes y sábado', 'Proyectos en clase', 'Dos notebooks en Colab, sin nota: una CNN que reconoce ropa y redes que recuerdan. Todo el código ya está escrito y explicado.', '#proyectos', 'Ver proyectos'),
    step(3, 'Después de clase', 'Repasa', 'Las slides interactivas y la guía de estudio: imágenes, secuencias, atención y cómo elegir la arquitectura.', 'guia/index.html', 'Estudiar', 'purple'),
    step(4, 'Sábado, al cerrar', 'Quiz final', '10 preguntas cortas. Las 5 ideas clave del pre-quiz vuelven con otra versión: mide tu avance.', 'quiz/index.html?final', 'Jugar', 'amber'),
])

projects = ''.join([
    project('Viernes 6', 'NB03 · Tu primera red convolucional',
            'Una foto es una tabla de números. Pasa un filtro de 3 × 3 a mano, compara una red densa con una CNN en 70 000 fotos de ropa y pon a prueba la suposición de cada una.',
            ['Densa: <b>101 770</b> parámetros, cerca de <b>87 %</b>. CNN: <b>12 810</b>, cerca de <b>88 %</b>',
             '¿Qué pasa si mueves la prenda 2 píxeles? ¿Y si mezclas los píxeles?', '<b>Experimento 3</b> (opcional): cambia el número de filtros'], 'nb03'),
    project('Sábado 7', 'NB04 · Redes que recuerdan',
            'La libreta de una RNN calculada a mano, por qué el orden importa, un examen de memoria para SimpleRNN y LSTM, y la atención que mira directo al paso importante.',
            ['El promedio adivina (<b>48 %</b>); la RNN acierta (<b>100 %</b>)',
             'Con 80 pasos las recurrentes se olvidan; la atención, con <b>82</b> parámetros, llega a <b>100 %</b>', '<b>Experimento 4</b> (opcional): 50 pasos con dos semillas'], 'nb04'),
])

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deep Learning · Semana 2 · UIDE</title>
<meta name="description" content="Semana 2 de Neural Networks: Deep Learning (UIDE / EIG Campus): redes convolucionales, recurrentes y atención. Proyectos en Colab, guía de estudio, pre-quiz y quiz final.">
<script>
// short links: ?nb03 ?nb04 ?pre ?final ?clase ?guia ?slides
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
</style>
</head>
<body>
<div class="wrap">
{weeks(2, '../index.html', 'index.html')}
<div class="hero">
<span class="chip">UIDE · Maestría en Ciencia de Datos · Semana 2</span>
<h1 style="margin-top:14px">Neural Networks: Deep Learning</h1>
<p>Arquitecturas para problemas complejos: cómo mira una red una imagen (redes convolucionales) y cómo lee una secuencia (redes recurrentes, LSTM y atención). Cada arquitectura es una suposición sobre los datos. Sigue los cuatro pasos de abajo; no necesitas instalar nada.</p>
<p style="font-size:15px">Docente: Andrés Ordóñez-Bolaños · Sesiones: viernes 6 (18:00–20:00) y sábado 7 de noviembre de 2026 (08:00–12:00)</p>
</div>

<nav class="steps" aria-label="Tu semana en cuatro pasos">{steps}</nav>

<div class="pend"><p><b>¿Te quedó pendiente Keras?</b> El viernes empezamos con un repaso de 15 minutos. Para practicar en casa, abre el NB02 de la semana 1 en las partes E y F: la red de las lunas en diez líneas.</p>
<a class="btn ghost" href="{COLAB_W1}NB02_sabado_tu_primera_red.ipynb">NB02 de la semana 1 ↗</a></div>

<section class="sec" id="proyectos">
<h2>Proyectos en clase</h2>
<p>Se trabajan durante la clase, solos o en parejas, y <b>no tienen nota</b>. Cada notebook ya viene completo y ejecutado. En cada sección: <b>la idea → el código explicado → ¿qué crees que saldrá? → lo que deberías ver → preguntas para pensar</b>, con la respuesta desplegable. Se aprende leyendo, prediciendo y explicando, no rellenando.</p>
<div class="projs">{projects}</div>
<h3 style="margin-top:26px">Cómo abrir un notebook en Colab</h3>
<div class="how">
<div><b class="n">1</b>Clic en <b>Abrir en Colab</b> y entra con tu cuenta de Google.</div>
<div><b class="n">2</b><b>Archivo → Guardar una copia en Drive.</b> Si no, tus cambios se pierden al cerrar la pestaña.</div>
<div><b class="n">3</b>Ejecuta primero la celda <b>Configuración</b>; luego en orden con <code>Shift + Enter</code>. Cada notebook tarda unos 2 minutos en total.</div>
<div><b class="n">4</b>Antes de cada celda, apuesta un resultado en <b>🔮 Antes de ejecutar</b> y compáralo con <b>Qué deberías ver</b>.</div>
</div>
</section>

<section class="sec">
<h2>Material de apoyo</h2>
<p>Para repasar con calma. Las slides son interactivas: puedes mover el filtro sobre una foto, ver cómo se llena la libreta de una RNN y a qué palabra mira la atención.</p>
<div class="mat">
<a class="btn" href="docencia/slides/index.html">Slides interactivas de la clase</a>
<a class="btn ghost" href="guia/index.html">Guía de estudio</a>
<a class="btn ghost" href="material/Lectura_tendencia_Semana2.pdf">Lectura de tendencia «¿El regreso de las redes recurrentes?» (PDF)</a>
</div>
</section>

<p style="margin-top:22px;color:var(--muted);font-size:14px">Código y materiales: <a href="{REPO}">{REPO.replace('https://', '')}</a> · Fashion-MNIST: Xiao, Rasul y Vollgraf (2017), Zalando Research. Los historiales de pago del NB04 son ficticios y se generaron solo para el curso.</p>
</div>
</body>
</html>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'index.html').write_text(html)
mat = OUT / 'material'
mat.mkdir(exist_ok=True)
src = pathlib.Path('/root/.claude/uploads/9cf15e00-cc8b-5e4f-968c-d9e594c33d06/32dd8188-Lectura_tendencia_Semana2.pdf')
if src.exists() and not (mat / 'Lectura_tendencia_Semana2.pdf').exists():
    (mat / 'Lectura_tendencia_Semana2.pdf').write_bytes(src.read_bytes())
print('week-2 home built')
