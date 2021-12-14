#!/usr/bin/env python
import time
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from jsk_recognition_msgs.msg import BoundingBoxArray

pub = rospy.Publisher('/navigation_velocity_smoother/raw_cmd_vel', Twist, queue_size=1)
moving = False
r_passed = False
g_passed = False
b_passed = False

def go_right(x, y, z):
    global moving
    start_time = time.time()
    moving = True

    cmd_vel = Twist()

    # Turn right
    print("[INFO] Turning right ...")
    cmd_vel.angular.z = -np.pi / 10
    pub.publish(cmd_vel) 
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.angular.z = 0.0
    pub.publish(cmd_vel)
    start_time = time.time()
    # Move forawrd
    print("[INFO] Moving {:.2f}m forawrd ...".format(y + 0.3))
    cmd_vel.linear.x = (y + 0.3) / 5
    pub.publish(cmd_vel)
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.linear.x = 0.0
    pub.publish(cmd_vel)
    start_time = time.time()

    # Turn left
    print("[INFO] Turning left ...")
    cmd_vel.angular.z = np.pi / 10
    pub.publish(cmd_vel) 
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.angular.z = 0.0
    pub.publish(cmd_vel)
    start_time = time.time()
    # Move forawrd
    print("[INFO] Moving {:.2f}m forawrd ...".format(z + 0.3))
    cmd_vel.linear.x = (z + 0.3) / 5
    pub.publish(cmd_vel)
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.linear.x = 0.0
    pub.publish(cmd_vel)
    start_time = time.time() 

    moving = False

def go_left(x, y, z):
    global moving
    start_time = time.time()
    moving = True

    cmd_vel = Twist()

    # Turn left
    print("[INFO] Turning left ...")
    cmd_vel.angular.z = np.pi / 10
    pub.publish(cmd_vel) 
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.angular.z = 0.0
    pub.publish(cmd_vel)
    start_time = time.time()
    # Move forawrd
    print("[INFO] Moving {:.2f}m forawrd ...".format(abs(y) + 0.3))
    cmd_vel.linear.x = (abs(y) + 0.3) / 5
    pub.publish(cmd_vel)
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.linear.x = 0.0
    pub.publish(cmd_vel)
    start_time = time.time()

    # Turn right
    print("[INFO] Turning right ...")
    cmd_vel.angular.z = -np.pi / 10
    pub.publish(cmd_vel) 
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.angular.z = 0.0
    pub.publish(cmd_vel)
    start_time = time.time()
    # Move forawrd
    print("[INFO] Moving {:.2f}m forawrd ...".format(z + 0.3))
    cmd_vel.linear.x = (z + 0.3) / 5
    pub.publish(cmd_vel)
    while time.time() - start_time < 5:
        pub.publish(cmd_vel) 
        time.sleep(0.001)
    cmd_vel.linear.x = 0.0
    pub.publish(cmd_vel)
    start_time = time.time() 

    moving = False

# Red box call back function
def rcb(msg):
    global pub, moving, r_passed, g_passed, b_passed
    # If any red boxes are detected
    if len(msg.boxes):
        # print("[INFO] Found red box ...")
        x = msg.boxes[0].pose.position.x
        y = msg.boxes[0].pose.position.y
        z = msg.boxes[0].pose.position.z
        # print "red box pos: ({} {} {})".format(x, y, z)

        # Call go_right function if turtlebot is not moving
        # and if red box is not passed
        if not moving and r_passed == 0:
            go_right(x, y, z)
            r_passed = True
    else:
        # print "no red box"  
        pass

# Green box call back function
def gcb(msg):
    global pub, moving, r_passed, g_passed, b_passed
    # If any green boxes are detected
    if len(msg.boxes):
        # print("[INFO] Found green box ...")
        x = msg.boxes[0].pose.position.x
        y = msg.boxes[0].pose.position.y
        z = msg.boxes[0].pose.position.z
        # print "green box pos: ({} {} {})".format(x, y, z)

        # Call go_left function if turtlebot is not moving,
        # red box is passed and green box is not passed    
        if not moving and r_passed and not g_passed::
            go_left(x, y, z)
            g_passed = True
    else:
        # print "no green box"  
        pass

# Blue box call back function
def bcb(msg):
    global pub, moving, r_passed, g_passed, b_passed
    # If any blue boxes are detected
    if len(msg.boxes):
        # print("[INFO] Found blue box ...")
        x = msg.boxes[0].pose.position.x
        y = msg.boxes[0].pose.position.y
        z = msg.boxes[0].pose.position.z
        # print "blue box pos: ({} {} {})".format(x, y, z)

        # Call go_right function if turtlebot is not moving,
        # red and green box is passed, and blue box is not passed          
        if not moving and r_passed and g_passed and not b_passed:
            go_right(x, y, z)
            b_passed = True
    else:
        # print "no blue box"
        pass

def main():
    global r_passed, g_passed, b_passed
    rospy.init_node('control', anonymous=True)
    if not r_passed:
        rospy.Subscriber('/camera/depth_registered/boxes_r', BoundingBoxArray, rcb)
    if not g_passed:
        rospy.Subscriber('/camera/depth_registered/boxes_g', BoundingBoxArray, gcb)
    if not b_passed:
        rospy.Subscriber('/camera/depth_registered/boxes_b', BoundingBoxArray, bcb)
    rate = rospy.Rate(10)
    
    rospy.spin()
    rate.sleep()
    
if __name__ == '__main__':
    main()

"""
[INFO] Turning right ...
[INFO] Moving 0.55m forawrd ...
[INFO] Turning left ...
[INFO] Moving 1.33m forawrd ...
[INFO] Turning left ...
[INFO] Moving 0.54m forawrd ...
[INFO] Turning right ...
[INFO] Moving 1.10m forawrd ...
[INFO] Turning right ...
[INFO] Moving 0.55m forawrd ...
[INFO] Turning left ...
[INFO] Moving 1.22m forawrd ...
"""