#include <iostream>
#include <string>
#include <ros/ros.h>
#include <serial/serial.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>
#include "localsense/serial.h"

#define rBUFFERSIZE     50
unsigned char r_buffer[rBUFFERSIZE];
unsigned char char_buffer = 0x00;
unsigned char start_indicator;
std::string buffer;
serial::Serial ser;


std::string num_int2hex(int numb){
    std::string output;
    switch (numb){
        case 0 : output = "0";break;
        case 1 : output = "1";break;
        case 2 : output = "2";break;
        case 3 : output = "3";break;
        case 4 : output = "4";break;
        case 5 : output = "5";break;
        case 6 : output = "6";break;
        case 7 : output = "7";break;
        case 8 : output = "8";break;
        case 9 : output = "9";break;
        case 10 : output = "A";break;
        case 11 : output = "B";break;
        case 12 : output = "C";break;
        case 13 : output = "D";break;
        case 14 : output = "E";break;
        case 15 : output = "F";break;
    }
    return output;
}

std::string int2hex(unsigned char num){
    int number;
    int first_num;
    int second_num;
    std::string result;
    number = (int)num;
    first_num = floor(number/16);
    second_num = number - first_num * 16;
    result = num_int2hex(first_num) + num_int2hex(second_num);
    return result;
}

int main (int argc, char** argv){
    ros::init(argc, argv, "serial_port_read2");
    ros::NodeHandle nh;

   // ros::Subscriber write_sub = nh.subscribe("write", 1000, write_callback);
    ros::Publisher msg_pub = nh.advertise<std_msgs::String>("Serial_read_2", 1000);

    try
    {
        ser.setPort("/dev/ttyUSB0");
        ser.setBaudrate(115200);
        serial::Timeout to = serial::Timeout::simpleTimeout(1000);
        ser.setTimeout(to);
        ser.open();
    }
    catch (serial::IOException& e)
    {
        ROS_ERROR_STREAM("Unable to open port ");
        return -1;
    }

    if(ser.isOpen()){
        ROS_INFO_STREAM("Serial Port initialized");
    }else{
        return -1;
    }

    ros::Rate loop_rate(3000);
    while(ros::ok()){
        std_msgs::String msg;
        ros::spinOnce();
        if(ser.available()){
            ROS_INFO_STREAM("Reading from serial port");
            ser.read(r_buffer,rBUFFERSIZE);
			for(int i=0;i<rBUFFERSIZE;i++)
			{
                ROS_INFO("[0x%02x]",r_buffer[i]);
                }
			ROS_INFO_STREAM("End reading from serial port");        
            for(int l=0;l<rBUFFERSIZE;l++)
            {
                if(r_buffer[l] == 0x5A && char_buffer == 0xA5)
                {
                    start_indicator = 1;
                    }
                if(r_buffer[l] == 0xA5 && char_buffer == 0xAA)
                {
                    start_indicator = 0;
                    msg.data = buffer;
                    msg_pub.publish(msg);
                    buffer = "";
                    buffer = buffer + "A5";
                    }
                if(start_indicator == 1)
                {
                    buffer = buffer + int2hex(r_buffer[l]);
                    }
                char_buffer = r_buffer[l];
                }
                      
            } 
        loop_rate.sleep();
    }
}