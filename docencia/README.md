# Docencia · Semana 1

Panel del profesor: abre **[deeplearningweek1.vercel.app/docencia/](https://deeplearningweek1.vercel.app/docencia/)**.

| Archivo | Para qué |
|---|---|
| `index.html` | El panel: slides, código en Colab, guías y herramientas |
| `Guia_docente.html` | El orden de todo, plan minuto a minuto, apuntes, preguntas probables y claves |
| `Slides_Clase1.pdf` | Las 78 láminas (el deck editable está en claude.ai) |
| `Resultados_quiz.html` | Pegas el chat de Teams y ves el antes y el después de los quizzes |
| `Seguimiento_grupos.xlsx` | Avance de cada grupo en el NB03, rúbrica y notas de sala |
| `Logistica_y_encuesta.pdf` | Checklist, encuesta de tendencia y pendientes |
| `codigo_fuente/` | El código que genera notebooks, páginas y quizzes (para la semana 2) |

Las **soluciones** de los notebooks no están aquí: el repositorio es público. Viven en la carpeta `Soluciones_privadas` del profesor.

## Regenerar (Python 3.10+ con `nbformat`, `nbclient`, `openpyxl`)

Desde `docencia/codigo_fuente/sitio/`:

```bash
python build_quiz.py     ../../..  ../..
python build_inicio.py   ../../..
python build_guia.py     ../../..
python build_docente.py  ../..
python build_docencia.py ../..
```
