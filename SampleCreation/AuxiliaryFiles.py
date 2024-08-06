# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 08:34:36 2023

@author: Administrator
"""

'''
Auxiliary functions
'''

def Condition_function(count1,count2,count3,count4):
    if (count1 < 9) and (count2 == 0) and (count3 == 0) and (count4 == 0):
        count1 += 1
    elif (count1 == 9 and count2 < 9 and count3 == 0 and count4 == 0):
        count2 += 1
    elif (count1 == 9 and count2 == 9 and count3 < 9 and count4 == 0):
        count3 += 1
    elif (count1 == 9 and count2 == 9 and count3 == 9 and count4 < 9):
        count4 += 1
    return count1, count2, count3, count4