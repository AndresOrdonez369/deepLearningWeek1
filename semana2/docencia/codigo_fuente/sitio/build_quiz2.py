"""Week 2: build the Kahoot-style web quiz (semana2/quiz/index.html) and the teacher results panel.

usage: python build_quiz2.py <repo_root>
  <repo_root>/semana2/quiz/index.html               pre-quiz and final quiz (students)
  <repo_root>/semana2/docencia/Resultados_quiz.html  paste the chat codes (tag DL2), see before vs after (teacher)
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from banco2 import PRE, FINAL, TEMAS, CLAVES

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
SITE, TEACHER = ROOT / 'semana2', ROOT / 'semana2' / 'docencia'

KEEP = ("q", "options", "ok", "why", "no", "fig", "tema", "clave")
bank = {
    "pre": {"title": "Pre-quiz · ¿de dónde partimos?", "time": 20,
            "sub": "Ocho preguntas cortas, sin cuentas: tres de calentamiento y las cinco ideas clave de la semana 2 (imágenes, secuencias y atención). No es nota: es tu punto de partida. Es normal no saberlas todas.",
            "questions": [{k: q[k] for k in KEEP if k in q} for q in PRE]},
    "final": {"title": "Quiz final · ¿cuánto avanzamos?", "time": 25,
              "sub": "Diez preguntas cortas, sin cuentas, sobre toda la semana: la suposición de cada arquitectura, filtros y pooling, compartir pesos, la libreta de la RNN y la LSTM, la atención y su precio, los híbridos y cómo elegir. Las cinco ideas clave del pre-quiz vuelven con otra versión.",
              "questions": [{k: q[k] for k in KEEP if k in q} for q in FINAL]},
}


def fill(template):
    tpl = (HERE / template).read_text()
    return (tpl.replace('__BANK__', json.dumps(bank, ensure_ascii=False))
               .replace('__TEMAS__', json.dumps(TEMAS, ensure_ascii=False))
               .replace('__CLAVES__', json.dumps(CLAVES, ensure_ascii=False)))


(SITE / 'quiz').mkdir(parents=True, exist_ok=True)
(SITE / 'quiz' / 'index.html').write_text(fill('quiz_template2.html'))
TEACHER.mkdir(parents=True, exist_ok=True)
(TEACHER / 'Resultados_quiz.html').write_text(fill('resultados_template2.html'))
print('week-2 quiz and results panel built')
