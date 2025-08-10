# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:32:40 2023

@author: Administrator
"""

#Get frames from a video
#1-create video object
#2- find number of frames
#3- do a list with random numbers
#4- go through each frame of the list and save it

import cv2
import random


class GetFramesFromVideo:
    def __init__(self,inputMovie,outputFolder,nframes_to_take):
      self._input = inputMovie
      self._outputFolder = outputFolder
      self._totalframecount = 0
      self._randomlist = []
      self._nframes = nframes_to_take
      
    def read_video(self):
        self._vobj = cv2.VideoCapture(self._input)
        self._totalframecount = int(self._vobj.get(cv2.CAP_PROP_FRAME_COUNT))
        return self._vobj,self._totalframecount 
        
    def Create_list_frames(self,selected_frames):
       #select frames either randomic or manually
        if len(selected_frames) == 0:
         #Generate n random numbers between 0 and number of frames
         self._randomlist = random.sample(range(0, self._totalframecount), self._nframes)
        else:
         self._randomlist = selected_frames  
        
    def Get_video(self,start_image):
        count = start_image
        for frame_id in self._randomlist:
            self._vobj.set(cv2.CAP_PROP_POS_FRAMES,frame_id)
            ret,frame = self._vobj.read()
            if ret:
               text_frame = f"Frame ID: {frame_id}"
               font = cv2.FONT_HERSHEY_SIMPLEX
               font_scale = 1
               color = (0, 255, 0)  # Green
               thickness = 2
               cv2.putText(frame, text_frame, (10, 70), font, font_scale, color, thickness, cv2.LINE_AA)
             # if video is still left continue creating images
               name = self._outputFolder + "/" + str(count) +"_image.png"
               cv2.imwrite(name,frame)
               count += 1
            else:
                break
        self._vobj.release()
    #    cv2.destroyAllWindows()
        
def Get_Results(inputMovie,outputFolder,nframestotake,selected_frames,start_image):
    new_object = GetFramesFromVideo(inputMovie,outputFolder,nframestotake)
    new_object.read_video()
    new_object.Create_list_frames(selected_frames)
    new_object.Get_video(start_image)
    start_image = start_image + nframestotake
    return start_image 