from scipy.signal import find_peaks, peak_widths
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.ndimage import uniform_filter1d
import numpy as np
from scipy.signal import medfilt


def characterize_peaks_pattern_vs1(signal, matches, pattern_length,distance_profile):
    Patterns_dict = defaultdict(list)
    prominence_threshold = 0.5
    min_slope = 0.8
    ds = 3 #samples outside
    
    
    for i, match_idx in enumerate(matches):
        #suppose interval of 
        intervalf = 1.0 #frame
        pattern = signal[match_idx:match_idx + pattern_length]
        pattern1 = (pattern.values).ravel()
        #first derivative
        dy_pat = np.gradient(pattern1, intervalf)
        
        peaks_rel,_ = find_peaks(pattern1,prominence=prominence_threshold)
        #shift peaks to global
        peaks_global = peaks_rel + match_idx
        good_peaks = []
        
        for pks_rel, pks_global in zip(peaks_rel, peaks_global):
            #ensure they are in the range
            if pks_rel - ds < 0 or pks_rel + ds > (len(pattern1)-1):
                continue
            left_slope = ((pattern1[pks_rel] - pattern1[pks_rel - ds])/(ds*intervalf)) #positive slope
            right_slope = ((pattern1[pks_rel+ds] - pattern1[pks_rel])/(ds*intervalf)) #negative slope
            if left_slope > min_slope and right_slope < -min_slope:
                good_peaks.append(pks_global)
        
        Patterns_dict[i]= [match_idx, good_peaks, distance_profile[match_idx]]
        #get interval
        
        
    return Patterns_dict

def characterize_peaks_pattern(signal, matches, pattern_length,distance_profile):
    Patterns_dict = defaultdict(list)
   
    #go through each find peaks
    for i, match_idx in enumerate(matches):
           
            pattern = signal[match_idx:match_idx + pattern_length]
            pattern_aux = (pattern.values).ravel()
            
            #Baseline substraction via median filter
            baseline = medfilt(pattern_aux, kernel_size=5) # this is 5 points
            detrended = pattern_aux -baseline
            #Find all local maxima and compute their prominences (it is the delta y) with height above zero
            #compute a robust threshold
            max_val = np.max(detrended)
            height_thr = 0.1*max_val
            
            max_val_min = np.min(-detrended)
            height_thr_min = 0.1*max_val_min
            
            peaks_rel, props = find_peaks(detrended, height = height_thr)
            #invert signal for minimum
            minimum_rel, _ = find_peaks(-detrended, height = height_thr_min)
            
            nearest_min_rel = find_nearest_minimum(peaks_rel,minimum_rel)
                          
            #return to original peaks
            peaks_original = peaks_rel + match_idx
            peaks_original = peaks_original.tolist()
            
            minimum_original = minimum_rel + match_idx
            minimum_original = minimum_original.tolist()
            
            nearest_minima_pairs_original = [
            (lm + match_idx if lm is not None else None,
             rm + match_idx if rm is not None else None)
            for lm, rm in nearest_min_rel
        ]
            
            Patterns_dict[i]= [match_idx, peaks_original, nearest_minima_pairs_original, distance_profile[match_idx]]
    return Patterns_dict
    '''
    for each peak find the nearest minimum
    '''
def find_nearest_minimum(peaks_rel,minima_rel):
        nearest_min_rel =[]
        for p in peaks_rel:
            left_mins = minima_rel[minima_rel < p]
            right_mins = minima_rel[minima_rel > p]
            
            left_min =left_mins.max() if left_mins.size > 0 else None
            right_min =right_mins.min() if right_mins.size > 0 else None
            
            nearest_min_rel.append((left_min,right_min))
        return nearest_min_rel
                

'''
find peaks of a given signal
input:signal
output:number_peaks
'''
def Find_peaks(data):
    data_aux = (data.values).ravel()
    #Baseline substraction via median filter
    baseline = medfilt(data_aux, kernel_size=5) # this is 5 points
    detrended = data_aux -baseline
    #compute a robust threshold
    max_val = np.max(detrended)
    height_thr = 0.1*max_val
    peaks_rel, props = find_peaks(detrended, height = height_thr)
    number_peaks = len(peaks_rel.tolist())
    
    return number_peaks