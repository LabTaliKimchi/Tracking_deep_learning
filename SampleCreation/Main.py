# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 09:40:20 2023

@author: Administrator
"""

import cv2
import AuxiliaryFiles as AF


def main():
    count = 0

    outputfile = 'F:/YaelShammaiData/data/images/train/'
    video_file = 'X:/Users/Members/Yael_Shammai/results/behavioral assays/social interaction/20230801 C57-BTBR + Balbc pilot/upward view/BTBR 103-1m.avi'
    list_frames = [5333,5713,5796,3209,3308,3424,6616,7674,10419,10502,10601,10765,11377,16422,16885,17099,17149,17546,17811,23384,24056,25782,30627]
    
    video = cv2.VideoCapture(video_file)
    for frame_id  in  list_frames:
        count += 1
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        namefile = outputfile + str(count) + '_image' + '.png'
        cv2.imwrite(namefile, frame)
        

if __name__ == "__main__":
    main()











