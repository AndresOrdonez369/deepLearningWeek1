"""Layout audit: every slide at its last step. Reports code that overflows, content below the safe bottom edge,
wrapped equations and console errors.  usage: python audit.py <index.html> [ids...]"""
import sys, asyncio, json, pathlib
from playwright.async_api import async_playwright
src = pathlib.Path(sys.argv[1]).resolve(); only = sys.argv[2:]
JS = r"""(i) => {
  const s = document.querySelectorAll('section.slide')[i], out = [];
  const sr = s.getBoundingClientRect(), bottom = sr.top + 1080 - 24, right = sr.left + 1920 - 40;
  s.querySelectorAll('pre.code').forEach(p => { if (p.scrollWidth > p.clientWidth + 2) out.push('code overflow +' + (p.scrollWidth - p.clientWidth) + 'px: ' + p.textContent.slice(0, 40)); });
  s.querySelectorAll('.eq-row').forEach(r => { const cs = [...r.children].map(c => c.getBoundingClientRect().top); if (Math.max(...cs) - Math.min(...cs) > 8) out.push('equation wraps: ' + r.textContent.slice(0, 40)); });
  s.querySelectorAll('*').forEach(e => {
    if (e.closest('aside.notes') || e.closest('[aria-hidden]')) return;
    const st = getComputedStyle(e); if (st.visibility === 'hidden' || st.display === 'none' || +st.opacity === 0) return;
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
    if (r.bottom > bottom + 1 && !(e.parentElement && e.parentElement.getBoundingClientRect().bottom > bottom + 1)) out.push('below edge by ' + Math.round(r.bottom - bottom) + 'px: <' + e.tagName.toLowerCase() + ' class="' + e.className.baseVal + e.className + '"> ' + (e.textContent || '').trim().slice(0, 40));
    if (r.right > right + 1 && !(e.parentElement && e.parentElement.getBoundingClientRect().right > right + 1)) out.push('right of edge by ' + Math.round(r.right - right) + 'px: <' + e.tagName.toLowerCase() + '> ' + (e.textContent || '').trim().slice(0, 40));
  });
  return out;
}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        await pg.goto(src.as_uri()); await pg.wait_for_timeout(800)
        meta = await pg.evaluate('Deck.meta.map(m=>({id:m.id,steps:m.steps}))')
        bad = 0
        for i, m in enumerate(meta):
            if only and m['id'] not in only: continue
            await pg.evaluate(f'Deck.go({i},{m["steps"]})'); await pg.wait_for_timeout(700)
            res = await pg.evaluate(JS, i)
            if res:
                bad += 1; print(f'{i+1:02d} {m["id"]}:'); [print('   ', r) for r in res[:6]]
        print('slides with issues:', bad, '| errors:', errs[:10])
        await b.close()
asyncio.run(main())
