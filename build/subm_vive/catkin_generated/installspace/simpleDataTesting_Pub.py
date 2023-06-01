#!/usr/bin/env python3

import rospy
import numpy as np
import math as m
from geometry_msgs.msg import TwistStamped
from matplotlib import pyplot as plt

def main():
    pub = rospy.Publisher("test_data", TwistStamped, queue_size=10)
    rospy.init_node("test_data_publisher", anonymous=True)
    rate = rospy.Rate(10)
    i = 0
    # plt.ion()
    # plt.show()
    while not rospy.is_shutdown():
        msg = TwistStamped()
        msg.header.stamp = rospy.Time.now() 
        msg.twist.angular.x = 50*m.sin(3*i)
        msg.twist.angular.y = 3*m.sin(1*i)
        msg.twist.angular.z = 1*m.sin(2*i)
        pub.publish(msg)
        i = i+1
        # if i >= 0 and i <= 100:
        #     plt.plot(i, msg.twist.angular.x, '*')
        #     plt.plot(i, msg.twist.angular.y, '-')
        #     plt.plot(i, msg.twist.angular.z, '+')
        #     plt.axis("equal")
        #     plt.draw()
        #     plt.pause(0.0000001)
       
        #rospy.loginfo(msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
