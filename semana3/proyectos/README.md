# Proyectos en clase · Semana 3

Dos notebooks para abrir en Google Colab durante la clase. **No tienen nota y no hay que programar nada para avanzar**: todo el código ya está escrito y comentado. Tú lees, predices qué va a salir, ejecutas y comparas. Al final de cada uno hay **✍️ Ejercicios** que se responden leyendo tus resultados y pensando. Los enlaces directos están en la [página de la semana 3](https://deeplearningweek1.vercel.app/semana3/#proyectos).

| Notebook | Tema | Qué haces | Abrir |
|---|---|---|---|
| `NB05_generalizar_y_robustez.ipynb` | Tema 1 · ¿Funcionará con casos nuevos? | El estudiante que memoriza: la CNN de siempre con solo 1 000 fotos y las curvas del **sobreajuste**; tres **frenos** (aumento de datos, dropout y parar a tiempo) y la lección de que más datos ayudan más; el aumento de datos contra fotos **movidas**; un **ejemplo adversarial** hecho a mano con `tf.GradientTape` (FGSM) y la red **vacunada** con entrenamiento adversarial; y una **búsqueda al azar de hiperparámetros** juzgada con el simulacro. Cierra con **Ejercicios**, **Para comprobar que entendiste** y el **Experimento 5 (opcional): ¿cuántas fotos hacen falta?** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana3/proyectos/NB05_generalizar_y_robustez.ipynb) |
| `NB06_reutilizar_y_explicar.ipynb` | Tema 2 · Reutilizar y explicar | **Transfer learning** con 5, 20 y 100 fotos por clase (desde cero, congelar y ajuste fino); **¿dónde miró la red?** con oclusión, Grad-CAM y gradiente × imagen escritos a mano; la **prueba de cordura** con una red de pesos al azar; y una **cooperativa ficticia**: importancia por permutación, **SHAP** para la socia rechazada, el **contrafactual** que le sirve a ella y las tasas **por zona**, con y sin la columna rural. Cierra con **Ejercicios**, **Para comprobar que entendiste** y el **Experimento 6 (opcional): ¿dónde pones la raya?** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana3/proyectos/NB06_reutilizar_y_explicar.ipynb) |

### Cómo usarlos

1. Clic en **Open in Colab** y entra con tu cuenta de Google.
2. **Archivo → Guardar una copia en Drive**; si no, tus cambios se pierden al cerrar la pestaña.
3. Ejecuta primero la celda **Configuración** y luego sigue en orden con `Shift + Enter`.
4. Cada sección sigue el mismo orden: qué vas a hacer → la necesidad → ejemplo → el nombre → la fórmula («Léelo así») → **Qué hace este código** → **🔮 Antes de ejecutar: ¿qué crees que saldrá?** → ejecuta → **Qué deberías ver** (con los números de nuestra corrida) → **💭 Para pensar** (las respuestas están plegadas en «Ver respuesta»).
5. Las celdas **🧪 Experimenta** son opcionales: cambia el único valor marcado (por ejemplo `n_fotos = 1000   # try 3000`) y vuelve a ejecutar.
6. Si algo falla, cada notebook tiene al inicio un recuadro **🛟 Si algo falla**.

En Colab (CPU), el NB05 tarda unos 4 minutos en ejecutarse completo y el NB06 unos 2. Se publican ya ejecutados, así que puedes ver todas las salidas y gráficas antes de correrlos. El NB06 usa la librería `shap`; si Colab no la tiene, la celda la instala sola.

Para correrlos en tu computador en vez de Colab: `pip install -r requirements.txt` (Python 3.10 o superior).

Las fotos son del conjunto público Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017), que Keras descarga solo. La cooperativa, sus 6 000 socios y «la socia» del NB06 son **ficticios**: se generaron con código, dentro del propio notebook, solo con fines educativos.
