#!/usr/bin/env python
import rospy
import sys
import select
import tty
import termios
from std_msgs.msg import String

from gazebo_msgs.msg import ModelState
from gazebo_msgs.msg import ModelStates

from tf.transformations import quaternion_from_euler

import math

from geometry_msgs.msg import Point,Pose, PoseStamped, PoseArray, Quaternion

if __name__ == '__main__':
    rospy.init_node('keyboard')

    pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
    rate = rospy.Rate(100)

    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    print('Please input keys, press Ctrl + C to quit')

    pose_px = 0
    pose_py = 0
    pose_pz = 0
    pose_or = 0
    pose_op = 0
    pose_oy = 0

    pose_msg = ModelState()
    pose_msg.model_name = 'test13'
    pose_msg.pose.position = Point(pose_px,pose_py,pose_pz)
    pose_msg.pose.orientation = Quaternion(*quaternion_from_euler(pose_or, pose_op, pose_oy))

    qnt = quaternion_from_euler(0, 0, 0)
    
    while not rospy.is_shutdown():
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:  # 设置超时参数为0，防止阻塞
            key_input = sys.stdin.read(1)

            if key_input == 'w':

                pose_msg.pose.position.x -= 0.05*math.sin(pose_oy)
                pose_msg.pose.position.y += 0.05*math.cos(pose_oy)
                pub.publish(pose_msg)


            if key_input == 's':
                pose_msg.pose.position.x += 0.05*math.sin(pose_oy)
                pose_msg.pose.position.y -= 0.05*math.cos(pose_oy)
                pub.publish(pose_msg)

            if key_input == 'd':

                pose_oy -= 0.05

                if pose_oy <= -math.pi:
                    pose_oy += 2*math.pi

                rospy.loginfo(pose_oy)
            
                pose_msg.pose.orientation = Quaternion(*quaternion_from_euler(pose_or, pose_op, pose_oy))

                pub.publish(pose_msg)

            if key_input == 'a':

                pose_oy += 0.05
                if pose_oy >= math.pi:
                    pose_oy -= 2*math.pi

                rospy.loginfo(pose_oy)

                pose_msg.pose.orientation = Quaternion(*quaternion_from_euler(pose_or, pose_op, pose_oy))   

                pub.publish(pose_msg)

        rate.sleep()  # 使用sleep()函数消耗剩余时间
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
