import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
'''
input: signal, where the peaks found, length of the pattern
output: plot of the signal
'''

def plot_peaks(signal, matches, pattern_length):
     # Plot the original signal
           # Generate distinct colors
           colors = cm.viridis(np.linspace(0, 1, len(matches)))
           plt.figure(figsize=(14, 6))
           plt.plot(signal, label='Original Signal', color='gray', alpha=0.6)

            # Overlay each matching pattern with a different color
           for i, match_idx in enumerate(matches):
                plt.plot(
                    range(match_idx, match_idx + pattern_length),
                    signal[match_idx:match_idx + pattern_length],
                    color=colors[i],
                    linewidth=2,
                    label=f'Match at {match_idx}'
                )

           plt.title('Signal with Matched Patterns Highlighted')
           plt.xlabel('Index')
           plt.ylabel('Value')
           #plt.legend(fontsize='small', ncol=2, loc='upper right')
           plt.grid(True)
           plt.tight_layout()
           plt.show()