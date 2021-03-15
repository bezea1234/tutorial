#!/usr/bin/env python 
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


if __name__ == '__main__':
    bridge=CvBridge()

    video_capture=cv2.VideoCapture('video/tennis-ball-video.mp4')

    topic='/tennis_ball_image'
    rospy.init_node('tennis_ball_publisher',anonymous=True)
    tennis_ball_publisher=rospy.Publisher(topic,Image,queue_size=5)
    rate=rospy.Rate(0.7)

    while not rospy.is_shutdown():
        ret,frame=video_capture.read()
        if ret:
            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            tennis_ball_publisher.publish(ros_image)
        else:
            print 'ret=false'
        rate.sleep()
