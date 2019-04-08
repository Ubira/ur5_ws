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

waypoints = [[0.0, -1.44, 1.4, 0.6, 0, -0.33], [0, -1.57, 0, -1.57 , 0, 0], [0, -1.0, 0.7, 0 , 0, 0], [0, -0.5, 0.7, -1.0 , 0, 0], [0, -0.3, 0.5, -0.5 , 1, 0], [0, 0, 0, 0, 0, 0]]
#waypoints = [[0, 0, 0, 0, 0, 0]]

def main():

    rospy.init_node('send_joints')
    pub = rospy.Publisher('/arm_controller/command',
                          JointTrajectory,
                          queue_size=10)

    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR5
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(1)
    cnt = 0
    pts = JointTrajectoryPoint()
    traj.header.stamp = rospy.Time.now()
    
    pathLength = len(waypoints)
    print "\nThe path length is",pathLength

    while not rospy.is_shutdown():
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        #print(joints_pos)
        pts.positions = joints_pos
        pts.time_from_start = 0

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        print("\nSending dummy command\n")
        pub.publish(traj)
        rate.sleep()
        #pub.publish(traj)
        rate.sleep()
        for cnt in range(0, pathLength):
            print "Goint to point",(cnt+1)
            pts.positions = waypoints[cnt]

            pts.time_from_start = rospy.Duration(0.5)

            # Set the points to the trajectory
            traj.points = []
            traj.points.append(pts)
            # Publish the message
            pub.publish(traj)
            rate.sleep()
            if (cnt == pathLength - 1):
                print("\nTask completed\n")
                rospy.signal_shutdown("Task completed")


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
	print ("Program interrupted before completion")
