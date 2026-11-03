import os, json
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import numpy as np, keras
from keras import layers
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
SEED = 2026
keras.utils.set_random_seed(SEED)
X_m, y_m = make_moons(600, noise=0.2, random_state=SEED)
X_train, X_test, y_train, y_test = train_test_split(X_m, y_m, test_size=0.2, random_state=SEED, stratify=y_m)
keras.utils.set_random_seed(SEED)
model = keras.Sequential([keras.Input(shape=(2,)), layers.Dense(16, activation="relu"), layers.Dense(16, activation="relu"), layers.Dense(1, activation="sigmoid")])
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01), loss="binary_crossentropy", metrics=["accuracy"])
x0, x1, y0, y1 = -1.6, 2.6, -1.2, 1.7
GX, GY = 64, 44
g1, g2 = np.meshgrid(np.linspace(x0, x1, GX), np.linspace(y1, y0, GY))
grid = np.c_[g1.ravel(), g2.ravel()]
snaps = {}
SNAP = [0, 1, 3, 6, 10, 20, 40, 60]
snaps[0] = model.predict(grid, verbose=0).ravel()
class CB(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if epoch + 1 in SNAP:
            snaps[epoch + 1] = self.model.predict(grid, verbose=0).ravel()
history = model.fit(X_train, y_train, epochs=60, batch_size=32, validation_split=0.2, verbose=0, callbacks=[CB()])
h = history.history
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
NUEVOS = np.array([[0.0, 1.0], [1.0, -0.5], [0.5, 0.25]])
pn = model.predict(NUEVOS, verbose=0).ravel()
print("params", model.count_params(), "val_acc", h['val_accuracy'][-1], "test", test_loss, test_acc)
print("nuevos", pn)
print("loss", [round(v,3) for v in h['loss'][:5]], h['loss'][-1], "val", h['val_loss'][-1])
out = dict(loss=[round(v, 4) for v in h['loss']], val_loss=[round(v, 4) for v in h['val_loss']],
           acc=[round(v, 4) for v in h['accuracy']], val_acc=[round(v, 4) for v in h['val_accuracy']],
           test=[round(test_loss, 4), round(test_acc, 4)], nuevos=NUEVOS.tolist(), pn=[round(float(v), 3) for v in pn],
           box=[x0, x1, y0, y1], gx=GX, gy=GY,
           snaps={str(k): ''.join(chr(48 + int(round(float(v) * 9))) for v in snaps[k]) for k in SNAP},
           pts=[[round(a, 3), round(b, 3), int(c)] for (a, b), c in zip(X_train[:384], y_train[:384])],
           n_train=int(X_train.shape[0]), n_fit=384, n_val=96)
json.dump(out, open('moons.json', 'w'))
print('ok', len(json.dumps(out)))
