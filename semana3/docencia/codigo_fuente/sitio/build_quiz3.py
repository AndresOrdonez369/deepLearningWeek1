"""Week 3: build the Kahoot-style web quiz (semana3/quiz/index.html) and the teacher results panel.

usage: python build_quiz3.py <repo_root>
  <repo_root>/semana3/quiz/index.html               pre-quiz and final quiz (students)
  <repo_root>/semana3/docencia/Resultados_quiz.html  paste the chat codes (tag DL3), see before vs after (teacher)
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from banco3 import PRE, FINAL, TEMAS, CLAVES

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
SITE, TEACHER = ROOT / 'semana3', ROOT / 'semana3' / 'docencia'

# only these fields reach the students' page (mide is for the teacher guide)
KEEP = ("q", "options", "ok", "why", "no", "fig", "tema", "clave")
bank = {
    "pre": {"title": "Pre-quiz · ¿de dónde partimos?", "time": 20,
            "sub": "Ocho preguntas cortas, sin cuentas: tres de calentamiento (semanas 1 y 2) y las cinco ideas clave de la semana 3 (memorizar, frenos, robustez, transfer learning y explicaciones). No es nota: es tu punto de partida. Es normal no saberlas todas.",
            "questions": [{k: q[k] for k in KEEP if k in q} for q in PRE]},
    "final": {"title": "Quiz final · ¿cuánto avanzamos?", "time": 25,
              "sub": "Diez preguntas cortas, sin cuentas, sobre toda la semana: las curvas del sobreajuste, el dropout, los ejemplos adversariales, el aumento de datos, afinar con el simulacro, transfer learning, la prueba de cordura, el contrafactual, la mirada por grupo y las reglas que llegan. Las cinco ideas clave del pre-quiz vuelven con otra versión.",
              "questions": [{k: q[k] for k in KEEP if k in q} for q in FINAL]},
}


def fill(template):
    tpl = (HERE / template).read_text()
    return (tpl.replace('__BANK__', json.dumps(bank, ensure_ascii=False))
               .replace('__TEMAS__', json.dumps(TEMAS, ensure_ascii=False))
               .replace('__CLAVES__', json.dumps(CLAVES, ensure_ascii=False)))


(SITE / 'quiz').mkdir(parents=True, exist_ok=True)
(SITE / 'quiz' / 'index.html').write_text(fill('quiz_template3.html'))
TEACHER.mkdir(parents=True, exist_ok=True)
(TEACHER / 'Resultados_quiz.html').write_text(fill('resultados_template3.html'))
print('week-3 quiz and results panel built')
