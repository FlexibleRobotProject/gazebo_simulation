#! /usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.msg import ModelStates

import sys
import select
import termios
import tty

pub_flag = 0


def getKey():
    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

    if rlist:
        key = sys.stdin.read(1)  # 读取终端上的交互输入
    else:
        key = 'a'

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    return key



def callback1(ModelStates):

    global pub_flag



    pose_msg = ModelState()
    pose_msg.model_name = 'test13'

    for i in range(len(ModelStates.name)):
        if ModelStates.name[i] == "test13":
            pose_msg.pose.position.x = ModelStates.pose[i].position.x
            pose_msg.pose.position.y = ModelStates.pose[i].position.y
            pose_msg.pose.position.z = ModelStates.pose[i].position.z
            pose_msg.pose.orientation.x = ModelStates.pose[i].orientation.x
            pose_msg.pose.orientation.y = ModelStates.pose[i].orientation.y
            pose_msg.pose.orientation.z = ModelStates.pose[i].orientation.z
            pose_msg.pose.orientation.w = ModelStates.pose[i].orientation.w
    
    key = getKey()
    rospy.loginfo(pose_msg.pose.position.x)
    #if key == 'w':
    pose_msg.pose.position.x += 0.2
    pub_flag = 1
    
    if pub_flag == 1:
        #pub_flag = 0
        pub.publish(pose_msg)








if __name__ == '__main__':
    rospy.init_node('pose_publisher')

    pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)
    rospy.Subscriber('/gazebo/model_states', ModelStates, callback1)

    settings = termios.tcgetattr(sys.stdin)

    rospy.spin()
