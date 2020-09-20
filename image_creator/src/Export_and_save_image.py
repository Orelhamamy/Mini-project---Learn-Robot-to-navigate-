#!/usr/bin/env python3

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2
import time


stime = time.time()
def image_listener(image):
    global stime
    diff_time = time.time() - stime
    print('image receive %.2f' % diff_time)
    bridge = CvBridge()
    try:
        cv_img = bridge.imgmsg_to_cv2(image, "32FC1")
        print ('123')
    except CvBridgeError as e:
        print(e)
    #cv2.imshow(cv_img)
if __name__ == '__main__':
    rospy.init_node('image_creator', anonymous ='True')
    rate = rospy.Rate(1)
    image_topic = '/depth_camera/depth/image_raw'
    while not rospy.is_shutdown():
        rospy.Subscriber(image_topic, Image, image_listener)
        rate.sleep()
    print('finish')
    