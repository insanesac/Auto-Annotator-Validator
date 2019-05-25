#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:30:53 2019

@author: insanesac
"""
#import csv
#
#header = ['filename','file_size','file_attributes','region_count','region_id','region_shape_attributes']
#
#a = ['united colors of benettonUCB (1).jpg	102288',	'{}',	'5',	'0','{"name":"polygon","all_points_x":[296,331,371,379,382,383,383,374,343,297,293,292,292,297],"all_points_y":[505,506,506,506,512,598,620,622,621,621,616,535,510,506]}	{}']
#
#with open('customers.csv', 'wt') as f:
#    csv_writer = csv.writer(f)
# 
#    csv_writer.writerow(header) # write header
# 
import numpy as np

A = [[1, 1, 1],
     [3, 2, 1],
     [2, 1, 2]]
Ainv = np.linalg.inv(A)
