#!/usr/bin/env python

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2


def timed_msg(event):
    print('in_function')
    cv2.namedWindow('image_rate', flags=cv2.WINDOW_NORMAL)
    img_msg = rospy.wait_for_message('/depth_camera/depth/image_raw', Image)
    bridge = CvBridge()
    try:
        img_cv = bridge.imgmsg_to_cv2(img_msg, 'passthrough')
    except CvBridgeError as e:
        print(e)
    cv2.imshow('image_rate',img_cv)
    print('img_display')
        
if __name__ == '__main__':
    rospy.init_node('Timer_exp')
    # cv2.namedWindow('image_rate', flags=cv2.WINDOW_NORMAL)
    timer = rospy.Timer(rospy.Duration(0.5), timed_msg)
    while not rospy.is_shutdown():
        True
    print("\nshow is over")
    cv2.destroyAllWindows()
        
    
