"""Runs the NB03 experiments exactly as the notebook does and exports deck/src/data/fmnist.json
(real images, learned filters, predictions and results for the slides)."""
import os, json, time, sys; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np, keras
from keras import layers
SEED = 2026
CLASES = ['camiseta', 'pantalón', 'suéter', 'vestido', 'abrigo', 'sandalia', 'camisa', 'zapatilla', 'bolso', 'botín']
(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
x_train = (x_train / 255.0).astype('float32')[..., None]
x_test = (x_test / 255.0).astype('float32')[..., None]

def red_densa():
    return keras.Sequential([keras.Input(shape=(28, 28, 1)), layers.Flatten(),
                             layers.Dense(128, activation='relu'), layers.Dense(10, activation='softmax')])
def red_cnn():
    return keras.Sequential([keras.Input(shape=(28, 28, 1)),
                             layers.Conv2D(16, 3, activation='relu'), layers.MaxPooling2D(2),
                             layers.Conv2D(32, 3, activation='relu'), layers.MaxPooling2D(2),
                             layers.Flatten(), layers.Dense(10, activation='softmax')])
def entrenar(model, X, y):
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    t = time.time()
    h = model.fit(X, y, epochs=5, batch_size=128, validation_split=0.1, verbose=0)
    return h, time.time() - t
def mover(X, px):
    out = np.zeros_like(X); out[:, :, px:, :] = X[:, :, :-px, :]; return out

R = {}
keras.utils.set_random_seed(SEED); densa = red_densa(); hd, td = entrenar(densa, x_train, y_train)
keras.utils.set_random_seed(SEED); cnn = red_cnn(); hc, tc = entrenar(cnn, x_train, y_train)
for name, m, h, t in [('densa', densa, hd, td), ('cnn', cnn, hc, tc)]:
    R[name] = dict(params=int(m.count_params()), test=float(m.evaluate(x_test, y_test, verbose=0)[1]), secs=round(t, 1),
                   val=[float(v) for v in h.history['val_accuracy']], loss=[float(v) for v in h.history['loss']],
                   shift={px: float(m.evaluate(mover(x_test, px), y_test, verbose=0)[1]) for px in (1, 2, 3, 4)})
    print(name, R[name], flush=True)
# shuffle the pixels: the same permutation for every image
perm = np.random.default_rng(SEED).permutation(28 * 28)
mezclar = lambda X: X.reshape(len(X), -1)[:, perm].reshape(X.shape)
xp_train, xp_test = mezclar(x_train), mezclar(x_test)
for name, f in [('densa', red_densa), ('cnn', red_cnn)]:
    keras.utils.set_random_seed(SEED); m = f(); entrenar(m, xp_train, y_train)
    R[name]['mezclada'] = float(m.evaluate(xp_test, y_test, verbose=0)[1]); print(name, 'mezclada', R[name]['mezclada'], flush=True)
# confusion of the CNN
pred_c = cnn.predict(x_test, verbose=0).argmax(1)
cm = np.zeros((10, 10), int)
for a, b in zip(y_test, pred_c): cm[a, b] += 1
off = cm.copy(); np.fill_diagonal(off, 0); i, j = np.unravel_index(off.argmax(), off.shape)
R['confusion_top'] = dict(real=CLASES[i], pred=CLASES[j], n=int(off[i, j]), por_clase={CLASES[k]: float(cm[k, k] / cm[k].sum()) for k in range(10)})
# sample images: the first test image of some classes
pick = []
for c in [9, 0, 8, 7, 1, 3, 6]:
    pick.append(int(np.where(y_test == c)[0][0]))
pd_ = densa.predict(x_test[pick], verbose=0); pc_ = cnn.predict(x_test[pick], verbose=0)
samples = [dict(i=k, label=int(y_test[k]), px=(x_test[k, :, :, 0] * 255).round().astype(int).tolist(),
                densa=[round(float(v), 4) for v in pd_[n]], cnn=[round(float(v), 4) for v in pc_[n]]) for n, k in enumerate(pick)]
W, b = cnn.layers[0].get_weights()
filt = [dict(w=[[round(float(W[r, c, 0, f]), 4) for c in range(3)] for r in range(3)], b=round(float(b[f]), 4)) for f in range(16)]
# activations of the first conv layer for the first sample (after ReLU)
act = keras.Model(cnn.inputs, cnn.layers[0].output).predict(x_test[pick[:1]], verbose=0)[0]
R['shapes'] = [list(l.output.shape[1:]) for l in cnn.layers]
out = dict(clases=CLASES, results=R, samples=samples, filters=filt,
           act0=[(act[:, :, f] / (act[:, :, f].max() + 1e-6) * 255).round().astype(int).tolist() for f in range(16)])
dst = sys.argv[1] if len(sys.argv) > 1 else 'fmnist.json'
json.dump(out, open(dst, 'w'), separators=(',', ':'), ensure_ascii=False)
print('saved', dst, os.path.getsize(dst) // 1024, 'KB')
