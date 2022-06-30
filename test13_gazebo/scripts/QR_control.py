#! /usr/bin/env python
from yaml import YAMLError
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

    pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)

    # rospy.Subscriber('/gazebo/model_states', ModelStates, callback1)

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(50.0)

    pose_px = 0
    pose_py = 3
    pose_pz = 0.017317
    pose_or = 0
    pose_op = 0
    pose_oy = 0

    pose_msg = ModelState()
    pose_msg.model_name = 'test13'
    pose_msg.pose.position = Point(pose_px, pose_py, pose_pz)
    pose_msg.pose.orientation = Quaternion(
        *quaternion_from_euler(pose_or, pose_op, pose_oy))

    pose_target_px = 1
    pose_target_py = 8
    pose_target_doy = math.atan(
        (pose_target_px-pose_px)/(pose_target_py-pose_py))
    pose_target_dr = math.sqrt((pose_target_px-pose_px)**2 + (pose_target_py-pose_py)**2)


    rospy.loginfo(pose_target_doy)
    rospy.loginfo(range(int(pose_target_doy/0.01)))


    step1_flag = 1
    step1_num = int(pose_target_doy/0.01)

    step2_flag = 0
    step2_num = int(pose_target_dr/0.01)    

    step3_flag = 0
    step3_num = int(pose_target_doy/0.01)

    while not rospy.is_shutdown():
        try:
            # trans = tfBuffer.lookup_transform(
            #    'base_footprint', 'ar_marker_0', rospy.Time())

            #t_x = trans.transform.translation.y

            #t_y = trans.transform.translation.z

            #t_z = trans.transform.translation.x

            #r_x = trans.transform.rotation.x
            #r_y = trans.transform.rotation.y
            #r_z = trans.transform.rotation.z
            #r_w = trans.transform.rotation.w

            #yaw = euler_from_quaternion([r_x, r_y, r_z, r_w])[2]

            # rospy.loginfo(yaw)

            #rospy.loginfo(t_x, t_y)

            # if abs(t_x) > 2 or abs(t_y) > 2:

            #pose_msg.pose.position.x -= 0.05*math.sin(pose_y)
            #pose_msg.pose.position.y += 0.05*math.cos(pose_y)
            # pub.publish(pose_msg)
            if  step1_flag == 1 and abs(step1_num) >= 1:

                if step1_num >= 1:
                    step1_num -= 1
                    pose_oy -= 0.01
                else :
                    step1_num += 1
                    pose_oy += 0.01

                if step1_num == 0:
                    step1_flag = 0
                    step2_flag = 1

                pose_msg.pose.orientation = Quaternion(*quaternion_from_euler(pose_or, pose_op, pose_oy))
                rospy.loginfo(pose_oy)
                pub.publish(pose_msg)

            if  step2_flag == 1 and abs(step2_num) >= 1:

                if step2_num >= 1:
                    step2_num -= 1
                    pose_msg.pose.position.x -= 0.01*math.sin(pose_oy)
                    pose_msg.pose.position.y += 0.01*math.cos(pose_oy)
                else :
                    step2_num += 1
                    pose_msg.pose.position.x += 0.01*math.sin(pose_oy)
                    pose_msg.pose.position.y -= 0.01*math.cos(pose_oy)


                if step2_num == 0:
                    step2_flag = 0
                    step3_flag = 1

                pub.publish(pose_msg)

            if  step3_flag == 1 and abs(step3_num) >= 1:

                if step3_num >= 1:
                    step3_num -= 1
                    pose_oy += 0.01
                else :
                    step3_num += 1
                    pose_oy -= 0.01

                if step3_num == 0:
                    step3_flag = 0

                pose_msg.pose.orientation = Quaternion(*quaternion_from_euler(pose_or, pose_op, pose_oy))
                rospy.loginfo(pose_oy)
                pub.publish(pose_msg)


            rate.sleep()


        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
