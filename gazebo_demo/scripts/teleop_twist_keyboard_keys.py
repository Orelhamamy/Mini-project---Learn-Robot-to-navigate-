#!/usr/bin/env python

from getkey import getkey, keys
import rospy
from geometry_msgs.msg import Twist
import time

rospy.init_node('teleop_by_arrows')
pub_vel_cmd = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
senstive = 1

def stop(pub, msg): # msg - geometry_msg - Twist
    msg.linear.x = 0 
    msg.angular.z = 0
    pub.publish(msg)
    
def move(linear, angular):
    global pub_vel_cmd, senstive
    msg = Twist()
    msg.linear.x = linear * senstive
    msg.angular.z = angular * senstive
    pub_vel_cmd.publish(msg)
    time.sleep(.75)
    stop(pub_vel_cmd, msg)
    
        
def listener():
    global senstive
    key = getkey()
    while not rospy.is_shutdown():
        while not key:
            True
        if key==keys.UP:
            move(0.5,0)
        elif key==keys.DOWN:
            move(-0.5,0)
        elif key==keys.RIGHT:
            move(0,-1)
        elif key==keys.LEFT:
            move(0,1)
        elif key=='q':
            senstive = senstive*1.1
        elif key=='a':
            senstive = senstive*0.9
        key = getkey()
        
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    
    