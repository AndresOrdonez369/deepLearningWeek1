"""Teacher tracking workbook for Week 1: groups' NB03 progress, rubric, quiz results, room notes."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as L

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'Seguimiento_grupos.xlsx')

F = 'Arial'
BLUE = '1D4ED8'; NAVY = '0B1220'; INPUT = 'FFF7D6'; EXFILL = 'EEF2F7'; HEAD = 'DCE6FB'
thin = Side(style='thin', color='C9D3E3'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
f_title = Font(name=F, size=16, bold=True, color=NAVY)
f_sub = Font(name=F, size=10, color='475569')
f_head = Font(name=F, size=10, bold=True, color=NAVY)
f_in = Font(name=F, size=10, color='0000FF')        # inputs: blue
f_calc = Font(name=F, size=10, color='000000')      # formulas: black
f_ex = Font(name=F, size=10, italic=True, color='64748B')
fill_in = PatternFill('solid', fgColor=INPUT); fill_head = PatternFill('solid', fgColor=HEAD)
fill_ex = PatternFill('solid', fgColor=EXFILL)
wrap = Alignment(wrap_text=True, vertical='top'); center = Alignment(horizontal='center', vertical='center', wrap_text=True)

wb = Workbook()

def header(ws, row, labels, widths=None):
    for i, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=t); c.font = f_head; c.fill = fill_head; c.alignment = center; c.border = BOX
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[L(i)].width = w
    ws.row_dimensions[row].height = 32

def title(ws, t, sub):
    ws['A1'] = t; ws['A1'].font = f_title
    ws['A2'] = sub; ws['A2'].font = f_sub
    ws.row_dimensions[1].height = 24

def cellfmt(c, kind):
    c.border = BOX
    if kind == 'in': c.font = f_in; c.fill = fill_in; c.alignment = wrap
    elif kind == 'calc': c.font = f_calc; c.alignment = center
    elif kind == 'ex': c.font = f_ex; c.fill = fill_ex; c.alignment = wrap
    elif kind == 'label': c.font = Font(name=F, size=10, bold=True); c.alignment = wrap

GROUPS = [f'G{i}' for i in range(1, 9)]

# ---------------------------------------------------------------- Léeme
ws = wb.active; ws.title = 'Léeme'
title(ws, 'Seguimiento · Semana 1 · Deep Learning UIDE', 'Solo profesor: descárgalo y llénalo en tu computador. Llénalo durante las salas del sábado y al calificar.')
rows = [
    ('Cómo se usa', ''),
    ('Celdas amarillas, texto azul', 'Las llenas tú (integrantes, avance, puntajes, notas).'),
    ('Texto negro sin relleno', 'Se calculan solas (porcentajes, totales, promedios). No las edites.'),
    ('Fila gris en cursiva', 'Ejemplo de cómo llenar cada hoja. Puedes borrarla o dejarla.'),
    ('', ''),
    ('Hojas', ''),
    ('Grupos', 'Integrantes, dataset y avance del NB03 por sección (S1–S9): elige ✔ / en curso / — en la lista. El % se calcula solo (en curso = media sección).'),
    ('Rúbrica', 'Puntaje por criterio (máx. 25, 15, 15, 10 y 5). El total sobre 70 se suma solo; una celda se pone roja si supera el máximo de su criterio.'),
    ('Quizzes', 'No van aquí: pega el chat en Resultados_quiz.html (misma carpeta) y verás el antes y el después de cada estudiante.'),
    ('Notas de sala', 'Una fila por visita a una sala: qué los bloqueaba y qué les sugeriste. Sirve para la socialización y para la retro.'),
    ('', ''),
    ('Secciones del NB03', ''),
    ('S1', 'Carga de datos'), ('S2', 'Exploración mínima'), ('S3', 'Partición y preprocesamiento sin fuga'),
    ('S4', 'Líneas base y métricas'), ('S5', 'Parte A · Perceptrón desde cero'), ('S6', 'Parte B · MLP con retropropagación (NumPy)'),
    ('S7', 'Parte C · El mismo MLP en Keras'), ('S8', 'Parte D · Experimentos de optimización'), ('S9', 'Evaluación final y umbral'),
    ('', ''),
    ('Meta en las salas (55 min)', 'Al salir de salas: S1–S5 y S7 avanzadas y un primer experimento de S8 (lámina 73). S6, el resto de S8 y S9 se terminan en casa (entrega el martes 27).'),
    ('Rúbrica', 'Provisional hasta recibir la institucional. Retroalimenta solo contenido de deep learning (formato y APA los revisa Titulación).'),
]
for i, (a, b) in enumerate(rows, 4):
    ws.cell(row=i, column=1, value=a); ws.cell(row=i, column=2, value=b)
    ws.cell(row=i, column=1).font = Font(name=F, size=10, bold=True, color=NAVY if b == '' else '000000')
    ws.cell(row=i, column=2).font = Font(name=F, size=10); ws.cell(row=i, column=2).alignment = wrap
    if b == '' and a: ws.cell(row=i, column=1).font = Font(name=F, size=12, bold=True, color=BLUE)
ws['A5'].fill = fill_in; ws['A5'].font = Font(name=F, size=10, bold=True, color='0000FF')
ws['A7'].fill = fill_ex; ws['A7'].font = f_ex
ws.column_dimensions['A'].width = 30; ws.column_dimensions['B'].width = 100

# ---------------------------------------------------------------- Grupos
ws = wb.create_sheet('Grupos')
title(ws, 'Grupos y avance del NB03', 'Elige en cada sección: ✔ (terminada) · en curso · — (sin empezar). El % cuenta «en curso» como media sección.')
cols = ['Grupo', 'Integrantes', 'Dataset'] + [f'S{i}' for i in range(1, 10)] + ['% avance', 'Próximo paso / comentario']
header(ws, 4, cols, [9, 38, 16] + [9] * 9 + [11, 44])
dv_sec = DataValidation(type='list', formula1='"✔,en curso,—"', allow_blank=True)
dv_ds = DataValidation(type='list', formula1='"Cooperativa,Propio"', allow_blank=True)
ws.add_data_validation(dv_sec); ws.add_data_validation(dv_ds)
ex = ['Ej.', 'Ana P., Luis M., Carla R., Diego T.', 'Cooperativa', '✔', '✔', '✔', '✔', 'en curso', '—', '—', '—', '—', None,
      'Revisar fuga: escalaron antes de partir']
r0 = 5
for j, v in enumerate(ex, 1):
    c = ws.cell(row=r0, column=j, value=v); cellfmt(c, 'ex')
for k, g in enumerate(GROUPS, r0 + 1):
    ws.cell(row=k, column=1, value=g); cellfmt(ws.cell(row=k, column=1), 'label')
    for j in list(range(2, 13)) + [14]:
        cellfmt(ws.cell(row=k, column=j), 'in')
last = r0 + len(GROUPS)
for k in range(r0, last + 1):
    rng = f'D{k}:L{k}'
    c = ws.cell(row=k, column=13, value=f'=(COUNTIF({rng},"✔")+0.5*COUNTIF({rng},"en curso"))/9')
    c.number_format = '0%'; cellfmt(c, 'calc')
    if k == r0: c.font = f_ex; c.fill = fill_ex
    for j in range(4, 13): ws.cell(row=k, column=j).alignment = center
    ws.row_dimensions[k].height = 30
dv_sec.add(f'D{r0}:L{last}'); dv_ds.add(f'C{r0}:C{last}')
ws.cell(row=last + 2, column=12, value='Promedio G1–G8').font = Font(name=F, size=10, bold=True)
c = ws.cell(row=last + 2, column=13, value=f'=AVERAGE(M{r0+1}:M{last})'); c.number_format = '0%'; cellfmt(c, 'calc')
ws.conditional_formatting.add(f'D{r0}:L{last}', CellIsRule(operator='equal', formula=['"✔"'], fill=PatternFill('solid', fgColor='D1FAE5')))
ws.conditional_formatting.add(f'D{r0}:L{last}', CellIsRule(operator='equal', formula=['"en curso"'], fill=PatternFill('solid', fgColor='FEF3C7')))
ws.freeze_panes = 'B5'

# ---------------------------------------------------------------- Rúbrica
ws = wb.create_sheet('Rúbrica')
title(ws, 'Rúbrica del mini-proyecto · 70 pts', 'Provisional. Escribe el puntaje de cada criterio; el total se suma solo. Rojo = supera el máximo del criterio.')
crit = ['Implementación técnica', 'Experimentación', 'Justificación', 'Integración al proyecto', 'Comunicación']
maxes = [25, 15, 15, 10, 5]
header(ws, 4, ['Grupo'] + crit + ['Total /70', 'Retroalimentación (solo contenido DL)'], [9, 16, 16, 16, 16, 16, 11, 60])
ws.cell(row=5, column=1, value='Máximo'); cellfmt(ws.cell(row=5, column=1), 'label')
for j, m in enumerate(maxes, 2):
    c = ws.cell(row=5, column=j, value=m); cellfmt(c, 'calc'); c.font = Font(name=F, size=10, bold=True)
c = ws.cell(row=5, column=7, value='=SUM(B5:F5)'); cellfmt(c, 'calc'); c.font = Font(name=F, size=10, bold=True)
ws.cell(row=5, column=8, value='Criterios en _docente/Guia_docente_y_apuntes.html → Seguimiento').font = f_sub
exr = ['Ej.', 22, 12, 11, 8, 4, None, 'Gradient check aprobado y Keras corre. Falta justificar por qué PR-AUC y no exactitud.']
for j, v in enumerate(exr, 1):
    c = ws.cell(row=6, column=j, value=v); cellfmt(c, 'ex')
    if j in range(2, 7): c.alignment = center
for k, g in enumerate(GROUPS, 7):
    ws.cell(row=k, column=1, value=g); cellfmt(ws.cell(row=k, column=1), 'label')
    for j in range(2, 7): c = ws.cell(row=k, column=j); cellfmt(c, 'in'); c.alignment = center
    cellfmt(ws.cell(row=k, column=8), 'in')
last = 6 + len(GROUPS)
for k in range(6, last + 1):
    c = ws.cell(row=k, column=7, value=f'=IF(COUNT(B{k}:F{k})=0,"",SUM(B{k}:F{k}))'); cellfmt(c, 'calc')
    if k == 6: c.font = f_ex; c.fill = fill_ex
    ws.row_dimensions[k].height = 30
dv_pts = DataValidation(type='decimal', operator='between', formula1='0', formula2='25', allow_blank=True)
ws.add_data_validation(dv_pts); dv_pts.add(f'B6:F{last}')
for j in range(2, 7):
    col = L(j)
    ws.conditional_formatting.add(f'{col}6:{col}{last}', FormulaRule(formula=[f'AND(ISNUMBER({col}6),{col}6>{col}$5)'],
                                  fill=PatternFill('solid', fgColor='FECACA'), font=Font(name=F, color='B91C1C', bold=True)))
ws.cell(row=last + 2, column=6, value='Promedio G1–G8').font = Font(name=F, size=10, bold=True)
c = ws.cell(row=last + 2, column=7, value=f'=IFERROR(AVERAGE(G7:G{last}),"")'); cellfmt(c, 'calc'); c.number_format = '0.0'
ws.freeze_panes = 'B6'

# ---------------------------------------------------------------- Notas de sala
ws = wb.create_sheet('Notas de sala')
title(ws, 'Notas de sala', 'Una fila por visita. Tres preguntas por sala: ¿qué datos? ¿qué métrica y por qué? ¿partieron antes de escalar?')
header(ws, 4, ['Fecha', 'Hora', 'Grupo', 'Sección NB03', 'Bloqueo detectado', 'Qué les sugeriste', '¿Resuelto?'], [12, 9, 9, 12, 46, 46, 11])
dv_s = DataValidation(type='list', formula1='"' + ','.join(f'S{i}' for i in range(1, 10)) + '"', allow_blank=True)
dv_ok = DataValidation(type='list', formula1='"Sí,No,En casa"', allow_blank=True)
dv_g2 = DataValidation(type='list', formula1='"' + ','.join(GROUPS) + '"', allow_blank=True)
for d in (dv_s, dv_ok, dv_g2): ws.add_data_validation(d)
exn = ['24/10/2026', '10:52', 'G3', 'S3', 'Cambiaron el escalado y lo ajustaron con todo el dataset (fuga).', 'Volver a ajustar el escalador solo con train, como venía en el NB03 (sección 3).', 'Sí']
for j, v in enumerate(exn, 1):
    c = ws.cell(row=5, column=j, value=v); cellfmt(c, 'ex')
for k in range(6, 46):
    for j in range(1, 8): cellfmt(ws.cell(row=k, column=j), 'in')
dv_g2.add('C5:C45'); dv_s.add('D5:D45'); dv_ok.add('G5:G45')
ws.freeze_panes = 'A5'

for w in wb.worksheets:
    w.sheet_view.showGridLines = False
    w.page_setup.orientation = 'landscape'; w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.fitToWidth = 1; w.page_setup.fitToHeight = 0
wb.save(OUT)
print('saved', OUT)
