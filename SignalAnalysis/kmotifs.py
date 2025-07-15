import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1) Load your data
df = pd.read_excel('F:/BlindMole_tracking_Juna/2025/BMR10/BMR10/output/BMR10_with_landmarks_left_ToPlot.xlsx', engine='openpyxl')
series = df.iloc[:, 0].values
segment = series # points 0–2000

# 2) SAX parameters
window_size = 100     # length of each motif window
paa_size    = 10        # number of PAA segments
alphabet    = list('abcde')  # 5‐symbol alphabet
# Gaussian breakpoints for 5‐symbol SAX (quantiles for N(0,1))
breakpoints = np.array([-0.8416212335729143, -0.2533471031357997,
                         0.2533471031357997, 0.8416212335729143])

def sax_word(subseq):
    μ, σ = subseq.mean(), subseq.std()
    if σ < 1e-6:
        return None
    zn = (subseq - μ) / σ
    seg_len = len(zn) // paa_size
    paa = zn.reshape(paa_size, seg_len).mean(axis=1)
    inds = np.searchsorted(breakpoints, paa)
    return ''.join(alphabet[i] for i in inds)

# 3) Slide window → collect SAX words and start positions
sax_dict = {}
for i in range(len(segment) - window_size + 1):
    w = sax_word(segment[i : i + window_size])
    if w:
        sax_dict.setdefault(w, []).append(i)

# 4) Filter motifs that occur exactly 5 times
motifs = {w: pos for w, pos in sax_dict.items() if len(pos) > 50}

# 5) Plot those motifs
if not motifs:
    print("No motifs found with exactly 5 occurrences in points 0–2000.")
else:
    # define x‐range to cover all motif windows
    starts = [p for positions in motifs.values() for p in positions]
    x0 = max(min(starts) - 10, 0)
    x1 = min(max(starts) + window_size + 10, len(segment))
    
    x = np.arange(x0, x1)
    y = segment[x0:x1]
    
    plt.figure(figsize=(12, 4))
    plt.plot(x, y, color='lightgray', linewidth=1)
    
    cmap = plt.get_cmap('tab10')
    legend_patches = []
    for idx, (word, positions) in enumerate(motifs.items()):
        color = cmap(idx % cmap.N)
        for p in positions:
            plt.axvspan(p, p+window_size, color=color, alpha=0.4)
            plt.axvline(p, linestyle='--', color=color)
        legend_patches.append(
            mpatches.Patch(color=color, alpha=0.4, label=f"Motif '{word}'")
        )
    
    plt.title(f"SAX Motifs (window={window_size}) Appearing Exactly 5 Times")
    plt.xlabel("Index")
    plt.ylabel("Signal Value")
    plt.xlim(x0, x1)
    plt.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1,1))
    plt.tight_layout()
    plt.show()
