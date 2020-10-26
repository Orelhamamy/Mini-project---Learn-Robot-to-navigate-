#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display random 3 input, and print the output
"""

# Need to import x_data from train_model x_data[:326] -> interval = 0.75 ; x_data[326:] -> interval = 1
import numpy as np
import cv2

samples = x_data.shape[0]

test = np.random.randint(326,samples)
x_sample = x_data[test,:,:,0]
x_sample = np.concatenate((x_sample,np.ones((128,5)),
                           x_data[test,:,:,1],np.ones((128,5)),
                           x_data[test,:,:,2]),axis = 1 )
cv2.imshow('test',x_sample)
print(y_data[test].argmax())
