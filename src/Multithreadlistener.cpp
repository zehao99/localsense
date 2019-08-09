#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Point.h"
#include <boost/thread.hpp>


class multiThreadListener
{
public:
	multiThreadListener()
	{	
		sub = n.subscribe("/tag0_position", 1, &multiThreadListener::chatterCallback1,this);
		sub2 = n.subscribe("/tag1_position", 1, &multiThreadListener::chatterCallback2,this);
	}
	void chatterCallback1(const geometry_msgs::Point::ConstPtr& msg);
	void chatterCallback2(const geometry_msgs::Point::ConstPtr& msg);

private:
	ros::NodeHandle n;
	ros::Subscriber sub;
	ros::Subscriber sub2;
};


void multiThreadListener::chatterCallback1(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str());
  ros::Rate loop_rate(0.5);//block chatterCallback2()
  loop_rate.sleep();
}


void multiThreadListener::chatterCallback2(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str());
}
  

int main(int argc, char **argv)
{

  ros::init(argc, argv, "multi_sub");

  multiThreadListener listener_obj;
  ros::MultiThreadedSpinner s(2);
  ros::spin(s);

  return 0;
}
