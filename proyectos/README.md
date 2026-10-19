# Proyectos · Semana 1

Tres notebooks para abrir en Google Colab. Los enlaces directos están en la [página de inicio](https://deeplearningweek1.vercel.app/#proyectos).

| Notebook | Cuándo | Qué haces | Abrir |
|---|---|---|---|
| `NB01_viernes_tu_primera_neurona.ipynb` | Viernes | 8 tareas y el **Mini-reto 1** (tu comité de crédito) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/NB01_viernes_tu_primera_neurona.ipynb) |
| `NB02_sabado_tu_primera_red.ipynb` | Sábado | 6 tareas y el **Mini-reto 2** (los círculos) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/NB02_sabado_tu_primera_red.ipynb) |
| `NB03_miniproyecto_cooperativa_starter.ipynb` | En grupo, entrega el martes 27 | **Mini-proyecto**: riesgo de mora en una cooperativa | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AndresOrdonez369/deepLearningWeek1/blob/main/proyectos/NB03_miniproyecto_cooperativa_starter.ipynb) |

Para correrlos en tu computador en vez de Colab: `pip install -r requirements.txt` (Python 3.10 o superior).

---

## Datos del mini-proyecto · Cooperativa “Valle Andino” (ficticia)

`cooperativa_ficticia_mora.csv` tiene **8 000 socios** (filas) y **14 columnas**: 13 variables y la variable objetivo `mora_30d`. El **12.7 %** de los socios cae en mora de más de 30 días.

> Los datos son **100 % sintéticos**: se generaron con una simulación para este curso. Cualquier parecido con una institución o persona real es coincidencia.

| Variable | Tipo | Descripción | Rango o valores |
|---|---|---|---|
| `edad` | entero | Edad del socio, en años | 19 a 75 |
| `provincia` | categórica | Provincia de la agencia | Azuay, Chimborazo, Cotopaxi, El Oro, Guayas, Imbabura, Loja, Manabí, Pichincha, Tungurahua |
| `zona` | categórica | Zona donde vive | `urbana`, `rural` |
| `sector` | categórica | Actividad económica principal | agricultura, artesania, comercio, manufactura, servicios, transporte |
| `ingreso_mensual` | USD | Ingreso mensual declarado | 87 a 3 086 (mediana 577) |
| `monto_credito` | USD | Monto desembolsado | 300 a 40 000 (mediana 2 650) |
| `plazo_meses` | entero | Plazo del crédito | 6, 12, 18, 24, 36 o 48 |
| `cuota_mensual` | USD | Cuota fija mensual (tasa anual ficticia de 18 %) | 11 a 2 080 (mediana 166) |
| `antiguedad_socio_meses` | entero | Meses como socio de la cooperativa | 0 a 345 |
| `creditos_previos` | entero | Créditos anteriores en la cooperativa | 0 a 18 |
| `atrasos_previos_12m` | entero | Atrasos registrados en los últimos 12 meses | 0 a 4 |
| `tiene_garante` | 0/1 | El crédito tiene garante | 0 = no, 1 = sí |
| `ahorro_promedio` | USD | Saldo promedio de ahorro | 27 a 30 430 |
| **`mora_30d`** | **0/1** | **Objetivo:** el socio cayó en mora de más de 30 días | 0 = pagó al día, 1 = mora |

No hace falta descargarlo a mano: la sección 1 del NB03 lo lee de esta carpeta. Si trabajas sin internet, súbelo al panel de archivos de Colab (icono de carpeta, a la izquierda). En el notebook, las 3 variables categóricas se convierten en 18 columnas *one-hot*; junto con las 10 numéricas, la red recibe **28 entradas**.
