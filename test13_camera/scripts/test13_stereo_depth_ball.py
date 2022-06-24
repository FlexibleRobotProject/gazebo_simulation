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


bridge = CvBridge()
hfov = 1.3962634
image_width = 800
flength = (image_width/2) / ( math.tan(hfov/2) )
base_line = 0.07
cx = 400
cy = 400


def callback(left_ros_image,right_ros_image):
    global flength
    global cx 
    global cy

    left_cv_image = bridge.imgmsg_to_cv2(left_ros_image)
    right_cv_image = bridge.imgmsg_to_cv2(right_ros_image)




    #仅作测试用途,图像处理小球测距，后续改为yolo

    #灰度图转换
    grayl = cv2.cvtColor(left_cv_image, cv2.COLOR_BGR2GRAY) 
    grayr = cv2.cvtColor(right_cv_image, cv2.COLOR_BGR2GRAY)
    #阈值二值化,颜色反转
    ret1l,andMaskBil = cv2.threshold(grayl, 100, 255, cv2.THRESH_BINARY_INV); 
    ret1r,andMaskBir = cv2.threshold(grayr, 100, 255, cv2.THRESH_BINARY_INV); 
    #轮廓提取        
    contoursl, hierarchyl = cv2.findContours(andMaskBil.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursr, hierarchyr = cv2.findContours(andMaskBir.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #轮廓中心矩代表横纵坐标
    cntl = contoursl[0]
    Ml = cv2.moments(cntl)
    cxl_f=((Ml['m10']/Ml['m00']))
    cyl_f=((Ml['m01']/Ml['m00']))
    cntr = contoursr[0]
    Mr = cv2.moments(cntr)
    cxr_f=((Mr['m10']/Mr['m00'])) 
    cyr_f=((Mr['m01']/Mr['m00']))




   
    disparity = abs(cxl_f - cxr_f)
    depth =   (flength * base_line)/(disparity)
    x =  ((cxl_f - cx) * base_line)/(disparity)
    y = (( cyl_f - cy) * base_line)/(disparity)
    #print(x)
    #print(y)
    print(depth)

    #仅作测试用途，显示在darknet中执行
    cv2.imshow('left_image',left_cv_image)
    cv2.imshow('andMaskBil',andMaskBil)

    key =cv2.waitKey(30)


if __name__ == '__main__':
    rospy.init_node('stero_depth_cal_node', anonymous=True)

    left_ros_image = message_filters.Subscriber("/stereocamera/left/image_raw", Image)
    right_ros_image =message_filters.Subscriber("/stereocamera/right/image_raw", Image)

    ts = message_filters.TimeSynchronizer([left_ros_image , right_ros_image], 10)
    ts.registerCallback(callback)

    rospy.spin()