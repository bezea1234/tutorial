#! /usr/bin/env python

import rospy
from turtlesim.msg import Pose

def poseCallback(pose_message):

   # display the x, y, and theta received from the message
    print "pose callback"
    print ('x = {} ' .format(pose_message.x))
    print ('y = {} ' .format(pose_message.y))
    print ('yaw = {} '.format(pose_message.theta)) #python3


if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_tutorial_subscriber_pose', anonymous=True)        

       # subscribe to the topic of the pose of the Turtlesim
        pose_subscriber=rospy.Subscriber('/turtle1/pose',Pose,poseCallback)

       # spin=start Listening
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")