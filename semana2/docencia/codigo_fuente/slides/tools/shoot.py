"""Screenshot slides. usage: python shoot.py <index.html> <outdir> [ids...] [--steps=max|0] [--w=1920 --h=1080]"""
import sys, asyncio, json, pathlib
from playwright.async_api import async_playwright
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opts = dict(a[2:].split('=') for a in sys.argv[1:] if a.startswith('--'))
src, out = pathlib.Path(args[0]).resolve(), pathlib.Path(args[1]); out.mkdir(parents=True, exist_ok=True)
only = args[2:]
W, H = int(opts.get('w', 1920)), int(opts.get('h', 1080))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if pathlib.Path('/opt/pw-browsers/chromium').exists() else None)
        pg = await b.new_page(viewport={'width': W, 'height': H})
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
        await pg.goto(src.as_uri() + opts.get('q', ''))
        await pg.wait_for_timeout(800)
        meta = await pg.evaluate('Deck.meta.map(m=>({id:m.id,steps:m.steps}))')
        for i, m in enumerate(meta):
            if only and m['id'] not in only: continue
            st = m['steps'] if opts.get('steps', 'max') == 'max' else int(opts['steps'])
            await pg.evaluate(f'Deck.go({i},0)')
            for s in range(1, st + 1):
                await pg.evaluate(f'Deck.go({i},{s})'); await pg.wait_for_timeout(120)
            await pg.wait_for_timeout(int(opts.get('wait', 1300)))
            await pg.screenshot(path=str(out / f'{i+1:02d}-{m["id"]}.png'))
        print(json.dumps(errs[:30], ensure_ascii=False, indent=0))
        await b.close()
asyncio.run(main())
