#include <ros/ros.h>
//#include <std_msgs/String.h>
//#include <geometry_msgs/Twist.h>
#include <geometry_msgs/TwistStamped.h>

#define BUFFER_SIZE 5

float omega_x, omega_y, omega_z, prev_omega_x, prev_omega_y, prev_omega_z;
float x_buffer[BUFFER_SIZE], y_buffer[BUFFER_SIZE], z_buffer[BUFFER_SIZE];

void twister_callback(const geometry_msgs::TwistStamped::ConstPtr& msg)
{
  //ROS_INFO("I heard: [%s]", msg->data.c_str());
  ROS_INFO("angular velocies: [%f, %f, %f]", msg->twist.angular.x, msg->twist.angular.y, msg->twist.angular.z);


}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "subm_vive");

  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("vive/twist0", 1000, twister_callback);

  ros::spin();

  return 0;
}