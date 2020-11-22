#!/usr/bin/env python

from tutorial.srv import RectangleAeraService
from tutorial.srv import RectangleAeraServiceRequest
from tutorial.srv import RectangleAeraServiceResponse

import rospy

def handle_rectangle_aera(req):
    print "Returning [%s * %s = %s]"%(req.width, req.height, (req.width * req.height))
    return RectangleAeraServiceResponse(req.width * req.height)

def rectangle_aera_server():
    rospy.init_node('rectangle_aera_server')
    s = rospy.Service('rectangle_aera', RectangleAeraService, handle_rectangle_aera)
    print "Ready to find the rectangle aera."
    rospy.spin()
    
if __name__ == "__main__":
    rectangle_aera_server()