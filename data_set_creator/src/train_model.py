#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Build a model for predict robot next progress


import pickle
import numpy as np
from tensorflow.keras.layers import Input, Dense, Conv3D, Dropout, Flatten, Conv2D
from tensorflow.keras import Model
from tensorflow.keras.utils import to_categorical
import numpy as np
import cv2

def get_data_from_file(path_name):
    # Get the path of the pickle file and return array of data.
    with open(path_name,'rb') as f:
        try:
            data=[]
            while True:
                data.append(pickle.load(f, encoding='bytes'))
        except EOFError:
            pass
    f.close()
    data_concatenate=[]
    for i in data:
        data_concatenate+=i
    # data_concatenate = [[i[0].decode('utf-8'), i[1]] for i in data_concatenate]
    return data_concatenate

def open_imgs(data, path):
    imgs = []
    for sample in data:
        img_name = path+'/'+sample
        imgs.append([cv2.imread(img_name+'_1.jpg')/255,
                    cv2.imread(img_name+'_2.jpg')/255,
                    cv2.imread(img_name+'_3.jpg')/255])
    return imgs

path = '/home/lab/Orel_ws/Training_data'
data = get_data_from_file(path +'/output')
K = 4 # 4 optional key press 
data = np.asarray(data)

x_train = open_imgs(data[:,0], path)
y_train = np.zeros((len(data),K))

for i,j in zip(data[:,1],range(len(data))): # convert to One hot Ecoded
    y_train[j,int(i)-1] = 1
# y_train = to_categorical(data[:,1]) # Second method to convert
# y_train = y_train[:,1:]


'''
Sample one keypress and display the three imgs in buffer
indx = np.random.choice(len(x_train))
one_two = np.concatenate((x_train[indx][0], x_train[indx][1]), axis = 1)
three_zero = np.concatenate((x_train[indx][2], np.zeros(x_train[0][0].shape, dtype='uint8')), axis = 1)
three = np.concatenate((one_two, three_zero), axis =0)
cv2.imshow('img',three)
'''

i = Input(shape = (128 ,128, 3))

x = Conv2D(32, (3,3), strides=(2,2), activation='relu') (i)
x = Conv2D(64, (3,3), strides=(2,2), activation = 'relu') (x)
x = Conv2D(128, (3,3), strides=(2,2), activation ='relu') (x)

x = Flatten()(x)
# x = Dropout(0.5)(x)
x = Dense(1024, activation='relu')(x)
# x = Dropout(0.2)(x)
x = Dense(K, activation='softmax')(x)

model = Model(i,x)

model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])
r = model.fit(x_train, y_train, validation_data=0.3, epochs=10)


    