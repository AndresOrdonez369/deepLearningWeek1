"""Question bank of week 2 for the Kahoot-style web quizzes (pre and final).
Single source for semana2/quiz/index.html, the teacher results panel and the teacher guide answer key.

Design (same as week 1): the five KEY IDEAS of the week (clave C1..C5) appear in BOTH quizzes as parallel items
(same idea, different words or context). Comparing them shows how much the group moved on each idea.
The pre-quiz adds three simple base items; the final adds five more items about the week. No calculations."""

# tema keys map to study-guide anchors (semana2/guia/index.html#b01 ...)
TEMAS = {
    "b00": "00 · Keras en 4 pasos",
    "b01": "01 · Imágenes y redes convolucionales",
    "b02": "02 · Secuencias, RNN y LSTM",
    "b03": "03 · Atención, Transformers y la tendencia",
    "b04": "04 · Elegir la arquitectura",
    "pre": "Bases previas",
}

CLAVES = {
    "C1": "Cada arquitectura es una suposición sobre los datos",
    "C2": "Qué hace un filtro convolucional",
    "C3": "Por qué una CNN necesita muchos menos parámetros",
    "C4": "Qué guarda una RNN y por qué se olvida",
    "C5": "Qué hace la atención y cuál es su precio",
}

# Each item: q, options (4), ok (index), tema, clave (optional), mide (teacher only) and, shown to students after answering:
#   why · why the right answer is right, in plain words (uses the week's analogies)
#   no  · one short line per option: why that wrong option is tempting but wrong (None for the right one)
#   fig · optional key of a mini drawing in quiz_template2.html
PRE = [
    dict(q="Para una computadora, una foto en blanco y negro es…",
         options=["Una tabla de números: el brillo de cada píxel", "Un texto que describe la foto", "Una lista de colores con nombre", "Algo que no se puede convertir en números"],
         ok=0, tema="pre", mide="Base: una imagen es una tabla de números (28 × 28 = 784 brillos).", fig="pixels",
         why="Cada píxel guarda un número de brillo: 0 es negro y 255 es blanco. Una foto de 28 × 28 píxeles es una tabla de 784 números, y eso es todo lo que la red recibe.",
         no=[None, "La red no recibe palabras: recibe los números de cada píxel.",
             "Los colores también se guardan como números (rojo, verde y azul); aquí es blanco y negro: un número por píxel.",
             "Toda foto digital ya es números: así la guarda tu celular."]),
    dict(q="¿Cuál de estos datos llega en un orden que importa?",
         options=["Las edades de 100 socios en una tabla", "Las palabras de una frase", "El color favorito de cada estudiante", "El inventario de una bodega"],
         ok=1, tema="pre", mide="Base: reconocer datos secuenciales (el orden cambia el significado).", fig="orden",
         why="«El perro mordió al cartero» y «el cartero mordió al perro» tienen las mismas palabras y dicen cosas distintas. En una frase, el orden es parte del significado.",
         no=["Si ordenas la tabla de otra forma, las edades no cambian de significado.", None,
             "El color favorito de cada uno no depende de quién se anotó primero.",
             "Contar lo que hay en la bodega da lo mismo en cualquier orden."]),
    dict(q="En Keras, ¿qué paso entrena la red?",
         options=["model.summary()", "keras.Input(...)", "model.fit(...)", "model.predict(...)"],
         ok=2, tema="b00", mide="Base (pendiente de la semana 1): los pasos de Keras; fit es el que entrena.", fig="keras",
         why="fit repite adelante, atrás y actualizar con los datos de entrenamiento, por lotes y durante varias épocas. Es el único paso que cambia los pesos.",
         no=["summary solo muestra la tabla de capas y parámetros: no entrena.",
             "Input solo dice qué forma tiene cada ejemplo que entra a la red.", None,
             "predict usa lo aprendido para responder: no cambia ningún peso."]),
    dict(q="Una red densa recibe cada foto aplanada en una fila de 784 números. Si mezclamos los píxeles de TODAS las fotos de la misma manera, ¿qué le pasa a su exactitud?",
         options=["Casi nada: nunca usó qué píxel está al lado de cuál", "Se cae a cero", "Sube mucho", "La red deja de funcionar"],
         ok=0, tema="b01", clave="C1", mide="Idea clave 1 antes de la clase: la red densa no supone nada sobre la vecindad de los píxeles.", fig="suposicion",
         why="Para una red densa, cada píxel es una columna más de una tabla: no sabe cuál está junto a cuál. Si la mezcla es la misma para todas las fotos, para ella el problema es idéntico (en el NB03: 86.7 % normal y 87.2 % mezclada).",
         no=[None, "No se cae: los píxeles siguen ahí, solo que en otras columnas, y la densa nunca miró el orden.",
             "No sube: es el mismo problema con otras columnas; la diferencia es ruido.",
             "Sigue funcionando igual: recibe 784 números como siempre."]),
    dict(q="Un filtro de 3 × 3 que detecta bordes verticales recorre una foto. ¿Dónde responde con fuerza?",
         options=["En el centro de la foto, siempre", "Donde un lado está oscuro y el otro claro: en un borde", "Donde todo es del mismo color", "En ninguna parte: solo cuenta píxeles"],
         ok=1, tema="b01", clave="C2", mide="Idea clave 2 antes de la clase: un filtro es un detector de un patrón local.", fig="filtro",
         why="El filtro es una lupa que mira 9 píxeles a la vez: resta la columna de la izquierda y suma la de la derecha. Si los dos lados son iguales da 0; si hay un borde (oscuro → claro) da un número grande.",
         no=["No depende del lugar: responde donde encuentre su patrón, esté donde esté.", None,
             "Donde todo es igual, la resta de los dos lados da 0: no hay nada que detectar.",
             "No cuenta: multiplica cada píxel por un peso y suma. Eso detecta formas."]),
    dict(q="¿Por qué una red convolucional (CNN) necesita muchos menos parámetros que una densa para la misma foto?",
         options=["Porque mira menos píxeles", "Porque no tiene sesgos", "Porque usa el mismo filtro pequeño en toda la imagen", "Porque solo funciona con fotos pequeñas"],
         ok=2, tema="b01", clave="C3", mide="Idea clave 3 antes de la clase: compartir pesos.", fig="share",
         why="Un filtro de 3 × 3 tiene 9 pesos y 1 sesgo, y se usa en todas las posiciones de la foto, como un sello que se estampa en toda la hoja. Una neurona densa, en cambio, necesita un peso por cada píxel.",
         no=["La CNN mira todos los píxeles: el filtro pasa por toda la foto.",
             "Sí tiene sesgos: uno por filtro.", None,
             "Funciona con fotos de cualquier tamaño; la idea de compartir el filtro sirve igual."]),
    dict(q="Una red recurrente (RNN) lee una frase palabra por palabra y guarda lo leído en un resumen de tamaño fijo. ¿Qué le cuesta más?",
         options=["Leer la palabra actual", "Leer frases cortas", "Saber cuántas letras tiene una palabra", "Recordar algo que leyó muchas palabras atrás"],
         ok=3, tema="b02", clave="C4", mide="Idea clave 4 antes de la clase: la libreta de tamaño fijo se olvida de lo lejano.", fig="libreta",
         why="Es como leer un libro con una libreta pequeña: en cada página reescribes el resumen. Lo del principio se va borrando, y al entrenar la culpa que viaja hacia atrás se debilita en cada paso.",
         no=["La palabra actual es lo más fácil: la tiene enfrente.",
             "Con frases cortas casi no hay nada que olvidar.",
             "Eso no es lo difícil: lo difícil es mantener lo importante durante muchos pasos.", None]),
    dict(q="En un Transformer, la atención permite que cada palabra…",
         options=["Lea solo a la palabra anterior", "Mire a todas las demás y decida cuáles le importan", "Se lea una sola vez y se olvide", "Cuente cuántas letras tiene la frase"],
         ok=1, tema="b03", clave="C5", mide="Idea clave 5 antes de la clase: la atención compara cada palabra con todas.", fig="atencion",
         why="En «el socio pagó la cuota porque él recibió su sueldo», la palabra «él» mira a todas y descubre que se refiere a «socio», no a «cuota». Cada palabra consulta directamente a las demás.",
         no=["Leer solo la anterior es lo que hace una RNN paso a paso; la atención mira todo a la vez.", None,
             "Al revés: la atención puede volver a consultar cualquier palabra del texto.",
             "No cuenta letras: compara significados para decidir a quién mirar."]),
]

FINAL = [
    dict(q="Cada arquitectura supone algo sobre los datos. ¿Qué supone una red convolucional (CNN)?",
         options=["Que el orden en el tiempo es lo más importante", "Que lo cercano importa y el mismo patrón puede aparecer en cualquier parte", "Que todos los datos se relacionan con todos por igual", "Nada: funciona igual con cualquier dato"],
         ok=1, tema="b01", clave="C1", mide="Idea clave 1: la suposición de cada arquitectura (densa, CNN, RNN).", fig="suposicion",
         why="La CNN es una lupa que recorre la foto: mira vecindarios pequeños (lo cercano importa) y usa la misma lupa en todas partes. Por eso, si mezclamos los píxeles, le duele (87.7 % → 85.2 %) y a la densa no.",
         no=["Esa es la suposición de la RNN: el orden importa.", None,
             "Esa es la de la red densa: todo con todo.",
             "Toda arquitectura supone algo; elegir bien es saber qué supone cada una."]),
    dict(q="¿Qué es un mapa de activación?",
         options=["El resultado de pasar un filtro por toda la imagen: dónde encontró su patrón", "La lista de las 10 clases posibles", "El dibujo de las capas de la red", "La foto original en colores"],
         ok=0, tema="b01", clave="C2", mide="Idea clave 2: filtro → mapa de activación.", fig="filtro",
         why="El filtro se coloca en cada ventana de 3 × 3, multiplica y suma, y anota un número. Al recorrer toda la foto queda una tabla nueva (26 × 26 en el NB03) que se enciende donde está el patrón: un borde, una esquina, una suela.",
         no=[None, "Las clases salen al final, de la capa softmax.",
             "Ese dibujo es el resumen de la red (model.summary).",
             "El mapa es una tabla nueva calculada por el filtro, no la foto."]),
    dict(q="La primera capa de la CNN del NB03 tiene 16 filtros de 3 × 3 y solo 160 parámetros, aunque cada foto tiene 784 píxeles. ¿Por qué tan pocos?",
         options=["Porque ignora la mayoría de los píxeles", "Porque los filtros no se aprenden", "Porque cada filtro (9 pesos + 1 sesgo) se reutiliza en todas las posiciones", "Porque la foto se reduce antes a 16 píxeles"],
         ok=2, tema="b01", clave="C3", mide="Idea clave 3: compartir pesos explica 160 frente a 100 480.", fig="share",
         why="Cada filtro tiene 10 números y se estampa en toda la foto, como un sello. 16 filtros × 10 = 160. La primera capa densa, con un peso por píxel para cada neurona, necesita 100 480.",
         no=["El filtro pasa por todos los píxeles, de tres en tres.",
             "Sí se aprenden: en el NB03 se ve que salen detectores de bordes, y nadie los programó.", None,
             "La foto entra completa (28 × 28); la que se achica es la salida, después."]),
    dict(q="¿Por qué una RNN simple «se olvida» de lo que leyó al principio de una secuencia larga?",
         options=["Porque borra su memoria cada 10 pasos", "Porque la señal del error se debilita en cada paso al viajar hacia atrás", "Porque solo lee la última palabra", "Porque tiene demasiados parámetros"],
         ok=1, tema="b02", clave="C4", mide="Idea clave 4: la libreta de tamaño fijo y la culpa que se debilita en el tiempo.", fig="olvido",
         why="Al entrenar, la culpa viaja hacia atrás paso por paso y en cada uno se multiplica por un número pequeño: con 0.5 por paso, después de 10 pasos queda 0.001. Es el teléfono dañado de la semana 1, ahora en el tiempo. En el NB04, con 80 pasos, la RNN adivina (52 %).",
         no=["No hay un borrado programado: el olvido sale de las multiplicaciones.", None,
             "Lee todas las palabras, una por una; el problema es mantener lo lejano.",
             "La SimpleRNN del NB04 tiene pocos (1 153); el problema es la distancia, no el tamaño."]),
    dict(q="La atención compara cada palabra con todas las demás. Si el texto es 10 veces más largo, ¿cuántas comparaciones hace?",
         options=["Las mismas", "10 veces más", "Unas 100 veces más: crece con el cuadrado", "La mitad"],
         ok=2, tema="b03", clave="C5", mide="Idea clave 5: el precio cuadrático de la atención.", fig="costo",
         why="Con n palabras son n × n comparaciones: con 1 000 palabras, un millón. Diez veces más palabras son cien veces más comparaciones. Por eso los textos larguísimos se volvieron un cuello de botella y volvieron las recurrentes (lectura de tendencia).",
         no=["Más palabras, más comparaciones: cada una mira a todas.",
             "Sería así si cada palabra mirara solo a unas pocas; mira a todas.", None,
             "Nunca baja: crece, y rápido."]),
    dict(q="¿Qué hace un MaxPooling de 2 × 2?",
         options=["Duplica el tamaño de la imagen", "De cada ventana de 2 × 2 se queda con el número más grande", "Promedia todas las imágenes del lote", "Borra los bordes de la foto"],
         ok=1, tema="b01", mide="Pooling: resumir el mapa quedándose con lo más fuerte.", fig="pool",
         why="Resume el mapa: de cada cuadrito de 4 números se queda con el mayor, como subrayar la frase más importante de cada párrafo. El mapa queda de la mitad de alto y de ancho (26 × 26 → 13 × 13).",
         no=["Hace lo contrario: el mapa queda de la mitad de tamaño.", None,
             "Trabaja dentro de cada mapa, no mezcla fotos distintas.",
             "No borra nada a propósito: conserva el valor más fuerte de cada ventana."]),
    dict(q="En Keras, para pasar de la red densa a una CNN, ¿qué cambias?",
         options=["Las capas: Conv2D y MaxPooling2D antes de la salida; compile y fit siguen igual", "Todo: Keras usa otro método para entrenar CNN", "Solo el número de épocas", "Nada: una Dense ya es una CNN"],
         ok=0, tema="b00", mide="Keras en 4 pasos con otra arquitectura: solo cambia el paso construir.", fig="keras",
         why="Los cuatro pasos son los mismos: construir, compilar, entrenar y predecir. Lo único que cambia es la lista de capas dentro de Sequential.",
         no=[None, "El entrenamiento es el mismo: adelante, atrás y actualizar dentro de fit.",
             "Las épocas no cambian la arquitectura: una Dense sigue siendo densa.",
             "Una Dense mira todos los píxeles con un peso propio cada uno; no tiene filtros."]),
    dict(q="¿Qué agrega una LSTM a la libreta de la RNN simple?",
         options=["Filtros de 3 × 3", "Compuertas que deciden qué olvidar, qué guardar y qué mostrar", "Más capas densas al final", "Una cámara para ver imágenes"],
         ok=1, tema="b02", mide="LSTM (1997): compuertas como válvulas entre 0 y 1.", fig="lstm",
         why="Cada compuerta es una sigmoide entre 0 y 1, como una válvula: una decide qué borrar de la libreta, otra qué anotar y otra qué leer en voz alta. Así lo importante puede viajar más lejos sin borrarse.",
         no=["Los filtros de 3 × 3 son de las CNN.", None,
             "Las capas densas no le dan memoria; las compuertas sí.",
             "La LSTM lee secuencias, no fotos."]),
    dict(q="Según la lectura de tendencia, ¿qué hacen modelos híbridos como Jamba o Nemotron-H?",
         options=["Usan solo atención, cada vez más grande", "Vuelven a las redes de la década de 1950", "Reemplazan las redes por reglas escritas a mano", "Mezclan muchas capas recurrentes baratas con unas pocas capas de atención"],
         ok=3, tema="b03", mide="Tendencia de la semana: los híbridos recurrente + atención.", fig="hibrido",
         why="Son como un buen estudiante: toman apuntes resumidos de casi todo (capas recurrentes, como Mamba) y de vez en cuando vuelven al libro para un dato exacto (atención). Jamba usa una capa de atención por cada siete de Mamba.",
         no=["Esa es la idea que se volvió cara con textos larguísimos.",
             "Usan versiones modernas de la recurrencia, que se entrenan en paralelo.",
             "Siguen siendo redes que aprenden de ejemplos.", None]),
    dict(q="Tienes el historial de pagos, mes a mes, de cada socio y quieres predecir la mora. Además de una línea base sencilla, ¿qué suposición conviene que haga tu modelo?",
         options=["Que el orden de los meses importa (una red para secuencias)", "Que lo cercano en una foto importa (una CNN de imágenes)", "Que los datos no tienen ninguna estructura", "Que hay que generar socios nuevos (una GAN)"],
         ok=0, tema="b04", mide="Elegir la arquitectura según la estructura de los datos.", fig="orden",
         why="Un socio que empeora y uno que mejora pueden tener los mismos meses en distinto orden (el mismo promedio). Una red para secuencias (RNN, LSTM o atención) usa el orden; en el NB04 el promedio adivina (48 %) y la RNN acierta (100 %).",
         no=[None, "Un historial no es una foto: no hay vecinos en dos dimensiones.",
             "Sí la tienen: los meses vienen en orden, y ese orden distingue a los que empeoran.",
             "Una GAN sirve para generar datos nuevos, no para predecir la mora."]),
]

FIGS = ("pixels", "orden", "keras", "suposicion", "filtro", "share", "libreta", "atencion", "olvido", "costo", "pool", "lstm", "hibrido")


def _check():
    for name, bank in (("PRE", PRE), ("FINAL", FINAL)):
        for q in bank:
            assert len(q["options"]) == 4 and 0 <= q["ok"] < 4, q["q"]
            assert q["tema"] in TEMAS and q.get("clave", "C1") in CLAVES, q["q"]
            assert len(q["no"]) == 4 and q["no"][q["ok"]] is None and all(q["no"][j] for j in range(4) if j != q["ok"]), q["q"]
            assert q.get("fig") in (None,) + FIGS, q["q"]
        keys = [q["clave"] for q in bank if "clave" in q]
        assert sorted(keys) == sorted(CLAVES), (name, keys)
    assert len(PRE) == 8 and len(FINAL) == 10


_check()
