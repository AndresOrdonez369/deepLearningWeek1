"""Semana 3 · Tema 2 experiments (NB06): transfer learning (camiseta vs camisa with 200 photos), explaining images
(occlusion, Grad-CAM, gradient x image) with the sanity check, and explaining a credit decision (permutation importance,
SHAP, counterfactual, check by zone) on a fictional cooperative."""
import os, json, time, sys; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np, keras, tensorflow as tf
from keras import layers
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
SEED = 2026; R = {}; t0 = time.time()
(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
x_train = (x_train / 255.0).astype('float32')[..., None]; x_test = (x_test / 255.0).astype('float32')[..., None]
# ---- B1 transfer learning: 4 kinds of tops (camiseta, suéter, abrigo, camisa) from a network that never saw tops
def base_conv():
    return [layers.Conv2D(16, 3, activation='relu'), layers.MaxPooling2D(2),
            layers.Conv2D(32, 3, activation='relu'), layers.MaxPooling2D(2), layers.Flatten()]
BASE, TOPS = [1, 3, 5, 7, 8, 9], [0, 2, 4, 6]
mk = np.isin(y_train, BASE); remap = {c: i for i, c in enumerate(BASE)}
keras.utils.set_random_seed(SEED); convs = base_conv()
base = keras.Sequential([keras.Input((28, 28, 1)), *convs, layers.Dense(len(BASE), activation='softmax')])
base.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
base.fit(x_train[mk], np.array([remap[c] for c in y_train[mk]]), epochs=5, batch_size=128, verbose=0)
mt = np.isin(y_test, BASE)
R['base_6clases'] = float(base.evaluate(x_test[mt], np.array([remap[c] for c in y_test[mt]]), verbose=0)[1])
W = [l.get_weights() for l in convs]; tm = {c: i for i, c in enumerate(TOPS)}
def pick(X, Y, n, start=0):
    idx = np.concatenate([np.where(Y == c)[0][start:start + n] for c in TOPS]); return X[idx], np.array([tm[c] for c in Y[idx]])
xte4, yte4 = pick(x_test, y_test, 1000)
xv4, yv4 = pick(x_train, y_train, 50, start=1000)
stop = lambda: keras.callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
tr = {}
for n in (5, 20, 100):
    xt4, yt4 = pick(x_train, y_train, n)
    keras.utils.set_random_seed(SEED)
    s0 = keras.Sequential([keras.Input((28, 28, 1)), *base_conv(), layers.Dense(4, activation='softmax')])
    s0.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
    s0.fit(xt4, yt4, epochs=100, batch_size=16, validation_data=(xv4, yv4), callbacks=[stop()], verbose=0)
    c2 = base_conv(); keras.utils.set_random_seed(SEED)
    fz = keras.Sequential([keras.Input((28, 28, 1)), *c2, layers.Dense(4, activation='softmax')])
    for l, w in zip(c2, W): l.set_weights(w); l.trainable = False
    fz.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
    fz.fit(xt4, yt4, epochs=100, batch_size=16, validation_data=(xv4, yv4), callbacks=[stop()], verbose=0)
    b_ = float(fz.evaluate(xte4, yte4, verbose=0)[1]); ntr = int(sum(np.prod(w.shape) for w in fz.trainable_weights))
    for l in c2: l.trainable = True
    fz.compile(keras.optimizers.Adam(1e-4), 'sparse_categorical_crossentropy', metrics=['accuracy'])
    fz.fit(xt4, yt4, epochs=40, batch_size=16, validation_data=(xv4, yv4), callbacks=[stop()], verbose=0)
    tr[n] = dict(desde_cero=float(s0.evaluate(xte4, yte4, verbose=0)[1]), congelada=b_, ajuste_fino=float(fz.evaluate(xte4, yte4, verbose=0)[1]),
                 entrenables_congelada=ntr, params=int(s0.count_params()))
    print('B1', n, tr[n], time.time() - t0, flush=True)
R['transfer'] = tr
# ---- B2 explain images with a 10-class CNN (same as NB03)
keras.utils.set_random_seed(SEED)
cnn = keras.Sequential([keras.Input((28, 28, 1)), *base_conv(), layers.Dense(10, activation='softmax')])
cnn.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
cnn.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1, verbose=0)
R['cnn10'] = float(cnn.evaluate(x_test, y_test, verbose=0)[1])
def gradcam(model, x, cls):
    inp = keras.Input((28, 28, 1)); h = inp; conv_out = None
    for i, l in enumerate(model.layers):
        h = l(h)
        if i == 2: conv_out = h
    g_model = keras.Model(inp, [conv_out, h])
    with tf.GradientTape() as g:
        co, p = g_model(x[None]); s = p[0, cls]
    gr = g.gradient(s, co)[0]; w = tf.reduce_mean(gr, axis=(0, 1))
    cam = tf.nn.relu(tf.reduce_sum(co[0] * w, -1)).numpy()
    cam = tf.image.resize(cam[..., None], (28, 28)).numpy()[..., 0]
    return cam / (cam.max() + 1e-8)
def grad_x(model, x, cls):
    xt = tf.convert_to_tensor(x[None])
    with tf.GradientTape() as g:
        g.watch(xt); s = model(xt)[0, cls]
    gr = g.gradient(s, xt).numpy()[0, :, :, 0]
    return np.abs(gr * x[:, :, 0])
def oclusion(model, x, cls, k=6, s=2):
    p0 = model.predict(x[None], verbose=0)[0, cls]; H = np.zeros((28, 28)); C = np.zeros((28, 28)); batch, pos = [], []
    for i in range(0, 28 - k + 1, s):
        for j in range(0, 28 - k + 1, s):
            xx = x.copy(); xx[i:i + k, j:j + k, 0] = 0; batch.append(xx); pos.append((i, j))
    P = model.predict(np.array(batch), verbose=0)[:, cls]
    for (i, j), p in zip(pos, P): H[i:i + k, j:j + k] += p0 - p; C[i:i + k, j:j + k] += 1
    return H / np.maximum(C, 1)
idx = [int(np.where(y_test == c)[0][0]) for c in (9, 6, 8)]   # botín, camisa, bolso
maps = []
for k in idx:
    x = x_test[k]; c = int(y_test[k])
    maps.append(dict(i=k, label=c, p=round(float(cnn.predict(x[None], verbose=0)[0, c]), 4),
                     gradcam=np.round(gradcam(cnn, x, c), 3).tolist(), oclusion=np.round(oclusion(cnn, x, c), 3).tolist(),
                     gradx=np.round(grad_x(cnn, x, c) / (grad_x(cnn, x, c).max() + 1e-8), 3).tolist()))
R['mapas'] = maps
# sanity check: same architecture with random weights
keras.utils.set_random_seed(SEED + 1)
rnd = keras.Sequential([keras.Input((28, 28, 1)), *base_conv(), layers.Dense(10, activation='softmax')])
corr = {'gradcam': [], 'gradx': [], 'oclusion': []}
for k in range(30):
    x = x_test[k]; c = int(y_test[k])
    for name, f in [('gradcam', gradcam), ('gradx', grad_x), ('oclusion', oclusion)]:
        a, b = f(cnn, x, c).ravel(), f(rnd, x, c).ravel()
        r = spearmanr(a, b).correlation; corr[name].append(0.0 if np.isnan(r) else float(r))
R['cordura'] = {k: round(float(np.mean(v)), 3) for k, v in corr.items()}
x = x_test[idx[0]]
R['cordura_mapas'] = dict(gradcam=np.round(gradcam(rnd, x, 9), 3).tolist(), gradx=np.round(grad_x(rnd, x, 9) / (grad_x(rnd, x, 9).max() + 1e-8), 3).tolist())
print('B2', R['cnn10'], R['cordura'], time.time() - t0, flush=True)
# ---- B3 a fictional cooperative: explain a credit decision
rng = np.random.default_rng(SEED); n = 6000
rural = (rng.random(n) < 0.4).astype(int)
ingreso = np.round(rng.lognormal(np.log(620), 0.45, n) * np.where(rural, 0.85, 1.0), 2)
carga = np.clip(rng.lognormal(np.log(0.25), 0.45, n), 0.05, 0.9)         # cuota / ingreso
antig = np.round(rng.exponential(40, n))                                 # months as a member
atrasos = rng.poisson(0.35 + 0.25 * (carga > 0.4))                       # late payments, last 12 months
garante = (rng.random(n) < 0.42).astype(int)
ahorro = np.round(rng.lognormal(np.log(0.8), 0.8, n), 2)                 # savings, in months of income
logit = (-1.6 + 3.2 * np.tanh(4 * np.maximum(carga - 0.32, 0)) + 0.9 * np.minimum(atrasos, 2)
         - 1.4 * (1 - np.exp(-antig / 18)) - 1.0 * garante - 0.5 * np.log1p(ahorro) + 0.5 * rural)
mora = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
cols = ['ingreso', 'carga', 'antiguedad', 'atrasos', 'garante', 'ahorro', 'rural']
X = np.c_[ingreso, carga, antig, atrasos, garante, ahorro, rural].astype('float32')
Xtr, Xte, ytr, yte = X[:4800], X[4800:], mora[:4800], mora[4800:]
mu, sd = Xtr.mean(0), Xtr.std(0)
norm = lambda A: (A - mu) / sd
keras.utils.set_random_seed(SEED)
m = keras.Sequential([keras.Input((7,)), layers.Dense(16, activation='relu'), layers.Dense(8, activation='relu'), layers.Dense(1, activation='sigmoid')])
m.compile(keras.optimizers.Adam(0.01), 'binary_crossentropy', metrics=['accuracy'])
m.fit(norm(Xtr), ytr, epochs=30, batch_size=64, validation_split=0.2, verbose=0)
f = lambda A: m.predict(norm(A), verbose=0)[:, 0]
pte = f(Xte); auc = roc_auc_score(yte, pte)
R['coop'] = dict(n=n, tasa_mora=float(mora.mean()), auc=float(auc), acc=float(((pte >= 0.5) == yte).mean()), rechazados=float((pte >= 0.5).mean()))
imp = {}
for j, c in enumerate(cols):
    Xp = Xte.copy(); Xp[:, j] = np.random.default_rng(SEED).permutation(Xp[:, j]); imp[c] = float(auc - roc_auc_score(yte, f(Xp)))
R['coop']['importancia'] = imp
# a rejected member: the first test member with probability between 0.6 and 0.8
k = int(np.where((pte > 0.6) & (pte < 0.8))[0][0]); socia = Xte[k]
import shap
expl = shap.KernelExplainer(f, Xtr[:100]); sv = expl.shap_values(socia[None], nsamples=500, silent=True)[0]
R['coop']['socia'] = dict(valores=dict(zip(cols, [float(v) for v in socia])), prob=float(pte[k]),
                          shap=dict(zip(cols, [float(v) for v in sv])), base=float(np.asarray(expl.expected_value).ravel()[0]))
# counterfactual: how much must the payment burden fall to be approved (p < 0.5)?
cf = None
for c in np.arange(socia[1], 0.04, -0.01):
    s2 = socia.copy(); s2[1] = c
    if f(s2[None])[0] < 0.5: cf = dict(carga=float(round(c, 2)), prob=float(f(s2[None])[0])); break
R['coop']['contrafactual_carga'] = cf
s3 = socia.copy(); s3[3] = 0; R['coop']['sin_atrasos_prob'] = float(f(s3[None])[0])
# by zone
z = Xte[:, 6] == 1
def rates(mask):
    y, p = yte[mask], pte[mask] >= 0.5
    return dict(n=int(mask.sum()), mora_real=float(y.mean()), rechazo=float(p.mean()), falsa_alarma=float(p[y == 0].mean()))
R['coop']['por_zona'] = dict(rural=rates(z), urbana=rates(~z))
# the same model WITHOUT the rural column: does the gap disappear?
keras.utils.set_random_seed(SEED); keep = [0, 1, 2, 3, 4, 5]
m2 = keras.Sequential([keras.Input((6,)), layers.Dense(16, activation='relu'), layers.Dense(8, activation='relu'), layers.Dense(1, activation='sigmoid')])
m2.compile(keras.optimizers.Adam(0.01), 'binary_crossentropy', metrics=['accuracy'])
m2.fit(norm(Xtr)[:, keep], ytr, epochs=30, batch_size=64, validation_split=0.2, verbose=0)
pte = m2.predict(norm(Xte)[:, keep], verbose=0)[:, 0]
R['coop']['sin_rural'] = dict(auc=float(roc_auc_score(yte, pte)), rural=rates(z), urbana=rates(~z))
print('B3', json.dumps(R['coop'], ensure_ascii=False)[:1500], 'total', time.time() - t0, flush=True)
json.dump(R, open(sys.argv[1] if len(sys.argv) > 1 else 'tema2.json', 'w'), separators=(',', ':'), ensure_ascii=False)
