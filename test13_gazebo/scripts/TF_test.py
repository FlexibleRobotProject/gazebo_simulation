#! /usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.msg import ModelStates

from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion

from geometry_msgs.msg import Point, Pose, PoseStamped, PoseArray, Quaternion

import tf2_ros

import math


if __name__ == '__main__':

    rospy.init_node('pose_publisher')


    # rospy.Subscriber('/gazebo/model_states', ModelStates, callback1)

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(50.0)


    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('base_footprint', 'camera_link', rospy.Time())

            #t_x = trans.transform.translation.y

            #t_y = trans.transform.translation.z

            #t_z = trans.transform.translation.x

            #r_x = trans.transform.rotation.x
            #r_y = trans.transform.rotation.y
            #r_z = trans.transform.rotation.z
            #r_w = trans.transform.rotation.w

            #yaw = euler_from_quaternion([r_x, r_y, r_z, r_w])[2]

            # rospy.loginfo(yaw)

            rospy.loginfo(trans)

            # if abs(t_x) > 2 or abs(t_y) > 2:

            #pose_msg.pose.position.x -= 0.05*math.sin(pose_y)
            #pose_msg.pose.position.y += 0.05*math.cos(pose_y)
            # pub.publish(pose_msg)


            rate.sleep()


        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
