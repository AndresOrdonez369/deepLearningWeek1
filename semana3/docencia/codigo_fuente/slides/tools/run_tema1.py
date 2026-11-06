"""Semana 3 · Tema 1 experiments (NB05): overfitting + regularization, augmentation vs shifts, FGSM + adversarial training, random search."""
import os, json, time, sys; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np, keras, tensorflow as tf
from keras import layers
SEED = 2026
(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
x_train = (x_train / 255.0).astype('float32')[..., None]; x_test = (x_test / 255.0).astype('float32')[..., None]
R = {}
def cnn(extra_in=(), drop=0.0, f1=16, f2=32):
    L = [keras.Input(shape=(28, 28, 1)), *extra_in,
         layers.Conv2D(f1, 3, activation='relu'), layers.MaxPooling2D(2),
         layers.Conv2D(f2, 3, activation='relu'), layers.MaxPooling2D(2), layers.Flatten()]
    if drop: L.append(layers.Dropout(drop))
    L.append(layers.Dense(10, activation='softmax'))
    return keras.Sequential(L)
def mover(X, px):
    out = np.zeros_like(X); out[:, :, px:, :] = X[:, :, :-px, :]; return out
t0 = time.time()
# ---- A1 overfitting with little data
x_small, y_small = x_train[:1000], y_train[:1000]          # 1 000 photos to study
x_val, y_val = x_train[50000:52000], y_train[50000:52000]  # 2 000 photos for the simulacro
keras.utils.set_random_seed(SEED); m = cnn()
m.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
h = m.fit(x_small, y_small, epochs=60, batch_size=64, validation_data=(x_val, y_val), verbose=0)
H = h.history; best = int(np.argmin(H['val_loss']))
R['sobreajuste'] = dict(train_acc=[round(v, 4) for v in H['accuracy']], val_acc=[round(v, 4) for v in H['val_accuracy']],
                        train_loss=[round(v, 4) for v in H['loss']], val_loss=[round(v, 4) for v in H['val_loss']],
                        best_epoch=best + 1, test=float(m.evaluate(x_test, y_test, verbose=0)[1]))
print('A1 sin', R['sobreajuste']['best_epoch'], H['accuracy'][-1], H['val_accuracy'][-1], R['sobreajuste']['test'], flush=True)
keras.utils.set_random_seed(SEED)
m = cnn(extra_in=(layers.RandomTranslation(0.05, 0.05),), drop=0.3)      # small shifts + dropout
m.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
h = m.fit(x_small, y_small, epochs=100, batch_size=64, validation_data=(x_val, y_val), callbacks=[stop], verbose=0)
H = h.history
R['regularizada'] = dict(train_acc=[round(v, 4) for v in H['accuracy']], val_acc=[round(v, 4) for v in H['val_accuracy']],
                         train_loss=[round(v, 4) for v in H['loss']], val_loss=[round(v, 4) for v in H['val_loss']],
                         epochs=len(H['loss']), best_epoch=int(np.argmin(H['val_loss'])) + 1, test=float(m.evaluate(x_test, y_test, verbose=0)[1]))
print('A1 con', R['regularizada']['epochs'], R['regularizada']['best_epoch'], R['regularizada']['test'], time.time() - t0, flush=True)
# ---- A2 augmentation (full data) vs shifted photos
res = {}
for name, extra in [('sin', ()), ('con', (layers.RandomTranslation(0.15, 0.15),))]:
    keras.utils.set_random_seed(SEED); m = cnn(extra_in=extra)
    m.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
    m.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1, verbose=0)
    res[name] = dict(test=float(m.evaluate(x_test, y_test, verbose=0)[1]),
                     shift={px: float(m.evaluate(mover(x_test, px), y_test, verbose=0)[1]) for px in (1, 2, 3, 4)})
    if name == 'sin': base = m
    print('A2', name, res[name], time.time() - t0, flush=True)
R['aumento'] = res
# ---- A3 FGSM on the plain CNN, then adversarial training
loss_fn = keras.losses.SparseCategoricalCrossentropy()
def fgsm(model, X, y, eps, bs=2000):
    out = []
    for i in range(0, len(X), bs):
        x = tf.convert_to_tensor(X[i:i + bs]); t = tf.convert_to_tensor(y[i:i + bs])
        with tf.GradientTape() as g:
            g.watch(x); l = loss_fn(t, model(x, training=False))
        out.append(tf.clip_by_value(x + eps * tf.sign(g.gradient(l, x)), 0, 1).numpy())
    return np.concatenate(out)
EPS = [0.01, 0.02, 0.05, 0.1]
R['fgsm'] = {'limpia': float(base.evaluate(x_test, y_test, verbose=0)[1])}
for e in EPS:
    R['fgsm'][e] = float(base.evaluate(fgsm(base, x_test, y_test, e), y_test, verbose=0)[1])
print('A3', R['fgsm'], time.time() - t0, flush=True)
# adversarial training (Goodfellow et al., 2015): every batch = the clean photos + their FGSM version, made with the current weights
keras.utils.set_random_seed(SEED); adv = cnn(); opt = keras.optimizers.Adam()
@tf.function
def paso_adversarial(x, y, eps):
    with tf.GradientTape() as g:
        g.watch(x); l = loss_fn(y, adv(x, training=False))
    xa = tf.clip_by_value(x + eps * tf.sign(g.gradient(l, x)), 0, 1)
    xx, yy = tf.concat([x, xa], 0), tf.concat([y, y], 0)
    with tf.GradientTape() as g2:
        l2 = loss_fn(yy, adv(xx, training=True))
    opt.apply_gradients(zip(g2.gradient(l2, adv.trainable_variables), adv.trainable_variables))
ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(60000, seed=SEED).batch(128)
for ep in range(5):
    for xb, yb in ds: paso_adversarial(xb, yb, 0.05)
adv.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
R['fgsm_entrenada'] = {'limpia': float(adv.evaluate(x_test, y_test, verbose=0)[1])}
for e in EPS:
    R['fgsm_entrenada'][e] = float(adv.evaluate(fgsm(adv, x_test, y_test, e), y_test, verbose=0)[1])
print('A3 adv', R['fgsm_entrenada'], time.time() - t0, flush=True)
# one adversarial example for the slides
xa1 = fgsm(base, x_test[:1], y_test[:1], 0.05)
p0 = base.predict(x_test[:1], verbose=0)[0]; p1 = base.predict(xa1, verbose=0)[0]
R['ejemplo_adv'] = dict(label=int(y_test[0]), orig=(x_test[0, :, :, 0] * 255).round().astype(int).tolist(),
                        adv=(xa1[0, :, :, 0] * 255).round().astype(int).tolist(), p_orig=[round(float(v), 4) for v in p0], p_adv=[round(float(v), 4) for v in p1])
print('ej', int(p0.argmax()), float(p0.max()), int(p1.argmax()), float(p1.max()), flush=True)
# ---- A4 random search on validation
rng = np.random.default_rng(SEED)
xs, ys = x_train[:10000], y_train[:10000]; xv, yv = x_train[50000:55000], y_train[50000:55000]
trials = []
for k in range(6):
    cfg = dict(lr=float(rng.choice([1e-4, 1e-3, 1e-2])), f1=int(rng.choice([8, 16, 32])), drop=float(rng.choice([0.0, 0.3])))
    keras.utils.set_random_seed(SEED); m = cnn(drop=cfg['drop'], f1=cfg['f1'], f2=2 * cfg['f1'])
    m.compile(keras.optimizers.Adam(cfg['lr']), 'sparse_categorical_crossentropy', metrics=['accuracy'])
    m.fit(xs, ys, epochs=4, batch_size=128, verbose=0)
    cfg['val'] = float(m.evaluate(xv, yv, verbose=0)[1]); cfg['params'] = int(m.count_params()); trials.append(cfg)
    if k == 0 or cfg['val'] > max(t['val'] for t in trials[:-1]): best_m = m
    print('A4', cfg, flush=True)
bi = int(np.argmax([t['val'] for t in trials]))
R['busqueda'] = dict(trials=trials, best=bi, test_best=float(best_m.evaluate(x_test, y_test, verbose=0)[1]))
print('A4 best', bi, R['busqueda']['test_best'], 'total', time.time() - t0, flush=True)
json.dump(R, open(sys.argv[1] if len(sys.argv) > 1 else 'tema1.json', 'w'), separators=(',', ':'), ensure_ascii=False)
