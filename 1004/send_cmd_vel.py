#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist

if __name__ == '__main__':
	try:
		rospy.init_node('send_cmd_vel', anonymous = True)
		'''
		Setting the queue_size to 1 is a valid approach if you want to 
		make sure that a new published value will always prevent any 
		older not yet sent values to be dropped. This is good for, say, 
		a sensor that only cares about the latest measurement. e.g. 
		never send older measurements if a newer one exists.
		'''
		pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
		rospy.sleep(1)

		cmd_vel = Twist()
		cmd_vel.linear.x = 2.0
		cmd_vel.linear.y = 2.0
		cmd_vel.linear.z = 0.0
		cmd_vel.angular.x = 0.0
		cmd_vel.angular.y = 0.0
		cmd_vel.angular.z = 1.0

		rospy.loginfo("Send cmd_vel:")
		rospy.loginfo(cmd_vel)
		pub.publish(cmd_vel)

	except rospy.ROSInterruptException:
		pass