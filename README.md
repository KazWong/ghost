# Ghost package
A package to launch core nodes for robots.  

Ghost package also build the self-define msg, srv, and actionlib.

## How to Use

1. Create a launch file to organize the nodes to be called.
2. Add that launch file into boot.launch.
3. Add the arg in the top of boot.launch.

For example, to spawn a robot in ROS:  

1. Create a tf.launch file, set the args and call the nodes.  
  Those are the args and parameters of the node in tf.launch.  
```
<arg name="ns" default=""/>
<arg name="config" default="$(find ghost)"/>
<arg name="robot" default="robot"/>
<arg name="joint_pub" default="false"/>
<arg name="shift_x" default="0.0"/>
<arg name="shift_y" default="0.0"/>
<arg name="shift_z" default="0.0"/>  
<!-- Parsing xacro and setting robot_description parameter -->
<param name="robot_description"
       command="$(find xacro)/xacro '$(arg config)/urdf/$(arg robot).urdf.xacro'" />
```
Call the node with the arg (here is robot_state_publisher)
```
<!-- Starting robot state publish which will publish tf -->
<node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher">
  <!-- <param if="$(arg sim)" name="publish_frequency" type="double" value="50.0" /> -->
  <param name="tf_prefix" type="string" value="$(arg ns)" />
  <param name="use_tf_static" type="bool" value="true" />
  <param name="ignore_timestamp" type="bool" value="true" />
</node>
```

2. In boot.launch, include the tf.launch and set the args.  
arg for tf.launch
```
<!-- tf -->
<arg name="robot" default=""/>
<arg name="joint_pub" default="false"/>
<arg name="shift_x" default="0.0"/>
<arg name="shift_y" default="0.0"/>
<arg name="shift_z" default="0.0"/>
```
call tf.launch with the args.
```
<!-- tf -->
<include if="$(arg tf)" file="$(find ghost)/launch/tf.launch">
  <arg name="ns" value="$(arg ns)"/>
  <arg name="config" value="$(arg config_urdf)"/>
  <arg name="robot" value="$(arg robot)"/>
  <arg name="joint_pub" value="$(arg joint_pub)"/>
  <arg name="shift_x" value="$(arg shift_x)"/>
  <arg name="shift_y" value="$(arg shift_y)"/>
  <arg name="shift_z" value="$(arg shift_z)"/>
</include>
```

## Introduction

Ghost package act as the API of the common workspace by adding the launch file in ghost package to call the launch / node of packages in common workspace. The project workspace call the boot.launch to select the nodes in common workspace. Functions included in boot.launch are:
1. tf.launch
2. manual.launch
3. navigation.launch
4. rosbag.launch
5. gazebo.launch

## Use of ROS
There are three main ROS workspaces in a robot.
1. ROS main distro workspace (/opt/ros/[distro])
2. Common workspace (general packages)
3. Project workspace (hardware depended / tasks)

| Distro Workspace        |      | Common Workspace        |      | Project Workspace  |
| -----------             |      | -----------             |      | -------            |
|                         | <->  | ghost                   | <->  | launcher           |
|                         |      |                         |      | config_robot       |
|                         |      |                         |      | config_env         |
|                         |      |                         |      |                    |
|                         |      | navigation related      |      | tasks related      |

ROS distro workspace is a workspace for original packages from the internet.  
Common workspace is a prebuild workspace which install to the robot.  
Project workspace is the development workspace for each project or robot.

Common workspace source distro workspace to build, project workspace source common workspace to build.
