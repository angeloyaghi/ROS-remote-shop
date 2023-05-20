README:
-------

The project is divided into two main packages:
	1. UR5-Pick-and-Place-Simulation
	2. my_hunter_rover
	
	
1. UR5-Pick-and-Place-Simulation:
-----------------------------------
The first package contains all files and launch files connected to the arm. 
To launch the arm along with the gripper and the camera:
	- "roslaunch ur5_gripper_moveit_config demo_gazebo.launch"
	- This launch file will launch both the gazebo along with the RVIZ/ Moveit extension
	- Furthermore, the arm will launch in an environment containing a shelf along with a clock in it.

A code should be run along with the simulation in order to run the object detection and have the arm grab the clock from the shelf.
To do so, it is advised to fix the initial positions the arm from Rviz by setting the following positions:
shoulder_pan: 0 degree
shoulder_lift: -29 degrees
elbow_joint:-118 degrees
wrist_1: -35 
wrist_2: 96 
wrist_3: 0


Then we should run the following command:
	- "rosrun ur5_moveit_gripper_config pick_and_place.py"
	
2. my_hunter_rover + robotic arm:
------------------------------------------
The second package contains all files and launch files for the rover along with the URDF that combines both.
To launch the rover along with the arm, we can either:
	- launch it in a world using spawn.launch
	- launch it for gmapping using gmapping.launch
	- launch it for navigation using navigation.launch which is also the project launch file
	- launch the GUI using gui.launch
	- use pkg name rover_description
	- The launch files will launch both the gazebo along with the RVIZ.

A code should be run along with the simulation in order to run the navigation and have the rover navigate to the shelves.
To do so, run first:
	-"roslaunch rover_description navigation.launch"
then:
	-"roslaunch rover_description gui.launch"
	
PS: you can also move the robot using teleop_keyboard.
