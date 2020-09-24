#!/usr/bin/env python

# Image creator with class

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import time
from std_msgs.msg import String


stime = time.time()
waitkey = 30
class image_receiver():

    def __init__(self, waitkey):
        self.waitkey = waitkey
        self.time_pub = rospy.Publisher('/image_topic/time', String, queue_size = 10)
        self.image_pub = rospy.Publisher('/image_topic/image', Image, queue_size = 10)
        self.bridge = CvBridge()
        image_topic = '/depth_camera/depth/image_raw'
        
        self.image_sub = rospy.Subscriber(image_topic, Image, self.callback)
        cv2.namedWindow('image_window', flags=cv2.WINDOW_NORMAL)#,1
        
    def callback(self, data):
        
        global stime
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
        except CvBridgeError as e:
            print(e)
        
        (rows, cols) = cv_image.shape
        deff_time = time.time() - stime
        self.time_pub.publish('{:.2f}'.format(deff_time))
        cv2.imshow("image_window", cv_image)
        cv2.waitKey(self.waitkey)
    
def main():
    global waitkey
    rospy.init_node('image_receiver', anonymous = True)
    ic = image_receiver(waitkey)
    while not rospy.is_shutdown():
        rospy.spin()
    print('shotting down')
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
        
        
        


