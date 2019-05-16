#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 17:03:17 2019

@author: insanesac
"""
import cv2,os
from east_invoke import East
import pytesseract as pt
import numpy as np
from east_single_validate import validator 

def ocr(cropped):
    cropped = threshold_attr(cropped)
    ocr = pt.image_to_string(cropped, config='--psm 6')
    return ocr

def threshold_attr(image):
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    resized_gray_2x = cv2.resize(gray_image,None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC)
    threshold_2x = cv2.adaptiveThreshold(resized_gray_2x,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,151,13)
    threshold_eroded_2x = cv2.erode(threshold_2x,np.ones((2,5)))
    return threshold_eroded_2x

class EastAnnot():
    def inference(img_list):
        for path in img_list:
            base = os.path.basename(path)
            print('Annotating file --------> %s'%base)
            direc = path.replace(base,'')
            txt_path = os.path.join(direc,base.split('.')[0])+'.txt'
            img = cv2.imread(path)
            boxes = East.segment(img)
                    
            final_annot = []
            
            for i,box in enumerate(boxes):
                x_min,y_min = box[0]
                x_max,y_max = box[2]
                
                cropped_img = img[int(y_min)-2:int(y_max)+2,int(x_min)-2:int(x_max)+2,:]
                read_label = ocr(cropped_img).replace('\n','')
                x1, y1 = x_min, y_min
                x2, y2 = x_min, y_max
                x3, y3 = x_max, y_max
                x4, y4 = x_max, y_min
                ordered_txt = [str(int(y1)), str(int(x1)), str(int(y2)), str(int(x2)), str(int(y3)), str(int(x3)), str(int(y4)), str(int(x4)), read_label]
                final_annot.append(",".join(ordered_txt))
                
            with open(txt_path,'w') as txt:
                for annot in final_annot:
                    txt.write("%s\n"%annot)
                    
class EastValid():
    def verify(img_list):
        for path in img_list:
            base = os.path.basename(path)
            print('Validating file --------> %s'%base)
            direc = path.replace(base,'')
            txt_path = os.path.join(direc,base.split('.')[0])+'.txt'
            validator(path,txt_path)
            
class EastTrain():
    def train():            
        print('Initializing Trainer')
                