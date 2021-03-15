#! /usr/bin/env python

import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    try:

        rospy.init_node('tutorial_publisher',anonymous=True)

        publisher=rospy.Publisher('/sayhello',String,queue_size=10)

        rate=rospy.Rate(1)

        while not rospy.is_shutdown():
            publisher.publish('hello!')
            rate.sleep()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")