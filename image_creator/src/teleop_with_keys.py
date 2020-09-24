#!/usr/bin/env python

from getkey import getkey, keys
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

rospy.init_node('teleop_by_arrows')
pub_vel_cmd = rospy.Publisher('cmd_vel', Twist,queue_size=1)
key_publisher = rospy.Publisher('/image_topic/key_press', Int16,queue_size=1)
linear_speed = 0.5
angular_speed = 0.2
def stop():
    global pub_vel_cmd
    msg = Twist()
    msg.linear.x = 0 
    msg.angular.z = 0
    pub_vel_cmd.publish(msg)

    
def move(linear, angular):
    global pub_vel_cmd
    msg = Twist()
    msg.linear.x = linear 
    msg.angular.z = angular
    pub_vel_cmd.publish(msg)
    rospy.sleep(0.5)
    stop()
    
        
def listener():
    global angular_speed, linear_speed
    key = getkey()
    while not rospy.is_shutdown():
        while not key:
            True
        if key==keys.UP:
            move(linear_speed,0)
            key_publisher.publish(1)
        elif key==keys.DOWN:
            move(-linear_speed,0)
            key_publisher.publish(2)
        elif key==keys.RIGHT:
            move(0,-angular_speed)
            key_publisher.publish(3)
        elif key==keys.LEFT:
            move(0,angular_speed)
            key_publisher.publish(4)
        key = getkey()
        
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    
    

