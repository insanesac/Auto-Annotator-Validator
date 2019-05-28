#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:28:14 2019

@author: insanesac
"""

import csv, os, cv2
import numpy as np
import shutil, random

report_path = 'east_report.txt'
invalid = []
wrong = []

dest1 = os.path.join(os.getcwd(),'invalid')
dest2 = os.path.join(os.getcwd(),'wrong')
def load_annoataion(p):
    '''
    load annotation from the text file
    :param p:
    :return:
    '''
    text_polys = []
    text_tags = []
    if not os.path.exists(p):
        return np.array(text_polys, dtype=np.float32)
    with open(p, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            label = line[-1]
            # strip BOM. \ufeff for python3,  \xef\xbb\bf for python2
            line = [i.strip('\ufeff').strip('\xef\xbb\xbf') for i in line]

            x1, y1, x2, y2, x3, y3, x4, y4 = list(map(float, line[:8]))
            text_polys.append([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
            if label == '*' or label == '###':
                text_tags.append(True)
            else:
                text_tags.append(False)
        return np.array(text_polys, dtype=np.float32), np.array(text_tags, dtype=np.bool)
    
def polygon_area(poly):
    '''
    compute area of a polygon
    :param poly:
    :return:
    '''
    edge = [
        (poly[1][0] - poly[0][0]) * (poly[1][1] + poly[0][1]),
        (poly[2][0] - poly[1][0]) * (poly[2][1] + poly[1][1]),
        (poly[3][0] - poly[2][0]) * (poly[3][1] + poly[2][1]),
        (poly[0][0] - poly[3][0]) * (poly[0][1] + poly[3][1])
    ]
    return np.sum(edge)/2.

def check_and_validate_polys(polys, tags, xxx_todo_changeme,base):
    '''
    check so that the text poly is in the same direction,
    and also filter some invalid polygons
    :param polys:
    :param tags:
    :return:
    '''
    
    (h, w) = xxx_todo_changeme
    if polys.shape[0] == 0:
        return polys
    polys[:, :, 0] = np.clip(polys[:, :, 0], 0, w-1)
    polys[:, :, 1] = np.clip(polys[:, :, 1], 0, h-1)

    validated_polys = []
    validated_tags = []
    for i,poly, tag in enumerate(zip(polys, tags)):
        p_area = polygon_area(poly)
        if abs(p_area) < 1:
            print('invalid poly in file %s, line number %d'%(base,i))
            with open(report_path,'w') as rp:
                rp.writelines('invalid poly : file %s, line number %d\n'%(base,i))
            continue
        if p_area > 0:
            print('poly in wrong direction in file %s, line number %d'%(base,i))
            with open(report_path,'w') as rp:
                rp.writelines('poly in wrong direction : file %s, line number %d\n'%(base,i))
            poly = poly[(0, 3, 2, 1), :]
        validated_polys.append(poly)
        validated_tags.append(tag)
    return np.array(validated_polys), np.array(validated_tags),invalid,wrong

class EastVisualize:
    def validator(img_path,txt_path, test):
        length = len(img_path)
        img = cv2.imread(img_path)
        
        h, w, _ = img.shape
        
        poly,tag = load_annoataion(txt_path)
        poly,tag,invalid,wrong = check_and_validate_polys(poly,tag,(h,w),img_path)
        
        invalid = list(set(invalid))
        wrong = list(set(wrong))
        
        for iv in invalid:
            iv_img = iv
            iv_base = iv.split(',')[0]
            iv_txt = iv_base +'.txt'
            
            shutil.move(iv_img,dest1+os.path.basename(iv_img))
            shutil.move(iv_txt,dest2+os.path.basename(iv_txt))
          
        if test == 'P':
            print('Visualizing random 10 percent data points')
            num_selections = int(length/10)
            new_img_list = random.sample(img_path, num_selections)
            
        else:
            print('Visualizing all data points')
            new_img_list = img_path
            
        
        for imgp in new_img_list:
            cropped = []
            val_img_path = imgp
            val_base = val_img_path.split(',')[0]
            val_txt = val_base + '.txt'
            val_img = cv2.imread(val_img_path)
            with open(val_txt,'r') as t:
                lines = t.readlines()
            for i,line in enumerate(lines):
                split_line = line.split(',')
                y1,x1,y2,x2,y3,x3,y4,x4,label = split_line[:9]
                cv2.rectangle(img,(int(x1),int(y1)),(int(x3),int(y3)),(0,200,0),3)
                
                cropped.append(val_img[int(x1):int(x3),int(y1):int(y3)])
                
                cv2.imshow('cropped %d out of %d'%(i,len(lines)),cropped)
                
                    
                    
                    
                
                
                