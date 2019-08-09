#!/usr/bin/env python
'''
This python script establishes node 'yaw_angle'.
It reads string message from /tag_positon topic which contains Tag-ID and current tag positions.
It uses function np.arctan2() to calculate yaw_angle and then translate it into UWBInfo message type.
Then publish it through topic /UWBInfo.
'''
import rospy
import sys
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Point
import csv
from localsense.msg import UWBInfo

tag_position = {'55452':[0, 0, 0], '55460':[0, 0, 0]}
yaw_angle = 0
iterator = 0
angle = UWBInfo()


def msg_callback0(ros_str):
    tag_pos_str = ros_str.data#Read string message containing tag positions
    tag_pos_str = tag_pos_str.split(' ')
    tag_position[tag_pos_str[0]] = [int(tag_pos_str[1]), int(tag_pos_str[2]), int(tag_pos_str[3])]
    X1 = tag_position['55452'][0]#Get tag coordinates
    Y1 = tag_position['55452'][1]
    X2 = tag_position['55460'][0]
    Y2 = tag_position['55460'][1]
    angle.fuwb_id = int(tag_pos_str[0])
    angle.flidar_pose.x = (X1+X2)/2
    angle.flidar_pose.y = (Y1+Y2)/2
    angle.flidar_pose.z = 0
    yaw_angle = np.arctan2((Y1 - Y2),(X1 - X2))#Calculate yaw angle
    angle.yaw = yaw_angle
    rospy.loginfo("X1 %s Y1 %s cm X2 %s Y2 %s Yaw %s" % (str(X1), str(Y1),str(X2), str(Y2), str(yaw_angle)))
    yaw_angle_pub = rospy.Publisher('/UWBInfo', UWBInfo, queue_size=1)
    yaw_angle_pub.publish(angle)#publish message

    

def main(args):
    rospy.init_node('yaw_angle', anonymous=True)
    msg_sub0 = rospy.Subscriber("/tag_position",String, msg_callback0)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)