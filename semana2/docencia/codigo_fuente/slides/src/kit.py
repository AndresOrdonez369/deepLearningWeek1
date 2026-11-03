"""Building blocks for the week-1 deck (HTML strings)."""
import html as _h
import segno

SITE = 'https://deeplearningweek1.vercel.app/'
SLIDES = []          # filled by slide()


def esc(s):
    return _h.escape(s, quote=True)


def slide(sid, title, body, notes, *, layout='', block='', group='', minutes=None, steps=None, label='', blockname=''):
    attrs = [f'id="{sid}"', f'class="slide {layout}"', f'data-title="{esc(title)}"', f'data-block="{block}"', f'data-group="{esc(group)}"']
    if minutes:
        attrs.append(f'data-min="{minutes}"')
    if steps:
        attrs.append(f'data-steps="{steps}"')
    if label:
        attrs.append(f'data-label="{esc(label)}"')
    if blockname:
        attrs.append(f'data-blockname="{esc(blockname)}"')
    SLIDES.append({'id': sid, 'title': title, 'block': block, 'group': group, 'minutes': minutes,
                   'html': f'<section {" ".join(attrs)}>\n{body}\n<aside class="notes">{notes}</aside>\n</section>'})


def head(title, lede='', tags=''):
    """Slide heading. Tags (key-idea badge, trend, time) ride at the end of the title line, never above it."""
    t = f' <span class="h-tags">{tags}</span>' if tags else ''
    l = f'<p class="lede">{lede}</p>' if lede else ''
    return f'<header class="s-head"><h2>{title}{t}</h2>{l}</header>'


ROLE = {'out': 'resultado', 'w': 'se aprende', 'x': 'dato', 'eta': 'tú lo eliges', 'num': '', 'op': ''}


def eq(parts, read='', steps=False, size=''):
    """An equation you can read: each term in its own cell with a plain-words label under it.
    parts: (tex, label, role) with role out | w (what the network learns) | x (data) | eta | num | op."""
    cells, k = [], 0
    for tex, lab, role in parts:
        sm = ''
        if lab:
            k += 1
            sm = f'<small data-step="{k}">{lab}</small>' if steps else f'<small>{lab}</small>'
        cells.append(f'<span class="et r-{role}"><span class="em"><m>{tex}</m></span>{sm}</span>')
    r = ''
    if read:
        r = (f'<p class="eq-read" data-step="{k + 1}"><b>Léelo así:</b> {read}</p>' if steps else
             f'<p class="eq-read"><b>Léelo así:</b> {read}</p>')
    st_ = f' style="font-size:{size}"' if size else ''
    return f'<div class="eqx"{st_}><div class="eq-row">{"".join(cells)}</div>{r}</div>'


def hist(year, text, step=None):
    """A small dated note: when this idea was born."""
    d = f' data-step="{step}"' if step else ''
    return f'<p class="hist"{d}><span class="y num">{year}</span><span>{text}</span></p>'


import keyword as _kw, re as _re
_PYKW = set(_kw.kwlist)
_TOK = _re.compile(r'(#.*$)|("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|(\b\d+(?:\.\d+)?(?:e-?\d+)?\b)|([A-Za-z_]\w*)|(\s+)|(.)')


def _py(line):
    out, i = [], 0
    for m in _TOK.finditer(line):
        cm, st_, nu, idf, sp, other = m.groups()
        if cm is not None:
            out.append(f'<span class="cm">{esc(cm)}</span>')
        elif st_ is not None:
            out.append(f'<span class="st">{esc(st_)}</span>')
        elif nu is not None:
            out.append(f'<span class="nu">{nu}</span>')
        elif idf is not None:
            rest = line[m.end():].lstrip()
            if idf in _PYKW:
                out.append(f'<span class="kw">{idf}</span>')
            elif rest.startswith('('):
                out.append(f'<span class="fn">{idf}</span>')
            else:
                out.append(esc(idf))
        else:
            out.append(esc(sp if sp is not None else other))
    return ''.join(out)


def code(src, hl='', cls='', style='', out=''):
    """Python code with syntax colours; hl = 'step:first-last;…' highlights lines as the presenter advances.
    out = optional printed output shown under the code."""
    lines = src.strip('\n').split('\n')
    body = ''.join(f'<span class="ln">{_py(l) or " "}</span>' for l in lines)
    o = f'<span class="out">{out}</span>' if out else ''
    s = f' style="{style}"' if style else ''
    d = f' data-demo="codehl" data-hl="{hl}"' if hl else ''
    return f'<pre class="code {cls}"{d}{s}>{body}{o}</pre>'


def key(n):
    return f'<span class="chip key">Idea clave {n}</span>'


def chip(s, kind=''):
    return f'<span class="chip {kind}">{s}</span>'


def st(n, inner, tag='div', cls='', style=''):
    c = f' class="{cls}"' if cls else ''
    s = f' style="{style}"' if style else ''
    return f'<{tag} data-step="{n}"{c}{s}>{inner}</{tag}>'


def demo(name, cls='fig', style='', **data):
    d = ' '.join(f'data-{k.replace("_", "-")}="{esc(str(v))}"' for k, v in data.items())
    s = f' style="{style}"' if style else ''
    return f'<div class="{cls}" data-demo="{name}" {d}{s}></div>'


def count(to, dec=0, at=0, frm=0, unit='', sign=False, cls='', ms=1100):
    return (f'<span class="num {cls}" data-demo="count" data-to="{to}" data-from="{frm}" data-dec="{dec}" data-at="{at}" '
            f'data-unit="{esc(unit)}" data-sign="{1 if sign else 0}" data-ms="{ms}">{to}</span>')


def qr(keyname, label=None):
    url = SITE + '?' + keyname
    q = segno.make(url, error='m')
    svg = q.svg_inline(dark='#07101c', light=None, border=1, omitsize=True)
    shown = label or (SITE.replace('https://', '').rstrip('/') + '/<br>?' + keyname)
    return f'<div class="qr">{svg}<div class="url">{shown}</div></div>'


def notes(*ps):
    return ''.join(f'<p>{p}</p>' for p in ps)


def move(sid, after):
    """Place slide sid right after slide 'after' (lets new slides live next to their neighbours' code)."""
    i = next(k for k, s in enumerate(SLIDES) if s['id'] == sid)
    s = SLIDES.pop(i)
    j = next(k for k, t in enumerate(SLIDES) if t['id'] == after)
    SLIDES.insert(j + 1, s)
