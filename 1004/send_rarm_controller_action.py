#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, actionlib, sys, time

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint

def main():
	print("Initializing node...")
	rospy.init_node('send_rarm_controller_action')
	rospy.sleep(1)

	print("Running. Ctrl-c to quit.")
	positions = {'RARM_JOINT0': 0.0, 'RARM_JOINT1': 0.0, 'RARM_JOINT2': -1.6, 
				 'RARM_JOINT3': 0.0, 'RARM_JOINT4': 0.0, 'RARM_JOINT5': 0.0}

	client = actionlib.SimpleActionClient('/rarm_controller/follow_joint_trajectory_action', FollowJointTrajectoryAction)
	if not client.wait_for_server(timeout = rospy.Duration(10)):
		sys.exit(1)

	# init goal
	goal = FollowJointTrajectoryGoal()
	goal.goal_time_tolerance = rospy.Time(1)
	goal.trajectory.joint_names = positions.keys()

	# 1st points
	point = JointTrajectoryPoint()
	point.positions = positions.values()
	point.time_from_start = rospy.Duration(3)
	goal.trajectory.points.append(point)

	# 2nd points
	point = JointTrajectoryPoint()
	positions['RARM_JOINT1'] = -0.7
	positions['RARM_JOINT2'] = -2.3
	point.positions = positions.values()
	point.time_from_start = rospy.Duration(6)
	goal.trajectory.points.append(point)

	# 3rd points
	point = JointTrajectoryPoint()
	positions['RARM_JOINT1'] = 0
	positions['RARM_JOINT2'] = -1.6
	point.positions = positions.values()
	point.time_from_start = rospy.Duration(9)
	goal.trajectory.points.append(point)	

	# send goal
	goal.trajectory.header.stamp = rospy.Time.now()
	client.send_goal(goal)
	print(goal)
	print("waiting...")

	if not client.wait_for_result(timeout = rospy.Duration(20)):
		rospy.logerr("Timed out waiting for JTA")
	rospy.loginfo("Exitting...")

if __name__ == '__main__':
	main()