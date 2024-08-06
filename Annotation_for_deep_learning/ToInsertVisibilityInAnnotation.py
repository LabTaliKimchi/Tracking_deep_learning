# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 09:40:45 2023

@author: Administrator
"""
import numpy as np

'''
Class add visibility to the annotation data in keypoints

IN dim=3 visibility values are = 0 not visible
1 is partial visible
2 is visible

Steps for the script:
    1)- Read the files from the folder
    2)- for each file read the text with  f.read
    3)- split the string into a list
    4)- insert  the number 2 after the keypoints coordinates
    if the element before is nan insert 0
    4)- convert into string
    5)- save in txt file
'''


class  AddVisibility:
      def __init__(self,f,outputpath):
          self._filename = f
          self._output = outputpath
          
         
    
      def readFile(self):
          with open(self._filename) as f:
               _contents = f.read()   
          f.close()
          return _contents
          
      
      def splitText(self,_contents):
          _list = _contents.split(" ")
          #get rid of  \n
          _list[len(_list)-1]=((_list[len(_list)-1]).split('\n'))[0]
          return _list
      
      '''
         Insert only numbers in the keypoints
      '''
      def insertData(self, _list):
          aux_list = _list.copy() 
          count =0
          for index in range(5,len(_list)-2,2):
              if _list[index] == "nan":

                  aux_list.insert(index+count+2,"0")
                  #add value to nan
                  aux_list[index+count+2-1] ="0"
                  aux_list[index+count+2-2] ="0"
              else:
                  aux_list.insert(index+count+2,"2")
              count = count + 1 
          #at the end 
          if _list[len(_list)-1] == "nan":

               aux_list.insert(len(aux_list),"0\n")
               aux_list[len(aux_list)-2] ="0"
               aux_list[len(aux_list)-3] ="0"
          else:
               aux_list.insert(len(aux_list),"2\n")    
          return aux_list
          
      
      def Join_list(self,aux_list):
          string = ' '.join([str(item) for item in aux_list])
          return string
      
      def SaveString(self, string):
          aux_list = self._filename.split("\\")
          outputfile = self._output + "/" + aux_list[len(aux_list) - 1]
          with open(outputfile, 'w') as f:
              f.write(string)
          f.close()
          
      def __call__(self):
          _contents = self.readFile()
          _list = self.splitText(_contents)
          aux_list = self.insertData(_list)
          string = self.Join_list(aux_list)
          self.SaveString(string)