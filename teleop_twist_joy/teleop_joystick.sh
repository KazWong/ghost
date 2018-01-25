#!/bin/bash

source /opt/ros/indigo/setup.bash
source /home/sae/r2d2_navigation_cps/devel/setup.bash
source /home/sae/r2d2/devel/setup.bash

export ROS_MASTER_URI=http://192.168.1.103:11311
export ROS_IP=192.168.1.103

roslaunch teleop_twist_joy teleop.launch
read
