import asyncio, pathlib, json
from playwright.async_api import async_playwright
src = pathlib.Path('out/index.html').resolve().as_uri()
out = pathlib.Path('shots_i'); out.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs=[]
        pg = await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(src + '#juega'); await pg.wait_for_timeout(500)
        await pg.click('#juega button:has-text("4")'); await pg.click('#juega button:has-text("Entrenar")')
        await pg.wait_for_timeout(4000); await pg.screenshot(path=str(out/'play.png'))
        await pg.evaluate("location.hash='#entrenar'"); await pg.wait_for_timeout(300)
        await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(9000); await pg.screenshot(path=str(out/'perc.png'))
        await pg.evaluate("location.hash='#carrera'"); await pg.wait_for_timeout(8000); await pg.screenshot(path=str(out/'race.png'))
        await pg.evaluate("location.hash='#xor'"); await pg.wait_for_timeout(300)
        await pg.click('#xor button:has-text("Probar")'); await pg.wait_for_timeout(2500); await pg.screenshot(path=str(out/'xor.png'))
        await pg.evaluate("location.hash='#cuenta'"); await pg.wait_for_timeout(300)
        for i in range(6): await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(1500); await pg.screenshot(path=str(out/'cuenta.png'))
        # keyboard on slider should not navigate
        await pg.evaluate("location.hash='#activacion'"); await pg.wait_for_timeout(300)
        await pg.focus('#activacion input[type=range]'); await pg.keyboard.press('ArrowLeft'); await pg.keyboard.press('ArrowLeft')
        cur = await pg.evaluate('Deck.cur'); print('cur after slider arrows', cur)
        # presenter
        pp = await b.new_page(viewport={'width':1400,'height':820})
        pp.on('pageerror', lambda e: errs.append('P:'+str(e)))
        await pp.goto(src + '?presenter#comite'); await pp.wait_for_timeout(1500); await pp.screenshot(path=str(out/'presenter.png'))
        # reading mode mobile
        m = await b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
        m.on('pageerror', lambda e: errs.append('M:'+str(e)))
        await m.goto(src); await m.wait_for_timeout(800)
        await m.screenshot(path=str(out/'m1.png'))
        await m.evaluate("document.getElementById('linea').scrollIntoView()"); await m.wait_for_timeout(800); await m.screenshot(path=str(out/'m2.png'))
        sw = await m.evaluate('document.documentElement.scrollWidth'); print('mobile scrollWidth', sw)
        print(json.dumps(errs))
        await b.close()
asyncio.run(main())
