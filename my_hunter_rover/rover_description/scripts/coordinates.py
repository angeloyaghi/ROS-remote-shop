#! /usr/bin/env python

import time
import tf.transformations as tf
import math
import rospy
from geometry_msgs.msg import PoseStamped
from rover_description.srv import GetItems, GetItemsRequest, GetItemsResponse
from actionlib_msgs.msg import GoalStatusArray

y_rover = 0 # height of the initial position of the arm

y_row_1 = 0 # height of the first row with respect to the origin
y_row_2 = 0 # height of the second row with respect to the origin
y_row_3 = 0 # height of the third row with respect to the origin

# shelfs coordinates with respect to the origin
x_shelf_1 = 1.15
y_shelf_1 = 6.55
z_shelf_1 = 0

o_x_shelf_1 = 0
o_y_shelf_1 = 0
o_z_shelf_1 = 0.709264
o_w_shelf_1 = 0.704943

x_shelf_1_1 = 1
y_shelf_1_1 = 5
z_shelf_1_1 = 0

o_x_shelf_1_1 = 0
o_y_shelf_1_1 = 0
o_z_shelf_1_1 = 0.3286
o_w_shelf_1_1 = 0.94446

x_shelf_2 = 3.85
y_shelf_2 = 6.44
z_shelf_2 = 0

o_x_shelf_2 = 0
o_y_shelf_2 = 0
o_z_shelf_2 = -0.002418
o_w_shelf_2 = 0.999997

x_shelf_0 = 0
y_shelf_0 = 0
z_shelf_0 = 0

o_x_shelf_0 = 0
o_y_shelf_0 = 0
o_z_shelf_0 = 0.404297
o_w_shelf_0 = 0.914627

row_1 = y_row_1 - y_rover # how much should the arm go elevate to reach item at row 1 after it goes to the center of the frame of the shelf
row_2 = y_row_2 - y_rover # how much should the arm go elevate to reach item at row 2 after it goes to the center of the frame of the shelf
row_3 = y_row_3 - y_rover # how much should the arm go elevate to reach item at row 3 after it goes to the center of the frame of the shelf

quaternion_1 = [o_x_shelf_1, o_y_shelf_1, o_z_shelf_1, o_w_shelf_1]
quaternion_2 = [o_x_shelf_2, o_y_shelf_2, o_z_shelf_2, o_w_shelf_2]
quaternion_1_1 = [o_x_shelf_1_1, o_y_shelf_1_1, o_z_shelf_1_1, o_w_shelf_1_1]

shelf_1 = [x_shelf_1, y_shelf_1, z_shelf_1, quaternion_1]
shelf_2 = [x_shelf_2, y_shelf_2, z_shelf_2, quaternion_2]

intermediate_pose = [x_shelf_1_1, y_shelf_1_1, z_shelf_1_1, quaternion_1_1]

pose_stamped = PoseStamped()
pose_stamped.header.frame_id = 'map'

pose_stamped.pose.position.x = 0
pose_stamped.pose.position.y = 0 
pose_stamped.pose.position.z = 0

pose_stamped.pose.orientation.x = 0
pose_stamped.pose.orientation.y = 0
pose_stamped.pose.orientation.z = 0
pose_stamped.pose.orientation.w = 1

status_goal_reached = False
resetted = False

def publish_goal(x, y, quaternion):
    pose_stamped.header.frame_id = 'map'

    pose_stamped.pose.position.x = x
    pose_stamped.pose.position.y = y 
    pose_stamped.pose.position.z = 0
    
    pose_stamped.pose.orientation.x = quaternion[0]
    pose_stamped.pose.orientation.y = quaternion[1]
    pose_stamped.pose.orientation.z = quaternion[2]
    pose_stamped.pose.orientation.w = quaternion[3]
    
    pub.publish(pose_stamped)

items_names = {
    0: "bottle",
    1: "cup"
}

items_location = {
    "bottle": [shelf_1, 1],
    "cup": [shelf_2, 2]
}

def get_items(request):
    stops = []

    items = request.items
    for i in range(5):
        item = items[i]
        if item != 0:
            name = items_names.get(i)
            location = items_location.get(name)
            stops.append([location, name, item])

    for i in range(len(stops)):
        global status_goal_reached
        if stops[i][0][0] == shelf_2 and i-1 >= 0 and stops[i-1][0][0] == shelf_1:
            go_to([[[intermediate_pose[0], intermediate_pose[1], intermediate_pose[-1]]]])
            time.sleep(10)
        go_to(stops[i])
        status_goal_reached = False
        while not status_goal_reached:
            time.sleep(0.2)

    go_to([[[x_shelf_0, y_shelf_0, [o_x_shelf_0, o_y_shelf_0, o_z_shelf_0, o_w_shelf_0]]]])
    status_goal_reached = False
    while not status_goal_reached:
        time.sleep(0.2)

def go_to(stop):
    print("Going to: ", stop[0][0])
    publish_goal(stop[0][0][0], stop[0][0][1], stop[0][0][-1])

def status_callback(status_msg):
    time.sleep(0.5)
    global status_goal_reached, resetted
    try:
        print("Status: ", status_msg.status_list[0].status)
        print("Waiting for reset: ", resetted)
        if status_msg.status_list[0].status == 3 and not resetted:
            resetted = True
            status_goal_reached = True
        elif status_msg.status_list[0].status != 3:
            resetted = False
    except IndexError:
        pass
    

if __name__ == "__main__":
    try:
        rospy.init_node("navigation_goal", anonymous=True)
        pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=3)
        s = rospy.Service('get_items', GetItems, get_items)
        sub = rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)
        print("Ready to take destination goals.")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass