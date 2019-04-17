# ur5_ws
Workspace for UR5 configuration in ROS

# Description
This repository intends to provide a simulation environment (Gazebo+ROS+Rviz) for the development of pick and place functions with the UR5.

# Installation
   
Clone the git repository in the home folder:

	$ git clone https://github.com/Ubira/ur5_ws.git
		
Build the catkin workspace:

	$ cd ~/ur5_ws/
	$ catkin_make
	$ source devel/setup.bash
		
# Usage:
For simulation with Gazebo run the command:

	$ roslaunch ur5_gazebo ur5.launch
		
A world should appear in your Gazebo's GUI with the UR5 in the center:
  
It's possible to run python scripts like "testmotion.py" with the command:

	$ rosrun ur5_gazebo testmotion.py

In case of writing a new script make sure to make it executable with (in the file folder):

	$ chmod +x YOUR_PYTHON_SCRIPT.py
