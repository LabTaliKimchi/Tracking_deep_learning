# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:40:49 2024

@author: Administrator
"""
from Manager_data import Manager_data
import configparser
import tkinter as tk
from tkinter import filedialog
import os
from TreatAudio import TreatAudio

def open_file():
    # Create a Tkinter root widget
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file browser dialog
    file_path = filedialog.askopenfilename(title = "Select ini config file with all the parameters")


    return file_path

def main():
    #%% USER DATAt
    
    #middle_tube_y = 1244  #in pixel units
    #middle_tube_x = 555 #in pixel units
    # input_excel = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_right1.xlsx'
    # input_excel_left = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_left1.xlsx'
    # input_video = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as st
    # imulus 8.7.21_side_CUT_YOLO_2blind_moles_5.avi'
    # sheet_name = 'BMR'
    #column_name = 'BM_snout_y'
   # _outputVideo = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_2blind_moles_6all_2graphs.avi'
    # _upper_tube = 1178
    # _lower_tube = 1310
    # _fps = 24
    # _if_Cropped = 1
    # _if_Plot_left = 1
    
    #define yaml path
   # file_path = 'conf-combination-video-data.ini'
    file_path = open_file()
    config = configparser.ConfigParser()
    config.read(file_path)
    
    # Access data
    input_excel = config['Input_files']['excel file left mouse']
    input_excel_left = config['Input_files']['excel file right mouse']
    input_video = config['Input_files']['input_video']
    sheet_name = config['Input_files']['sheet_name']
    original_video = config['Input_files']['original_video']
    
    column_name = config['data_to_plot']['name of the column to plot']
    
    _outputVideo = config['output_file']['video_output']
    
    middle_tube_y = int(config['settings']['middle_tube_y'])
    middle_tube_x = int(config['settings']['middle_tube_x'])
    _upper_tube = int(config['settings']['_upper_tube'])
    _lower_tube = int(config['settings']['_lower_tube'])
    _fps = float(config['settings']['_fps'])
    _if_Cropped = int(config['settings']['_if_cropped'])
    _if_Plot_left = int(config['settings']['_if_plot_left'])
    _title = config['settings']['_title']
    #coordinates to crop
    _xstart = int(config['settings']['_xstart'])
    _ystart = int(config['settings']['_ystart'])
    _xend = int(config['settings']['_xend'])
    _yend = int(config['settings']['_yend'])

    #%%
    
    # Manager_data.Manager_data( middle_tube_y, middle_tube_x, input_excel, input_video, sheet_name, column_name, _outputVideo, _upper_tube, _lower_tube, _fps,_if_Cropped,
    #                           _if_Plot_left, input_excel_left, _title,_xstart, _ystart, _xend, _yend)
    instance_audio = TreatAudio(original_video,_outputVideo)
    instance_audio()

if __name__ == "__main__":
    main()