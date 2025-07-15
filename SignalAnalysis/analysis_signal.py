# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:02:59 2024

@author: Administrator
"""
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np
import pywt
from scipy.signal import stft
from scipy.signal import find_peaks
import pandas as pd
import os
os.environ["NUMBA_DISABLE_CUDA"] = "1"
import stumpy
import matplotlib.cm as cm
import plot_peaks
import Caracterize_peaks
from  class_pattern_detection import class_pattern_detection

class analysis_signal:
    
      def __init__(self, input_data, fps):
          self.input_data = input_data
          self.fps = fps

      '''
      input : data and fps
      output: time in seconds
      '''
      def time_domain(self):
          _initial_time = 0
          _final_time = len(self.input_data)/self.fps #seconds
          _time_domain = np.arange(_initial_time,_final_time , 1/self.fps )
          return _time_domain
      
      '''
        input: data to plot
        output : plot
        '''
      @staticmethod
      def plot_graphs(x ,y, title = 0, x_name = 0, y_name =0):
          plt.figure(figsize=(10, 4))
          plt.plot(x, y, '-o' )
          plt.title(title)
          plt.xlabel(x_name)
          plt.ylabel(y_name)
          plt.grid()
          plt.show()
          
          
      def fourier_transform(self):
          # Compute the Fast Fourier Transform (FFT)
          N = len(self.input_data)
          yf = fft(self.input_data)
          xf = fftfreq(N, 1 / self.fps)
          y = np.abs(yf)
          return xf, y
      
      def wavelet_transform(self):
          coeffs, freqs = pywt.cwt(self.input_data, np.arange(1, 10), 'morl', sampling_period=1/self.fps)

          plt.figure(figsize=(10, 4))
          plt.imshow(np.abs(coeffs), extent=[0, 1, 1, 10], cmap='PRGn', aspect='auto',
                     vmax=abs(coeffs).max(), vmin=-abs(coeffs).max())
          plt.title('Wavelet Transform (CWT)')
          plt.xlabel('Time [s]')
          plt.ylabel('Frequency [Hz]')
          plt.colorbar(label='Amplitude')
          plt.show()

      def short_time_fourier(self):
         
          f, t, Zxx = stft(self.input_data, self.fps, nperseg=1)

          plt.figure(figsize=(10, 4))
          plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
          plt.title('STFT Magnitude')
          plt.ylabel('Frequency [Hz]')
          plt.xlabel('Time [s]')
          plt.colorbar(label='Amplitude')
          plt.show()
    
      @staticmethod
      def correlation(pattern, signal):
          # Ensure both pattern and signal are 1-dimensional
          pattern = np.asarray(pattern).flatten()
          signal = np.asarray(signal).flatten()
  
          # Normalize pattern and signal
          pattern_norm = (pattern - np.mean(pattern)) / (np.std(pattern) * len(pattern))
          signal_norm = (signal - np.mean(signal)) / np.std(signal)
  
          # Calculate correlation
          corr = np.correlate(signal_norm, pattern_norm, mode='valid')
          return corr
      
      @staticmethod
      def sliding_correlation(pattern, signal, window_size):
          correlations = []
          for i in range(len(signal) - window_size + 1):
              window = signal[i:i + window_size]
              corr = analysis_signal.correlation(pattern, window)
              correlations.append(corr.item())
          return correlations
      
      @staticmethod
      def find_peaks_in_correlations(correlations, height=None, distance=None):
          peaks, _ = find_peaks(correlations, height=height, distance=distance)
          return peaks
      
      @staticmethod
      def plot_signal_identification(x,y,peaks, windows_size, title = None, x_name = None, y_name =None):
          plt.figure(figsize=(10, 4))
          plt.plot(x, y)
          #% draw peaks
          count = 0
          for p in peaks:
            if count % 2 == 0:
                plt.plot(x[p:(p+windows_size)],y[p:(p+windows_size)],color = "red")
            else:
                plt.plot(x[p:(p+windows_size)],y[p:(p+windows_size)],color = "green")
            count = count + 1
          
          #%
          plt.title(title)
          plt.xlabel(x_name)
          plt.ylabel(y_name)
          plt.grid()
          plt.show()
      
      '''
      Find 2 motifs
      '''
      
      @staticmethod
      
      def FindMotif(signal): 
        signal = signal.values
        time_series =  signal.ravel()  # or signal.flatten()        
        # Example: your_signal is a 1D numpy array of your time series
        m = 20  # motif length (choose based on expected pattern size)
        k=3
        radius=2.0
        matrix_profile = stumpy.stump(time_series, m)

        # Find the location of the best motif pair
        motif_idx = np.argmin(matrix_profile[:, 0])
        motif_pair = [motif_idx, int(matrix_profile[motif_idx, 1])]

        # Plot the motifs
        plt.plot(signal, label='Time Series')
        for idx in motif_pair:
            plt.plot(range(idx, idx + m), signal[idx:idx + m], linewidth=3)
        plt.legend()
        plt.show() 
         # Find top-k motifs using stumpy.motifs
        a=1
        
      '''
        Find k motifs
        '''
      def Find_k_motifs(signal):
            m=100
            k=10     
            motif_indices = []
                   
            signal = signal.values
            time_series =  signal.ravel()  # or signal.flatten()
            #extract matrix profile
            mp = stumpy.stump(time_series, m)
            
            # Extract the matrix profile and indices
            matrix_profile = mp[:, 0]
            profile_indices = mp[:, 1]
            
            profile = matrix_profile.copy()
            for _ in range(k):
                idx= np.argmin(profile)
                match = profile_indices[idx]
                motif_indices.append((idx, match))
                # Exclude the neighborhood of the found motif to avoid trivial matches
                exclusion_zone = int(m/2)
                profile[max(0, idx - exclusion_zone):idx +exclusion_zone] = np.Inf
                profile[max(0, match - exclusion_zone):match +exclusion_zone] = np.Inf
    
               # Plot original signal
            plt.figure(figsize=(14, 4))
            plt.plot(signal, color='black', linewidth=1, label='Original Signal')

            # Overlay motifs using solid lines, unique color per motif
            colors = cm.get_cmap('tab10', k)

            for i, (a, b) in enumerate(motif_indices):
                color = colors(i)
                plt.plot(np.arange(a, a + m), signal[a:a + m], color=color, linewidth=2.5, label=f'Motif {i+1} A')
                plt.plot(np.arange(b, b + m), signal[b:b + m], color=color, linestyle = '--', linewidth=2.5, label=f'Motif {i+1} B')

            plt.title("Original Signal with Overlaid Motif Segments")
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.legend()
            plt.tight_layout()
            plt.show()
      '''
      input: pattern,signal
      output:find similar patterns accoss the signal
      '''
      def Find_similar_patterns(pattern, signal,threshold):
           pattern_length = len(pattern)
           signal = signal.values
           signal_series = signal.ravel()
           signal_series_aux =  analysis_signal.Normalized_data(signal.ravel())  # or signal.flatten()
           
           
           pattern = pattern.values
           pattern_series = pattern.ravel()
           pattern_series_aux = analysis_signal.Normalized_data(pattern.ravel())
           
           
           # Compute distance profile: similarity between pattern and every subsequence of same length in signal
           distance_profile = stumpy.mass(pattern_series, signal_series)
           
           threshold = np.percentile(distance_profile, 0.5)  # 5% most similar
           matches = np.where(distance_profile <= threshold)[0]
           for idx in matches:
               print(f"Match at index {idx}, distance {distance_profile[idx]}")
           
           return matches, pattern_length, distance_profile
      '''
       input: signal
       output: normalized signal
     ''' 
      def Normalized_data(data):
          data = (data -data.mean())/data.std()
          return data
     
      '''
      input: data as dictionary
      output: data frame in pandas 
      '''
      def convert_into_data_frame(data):
          df = pd.DataFrame.from_dict(data, orient='index', columns=['index', 'inter-peaks', 'inter-minimum','distance'])
          return df
            
      def Resume_all(pattern, signal,threshold): 
             instance1 = class_pattern_detection(pattern,signal)
             matches,cross_correlation = instance1.proccessing_conv(threshold)
             plot_peaks.plot_peaks(signal, matches, len(pattern))
             a=1
            # matches, pattern_length,distance_profile = analysis_signal.Find_similar_patterns(pattern, signal,threshold)
             Patterns_dict = Caracterize_peaks.characterize_peaks_pattern(signal, matches, len(pattern),cross_correlation)
             number_peaks = Caracterize_peaks.Find_peaks(pattern)
             df = analysis_signal.convert_into_data_frame(Patterns_dict)
            #  plot_peaks.plot_peaks(signal, matches, pattern_length)
             
            #  print(number_peaks)
             return df
           
           