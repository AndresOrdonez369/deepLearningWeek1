# Docencia · Semana 1

Panel del profesor: abre **[deeplearningweek1.vercel.app/docencia/](https://deeplearningweek1.vercel.app/docencia/)**.

| Archivo | Para qué |
|---|---|
| `index.html` | El panel: slides, mapas, código en Colab, guía y resultados |
| `slides/` | Las slides interactivas (HTML). Tecla **P**: vista del presentador con notas y reloj · **G**: índice · **F**: pantalla completa |
| `mapas/` | Mapas conceptuales de la semana y de cada bloque: qué decir, ejemplo, pregunta y error frecuente. Se imprimen en A4 |
| `Guia_docente.html` | El orden de todo, el plan minuto a minuto, apuntes, preguntas probables y claves |
| `Slides_Semana1.pdf` | Las slides en PDF, de respaldo (todas las demos en su estado final) |
| `Resultados_quiz.html` | Pegas el chat de Teams y ves el antes y el después de los quizzes |
| `codigo_fuente/` | El código que genera notebooks, páginas, quizzes, slides y mapas (para la semana 2) |

Las **soluciones** de los notebooks no están aquí: el repositorio es público. Viven en la carpeta `Soluciones_privadas` del profesor.

## Regenerar

Páginas y quizzes (Python 3.10+ con `nbformat` y `nbclient`), desde `docencia/codigo_fuente/sitio/`:

```bash
python build_quiz.py     ../../..  ../..
python build_inicio.py   ../../..
python build_guia.py     ../../..
python build_docencia.py ../..
python build_docente.py  ../..
```

Slides y mapas (Python 3.12+ con `segno`, y Node 18+), desde `docencia/codigo_fuente/slides/`:

```bash
cd fonts && npm install && cd ..
python src/build_deck.py   ../../slides
python maps/build_mapas.py ../../mapas ../../slides/slides.json
```

Después de cambiar las slides, vuelve a correr `build_docencia.py` y `build_docente.py`: leen los números de lámina de `slides/slides.json`.
