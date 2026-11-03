"""Runs the NB04 experiments as the notebook does and exports deck/src/data/seq.json."""
import os, json, time, sys; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np, keras
from keras import layers
SEED = 2026
OUT = {}
# ---- order matters: 12 months of days late, worse vs better (the same months reversed)
rng = np.random.default_rng(SEED)
def historial(n, meses=12):
    inicio = rng.uniform(0, 5, n); pend = rng.uniform(1, 3, n)
    t = np.arange(meses)
    x = np.clip(inicio[:, None] + pend[:, None] * t + rng.normal(0, 3, (n, meses)), 0, None)
    y = rng.integers(0, 2, n)
    x = np.where(y[:, None] == 1, x, x[:, ::-1])
    return x[..., None].astype('float32') / 30, y
X, y = historial(2000); Xt, yt = historial(500)
res = {}
for name in ['promedio', 'rnn']:
    keras.utils.set_random_seed(SEED)
    if name == 'promedio':
        m = keras.Sequential([keras.Input((12, 1)), layers.Dense(8, activation='relu'), layers.GlobalAveragePooling1D(), layers.Dense(1, activation='sigmoid')])
    else:
        m = keras.Sequential([keras.Input((12, 1)), layers.SimpleRNN(8), layers.Dense(1, activation='sigmoid')])
    m.compile(keras.optimizers.Adam(0.01), 'binary_crossentropy', metrics=['accuracy'])
    h = m.fit(X, y, epochs=15, batch_size=32, verbose=0)
    res[name] = dict(params=int(m.count_params()), test=float(m.evaluate(Xt, yt, verbose=0)[1]), acc=[float(a) for a in h.history['accuracy']])
    print(name, res[name]['params'], res[name]['test'], flush=True)
i1 = int(np.where(yt == 1)[0][0])
OUT['orden'] = dict(res=res, ejemplo=[round(float(v) * 30, 1) for v in Xt[i1, :, 0]])
# ---- memory test: remember the value at the marked month
def examen(T, n, rng, K=10):
    v = rng.choice([-1.0, 1.0], size=(n, T)).astype('float32')
    pos = rng.integers(0, K, size=n)
    marca = np.zeros((n, T), dtype='float32'); marca[np.arange(n), pos] = 1
    return np.stack([v, marca], -1), (v[np.arange(n), pos] > 0).astype('int32'), pos
def modelo(kind, T):
    x = keras.Input((T, 2))
    if kind == 'atencion':
        h = layers.Dense(16, activation='tanh')(x)
        w = layers.Softmax(axis=1, name='pesos')(layers.Dense(1)(h))
        o = layers.Dense(1, activation='sigmoid')(layers.Flatten()(layers.Dot(axes=1)([w, h])))
    else:
        L = {'rnn': layers.SimpleRNN, 'lstm': layers.LSTM}[kind]
        o = layers.Dense(1, activation='sigmoid')(L(32)(x))
    return keras.Model(x, o)
mem, attw = {}, None
for T in [10, 30, 80]:
    mem[T] = {}
    for kind in ['rnn', 'lstm', 'atencion']:
        r = np.random.default_rng(SEED)
        Xm, ym, _ = examen(T, 3000, r); Xmt, ymt, pmt = examen(T, 1000, r)
        keras.utils.set_random_seed(SEED)
        m = modelo(kind, T)
        m.compile(keras.optimizers.Adam(0.003), 'binary_crossentropy', metrics=['accuracy'])
        t = time.time(); h = m.fit(Xm, ym, epochs=10, batch_size=64, verbose=0)
        mem[T][kind] = dict(params=int(m.count_params()), test=float(m.evaluate(Xmt, ymt, verbose=0)[1]), secs=round(time.time() - t, 1),
                            acc=[round(float(a), 3) for a in h.history['accuracy']])
        print(T, kind, mem[T][kind], flush=True)
        if kind == 'atencion' and T == 80:
            pw = keras.Model(m.inputs, m.get_layer('pesos').output).predict(Xmt[:1], verbose=0)[0, :, 0]
            attw = dict(pesos=[round(float(v), 4) for v in pw], marca=int(pmt[0]), valores=[int(v) for v in Xmt[0, :, 0]], y=int(ymt[0]))
OUT['memoria'] = mem; OUT['atencion'] = attw
dst = sys.argv[1] if len(sys.argv) > 1 else 'seq.json'
json.dump(OUT, open(dst, 'w'), separators=(',', ':'), ensure_ascii=False)
print('saved', dst)
