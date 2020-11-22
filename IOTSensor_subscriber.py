#!/usr/bin/env python
import rospy
from tutorial.msg import IoTSensorTutorial

def iot_sensor_callback(iot_sensor_message):
    rospy.loginfo("new IoT data received: (%d, %s, %.2f ,%.2f)", 
        iot_sensor_message.id,iot_sensor_message.name,
        iot_sensor_message.temperature,iot_sensor_message.humidity)
    
rospy.init_node('iotsensor_tutorial_subscriber', anonymous=True)

rospy.Subscriber('/iotsensor_tutorial_topic', IoTSensorTutorial, iot_sensor_callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()