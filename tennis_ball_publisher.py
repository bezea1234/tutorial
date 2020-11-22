#!/usr/bin/env python 
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

video_capture=cv2.VideoCapture('tennis-ball-video.mp4')

topic='/tennis_ball_image'
rospy.init_node('tennis_ball_publisher',anonymous=True)
tennis_ball_publisher=rospy.Publisher(topic,Image,queue_size=10)
rate=rospy.Rate(1)

bridge=CvBridge()

image_name = "tennisball05.jpg"
#while not rospy.is_shutdown():
    #ret,frame=video_capture.read()
    #if ret:
        frame=cv2.imread(image_name)
        ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        tennis_ball_publisher.publish(ros_image)
    #else:
    #    print 'ret=false'
        rate.sleep()
