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
          plt.plot(x, y)
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
      
      