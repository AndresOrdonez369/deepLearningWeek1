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
    t = f'<div class="tags">{tags}</div>' if tags else ''
    l = f'<p class="lede">{lede}</p>' if lede else ''
    return f'<header class="s-head">{t}<h2>{title}</h2>{l}</header>'


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
