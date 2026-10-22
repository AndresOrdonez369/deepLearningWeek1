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

# Simple, no-calculation questions. Each: q, options (4), ok (index), why (shown to students), tema,
# mide (what it diagnoses, teacher only), clave (optional: the same key idea appears in PRE and FINAL)
PRE = [
    dict(q="Un modelo de machine learning aprende…",
         options=["De reglas que escribe una persona", "De ejemplos con su respuesta correcta", "Buscando en internet en tiempo real", "Solo de imágenes"],
         ok=1, tema="b01", mide="Idea central del machine learning: aprender de ejemplos con respuesta.",
         why="Le damos ejemplos con la respuesta correcta y el algoritmo descubre las reglas solo."),
    dict(q="¿Cuál de estos usa deep learning?",
         options=["Una calculadora", "Desbloquear el celular con tu cara", "Un reloj despertador", "Una fórmula de Excel"],
         ok=1, tema="b01", mide="Reconocer usos cotidianos del deep learning.",
         why="El desbloqueo facial usa una red neuronal que aprendió de millones de fotos de caras."),
    dict(q="Una neurona artificial recibe varios datos. ¿Qué hace con ellos?",
         options=["Elige el dato más grande", "Multiplica cada dato por su peso, suma todo y añade el sesgo", "Ordena los datos de menor a mayor", "Los guarda sin cambios"],
         ok=1, tema="b02", clave="C1", mide="Idea clave 1 antes de la clase: intuición de la suma con pesos.",
         why="Cada dato cuenta según su peso; se suma todo y se agrega el sesgo. Ese puntaje decide la respuesta."),
    dict(q="Si una red solo suma y multiplica (sin función de activación), ¿qué fronteras puede aprender?",
         options=["Solo líneas rectas", "Cualquier curva", "Solo círculos", "Ninguna"],
         ok=0, tema="b02", clave="C2", mide="Idea clave 2 antes de la clase: sin activación todo sigue siendo lineal.",
         why="Una suma de sumas sigue siendo una suma: una recta. La activación es la que permite curvas."),
    dict(q="La luz de la escalera se enciende si los dos interruptores están en posiciones distintas. ¿Una sola línea recta puede separar «encendida» de «apagada»?",
         options=["Sí, una horizontal", "Sí, una diagonal", "No, ninguna recta lo logra", "Sí, cualquier recta"],
         ok=2, tema="b03", clave="C3", mide="Idea clave 3 antes de la clase: hay patrones que ninguna recta separa (XOR).",
         why="Las luces encendidas quedan en esquinas opuestas: cualquier recta deja una encendida y una apagada del mismo lado."),
    dict(q="Una probabilidad de 0.8 significa que algo pasa…",
         options=["80 de cada 100 veces", "8 de cada 100 veces", "Siempre", "Nunca"],
         ok=0, tema="pre", mide="Leer probabilidades: base para la sigmoide.",
         why="0.8 es 80 %. Una neurona con sigmoide entrega justamente un número así, entre 0 y 1."),
    dict(q="Bajas una montaña con neblina y sientes que el suelo sube hacia la derecha. Para bajar, caminas hacia…",
         options=["La izquierda", "La derecha", "Te quedas quieto", "Da igual"],
         ok=0, tema="b04", clave="C4", mide="Idea clave 4 antes de la clase: moverse en contra de la pendiente.",
         why="Si sube hacia la derecha, bajar es ir a la izquierda. El descenso de gradiente hace eso con los pesos."),
    dict(q="5 de cada 100 compras con tarjeta son fraude. Un modelo que siempre dice «no es fraude», ¿es un buen modelo?",
         options=["Sí, acierta casi siempre", "No: acierta mucho, pero no encuentra ningún fraude", "Sí, nunca da falsas alarmas", "No se puede saber"],
         ok=1, tema="b09", clave="C5", mide="Idea clave 5 antes de la clase: intuición del desbalance.",
         why="Acierta con las 95 compras normales, pero no detecta ninguno de los 5 fraudes, que es lo que importa."),
]

FINAL = [
    dict(q="Una neurona calcula z = w·x + b. ¿Qué son los pesos w?",
         options=["Los datos de entrada", "Cuánto cuenta cada dato en la decisión", "La respuesta correcta", "El número de capas"],
         ok=1, tema="b02", clave="C1", mide="Idea clave 1: el papel de los pesos en la suma de la neurona.",
         why="Cada dato se multiplica por su peso: un peso grande hace que ese dato cuente mucho; uno negativo resta."),
    dict(q="¿Para qué sirve la función de activación?",
         options=["Para que la red pueda aprender curvas, no solo rectas", "Para que entrene más rápido", "Para guardar los datos", "Para borrar el sesgo"],
         ok=0, tema="b02", clave="C2", mide="Idea clave 2: el rol de la no linealidad.",
         why="Sin activación, apilar capas es solo sumar sumas. La activación «dobla» la línea y así aparecen las curvas."),
    dict(q="¿Cuándo corrige sus pesos el perceptrón?",
         options=["Siempre, aunque acierte", "Solo cuando se equivoca", "Nunca", "Solo al final del entrenamiento"],
         ok=1, tema="b03", mide="La regla del perceptrón: aprender de los errores.",
         why="Si acierta, no toca nada. Si se equivoca, empuja los pesos hacia la respuesta correcta."),
    dict(q="¿Por qué una sola neurona no puede aprender XOR (la luz de la escalera)?",
         options=["Porque le faltan épocas", "Porque solo traza una línea recta, y XOR necesita más de una", "Porque tiene pocos datos", "Porque el sesgo vale cero"],
         ok=1, tema="b03", clave="C3", mide="Idea clave 3: el límite lineal de una neurona.",
         why="Una neurona traza una sola recta. Con dos neuronas ocultas (dos rectas) la red sí lo resuelve."),
    dict(q="¿Qué mide la pérdida (loss)?",
         options=["Qué tan equivocado está el modelo", "Cuántos datos hay", "Cuánto tarda en entrenar", "Cuántas capas tiene la red"],
         ok=0, tema="b04", mide="Concepto de función de pérdida.",
         why="Es un solo número que dice qué tan mal vamos: como una nota al revés, 0 es perfecto."),
    dict(q="En el descenso de gradiente, cada paso va…",
         options=["Hacia donde sube el error", "En contra de la pendiente, hacia donde baja el error", "Siempre hacia la derecha", "Al azar"],
         ok=1, tema="b04", clave="C4", mide="Idea clave 4: la dirección del paso.",
         why="La pendiente apunta cuesta arriba; por eso se resta: el peso se mueve hacia donde la pérdida baja."),
    dict(q="Si el tamaño del paso (learning rate) es demasiado grande…",
         options=["Siempre aprende mejor", "Se pasa del fondo y la pérdida puede crecer", "No cambia nada", "La red se queda sin datos"],
         ok=1, tema="b07", mide="Efecto de una tasa de aprendizaje excesiva.",
         why="Como echar medio salero al locro: te pasas, corriges al revés y te alejas cada vez más."),
    dict(q="En la retropropagación, la culpa del error viaja…",
         options=["De la entrada hacia la salida", "De la salida hacia la entrada", "Solo dentro de la capa de salida", "Al azar"],
         ok=1, tema="b06", mide="Dirección del paso hacia atrás (backward).",
         why="El error se descubre al final y se reparte hacia atrás, como la barra de chocolate amarga en la cadena del cacao."),
    dict(q="En Keras, ¿qué hace model.fit(...)?",
         options=["Dibuja la red", "Entrena la red con los datos", "Borra los pesos", "Descarga los datos"],
         ok=1, tema="b08", mide="Los tres pasos de Keras: construir, compilar, entrenar.",
         why="fit repite adelante, atrás y actualizar, por lotes y durante varias épocas: eso es entrenar."),
    dict(q="Solo 13 de cada 100 socios caen en mora. Un modelo que siempre dice «está al día» tiene 87 % de exactitud. ¿Qué pasa?",
         options=["Es un modelo excelente", "No encuentra a ningún moroso: la exactitud engaña", "Encuentra a 87 morosos", "Su exactitud real es 13 %"],
         ok=1, tema="b09", clave="C5", mide="Idea clave 5: métricas con datos desbalanceados.",
         why="Acertar 87 de 100 sin encontrar a ningún moroso no sirve. Por eso miramos cuántos morosos detecta (recall) y el AUC."),
]


def _check():
    for name, bank in (("PRE", PRE), ("FINAL", FINAL)):
        for q in bank:
            assert len(q["options"]) == 4 and 0 <= q["ok"] < 4, q["q"]
            assert q["tema"] in TEMAS and q.get("clave", "C1") in CLAVES, q["q"]
        keys = [q["clave"] for q in bank if "clave" in q]
        assert sorted(keys) == sorted(CLAVES), (name, keys)


_check()
