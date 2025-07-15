import numpy as np

# 1) Your original signal:
x_orig = np.array([0, 1, 2, 3, 4])       # original sample positions
y_orig = np.array([0.0, 0.8, 0.9, 0.1, 0])  # original amplitudes

# 2) Define a finer grid of positions:
num_new = 50
x_new = np.linspace(x_orig.min(), x_orig.max(), num_new)

# 3) Interpolate:
y_new = np.interp(x_new, x_orig, y_orig)
a=1