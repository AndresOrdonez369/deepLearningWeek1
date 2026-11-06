"""Week-3 student study guide: semana3/guia/index.html
usage: python build_guia3.py <repo_root>          (slide numbers come from <repo_root>/semana3/docencia/slides/slides.json)

Organized by the two themes of the week (not by days): 00 recap of weeks 1 and 2 · Tema 1 (generalize and be robust, NB05)
· Tema 2 (reuse and explain, NB06) · closing «¿Le creerías a tu red?». All numbers are the real runs (DISENO3.md)."""
import json, pathlib, sys, unicodedata as _u
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from doc_kit3 import page, section, chip, idea, box, formula, ex, colab, fig, hist, weeks
import figs_guia3 as F

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
OUT = ROOT / 'semana3'
COLAB = 'https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana3/proyectos/'
NB5, NB6 = COLAB + 'NB05_generalizar_y_robustez.ipynb', COLAB + 'NB06_reutilizar_y_explicar.ipynb'
B, A, T, P, I = 'var(--blue)', 'var(--amber-f)', 'var(--teal)', 'var(--purple)', 'var(--ink)'

_sj = OUT / 'docencia' / 'slides' / 'slides.json'
SL = {s['id']: s['n'] for s in json.loads(_sj.read_text())} if _sj.exists() else {}


def lam(*ids):
    """'lámina 14' or 'láminas 14 y 15' from the deck; 'las slides' if the slide is not in the deck."""
    ns = sorted({SL[i] for i in ids if i in SL})
    if not ns:
        return 'las slides'
    return f'lámina {ns[0]}' if len(ns) == 1 else 'láminas ' + ', '.join(map(str, ns[:-1])) + f' y {ns[-1]}'


S = []

# ------------------------------------------------------------------ start
S.append(('inicio', '★', 'Cómo usar esta guía', f"""
<div class="hero">
<h1>¿Le creerías a tu red?</h1>
<span class="chip" style="margin-top:14px">Semana 3 · Guía de estudio</span>
<p>Generalizar, ser robusto, reutilizar y explicar, en palabras sencillas: primero el problema, después un ejemplo, luego el nombre y al final la cuenta, leída en voz alta («Léelo así»). Con los números reales de los notebooks NB05 y NB06 y ejercicios con su respuesta.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?pre">Jugar el pre-quiz</a><a class="btn" href="#rec">Empezar a estudiar</a><a class="btn ghost" style="color:#EEF2F8;border-color:#2A3B5C" href="../material/Lectura_tendencia_Semana3.pdf">Lectura de tendencia (PDF)</a></div>
</div>
<h2 class="sr">Cómo usar esta guía</h2>
{idea('El hilo de la semana: <b>que la red acierte en el examen no basta.</b> Tiene que funcionar con casos nuevos, aguantar cambios pequeños, aprovechar lo que ya se sabe y poder explicar por qué decide.')}
<div class="grid">
<div class="tile"><h3>1 · Lee</h3><p>Cada tema empieza con <b>la idea en una frase</b>. Si solo tienes 5 minutos, lee esas frases.</p></div>
<div class="tile"><h3>2 · Practica</h3><p>Resuelve los ejercicios en papel <b>antes</b> de abrir la respuesta. Equivocarse aquí es gratis.</p></div>
<div class="tile"><h3>3 · Lee el código</h3><p>Los notebooks NB05 y NB06 ya vienen <b>escritos y ejecutados</b>. Apuesta un resultado antes de cada celda y compáralo con lo que sale.</p></div>
<div class="tile"><h3>4 · Comprueba</h3><p>Al final juega el <a href="../quiz/index.html?final">quiz final</a>: te dice qué temas repasar.</p></div>
</div>
{box('ojo', 'Mapa de la semana: dos temas', '''<p><b>Recorderis:</b> las semanas 1 y 2 en una sola cadena, de la neurona a la CNN que reconoce ropa.</p>
<p><b>Tema 1 · ¿Funcionará con casos nuevos?</b> Aprender no es memorizar, frenos para la memoria, mover la foto, engañar a la red y vacunarla, el mundo que cambia y afinar sin hacer trampa · notebook <b>NB05</b>.</p>
<p><b>Tema 2 · ¿Puedo reutilizarla y explicar lo que decide?</b> Transfer learning con pocos datos, dónde miró la red, la prueba de cordura, explicar un «no» de crédito y las reglas que llegan · notebook <b>NB06</b>.</p>
<p><b>Cierre · ¿Le creerías a tu red?</b> Si trata a todos por igual y cinco preguntas antes de usar un modelo con personas. Cada sesión sigue donde terminó la anterior.</p>
<p>Las prácticas son <b>en clase y sin nota</b>. Las <a href="../docencia/slides/index.html">slides interactivas</a> quedan publicadas para repasar.</p>''')}
<p>Marca <b>«Ya lo entendí»</b> al final de cada tema: tu avance se guarda en este navegador y aparece en el índice.</p>
"""))


# ------------------------------------------------------------------ 00 · recap of weeks 1 and 2
def cadena():
    """The chain of weeks 1 and 2 as responsive cards (readable on a phone). Amber = what comes back this week."""
    steps = [('Neurona', 'z = w·x + b', 0), ('Pérdida', 'qué tan mal vamos', 0), ('Gradiente', 'bajar la montaña', 1), ('Keras', 'cuatro pasos', 0),
             ('Validación', 'el simulacro', 1), ('Suposición', 'densa · CNN · RNN', 0), ('CNN', 'la lupa: 87.7 %', 1), ('Atención', 'mirar directo', 0)]
    cards = ''.join(
        f'<li style="list-style:none;background:var(--paper);border:2px solid {"var(--amber-f)" if hot else "var(--blue)"};border-radius:14px;padding:10px 12px">'
        f'<span style="display:block;font:700 13px \'Space Grotesk\',sans-serif;color:var(--muted)">{"S1" if i < 5 else "S2"} · {i + 1}</span>'
        f'<b style="display:block;font:700 16px \'Space Grotesk\',sans-serif;color:var(--ink)">{t}</b>'
        f'<span style="font-size:14px;color:var(--muted)">{d}</span></li>' for i, (t, d, hot) in enumerate(steps))
    return (f'<ol style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;padding:0;margin:18px 0 8px">{cards}</ol>'
            '<p style="font-size:14.5px;color:var(--muted);margin:0 0 18px">En ámbar, las tres piezas que más vuelven esta semana: el <b>gradiente</b> '
            '(un ejemplo adversarial sube la montaña a propósito), la <b>validación</b> (el simulacro delata al que memoriza) y la <b>CNN</b> de ropa (es la red de toda la semana).</p>')


S.append(('rec', '00', 'Recorderis de las semanas 1 y 2', f"""
{idea('Esta semana no aparece una arquitectura nueva. Usamos la CNN de ropa de la semana 2 y nos hacemos otras preguntas: ¿funciona con casos nuevos?, ¿aguanta cambios?, ¿puedo reutilizarla?, ¿puedo explicar lo que decide?')}
{cadena()}
<table><tr><th>Pieza</th><th>Qué es, en una frase</th><th>Dónde vuelve esta semana</th></tr>
<tr><td><b>Entrenamiento, validación y prueba</b></td><td>La red <b>estudia</b> con el entrenamiento, se mide en un <b>simulacro</b> (validación) y al final rinde el <b>examen final</b> (prueba), una sola vez.</td><td>El simulacro delata a la red que memoriza y sirve para afinar sin hacer trampa.</td></tr>
<tr><td><b>Pérdida</b></td><td>Un solo número que dice qué tan mal vamos: más pequeño es mejor.</td><td>Las curvas de pérdida de entrenamiento y de validación.</td></tr>
<tr><td><b>Descenso de gradiente</b></td><td>La pendiente dice hacia dónde sube la pérdida; los pesos dan un paso <b>en contra</b>, de largo η.</td><td>Un ejemplo adversarial hace lo contrario con la foto: un paso <b>cuesta arriba</b>.</td></tr>
<tr><td><b>Keras en 4 pasos</b></td><td>Construir, compilar, entrenar (<code>fit</code>) y predecir.</td><td>Los frenos son capas (<code>Dropout</code>, <code>RandomTranslation</code>) y un aviso para <code>fit</code> (<code>EarlyStopping</code>).</td></tr>
<tr><td><b>La suposición de cada arquitectura</b></td><td>Densa: todo con todo. CNN: lo cercano importa. RNN: el orden importa. Atención: cada parte mira a todas.</td><td>Una suposición ayuda a generalizar, pero no hace robusta a la red.</td></tr>
<tr><td><b>La CNN de ropa (NB03)</b></td><td>Fashion-MNIST, 12 810 parámetros, <b>87.7 %</b> en el examen final.</td><td>Es la red de toda la semana.</td></tr>
<tr><td><b>Mover la prenda</b></td><td>Con 2 píxeles: densa 56.5 %, CNN 75.2 %. Con 4 píxeles la CNN cae a <b>28.2 %</b>.</td><td>La promesa de la semana 2: aquí vemos cómo hacerla más robusta.</td></tr>
<tr><td><b>Métricas</b></td><td>La exactitud puede engañar: un modelo que dice «al día» a todos acierta el 87 % y no encuentra ni un moroso.</td><td>Esta semana miramos al modelo <b>por grupo</b> (zona rural y urbana).</td></tr></table>
{box('analogia', 'Lo que cambia esta semana', '<p>Hasta ahora la pregunta era <b>«¿qué tan exacto es mi modelo?»</b>. Si un estudiante saca 100 en un examen que ya conocía, ¿confiarías en él para un trabajo nuevo? Esta semana se suman cuatro preguntas: ¿funcionará con casos nuevos?, ¿aguanta cambios pequeños?, ¿puedo reutilizar lo que ya sabe? y ¿puedo explicar por qué decide?</p>')}
<h3>Para comprobar</h3>
{ex('Si la red no aprende con la validación, ¿para qué la apartamos?', '<p>Es el <b>simulacro</b>: dice cómo le va con ejemplos que no estudió. Con él decidimos cuándo parar y qué ajustes usar. El examen final se usa una sola vez, al terminar.</p>')}
{ex('Un peso vale 2, la pendiente de la pérdida es +4 y η = 0.1. El peso nuevo es 2 − 0.1 × 4 = 1.6. ¿Qué pasaría con la pérdida si en vez de restar sumáramos?', '<p>Subiría: daríamos un paso <b>cuesta arriba</b>. Nadie entrena así, pero esa es justo la idea de un ejemplo adversarial, aplicada a los píxeles de la foto en vez de a los pesos.</p>')}
{ex('La CNN de la semana 2 acierta 87.7 % y cae a 28.2 % si la prenda se mueve 4 píxeles. ¿Es exacta? ¿Es robusta?', '<p>Es <b>exacta</b> en el examen, pero <b>no es robusta</b>: un cambio pequeño la tumba. Son dos cosas distintas, y esta semana aprendemos a medir y a mejorar la segunda.</p>')}
<p>Si alguna pieza no te queda clara: la <a href="../../guia/index.html">guía de la semana 1</a> (neurona, pérdida, gradiente, Keras) y la <a href="../../semana2/guia/index.html">guía de la semana 2</a> (CNN, RNN y atención).</p>
"""))

# ------------------------------------------------------------------ 01 · memorizing and brakes
sb, rg = F.T1['sobreajuste'], F.T1['regularizada']
S.append(('b01', 'T1', 'Aprender no es memorizar: sobreajuste y frenos', f"""
{idea('Aprender es que te vaya bien con casos nuevos. Si la red se aprende de memoria los ejemplos de estudio, su pérdida de entrenamiento sigue bajando mientras la de validación sube: eso es el <b>sobreajuste</b>. Los frenos (aumento de datos, dropout y parar a tiempo) le dificultan memorizar, y el mejor freno de todos es tener más datos.')}
<h3>Primero, la necesidad</h3>
<p>Casi nunca tienes 60 000 fotos etiquetadas. En el NB05 le damos a la CNN de siempre solo <b>1 000 fotos</b> para estudiar, un simulacro de 2 000 y el examen final de 10 000, y la dejamos entrenar 60 épocas sin ningún freno.</p>
{box('analogia', 'Analogía: el solucionario', '<p>Un estudiante se aprende de memoria el solucionario del examen pasado. Saca casi 100 en los ejercicios que ya vio y falla los nuevos. No aprendió la materia: aprendió <b>esas</b> respuestas. La validación es el simulacro que lo delata antes del examen final.</p>')}
<h3>Idea clave 1 · Las curvas que se separan</h3>
{fig(F.curvas(), 'Las curvas reales del NB05. A la izquierda, sin frenos: la pérdida de entrenamiento baja hasta el final y la de validación es mínima en la época 33 y después sube. A la derecha, con frenos: bajan juntas.')}
<table><tr><th>Sin frenos, 1 000 fotos</th><th>Resultado</th></tr>
<tr><td>Exactitud en entrenamiento (época 60)</td><td><b>{F.pct(sb['train_acc'][-1])}</b></td></tr>
<tr><td>Exactitud en el simulacro (época 60)</td><td><b>{F.pct(sb['val_acc'][-1])}</b></td></tr>
<tr><td>Época con la menor pérdida de validación</td><td><b>{sb['best_epoch']}</b></td></tr>
<tr><td>Examen final (10 000 fotos)</td><td><b>{F.pct(sb['test'])}</b></td></tr></table>
<p class="read"><b>Léelo así:</b> hasta la época 33 las dos pérdidas bajan: la red aprende cosas que sirven para cualquier prenda. Desde ahí, la de entrenamiento sigue bajando y la de validación sube: lo que aprende ahora son detalles de esas 1 000 fotos (una arruga, un píxel suelto) que no sirven con fotos nuevas. La brecha de casi 14 puntos entre 96.7 % y 83.0 % es la señal del sobreajuste.</p>
<ul>
<li><b>Generalizar:</b> que te vaya bien con casos que no viste. Es lo único que nos importa de verdad.</li>
<li><b>Sobreajuste</b> (<i>overfitting</i>): memorizar los ejemplos de estudio; brecha grande entre entrenamiento y validación.</li>
<li><b>Subajuste</b> (<i>underfitting</i>): lo contrario, la red no aprende ni lo de estudio; las dos curvas se quedan altas.</li>
</ul>
<h3>¿Por qué memoriza?</h3>
<p>La CNN tiene <b>12 810</b> números que ajustar y solo 1 000 fotos: le sobra capacidad para acomodarse a cada foto en particular. Con 60 000 fotos esos detalles se promedian y memorizar se vuelve mucho más difícil. La misma red, con todas las fotos, llega a <b>87.7 %</b>.</p>
<h3>Idea clave 2 · Frenos para la memoria</h3>
<p>Regularizar es ponerle frenos a la memoria: cualquier truco que le haga más difícil a la red aprenderse los ejemplos y la obligue a quedarse con lo general.</p>
<ul>
<li><b>Aumento de datos</b> (<code>RandomTranslation</code>): en cada época la red ve las fotos movidas un poquito al azar. Es practicar con la misma prenda corrida: no puede memorizar la posición exacta de cada píxel.</li>
<li><b>Dropout</b> (<code>Dropout(0.3)</code>): en cada paso de entrenamiento apaga al azar el 30 % de los números de esa capa. Es un equipo que entrena sabiendo que en cada partido puede faltar cualquiera: nadie puede depender de un solo compañero.</li>
<li><b>Parar a tiempo</b> (<i>early stopping</i>): mirar el simulacro en cada época y detenerse cuando deja de mejorar. Es dejar de estudiar cuando el simulacro empieza a salir peor.</li>
<li><b>L2</b>, de pasada: una multa en la pérdida para los pesos muy grandes (<code>kernel_regularizer</code>). No la usamos en el NB05.</li>
</ul>
{fig(F.dropout(), 'Dropout: en cada paso se apagan neuronas distintas, así que ninguna puede depender de otra. Al predecir trabajan todas.')}
<h3>Los frenos en Keras</h3>
<pre><code>model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.RandomTranslation(0.05, 0.05),     # brake 1: move each photo up to 5 % (only while training)
    layers.Conv2D(16, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Flatten(),
    layers.Dropout(0.3),                      # brake 2: switch off 30 % of the numbers at random (only while training)
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=8,    # brake 3: stop when the mock exam stops improving
                                     restore_best_weights=True)         # ...and go back to the best epoch
model.fit(x_small, y_small, epochs=100, validation_data=(x_val, y_val), callbacks=[stop])</code></pre>
<p class="read"><b>Léelo así:</b> la red es la misma de la semana 2 con dos capas más: <code>RandomTranslation</code> mueve cada foto al azar antes de mirarla y <code>Dropout(0.3)</code> apaga al azar el 30 % de los 800 números antes de la salida. <code>EarlyStopping</code> es un aviso (un <i>callback</i>) que <code>fit</code> consulta al final de cada época: si la pérdida de validación no mejora en <b>8 épocas seguidas</b> (<code>patience</code>), detiene el entrenamiento y vuelve a los pesos de la mejor época. Ninguno de los tres cuesta parámetros.</p>
<h3>El resultado, con honestidad</h3>
<p>Con los tres frenos y un máximo de 100 épocas, el entrenamiento se detiene en la época <b>{rg['epochs']}</b> y se queda con la <b>{rg['best_epoch']}</b>. Las curvas ya no se separan ({lam('regularizada')}).</p>
<table><tr><th>Situación</th><th>Examen final</th></tr>
<tr><td>1 000 fotos, sin frenos</td><td>{F.pct(sb['test'])}</td></tr>
<tr><td>1 000 fotos, con los tres frenos</td><td>{F.pct(rg['test'])}</td></tr>
<tr><td>60 000 fotos, sin frenos (semana 2)</td><td><b>87.7 %</b></td></tr></table>
<p class="read"><b>Léelo así:</b> los frenos ayudan un poco (de 80.9 % a 81.6 %) y, sobre todo, la red ya no se engaña a sí misma: su exactitud de entrenamiento dice la verdad sobre lo que hará con fotos nuevas. Lo que ayuda <b>mucho</b> es tener más datos: con las 60 000 fotos, 87.7 %. Más datos es el mejor regularizador.</p>
{box('ojo', 'Solo al entrenar', '<p><code>RandomTranslation</code> y <code>Dropout</code> trabajan solo durante <code>fit</code>. En <code>predict</code> y <code>evaluate</code> se apagan solos: la red ve la foto tal cual y usa todas sus neuronas.</p>')}
{box('error', 'Errores comunes', '<ul><li>Mirar solo la exactitud de entrenamiento y celebrar un 97 %.</li><li>Elegir la mejor época mirando el examen final: el examen deja de medir casos nuevos.</li><li>Creer que el dropout borra neuronas para siempre.</li><li>Poner <code>patience</code> muy pequeño: un simulacro sube y baja un poco por azar.</li></ul>')}
<h3>Practica</h3>
{ex('En tu proyecto, la pérdida de validación sube desde la época 20 mientras la de entrenamiento sigue bajando. ¿Qué pasa y qué puedes hacer?', '<p>La red empezó a memorizar. Puedes parar cerca de la época 20 (early stopping), agregar frenos (aumento de datos, dropout) y, si se puede, conseguir más datos.</p>')}
{ex('Con <code>Dropout(0.5)</code> en una capa de 10 neuronas, ¿cuántas se apagan más o menos en cada paso de entrenamiento? ¿Y al predecir?', '<p>Unas 5 en cada paso, cada vez otras. Al predecir, ninguna.</p>')}
{ex('<code>EarlyStopping(patience=8, restore_best_weights=True)</code> y la menor pérdida de validación ocurre en la época 71. ¿En qué época se detiene y con qué pesos se queda?', '<p>Espera 8 épocas sin mejora: se detiene en la <b>79</b> y vuelve a los pesos de la <b>71</b>. Es lo que pasó en el NB05.</p>')}
{ex('¿Por qué decimos que más datos es el mejor freno?', '<p>Porque con muchas fotos los detalles de cada una se promedian y la red tiene que quedarse con lo general: la misma CNN pasa de 80.9 % con 1 000 fotos a 87.7 % con 60 000.</p>')}
{colab(NB5, '<b>NB05 · Generalizar y ser robusto</b>, partes 1 y 2: el estudiante que memoriza (las curvas con 1 000 fotos) y los frenos para la memoria.')}
"""))

# ------------------------------------------------------------------ 02 · robustness and tuning
au, fg, fe, bq = F.T1['aumento'], F.T1['fgsm'], F.T1['fgsm_entrenada'], F.T1['busqueda']
S.append(('b02', 'T1', 'Exacto no es robusto: fotos movidas, ejemplos adversariales y afinar sin trampa', f"""
{idea('Un modelo puede ser muy exacto en el examen y frágil ante un cambio pequeño: mover la foto, un ruido invisible elegido para engañarlo o un mundo que cambia. La robustez también se entrena, y los ajustes de la red se eligen con el simulacro, nunca con el examen final.')}
<h3>Primero, la necesidad</h3>
<p>La CNN de la semana 2 acierta 87.7 %. Pero si la prenda está corrida 4 píxeles cae a 28.2 %, peor que adivinar entre tres opciones. En el mundo real las fotos nunca llegan perfectamente centradas.</p>
<h3>Mover la foto: aumento de datos</h3>
<p>Entrenamos la misma CNN con las 60 000 fotos y 5 épocas, pero con <code>RandomTranslation(0.15)</code>: en cada época ve cada prenda movida al azar hasta un 15 % (unos 4 píxeles).</p>
{fig(F.mover(), 'Lo que pasa al mover la prenda en el examen final. Sin aumento la red se cae; con aumento aguanta.')}
<table><tr><th>Mover la prenda</th><th>0 px</th><th>1 px</th><th>2 px</th><th>3 px</th><th>4 px</th></tr>
<tr><td><b>Sin aumento</b></td><td>{F.pct(au['sin']['test'])}</td>{''.join(f"<td>{F.pct(au['sin']['shift'][str(k)])}</td>" for k in range(1, 5))}</tr>
<tr><td><b>Con aumento</b></td><td>{F.pct(au['con']['test'])}</td>{''.join(f"<td>{F.pct(au['con']['shift'][str(k)])}</td>" for k in range(1, 5))}</tr></table>
<p class="read"><b>Léelo así:</b> con aumento la red aprendió que moverse no cambia la clase: con 4 píxeles aguanta 76.4 % en vez de 28.2 %. El precio: con las fotos sin mover baja de 87.7 % a 82.6 %, porque con las mismas 5 épocas tiene que aprender algo más difícil. Compramos robustez a cambio de unos puntos.</p>
<h3>Idea clave 3 · Engañar a la red: ejemplos adversariales</h3>
<p>En 2015, Goodfellow, Shlens y Szegedy mostraron que basta con alterar los píxeles de una imagen de forma imperceptible para que una red la clasifique mal con total seguridad. Un <b>ejemplo adversarial</b> es una foto cambiada muy poquito, <b>a propósito</b>, en la dirección que más confunde a la red.</p>
{box('analogia', 'Analogía: subir la montaña a propósito', '<p>Al entrenar, el gradiente dice hacia dónde sube la pérdida y los <b>pesos</b> bajan la montaña. Para engañar a la red hacemos lo contrario: dejamos los pesos quietos y movemos cada <b>píxel</b> un pasito <b>cuesta arriba</b>, donde la red se equivoca más.</p>')}
{formula(r"x' = x + \varepsilon \cdot \operatorname{signo}\!\big(\nabla_{x}\,\text{pérdida}\big)",
         [(r'x', 'la foto original (cada píxel entre 0 y 1)', B), (r'\nabla_x\,\text{pérdida}', 'hacia dónde sube la pérdida si cambia cada píxel', A),
          (r'\operatorname{signo}', 'se queda solo con +1 o −1 en cada píxel', T), (r'\varepsilon', 'cuánto se permite cambiar cada píxel: 0.05 = 5 % del brillo', P)],
         read='la foto engañosa es la foto original más un pasito de tamaño épsilon en cada píxel, hacia arriba o hacia abajo, según hacia dónde suba la pérdida. Se llama FGSM (<i>fast gradient sign method</i>): un solo paso, calculado con el gradiente.')}
{fig(F.adversarial(), 'El primer botín de prueba. La red lo ve como botín con 96 %; con un ruido de ± 0.05 por píxel dice «zapatilla» con 67 %. A la vista es la misma foto.')}
<pre><code>x = tf.convert_to_tensor(x_test[:1])                 # the first botín of the test set
with tf.GradientTape() as tape:                      # records the operations to compute slopes
    tape.watch(x)                                    # the slope with respect to the PIXELS, not the weights
    loss = keras.losses.sparse_categorical_crossentropy(y_test[:1], cnn(x))
grad = tape.gradient(loss, x)                        # for each pixel: in which direction does the loss go up?
x_adv = tf.clip_by_value(x + 0.05 * tf.sign(grad), 0, 1)   # one small step UP the hill, kept between 0 and 1</code></pre>
<p class="read"><b>Léelo así:</b> <code>GradientTape</code> es la grabadora que TensorFlow usa por dentro para la retropropagación; con <code>tape.watch(x)</code> le pedimos la pendiente con respecto a la foto. Después sumamos 0.05 en la dirección del signo y recortamos entre 0 y 1 para que siga siendo una foto válida. Son cinco líneas.</p>
{fig(F.fgsm_curva(), 'Exactitud de la CNN frente a ejemplos adversariales cada vez más fuertes, y la misma CNN vacunada.')}
<table><tr><th>ε (cuánto cambia cada píxel)</th><th>0</th><th>0.01</th><th>0.02</th><th>0.05</th><th>0.1</th></tr>
<tr><td><b>La CNN normal</b></td>{''.join(f"<td>{F.pct(fg[k])}</td>" for k in ('limpia', '0.01', '0.02', '0.05', '0.1'))}</tr>
<tr><td><b>Vacunada</b></td>{''.join(f"<td>{F.pct(fe[k])}</td>" for k in ('limpia', '0.01', '0.02', '0.05', '0.1'))}</tr></table>
<h3>Vacunar a la red: entrenamiento adversarial</h3>
<p>Si la red se deja engañar por esos ejemplos, se los mostramos al estudiar: en cada lote del entrenamiento van las fotos limpias <b>y</b> su versión FGSM con ε = 0.05, con su etiqueta correcta. Es <b>vacunarse</b>: exponerse a una versión controlada del ataque.</p>
<p class="read"><b>Léelo así:</b> con ε = 0.05 la red normal cae a 39.2 % y la vacunada aguanta 71.7 %. La vacuna tiene un costo: con fotos limpias baja de 87.7 % a 84.1 %. Y no es un escudo total: con ε = 0.1 la vacunada también cae (57.2 %).</p>
<h3>El riesgo más común: el mundo cambia</h3>
<p>Nadie tiene que atacar a un modelo para que falle. Un modelo de crédito entrenado con socios urbanos puede fallar con socios rurales; uno entrenado antes de una crisis económica puede fallar después de ella. A esto se le llama <b>cambio de distribución</b>: los datos nuevos ya no se parecen a los de estudio. Lo peligroso es que <b>el modelo no avisa</b>: sigue respondiendo con la misma seguridad ({lam('mundo-cambia')}).</p>
<p>Qué se hace: validar con datos recientes y del lugar donde se usará, medir por grupos y vigilar el modelo en uso (si sus respuestas o los datos que recibe cambian, algo pasa).</p>
<h3>Afinar sin hacer trampa: los hiperparámetros</h3>
<p>Los <b>hiperparámetros</b> son lo que eliges tú antes de entrenar y la red no aprende: el learning rate, el número de filtros, el dropout, las épocas. Para elegirlos se prueban varias combinaciones y se comparan <b>en el simulacro</b>. Una forma sencilla y eficaz es la <b>búsqueda al azar</b> (Bergstra y Bengio, 2012): sortear combinaciones en vez de probarlas todas.</p>
{box('analogia', 'Analogía: afinar la guitarra', '<p>Se afina con el simulacro, nunca con el examen final. Si eliges la combinación que mejor sale en el examen final, ese número deja de ser honesto: ya no mide casos nuevos, mide lo bien que elegiste para ese examen.</p>')}
{fig(F.busqueda(), 'Las 6 combinaciones al azar del NB05 (10 000 fotos, 4 épocas, simulacro de 5 000). La mejor, medida una sola vez en el examen final.')}
<p class="read"><b>Léelo así:</b> entre learning rate {{0.0001, 0.001, 0.01}}, filtros {{8, 16, 32}} y dropout {{0, 0.3}} se sortearon 6 combinaciones. La mejor en el simulacro fue learning rate 0.01, 32 filtros y dropout 0.3 (34 826 parámetros): <b>86.8 %</b>. En el examen final, medido una sola vez, dio <b>86.9 %</b>: el simulacro no mintió. Con learning rate 0.0001 la red apenas avanzó en 4 épocas (69.3 % y 72.6 %): pasos demasiado pequeños.</p>
{box('error', 'Errores comunes', '<ul><li>Creer que un modelo exacto es robusto.</li><li>Probar la robustez con ruido al azar: el ruido adversarial se elige para engañar y es mucho más dañino.</li><li>Elegir hiperparámetros mirando el examen final.</li><li>Pensar que el entrenamiento adversarial protege contra todo.</li></ul>')}
<h3>Practica</h3>
{ex('Un píxel vale 0.40 y el signo de su gradiente es −1. Con ε = 0.05, ¿cuánto vale en la foto adversarial? ¿Y si ε = 0?', '<p>0.40 + 0.05 × (−1) = <b>0.35</b>. Con ε = 0 la foto queda igual.</p>')}
{ex('¿Por qué decimos que el ejemplo adversarial «sube la montaña»?', '<p>Porque da un paso en la dirección en que <b>sube</b> la pérdida, justo lo contrario del descenso de gradiente. Y lo da sobre los píxeles, no sobre los pesos.</p>')}
{ex('Con ε = 0.05, ¿cuánto acierta la red normal y cuánto la vacunada? ¿Qué costo pagó la vacunada?', '<p>39.2 % contra 71.7 %. El costo: con fotos limpias baja de 87.7 % a 84.1 %.</p>')}
{ex('Probaste 20 combinaciones y eliges la que da 90 % en el examen final. ¿Qué problema hay?', '<p>Ese 90 % ya no es una medida honesta: elegiste mirando el examen. Había que elegir con la validación y medir el examen una sola vez, al final.</p>')}
{ex('Un modelo de mora se entrenó con socios de 2019. ¿Qué revisarías antes de usarlo en 2026?', '<p>Si los socios de hoy se parecen a los de 2019 (el mundo cambia): validarlo con datos recientes, mirar sus resultados por grupo y vigilarlo mientras se usa.</p>')}
{colab(NB5, '<b>NB05</b>, partes 3 a 6: mover la foto, engañar a la red (FGSM a mano), vacunarla y afinar con búsqueda al azar. Al final, los <b>ejercicios</b> y el <b>Experimento 5</b> (opcional).')}
"""))

# ------------------------------------------------------------------ 03 · transfer learning
tf_ = F.T2['transfer']
S.append(('b03', 'T2', 'Reutilizar lo aprendido: transfer learning', f"""
{idea('Transfer learning es reutilizar lo que una red ya aprendió en otra tarea. Se <b>congelan</b> sus capas, que ya saben ver bordes y formas, y solo se entrena una salida nueva; o se ajustan un poco todas, con pasos pequeños (<b>ajuste fino</b>). Ayuda sobre todo cuando tienes pocos datos.')}
<h3>Primero, la necesidad</h3>
<p>Una asociación de productores quiere reconocer enfermedades del cacao con fotos de hojas, pero solo tiene unas pocas decenas por enfermedad. Entrenar una red desde cero con tan poco es casi imposible: memoriza enseguida. Pocas organizaciones entrenan sus modelos desde cero: la mayoría parte de un modelo que ya entrenó otra empresa con enormes cantidades de datos y lo ajusta a su problema.</p>
{box('analogia', 'Analogía: el profesional con experiencia', '<p>Es como contratar a un profesional con experiencia y darle una inducción corta sobre tu empresa. Aprende rápido, pero trae hábitos de trabajos anteriores que no conoces del todo. <b>Congelar</b> es usar su experiencia tal cual y enseñarle solo la última parte; el <b>ajuste fino</b> es dejar que también ajuste un poco sus hábitos.</p>')}
<h3>El experimento del NB06</h3>
<ul>
<li><b>La red base:</b> la CNN de siempre, entrenada 5 épocas con 6 clases que <b>no son prendas de arriba</b> (pantalón, vestido, sandalia, zapatilla, bolso y botín): {F.pct(F.T2['base_6clases'])} en esas clases. Nunca vio una camiseta.</li>
<li><b>La tarea nueva:</b> 4 prendas de arriba muy parecidas entre sí (camiseta, suéter, abrigo y camisa); adivinar da 25 %. Examen final de 4 000 fotos y simulacro de 200.</li>
<li><b>Tres formas de aprenderla</b> con 5, 20 y 100 fotos por clase: desde cero, con la base congelada y con ajuste fino.</li>
</ul>
{fig(F.congelar(), 'Congelar: las capas que ya saben ver no se tocan y solo se entrena la salida nueva. Ajuste fino: después se ajusta todo con pasos pequeños.')}
<pre><code>new = keras.Sequential([keras.Input(shape=(28, 28, 1)), *base_layers,   # the layers that already learned to see
                        layers.Dense(4, activation="softmax")])          # a new output: 4 kinds of tops
for layer in base_layers:
    layer.trainable = False                    # 1 · freeze: keep what it learned, train only the new output
new.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
new.fit(x_few, y_few, epochs=100, validation_data=(x_val, y_val), callbacks=[stop])

for layer in base_layers:
    layer.trainable = True                     # 2 · fine-tune: unlock everything...
new.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001),       # ...with small steps, so it does not forget
            loss="sparse_categorical_crossentropy", metrics=["accuracy"])
new.fit(x_few, y_few, epochs=40, validation_data=(x_val, y_val), callbacks=[stop])</code></pre>
<p class="read"><b>Léelo así:</b> la red nueva reutiliza las capas de la base y les pone una salida nueva de 4 clases. Con <code>trainable = False</code> esas capas quedan congeladas: de los 8 004 números de la red solo se entrenan <b>3 204</b>, los de la salida nueva (800 × 4 + 4). Para el ajuste fino se descongelan y se vuelve a compilar con un learning rate 10 veces más pequeño que el habitual de Adam (0.001): pasos pequeños para no borrar lo que ya sabía. Ojo: <code>trainable</code> se cambia <b>antes</b> de <code>compile</code>.</p>
<h3>Idea clave 4 · Ayuda sobre todo con pocos datos</h3>
{fig(F.transfer(), 'Exactitud real del NB06 en el examen final de las 4 prendas de arriba.')}
<table><tr><th>Fotos por clase para estudiar</th><th>Desde cero</th><th>Congelada</th><th>Ajuste fino</th></tr>
{''.join(f"<tr><td>{n} ({4 * int(n)} fotos)</td><td>{F.pct(tf_[n]['desde_cero'])}</td><td>{F.pct(tf_[n]['congelada'])}</td><td>{F.pct(tf_[n]['ajuste_fino'])}</td></tr>" for n in ('5', '20', '100'))}</table>
<p class="read"><b>Léelo así:</b> con solo 5 fotos por clase, lo heredado vale <b>unos 15 puntos</b> (30.6 % → 45.9 % y 47.2 %). Con 20 fotos la ventaja casi desaparece y con 100, entrenar desde cero empata o gana (68.8 %). Lección honesta: la experiencia heredada ayuda mucho cuando hay muy pocos datos. Aquí la base aprendió con pantalones y calzado, que se parecen poco a una camisa; en la vida real la base aprendió de millones de fotos variadas y la ventaja es mucho mayor.</p>
<h3>En la vida real</h3>
<ul>
<li><b>Imágenes:</b> <code>keras.applications</code> trae redes ya entrenadas con <b>ImageNet</b>, más de un millón de fotos de 1 000 clases (MobileNetV2, ResNet50, EfficientNet…).</li>
<li><b>Texto:</b> casi todos los modelos de lenguaje se usan así: se parte de un modelo preentrenado y se ajusta. Técnicas como <b>LoRA</b> (Hu y colegas, 2022) modifican solo una pequeña parte del modelo.</li>
</ul>
<pre><code>base = keras.applications.MobileNetV2(input_shape=(160, 160, 3), include_top=False, weights="imagenet")
base.trainable = False                         # freeze what it learned from ImageNet
model = keras.Sequential([base, layers.GlobalAveragePooling2D(),          # summarize each map in one number
                          layers.Dense(4, activation="softmax")])         # the new output for YOUR classes</code></pre>
{box('curioso', 'Heredas lo que no conoces', '<p>Esa herencia ahorra datos, cómputo y tiempo, pero el modelo puede traer sesgos o puntos ciegos aprendidos de datos que nunca viste. Antes de usarlo con personas conviene preguntar: ¿alguien sabe qué datos lo formaron?</p>')}
{box('error', 'Errores comunes', '<ul><li>Hacer el ajuste fino con un learning rate grande: borra lo que la red ya sabía.</li><li>Cambiar <code>trainable</code> después de <code>compile</code> sin volver a compilar.</li><li>Dar por hecho que heredar siempre gana: con 100 fotos por clase, desde cero empató.</li></ul>')}
<h3>Practica</h3>
{ex('Con 100 fotos por clase, desde cero da 68.8 % y congelada 66.7 %. ¿Por qué lo heredado ya no ayuda?', '<p>Porque ya hay datos suficientes para aprender desde cero, y lo que sabía la base (pantalones, calzado, bolsos) se parece poco a las prendas de arriba.</p>')}
{ex('Con la base congelada solo se entrenan 3 204 de los 8 004 números. ¿Cuáles son?', '<p>Los de la salida nueva: 800 números de entrada × 4 clases + 4 sesgos = 3 204.</p>')}
{ex('Una clínica tiene 300 radiografías etiquetadas. ¿Entrena desde cero o usa transfer learning? ¿Qué cuidaría?', '<p>Transfer learning: partir de una red preentrenada, congelar y después un ajuste fino con pasos pequeños, eligiendo con validación. Y preguntar con qué datos se entrenó la base.</p>')}
{ex('¿Por qué el ajuste fino usa learning rate 0.0001 y no 0.01?', '<p>Para dar pasos pequeños: con pasos grandes la red se alejaría de lo que ya sabía y lo olvidaría.</p>')}
{colab(NB6, '<b>NB06 · Reutilizar y explicar</b>, parte 1: la red que nunca vio camisetas, con 5, 20 y 100 fotos por clase.')}
"""))

# ------------------------------------------------------------------ 04 · explain and verify
co = F.T2['coop']; so = co['socia']; cr = F.T2['cordura']
NSOC = f"{co['n']:,}".replace(',', ' ')            # 6 000 (Spanish thousands separator)
sg = lambda v: f'{v:.2f}'.replace('-', '−')         # −0.12 with a real minus sign
S.append(('b04', 'T2', 'Explicar y verificar: ¿por qué decidió eso?', f"""
{idea('Como nadie escribió las reglas de una red, usamos herramientas que la observan desde afuera: la oclusión y Grad-CAM en imágenes, la importancia por permutación y SHAP en tablas. Son <b>interpretaciones del modelo, no el modelo</b>: también se ponen a prueba, y una buena explicación depende de a quién va dirigida.')}
<h3>Primero, la necesidad</h3>
<p>Una cooperativa usa un modelo para decidir créditos. Una socia recibe un «no» y pregunta, con todo derecho: ¿por qué? En Ecuador, desde marzo de 2026, «así lo decidió el sistema» ya no basta: una norma permite a las personas afectadas por decisiones automatizadas pedir <b>una explicación de la lógica aplicada por el algoritmo</b> ({lam('por-que-explicar')}).</p>
<p>Un programa tradicional se puede leer línea por línea. Una red aprende sus propias reglas y las reparte en miles de números que nadie escribió. Por eso usamos métodos de explicación <b>post hoc</b>: miran el modelo ya entrenado e intentan describir qué influyó en una decisión.</p>
<h3>¿Dónde miró la red?</h3>
<ul>
<li><b>Oclusión:</b> tapar un cuadrito de 6 × 6 píxeles, como con la mano, y medir cuánto baja la probabilidad de la clase. Se repite en toda la foto: donde más baja, más importaba.</li>
<li><b>Grad-CAM</b> (Selvaraju y colegas, 2017): un mapa de calor que usa los gradientes de la última capa convolucional (32 mapas de 11 × 11) para pintar las zonas que más empujaron hacia la clase.</li>
<li><b>Gradiente × imagen:</b> el gradiente de la clase con respecto a cada píxel, multiplicado por el píxel. Es el más sencillo de calcular.</li>
</ul>
{formula(r'\alpha_k = \text{promedio}_{i,j}\;\frac{\partial\, p_{\text{clase}}}{\partial A^k_{ij}} \qquad\qquad \text{mapa} = \operatorname{ReLU}\Big(\sum_{k} \alpha_k\, A^k\Big)',
         [(r'A^k', 'el mapa k de la última capa convolucional (11 × 11)', B), (r'\partial p / \partial A^k_{ij}', 'cuánto sube la probabilidad si esa casilla se enciende más', A),
          (r'\alpha_k', 'cuánto importa el mapa k para esta clase', T), (r'\operatorname{ReLU}', 'se queda solo con lo que empuja a favor', P)],
         read='primero se calcula cuánto importa cada uno de los 32 mapas para la clase (el promedio de su gradiente). Después se suman los mapas, cada uno pesado por su importancia, y se borra lo negativo. El resultado de 11 × 11 se agranda a 28 × 28 y se pinta encima de la foto.')}
{fig(F.mapas(), 'Mapas reales del NB06 para tres fotos de prueba, con la probabilidad que la red le dio a la clase correcta. Cuanto más color, más influyó esa zona.')}
<p class="read"><b>Léelo así:</b> en el botín, la oclusión y Grad-CAM se encienden sobre el cuerpo y la suela; en el bolso, la oclusión marca la zona del centro. Gradiente × imagen, en cambio, se parece mucho a la foto misma: dibuja la prenda entera. ¿Cuál dice la verdad sobre la red? Para eso está la prueba de cordura.</p>
{box('analogia', 'Para qué sirve mirar', '<p>Si un modelo dice «neumonía», el mapa debería iluminar el pulmón y no una etiqueta del hospital en la esquina de la radiografía. Un mapa así destapa a la red que acierta por la razón equivocada (un atajo).</p>')}
<h3>Idea clave 5 · La prueba de cordura</h3>
<p>En 2018, Adebayo y sus colegas propusieron una prueba muy simple: tomar la red entrenada, <b>borrar lo que aprendió</b> poniendo sus pesos al azar y volver a calcular los mapas. Si el método es fiel al modelo, el mapa debe cambiar por completo, porque el modelo ya no sabe nada.</p>
{box('analogia', 'Analogía: el traductor que sigue el tono', '<p>Es como un traductor que, aunque cambies el discurso del orador, sigue diciendo frases parecidas porque se guía por el tono de voz y no por las palabras. Suena convincente, pero no traduce.</p>')}
{fig(F.cordura(), 'La prueba de cordura del NB06: el mismo botín con la red entrenada y con pesos al azar, y el parecido promedio en 30 fotos.')}
<p>Para medir el parecido usamos la <b>correlación de Spearman</b> entre los dos mapas: 1 quiere decir que ordenan las zonas igual y 0 que no tienen nada que ver.</p>
<table><tr><th>Método</th><th>Parecido con pesos al azar</th><th>¿Pasa?</th></tr>
<tr><td><b>Grad-CAM</b></td><td>{sg(cr['gradcam'])}</td><td>Sí: el mapa cambia por completo</td></tr>
<tr><td><b>Oclusión</b></td><td>{sg(cr['oclusion'])}</td><td>Sí</td></tr>
<tr><td><b>Gradiente × imagen</b></td><td><b>{sg(cr['gradx'])}</b></td><td><b>No:</b> casi el mismo mapa aunque la red no sepa nada; se parece a la foto</td></tr></table>
<p class="read"><b>Léelo así:</b> un mapa de gradiente × imagen se ve muy convincente, pero sale casi igual con una red que no aprendió nada: dibuja la foto, no la decisión. La lección no es tirar las herramientas, sino <b>verificarlas</b>: una explicación también debe pasar pruebas antes de presentarse como verdad. Coincide con lo que encontraron Adebayo y colegas.</p>
<h3>Explicar una decisión de crédito</h3>
<p>Volvemos a una tabla. En el NB06 inventamos una cooperativa con <b>{NSOC}</b> socios ficticios y 7 datos por socio: ingreso, carga (cuota ÷ ingreso), antigüedad en meses, atrasos en los últimos 12 meses, si tiene garante, ahorro (en meses de ingreso) y si vive en zona rural. El {F.pct(co['tasa_mora'])} cae en mora. Una red densa 16-8-1 logra un <b>AUC de {co['auc']:.2f}</b> y {F.pct(co['acc'])} de exactitud, y rechaza (probabilidad ≥ 0.5) al {F.pct(co['rechazados'])}.</p>
<p>El <b>AUC</b> responde: si tomo un socio que cae en mora y uno que no, ¿qué tan seguido el modelo le da más riesgo al primero? 0.5 es adivinar y 1 es perfecto.</p>
<h4>Lo que importa en general: importancia por permutación</h4>
<p>Se <b>mezcla</b> una columna al azar (como barajar las cartas de esa columna entre los socios) y se mide cuánto baja el AUC. Si el modelo dependía de esa columna, se desploma; si no la usaba, no pasa nada.</p>
{fig(F.importancia(), 'Importancia por permutación en la cooperativa ficticia: lo que más usa el modelo, en general, es la carga.')}
<h4>Lo que pesó en su caso: SHAP</h4>
<p>La socia (ficticia): ingreso de $506, carga 0.29 (una cuota de unos $144), 1 mes de antigüedad, <b>2 atrasos</b>, sin garante, 1.5 meses de ahorro y zona rural. Probabilidad de mora: <b>{round(100 * so['prob'])} %</b> → rechazada.</p>
<p><b>SHAP</b> (Lundberg y Lee, 2017) reparte su resultado entre sus datos, como se repartiría el mérito de un gol entre los jugadores que participaron en la jugada: parte del promedio de todos los socios y suma lo que aportó cada dato.</p>
{formula(r'p_{\text{socia}} = \text{base} + \sum_{j} \phi_j',
         [(r'\text{base}', f'el promedio de todos: {so["base"]:.2f}', B), (r'\phi_j', 'lo que empuja el dato j (positivo: hacia rechazar)', A)],
         read=f'su probabilidad es el promedio más lo que aportó cada uno de sus datos: {so["base"]:.2f} + 0.30 (atrasos) + 0.08 (rural) + 0.04 (sin garante) + 0.04 (antigüedad) + 0.02 (ingreso) + 0.02 (ahorro) − 0.02 (carga) = {so["prob"]:.2f}.')}
{fig(F.shap_socia(), 'SHAP de la socia: desde el promedio, cada dato empuja hacia rechazar o hacia aprobar hasta llegar a su probabilidad.')}
<p class="read"><b>Léelo así:</b> lo que más pesa <b>en general</b> (la carga) no es lo que más pesó <b>en su caso</b> (sus atrasos, +0.30). En su caso, la carga incluso empuja un poco hacia aprobar (−0.02). La importancia explica al modelo; SHAP explica una decisión.</p>
<h3>Lo que le sirve a la socia: el contrafactual</h3>
<p>A ella no le interesa la contribución de cada variable, sino <b>qué tendría que cambiar para ser aprobada</b>. Eso es un <b>contrafactual</b> ({lam('contrafactual')}):</p>
<ul>
<li>Sin sus 2 atrasos, su probabilidad bajaría a <b>{round(100 * co['sin_atrasos_prob'])} %</b>.</li>
<li>O con una cuota de unos $124 en vez de $144 ($20 menos al mes, por ejemplo con un plazo más largo), bajaría a <b>{round(100 * co['contrafactual_carga']['prob'])} %</b> y la aprobarían.</li>
</ul>
<table><tr><th>Destinatario</th><th>Lo que necesita saber</th><th>La explicación que le sirve</th></tr>
<tr><td><b>El científico de datos</b></td><td>¿El modelo es correcto? ¿Usa lo que debe?</td><td>Importancia, SHAP, mapas… y la prueba de cordura</td></tr>
<tr><td><b>La persona afectada</b></td><td>¿Qué puedo hacer?</td><td>El contrafactual y la revisión de una persona</td></tr></table>
<p>Rara vez la misma explicación sirve para los dos.</p>
<h3>¿Y si le preguntamos al propio modelo?</h3>
<p>Los modelos de lenguaje pueden explicar sus respuestas con palabras, pero esa explicación también es texto generado por el modelo ({lam('ia-se-explica')}):</p>
<ul>
<li>Al preguntarle a un modelo cómo sumó 36 + 59, respondió con el método escolar de «llevar uno»; por dentro combinaba una estimación aproximada con un cálculo preciso de la última cifra (Lindsey y colegas, 2025).</li>
<li>Ese mismo estudio, que abrió el modelo por dentro (<b>interpretabilidad mecanicista</b>), vio que ante «¿cuál es la capital del estado donde está Dallas?» representaba Texas como paso intermedio antes de decir Austin. Aun así, el método dio una comprensión satisfactoria en cerca de una cuarta parte de los casos.</li>
<li>Con una pista escondida en la pregunta, Claude 3.7 Sonnet mencionó en su razonamiento que la usó solo el 25 % de las veces y DeepSeek R1 el 39 % (Anthropic, 2025). Leer ese razonamiento es una oportunidad valiosa pero «frágil» (Korbak y colegas, 2025).</li>
</ul>
{box('analogia', 'Analogía de la lectura', '<p>Pedirle a un modelo que explique su respuesta se parece a preguntarle a alguien por qué eligió una camisa: te dará una razón coherente, pero no siempre la que realmente influyó.</p>')}
<h3>La tendencia: llegan las reglas</h3>
<table><tr><th>Cuándo</th><th>Dónde</th><th>Qué pasó (según la lectura)</th></tr>
<tr><td>diciembre de 2024</td><td>Brasil</td><td>El Senado aprobó el proyecto de ley 2338/2023, que clasifica los sistemas de IA según su riesgo; en octubre de 2026 seguía pendiente en la Cámara de Diputados.</td></tr>
<tr><td>marzo de 2026</td><td>Ecuador</td><td>La Superintendencia de Protección de Datos Personales publicó una norma para el uso de IA: evaluaciones de impacto, revisión humana de decisiones automatizadas con efectos jurídicos y derecho a pedir una explicación de la lógica del algoritmo.</td></tr>
<tr><td>julio de 2026</td><td>Unión Europea</td><td>El paquete «Digital Omnibus» aplazó las obligaciones para la IA de alto riesgo del AI Act, del 2 de agosto de 2026 al 2 de diciembre de 2027.</td></tr>
<tr><td>octubre de 2026</td><td>Ecuador</td><td>La Asamblea Nacional tramitaba 12 proyectos de ley sobre IA; uno propone el derecho a recibir explicaciones.</td></tr></table>
<p>La dirección es clara: quien use IA para decidir sobre personas deberá explicar, documentar y permitir la revisión humana. Lo que todavía no está claro es si sabemos hacerlo bien.</p>
{hist('2017', 'En el mismo año aparecieron Grad-CAM (Selvaraju y colegas) para imágenes y SHAP (Lundberg y Lee) para tablas, hoy dos de las herramientas de explicación más usadas. Un año después, la prueba de cordura (Adebayo y colegas, 2018) mostró que algunos mapas populares no explicaban al modelo.')}
<h3>Debates abiertos (para la encuesta y la clase)</h3>
<ul>
<li><b>Interpretable o explicado:</b> Cynthia Rudin (2019) sostiene que, en decisiones de alto impacto, hay que usar modelos interpretables por diseño en lugar de explicar cajas negras después. ¿Cuánta exactitud sacrificarías por entender un modelo?</li>
<li><b>Explicación o verdad:</b> una explicación clara genera confianza; si no refleja lo que el modelo calcula, genera una confianza falsa.</li>
<li><b>Regular ahora o esperar:</b> si la ciencia de explicar todavía es inmadura, ¿explicar se puede volver un trámite sin contenido?</li>
<li><b>Reutilizar o entender:</b> el transfer learning ahorra recursos, pero heredamos lo que no podemos auditar.</li>
</ul>
{box('error', 'Errores comunes', '<ul><li>Presentar un mapa de calor como «lo que piensa la red» sin ponerlo a prueba.</li><li>Confundir lo que importa en general (importancia) con lo que pesó en un caso (SHAP).</li><li>Darle a la persona afectada una lista de contribuciones en vez de decirle qué puede hacer.</li><li>Creerle sin más a la explicación que da el propio modelo.</li></ul>')}
<h3>Practica</h3>
{ex('Grad-CAM de una red que detecta neumonía ilumina la esquina donde está la marca del hospital. ¿Qué concluyes?', '<p>La red usa un <b>atajo</b>: reconoce el hospital (donde quizá hay más casos), no el pulmón. No hay que confiar en ella aunque acierte; hay que revisar los datos.</p>')}
{ex('¿Qué resultado esperas de un buen método en la prueba de cordura: un parecido cerca de 1 o cerca de 0?', '<p>Cerca de <b>0</b>: si la red ya no sabe nada, su explicación tiene que cambiar.</p>')}
{ex('La importancia dice que la carga es lo que más pesa; SHAP dice que en el caso de la socia fueron los atrasos. ¿Se contradicen?', '<p>No: la importancia mira al modelo con todos los socios; SHAP mira una sola decisión. Pueden y suelen ser distintos.</p>')}
{ex('Suma la explicación SHAP de la socia: 0.13 + 0.30 + 0.08 + 0.04 + 0.04 + 0.02 + 0.02 − 0.02.', '<p>0.61: su probabilidad de mora. SHAP está hecho para que el promedio más las contribuciones dé exactamente la predicción.</p>')}
{ex('Escribe en una frase la explicación que le darías a la socia.', '<p>Por ejemplo: «Lo que más pesó fueron sus dos atrasos recientes; sin ellos, su riesgo sería mucho menor. Si prefiere, podemos revisar su solicitud con un plazo más largo para que la cuota sea de unos $124, y una persona revisará la decisión».</p>')}
{colab(NB6, '<b>NB06</b>, partes 2 a 5: oclusión y Grad-CAM a mano, la prueba de cordura, la importancia y SHAP de la cooperativa ficticia y el contrafactual.')}
<p class="btnrow"><a class="btn" href="../material/Lectura_tendencia_Semana3.pdf">Leer la lectura de tendencia completa (PDF)</a></p>
"""))

# ------------------------------------------------------------------ 05 · closing
pz, sr = co['por_zona'], co['sin_rural']
S.append(('b05', 'C', '¿Le creerías a tu red?', f"""
{idea('Antes de usar un modelo con personas, cinco preguntas: ¿funciona con casos nuevos?, ¿aguanta cambios?, ¿de dónde viene lo que heredó?, ¿sus explicaciones pasan pruebas? y ¿trata a todos por igual?')}
<h3>¿Trata a todos por igual?</h3>
<p>Un buen AUC no dice si el modelo se equivoca igual con todos. En el NB06 (parte 6) miramos a la cooperativa ficticia <b>por zona</b>. En sus datos, la mora real es de {F.pct(pz['rural']['mora_real'])} en lo rural y {F.pct(pz['urbana']['mora_real'])} en lo urbano. Una <b>falsa alarma</b> es rechazar a alguien que sí habría pagado.</p>
{fig(F.zona(), 'Rechazados y falsas alarmas por zona, con y sin la columna «rural».')}
<table><tr><th></th><th>Rechazo rural</th><th>Rechazo urbano</th><th>Falsas alarmas rural</th><th>Falsas alarmas urbana</th><th>AUC</th></tr>
<tr><td><b>Con la columna «rural»</b></td><td>{F.pct(pz['rural']['rechazo'])}</td><td>{F.pct(pz['urbana']['rechazo'])}</td><td>{F.pct(pz['rural']['falsa_alarma'])}</td><td>{F.pct(pz['urbana']['falsa_alarma'])}</td><td>{co['auc']:.2f}</td></tr>
<tr><td><b>Sin la columna «rural»</b></td><td>{F.pct(sr['rural']['rechazo'])}</td><td>{F.pct(sr['urbana']['rechazo'])}</td><td>{F.pct(sr['rural']['falsa_alarma'])}</td><td>{F.pct(sr['urbana']['falsa_alarma'])}</td><td>{sr['auc']:.2f}</td></tr></table>
<p class="read"><b>Léelo así:</b> con la columna, a un socio rural lo rechazan más del doble que a uno urbano. Al quitarla, las tasas se acercan con un costo pequeño en AUC. Pero eso no resuelve la pregunta de fondo: ¿por qué la mora real es distinta? Otras columnas pueden seguir llevando parte de esa información, y decidir qué es justo no tiene una respuesta solo técnica: hay que conversarlo con quienes conocen el contexto.</p>
<h3>Cinco preguntas antes de usar un modelo con personas</h3>
<table><tr><th>Pregunta</th><th>Cómo se comprueba</th><th>Dónde lo vimos</th></tr>
<tr><td><b>1 · ¿Funciona con casos nuevos?</b></td><td>Curvas de entrenamiento y validación; examen final medido una sola vez.</td><td>NB05, partes 1, 2 y 6</td></tr>
<tr><td><b>2 · ¿Aguanta cambios?</b></td><td>Probar con datos movidos, ruidosos, adversariales y recientes.</td><td>NB05, partes 3 a 5</td></tr>
<tr><td><b>3 · ¿De dónde viene lo que heredó?</b></td><td>Saber con qué datos se entrenó el modelo base.</td><td>NB06, parte 1</td></tr>
<tr><td><b>4 · ¿Sus explicaciones pasan pruebas?</b></td><td>Prueba de cordura; comparar métodos; un contrafactual para la persona.</td><td>NB06, partes 2 a 5</td></tr>
<tr><td><b>5 · ¿Trata a todos por igual?</b></td><td>Medir rechazos y errores por grupo.</td><td>NB06, parte 6</td></tr></table>
{box('analogia', 'El mismo título del entregable de la semana 1', '<p>En la semana 1 preguntamos «¿le creerías a tu red?» mirando la exactitud y la matriz de confusión. Ahora la pregunta tiene cinco partes. Una explicación de un modelo que no generaliza termina siendo, simplemente, una explicación muy clara de un error.</p>')}
<h3>Tu proyecto de titulación</h3>
<p>Respondan en grupo ({lam('tu-proyecto3')}): ¿Cómo sabrán si su modelo memoriza? ¿Qué cambio pequeño podría tumbarlo en la vida real? ¿Partirán de un modelo preentrenado y qué saben de sus datos? ¿A quién le deberán explicar sus decisiones y qué explicación le serviría? ¿Qué grupos conviene mirar por separado?</p>
<h3>Las tres semanas en un mapa</h3>
<table><tr><th>Semana</th><th>La pregunta</th><th>Lo que aprendimos</th></tr>
<tr><td><b>1</b></td><td>¿Cómo aprende una red?</td><td>Neurona, activación, pérdida, gradiente, retropropagación y Keras.</td></tr>
<tr><td><b>2</b></td><td>¿Cómo mira y cómo lee?</td><td>Cada arquitectura es una suposición: CNN, RNN, LSTM, atención e híbridos.</td></tr>
<tr><td><b>3</b></td><td>¿Le creerías?</td><td>Generalizar, ser robusta, reutilizar lo aprendido y explicar con pruebas.</td></tr></table>
<h3>Practica</h3>
{ex('Tu modelo tiene AUC 0.80 con todos los socios. ¿Ya sabes si trata a todos por igual?', '<p>No: el AUC mezcla a todos. Hay que medir rechazos y errores <b>por grupo</b>.</p>')}
{ex('Quitar la columna «rural» acercó las tasas de rechazo. ¿Por qué no basta?', '<p>Porque la mora real sigue siendo distinta y otras columnas pueden llevar esa información. La pregunta de qué es justo necesita contexto, no solo un ajuste técnico.</p>')}
{ex('Elige una de las cinco preguntas y di cómo la comprobarías en tu proyecto.', '<p>Respuesta abierta. Por ejemplo, para la 2: evaluar el modelo con los datos del último trimestre, que nunca vio, y compararlo con su resultado en el examen final.</p>')}
"""))

# ------------------------------------------------------------------ reference
FORMULAS = r"""
<table>
<tr><th>Qué</th><th>Fórmula</th><th>En palabras</th></tr>
<tr><td>Brecha de sobreajuste</td><td>exactitud de entrenamiento − exactitud de validación</td><td>96.7 % − 83.0 % ≈ 14 puntos: memoriza</td></tr>
<tr><td>Dropout(p)</td><td>cada número se apaga con probabilidad \(p\)</td><td>Dropout(0.3): el 30 %, solo al entrenar</td></tr>
<tr><td>Early stopping</td><td>parar si la validación no mejora en <i>patience</i> épocas</td><td>mejor 71 + 8 de espera = se detiene en 79</td></tr>
<tr><td>FGSM</td><td>\(x' = x + \varepsilon\cdot\operatorname{signo}(\nabla_x\,\text{pérdida})\)</td><td>un paso cuesta arriba en cada píxel</td></tr>
<tr><td>Parámetros entrenables al congelar</td><td>\(n_{in}\cdot n_{out} + n_{out}\) de la salida nueva</td><td>800 × 4 + 4 = 3 204 de 8 004</td></tr>
<tr><td>Grad-CAM</td><td>\(\operatorname{ReLU}\big(\sum_k \alpha_k A^k\big)\), \(\alpha_k\) = promedio del gradiente</td><td>sumar los mapas pesados por su importancia</td></tr>
<tr><td>Importancia por permutación</td><td>AUC − AUC con la columna mezclada</td><td>carga: 0.125</td></tr>
<tr><td>SHAP</td><td>\(p = \text{base} + \sum_j \phi_j\)</td><td>0.13 + … = 0.61</td></tr>
<tr><td>Prueba de cordura</td><td>parecido (Spearman) entre el mapa entrenado y con pesos al azar</td><td>cerca de 0: pasa · cerca de 1: no pasa</td></tr>
</table>"""
S.append(('formulas', 'Σ', 'Fórmulas de bolsillo', FORMULAS))

GLOS = [
    ("Ajuste fino (fine-tuning)", "Descongelar la red reutilizada y seguir entrenándola con pasos pequeños para adaptarla a la tarea nueva."),
    ("Aumento de datos", "Mostrarle a la red versiones cambiadas de sus fotos (movidas, giradas…) para que no memorice detalles como la posición exacta."),
    ("AUC", "Qué tan seguido el modelo le da más riesgo a un caso positivo que a uno negativo, tomados al azar: 0.5 es adivinar, 1 es perfecto."),
    ("Búsqueda al azar", "Elegir hiperparámetros sorteando combinaciones y comparándolas en la validación."),
    ("Callback", "Un aviso que fit consulta durante el entrenamiento, como EarlyStopping."),
    ("Cambio de distribución", "Cuando los datos nuevos ya no se parecen a los de entrenamiento: el mundo cambió y el modelo no avisa."),
    ("Congelar (capas)", "Marcar capas con trainable = False para que no cambien al entrenar."),
    ("Contrafactual", "Explicación de qué tendría que cambiar para obtener otro resultado: «sin tus atrasos, te aprobarían»."),
    ("Correlación de Spearman", "Mide si dos listas ordenan las cosas igual: 1 idéntico, 0 nada que ver."),
    ("Dropout", "Capa que en cada paso de entrenamiento apaga al azar una parte de los números; al predecir no hace nada."),
    ("Early stopping", "Parar el entrenamiento cuando la validación deja de mejorar y quedarse con la mejor época."),
    ("Ejemplo adversarial", "Una entrada cambiada muy poquito, a propósito, para que la red se equivoque."),
    ("Entrenamiento adversarial", "Entrenar también con ejemplos adversariales (con su etiqueta correcta) para que la red los resista: vacunarla."),
    ("Épsilon (ε)", "En FGSM, cuánto se permite cambiar cada píxel (0.05 = 5 % del brillo máximo)."),
    ("Explicabilidad", "Poder describir por qué un modelo tomó una decisión, de forma que alguien la entienda y la pueda revisar."),
    ("Explicación post hoc", "Una explicación calculada después de entrenar, mirando al modelo desde afuera (oclusión, Grad-CAM, SHAP)."),
    ("Falsa alarma", "Rechazar a alguien que sí habría pagado (un falso positivo)."),
    ("FGSM", "Fast gradient sign method: fabricar un ejemplo adversarial con un solo paso del signo del gradiente."),
    ("Generalizar", "Que un modelo funcione bien con casos que no vio al entrenar."),
    ("Grad-CAM", "Mapa de calor que usa los gradientes de la última capa convolucional para mostrar qué zonas empujaron hacia una clase (2017)."),
    ("Gradiente × imagen", "Mapa que multiplica el gradiente de la clase por cada píxel; no pasó la prueba de cordura en el NB06."),
    ("GradientTape", "La herramienta de TensorFlow que graba las cuentas para calcular gradientes."),
    ("Hiperparámetro", "Lo que eliges antes de entrenar y la red no aprende: learning rate, filtros, dropout, épocas."),
    ("ImageNet", "Conjunto de más de un millón de fotos de 1 000 clases con el que se entrenan muchas redes que luego se reutilizan."),
    ("Importancia por permutación", "Cuánto empeora el modelo si se mezcla una columna: mide qué usa el modelo en general."),
    ("Interpretabilidad mecanicista", "Abrir la red y estudiar sus mecanismos internos, como un biólogo estudia órganos."),
    ("keras.applications", "Módulo de Keras con redes ya entrenadas (MobileNetV2, ResNet50…) listas para reutilizar."),
    ("L2 (regularización)", "Una multa en la pérdida para los pesos grandes."),
    ("LoRA", "Técnica para ajustar un modelo grande modificando solo una pequeña parte de él (2022)."),
    ("Oclusión", "Tapar partes de la foto y medir cuánto baja la probabilidad de la clase."),
    ("Patience", "En EarlyStopping, cuántas épocas sin mejora se esperan antes de parar."),
    ("Prueba de cordura", "Poner los pesos al azar y ver si la explicación cambia; si no cambia, no explicaba a la red (Adebayo y colegas, 2018)."),
    ("RandomTranslation", "Capa de Keras que mueve cada foto al azar mientras se entrena (aumento de datos)."),
    ("Regularizar", "Ponerle frenos a la memoria de la red para que generalice: aumento de datos, dropout, early stopping, L2."),
    ("Robustez", "Que el modelo siga funcionando ante cambios pequeños o inesperados en los datos."),
    ("SHAP", "Método que reparte una predicción entre los datos de entrada, como el mérito de un gol entre los jugadores (2017)."),
    ("Simulacro (validación)", "Datos que la red no usa para aprender y que sirven para parar a tiempo y elegir ajustes."),
    ("Sobreajuste", "Memorizar los ejemplos de estudio: muy bien en entrenamiento, peor con casos nuevos."),
    ("Subajuste", "No aprender ni siquiera lo de estudio: las dos curvas se quedan altas."),
    ("trainable", "Propiedad de una capa de Keras: si es False, sus pesos no cambian al entrenar."),
    ("Transfer learning", "Reutilizar lo que una red aprendió en una tarea para aprender otra, sobre todo con pocos datos."),
]
GLOS.sort(key=lambda t: _u.normalize('NFD', t[0]).encode('ascii', 'ignore').decode().lower())
S.append(('glosario', 'A–Z', 'Glosario', '<input id="search" class="search" type="search" placeholder="Buscar una palabra…" aria-label="Buscar en el glosario"><dl class="glos">' +
          ''.join(f'<div data-search><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOS) + '</dl>'))

S.append(('cierre', '✓', '¿Listo? Comprueba lo que aprendiste', """
<p>Juega el quiz final: 10 preguntas cortas, sin cuentas, 25 segundos cada una. Al terminar te dice tu puntaje, qué temas repasar (con enlace a esta guía) y tu avance frente al pre-quiz.</p>
<div class="btnrow"><a class="btn amber" href="../quiz/index.html?final">Jugar el quiz final</a><a class="btn ghost" href="../index.html">Volver al inicio</a></div>
<h3>La semana completa en un minuto</h3>
<p class="read">Que la red acierte en el examen no basta. Con pocos datos, la red se aprende de memoria los ejemplos: su pérdida de entrenamiento baja y la de validación sube. Los frenos (aumento de datos, dropout y parar a tiempo) la ayudan a quedarse con lo general, y el mejor freno es tener más datos.</p>
<p class="read">Exacto no es robusto: mover la foto unos píxeles o sumarle un ruido invisible elegido para engañarla (subir la montaña a propósito) puede tumbarla. El aumento de datos y el entrenamiento adversarial compran robustez a cambio de unos puntos, y los ajustes se eligen con el simulacro, nunca con el examen final. El riesgo más común es más silencioso: el mundo cambia y el modelo no avisa.</p>
<p class="read">Con pocos datos, reutilizar lo que otra red aprendió (congelar y ajustar) ayuda mucho, aunque heredamos lo que no conocemos. Para explicar lo que decide usamos oclusión, Grad-CAM, la importancia y SHAP, pero son interpretaciones: la prueba de cordura muestra que algunas no explican a la red. A la persona afectada le sirve un contrafactual, y antes de usar un modelo con personas hay que mirar si trata a todos por igual.</p>
<h3>Preguntas rápidas</h3>
""" + ''.join(ex(q, f'<p>{r}</p>') for q, r in [
    ('¿Cómo se ve el sobreajuste en las curvas?', 'La pérdida de entrenamiento sigue bajando y la de validación empieza a subir.'),
    ('Nombra tres frenos para la memoria.', 'Aumento de datos, dropout y early stopping (y el mejor: más datos).'),
    ('¿Qué hace el dropout al predecir?', 'Nada: solo actúa al entrenar; al predecir trabajan todas las neuronas.'),
    ('¿Qué es un ejemplo adversarial?', 'Una foto cambiada muy poquito, a propósito, en la dirección en que más sube la pérdida.'),
    ('¿Con qué datos se eligen los hiperparámetros?', 'Con la validación (el simulacro); el examen final se mide una sola vez.'),
    ('¿Cuándo ayuda más el transfer learning?', 'Cuando hay pocos datos: con 5 fotos por clase sumó unos 15 puntos.'),
    ('¿Qué es congelar una capa?', 'Ponerle trainable = False para que no cambie al entrenar.'),
    ('¿Qué mide la prueba de cordura?', 'Si el mapa cambia cuando la red ya no sabe nada (pesos al azar); si no cambia, no la explicaba.'),
    ('¿Qué diferencia hay entre la importancia y SHAP?', 'La importancia mira al modelo en general; SHAP explica una decisión.'),
    ('¿Qué explicación le sirve a la persona afectada?', 'Un contrafactual: qué tendría que cambiar para obtener otro resultado.'),
]) + """
<p>En Canvas te esperan el test de la semana, la lectura de tendencia con su encuesta y el entregable; las fechas exactas están allí.</p>
"""))

# ------------------------------------------------------------------ assemble
body, toc = '', []
for sid, n, title, inner in S:
    kick = {'inicio': chip('Empieza aquí', 'amber'), 'formulas': chip('Resumen', 'purple'), 'glosario': chip('Referencia', 'purple'),
            'cierre': chip('Autoevaluación', 'teal')}.get(sid)
    if not kick:
        kick = chip({'rec': 'Recorderis de las semanas 1 y 2', 'b01': 'Tema 1 · Generalizar', 'b02': 'Tema 1 · Robustez',
                     'b03': 'Tema 2 · Reutilizar', 'b04': 'Tema 2 · Explicar', 'b05': 'Cierre de la semana'}[sid])
        kick += chip({'b01': 'NB05', 'b02': 'NB05', 'b03': 'NB06', 'b04': 'NB06', 'b05': 'NB06'}[sid], 'gray') if sid != 'rec' else ''
    body += f'<section id="inicio">{inner}</section>' if sid == 'inicio' else section(sid, kick, title, inner)
    toc.append((sid, n, title))

html = page('Guía de estudio · Semana 3 · Deep Learning UIDE',
            'Guía de estudio de la semana 3 de Neural Networks: Deep Learning (UIDE): sobreajuste y regularización, robustez y ejemplos adversariales, hiperparámetros, transfer learning y explicabilidad.',
            toc, body, 'dl-uide-w3-guia', topbar=weeks(3, '../../guia/index.html', '../../semana2/guia/index.html', 'index.html'))
(OUT / 'guia').mkdir(parents=True, exist_ok=True)
(OUT / 'guia' / 'index.html').write_text(html)
print('guía semana 3 built', len(html) // 1024, 'KB')
