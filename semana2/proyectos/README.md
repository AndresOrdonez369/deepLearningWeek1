# Proyectos en clase · Semana 2

Dos notebooks para abrir en Google Colab durante la clase. **No tienen nota y no hay que programar nada para avanzar**: todo el código ya está escrito y comentado. Tú lees, predices qué va a salir, ejecutas y comparas. Los enlaces directos están en la [página de la semana 2](https://deeplearningweek1.vercel.app/semana2/#proyectos).

| Notebook | Cuándo | Qué haces | Abrir |
|---|---|---|---|
| `NB03_viernes_tu_primera_cnn.ipynb` | Viernes 6 | Una imagen como tabla de números (Fashion-MNIST), un filtro de 3 × 3 a mano, una red densa contra una **red convolucional (CNN)** con las mismas reglas, los filtros que aprendió la red, y dos pruebas de la suposición de cada arquitectura: mover la prenda 2 píxeles y mezclar los píxeles. Cierra con **Para comprobar que entendiste** y el **Experimento 3 (opcional): ¿cuántos filtros necesita?** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana2/proyectos/NB03_viernes_tu_primera_cnn.ipynb) |
| `NB04_sabado_redes_que_recuerdan.ipynb` | Sábado 7 | Una secuencia como tabla con orden, la libreta de una **RNN** calculada a mano (y cómo se olvida), el orden importa (promedio contra RNN), el examen de memoria con **SimpleRNN** y **LSTM** de 10, 30 y 80 pasos, y la **atención**: mirar directo al paso importante y un cálculo a mano con tres palabras. Cierra con **Para comprobar que entendiste** y el **Experimento 4 (opcional): 50 pasos y dos semillas** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/semana2/proyectos/NB04_sabado_redes_que_recuerdan.ipynb) |

### Cómo usarlos

1. Clic en **Open in Colab** y entra con tu cuenta de Google.
2. **Archivo → Guardar una copia en Drive**; si no, tus cambios se pierden al cerrar la pestaña.
3. Ejecuta primero la celda **Configuración** y luego sigue en orden con `Shift + Enter`.
4. Cada sección sigue el mismo orden: qué vas a hacer → la necesidad → ejemplo → el nombre → la fórmula («Léelo así») → **Qué hace este código** → **🔮 Antes de ejecutar: ¿qué crees que saldrá?** → ejecuta → **Qué deberías ver** (con los números de nuestra corrida) → **💭 Para pensar** (las respuestas están plegadas en «Ver respuesta»).
5. Las celdas **🧪 Experimenta** son opcionales: cambia el único valor marcado (por ejemplo `filtros = 16   # try 4`) y vuelve a ejecutar.
6. Si algo falla, cada notebook tiene al inicio un recuadro **🛟 Si algo falla**.

Cada notebook tarda alrededor de 2 minutos en ejecutarse completo en Colab (CPU). Se publican ya ejecutados, así que puedes ver todas las salidas y gráficas antes de correrlos.

Para correrlos en tu computador en vez de Colab: `pip install -r requirements.txt` (Python 3.10 o superior).

Las fotos son del conjunto público Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017), que Keras descarga solo. Los historiales de pago y las secuencias del NB04 son ficticios y se generaron solo con fines educativos.
