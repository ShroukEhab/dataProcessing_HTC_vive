#!/usr/bin/env python

import rospy
import math as m
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import Int32MultiArray
from matplotlib import pyplot as plt
import numpy as np
import scipy
from scipy.integrate import simps
from scipy.interpolate import InterpolatedUnivariateSpline
import time

QUEUE_SIZE = 5

prev_ts = 0
prev_omega_x = []
prev_omega_y = []
prev_omega_z = []
prev_omega_x.append(0)
prev_omega_y.append(0)
prev_omega_z.append(0)
avg_omega_x = 0
avg_omega_y = 0
avg_omega_z = 0
prev_avg_omega_x = 0
prev_avg_omega_y = 0
prev_avg_omega_z = 0
theta_x = 0
theta_y = 0
theta_z = 0
t_0 = 0
i=0
fil_omega_x = []
fil_omega_y = []
fil_omega_z = []
time_s = []
#time.append(0)

pub = rospy.Publisher("rotation_angles", Int32MultiArray, queue_size=10)

def push_to_queue( queue, value ):
    new_queue = queue
    new_queue.append(value)
    if len(new_queue) >= QUEUE_SIZE:
        new_queue = new_queue[1:]
    return new_queue

def average_queue( queue ):
    queue_sum = sum(queue)
    queue_len = len(queue)
    average = queue_sum/queue_len
    return average

def trapezoidal_accumulation(prev_omega, cur_omega, prev_time, cur_time, prev_theta):
    return prev_theta + ((prev_omega+cur_omega)*(cur_time-prev_time)/2)
    #return prev_theta + ((prev_omega+cur_omega)*0.002/2)
    


def rad2deg(radian):
    return radian*180/m.pi

def callback(msg):
    global prev_omega_x, prev_omega_y, prev_omega_z
    global avg_omega_x, avg_omega_y, avg_omega_z
    global prev_avg_omega_x, prev_avg_omega_y, prev_avg_omega_z
    global theta_x, theta_y, theta_z, prev_ts
    global pub
    global t_0, i
    global fil_omega_x, fil_omega_y, fil_omega_z
    
    i +=1
    ts = msg.header.stamp.secs + (msg.header.stamp.nsecs * 1e-9)
    #ts = msg.header.stamp.secs
    time_s.append(ts)
    omega_x = msg.twist.angular.x
    omega_y = msg.twist.angular.y
    omega_z = msg.twist.angular.z
    # data processing
    ## Filtering data with moving average
    ### push value to queue
    prev_omega_x = push_to_queue(prev_omega_x, omega_x)
    prev_omega_y = push_to_queue(prev_omega_y, omega_y)
    prev_omega_z = push_to_queue(prev_omega_z, omega_z)
    ### average queue to get moving average
    avg_omega_x = average_queue(prev_omega_x)
    avg_omega_y = average_queue(prev_omega_y)
    avg_omega_z = average_queue(prev_omega_z)

    ## append avergae omegas to be integrated 
    fil_omega_x.append(avg_omega_x)
    fil_omega_y.append(avg_omega_y)
    fil_omega_z.append(avg_omega_z)
    ## Acuumulate data
    # theta_x = rad2deg(trapezoidal_accumulation(prev_avg_omega_x, avg_omega_x, prev_ts, ts, theta_x))%180
    # theta_y = rad2deg(trapezoidal_accumulation(prev_avg_omega_y, avg_omega_y, prev_ts, ts, theta_y))%180
    # theta_z = rad2deg(trapezoidal_accumulation(prev_avg_omega_z, avg_omega_z, prev_ts, ts, theta_z))%180

    ## integration
    # theta_x =  rad2deg(scipy.integrate.simps(fil_omega_x))%180
    # theta_y = rad2deg(scipy.integrate.simps(fil_omega_y))%180
    # theta_z = rad2deg(scipy.integrate.simps(fil_omega_z))%180
    # theta_x = InterpolatedUnivariateSpline(time_s,avg_omega_x, k=1)
    # theta_x = rad2deg(theta_x.integral(1.5, 2.2))%180
    # theta_y = InterpolatedUnivariateSpline(time_s, avg_omega_y, k=1)
    # theta_y = rad2deg(theta_y.integral(1.5, 2.2))%180
    # theta_z = InterpolatedUnivariateSpline(time_s, avg_omega_z, k=1)
    # theta_z = rad2deg(theta_z.integral(1.5, 2.2))%180
    theta_x = scipy.integrate.trapz(fil_omega_x, time_s)
    theta_x = rad2deg(theta_x) + 90
    theta_y = scipy.integrate.trapz(fil_omega_y, time_s)
    theta_y = rad2deg(theta_y) + 90
    #theta_x = 90
    #theta_y = 90
    theta_z = scipy.integrate.trapz(fil_omega_z, time_s)
    theta_z = -rad2deg(theta_z) - 20




    #rospy.loginfo("%f --> %f, %f, %f", ts, omega_x, omega_y, omega_z)
    #rospy.loginfo("%d --> %d, %d, %d", ts, int(theta_x), int(theta_y), int(theta_z))

    #pub.publish(data=[int(theta_x), int(theta_y), int(theta_z)])
    pub.publish(Int32MultiArray(data=[int(theta_x), int(theta_y), int(theta_z)]))
    #if i >= 0 and i<=50:
    # plt.plot((i), theta_x, 'r*')
    # plt.plot((i), theta_y, 'b-')
    # plt.plot((i), theta_z, 'g+')
    # plt.axis("equal")
    # plt.draw()
    # plt.pause(0.000000000001)

    # Saving data from previous sample
    prev_avg_omega_x = avg_omega_x
    prev_avg_omega_y = avg_omega_y
    prev_avg_omega_z = avg_omega_z
    prev_ts = ts

    ## Latency calculation
    receive_timestamp = rospy.get_rostime()
    send_timestamp = rospy.Time.from_sec(time.time())
    latency = receive_timestamp - send_timestamp
    rospy.loginfo("Latency: %f seconds", latency.to_sec())
    

#rospy.loginfo('x: {}, y:{}, orientation_z:{},' .format(x,y, orientation_z))

def main():
    global t_0 
    
    rospy.init_node('sub_vive_pub_ard')
    rate = rospy.Rate(20) #HZ

    #rospy.Subscriber("/test_data",TwistStamped,callback)
    rospy.Subscriber("/vive/twist0",TwistStamped,callback)
    t_0 = rospy.Time.now().secs
    # plt.ion()
    # plt.show()
    rate.sleep()
    rospy.spin()
    

if __name__ == '__main__':
    main()