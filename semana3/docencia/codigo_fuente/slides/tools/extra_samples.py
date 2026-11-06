"""Extra Fashion-MNIST test photos for the week-3 deck (classes missing from fmnist.json: suéter, abrigo, sandalia).
usage: python extra_samples.py <out.json>   (reads the Keras cache ~/.keras/datasets/fashion-mnist)"""
import gzip, json, pathlib, sys
import numpy as np

D = pathlib.Path.home() / '.keras' / 'datasets' / 'fashion-mnist'
with gzip.open(D / 't10k-labels-idx1-ubyte.gz') as f:
    y = np.frombuffer(f.read(), np.uint8, offset=8)
with gzip.open(D / 't10k-images-idx3-ubyte.gz') as f:
    x = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28, 28)
out = []
for c in (2, 4, 5):                       # suéter, abrigo, sandalia: the first test photo of each class
    i = int(np.where(y == c)[0][0])
    out.append(dict(i=i, label=c, px=x[i].astype(int).tolist()))
pathlib.Path(sys.argv[1]).write_text(json.dumps(out, separators=(',', ':')))
print([(o['i'], o['label']) for o in out])
