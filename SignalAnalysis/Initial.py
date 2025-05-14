# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:55:41 2024

@author: Administrator
"""
import pandas as pd 
from analysis_signal import analysis_signal
import numpy as np
from numba import cuda

def main():

    #%% User input
       input_data = 'D:/Silvia/Blindmole_deep_learning/BMR10/output/BMR10_with_landmarks_left_ToPlot.xlsx'
       _fps = 24.004
       sheet_name = 'BM_snout_y'
    #%%
       df = pd.read_excel(input_data, sheet_name=sheet_name)
       data = df[['Left_side']]

       signal = data[250:350]
      # analysis_signal.plot_graphs(range(len(signal)), signal)
       analysis_signal.FindMotif(signal)
       
       #%%
      #% data = data[1000:1100]
       # instance1 = analysis_signal(data, _fps)
       # time = instance1.time_domain()
       # instance1.plot_graphs(time,data,'time_domain', 'time(sec)','BM_snout')
       # xfreq, yfreq = instance1.fourier_transform()
       # instance1.plot_graphs(xfreq, yfreq, 'freq domain', 'frequency','amplitude')
       # instance1.wavelet_transform()
      #instance1.short_time_fourier()
      
      #%%
      #  pattern = data[11275:11300]
       
      #  analysis_signal.plot_graphs(range(len(pattern)), pattern)
      #  #signal = data[11175:11375]
      #  signal = data[0:5000]
      #  analysis_signal.plot_graphs(range(len(signal)), signal)
      #  window_size = len(pattern)  # Use the pattern length as window size for example
      #  correlations = analysis_signal.sliding_correlation(pattern, signal, window_size)
      #  print("Correlations:", correlations)
      #  analysis_signal.plot_graphs(range(len(correlations)), correlations)
      #  correlations = np.asarray(correlations)  # Convert to numpy array
      #  peaks = analysis_signal.find_peaks_in_correlations(correlations,height = 0.7, distance = 20)
      #  print('peaks:', peaks)
      #  analysis_signal.plot_signal_identification(range(len(signal)), signal, peaks, window_size)
      
      
      
      #%%

if __name__ == "__main__":
    main()