#!/usr/bin/env python
import sys
import rospy
import numpy as np
from std_msgs.msg import String
import csv

Yaw_angle = String()
curr_tag_position = [0,0,0]
tag_id = 0

def msg_callback2(ros_str):
    py_str = ros_str.data
    rospy.loginfo("this is one message: %s",(py_str))
    msg = py_str.split("AA")
    for line in msg:
        if line[6:8] == "A1":
            Yaw_angle.data = str(int("0x" + line[8:12],16))
    rospy.loginfo(Yaw_angle)
    yaw_angle_pub = rospy.Publisher("/imu_yaw_anlge",String,queue_size=1)
    yaw_angle_pub.publish(Yaw_angle)
'''
    with open('IMU_yaw_angle_record.csv','a') as out:
        csv_write = csv.writer(out, dialect = 'excel')
        now = str(rospy.Time.now())
        current_line = [
            now, Yaw_angle.data
        ]
        csv_write.writerow(current_line)
'''

def main(args):
    rospy.init_node('msg_converter0', anonymous=True)
    msg_sub2 = rospy.Subscriber("/Serial_read_2",String, msg_callback2)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
'''
with open('IMU_yaw_angle_record.csv','a') as out:
    csv_write = csv.writer(out, dialect = 'excel')
    first_line = [
        'time', 'yaw'
    ]
    csv_write.writerow(first_line)
'''
if __name__ == '__main__':
    main(sys.argv)