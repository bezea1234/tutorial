#! /usr/bin/env python

import rospy
from std_msgs.msg import String

def data_callback(message):
    rospy.loginfo("I heard %s",message.data)

if __name__ == '__main__':
    try:

        rospy.init_node('tutorial_subscriber',anonymous=True)

        publisher=rospy.Subscriber('/sayhello',String,data_callback)

        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")