#!/usr/bin/env python2.7



import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
import cv2
import pickle

intervals = .75 # Sec between images
height = 128
width = 128

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
        cv2.imwrite('{}/{}.jpg'.format(path, titles[0]), self.img_one)
        cv2.imwrite('{}/{}.jpg'.format(path, titles[1]), self.img_two)
        cv2.imwrite('{}/{}.jpg'.format(path, titles[2]), self.img_three)
        return '{:.2f}'.format(time)

def get_data(event, img_buffer, bridge):
    img_msg = rospy.wait_for_message('/depth_camera/color/image_raw', Image)
    img = bridge.imgmsg_to_cv2(img_msg)
    img_buffer.recive_img(img)
    print(rospy.get_time())

def save_data_set(path, name, data):
    f = open('{}/{}'.format(path, name),'ab')
    pickle.dump(data, f)
    f.close()
    print('save {:s}'.format(name))
    
def main(bridge):
    # st = rospy.get_time()
    global intervals
    path='/home/lab/Orel_ws/Training_data'
    img_msg = rospy.wait_for_message('/depth_camera/color/image_raw', Image)
    img_buffer = images_buffer(bridge.imgmsg_to_cv2(img_msg))
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



    
