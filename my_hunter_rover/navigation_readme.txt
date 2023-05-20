launch the gazebo simulation

roslaunch rover_description spawn.launch

-------------------------------------------------

Launch rviz

roslaunch rover_description rviz.launch

add a map
add a laserscan
add posearray (topic = /particlecloud)

-------------------------------------------------

launch the amcl and move_base nodes

roslaunch rover_description amcl_movebase.launch

-------------------------------------------------
