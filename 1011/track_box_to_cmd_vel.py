#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from opencv_apps.msg import RotatedRectStamped
from geometry_msgs.msg import Twist

class track_box_to_cmd_vel:

	rect = None
	pub = None

	def __init__(self):
		self.rect = RotatedRectStamped()
		rospy.init_node('client')

		rospy.Subscriber('/camshift/track_box', RotatedRectStamped, self.call_back)
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)

		rospy.Timer(rospy.Duration(0.1), self.loop_once)

	def call_back(self, msg):
		area = msg.rect.size.width * msg.rect.size.height
		rospy.loginfo("area = {}, center = ({}, {})".format(area, msg.rect.center.x, msg.rect.center.y))
		if area > 100 * 100:
			self.rect = msg

	def loop(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			self.loop_once()
			rate.sleep()

	def loop_once(self):
		cmd_vel = Twist()
		rect_arrived = rospy.Time.now() - self.rect.header.stamp

		if rect_arrived.to_sec() < 1.0:

			if self.rect.rect.center.x < 320:
				cmd_vel.angular.z = 0.1
				cmd_vel.linear.x = 0
				cmd_vel.linear.y = 0

			else:
				cmd_vel.angular.z = -0.1
				cmd_vel.linear.x = 0
				cmd_vel.linear.y = 0

		else:
			cmd_vel.linear.x = - 0.5
			cmd_vel.linear.y = 0.5
			cmd_vel.angular.z = 0.3

		rospy.loginfo("\t\t\t\t\t\tpublish {}".format(cmd_vel.angular.z))
		self.pub.publish(cmd_vel)		

if __name__ == '__main__':
	try:
		obj = track_box_to_cmd_vel()
		obj.loop()

	except rospy.ROSInterruptException:
		pass