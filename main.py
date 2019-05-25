#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:16:25 2019

@author: insanesac
"""

import os
import cv2

def txt_path_reader(dataset):
    txt_files = []
    files = os.listdir(dataset)
    for file in files:
        if 'txt' in file.lower():
            txt_files.append(os.path.join(dataset,file))
    length = len(txt_files)
    print('Total number of text files found in dataset folder ----> %d'%length)
    return txt_files


def image_path_reader(dataset):
    img_files = []
    files = os.listdir(dataset)
    for file in files:
        if 'jpg' in file.lower() or 'jpeg' in file.lower():
            img_files.append(os.path.join(dataset,file))
    length = len(img_files)
    print('Total number of images found in dataset folder ----> %d'%length)
    return img_files

import argparse

parser = argparse.ArgumentParser(description='Auto Annotator')

parser.add_argument('--option', type = str, help='Annotator(A) or Validator(V) or Trainer(T)')
parser.add_argument('--dataset', type = str, help='path to dataset')
parser.add_argument('--mode', type = int, help='0 -> myntra east, 1 -> myntra mask, 2 -> bajaj rcnn')
parser.add_argument('--test', type = int, help='F -> Visualize full data, P -> Visulaize random 10 percent', default = 'P')

args = vars(parser.parse_args())

dataset = args['dataset']
mode = args['mode']
option = args['option']
test = args['test']

if mode == 0:
    mode_name = 'EAST'
elif mode == 1:
    mode_name = 'MASK'
else:
    mode_name = 'RCNN'
print('\n')
print('Dataset path ---->%s'%dataset)
print('Mode chosen  ---->%s'%mode_name)

img_list = image_path_reader(dataset)

if len(img_list)  == 0:
    raise Exception({'message': 'No images found in dataset folder'})

if option == 'A':
    print('\n')
    print('Setting up Annotator')
    if mode == 0:
        print('\n')
        print('Switching to EAST mode')
        print('\n')
        from east_main import EastAnnot
        EastAnnot.inference(img_list)
        
    elif mode == 1:
        print('\n')
        print('Switching to MASKNET mode')
        print('\n')
        from mask_main import MaskAnnot
        MaskAnnot.inference(img_list)
    
    elif mode == 2:
        print('\n')
        print('Switching to RCNN mode')
        print('\n')
        from rcnn_main import RcnnAnnot
        RcnnAnnot.inference(img_list)
    
            
elif option == 'V':
    print('\n')
    print('Setting up Validator')
    
    txt_list = txt_path_reader(dataset)
    if len(txt_list)  == 0:
        raise Exception({'message': 'No text annotation files found in dataset folder'})

    if mode == 0:
        print('\n')
        print('Switching to EAST mode')
        print('\n')
        from east_main import EastValid
        EastValid.verify(img_list,txt_list,test)
        
    elif mode == 0:
        print('\n')
        print('Switching to MASKNET mode')
        print('\n')
        from mask_main import MaskValid
        MaskValid.verify(img_list, txt_list)
        
    elif mode == 0:
        print('\n')
        print('Switching to RCNN mode')
        print('\n')
        from rcnn_main import RcnnValid
        RcnnValid.verify(img_list,txt_list)
    
else:
    print('\n')
    print('Setting up Trainer')
    
    if mode == 0:
        print('\n')
        print('Switching to EAST mode')
        print('\n')
        
        



    
