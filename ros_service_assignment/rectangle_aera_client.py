#!/usr/bin/env python

import sys
import rospy

from tutorial.srv import RectangleAeraService
from tutorial.srv import RectangleAeraServiceRequest
from tutorial.srv import RectangleAeraServiceResponse

def rectangle_aera_client(x, y):
    rospy.wait_for_service('rectangle_aera')
    try:
        rectangle_aera = rospy.ServiceProxy('rectangle_aera', RectangleAeraService)
        resp1 = rectangle_aera(x, y)
        return resp1.aera
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print usage()
        sys.exit(1)
    print "Requesting  width and height  %s*%s"%(x, y)
    s = rectangle_aera_client(x, y)
    print "%s * %s = %s"%(x, y, s)