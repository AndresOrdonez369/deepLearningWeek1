"""Question bank for the Kahoot-style web quizzes (pre and final).
Single source for quiz/index.html, the teacher results panel and the teacher guide answer key.

Design: five KEY IDEAS (clave C1..C5) appear in BOTH quizzes as parallel items (same idea, different
numbers or context). Comparing them shows how much the group moved on each idea during the week.
The pre-quiz adds three simple base items; the final adds five more items about the week. No calculations."""

# tema keys map to study-guide anchors
TEMAS = {
    "b01": "01 · IA, machine learning y deep learning",
    "b02": "02 · La neurona artificial",
    "b03": "03 · El perceptrón y XOR",
    "b04": "04 · Pérdida y descenso de gradiente",
    "b05": "05 · De una neurona a una red",
    "b06": "06 · Retropropagación",
    "b07": "07 · Entrenar bien",
    "b08": "08 · Keras",
    "b09": "09 · ¿El modelo es bueno?",
    "pre": "Bases previas",
}

CLAVES = {
    "C1": "Qué calcula una neurona (pesos, suma y sesgo)",
    "C2": "Para qué sirve la activación",
    "C3": "El límite de una sola línea (XOR)",
    "C4": "Hacia dónde camina el descenso de gradiente",
    "C5": "Por qué la exactitud engaña con datos desbalanceados",
}

# Simple, no-calculation questions. Each: q, options (4), ok (index), tema, clave (optional: the same key idea
# appears in PRE and FINAL), mide (what it diagnoses, teacher only) and, shown to students after answering:
#   why  · why the right answer is right, in plain words (uses the week's analogies)
#   no   · one short line per option: why that wrong option is tempting but wrong (None for the right one)
#   fig  · optional key of a mini drawing in quiz_template.html (neuron, bend, xor, slope, alarm, eta, back, sigmoid, rules)
PRE = [
    dict(q="Un modelo de machine learning aprende…",
         options=["De reglas que escribe una persona", "De ejemplos con su respuesta correcta", "Buscando en internet en tiempo real", "Solo de imágenes"],
         ok=1, tema="b01", mide="Idea central del machine learning: aprender de ejemplos con respuesta.", fig="rules",
         why="Le mostramos muchos ejemplos con su respuesta (correos ya marcados como spam o no) y el algoritmo descubre solo las reglas. Es lo contrario de la programación clásica, donde una persona las escribe.",
         no=["Eso es programación clásica: reglas escritas a mano. En machine learning las reglas salen de los ejemplos.", None,
             "No busca nada en internet: aprende antes, de los ejemplos que le damos para entrenar.",
             "Aprende de cualquier tipo de dato: tablas, texto, audio o imágenes."]),
    dict(q="¿Cuál de estos usa deep learning?",
         options=["Una calculadora", "Desbloquear el celular con tu cara", "Un reloj despertador", "Una fórmula de Excel"],
         ok=1, tema="b01", mide="Reconocer usos cotidianos del deep learning.",
         why="El desbloqueo facial usa una red neuronal de muchas capas que aprendió de millones de fotos de caras. Nadie escribió a mano la regla de «cómo se ve tu cara».",
         no=["Una calculadora sigue reglas fijas de aritmética: no aprende nada.", None,
             "Un despertador solo compara la hora actual con la que programaste.",
             "Una fórmula de Excel hace exactamente lo que alguien escribió: es una regla, no aprende."]),
    dict(q="Una neurona artificial recibe varios datos. ¿Qué hace con ellos?",
         options=["Elige el dato más grande", "Multiplica cada dato por su peso, suma todo y añade el sesgo", "Ordena los datos de menor a mayor", "Los guarda sin cambios"],
         ok=1, tema="b02", clave="C1", mide="Idea clave 1 antes de la clase: intuición de la suma con pesos.", fig="neuron",
         why="Es como tu nota final del curso: cada nota se multiplica por lo que pesa, se suma todo y se le resta la exigencia (el sesgo). Ese puntaje decide la respuesta.",
         no=["No se queda con un solo dato: todos cuentan, cada uno según su peso.", None,
             "Ordenar no decide nada: la neurona combina los datos en un solo puntaje.",
             "Si los guardara sin cambios no podría decidir: los convierte en un puntaje."]),
    dict(q="Si una red solo suma y multiplica (sin función de activación), ¿qué fronteras puede aprender?",
         options=["Solo líneas rectas", "Cualquier curva", "Solo círculos", "Ninguna"],
         ok=0, tema="b02", clave="C2", mide="Idea clave 2 antes de la clase: sin activación todo sigue siendo lineal.", fig="bend",
         why="Una suma de sumas sigue siendo una suma: una línea recta, aunque apiles 100 capas. La activación es el «doblez» que permite curvas.",
         no=[None, "Para hacer curvas hace falta la activación: sin ella cada capa solo vuelve a sumar.",
             "Un círculo también es una curva: sin activación tampoco sale.",
             "Sí aprende algo: rectas. Lo que no puede es doblarlas."]),
    dict(q="La luz de la escalera se enciende si los dos interruptores están en posiciones distintas. ¿Una sola línea recta puede separar «encendida» de «apagada»?",
         options=["Sí, una horizontal", "Sí, una diagonal", "No, ninguna recta lo logra", "Sí, cualquier recta"],
         ok=2, tema="b03", clave="C3", mide="Idea clave 3 antes de la clase: hay patrones que ninguna recta separa (XOR).", fig="xor",
         why="Las luces encendidas quedan en esquinas opuestas. Cualquier recta que traces deja una encendida y una apagada del mismo lado. Para lograrlo hacen falta dos rectas, es decir, dos neuronas.",
         no=["Una horizontal deja juntas una encendida y una apagada: falla en dos esquinas.",
             "Una diagonal deja un par de esquinas opuestas del mismo lado: siempre se equivoca en una.", None,
             "Pruébalo con la que quieras: ninguna recta acierta las cuatro esquinas."]),
    dict(q="Una probabilidad de 0.8 significa que algo pasa…",
         options=["80 de cada 100 veces", "8 de cada 100 veces", "Siempre", "Nunca"],
         ok=0, tema="pre", mide="Leer probabilidades: base para la sigmoide.", fig="sigmoid",
         why="0.8 es 80 %: 80 de cada 100 veces. Una neurona con sigmoide entrega justo un número así, entre 0 y 1, como un regulador de luz que va de apagado a encendido.",
         no=[None, "8 de cada 100 sería 0.08.", "«Siempre» sería 1. 0.8 es alto, pero no seguro.", "«Nunca» sería 0."]),
    dict(q="Bajas una montaña con neblina y sientes que el suelo sube hacia la derecha. Para bajar, caminas hacia…",
         options=["La izquierda", "La derecha", "Te quedas quieto", "Da igual"],
         ok=0, tema="b04", clave="C4", mide="Idea clave 4 antes de la clase: moverse en contra de la pendiente.", fig="slope",
         why="Si el suelo sube hacia la derecha, bajar es ir a la izquierda: en contra de la pendiente. Es el Cotopaxi con neblina: no ves la laguna, pero el pie siente la inclinación. El descenso de gradiente hace eso con los pesos.",
         no=[None, "Hacia la derecha subes: la pérdida aumentaría.",
             "Quieto no llegas al fondo; solo te detienes cuando el suelo ya está plano.",
             "No da igual: un lado sube y el otro baja."]),
    dict(q="5 de cada 100 compras con tarjeta son fraude. Un modelo que siempre dice «no es fraude», ¿es un buen modelo?",
         options=["Sí, acierta casi siempre", "No: acierta mucho, pero no encuentra ningún fraude", "Sí, nunca da falsas alarmas", "No se puede saber"],
         ok=1, tema="b09", clave="C5", mide="Idea clave 5 antes de la clase: intuición del desbalance.", fig="alarm",
         why="Acierta con las 95 compras normales (95 % de exactitud), pero no detecta ninguno de los 5 fraudes, que es justo lo que importa. Es como una alarma de humo que nunca suena.",
         no=["Acertar mucho no basta si falla en todos los casos que buscas.", None,
             "No da falsas alarmas porque nunca da ninguna alarma: tampoco encuentra fraudes.",
             "Sí se puede saber: no encuentra ninguno de los 5 fraudes."]),
]

FINAL = [
    dict(q="Una neurona calcula z = w·x + b. ¿Qué son los pesos w?",
         options=["Los datos de entrada", "Cuánto cuenta cada dato en la decisión", "La respuesta correcta", "El número de capas"],
         ok=1, tema="b02", clave="C1", mide="Idea clave 1: el papel de los pesos en la suma de la neurona.", fig="neuron",
         why="Los pesos dicen cuánto cuenta cada dato, como el porcentaje de cada nota en tu nota final. Un peso grande hace que ese dato pese mucho; uno negativo resta, como los atrasos en el comité de crédito.",
         no=["Los datos de entrada son las x; los pesos son los números que los multiplican.", None,
             "La respuesta correcta es la y, la que usamos para corregir al entrenar.",
             "Las capas son el diseño de la red; los pesos viven dentro de cada neurona."]),
    dict(q="¿Para qué sirve la función de activación?",
         options=["Para que la red pueda aprender curvas, no solo rectas", "Para que entrene más rápido", "Para guardar los datos", "Para borrar el sesgo"],
         ok=0, tema="b02", clave="C2", mide="Idea clave 2: el rol de la no linealidad.", fig="bend",
         why="Sin activación, apilar capas es solo sumar sumas: una recta. La activación (interruptor, regulador de luz o válvula) «dobla» la línea, y con varios dobleces la red arma curvas.",
         no=[None, "La velocidad depende del optimizador y del tamaño del paso, no de la activación.",
             "Los datos no se guardan en la activación: ella transforma el puntaje.",
             "El sesgo sigue ahí: la activación se aplica después de sumarlo."]),
    dict(q="¿Cuándo corrige sus pesos el perceptrón?",
         options=["Siempre, aunque acierte", "Solo cuando se equivoca", "Nunca", "Solo al final del entrenamiento"],
         ok=1, tema="b03", mide="La regla del perceptrón: aprender de los errores.",
         why="Solo aprende de sus errores: si acierta, no toca nada; si se equivoca, empuja los pesos hacia la respuesta correcta. Como sazonar un locro: solo echas sal si le falta.",
         no=["Si corrigiera cuando acierta, podría deshacer lo que ya sabe.", None,
             "Si nunca corrigiera, nunca aprendería.",
             "Corrige durante todo el entrenamiento, ejemplo por ejemplo."]),
    dict(q="¿Por qué una sola neurona no puede aprender XOR (la luz de la escalera)?",
         options=["Porque le faltan épocas", "Porque solo traza una línea recta, y XOR necesita más de una", "Porque tiene pocos datos", "Porque el sesgo vale cero"],
         ok=1, tema="b03", clave="C3", mide="Idea clave 3: el límite lineal de una neurona.", fig="xor",
         why="Una neurona traza una sola recta, y las luces encendidas están en esquinas opuestas. Con dos neuronas ocultas (dos rectas) la red arma la franja del medio y lo resuelve.",
         no=["Más épocas no ayudan: ninguna recta lo separa, por más que entrene.", None,
             "Son solo cuatro casos: el problema es la forma, no la cantidad de datos.",
             "Cambiar el sesgo solo desplaza la recta: sigue siendo una recta."]),
    dict(q="¿Qué mide la pérdida (loss)?",
         options=["Qué tan equivocado está el modelo", "Cuántos datos hay", "Cuánto tarda en entrenar", "Cuántas capas tiene la red"],
         ok=0, tema="b04", mide="Concepto de función de pérdida.",
         why="La pérdida es un solo número que dice qué tan mal vamos: como una nota al revés, 0 es perfecto. Entrenar es hacer que baje.",
         no=[None, "La cantidad de datos no cambia al entrenar; la pérdida sí.",
             "El tiempo no dice si el modelo acierta o no.",
             "Las capas son el diseño de la red, no su error."]),
    dict(q="En el descenso de gradiente, cada paso va…",
         options=["Hacia donde sube el error", "En contra de la pendiente, hacia donde baja el error", "Siempre hacia la derecha", "Al azar"],
         ok=1, tema="b04", clave="C4", mide="Idea clave 4: la dirección del paso.", fig="slope",
         why="La pendiente apunta cuesta arriba; por eso se resta: peso nuevo = peso − η · pendiente. Como bajar el Cotopaxi con neblina: das el paso hacia donde el pie siente que el terreno baja.",
         no=["Ir hacia donde sube el error es subir la montaña: justo al revés.", None,
             "Depende de la pendiente: a veces el paso va a la derecha y a veces a la izquierda.",
             "No es al azar: cada paso usa la pendiente."]),
    dict(q="Si el tamaño del paso (learning rate) es demasiado grande…",
         options=["Siempre aprende mejor", "Se pasa del fondo y la pérdida puede crecer", "No cambia nada", "La red se queda sin datos"],
         ok=1, tema="b07", mide="Efecto de una tasa de aprendizaje excesiva.", fig="eta",
         why="Se pasa del fondo, cae al otro lado más alto y puede alejarse cada vez más. Como la ducha: giras de golpe la llave del agua caliente y te quemas, la cierras de golpe y te congelas.",
         no=["Más grande no es mejor: pasado cierto punto, el paso salta por encima del fondo.", None,
             "Sí cambia: el tamaño del paso es de lo que más afecta al entrenamiento.",
             "Los datos no se acaban: lo que falla es el tamaño del paso."]),
    dict(q="En la retropropagación, la culpa del error viaja…",
         options=["De la entrada hacia la salida", "De la salida hacia la entrada", "Solo dentro de la capa de salida", "Al azar"],
         ok=1, tema="b06", mide="Dirección del paso hacia atrás (backward).", fig="back",
         why="El error se descubre al final (en la salida) y la culpa se reparte hacia atrás, capa por capa, según cuánto influyó cada peso. Como la barra de chocolate amarga: se revisa del tostado hacia la cosecha.",
         no=["De la entrada a la salida va la predicción (hacia adelante), no la culpa.", None,
             "La culpa llega a todas las capas: así cada peso sabe cuánto moverse.",
             "No es al azar: sigue la regla de la cadena, como engranajes."]),
    dict(q="En Keras, ¿qué hace model.fit(...)?",
         options=["Dibuja la red", "Entrena la red con los datos", "Borra los pesos", "Descarga los datos"],
         ok=1, tema="b08", mide="Los tres pasos de Keras: construir, compilar, entrenar.",
         why="fit entrena: repite adelante, atrás y actualizar, por lotes y durante varias épocas. Antes van Sequential (construir la red, como apilar piezas de LEGO) y compile (elegir la pérdida y el optimizador).",
         no=["Para ver la red se usa model.summary().", None,
             "fit no borra nada: ajusta los pesos poco a poco.",
             "Los datos ya los tienes en X e y; fit los usa para aprender."]),
    dict(q="Solo 13 de cada 100 socios caen en mora. Un modelo que siempre dice «está al día» tiene 87 % de exactitud. ¿Qué pasa?",
         options=["Es un modelo excelente", "No encuentra a ningún moroso: la exactitud engaña", "Encuentra a 87 morosos", "Su exactitud real es 13 %"],
         ok=1, tema="b09", clave="C5", mide="Idea clave 5: métricas con datos desbalanceados.", fig="alarm",
         why="Acertar 87 de 100 sin encontrar a ningún moroso no sirve: es una alarma de humo que nunca suena. Por eso miramos el recall (cuántos morosos encontramos), la precisión y el AUC.",
         no=["87 % suena bien, pero es justo lo que logra quien nunca marca a nadie.", None,
             "No marca a nadie como moroso: encuentra 0.",
             "La exactitud sí es 87 %; el problema es que no mide lo que nos importa."]),
]

FIGS = ("neuron", "bend", "xor", "slope", "alarm", "eta", "back", "sigmoid", "rules")


def _check():
    for name, bank in (("PRE", PRE), ("FINAL", FINAL)):
        for q in bank:
            assert len(q["options"]) == 4 and 0 <= q["ok"] < 4, q["q"]
            assert q["tema"] in TEMAS and q.get("clave", "C1") in CLAVES, q["q"]
            assert len(q["no"]) == 4 and q["no"][q["ok"]] is None and all(q["no"][j] for j in range(4) if j != q["ok"]), q["q"]
            assert q.get("fig") in (None,) + FIGS, q["q"]
        keys = [q["clave"] for q in bank if "clave" in q]
        assert sorted(keys) == sorted(CLAVES), (name, keys)


_check()
