import sys, pathlib
from PIL import Image
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
fs = sorted(src.glob('*.png')); per = 4
for k in range(0, len(fs), per):
    im = Image.new('RGB', (1920, 1080), (0, 0, 0))
    for j, f in enumerate(fs[k:k + per]):
        t = Image.open(f).convert('RGB').resize((960, 540), Image.LANCZOS)
        im.paste(t, ((j % 2) * 960, (j // 2) * 540))
    im.save(out / f'sheet-{k // per + 1:02d}.png')
print(len(fs))
