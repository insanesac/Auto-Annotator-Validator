#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:16:25 2019

@author: insanesac
"""

import os
import cv2

MYNTRA_MASK_PATH = r'/home/insanesac/workspace/Auto-annotators/trained_models/mask_rcnn_tags_0060.h5'

MYNTRA_EAST_PATH = r'/home/insanesac/workspace/Auto-annotators/trained_models/east/checkpoint'

BAJAJ_FASTER_RCNN_PATH = r''

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

args = vars(parser.parse_args())

dataset = args['dataset']
mode = args['mode']

option = args['option']

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
        EastValid.verify(img_list,txt_list)
    
else:
    print('\n')
    print('Setting up Trainer')
    
    txt_list = txt_path_reader(dataset)
    if len(txt_list)  == 0:
        raise Exception({'message': 'No text annotation files found in dataset folder'})
    if mode == 0:
        print('\n')
        print('Switching to EAST mode')
        print('\n')
        
        



    
