#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import numpy as np

bridge=CvBridge()

topic='/tennis_ball_image'

def image_call_back(ros_image):
    print 'got an image'
    global bridge
    #convert ros_image into an opencv-compatible image
    try:
        cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
        print(e)
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)
    yellowLower =(30, 150, 100)
    yellowUpper = (50, 255, 255)
    binary_image_mask = filter_color(cv_image, yellowLower, yellowUpper)
    contours = getContours(binary_image_mask)
    draw_ball_contour(binary_image_mask, cv_image,contours)

def filter_color(rgb_image, lower_bound, upper_bound):
    #CONVERT TO HSV IMAGE
    hsv_image=cv2.cvtColor(rgb_image,cv2.COLOR_BGR2HSV)
    #DEFINE THE MASK
    mask=cv2.inRange(hsv_image,lower_bound,upper_bound)
    return mask

def getContours(binary_image):
    contours, hierarchy =cv2.findContours(binary_image.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_ball_contour(binary_image_mask, rgb_image,contours):
    black_image = np.zeros([binary_image_mask.shape[0], binary_image_mask.shape[1],3],'uint8')
    
    for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if (area>3000):
            cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
            cx, cy = get_contour_center(c)
            cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),5,(150,150,255),-1)
            print ("Area: {}, Perimeter: {}".format(area, perimeter))
    print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy


if __name__ == '__main__':
    rospy.init_node('tennis_ball_subscriber',anonymous=True)
    tennis_ball_subscriber=rospy.Subscriber(topic,Image,image_call_back)
    rospy.spin()
    cv2.destroyAllWindows()