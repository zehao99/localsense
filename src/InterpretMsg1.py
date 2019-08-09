#!/usr/bin/env python
import rospy
import sys
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Point
import csv

tag1_position = String()
tag_to_station = {'76123' : 0, '76124' : 0, '76126' : 0}
curr_tag_position = [0,0,0]
tag_id = 0

def msg_callback1(ros_str):
    py_str = ros_str.data
    msg = py_str.split("55AA")
    for line in msg:
        if line[4:6] == "2A":
            tag_id = int("0x" + line[10 : 12] + line [8 : 10], 16)
            curr_tag_position[0] = int("0x" + line[18 : 20] + line[16 : 18] + line[14 : 16] + line[12 : 14], 16)
            curr_tag_position[1] = int("0x" + line[26 : 28] + line[24 : 26] + line[22 : 24] + line[20 : 22], 16)
            curr_tag_position[2] = int("0x" + line[34 : 36] + line[32 : 34] + line[30 : 32] + line[28 : 30], 16)
            i = 0
            for number in curr_tag_position:
                if number > 4026531840:
                    curr_tag_position[i] = number - 4294967296
                i = i + 1
            rospy.loginfo("Current %s tag is at: X: %s cm Y: %s cm Z: %s cm." % (str(tag_id), str(curr_tag_position[0]), str(curr_tag_position[1]), str(curr_tag_position[2])))
        if line[4:6] == "2D":
            tag_id = int("0x" + line[10 : 12] + line [8 : 10], 16)
            l = len(line)
            num_of_stations = int(np.floor((l - 42) / 6))
            for i in range(0 , num_of_stations):
                station_id = str(int("0x" + line[14 + 12 * i : 16 + 12 * i] + line[12 + 12 * i : 14 + 12 * i], 16) + 65536)
                tag_to_station[station_id] = int("0x" + line[18 + 12 * i : 20 + 12 * i] + line[16 + 12 * i : 18 + 12 * i], 16)
                #rospy.loginfo("(76123, %s cm),(76124, %s cm),(76126, %s cm)" %(str(tag_to_station['76123']), str(tag_to_station['76124']), str(tag_to_station['76126'])))
    tag1_position.data = str(tag_id) + ' ' + str(curr_tag_position[0]) + ' ' + str(curr_tag_position[1]) + ' ' + str(curr_tag_position[2])
    position_pub = rospy.Publisher("/tag_position",String,queue_size=1)
    position_pub.publish(tag1_position)
    '''
    with open('tag1_record.csv','a') as out:
        csv_write = csv.writer(out, dialect = 'excel')
        now = str(rospy.Time.now())
        #One station
        
        current_line = [
            now, tag_id, curr_tag_position[0], curr_tag_position[1], curr_tag_position[2], tag_to_station['76123']
        ]
        
        #Three stations

        current_line = [
            now, tag_id, curr_tag_position[0], curr_tag_position[1], curr_tag_position[2], tag_to_station['76123'], tag_to_station['76124'], tag_to_station['76126']
        ]

        #Four stations

        current_line = [
            now, tag_id, curr_tag_position[0], curr_tag_position[1], curr_tag_position[2], tag_to_station['76123'], tag_to_station['76124'], tag_to_station['76126'], tag_to_station['76130']
        ]

        csv_write.writerow(current_line)
'''


def main(args):
    rospy.init_node('msg_converter1', anonymous=True)
    msg_sub1 = rospy.Subscriber("/Serial_read_1",String, msg_callback1)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
'''
with open('tag0_record.csv','a') as out:
    csv_write = csv.writer(out, dialect = 'excel')
    first_line = [
        'time', 'tag_id', 'X(cm)', 'Y(cm)', 'Z(cm)', '76123_distance', '76124_distance',
        '76126_distance', '76130_distance'
    ]
    csv_write.writerow(first_line)
'''
if __name__ == '__main__':
    main(sys.argv)