import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1) Load your data
df = pd.read_excel('F:/BlindMole_tracking_Juna/2025/BMR10/BMR10/output/BMR10_with_landmarks_left_ToPlot.xlsx', engine='openpyxl')
series = df.iloc[:, 0].values
segment = series[:2001]  # points 0–2000

# 2) SAX parameters for small motifs
window_size = 20      # much shorter motif length
paa_size    = 4       # reduce to 4 segments per window
alphabet    = list('abcd')  # 4‐symbol alphabet
# Gaussian breakpoints for 4 symbols (~quartiles)
breakpoints = np.array([-0.674, 0.0, 0.674])

def sax_word(subseq):
    μ, σ = subseq.mean(), subseq.std()
    if σ < 1e-6:
        return None
    zn = (subseq - μ) / σ
    seg_len = len(zn) // paa_size
    paa = zn.reshape(paa_size, seg_len).mean(axis=1)
    inds = np.searchsorted(breakpoints, paa)
    return ''.join(alphabet[i] for i in inds)

# 3) Slide window to collect SAX words → positions
sax_dict = {}
for i in range(len(segment) - window_size + 1):
    sw = sax_word(segment[i:i+window_size])
    if sw:
        sax_dict.setdefault(sw, []).append(i)

# 4) Filter for motifs (words with ≥2 occurrences)
motifs = {w: pos for w, pos in sax_dict.items() if len(pos) > 50}

# 5) Plot all small motifs in different colors
if not motifs:
    print("No small motifs found .")
else:
    # determine global x‐range
    starts = [p for positions in motifs.values() for p in positions]
    x0 = max(min(starts) - 5, 0)
    x1 = min(max(starts) + window_size + 5, len(segment))
    x = np.arange(x0, x1)
    y = segment[x0:x1]

    plt.figure(figsize=(12,4))
    plt.plot(x, y, color='lightgray', linewidth=1)

    cmap = plt.get_cmap('tab10')
    legend_patches = []
    for idx, (word, positions) in enumerate(motifs.items()):
        col = cmap(idx % cmap.N)
        for p in positions:
            plt.axvspan(p, p+window_size, color=col, alpha=0.5)
            plt.axvline(p, linestyle='--', color=col)
        legend_patches.append(mpatches.Patch(color=col, alpha=0.5, label=f"'{word}'"))

    plt.title(f"All small motifs (length {window_size}) highlighted")
    plt.xlabel("Index")
    plt.ylabel("Signal value")
    plt.xlim(x0, x1)
    plt.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.tight_layout()
    plt.show()
