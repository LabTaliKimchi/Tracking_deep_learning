# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 14:30:24 2024

@author: Administrator
"""

# Import module
import configparser

# Create a configparser object
config_object = configparser.ConfigParser()
# Add sections to the configuration object
config_object.add_section("Input_files")
#config_object.set('Input_files', '; comment here')
config_object.add_section("data_to_plot")
config_object.add_section("output_file")
config_object.add_section("settings")
# Add field names to the configuration object for each section
config_object.set("Input_files","Excel file left mouse","F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_left1.xlsx")
config_object.set("Input_files","Excel file right mouse","F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_right1.xlsx'")
config_object.set("Input_files","Input_video",'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_2blind_moles_5.avi')
config_object.set("Input_files","sheet_name",'BMR')

config_object.set("data_to_plot","name of the column to plot","BM_snout_y")

config_object.set("output_file","video_output","F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_2blind_moles_6all_2graphs.avi")

config_object.set("settings","middle_tube_y","1244")
config_object.set("settings","middle_tube_x","555")
config_object.set("settings","_upper_tube","1178")
config_object.set("settings","_upper_tube","1310")
config_object.set("settings","_fps","24")
config_object.set("settings","_if_Cropped","1")
config_object.set("settings"," _if_Plot_left","1")


# Save the configuration file
with open("conf-combination-video-data.ini","w") as file_object:
    config_object.write(file_object)