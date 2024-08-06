# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 09:02:26 2023

@author: Administrator
"""

'''
Script add visibility to the annotation data in keypoints

IN dim=3 visibility values are = 0 not visible
1 is partial visible
2 is visible

Steps for the script:
    1)- Read the files from the folder
    2)- for each file read the text with  f.read
    3)- split the string into a list
    4)- insert  the number 2 after the keypoints coordinates
    if the element before is nan insert 0
    5)- convert into text

'''
import glob
import ToInsertVisibilityInAnnotation as TIVIA

    

def main():
#directory
#open the directory with the files
    # path = "F:/Juna/19_6_2024/TrainingDataSecondmouse/labels/train_without_vis"
    # outputpath = "F:/Juna/19_6_2024/TrainingDataSecondmouse/labels/train"
    
    path = "F:/Juna/labelstest"
    outputpath = "F:/Juna/traintest"
    
    files = glob.glob(path + '/*.txt')
    
    for f in files:
         object_visibility = TIVIA.AddVisibility(f,outputpath)
         object_visibility()
         
         
    
    
    

if __name__ == "__main__":
    main()