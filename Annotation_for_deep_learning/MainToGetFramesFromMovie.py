# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:19:40 2023

@author: Administrator
"""

#Script to  get frames for training 
#0-add the settings-path of the movie, where to save the movies
#1-create video object
#2- find number of frames
#3- do a list with random numbers
#4- go through each frame of the list and save it

'''
Libraries
'''
import GetFramesFromVideo as GFFV
import tkinter as tk
from tkinter import  filedialog, simpledialog
import pandas as pd

'''
Settings
'''



# inputMovie = "X:/Users/Members/Juna/BMR2 vs BMR5 as stimulus 8.7.21_up.avi"
# outputFolder = "X:/Users/Members/Juna/images/train/"
# #use in the case of randomic selection
# nframestotake = 20
# #use for manually selection

# selected_frames = [2411,2420,2462,2746,2764,2791,2795,2807,2821,2834,2835,2836,2837,2839,2847,2874,2925,2941,2964,2998,3005,3023,3027,3107,3110,3117,3127,3167,3191,3195,3198,3310,3324,3325,3326,3338,3388,3391,3400,3425,3429,3432,3438,3480,4139,4144,4249,4250,4256,4267,4308,5870,5882,5920,6217,11076]




# #list(range(2415,2423+1)) + list(range(2830,2836+1)) + list(range(2916,2924+1)) + list(range(4410,4415+1)) + list(range(4441,4446+1)) +  [2154,2167,2198,2286,2404,2743,2808,3082,3176,3282,3383,3589,3782,3940,4238,4253,4316]

# #selected_frames = [2202,2235,2739,2925,2742,2806,2828,2854,2888,2925,3070,
#                  #  3400,3590,3940,3945,4254,4280,4445,4450,4489,
#                   # 4706,4818,5035,5042,5110,5290,5645,5882,6076,7414,
#                  #  9102,9123,10092,10208,10227,10245,11101,12311,23063]
                 


def main():
   root = tk.Tk()
   root.withdraw()
   
   file_path = filedialog.askopenfilename(title = "open excel with information", filetypes=[("Excel files", "*.xlsx *.xls")])
   outputFolder = filedialog.askdirectory(title="Select Output Folder with train images")
   start_image = simpledialog.askinteger("Start image", "From which # image to save the images?")
   sheet_names = pd.ExcelFile(file_path).sheet_names
   
   for sheet in sheet_names:
      df = pd.read_excel(file_path, sheet_name= sheet)
      
      for row in range(len(df)):
         inputMovie = df.loc[row, 'Frame']
         selected_frames = list(range(df.loc[row,'Start'], df.loc[row,'End'] + 1))
         nframestotake = len(selected_frames)
         start_image = GFFV.Get_Results(inputMovie,outputFolder,nframestotake,selected_frames, start_image)

if __name__ == "__main__":
    main()