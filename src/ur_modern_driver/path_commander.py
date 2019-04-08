#!/usr/bin/python
#
# Send joint values to UR5 using messages
#

import math
import time

from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
import rospy
from std_msgs.msg import Float32MultiArray
import numpy as np

waypoints = [[0.0, -1.44, 1.4, 0.6, 0, -0.33], [0, -1.57, 0, -1.57 , 0, 0], [0, -1.0, 0.7, 0 , 0, 0], [0, -0.5, 0.7, -1.0 , 0, 0], [0, -0.3, 0.5, -0.5 , 1, 0], [0, 0, 0, 0, 0, 0]]
#waypoints = [[0, 0, 0, 0, 0, 0]]

class Path_listener(object):
    def __init__(self):
        # Params
        self.layout = None
        self.path = None
        self.waypoints = None
        self.ready = False

        # Node cycle rate (in Hz).
        self.rate = rospy.Rate(1)

        # Subscribers
        rospy.Subscriber("path", Float32MultiArray, self.callback)


    def getCommandPath(self):
        return self.waypoints

    def callback(self, data):
        self.ready = True
        rospy.loginfo(rospy.get_caller_id() + "\nI heard:\n%s", data)
        self.path = data.data
        self.layout = data.layout
        #print(self.path, self.layout)
        self.makePath()

    def start(self):
        rospy.loginfo("Starting listener")

        while not rospy.is_shutdown():
                if self.ready:
                    break
                self.rate.sleep()

    def makePath(self):
        pathLength = self.layout.dim[0].size/3
        stride = self.layout.dim[1].stride
        size = self.layout.dim[1].size

        self.waypoints = np.zeros((pathLength, size + 3))

        for i in range(0, pathLength):
            for j in range(0, size):
                if (j == 0):
                    self.waypoints[i, j] = 0
                if (j == 2):
                    self.waypoints[i, j+2] = 0
                    self.waypoints[i, j+3] = 0
                self.waypoints[i, j+1] = self.path[j + stride*i]

        print "The command is:\n", self.waypoints

def main():

    rospy.init_node('path_listener', anonymous=True)

    pub = rospy.Publisher('/arm_controller/command',
                          JointTrajectory,
                          queue_size=10)

    path_listener = Path_listener()
    path_listener.start()

    #rospy.init_node('send_joints')

    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR5
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    #rate = rospy.Rate(1)
    cnt = 0
    pts = JointTrajectoryPoint()
    traj.header.stamp = rospy.Time.now()
    
    waypoints = path_listener.getCommandPath()
    print(waypoints)
    pathLength = len(waypoints)
    print "\nThe path length is",pathLength

    while not rospy.is_shutdown():
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        #print(joints_pos)
        pts.positions = joints_pos
        #pts.time_from_start = rospy.Duration(0.5)
        pts.time_from_start = 0

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        #print("\nSending dummy command\n")
        #pub.publish(traj)
        #path_listener.rate.sleep()
        #pub.publish(traj)
        #path_listener.rate.sleep()
        for cnt in range(0, pathLength):
            print "Goint to point",(cnt+1)
            pts.positions = waypoints[cnt]

            pts.time_from_start = rospy.Duration(0.5)

            # Set the points to the trajectory
            traj.points = []
            traj.points.append(pts)
            # Publish the message
            pub.publish(traj)
            path_listener.rate.sleep()
            if (cnt == pathLength - 1):
                print("\nTask completed\n")
                rospy.signal_shutdown("Task completed")


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
	print ("Program interrupted before completion")

