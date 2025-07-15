import numpy as np
from scipy.signal import fftconvolve, find_peaks

'''
This class includes tools to find given motifs given the pattern
'''


class class_pattern_detection:
    def __init__(self,pattern,signal):
        self.pattern = (pattern.values).ravel()
        self.signal = (signal.values).ravel()
    
    def proccessing_conv(self,threshold):
        self.signal = class_pattern_detection.fill_nan(self.signal)
        normcc = self.Convulation_signal()  
        peaks, cross_correlation = self.Find_peaks_corr(normcc,threshold)
        return peaks, normcc
    
    '''
    input: pattern ,signal
    output: normalized correlation
    normalize the pattern and also each window of the original signal
    '''
    def Convulation_signal(self):
        N,L = len(self.signal), len(self.pattern)
        
        mu_p = self.pattern.mean()
        sigma_p = self.pattern.std()
        p_z = (self.pattern-mu_p)[::-1] #zero mean, reversed template for correlation
        
        ones = np.ones(L) #mask or kernel to slide on the data
        #running sums over each window
        sum_s = fftconvolve(self.signal, ones, mode = 'valid')
        sum_s2 = fftconvolve(self.signal*self.signal, ones, mode = 'valid')
        #per window mean and std
        mu_w = sum_s/L
        sigma_w = np.sqrt(sum_s2/L - mu_w**2) # Var(X)= E[X2]−(E[X])2
        #cross- correlation between the signal and the reversed pattern for each window
        num = fftconvolve(self.signal, p_z, mode = 'valid') 
        denom = sigma_w * sigma_p * L
        #normalized cross correlation
        normcc = num / denom
        
        return normcc
    
    '''
    input :Cross correlation
    output: peaks
    '''   
    def Find_peaks_corr(self, normcc,threshold):
       peaks, props = find_peaks(normcc, height=threshold)  
       cross_correlation = normcc[peaks]
       return peaks, cross_correlation
    
    
    '''
    input: data
    output: data with nan values interpolated
    '''
    def fill_nan(data):
        x=np.arange(len(data)) #do vector with all positions
        nan_mask = np.isnan(data)
        
        s_interp = data.copy()
        s_interp[nan_mask] = np.interp(x[nan_mask],x[~nan_mask],data[~nan_mask])
        
        return s_interp
    
    
    
    
 