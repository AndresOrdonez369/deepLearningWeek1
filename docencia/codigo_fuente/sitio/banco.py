"""Question bank for the Kahoot-style web quizzes (pre and final).
Single source for quiz/index.html, the teacher results panel and the teacher guide answer key.

Design: five KEY IDEAS (clave C1..C5) appear in BOTH quizzes as parallel items (same idea, different
numbers or context). Comparing them shows how much the group moved on each idea during the week.
The pre-quiz adds five prerequisite items; the final adds seven more items about the week."""

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
    "b09": "09 · Mini-proyecto y métricas",
    "pre": "Bases previas",
}

CLAVES = {
    "C1": "Calcular una neurona: z = w·x + b",
    "C2": "Para qué sirve la activación",
    "C3": "El límite de una sola línea (XOR)",
    "C4": "Hacia dónde mueve el gradiente",
    "C5": "Por qué la exactitud engaña con datos desbalanceados",
}

# each: q, options (4), ok (index), why (explanation shown to students), tema,
# mide (what it diagnoses, teacher only), clave (optional, paired key idea)
PRE = [
    dict(q="Un modelo de machine learning aprende…",
         options=["De reglas que escribe una persona", "De ejemplos con su respuesta correcta", "Buscando en internet en tiempo real", "Solo de imágenes"],
         ok=1, tema="b01", mide="Idea central de ML: aprender de ejemplos (x, y).",
         why="En machine learning le damos ejemplos con la respuesta correcta y el algoritmo descubre las reglas solo."),
    dict(q="Si f(x) = 2x + 1, ¿cuánto vale f(3)?",
         options=["5", "6", "7", "9"], ok=2, tema="pre", mide="Leer y evaluar una función: base para z = w·x + b.",
         why="Se reemplaza x por 3: 2·3 + 1 = 7. Una neurona hace exactamente esto con sus pesos."),
    dict(q="Una neurona calcula z = w₁·x₁ + w₂·x₂ + b. Con x = (2, 1), w = (1, 3) y b = −1, ¿cuánto vale z?",
         options=["2", "4", "5", "6"], ok=1, tema="b02", clave="C1",
         mide="Idea clave 1 antes de la clase: ¿siguen la fórmula aunque nunca hayan visto una neurona?",
         why="z = 1·2 + 3·1 + (−1) = 2 + 3 − 1 = 4. Cada dato por su peso, se suma todo y se agrega el sesgo: eso hace una neurona."),
    dict(q="¿Qué mide la pendiente de una recta?",
         options=["Su altura máxima", "Cuánto sube y por cada paso en x", "Dónde corta el eje x", "Su largo total"],
         ok=1, tema="pre", mide="Intuición de pendiente: base del gradiente.",
         why="La pendiente dice cuánto cambia y cuando x avanza un paso. El gradiente es la pendiente de la pérdida."),
    dict(q="Si una red solo multiplica y suma (sin función de activación), por muchas capas que tenga solo puede dibujar fronteras…",
         options=["Rectas", "Con cualquier forma", "Circulares", "Ninguna"], ok=0, tema="b02", clave="C2",
         mide="Idea clave 2 antes de la clase: intuición de que sin activación todo sigue siendo lineal.",
         why="Una suma de sumas sigue siendo una suma: el resultado es una recta (o un plano). La activación es la que permite curvas."),
    dict(q="Una probabilidad de 0.8 significa que algo pasa…",
         options=["80 de cada 100 veces", "8 de cada 100 veces", "Siempre", "0.8 veces"],
         ok=0, tema="pre", mide="Leer probabilidades: base para la sigmoide y la BCE.",
         why="0.8 = 80 %. La sigmoide de una neurona produce justamente una probabilidad entre 0 y 1."),
    dict(q="Puntos azules en las esquinas (0, 0) y (1, 1); naranjas en (0, 1) y (1, 0). ¿Los separa UNA sola línea recta?",
         options=["Sí, una horizontal", "Sí, una diagonal", "No, ninguna recta lo logra", "Sí, cualquier recta"],
         ok=2, tema="b03", clave="C3",
         mide="Idea clave 3 antes de la clase: ¿ven que hay patrones que ninguna recta separa?",
         why="Los colores están en esquinas opuestas: cualquier recta deja un azul y un naranja del mismo lado. Ese patrón se llama XOR."),
    dict(q="En Python con NumPy, ¿qué da np.array([1, 2]) * 3?",
         options=["[3 6]", "[1 2 1 2 1 2]", "9", "Un error"],
         ok=0, tema="pre", mide="Operaciones vectorizadas de NumPy (las usaremos en todos los notebooks).",
         why="NumPy multiplica cada elemento: [1·3, 2·3] = [3 6]. Con una lista normal de Python se repetiría la lista."),
    dict(q="Bajas una montaña con neblina. Bajo tus pies el suelo sube hacia la derecha. Para bajar, das el paso hacia…",
         options=["La izquierda", "La derecha", "Te quedas quieto", "Da igual"], ok=0, tema="b04", clave="C4",
         mide="Idea clave 4 antes de la clase: moverse en contra de la pendiente.",
         why="Si el suelo sube hacia la derecha (pendiente positiva), bajar es ir a la izquierda. El descenso de gradiente hace eso con los pesos."),
    dict(q="5 de cada 100 clientes caen en mora. Un modelo que siempre dice «no mora» acierta…",
         options=["5 %", "50 %", "95 %", "0 %"], ok=2, tema="b09", clave="C5",
         mide="Idea clave 5 antes de la clase: intuición del desbalance.",
         why="Acierta con los 95 que no caen en mora, pero no encuentra a ninguno de los 5. Por eso usamos otras métricas."),
]

FINAL = [
    dict(q="Una neurona con x = (1, 2), w = (3, −1) y b = 0.5. ¿Cuánto vale z?",
         options=["−1.5", "0.5", "1.5", "5.5"], ok=2, tema="b02", clave="C1", mide="Calcular z = w·x + b a mano.",
         why="z = 3·1 + (−1)·2 + 0.5 = 3 − 2 + 0.5 = 1.5."),
    dict(q="¿Para qué sirve la función de activación?",
         options=["Para que la red aprenda curvas, no solo rectas", "Para entrenar más rápido", "Para guardar los datos", "Para eliminar el sesgo"],
         ok=0, tema="b02", clave="C2", mide="Rol de la no linealidad.",
         why="Sin activación, apilar capas es solo sumar sumas: todo sería una línea recta. La activación «dobla» el espacio."),
    dict(q="¿Por qué una sola neurona no puede aprender XOR?",
         options=["Le faltan épocas", "No existe una línea recta que separe las clases", "La tasa de aprendizaje es muy grande", "Los datos tienen ruido"],
         ok=1, tema="b03", clave="C3", mide="Límite lineal del perceptrón.",
         why="Una neurona traza una sola línea. En XOR las luces encendidas están en esquinas opuestas: ninguna línea las separa."),
    dict(q="El perceptrón aprobó a un socio que NO pagó (y = −1). La regla…",
         options=["Le suma η·x a los pesos", "Le resta η·x a los pesos", "No cambia los pesos", "Pone los pesos en cero"],
         ok=1, tema="b03", mide="Aplicar la regla w ← w + η·y·x con y negativo.",
         why="w ← w + η·y·x con y = −1 queda w − η·x: aleja la frontera de ese socio."),
    dict(q="El modelo dijo 99 % «paga» y el socio NO pagó. La pérdida BCE es…",
         options=["Cero", "Muy alta", "Igual a 0.99", "Negativa"], ok=1, tema="b04", mide="BCE castiga la falsa seguridad.",
         why="BCE = −log(1 − 0.99) = −log(0.01) ≈ 4.6. Estar muy seguro y equivocado cuesta mucho."),
    dict(q="w nuevo = w − η·pendiente. Si la pendiente es negativa, el peso w…",
         options=["Sube", "Baja", "No cambia", "Se vuelve cero"], ok=0, tema="b04", clave="C4", mide="Signo en el descenso de gradiente.",
         why="Restar un número negativo es sumar: w sube, en la dirección en que baja la pérdida."),
    dict(q="La pérdida sube época a época y aparece NaN. ¿Qué revisas primero?",
         options=["La tasa de aprendizaje η (muy grande)", "El número de capas", "Los datos de prueba", "La semilla aleatoria"],
         ok=0, tema="b07", mide="Diagnóstico de divergencia.",
         why="Un paso demasiado grande se pasa del fondo y rebota cada vez más lejos: la pérdida explota."),
    dict(q="En la retropropagación, la culpa del error viaja…",
         options=["De la entrada hacia la salida", "De la salida hacia la entrada", "Solo dentro de la capa de salida", "Al azar"],
         ok=1, tema="b06", mide="Dirección del backward.",
         why="El error se mide al final y se reparte hacia atrás, capa por capa, con la regla de la cadena."),
    dict(q="¿Cuántos parámetros tiene una red 2 → 16 → 1?",
         options=["33", "48", "50", "65"], ok=3, tema="b05", mide="Contar pesos y sesgos.",
         why="Capa oculta: 2·16 + 16 = 48. Salida: 16·1 + 1 = 17. Total: 65."),
    dict(q="Con 4 800 ejemplos y batch_size = 32, ¿cuántos pasos tiene una época?",
         options=["1", "32", "150", "4 800"], ok=2, tema="b07", mide="Relación lote, paso y época.",
         why="4 800 ÷ 32 = 150 lotes; cada lote es un paso de aprendizaje."),
    dict(q="En Keras, ¿qué hace model.compile(...)?",
         options=["Apila las capas", "Elige optimizador, pérdida y métrica", "Entrena la red", "Hace predicciones"],
         ok=1, tema="b08", mide="Los tres pasos de Keras.",
         why="Construir (Sequential) → compilar (optimizador, pérdida, métrica) → entrenar (fit)."),
    dict(q="Solo 13 % cae en mora. ¿Por qué no basta la exactitud (accuracy)?",
         options=["Porque decir siempre «no mora» ya da 87 %", "Porque es difícil de calcular", "Porque Keras no la calcula", "Porque siempre da 100 %"],
         ok=0, tema="b09", clave="C5", mide="Métricas con datos desbalanceados.",
         why="Un modelo que no aprendió nada logra 87 %. Por eso miramos ROC-AUC y cuántos morosos detecta."),
]


def _check():
    for name, bank in (("PRE", PRE), ("FINAL", FINAL)):
        for q in bank:
            assert len(q["options"]) == 4 and 0 <= q["ok"] < 4, q["q"]
            assert q["tema"] in TEMAS and q.get("clave", "C1") in CLAVES, q["q"]
        keys = [q["clave"] for q in bank if "clave" in q]
        assert sorted(keys) == sorted(CLAVES), (name, keys)


_check()
