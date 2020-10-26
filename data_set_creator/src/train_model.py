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
import matplotlib.pyplot as plt


def get_data_from_file(path_name):
    # Get the path of the pickle file and return array of data.
    with open(path_name,'rb') as f:
        try:
            data=[]
            data_concatenate=[]
            count = 0
            while True:
                data.append(pickle.load(f, encoding='bytes'))
                if not np.shape(data[count])==(0,):
                    if data_concatenate==[]:
                        data_concatenate = data[count]
                    else:
                        data_concatenate = np.concatenate((data_concatenate,data[count]),axis=0)
                count+=1
        except EOFError:
            pass
    f.close()
    # data_concatenate=[]
    # for i in data:
    #     data_concatenate = np.concatenate((data_concatenate,i),axis=0)
    data_concatenate = [[i[0].decode('utf-8'), int(i[1])] for i in data_concatenate] # .decode('utf-8')
    return data_concatenate

def open_imgs(data, path):
    imgs = []
    for sample in data:
        img_name = path+'/'+sample
        imgs.append(np.concatenate((np.expand_dims(np.load(img_name+'_1.npy'),2)/10,
                    np.expand_dims(np.load(img_name+'_2.npy'),2)/10,
                    np.expand_dims(np.load(img_name+'_3.npy'),2)/10), axis = 2))
    return imgs

def divide_data(x_data, y_data, validation):
    # validation - reprecent the size of test samples [0,1).
    # x_data as array
    # return x_train, y_train , x_test, y_test
    batch = np.asarray(range(len(x_data)))
    np.random.shuffle(batch)
    test = int(np.floor(len(x_data)*validation))
    x_test , y_test = x_data[:test] , y_data[:test]
    x_train, y_train = x_data[test:], y_data[test:]
    return x_train, y_train , x_test, y_test
    

path = '/home/lab/Orel_ws/Training_data'
data = get_data_from_file(path +'/output')
K = 4 # 4 optional key press 
data = np.asarray(data)

x_data = np.asarray(open_imgs(data[:,0], path), dtype = 'float32')

y_data = np.zeros((len(data),K),dtype ='float32')
for i,j in zip(data[:,1],range(len(data))): # convert to One hot Ecoded
    y_data[j,int(i)-1] = 1


# y_train = to_categorical(data[:,1]) # Second method to convert
# y_train = y_train[:,1:]

x_train, y_train, x_test, y_test = divide_data(x_data, y_data, 0.3)
'''
Sample one keypress and display the three imgs in buffer
indx = np.random.choice(len(x_train))
one_two = np.concatenate((x_train[indx][0], x_train[indx][1]), axis = 1)
three_zero = np.concatenate((x_train[indx][2], np.zeros(x_train[0][0].shape, dtype='uint8')), axis = 1)
three = np.concatenate((one_two, three_zero), axis =0)
cv2.imshow('img',three)
'''

i = Input(shape = (128 ,128, 3))

# x = Conv2D(8, (3,3), strides=(4,4), padding='same', activation='relu') (i) # 32x32x8
# x = Conv2D(16, (3,3), strides=(2,2), padding='same', activation = 'relu') (x) # 16x16x16
# x = Conv2D(32, (3,3), strides=(4,4), padding='same', activation ='relu') (x) # 4x4x32

x = Conv2D(8, (3,3), strides=(4,4), activation='relu') (i) # 32x32x8
x = Conv2D(16, (3,3), strides=(2,2), activation = 'relu') (x) # 16x16x16
x = Conv2D(32, (3,3), strides=(4,4), activation ='relu') (x) # 4x4x32

x = Flatten()(x)
# x = Dropout(0.5)(x)
x = Dense(512, activation='relu') (x)
# x = Dropout(0.2)(x)
x = Dense(K, activation='softmax') (x)

model = Model(i,x)

model.compile(optimizer = 'adam',
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

r = model.fit(x_train, y_train,validation_data = (x_test, y_test), epochs=500)

plt.figure()
plt.plot(r.history['loss'], label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

plt.figure()
plt.plot(r.history['accuracy'], label='accuracy')
plt.plot(r.history['val_accuracy'],label='val_accuracy')
plt.legend()
plt.show()
