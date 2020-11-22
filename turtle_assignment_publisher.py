#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move():

    rospy.init_node('turtle_tutorial_publisher',anonymous=True)

    speed_publisher=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)

    rate=rospy.Rate(1)

    while not rospy.is_shutdown():
        velocity=Twist()
        velocity.linear.x=-0.3
        speed_publisher.publish(velocity)



if __name__ == '__main__':
    try:
        move()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")