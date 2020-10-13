#!/usr/bin/env python

from getkey import getkey, keys
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

rospy.init_node('teleop_by_arrows')
pub_vel_cmd = rospy.Publisher('cmd_vel', Twist, queue_size=5)
key_publisher = rospy.Publisher('/image_topic/key_press', Int16, queue_size=1)
linear_speed = 0.5
angular_speed = 0.4
duration = 1


def stop():
    global pub_vel_cmd
    msg = Twist()
    msg.linear.x = 0 
    msg.angular.z = 0
    pub_vel_cmd.publish(msg)

    
def move(linear, angular):
    # print(rospy.get_time())
    global pub_vel_cmd, duration
    msg = Twist()
    msg.linear.x = linear 
    msg.angular.z = angular
    pub_vel_cmd.publish(msg)
    # rospy.sleep(duration)
    # stop()
    
        
def listener():
    global angular_speed, linear_speed
    key = getkey()
    while not rospy.is_shutdown():
        while not key:
            True
        if key==keys.UP:
            key_publisher.publish(1)
            print(rospy.get_time())
            move(linear_speed,0)
        elif key==keys.DOWN:
            key_publisher.publish(2)
            print(rospy.get_time())
            move(-linear_speed,0)
        elif key==keys.RIGHT:
            key_publisher.publish(3)
            print(rospy.get_time())
            move(0,-angular_speed)
        elif key==keys.LEFT:
            key_publisher.publish(4)
            print(rospy.get_time())
            move(0,angular_speed)
        elif key=='q':
            linear_speed = linear_speed*1.1
        elif key=='a':
            linear_speed = linear_speed*0.9
        elif key=='w':
            angular_speed = angular_speed*1.1
        elif key=='s':
            angular_speed = angular_speed*0.9
        key = getkey()
        
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException or KeyboardInterrupt:
        stop()
    
'''
hape = (None, image.shape[0], image.shape[1], 3)
shape = (None, 128,128, 3) 
'''
