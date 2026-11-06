"""Question bank of week 3 for the Kahoot-style web quizzes (pre and final).
Single source for semana3/quiz/index.html, the teacher results panel and the teacher guide answer key.

Design (same as weeks 1 and 2): the five KEY IDEAS of the week (clave C1..C5) appear in BOTH quizzes as parallel items
(same idea, different words or context). Comparing them shows how much the group moved on each idea.
The pre-quiz adds three simple base items (recap of weeks 1 and 2); the final adds five more items about the week.
No calculations: every item is answered by understanding the idea. All numbers are the real NB05/NB06 runs (DISENO3.md)."""

# tema keys map to study-guide anchors (semana3/guia/index.html#rec, #b01 ...)
TEMAS = {
    "rec": "Recorderis · semanas 1 y 2",
    "b01": "Tema 1 · Aprender sin memorizar",
    "b02": "Tema 1 · Robustez y afinar sin trampa",
    "b03": "Tema 2 · Transfer learning",
    "b04": "Tema 2 · Explicar y verificar",
    "b05": "Cierre · ¿Le creerías a tu red?",
}

CLAVES = {
    "C1": "Aprender no es memorizar (sobreajuste)",
    "C2": "Regularizar: frenos para la memoria",
    "C3": "Exacto no es robusto",
    "C4": "Transfer learning: reutilizar lo aprendido",
    "C5": "Una explicación también se pone a prueba",
}

# Each item: q, options (4), ok (index), tema, clave (optional), mide (teacher only) and, shown to students after answering:
#   why · why the right answer is right, in plain words (uses the week's analogies)
#   no  · one short line per option: why that wrong option is tempting but wrong (None for the right one)
#   fig · optional key of a mini drawing in quiz_template3.html
PRE = [
    dict(q="En las semanas 1 y 2 separamos los datos en entrenamiento, validación y prueba. ¿Para qué sirve la validación?",
         options=["Es el simulacro: mide cómo va la red con datos que no estudió", "Es lo único con lo que la red aprende", "Sirve para calcular el sesgo de cada neurona", "Sube la nota del examen final"],
         ok=0, tema="rec", mide="Base (semanas 1 y 2): entrenamiento, validación (simulacro) y prueba (examen final).", fig="simulacro",
         why="La red estudia con el entrenamiento. La validación es el simulacro: ejemplos que no usa para aprender y que dicen si le va bien con casos nuevos. El examen final (la prueba) se usa una sola vez, al terminar.",
         no=[None, "La red aprende solo con el entrenamiento; la validación no cambia ningún peso.",
             "El sesgo es un peso más y se aprende con el entrenamiento.",
             "La validación solo mide; no cambia el examen final."]),
    dict(q="¿Qué hace el descenso de gradiente con cada peso de la red?",
         options=["Lo borra si es pequeño", "Lo duplica en cada época", "Lo mueve un poquito en la dirección en que baja la pérdida", "Lo deja fijo y cambia los datos"],
         ok=2, tema="rec", mide="Base (semana 1): el gradiente mueve los pesos cuesta abajo en la pérdida (prepara FGSM: cuesta arriba).", fig="montana",
         why="Es bajar el Cotopaxi con neblina: la pendiente dice hacia dónde sube la pérdida y damos un paso en contra, de largo η. Esta semana haremos lo contrario con la foto: subir la montaña a propósito para engañar a la red.",
         no=["Ningún peso se borra: todos se corrigen un poco en cada paso.",
             "Los pasos son pequeños (η); duplicar haría saltar la pérdida.", None,
             "Al entrenar, los datos quedan fijos y se mueven los pesos. (Esta semana veremos qué pasa si movemos la foto.)"]),
    dict(q="La CNN de la semana 2 llegó a 87.7 % con 12 810 parámetros. ¿Qué supone sobre las fotos?",
         options=["Que el orden en el tiempo es lo más importante", "Que todos los píxeles se relacionan con todos por igual", "Que las fotos nunca cambian", "Que lo cercano importa y el mismo patrón puede aparecer en cualquier parte"],
         ok=3, tema="rec", mide="Base (semana 2): la suposición de la CNN (es la red que usamos toda la semana 3).", fig="suposicion",
         why="Es la lupa que recorre la foto: mira vecindarios pequeños y usa el mismo filtro en todas partes. Esta semana usamos esa misma CNN para ver si funciona con casos nuevos y si podemos explicar lo que decide.",
         no=["Esa es la suposición de la RNN: el orden importa.", "Esa es la de la red densa: todo con todo.",
             "No es una suposición de la CNN; justo esta semana vemos qué pasa cuando las fotos cambian.", None]),
    dict(q="Una red acierta el 97 % de las fotos con las que estudió y el 83 % de fotos que nunca vio. ¿Qué está pasando?",
         options=["Está memorizando: se aprendió las fotos de estudio más que la idea", "Todo está perfecto: 97 % es excelente", "Le faltan épocas: hay que entrenar mucho más", "Las fotos nuevas están mal etiquetadas"],
         ok=0, tema="b01", clave="C1", mide="Idea clave 1 antes de la clase: distinguir aprender de memorizar (la brecha entre entrenamiento y validación).", fig="memoriza",
         why="Es el estudiante que se aprende de memoria el solucionario del examen pasado: saca casi 100 en los ejercicios que ya vio y falla los nuevos. Se llama sobreajuste. Son los números reales del NB05 con 1 000 fotos: 96.7 % y 83.0 %.",
         no=[None, "El número que importa es el de las fotos nuevas; el de estudio puede engañar.",
             "Más épocas lo empeoran: sigue memorizando y el simulacro baja.",
             "Las etiquetas están bien; la diferencia aparece porque la red memorizó."]),
    dict(q="¿Cuál de estas acciones ayuda a que una red NO memorice?",
         options=["Entrenar el doble de épocas", "Parar de entrenar cuando el simulacro empieza a empeorar", "Elegir el modelo mirando el examen final", "Agregar muchas más neuronas"],
         ok=1, tema="b01", clave="C2", mide="Idea clave 2 antes de la clase: regularizar (parar a tiempo como freno para la memoria).", fig="frenos",
         why="Es dejar de estudiar cuando el simulacro empieza a salir peor: se llama early stopping. Junto con el aumento de datos y el dropout son frenos para la memoria. Y el mejor freno de todos: más datos.",
         no=["Más épocas son más tiempo para memorizar.", None,
             "Elegir mirando el examen final es hacer trampa: después ya no mide casos nuevos.",
             "Más neuronas son más memoria: suele empeorar el sobreajuste."]),
    dict(q="Una CNN acierta el 88 % de las fotos. A cada foto le sumamos un ruido tan pequeño que una persona no ve ninguna diferencia. ¿Qué puede pasar?",
         options=["Nada: si una persona no lo ve, la red tampoco", "Su exactitud sube", "Puede caer muchísimo, si el ruido se eligió para engañarla", "La red deja de funcionar y da un error"],
         ok=2, tema="b02", clave="C3", mide="Idea clave 3 antes de la clase: exacto no es robusto (ejemplos adversariales).", fig="adversarial",
         why="Si el ruido se elige a propósito, en la dirección que más confunde a la red, la exactitud se desploma: en el NB05 pasa de 87.7 % a 39.2 % con un cambio de solo 0.05 en cada píxel. Se llaman ejemplos adversariales.",
         no=["La red no mira como nosotros: mira números, y muchos cambios pequeños se suman.",
             "Un ruido elegido para engañar nunca ayuda.", None,
             "No da error: responde con la misma seguridad, pero mal."]),
    dict(q="Tienes solo 20 fotos de tu problema. ¿Qué suele ayudar más?",
         options=["Entrenar una red enorme desde cero", "Partir de una red que ya aprendió de muchas fotos y ajustarla a tu problema", "Repetir las mismas 20 fotos mil veces", "Usar las 20 fotos como examen final"],
         ok=1, tema="b03", clave="C4", mide="Idea clave 4 antes de la clase: transfer learning ayuda con pocos datos.", fig="transfer",
         why="Es contratar a un profesional con experiencia y darle una inducción corta: la red ya sabe ver bordes y formas y solo aprende la última parte. Se llama transfer learning. En el NB06, con 5 fotos por clase: desde cero 30.6 %; partiendo de una red ya entrenada, cerca de 47 %.",
         no=["Con 20 fotos, una red enorme memoriza enseguida.", None,
             "Repetir las mismas fotos no trae información nueva: la red las memoriza.",
             "Sin fotos para estudiar, la red no aprende nada."]),
    dict(q="Una herramienta pinta un mapa de calor con las zonas de la foto que más influyeron en la decisión de la red. Ese mapa es…",
         options=["La prueba de que la red razona como una persona", "Una interpretación de la red, que también hay que poner a prueba", "Una foto nueva que inventó la red", "La lista de los pesos de la red"],
         ok=1, tema="b04", clave="C5", mide="Idea clave 5 antes de la clase: una explicación es una interpretación que se verifica.", fig="calor",
         why="Grad-CAM o la oclusión son interpretaciones: describen a la red desde afuera y pueden equivocarse, así que se verifican. Por ejemplo, con la prueba de cordura: borrar lo que la red aprendió y ver si el mapa cambia.",
         no=["Un mapa muestra dónde influyó, no cómo razona; y puede fallar.", None,
             "El mapa se calcula sobre la misma foto: no inventa una nueva.",
             "Los pesos son miles de números; el mapa es un resumen calculado a partir de ellos."]),
]

FINAL = [
    dict(q="En el NB05, con 1 000 fotos, la pérdida de entrenamiento baja hasta el final, pero la de validación es mínima en la época 33 y después sube. ¿Qué pasó desde la época 33?",
         options=["La red empezó a memorizar: aprende detalles de las fotos de estudio que no sirven con fotos nuevas", "La red dejó de aprender por completo", "El simulacro tenía errores", "Nada raro: siempre hay que entrenar hasta la última época"],
         ok=0, tema="b01", clave="C1", mide="Idea clave 1: leer las curvas (la validación sube mientras el entrenamiento baja).", fig="memoriza",
         why="Las dos curvas se separan: la de entrenamiento baja porque la red se aprende el solucionario; la de validación sube porque eso no sirve con fotos nuevas. Al final: 96.7 % en entrenamiento, 83.0 % en el simulacro y 80.9 % en el examen final.",
         no=[None, "Sigue aprendiendo, pero lo equivocado: la pérdida de entrenamiento todavía baja.",
             "El simulacro está bien: gracias a él nos damos cuenta.",
             "Seguir entrenando empeora el simulacro: conviene parar cerca de la mejor época."]),
    dict(q="¿Qué hace layers.Dropout(0.3) mientras la red entrena?",
         options=["Borra para siempre el 30 % de las neuronas", "Quita el 30 % de las fotos de entrenamiento", "En cada paso apaga al azar el 30 % de las neuronas de esa capa, para que ninguna dependa de otra", "Baja un 30 % el learning rate"],
         ok=2, tema="b01", clave="C2", mide="Idea clave 2: qué hace el dropout (un freno para la memoria).", fig="dropout",
         why="Es un equipo que entrena sabiendo que en cada partido puede faltar cualquiera: nadie puede depender de un solo compañero. Solo actúa al entrenar; al predecir trabajan todas. En el NB05, con aumento, dropout y early stopping, las curvas ya no se separan (81.6 % en el examen final).",
         no=["No borra nada para siempre: en cada paso apaga a otras al azar, y al predecir trabajan todas.",
             "Las fotos no se tocan: se apagan neuronas.", None,
             "El learning rate se elige en compile; Dropout no lo cambia."]),
    dict(q="¿Cómo se fabrica un ejemplo adversarial con FGSM?",
         options=["Se cambia cada píxel un poquito en la dirección en que más sube la pérdida", "Se toma una foto de otra clase", "Se borra la mitad de la foto", "Se entrena la red con fotos al revés"],
         ok=0, tema="b02", clave="C3", mide="Idea clave 3: qué es un ejemplo adversarial (FGSM: subir la montaña a propósito).", fig="adversarial",
         why="Es subir la montaña a propósito: en vez de mover los pesos cuesta abajo, movemos cada píxel un poquito cuesta arriba en la pérdida: x' = x + ε · signo(gradiente). Con ε = 0.05, el botín que la red veía al 96 % pasa a «zapatilla» con 67 %, y a la vista es la misma foto.",
         no=[None, "Una foto de otra clase no engaña: la red acierta que es otra prenda.",
             "Borrar media foto es un cambio enorme y visible; el adversarial es invisible.",
             "Eso cambia la red, no fabrica una foto engañosa."]),
    dict(q="En el NB06, una red que ya sabía de pantalones, calzado y bolsos aprende 4 prendas de arriba. ¿Cuándo ayudó más lo que ya sabía?",
         options=["Siempre igual, con cualquier cantidad de fotos", "Con 100 fotos por clase", "Nunca: desde cero siempre gana", "Con solo 5 fotos por clase: unos 15 puntos más"],
         ok=3, tema="b03", clave="C4", mide="Idea clave 4: transfer learning ayuda sobre todo con pocos datos.", fig="pocos",
         why="Con 5 fotos por clase: desde cero 30.6 %, congelada 45.9 % y con ajuste fino 47.2 %. Con 100 fotos por clase, desde cero ya empata (68.8 %). La experiencia heredada vale sobre todo cuando hay pocos datos.",
         no=["La ventaja depende de los datos: con 100 fotos casi desaparece.",
             "Con 100 fotos por clase, entrenar desde cero ya empata o gana (68.8 %).",
             "Con 5 fotos, desde cero queda muy atrás (30.6 % contra 47.2 %).", None]),
    dict(q="En la prueba de cordura del NB06 borramos lo que la red aprendió (pesos al azar). El mapa de gradiente × imagen casi no cambia (0.90 de parecido). ¿Qué concluyes?",
         options=["Que la red al azar aprendió lo mismo", "Que ese mapa no explica a la red: se parece a la foto misma", "Que gradiente × imagen es el mejor método", "Que Grad-CAM falla"],
         ok=1, tema="b04", clave="C5", mide="Idea clave 5: una explicación se verifica (prueba de cordura, Adebayo et al., 2018).", fig="cordura",
         why="Si la red ya no sabe nada y el mapa sigue igual, el mapa no venía de lo aprendido: dibujaba la foto. Es el traductor que sigue el tono de voz y no las palabras. Grad-CAM (−0.12) y la oclusión (−0.05) sí cambian: pasan la prueba.",
         no=["Con pesos al azar la red no sabe nada: adivina.", None,
             "Es justo el que no pasó la prueba.", "Grad-CAM sí la pasó: su mapa cambió por completo (−0.12)."]),
    dict(q="Si mueves la prenda 4 píxeles, la CNN normal cae a 28.2 %; entrenada con RandomTranslation (aumento de datos) aguanta 76.4 %. ¿Qué hizo el aumento?",
         options=["Agregó fotos de otras prendas", "Le mostró en cada época las mismas prendas movidas un poco: aprendió que moverse no cambia la clase", "Hizo la red más grande", "Borró las fotos difíciles"],
         ok=1, tema="b02", mide="Aumento de datos: robustez frente a fotos movidas, y su costo.", fig="aumento",
         why="Es practicar con la misma prenda movida un poco: así no te sorprende verla corrida. El precio: con las fotos sin mover baja de 87.7 % a 82.6 % con las mismas 5 épocas. Robustez a cambio de unos puntos.",
         no=["Las clases son las mismas; lo que cambia es la posición.", None,
             "La red es la misma; cambian las fotos que ve al estudiar.", "No borra nada: crea versiones movidas."]),
    dict(q="Pruebas 6 combinaciones de learning rate, número de filtros y dropout. ¿Con qué datos eliges la mejor?",
         options=["Con el examen final (la prueba): la que más acierte", "Con los datos de entrenamiento", "Con la validación (el simulacro); el examen final se usa una sola vez, al final", "Con la que tenga más parámetros"],
         ok=2, tema="b02", mide="Optimización de hiperparámetros: elegir con validación; la prueba se mide una sola vez.", fig="simulacro",
         why="Es afinar la guitarra con el simulacro, nunca con el examen final. En el NB05 la mejor en validación (86.8 %: learning rate 0.01, 32 filtros y dropout 0.3) dio 86.9 % en el examen final, medido una sola vez.",
         no=["Si eliges con el examen final, deja de medir casos nuevos: es hacer trampa.",
             "En entrenamiento gana la que más memoriza.", None,
             "Más parámetros no garantizan nada; se compara en validación."]),
    dict(q="A una socia (ficticia) la cooperativa le negó el crédito: probabilidad de mora 61 %. ¿Qué explicación le sirve más a ella?",
         options=["La lista de los pesos de la red", "Qué tendría que cambiar: sin sus 2 atrasos, su probabilidad bajaría a 12 %", "El AUC del modelo (0.80)", "Que así lo decidió el sistema"],
         ok=1, tema="b04", mide="Dos destinatarios de una explicación: el contrafactual le sirve a la persona afectada.", fig="contrafactual",
         why="Es un contrafactual: dice qué tendría que cambiar para que la aprueben. A ella no le sirve la contribución de cada variable, sino qué puede hacer. Otra salida: una cuota de unos $124 en vez de $144 (unos $20 menos al mes) bajaría su probabilidad a 48 %.",
         no=["Miles de números no le explican nada a nadie.", None,
             "El AUC mide al modelo con todos los socios; no dice nada de su caso.",
             "Esa respuesta ya no basta: en Ecuador puede pedir una explicación de la lógica del algoritmo."]),
    dict(q="El modelo rechaza al 8.9 % de los socios rurales y al 3.7 % de los urbanos. Sin la columna «rural»: 6.4 % y 5.6 %. ¿Cuál es la conclusión más honesta?",
         options=["Quitar la columna acerca las tasas con un costo pequeño, pero queda la pregunta de fondo: por qué la mora real es distinta", "Ya está resuelto: quitar la columna lo arregla todo", "El modelo es justo porque su AUC es bueno", "Hay que sacar a los socios rurales de los datos"],
         ok=0, tema="b05", mide="Ética: mirar el modelo por grupo; quitar una columna no responde la pregunta de fondo.", fig="zona",
         why="En los datos, la mora real es 15.5 % en lo rural y 9.5 % en lo urbano. Quitar la columna acerca las tasas de rechazo (el AUC baja de 0.80 a 0.79), pero la pregunta de qué es justo no tiene una respuesta solo técnica.",
         no=[None, "Las tasas se acercan, pero la pregunta de fondo sigue abierta.",
             "Un buen AUC no dice si trata a todos por igual: hay que mirar por grupo.",
             "Sacar a un grupo de los datos no lo trata mejor: lo deja fuera."]),
    dict(q="Según la lectura de tendencia, ¿qué cambió en Ecuador desde marzo de 2026 para las decisiones automatizadas sobre personas?",
         options=["Se prohibió usar inteligencia artificial", "Se exige que los modelos acierten el 100 %", "Solo aplica a empresas extranjeras", "Las personas afectadas pueden pedir una explicación de la lógica del algoritmo y la revisión de una persona"],
         ok=3, tema="b04", mide="Tendencia: la norma de la SPDP (marzo de 2026), la revisión humana y el derecho a una explicación.", fig="reglas",
         why="La norma de la Superintendencia de Protección de Datos Personales pide evaluaciones de impacto, revisión humana de las decisiones automatizadas con efectos jurídicos y el derecho a pedir una explicación de la lógica del algoritmo. «Así lo decidió el sistema» ya no basta.",
         no=["No prohíbe la IA: pone condiciones para usarla con personas.",
             "Ningún modelo acierta siempre; la norma pide explicar y revisar.",
             "Aplica a quien use IA para decidir sobre personas en Ecuador.", None]),
]

FIGS = ("simulacro", "montana", "suposicion", "memoriza", "frenos", "adversarial", "transfer", "calor",
        "dropout", "pocos", "cordura", "aumento", "contrafactual", "zona", "reglas")


def _check():
    for name, bank in (("PRE", PRE), ("FINAL", FINAL)):
        for q in bank:
            assert len(q["options"]) == 4 and 0 <= q["ok"] < 4, q["q"]
            assert q["tema"] in TEMAS and q.get("clave", "C1") in CLAVES, q["q"]
            assert len(q["no"]) == 4 and q["no"][q["ok"]] is None and all(q["no"][j] for j in range(4) if j != q["ok"]), q["q"]
            assert q.get("fig") in (None,) + FIGS, q["q"]
            assert q.get("mide"), q["q"]
        keys = [q["clave"] for q in bank if "clave" in q]
        assert sorted(keys) == sorted(CLAVES), (name, keys)
    assert len(PRE) == 8 and len(FINAL) == 10


_check()
