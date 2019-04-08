#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
import numpy as np

class Path_listener(object):
    def __init__(self):
        # Params
        self.layout = None
        self.path = None
        self.commandPath = None

        # Node cycle rate (in Hz).
        self.rate = rospy.Rate(1)

        # Subscribers
        rospy.Subscriber("path", Float32MultiArray, self.callback)


    def getCommandPath(self):
        return self.commandPath

    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + "\nI heard:\n%s", data)
        self.path = data.data
        self.layout = data.layout
        #print(self.path, self.layout)
        self.makePath()

    def start(self):
        rospy.loginfo("Starting listener")

        while not rospy.is_shutdown():
                self.rate.sleep()

    def makePath(self):
        pathLength = self.layout.dim[0].size/3
        stride = self.layout.dim[1].stride
        size = self.layout.dim[1].size

        self.commandPath = np.zeros((pathLength, size + 2))

        for i in range(0, pathLength):
            for j in range(0, size):
                if (j == 0):
                    self.commandPath[i, j] = 0
                if (j == 2):
                    self.commandPath[i, j+2] = 0
                self.commandPath[i, j+1] = self.path[j + stride*i]

        print "The command is:\n", self.commandPath
 
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('path_listener', anonymous=True)

    path_listener = Path_listener()
    path_listener.start()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
