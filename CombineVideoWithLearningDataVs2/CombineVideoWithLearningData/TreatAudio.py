# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 07:59:28 2024

@author: Administrator

Class to read audio and add audio
"""
from moviepy.editor import VideoFileClip
import os

class TreatAudio:
    def  __init__(self,original_video,_outputVideo):
        self.file_original_video = original_video
        self.file_video_landmarks = _outputVideo
        
    '''
    input: original video
    output : extract audio
    '''
    def ExtractAudio(self):
  
       # Load the video clip
       video_clip = VideoFileClip(self.file_original_video)
       #get path of the file
       file_path =  os.path.dirname(self.file_original_video)
       
       # Extract the audio
       audio_clip = video_clip.audio
       
       # Save the audio as a WAV file
       audio_clip.write_audiofile(file_path + '/' + "extracted_audio.wav", codec='pcm_s16le')
       return audio_clip, file_path
   
    
    '''
    input: video, audio
    output : video with audio
    '''
    def AddAudio(self, audio, file_path):
        video = VideoFileClip(self.file_video_landmarks)
        # Convert the audio to a compatible format (if necessary)
        audio = audio.set_fps(video.fps)
        # Set the audio of the video file
        video = video.set_audio(audio)
        # Output path for the final video with added audio
        
        output_path = file_path + '/' + 'video_with_audio.mp4'

        # Write the video file with added audio
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    '''
    Resume all files
    '''
    def  __call__(self):
       audio, file_path = self.ExtractAudio()
       self.AddAudio(audio, file_path)