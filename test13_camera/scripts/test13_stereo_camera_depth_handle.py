#!/usr/bin/env python

'''
定位时，我们需要以下几个参数：
1.相机焦距 :          flength            单位 :pixel(像素）
2.两个相机的距离即基线: baseline           单位 :m(米)
3.图像的大小(分辨率):  height x width      单位 :pixel(像素）
  理想相机中点坐标:    cx = wigth/2,cy = height/2(无畸变)
4.定位的点在左右目中的图像定位的点 (xl,yl),(xr,yr)  单位:pixel(像素）

其中,前3个参数在相机固定时就已经是定值,第4个参数需要我自行得到

深度depth和x,y的位置(相对于左目）：
                                disparity = abs(xl- xr)
                                depth =   (flength * baseline)/(disparity)
                                x =  ((xl - cx) * baseline)/(disparity)
                                y = (( yl - cy) * baseline)/(disparity)
'''

import rospy
import cv2
import message_filters
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import math #计算正切
import numpy as np

from darknet_ros_msgs.msg  import BoundingBoxes

bridge = CvBridge()
hfov = 1.3962634
image_width = 800
flength = (image_width/2) / ( math.tan(hfov/2) )
base_line = 0.07
cx = 400
cy = 400


l_xmin = 0  
l_ymin = 0
l_xmax = 0
l_ymax = 0

r_xmin = 0  
r_ymin = 0
r_xmax = 0
r_ymax = 0



def callback1(BoundingBoxes):

    global l_xmin,l_ymin,l_xmax,l_ymax

    num_box =len(BoundingBoxes.bounding_boxes)
    if num_box >= 2:
       return
    box1 = BoundingBoxes.bounding_boxes[0]
    if box1.Class  != 'handle':
        return
    
    l_xmin = box1.xmin  
    l_ymin = box1.ymin
    l_xmax = box1.xmax
    l_ymax = box1.ymax

def callback2(BoundingBoxes):

    global r_xmin,r_ymin,r_xmax,r_ymax

    num_box =len(BoundingBoxes.bounding_boxes)
    if num_box >= 2:
       return
    box1 = BoundingBoxes.bounding_boxes[0]
    if box1.Class  != 'handle':
        return
    
    r_xmin = box1.xmin  
    r_ymin = box1.ymin
    r_xmax = box1.xmax
    r_ymax = box1.ymax


# 正戏
def callback3(left_ros_image,right_ros_image):
    global flength
    global cx 
    global cy

    global cxl_f,cyl_f,cxr_f,cy_f

    #转换为cv格式
    left_cv_image = bridge.imgmsg_to_cv2(left_ros_image)
    right_cv_image = bridge.imgmsg_to_cv2(right_ros_image)
    #截取物体框
    object_left = left_cv_image[l_ymin:l_ymax-1,l_xmin:l_xmax-1]
    object_right = right_cv_image[r_ymin:r_ymax-1,r_xmin:r_xmax-1]   
    #转换为灰度图
    grayl = cv2.cvtColor(object_left, cv2.COLOR_BGR2GRAY) 
    grayr = cv2.cvtColor(object_right, cv2.COLOR_BGR2GRAY) 
    #自适应阈值
    ret1l,andMaskBil = cv2.threshold(grayl,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1r,andMaskBir = cv2.threshold(grayr,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #闭运算去噪
    operation_kernel = np.ones((3,3), np.uint8)
    andMaskBil = cv2.morphologyEx(andMaskBil, cv2.MORPH_CLOSE, operation_kernel,iterations=5)
    andMaskBir = cv2.morphologyEx(andMaskBir, cv2.MORPH_CLOSE, operation_kernel,iterations=5)
    #取轮廓
    contoursl, hierarchyl = cv2.findContours(andMaskBil.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursr, hierarchyr = cv2.findContours(andMaskBir.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #取中心矩，坐标变换回完整图像
    cntl = contoursl[0]
    Ml = cv2.moments(cntl)
    cxl_f=((Ml['m10']/Ml['m00'])) + l_xmin
    cyl_f=((Ml['m01']/Ml['m00'])) + l_ymin

    cntr = contoursr[0]
    Mr = cv2.moments(cntr)
    cxr_f=((Mr['m10']/Mr['m00'])) + r_xmin
    cyr_f=((Mr['m01']/Mr['m00'])) + r_ymin


    #双目的测距   
    disparity = abs(cxl_f - cxr_f)
    if disparity == 0:
        return
    depth =   (flength * base_line)/(disparity)
    x =  ((cxl_f - cx) * base_line)/(disparity)
    y = (( cyl_f - cy) * base_line)/(disparity)
    print(x)
    print(y)
    print(depth)

    #随便看看
    cv2.circle(left_cv_image, (int(cxl_f), int(cyl_f)), 5, (0, 0, 255), 0)
    cv2.circle(right_cv_image, (int(cxr_f), int(cyr_f)), 5, (0, 0, 255), 0)
    #cv2.imshow('left',left_cv_image)
    key =cv2.waitKey(30)


if __name__ == '__main__':
    rospy.init_node('stero_depth_cal_node', anonymous=True)

    #这个或许也能用同步器，有时间试试
    rospy.Subscriber("/darknet_ros/left/bounding_boxes",BoundingBoxes,callback1)
    rospy.Subscriber("/darknet_ros/right/bounding_boxes",BoundingBoxes,callback2)

    left_ros_image = message_filters.Subscriber("/stereocamera/left/image_raw", Image)
    right_ros_image =message_filters.Subscriber("/stereocamera/right/image_raw", Image)

    ts = message_filters.TimeSynchronizer([left_ros_image , right_ros_image], 10)
    ts.registerCallback(callback3)

    rospy.spin()