"""Build the Kahoot-style web quiz (quiz/index.html) and the teacher results panel.

usage: python build_quiz.py <site_folder> <teacher_folder>
  <site_folder>/quiz/index.html          pre-quiz and final quiz (students)
  <teacher_folder>/Resultados_quiz.html  paste the chat codes, see before vs after (teacher)
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from banco import PRE, FINAL, TEMAS, CLAVES

HERE = pathlib.Path(__file__).parent
SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
TEACHER = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'out_profesor')

KEEP = ("q", "options", "ok", "why", "no", "fig", "tema", "clave")
bank = {
    "pre": {"title": "Pre-quiz · ¿de dónde partimos?", "time": 20,
            "sub": "Ocho preguntas cortas, sin cuentas: tres de calentamiento y cinco ideas clave que veremos esta semana. No es nota: es tu punto de partida. Es normal no saberlas todas.",
            "questions": [{k: q[k] for k in KEEP if k in q} for q in PRE]},
    "final": {"title": "Quiz final · ¿cuánto avanzamos?", "time": 25,
              "sub": "Diez preguntas cortas, sin cuentas, sobre toda la semana: la neurona, la activación, XOR, la pérdida, el gradiente, la retropropagación, Keras y las métricas. Las cinco ideas clave del pre-quiz vuelven con otra versión.",
              "questions": [{k: q[k] for k in KEEP if k in q} for q in FINAL]},
}

def fill(template):
    tpl = (HERE / template).read_text()
    return (tpl.replace('__BANK__', json.dumps(bank, ensure_ascii=False))
               .replace('__TEMAS__', json.dumps(TEMAS, ensure_ascii=False))
               .replace('__CLAVES__', json.dumps(CLAVES, ensure_ascii=False)))

(SITE / 'quiz').mkdir(parents=True, exist_ok=True)
(SITE / 'quiz' / 'index.html').write_text(fill('quiz_template.html'))
TEACHER.mkdir(parents=True, exist_ok=True)
(TEACHER / 'Resultados_quiz.html').write_text(fill('resultados_template.html'))
print('quiz and results panel built')
