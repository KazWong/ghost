#!/usr/bin/env python

import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

MAX_LIN_VEL = 0.6 #4.916592502868
MAX_ANG_VEL = 1.570796326 #4.71238898
PUB_HZ = 5.0
joy = Joy()
cmd_vel_msg = Twist()

def callback(msg):
    global joy
    joy = msg

def main():
    rospy.init_node('joy2cmd_vel', anonymous=True)

    rospy.Subscriber('joy', Joy, callback, queue_size = 1)
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_msg.linear.y = 0.0
    cmd_vel_msg.linear.z = 0.0
    cmd_vel_msg.angular.z = 0.0
    
    old_joy4 = 0;
	
    while not rospy.is_shutdown():
        if (len(joy.axes) > 0):
            cmd_vel_msg.linear.x = MAX_LIN_VEL * joy.axes[1]
            cmd_vel_msg.linear.y = 0.0 #MAX_LIN_VEL * joy.axes[0]
            cmd_vel_msg.angular.z = MAX_ANG_VEL * joy.axes[3]
        else:
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.linear.y = 0.0
            cmd_vel_msg.angular.z = 0.0

        if (len(joy.buttons) > 0):
            if (joy.buttons[0] == 1):
                cmd_vel_msg.linear.z = 0.1
            if (joy.buttons[7] == 1):
                cmd_vel_msg.linear.z = 0.2
            if (joy.buttons[1] == 1):
                cmd_vel_msg.linear.z = 0.3
            if (joy.buttons[0] == 0 and joy.buttons[1] == 0 and joy.buttons[7] == 0):
                cmd_vel_msg.linear.z = 0.0
                
            if (joy.buttons[4] == 1):
                cmd_vel_pub.publish(cmd_vel_msg)
            elif (joy.buttons[4] == 0 and old_joy4 == 1):
                cmd_vel_msg.linear.x = 0.0
                cmd_vel_msg.linear.y = 0.0
                cmd_vel_msg.angular.z = 0.0
                cmd_vel_pub.publish(cmd_vel_msg)
            old_joy4 = joy.buttons[4]
            
        rospy.sleep(1./PUB_HZ)
	
    rospy.spin()

if __name__ == '__main__':
    main()
