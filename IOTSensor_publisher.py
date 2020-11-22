#! /usr/bin/env python

import rospy
from tutorial.msg import IoTSensorTutorial
import random

if __name__ == '__main__':
    try:

        rospy.init_node('iotsensor_tutorial_publisher',anonymous=True)

        iot_publisher=rospy.Publisher('/iotsensor_tutorial_topic',IoTSensorTutorial,queue_size=10)

        rate=rospy.Rate(1)

        while not rospy.is_shutdown():
            iot_sensor=IoTSensorTutorial()
            iot_sensor.id=1
            iot_sensor.name="iot_parking_01"
            iot_sensor.temperature=random.random()
            iot_sensor.humidity=random.random()
            rospy.loginfo("i publish:")
            rospy.loginfo(iot_sensor)
            iot_publisher.publish(iot_sensor)
            rate.sleep()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")