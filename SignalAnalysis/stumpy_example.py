import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Model
from keras.layers import Input, Conv1D, MaxPooling1D, UpSampling1D
from keras.optimizers import Adam
from numpy import correlate

# 1. Load & preprocess signal
df = pd.read_excel("F:/BlindMole_tracking_Juna/2025/BMR10/BMR10/output/test.xlsx", sheet_name="BM_snout_y")
y = df["Left_side"].interpolate().fillna(method="bfill").to_numpy()
#add points
M = 10
N = len(y)
x= np.arange(N)
x_new = np.linspace(0, N-1, (N-1)*M + 1)
#linear interpolation
y_new = np.interp(x_new, x,y )
signal = y_new

#add points

signal_norm = (signal - signal.min()) / (signal.max() - signal.min())

# 2. Window function
def make_windows(sig, L=128, step=5):
    n = (len(sig) - L) // step + 1
    X = np.zeros((n, L, 1), dtype=float)
    for i in range(n):
        X[i, :, 0] = sig[i*step : i*step + L]
    return X

L, step = 32, 4
X = make_windows(signal_norm, L=L, step=step)

# 3. Build convolutional autoencoder
inp = Input(shape=(L,1))
number_filters = 4
x = Conv1D(4, 16, activation="relu", padding="same")(inp)
x = MaxPooling1D(2, padding="same")(x)
x = Conv1D(4, 16, activation="relu", padding="same")(x)
encoded = MaxPooling1D(2, padding="same")(x)
x = Conv1D(4, 16, activation="relu", padding="same")(encoded)
x = UpSampling1D(2)(x)
x = Conv1D(4, 32, activation="relu", padding="same")(x)
x = UpSampling1D(2)(x)
decoded = Conv1D(1, 3, activation="sigmoid", padding="same")(x)

autoencoder = Model(inp, decoded)
autoencoder.compile(optimizer=Adam(1e-3), loss="mse")

# 4. Train autoencoder
autoencoder.fit(X, X, epochs=10, batch_size=64, validation_split=0.1)

# 5. Extract filters and detect motifs
conv_w, _ = autoencoder.layers[1].get_weights()  # (kernel_size, 1, n_filters)
n_filters = conv_w.shape[-1]
kernel_size = conv_w.shape[0]

matches = {}
for i in range(n_filters):
    kernel = conv_w[:, 0, i]
    corr = correlate(signal_norm, kernel, mode="valid")
    thresh = 0.6 * corr.max()
    hits = np.where(corr > thresh)[0]
    matches[i] = hits

# 6. Plot signal and shaded motif spans
plt.figure(figsize=(12,4))
plt.plot(signal_norm, color='black', linewidth=1)

cmap = plt.get_cmap('tab10')    # switch to 'tab20' if n_filters > 10
colors = [cmap(i % cmap.N) for i in range(n_filters)]
for filt_idx, positions in matches.items():
    col = colors[filt_idx]
    for start in positions:
        plt.axvspan(start, start+kernel_size, color=col, alpha=0.3, lw=0)
    plt.plot([], [], color=col, linewidth=10, alpha=0.3, label=f'Motif {filt_idx}')

plt.title("Normalized Signal with Shaded Motif Regions")
plt.xlabel("Sample Index")
plt.ylabel("Normalized Amplitude")
plt.legend(loc='upper right', fontsize='small', ncol=2)
plt.tight_layout()
plt.show()