#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math
import time
import sys
from turtlesim.msg import Pose

#define Call back method
def poseCallback(pose_msg):
    pose_turtlesim.x=pose_msg.x
    pose_turtlesim.y=pose_msg.y
    pose_turtlesim.theta=pose_msg.theta

PI=3.14

vel_publisher=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
vel_msg=Twist()
pose_subscriber=rospy.Subscriber("/turtle1/pose",Pose,poseCallback)
pose_turtlesim=Pose()
#method to move the robot straight
def move(speed, distance, isForward):
    

    #set direction
    if isForward:
        vel_msg.linear.x=abs(speed)
    else:
        vel_msg.linear.x=-abs(speed)
    vel_msg.linear.y=0
    vel_msg.linear.z=0

    #set the angular velocity to zero
    vel_msg.angular.x=0
    vel_msg.angular.y=0
    vel_msg.angular.z=0
    
    #t0=current time
    t0=rospy.Time.now().to_sec()
    current_distance=0
    #rate
    rate=rospy.Rate(100)
    #loop
    while current_distance<distance :
        vel_publisher.publish(vel_msg)
        t1=rospy.Time.now().to_sec()
        #estimate the current distance=speed*time
        current_distance=speed*(t1-t0)
        #rospy.spin()
        rate.sleep()
    vel_msg.linear.x=0
    vel_publisher.publish(vel_msg)

#method to rotate the robot
def rotate(angular_speed,angle,clockwise):
    #set the linear velocity to zero
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0

    #set the angular  velocity 
    vel_msg.angular.x=0
    vel_msg.angular.y=0
    if clockwise:
        vel_msg.angular.z=-abs(angular_speed)
    else:
        vel_msg.angular.z=abs(angular_speed)
    
    #t0=current time
    t0=rospy.Time.now().to_sec()
    current_angle=0
    #rate
    rate=rospy.Rate(10)
    #loop
    while current_angle<angle :
        vel_publisher.publish(vel_msg)
        t1=rospy.Time.now().to_sec()
        #estimate the current distance=speed*time
        current_angle=angular_speed*(t1-t0)
        #rospy.spin()
        rate.sleep()
    vel_msg.angular.z=0
    vel_publisher.publish(vel_msg)

#method to transform in  degrees from radians
def degrees2radians(angle_in_degrees):
    return angle_in_degrees*PI/180.0

#method to rotate with a certain oriantation
def setDesiredOrinetation(degrees_desired_in_radians):
    relative_angle_in_radians=degrees_desired_in_radians-pose_turtlesim.theta
    if(relative_angle_in_radians<=0):
        clockwise=True
    else:
        clockwise=False
    rotate(degrees2radians(20) ,abs(relative_angle_in_radians),clockwise)

#method used to go to a goal
def moveToGoal(goal_pose,distance_tolerence):
    #rate
    rate=rospy.Rate(10)
    
    while (True):
        #---use a Proportional Controler---
        #set the linear velocity
        distance=abs(getDistance(pose_turtlesim.x,goal_pose.x,pose_turtlesim.y,goal_pose.y))
        k_liniar=1.5
        vel_msg.linear.x=k_liniar*distance
        vel_msg.linear.y=0
        vel_msg.linear.z=0

        #set the angular velocity 
        vel_msg.angular.x=0
        vel_msg.angular.y=0
        k_angular=4.0
        angle_goal=math.atan2(goal_pose.y-pose_turtlesim.y,goal_pose.x-pose_turtlesim.x)
        vel_msg.angular.z=4.0*(angle_goal-pose_turtlesim.theta)

        print 'distance=', distance, 'z=',vel_msg.angular.z
        print 'x=',pose_turtlesim.x, 'y=',pose_turtlesim.y
        vel_publisher.publish(vel_msg)
        rate.sleep()
        if distance<distance_tolerence:
            break
    
    print('turtle arives to the goal')
    vel_msg.linear.x=0
    vel_msg.angular.z=0
    vel_publisher.publish(vel_msg)


#method used to fin the distance between 2 points
def getDistance(x1,x2,y1,y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

#method that make a grid path
def gridClean():
    rate=rospy.Rate(1)

    #move to the goal
    start_pose=Pose()
    start_pose.x=1
    start_pose.y=1
    start_pose.theta=0
    moveToGoal(start_pose,0.01)
    #rate.sleep()
    #start moving 
    setDesiredOrinetation(degrees2radians(0))
    rate.sleep()
    move(2,9,1)
    rate.sleep()
    rotate(degrees2radians(20),degrees2radians(90),False)
    rate.sleep()
    move(2,9,1)
    rate.sleep()
    rotate(degrees2radians(20),degrees2radians(90),False)
    rate.sleep()
    move(2,1,1)
    rate.sleep()
    rotate(degrees2radians(20),degrees2radians(90),False)
    rate.sleep()
    move(2,9,1)
    rate.sleep()
    rotate(degrees2radians(20),degrees2radians(90),True)
    rate.sleep()
    move(2,1,1)
    rate.sleep()
    rotate(degrees2radians(20),degrees2radians(90),True)

#method that make a spin path
def spinClean(angular_speed):
    rate=rospy.Rate(1)
    rk=0
    while((pose_turtlesim.x<10.5)&(pose_turtlesim.y<10.5)):
        rk=rk+0.5
        vel_msg.linear.x=rk
        vel_msg.angular.z=angular_speed
        vel_publisher.publish(vel_msg)
        rate.sleep()
    vel_msg.linear=0
    vel_msg.angular=0
    vel_publisher.publish(vel_msg)   



if __name__ == '__main__':
    rospy.init_node('vel_publisher',anonymous=True)
    #print("enter speed, direction, isForward: ")
    #if len(sys.argv) == 3:
    #    speed = float(sys.argv[0])
    #    distance = float(sys.argv[1])
    #    isForward = float(sys.argv[2])
    #else:
    #    print("error")
    #    sys.exit(1)
    
    #move(speed,distance,isForward)
    
    #rotate(degrees2radians(20),degrees2radians(90),1)
    #rotate(degrees2radians(10),degrees2radians(45),0)
    #move(5,5,0)

    #setDesiredOrinetation(degrees2radians(90))
    #setDesiredOrinetation(degrees2radians(-45))
    #rospy.spin()
    x_goal=rospy.get_param("x_goal")
    y_goal=rospy.get_param("y_goal")

    pose=Pose()
    pose.x=x_goal
    pose.y=y_goal
    pose.theta=0

    moveToGoal(pose,0.01)
    
    gridClean()

    #spinClean(5)
    rospy.spin()
    






