#!/usr/bin/env python2.7



import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
import cv2
import pickle
import numpy as np

intervals = 1 # Sec between images
height = 128
width = 128
depth_camera = '/depth_camera/depth/image_raw'
color_camera = '/depth_camera/color/image_raw'
class images_buffer():
    def __init__(self, img):
        img = cv2.resize(img,(width, height))
        self.img_zero = img
        self.img_one = img
        self.img_two = img
        self.img_three = img
    
    def recive_img(self, new_img):
        new_img = cv2.resize(new_img,(width, height))
        self.img_three = self.img_two
        self.img_two = self.img_one
        self.img_one = self.img_zero
        self.img_zero = new_img
    
    def save_as_jpg(self, path =''):
        time = rospy.get_time()
        titles = [('{:.2f}_{:d}'.format(time, i+1)) for i in range(3)]
        np.save('{}/{}'.format(path, titles[0]), self.img_one)
        np.save('{}/{}'.format(path, titles[1]), self.img_two)
        np.save('{}/{}'.format(path, titles[2]), self.img_three)
        '''
        cv2.imwrite('{}/{}.jpg'.format(path, titles[0]), self.img_one)
        cv2.imwrite('{}/{}.jpg'.format(path, titles[1]), self.img_two)
        cv2.imwrite('{}/{}.jpg'.format(path, titles[2]), self.img_three)
        ''' 
        return '{:.2f}'.format(time)

def get_data(event, img_buffer, bridge):
    global depth_camera, color_camera
    img_msg = rospy.wait_for_message(depth_camera, Image)
    img = bridge.imgmsg_to_cv2(img_msg, desired_encoding ="passthrough")
    ''' Display Img from depth camera
    img_10 = img*0.1
    cv2.imshow('123',img_10)
    cv2.waitKey(20)
    '''
    img_buffer.recive_img(img)
    print(rospy.get_time())

def save_data_set(path, name, data):
    f = open('{}/{}'.format(path, name),'ab')
    pickle.dump(data, f)
    f.close()
    print('save {:s}'.format(name))
    
def main(bridge):
    # st = rospy.get_time()
    global intervals, depth_camera, color_camera
    path='/home/lab/Orel_ws/Training_data'
    img_msg = rospy.wait_for_message(depth_camera, Image)
    try: 
        img_buffer = images_buffer(bridge.imgmsg_to_cv2(img_msg))
    except CvBridgeError:
        pass 
    get_data_lambada = lambda x: get_data(x, img_buffer, bridge)
    output = []
    # output_with_img = []
    try:
        rospy.Timer(rospy.Duration(intervals), get_data_lambada)
        while not rospy.is_shutdown():
            key = rospy.wait_for_message('/image_topic/key_press', Int16)
            time = img_buffer.save_as_jpg(path=path)
            # output_with_img.append([img_buffer.img_one, img_buffer.img_two,
            #                         img_buffer.img_three, key.data])
            output.append([time, key.data])
            print('img capture at {}'.format(time))      
    except KeyboardInterrupt:
        save_data_set(path, 'output', output)
        # save_data_set(path, 'session_{:.0f}'.format(st), output_with_img)

if __name__=='__main__':
    rospy.init_node('image_creator')
    bridge = CvBridge()
    main(bridge)



    
