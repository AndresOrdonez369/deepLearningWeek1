"""Semana 3 · Tema 2 (reutilizar y explicar) y Cierre (¿Le creerías a tu red?).
Organized by themes, not by days: each session simply continues where the previous one stopped.
Every number comes from data/tema2.json (tools/run_tema2.py, the same code as NB06) or the reading of the week."""
import json, pathlib
from kit import slide, head, key, chip, st, demo, count, qr, notes, eq, hist, code
from slides_tema1 import section, practice, pct, miles, T1

T2 = json.loads((pathlib.Path(__file__).parent / 'data' / 'tema2.json').read_text())
TR, CO = T2['transfer'], T2['coop']
SO, V, CR = CO['socia'], CO['socia']['valores'], T2['cordura']
PZ, SR = CO['por_zona'], CO['sin_rural']
CUOTA = round(V['carga'] * V['ingreso'])                       # ≈ $144
CUOTA25 = round(CO['contrafactual_carga']['carga'] * V['ingreso'])   # ≈ $124 (carga 0.245, as NB06 prints it)

def neg(v, d=2):
    """A signed number with a real minus sign."""
    return f'{v:.{d}f}'.replace('-', '−')


G2 = 'Tema 2 · Reutilizar y explicar'
G3 = 'Cierre · ¿Le creerías a tu red?'

# ======================================================================= Tema 2 · reutilizar y explicar
section('b02', '02', 'Reutilizar y explicar', '¿Puedo aprovechar lo que otra red ya aprendió? ¿Y puedo explicar por qué decide lo que decide?',
        ['Repaso del Tema 1', 'Transfer learning', 'Congelar o ajustar', 'Pocos datos', 'En la vida real', 'Por qué explicar', 'Dónde miró', 'Prueba de cordura',
         'Explicar un crédito', 'Contrafactual', 'Por zona', 'La IA se explica', 'Las reglas', 'Práctica NB06'],
        'Tema 2 · ≈ 2 h con el NB06', G2, 'Tema 2 · Reutilizar y explicar',
        notes('<b>Tema 2.</b> Primera parte: transfer learning (<b>idea clave 4</b>). Segunda parte: explicar y verificar (<b>idea clave 5</b>), con la lectura de tendencia y la práctica NB06.',
              'Si el Tema 2 empieza en una sesión nueva, la lámina siguiente repasa el Tema 1 en tres ideas.'), shown='T2')

slide('repaso-tema1', 'El Tema 1 en tres ideas', head('El Tema 1 en tres ideas', '¿Quién explica cada una con sus palabras, antes de que aparezca?') + f"""
<div class="col" style="gap:1.1em;margin-top:.4em">
  {st(1, '<div class="mapi big"><span>1 · Memorizar</span><b>con 1 000 fotos: ' + pct(T1['sobreajuste']['train_acc'][-1]) + ' estudiando y ' + pct(T1['sobreajuste']['val_acc'][-1]) + ' en el simulacro</b></div>')}
  {st(2, '<div class="mapi big"><span>2 · Frenos</span><b>dropout, aumento y parar a tiempo; el mejor freno es tener más datos</b></div>')}
  {st(3, '<div class="mapi big"><span>3 · Robustez</span><b>ruido invisible con ε = 0.05: de ' + pct(T1['fgsm']['limpia']) + ' a ' + pct(T1['fgsm']['0.05']) + '; vacunada, ' + pct(T1['fgsm_entrenada']['0.05']) + '</b></div>')}
  {st(4, '<div class="keybar" style="margin-top:.6em"><span>Ahora dos preguntas nuevas: <b>¿y si tengo muy pocos datos?</b> y <b>¿y si me piden explicar por qué decidió?</b></span></div>')}
</div>""", notes('Cinco minutos. Úsala sobre todo si el Tema 2 empieza en una sesión nueva. Pide voluntarios por el chat para cada idea antes de mostrarla.',
                 'Si alguien no hizo el NB05 completo, recuérdale las secciones 1, 2 y 4 para casa.'),
    block='02', group=G2, minutes=5, steps=4)

slide('transfer', 'Transfer learning: no empezar de cero', head('Transfer learning: no empezar de cero', 'Una red que ya aprendió a mirar prendas le presta sus «ojos» a una tarea nueva. Solo le enseñamos la última parte.', key(4)) +
      demo('transfer', 'fill') +
      st(1, '<div class="analog" style="flex:none;margin-top:.6em"><span class="t">Contratar a un profesional con experiencia y darle una inducción corta</span><p>Aprende rápido, pero trae hábitos de trabajos anteriores que no conoces del todo (lectura de tendencia).</p></div>'),
      notes(f'<b>Idea clave 4.</b> Es la sección 1 del NB06. Paso 1: la red base es la CNN de siempre, entrenada 5 épocas con 6 prendas que <b>no son de arriba</b> (pantalón, vestido, sandalia, zapatilla, bolso, botín): {pct(T2["base_6clases"])}. Nunca vio una camiseta.',
            f'Paso 2, <b>congelar</b>: las capas convolucionales (los filtros que detectan bordes y formas) quedan fijas: 4 800 números. Le ponemos una cabeza nueva para 4 prendas de arriba (camiseta, suéter, abrigo, camisa), muy parecidas entre sí. Solo se entrenan {miles(TR["5"]["entrenables_congelada"])} números.',
            'Paso 3, <b>ajuste fino</b>: con la cabeza ya entrenada, se descongela todo y se sigue entrenando con pasos 10 veces más pequeños. La idea: ajustar un poco sus hábitos sin borrar su experiencia.',
            '<span class="q">Pregunta:</span> «¿Por qué tiene sentido que los filtros de un pantalón sirvan para una camisa?» (los bordes, las esquinas y las texturas son los mismos).'),
      block='02', group=G2, minutes=6, steps=3)

TCODE = code("""
base = keras.Sequential(convs)   # learned: 6 other garments
base.trainable = False           # freeze its experience
model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)), base,
    layers.Dense(4, activation="softmax")])   # new head
model.compile("adam", "sparse_categorical_crossentropy")
model.fit(x_few, y_few, epochs=100,
          validation_data=val, callbacks=[stop])
base.trainable = True            # fine-tuning: unfreeze
model.compile(keras.optimizers.Adam(1e-4),   # small steps
              "sparse_categorical_crossentropy")
model.fit(x_few, y_few, epochs=40,
          validation_data=val, callbacks=[stop])
""", hl='1:1-2;2:3-8;3:9-13', cls='sm')
slide('congelar', 'Congelar o ajustar', head('Congelar o ajustar, en código', 'Congelar es una línea: <code>trainable = False</code>. Ajustar es descongelar y compilar otra vez con <b>pasos pequeños</b>.', key(4)) + f"""
<div class="split" style="grid-template-columns:7fr 5fr;gap:2em;align-items:start">
  {TCODE}
  <div class="col" style="gap:1em">
    {st(1, '<div class="mapi stack" style="font-size:1.12em"><span>Congelar</span><b>usar su experiencia tal cual y enseñarle solo la última parte</b></div>')}
    {st(2, '<div class="mapi stack" style="font-size:1.12em"><span>Una cabeza nueva</span><b>Dense(4): 800 × 4 + 4 = ' + miles(TR['5']['entrenables_congelada']) + ' números para aprender</b></div>')}
    {st(3, '<div class="mapi stack" style="font-size:1.12em"><span>Ajuste fino</span><b>dejar que ajuste un poco sus hábitos, con pasos pequeños (0.0001 en vez de 0.001)</b></div>')}
    {st(3, '<p class="say">Si el paso es grande, la red <b>borra lo que sabía</b> en las primeras épocas, justo cuando hay pocos datos.</p>')}
  </div>
</div>""", notes(
    'El código de la sección 1 del NB06, simplificado (en el NB las capas se copian una por una con <code>set_weights</code>; la idea es la misma). Un clic por bloque.',
    '<code>trainable = False</code>: al entrenar, Keras no toca esos pesos. Hay que hacerlo <b>antes</b> de <code>compile</code>: si se cambia después, hay que volver a compilar.',
    f'La cabeza: el Flatten entrega 800 números; con 4 salidas son 800 × 4 + 4 = {miles(TR["5"]["entrenables_congelada"])} parámetros. Toda la red tiene {miles(TR["5"]["params"])}.',
    'Ajuste fino: se descongela y se compila otra vez con Adam(1e-4): pasos 10 veces más pequeños que el Adam por defecto (0.001).',
    '<span class="q">Pregunta:</span> «¿Por qué primero se entrena la cabeza con la base congelada, y solo después se descongela?» (al principio la cabeza es aleatoria y sus culpas grandes dañarían la base).'),
    block='02', group=G2, minutes=4, steps=3)

slide('transfer-resultado', 'Con pocos datos, la experiencia vale', head('Con pocos datos, la experiencia vale', 'Las 4 prendas de arriba con <b>5, 20 o 100 fotos por clase</b> para estudiar. Examen final: 4 000 fotos.', key(4)) +
      demo('transferbars', 'fill') +
      st(3, f'<div class="keybar" style="margin-top:.4em;flex:none"><span>La experiencia heredada ayuda <b>mucho con muy pocos datos</b> (+15 puntos con 5 fotos por clase) y <b>casi nada con suficientes</b>: con 100, desde cero ya empata.</span></div>'),
      notes(f'Resultados reales de la sección 1 del NB06. Paso 1: con 5 fotos por clase (20 en total): desde cero {pct(TR["5"]["desde_cero"])}, congelada {pct(TR["5"]["congelada"])}, ajuste fino {pct(TR["5"]["ajuste_fino"])}.',
            f'Paso 2: con 20 por clase: {pct(TR["20"]["desde_cero"])}, {pct(TR["20"]["congelada"])} y {pct(TR["20"]["ajuste_fino"])}. Paso 3: con 100 por clase: {pct(TR["100"]["desde_cero"])}, {pct(TR["100"]["congelada"])} y {pct(TR["100"]["ajuste_fino"])}. Desde cero empata o gana.',
            'Lección honesta: aquí la red base aprendió con 36 000 fotos pequeñas en gris. En la vida real la red base aprendió con millones de fotos y la ventaja es mucho mayor (siguiente lámina).',
            'Por qué todos quedan lejos del 100 %: camiseta, suéter, abrigo y camisa se parecen mucho incluso para una persona. Es la tarea más difícil de Fashion-MNIST.',
            '<span class="q">Pregunta:</span> «¿Cuántos ejemplos etiquetados tiene su proyecto? ¿Les conviene partir de una red ya entrenada?»'),
      block='02', group=G2, minutes=6, steps=3)

VR = [('Las redes ya entrenadas', '<code>keras.applications</code> trae CNN entrenadas con <b>ImageNet</b>, más de un millón de fotos en 1 000 clases: MobileNetV2, ResNet50…'),
      ('Para textos', 'Se parte de un modelo de lenguaje ya entrenado. Con <b>LoRA</b> se ajusta solo una pequeña parte de él (Hu et al., 2022).'),
      ('La herencia', 'Ahorra datos, cómputo y tiempo, pero puede traer <b>sesgos o puntos ciegos</b> de datos que nunca vimos.')]
VCODE = code("""
base = keras.applications.MobileNetV2(
    weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base.trainable = False                  # the same two ideas
""", cls='sm')
slide('transfer-vida-real', 'Transfer learning en la vida real', head('En la vida real: redes que ya vieron millones', 'Pocas organizaciones entrenan desde cero: parten de un modelo que entrenó otra empresa y lo ajustan.') +
      '<div class="three9">' + ''.join(st(i + 1, f'<div class="c9 mi"><h3>{t}</h3><p>{d}</p></div>') for i, (t, d) in enumerate(VR)) + '</div>' +
      st(1, f'<div style="margin-top:1em">{VCODE}</div>') +
      st(4, '<div class="trendbar" style="margin-top:1em">' + chip('Debate de la lectura', 'trend') + '<span><b>Reutilizar o entender:</b> el transfer learning ahorra recursos, pero heredamos lo que no podemos auditar. ¿Dónde está el límite?</span></div>'),
      notes('Paso 1: el mismo código, con una red de verdad. MobileNetV2 se entrenó con ImageNet; <code>include_top=False</code> quita su cabeza de 1 000 clases para ponerle la tuya. Las fotos deben ser a color y de 224 × 224.',
            'Paso 2: en texto pasa lo mismo, y más. LoRA (Hu et al., 2022) congela el modelo y le agrega matrices pequeñas que sí se entrenan. Así una organización pequeña puede ajustar un modelo enorme a sus documentos.',
            'Paso 3: la herencia. Si una red aprendió con fotos de otro país o de otra época, puede traer sus puntos ciegos. «Trae hábitos de trabajos anteriores que no conoces del todo».',
            'Paso 4: el debate de la lectura. Abre el chat 2 minutos: ¿usarían un modelo preentrenado sin saber con qué datos se entrenó para decidir créditos?'),
      block='02', group=G2, minutes=4, steps=4)

SOC = [('Ingreso', f'${round(V["ingreso"])} al mes'), ('Cuota', f'≈ ${CUOTA} ({round(V["carga"] * 100)} % del ingreso)'), ('Antigüedad', f'{round(V["antiguedad"])} mes como socia'),
       ('Atrasos', f'{round(V["atrasos"])} en los últimos 12 meses'), ('Garante', 'no tiene'), ('Ahorro', f'{V["ahorro"]:.1f} meses de ingreso'), ('Zona', 'rural')]
slide('por-que-explicar', '¿Por qué dijo «no»?', head('¿Por qué dijo «no»?', 'Una cooperativa usa una red para decidir créditos. Una socia recibe un «no» y pregunta, con todo derecho: ¿por qué? <b>(Datos ficticios.)</b>') + f"""
<div class="split" style="grid-template-columns:5fr 7fr;gap:2.2em;align-items:start">
  <div class="col" style="gap:.8em">
    {st(1, '<div class="socia">' + ''.join(f'<span>{a}</span><b>{b}</b>' for a, b in SOC) + f'<p class="res">Probabilidad de mora: <b class="num" style="color:var(--coral)">{round(SO["prob"] * 100)} %</b> → rechazada</p></div>')}
  </div>
  <div class="col" style="gap:1em">
    {st(2, '<div class="trendbar">' + chip('Ecuador · marzo de 2026', 'trend') + '<span>Una norma permite a las personas afectadas por decisiones automatizadas pedir <b>«una explicación sobre la lógica aplicada por el algoritmo»</b> (Lexis, 2026).</span></div>')}
    {st(3, '<div class="rcp2"><div class="c9 az"><h3>El científico de datos</h3><p>necesita saber si el modelo es <b>correcto</b>: ¿mira lo que debe?</p></div><div class="c9 am"><h3>La persona afectada</h3><p>necesita saber <b>qué puede hacer</b>: ¿qué tendría que cambiar?</p></div></div>')}
    {st(3, '<p class="say">Rara vez la misma explicación sirve para los dos. En este tema vemos herramientas para cada uno.</p>')}
  </div>
</div>""", notes(
    f'El caso de la lectura de tendencia, con números de la sección 4 del NB06. La cooperativa y la socia son <b>ficticias</b>: 6 000 socios inventados con 7 datos cada uno; el {pct(CO["tasa_mora"])} cae en mora. La red densa (16-8-1) tiene AUC {CO["auc"]:.2f}.',
    f'Paso 1: la socia. Ingreso ${round(V["ingreso"])}, cuota de unos ${CUOTA}, 1 mes de antigüedad, 2 atrasos, sin garante, 1.5 meses de ahorro, zona rural. La red le da {round(SO["prob"] * 100)} % de probabilidad de mora: con el umbral de 50 %, rechazada.',
    'Paso 2: la norma de la Superintendencia de Protección de Datos Personales (marzo de 2026): evaluaciones de impacto, revisión humana de decisiones automatizadas con efectos jurídicos y derecho a pedir una explicación de la lógica del algoritmo.',
    'Paso 3: los dos destinatarios. Primero miramos herramientas para el científico de datos (dónde miró la red, la prueba de cordura, SHAP); después, la explicación que le sirve a la socia (el contrafactual).',
    '<span class="q">Pregunta:</span> «Si fueran la socia, ¿qué respuesta les dejaría tranquilos?»'),
    block='02', group=G2, minutes=5, steps=3)

slide('donde-miro', '¿Dónde miró la red?', head('¿Dónde miró la red?', f'La CNN de 10 prendas ({pct(T2["cnn10"])}) y tres maneras de preguntarle qué zona de la foto influyó. Cambia de prenda y de método.', key(5)) +
      demo('mapas', 'fill') +
      st(3, '<div class="warnbar" style="margin-top:.5em;flex:none"><span>Son <b>interpretaciones</b> del modelo, no el modelo. Como toda interpretación, pueden equivocarse: hay que ponerlas a prueba.</span></div>'),
      notes('<b>Idea clave 5 (parte 1).</b> Mapas reales de la sección 2 del NB06. Paso 1, <b>oclusión</b>: tapar con la mano. Un cuadro negro de 6 × 6 recorre la foto (de 2 en 2 píxeles) y en cada lugar medimos cuánto baja la probabilidad del botín. Es lento pero muy fácil de entender.',
            'Paso 2, <b>Grad-CAM</b> (Selvaraju et al., 2017): usa los gradientes de la última capa convolucional (de 11 × 11) para pintar un mapa de calor. Es rápido: una sola pasada hacia atrás. La lectura: si el modelo dice «neumonía», el mapa debería iluminar el pulmón, no una etiqueta del hospital en la esquina.',
            'Paso 3, <b>gradiente × imagen</b>: cuánto cambia la respuesta si se mueve cada píxel, multiplicado por el brillo. Fíjense: se parece muchísimo a la foto. ¿Explica a la red o solo dibuja la prenda? Lo comprobamos en la lámina siguiente.',
            'Cambien a la camisa (77 %) y al bolso (99 %): ¿miran lo que una persona miraría?',
            '<span class="q">Pregunta:</span> «Si el mapa de una radiografía se encendiera en la esquina donde está el nombre del hospital, ¿qué concluirían?» (la red aprendió un atajo, no la enfermedad).'),
      block='02', group=G2, minutes=7, steps=3)

slide('cordura', 'La prueba de cordura', head('La prueba de cordura', 'Con pesos al azar la red no sabe nada: si el mapa casi no cambia, <b>no la explicaba</b>.', key(5)) +
      demo('cordura', 'fill', at='El traductor que sigue el tono, no las palabras', ap='Aunque cambies el discurso, dice frases parecidas. Suena convincente, pero no traduce.') +
      st(3, f'<div class="keybar" style="margin-top:.5em;flex:none"><span>Una explicación también tiene que <b>pasar pruebas</b>. La oclusión también pasa ({neg(CR["oclusion"])}).</span></div>'),
      notes('<b>Idea clave 5 (parte 2).</b> Sección 3 del NB06. La propuso un grupo de Google Brain (Adebayo et al., 2018). Paso 1: los mapas de la red entrenada, para el botín.',
            'Paso 2: la misma arquitectura con pesos al azar: una red que no sabe nada. El Grad-CAM cambia por completo. El gradiente × imagen sigue casi igual: sigue dibujando la forma del botín, como un filtro de fotografía.',
            f'Paso 3: la correlación entre los dos mapas, promediada en 30 fotos (1 = idénticos, 0 = nada que ver): Grad-CAM {neg(CR["gradcam"])} (pasa), oclusión {neg(CR["oclusion"])} (pasa), gradiente × imagen <b>{neg(CR["gradx"])}</b> (no pasa). Es lo mismo que encontraron Adebayo et al.',
            'La lección no es tirar las herramientas: es verificarlas. Si un método da el mismo mapa para una red entrenada y para una al azar, no te dice nada sobre lo que aprendió.',
            'Punto de corte posible: si la sesión termina aquí, la siguiente empieza en «Explicar un crédito».'),
      block='02', group=G2, minutes=6, steps=3)

slide('explicar-credito', 'Explicar un «no»: lo general y lo de ella', head('Explicar un «no»', 'La <b>importancia por permutación</b> mira a todos los socios; <b>SHAP</b> explica una sola decisión: la de ella.', key(5)) +
      demo('credito', 'fill') +
      st(3, '<div class="keybar" style="margin-top:.5em;flex:none"><span>Lo que más importa <b>en general</b> (la carga de la cuota) no es lo que más pesó <b>en su caso</b> (sus 2 atrasos).</span></div>'),
      notes(f'Sección 4 del NB06. Paso 1, <b>importancia por permutación</b>: mezclamos una columna al azar (rompemos su relación con la mora) y medimos cuánto baja el AUC. Si baja mucho, la red la usaba. La carga de la cuota: {CO["importancia"]["carga"]:.3f}; atrasos {CO["importancia"]["atrasos"]:.3f}; garante {CO["importancia"]["garante"]:.3f}. La zona rural y el ingreso casi nada.',
            f'Paso 2, <b>SHAP</b> para la socia: parte del promedio de todos ({SO["base"]:.2f}) y reparte la diferencia hasta su {SO["prob"]:.2f}. Sus 2 atrasos suman <b>+{SO["shap"]["atrasos"]:.2f}</b>; ser rural, +{SO["shap"]["rural"]:.2f}; no tener garante, +{SO["shap"]["garante"]:.2f}; su poca antigüedad, +{SO["shap"]["antiguedad"]:.2f}. SHAP es como repartir el mérito de un gol entre los jugadores de la jugada (Lundberg y Lee, 2017). Su carga resta un poco (−{abs(SO["shap"]["carga"]):.2f}): es algo menor que la de muchos socios.',
            'Paso 3: el contraste. Las dos son verdad: en general, la carga es lo que más usa la red; en el caso de ella, lo que la empujó fueron los atrasos. Por eso una explicación general no sirve para responderle a una persona.',
            'SHAP con <code>KernelExplainer</code>: prueba muchas combinaciones de «tener o no tener» cada dato (reemplazándolo por valores de otros socios) y reparte el resultado de forma justa. Es lento, pero funciona con cualquier modelo.',
            '<span class="q">Pregunta:</span> «La zona rural sumó +0.08 a su probabilidad. ¿Es justo que eso pese?» Guárdenla: la respondemos en dos láminas.'),
      block='02', group=G2, minutes=7, steps=3)

slide('contrafactual', 'Lo que le sirve a la socia', head('Lo que le sirve a la socia: ¿qué tendría que cambiar?', 'Un <b>contrafactual</b> no reparte culpas: busca el cambio más pequeño que haría cambiar la decisión. Prueba los botones.', key(5)) +
      demo('contra', 'fill') +
      st(2, f'<div class="keybar" style="margin-top:.5em;flex:none"><span>Dos respuestas que ella puede usar: <b>sin los 2 atrasos</b>, {round(CO["sin_atrasos_prob"] * 100)} %; o una cuota de unos <b>${CUOTA25}</b> (unos ${CUOTA - CUOTA25} menos al mes, con un plazo más largo), {round(CO["contrafactual_carga"]["prob"] * 100)} %. Las dos la aprueban.</span></div>'),
      notes(f'Sección 5 del NB06. Paso 1: si no tuviera los 2 atrasos, su probabilidad bajaría a {round(CO["sin_atrasos_prob"] * 100)} %. Pero el pasado no se cambia: le sirve para el futuro («paga a tiempo los próximos meses»).',
            f'Paso 2: lo que sí está en sus manos: una cuota de unos ${CUOTA25} en vez de ${CUOTA} (unos ${CUOTA - CUOTA25} menos al mes), por ejemplo con un plazo más largo. Su probabilidad baja a {round(CO["contrafactual_carga"]["prob"] * 100)} % y queda aprobada.',
            '<b>Ojo, para no confundir:</b> los tres botones son cálculos reales de la red del NB06. Los controles interpolan entre esos tres puntos para que se vea la tendencia: son ilustrativos, no la red misma.',
            'Es la explicación para el segundo destinatario: no le interesa la contribución de cada variable, sino qué puede hacer. Ojo con los contrafactuales imposibles («si fuera urbana…»): no le sirven y pueden ser discriminatorios.',
            '<span class="q">Pregunta:</span> «¿Qué contrafactual le darían ustedes, y cuál nunca le darían?»'),
      block='02', group=G2, minutes=6, steps=2)

slide('por-zona', '¿Trata a todos por igual?', head('¿Trata a todos por igual?', f'Los mismos 1 200 socios de prueba, separados por zona: {PZ["rural"]["n"]} rurales y {PZ["urbana"]["n"]} urbanos.', key(5)) +
      demo('zona', 'fill') +
      st(3, f'<div class="keybar" style="margin-top:.5em;flex:none"><span>Quitar la columna acerca las tasas con un costo pequeño (AUC {CO["auc"]:.2f} → {SR["auc"]:.2f}), pero no responde la pregunta de fondo: <b>¿por qué la mora real es distinta?</b> No hay una respuesta solo técnica.</span></div>'),
      notes(f'Sección 6 del NB06. Paso 1: la mora real es distinta: {pct(PZ["rural"]["mora_real"])} en zona rural y {pct(PZ["urbana"]["mora_real"])} en la urbana (en estos datos ficticios).',
            f'Paso 2: la red con la columna «rural» rechaza al {pct(PZ["rural"]["rechazo"])} de los rurales y al {pct(PZ["urbana"]["rechazo"])} de los urbanos. Falsas alarmas (rechazados que sí habrían pagado): {pct(PZ["rural"]["falsa_alarma"])} contra {pct(PZ["urbana"]["falsa_alarma"])}.',
            f'Paso 3: la misma red sin la columna: rechazo {pct(SR["rural"]["rechazo"])} contra {pct(SR["urbana"]["rechazo"])}; falsas alarmas {pct(SR["rural"]["falsa_alarma"])} contra {pct(SR["urbana"]["falsa_alarma"])}. El AUC casi no cambia. Ahora las falsas alarmas caen más en los urbanos.',
            'No hay una métrica de «justo» que sirva para todo: igualar el rechazo, igualar las falsas alarmas o usar la mejor predicción posible son metas distintas y a veces incompatibles. Y otras columnas pueden llevar parte de la información de la zona. Es una decisión de la cooperativa, con su comité y con la ley, no solo del científico de datos.',
            '<span class="q">Pregunta:</span> «Si fueran el comité de la cooperativa, ¿qué versión usarían y por qué?»'),
      block='02', group=G2, minutes=7, steps=3)

IA = [('Mirar adentro', 'Ante «¿cuál es la capital del estado donde está Dallas?», un modelo de Anthropic representaba <b>Texas</b> por dentro antes de decir <b>Austin</b>. Pero el método dio una comprensión satisfactoria en cerca de <b>una cuarta parte</b> de los casos.', 'Lindsey et al., 2025'),
      ('La explicación que suena bien', 'Al preguntarle cómo sumó <b>36 + 59</b>, respondió con el método escolar de «llevar uno». Por dentro hacía otra cosa: una estimación aproximada más el cálculo preciso de la última cifra.', 'Lindsey et al., 2025'),
      ('La cadena de pensamiento', 'Con una pista escondida en la pregunta, la mencionaron solo el <b>25 %</b> (Claude 3.7 Sonnet) y el <b>39 %</b> (DeepSeek R1) de las veces que la usaron. Leer ese razonamiento es una oportunidad valiosa, pero «frágil».', 'Anthropic, 2025 · Korbak et al., 2025')]
slide('ia-se-explica', '¿Y si le preguntamos a la propia IA?', head('¿Y si le preguntamos a la propia IA?', 'Un modelo de lenguaje puede explicar su respuesta con palabras. Pero esa explicación también es texto generado: no necesariamente describe lo que pasó adentro.', chip('Lectura de tendencia', 'trend')) +
      '<div class="three9">' + ''.join(st(i + 1, f'<div class="c9 li"><h3>{t}</h3><p>{d}</p><span class="src">{s}</span></div>') for i, (t, d, s) in enumerate(IA)) + '</div>' +
      st(4, '<div class="analog" style="margin-top:1.1em"><span class="t">Como preguntarle a alguien por qué eligió una camisa</span><p>Te dará una razón coherente, pero no siempre la que realmente influyó.</p></div>'),
      notes('La parte de la lectura sobre interpretabilidad mecanicista: abrir la red como un biólogo que estudia los órganos. Paso 1: Dallas → Texas → Austin. Si los investigadores reemplazaban la representación de Texas por la de otro estado, la respuesta cambiaba a la capital de ese otro estado. Fascinante, pero los propios autores advierten que entender un modelo grande por dentro sigue siendo un problema abierto.',
            'Paso 2: 36 + 59. La explicación sonaba razonable, pero no era la verdadera. Es la prueba de cordura en versión lenguaje.',
            'Paso 3: Anthropic (2025) dio a los modelos una pista con la respuesta correcta. Cuando la usaron, Claude 3.7 Sonnet lo dijo en su razonamiento el 25 % de las veces y DeepSeek R1 el 39 %. Korbak et al. (2025), 41 investigadores de varios laboratorios: leer la cadena de pensamiento es una oportunidad «frágil» para supervisar.',
            '<span class="q">Pregunta:</span> «Si un chatbot les explica por qué les negó algo, ¿le creerían?»'),
      block='02', group=G2, minutes=6, steps=4)

RULES = [('diciembre de 2024', 'Brasil', 'El Senado aprobó el proyecto de ley 2338/2023, que clasifica los sistemas de IA según su riesgo. En octubre de 2026 seguía pendiente en la Cámara de Diputados.', 'Bairo Gonzalez, 2026'),
         ('marzo de 2026', 'Ecuador', 'Norma para el uso de IA: evaluaciones de impacto, revisión humana de decisiones automatizadas y derecho a pedir una explicación de la lógica del algoritmo.', 'Lexis, 2026'),
         ('julio de 2026', 'Unión Europea', 'El «Digital Omnibus» aplazó las obligaciones para la IA de alto riesgo del AI Act: del 2 de agosto de 2026 al 2 de diciembre de 2027.', 'Orrick, 2026'),
         ('octubre de 2026', 'Ecuador', 'La Asamblea Nacional tramitaba 12 proyectos de ley sobre IA; uno propone una ley orgánica de gobernanza con derecho a recibir explicaciones.', 'El Diario, 2026')]
slide('reglas', 'Tendencia: llegan las reglas', head('Tendencia: llegan las reglas', 'Quien use IA para decidir sobre personas deberá <b>explicar, documentar y permitir la revisión humana</b>. Lo que no está claro es si sabemos hacerlo bien.', chip('Lectura de tendencia', 'trend')) +
      '<div class="tl4" style="margin-top:.4em">' + ''.join(st(i + 1, f'<div class="ev"><span class="y num">{y}</span><i></i><span class="m">{w}</span><span class="d">{d}</span><span class="src">{s}</span></div>') for i, (y, w, d, s) in enumerate(RULES)) + '</div>' +
      '<div class="split even" style="gap:1.3em;margin-top:1.3em;flex:none;align-items:stretch">' +
      st(5, '<div class="trendbar">' + chip('Debate', 'trend') + '<span><b>Interpretable o explicado.</b> Rudin (2019): en decisiones de alto impacto, usar modelos interpretables por diseño. ¿Cuánta exactitud sacrificarías por entender?</span></div>') +
      st(5, '<div class="trendbar">' + chip('Debate', 'trend') + '<span><b>Regular ahora o esperar.</b> Si la ciencia de explicar todavía es inmadura, ¿explicar puede volverse un trámite sin contenido?</span></div>') + '</div>',
      notes('La tendencia de la semana, con las fechas tal como las cita la lectura. Pasos 1 a 4: Brasil, Ecuador, la Unión Europea y otra vez Ecuador.',
            'Lo que muestra el aplazamiento europeo: el bloque con la regulación más ambiciosa necesitó más de un año extra. Convertir «transparencia» en requisitos técnicos verificables es difícil.',
            'Paso 5: dos debates de la lectura. Ábrelos en el chat 3 minutos. Rudin (2019) es polémica a propósito: dice que en decisiones de alto impacto no hay que explicar cajas negras, sino usar modelos que se entienden solos. Otros responden que los modelos profundos son más exactos.',
            'Conexión con lo que vimos: con la norma de Ecuador, a la socia hay que poder explicarle la lógica. SHAP es un buen comienzo, pero ¿pasaría una prueba de cordura? ¿Le sirve a ella? ¿Sabemos qué datos formaron el modelo?'),
      block='02', group=G2, minutes=6, steps=5)

practice('practica-nb06', 'Práctica en clase: NB06', 'En parejas. Todo el código ya viene escrito. Antes de cada celda, apuesta qué va a salir: en la sección 3 casi todos se equivocan.',
         [f'<b>1</b> · Con 5 fotos por clase: desde cero <b>{pct(TR["5"]["desde_cero"])}</b>, congelada <b>{pct(TR["5"]["congelada"])}</b>, ajuste fino <b>{pct(TR["5"]["ajuste_fino"])}</b>',
          '<b>2</b> · ¿Dónde miró? Los mapas de oclusión y Grad-CAM del botín, la camisa y el bolso',
          f'<b>3</b> · Cordura: Grad-CAM <b>{neg(CR["gradcam"])}</b> (pasa), gradiente × imagen <b>{neg(CR["gradx"])}</b> (no pasa)',
          f'<b>4</b> · La socia: <b>{round(SO["prob"] * 100)} %</b>; SHAP: atrasos <b>+{SO["shap"]["atrasos"]:.2f}</b>; en general, la carga (<b>{CO["importancia"]["carga"]:.3f}</b>)',
          f'<b>5</b> · Contrafactual: sin atrasos <b>{round(CO["sin_atrasos_prob"] * 100)} %</b>; cuota de ${CUOTA25} → <b>{round(CO["contrafactual_carga"]["prob"] * 100)} %</b>',
          f'<b>6</b> · Por zona: rechazo rural <b>{pct(PZ["rural"]["rechazo"])}</b> y urbano <b>{pct(PZ["urbana"]["rechazo"])}</b>; sin la columna, <b>{pct(SR["rural"]["rechazo"])}</b> y <b>{pct(SR["urbana"]["rechazo"])}</b>'], 'nb06', 40, G2, '02',
         notes('Dinámica: 30 minutos en parejas y 10 de puesta en común. Sin nota.',
               'Prioridad: <b>1, 2, 3 y 4</b>. Las secciones 5 y 6 ya las discutimos en las láminas: pueden quedar para casa.',
               'En la sección 3 pide que apuesten antes de ejecutar: casi todos esperan que los tres mapas cambien con pesos al azar. El gradiente × imagen casi no cambia: es la mejor sorpresa del notebook.',
               'SHAP se instala solo si falta (<code>%pip install -q shap</code>, unos segundos). Al final hay <b>ejercicios</b> que se responden leyendo los resultados, con la respuesta plegada.'))

slide('cierre-tema2', 'Lo que te llevas del Tema 2', head('Lo que te llevas del Tema 2') + f"""
<div class="col" style="gap:1.1em">
  {st(1, '<div class="mapi big"><span>4 · Transfer</span><b>congelar y ajustar: la experiencia heredada vale mucho cuando hay pocos datos</b></div>')}
  {st(2, '<div class="mapi big"><span>5 · Explicar</span><b>oclusión, Grad-CAM y SHAP son interpretaciones: dicen dónde miró o qué pesó</b></div>')}
  {st(3, '<div class="mapi big"><span>5 · Verificar</span><b>una explicación también tiene que pasar pruebas, y servirle a quien la recibe</b></div>')}
  {st(4, '<p class="say" style="margin-top:.4em"><b>En el cierre:</b> juntamos los dos temas en una sola pregunta, la misma del entregable de la semana 1: <b>¿le creerías a tu red?</b></p>')}
</div>""", notes(
    'Cierre del Tema 2, 5 minutos. Pide que alguien diga cada idea con sus palabras antes de mostrarla.',
    'En el chat, del 1 al 5: <b>¿podrías explicarle a un colega qué es una prueba de cordura?</b> Anota el promedio.',
    'Si aquí termina la sesión: <b>«Finalizar reunión para todos»</b>. Si queda tiempo, sigue con el cierre de la semana.'),
    block='02', group=G2, minutes=5)

# ======================================================================= cierre · ¿le creerías a tu red?
section('b03', '03', '¿Le creerías a tu red?', 'El mismo título del entregable de la semana 1. Ahora tenemos más preguntas para hacerle a un modelo antes de confiar en él.',
        ['Cinco preguntas', 'Tu proyecto', 'Quiz final', 'Las 3 semanas', 'Lo que viene'], 'Cierre · ≈ 40 minutos con la actividad y el quiz final', G3, 'Cierre · ¿Le creerías a tu red?',
        notes('<b>Cierre de la semana y del curso en vivo.</b> Juntamos los dos temas en una lista de preguntas y la aplicamos al proyecto de titulación de cada grupo.'), shown='✓')

CHK = [('1', '¿Generaliza?', '¿Lo medí con datos que no vio, y miré el examen final <b>una sola vez</b>?', 'Tema 1 · idea 1'),
       ('2', '¿Aguanta cambios?', 'Fotos movidas, ruido, otra sucursal, otra época: ¿qué pasa si el mundo cambia un poco?', 'Tema 1 · idea 3'),
       ('3', '¿De dónde viene lo que sabe?', 'Si partí de una red ya entrenada, ¿sé con qué datos se formó?', 'Tema 2 · idea 4'),
       ('4', '¿La explicación pasa pruebas?', '¿Cambia si borro lo aprendido (prueba de cordura)? ¿Mira lo que debe?', 'Tema 2 · idea 5'),
       ('5', '¿Trata a todos por igual y le sirve a la persona?', '¿Cómo le va a cada grupo? ¿Puedo decirle a alguien qué tendría que cambiar?', 'Tema 2 · idea 5')]
slide('checklist', 'Cinco preguntas antes de confiar', head('Cinco preguntas antes de usar un modelo con personas', 'La lista de la semana. Cada pregunta viene de una de las ideas clave.') +
      '<ol class="steps-list" style="gap:1em;margin-top:.3em">' + ''.join(st(i + 1, f'<span class="k key">{n}</span><span><b>{t}</b> <span style="color:var(--ink-3);font-size:.8em">· {s}</span><br>{d}</span>', 'li') for i, (n, t, d, s) in enumerate(CHK)) + '</ol>' +
      st(6, '<div class="keybar" style="margin-top:1.1em"><span>Si alguna respuesta es «no sé», <b>todavía no le creas</b>. La exactitud es solo la primera pregunta.</span></div>'),
      notes('La lista resume la semana. Un clic por pregunta; antes de cada clic, pide un ejemplo de algo que vimos (la curva del simulacro, los 4 píxeles, la red que nunca vio camisetas, el gradiente × imagen que no pasa, la socia).',
            'Conecta con la semana 1: el entregable «¿Le creerías a tu red?» pedía línea base, comparación justa y métricas más allá de la exactitud. Ahora la lista es más larga.',
            'Cierre de la lectura: hace pocos años la pregunta era «¿qué tan exacto es mi modelo?». Ahora se suman otras dos: ¿por qué decide lo que decide? y ¿seguirá funcionando cuando el mundo cambie?',
            '<span class="q">Pregunta:</span> «¿Cuál de las cinco es la más difícil de responder en su proyecto?»'),
      block='03', group=G3, minutes=5, steps=6)

ACT = [('1 · Memorizar', '¿Qué será su simulacro y qué su examen final? ¿Cuántos ejemplos tienen?'),
       ('2 · Robustez', '¿Qué cambio pequeño del mundo real podría tumbar a su modelo?'),
       ('3 · Transfer', '¿Partirían de una red ya entrenada? ¿Cuál, y qué saben de sus datos?'),
       ('4 · Explicar', '¿A quién le explicarían una decisión, y cómo comprobarían que la explicación es fiel?')]
slide('tu-proyecto3', 'Tu proyecto: ¿le creerías?', head('Actividad: ¿le creerías a la red de tu proyecto?', 'En salas, con tu grupo de titulación. Al final, cada grupo pega <b>4 líneas</b> en el chat, una por pregunta.', chip('15 minutos en salas', 'ok') + chip('5 de puesta en común', 'hint')) +
      '<div class="act4">' + ''.join(st(i + 1, f'<div class="case"><span class="chip">{a}</span><p>{b}</p></div>') for i, (a, b) in enumerate(ACT)) + '</div>' +
      st(4, '<p class="say" style="margin-top:1em">Ejemplo: «Radiografías de un hospital: simulacro con pacientes de otro mes y examen con otro hospital · cambio: otra máquina de rayos X · partir de una CNN entrenada con ImageNet · Grad-CAM para el médico, verificado con una prueba de cordura».</p>'),
      notes('Abre salas de 3 o 4 personas (los grupos de titulación). 15 minutos.',
            'Pasa por las salas: la pregunta más difícil suele ser la 2 (imaginar cómo cambia el mundo). Ayuda preguntar: «¿qué es distinto entre los datos que tienen y el lugar donde se usaría?».',
            'Puesta en común: lee dos o tres respuestas del chat. Corrige con cariño los simulacros que en realidad son el examen final y las explicaciones que nadie verificó.',
            'Esto alimenta la entrega de la semana aplicada al proyecto y la entrega final.'),
      block='03', group=G3, minutes=20)

slide('quizfinal3', 'Quiz final: ¿cuánto avanzamos?', head('Quiz final: ¿cuánto avanzamos?', '10 preguntas tipo Kahoot. Vuelven las 5 ideas clave del pre-quiz: así vemos tu avance.', chip('No es nota', 'ok')) + f"""
<div class="split top" style="grid-template-columns:7fr 4fr;margin-top:1em">
  <ol class="steps-list" style="gap:1.2em">
    <li><span class="k">1</span><span>Abre <b>deeplearningweek1.vercel.app/?final3</b></span></li>
    <li><span class="k">2</span><span>Usa <b>el mismo nombre</b> que en el pre-quiz del inicio de la semana</span></li>
    <li><span class="k">3</span><span>Pega tu código en el chat de Teams</span></li>
  </ol>
  <div class="center">{qr('final3')}</div>
</div>""", notes(
    'Ocho minutos. El mismo nombre que en el pre-quiz: el panel de resultados de la semana 3 los empareja por nombre.',
    'Después de clase, copia el chat en <b>Resultados_quiz.html</b> de la semana 3 y verás el avance en cada idea clave.'),
    block='03', group=G3, minutes=8)

WM = [('Semana 1', 'una neurona: pesos, suma y activación', 'az'), ('Semana 1', 'la pérdida y el gradiente: bajar la montaña', 'az'), ('Semana 1', 'la retropropagación y Keras', 'az'), ('Semana 1', 'métricas: el 87 % que no vale nada', 'az'),
      ('Semana 2', 'cada arquitectura es una suposición', 'mi'), ('Semana 2', 'la CNN: una lupa que recorre la foto', 'mi'), ('Semana 2', 'la RNN: una libreta que se olvida', 'mi'), ('Semana 2', 'la atención: mirar directo, a un precio', 'mi'),
      ('Semana 3', 'aprender no es memorizar: frenos y más datos', 'am'), ('Semana 3', 'exacto no es robusto: 4 píxeles y un ruido', 'am'), ('Semana 3', 'transfer learning: heredar experiencia', 'am'), ('Semana 3', 'explicar y verificar: la prueba de cordura', 'am')]
slide('mapa-curso', 'Las 3 semanas en un mapa', head('Las 3 semanas en un mapa', 'Cómo aprende una red, qué forma darle y cuándo creerle.') +
      '<div class="wmap">' + ''.join(st(i // 4 + 1, f'<div class="wm {k}"><span>{a}</span><b>{b}</b></div>') for i, (a, b, k) in enumerate(WM)) + '</div>',
      notes('Recorre el camino en voz alta, fila por fila. La semana 1: cómo aprende. La semana 2: qué forma darle según los datos. La semana 3: cuándo creerle.',
            'Si alguien quiere repasar, cada semana tiene su guía de estudio en la misma página web, con el selector de semanas arriba.'),
      block='03', group=G3, minutes=2, steps=3)

NEXT = [('Semana 4 · sin clase en vivo', 'Es la semana de cierre: no hay sesiones por Teams. Todo se entrega en Canvas.'),
        ('Video de conclusiones', 'El docente publica un video corto con lo que respondieron en la encuesta de la lectura de esta semana.'),
        ('Entrega final grupal', 'El proyecto de los grupos de titulación (20 % de la nota). Usen las cinco preguntas del cierre como lista de control.')]
slide('lo-que-viene3', 'Lo que viene: el cierre del curso', head('Lo que viene: el cierre del curso', 'Las fechas exactas están en Canvas.', chip('Semana 4', 'trend')) +
      '<div class="cases" style="margin-top:.4em">' + ''.join(st(i + 1, f'<div class="case"><span class="chip">{a}</span><p>{b}</p></div>') for i, (a, b) in enumerate(NEXT)) + '</div>',
      notes('La semana 4 no tiene clase en vivo: es el cierre del curso (video de conclusiones de la tendencia de la semana 3, calificación de la semana 3 y entrega final grupal, que vale el 20 % de la nota).',
            'Recuerda responder la encuesta de la lectura de tendencia: sus respuestas son el insumo del video de conclusiones.',
            '<span class="q">Pregunta para cerrar:</span> «De las cinco preguntas, ¿cuál van a responder primero en su entrega final?»'),
      block='03', group=G3, minutes=3)

slide('recursos3', 'Para repasar y gracias', head('Para repasar, y gracias') + f"""
<div class="split" style="grid-template-columns:7fr 4fr;gap:2.4em;align-items:start">
  <div class="col" style="gap:.9em">
    <div class="mapi"><span>Guía de estudio</span><b>el recorderis, los dos temas y el cierre, con ejemplos y ejercicios resueltos</b></div>
    <div class="mapi"><span>Slides</span><b>estas mismas, interactivas: mueve los deslizadores en casa</b></div>
    <div class="mapi"><span>NB05 y NB06</span><b>generalizar y ser robusto; reutilizar y explicar: todo escrito, para leer y experimentar</b></div>
    <div class="mapi"><span>Lectura</span><b>«¿Puedes explicar por qué tu modelo dijo «no»?» y su encuesta en Canvas</b></div>
    <p class="display" style="font-size:3em;margin-top:.6em">Gracias</p>
  </div>
  <div class="center">{qr('guia3')}</div>
</div>""", notes('Todo está en la página de la semana 3 (el código QR abre la guía de estudio). Al terminar, <b>«Finalizar reunión para todos»</b>.'),
    block='03', group=G3, minutes=1)
