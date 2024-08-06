# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 12:00:08 2023

@author: Administrator
"""
import albumentations as A
import cv2
import os
import math

'''
Group of function which help to augment the pictures and to save in the correct format
'''

class AugmentationFunctions:
    def __init__(self,filename,path_folder):
       self._filename = filename
       self._path = path_folder
       #read image
       self._image = cv2.imread(filename) 
      
       self.total_list = []
       self._name = os.path.splitext(os.path.basename(filename))[0]
    
    def arrangeBbox(self):
      
        text_file = self._path + '//labels//train//'+ self._name + '.txt'
       
        #read text box
        f = open(text_file, "r")
        #read each file
        line_all = f.read()
       
        line_all = line_all.split('\n')
        for line in line_all:
           
        #convert into list 
           list_aux = line.split(' ')
           
        #convert into a list order as should be
           if list_aux[0] != '':
            
              list_aux_1 = [float(list_aux[1]),float(list_aux[2]),float(list_aux[3]),float(list_aux[4]),list_aux[0]]
         
           
        
        # do the same with two lines
        #append to another listlist_aux[1]
              self.total_list.append(list_aux_1)
              print(self.total_list) 
        
          
        f.close()
        
        
    def arrangeKeypoints(self):
        
        text_file = self._path + '//labels//train//'+ self._name + '.txt'
        #read text box
        f = open(text_file, "r")
        #read each file
        line_all = f.read()
        line_all = line_all.split('\n')
        for line in line_all:
            #convert into list 
               list_aux = line.split(' ')
               print(list_aux)
                  
        #convert into a list order as should be
               if list_aux[0] != '':  
                  list1 = [float(s) for s in list_aux[5::3]]
                  list1 = [0 if math.isnan(x) else x for x in list1]
                  list2 = [float(s) for s in list_aux[6::3]]
                  list2 = [0 if math.isnan(x) else x for x in list2]
                  self._vis_list = [float(s) for s in list_aux[7::3]]
                  self._paired_tuples = list(zip(list1, list2))
              
        f.close()
        
        
        

    def augmentation(self):
        
        bboxes = self.total_list
        image = self._image
        keypoints = self._paired_tuples
        visibility = self._vis_list
        print(keypoints)
       ###############3
        
       # transform = A.Compose([A.HorizontalFlip(p=0.5)],bbox_params=A.BboxParams(format='yolo'))
        transform = A.Compose([A.VerticalFlip(p=1.0)],bbox_params=A.BboxParams(format='yolo'),keypoint_params=A.KeypointParams(format='yolo'))
       
        transformed = transform(image=image,bboxes = bboxes,keypoints = keypoints)
        transformed_image = transformed["image"]
        transformed_bboxes = transformed['bboxes']
        transformed_keypoints = transformed['keypoints']
        print('silvia')
        transformed_keypoints_vis = [(a, b, l) for (a, b), l in zip(transformed_keypoints,visibility)]
        print(transformed_keypoints_vis)
        #transform into list
        flattened_list_keypoints = [item for sublist in transformed_keypoints_vis for item in sublist]
        #add boxes
        #all_transform_points = transformed_bboxes + flattened_list_keypoints
        #print(all_transform_points)
       ###
       
        # save_pictures = self._path + '//augmentated//images//'+ 'fh_' + self._name + '.png'
        # save_text = self._path + '//augmentated//labels//'+ 'fh_' + self._name + '.txt'
        save_pictures = self._path + '//augmentated//images//'+ 'fv_' + self._name + '.png'
        save_text = self._path + '//augmentated//labels//'+ 'fv_' + self._name + '.txt'
        print(save_pictures)
        #save picture
        cv2.imwrite(save_pictures, transformed_image)
        
        #save text
        count=0
        string_list = []
        file1= open(save_text,"w")
        for l in transformed_bboxes:
            laux = [l[0],l[1],l[2],l[3]] + flattened_list_keypoints
            laux_string = ' '.join([str(item) for item in laux])
            laux_string = str(count) + ' ' + laux_string + "\n"
            
            string_list.append(laux_string)
            count = count + 1
        file1.writelines(string_list)
        file1.close()
        print('SilviaFinished')
        
    def augmentationImageHorizontal(self):
            #arrange path
            aux_1 = self._filename.split('\\')
            aux_2 = aux_1[len(aux_1)-1].split('.')
            self._name = aux_2[0]
            image = self._image
           ###############3
            
            transform = A.Compose([A.HorizontalFlip(p=1.0)]) #100% probability to flip
            #transform = A.Compose([A.VerticalFlip(p=0.5)],bbox_params=A.BboxParams(format='yolo'))
           
            transformed = transform(image=image)
            transformed_image = transformed["image"]
           
           ###
           
            save_pictures = self._path + '//augmentated//images//'+ 'fh_' + self._name + '.png'
            print(save_pictures)
           
            #save picture
            cv2.imwrite(save_pictures, transformed_image)
            
    def augmentationImageVertical(self):
              
                image = self._image
               ###############3
                
                transform = A.Compose([A.VerticalFlip(p=1.0)])
                #transform = A.Compose([A.VerticalFlip(p=0.5)],bbox_params=A.BboxParams(format='yolo'))
               
                transformed = transform(image=image)
                transformed_image = transformed["image"]
               
               ###
                print(self._name)
                save_pictures = self._path + '//augmentated//images//'+ 'fv_' + self._name + '.png'
               
                #save picture
                cv2.imwrite(save_pictures, transformed_image)
            
            
#Auxiliary functions
def verify(list_data):
    
    index = 0
    for index in range(4):
        if  list_data[index] < 0:
          list_data[index] = 0
        index = index +1
    return list_data