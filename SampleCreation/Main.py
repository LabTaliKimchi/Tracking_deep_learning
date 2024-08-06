# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 09:40:20 2023

@author: Administrator
"""

import cv2
import AuxiliaryFiles as AF
import yaml
import tkinter as tk
from tkinter import filedialog
import os

'''
 Function to select a YAML file
 '''
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select YAML file with general setting ", filetypes=[("YAML files", "*.yaml *.yml")])
    return file_path

'''
 function to open yaml
'''
def open_yaml():
    file_path = select_file()
    settings = {}
    if file_path:
        try:
            with open(file_path, 'r') as file:
                settings = yaml.safe_load(file)
              
        except Exception as e:
            print(f"Error reading the file: {e}")
    else:
        print("No file selected. Exiting...")
    return settings 

'''
 function to create a folder
'''
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")

    
    
    
    

def main():
    count = 0
    settings = open_yaml()
    output_folder = settings['Create_sample_settings']['Folder_with_data']
    list_frames = settings['Create_sample_settings']['list_frames']
    video_file = settings['Create_sample_settings']['video_file']
    count = settings['Create_sample_settings']['number_first_movie']
    
    #outputfile = 'F:/YaelShammaiData/data/images/train/'
    #video_file = 'X:/Users/Members/Yael_Shammai/results/behavioral assays/social interaction/20230801 C57-BTBR + Balbc pilot/upward view/BTBR 103-1m.avi'
   # list_frames = [5333,5713,5796,3209,3308,3424,6616,7674,10419,10502,10601,10765,11377,16422,16885,17099,17149,17546,17811,23384,24056,25782,30627]
    
    #Create folder if it doesn't exist
    outputfile1 = output_folder + '/' +  'images'
    outputfile = output_folder + '/' +  'images' + '/train/' 
    create_folder(outputfile1)
    create_folder(output_folder + '/' +  'images' + '/val/')
    create_folder(output_folder + '/' +  'images' + '/train/')
    create_folder( output_folder + '/' +  'labels')
    create_folder(output_folder + '/' +  'labels' + '/train/')
    create_folder(output_folder + '/' +  'labels' + '/val/')
       
   
    video = cv2.VideoCapture(video_file)
    for frame_id  in  list_frames:
        count += 1
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        namefile = outputfile + str(count) + '_image' + '.png'
        cv2.imwrite(namefile, frame)
        

if __name__ == "__main__":
    main()











