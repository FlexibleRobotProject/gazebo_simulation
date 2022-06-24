#!/usr/bin/env python

import rospy
import cv2
import cv_bridge
from sensor_msgs.msg import Image  # ROS内图片消息格式


image_num = 59

# 图片转换类，订阅ROS图片消息并转换为OpenCV格式处理
class Image_converter:

    def __init__(self):

        # 初始化图片转换功能
        self.bridge = cv_bridge.CvBridge()

        self.image_sub = rospy.Subscriber(
            "/stereocamera/right/image_raw", Image, self.callback)

        # 可用的发布者
        #self.image_pub = rospy.Publisher("cv_bridge_image", Image, queue_size=1)


    def callback(self, data):

        global image_num

        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        (rows, cols, channels) = cv_image.shape  # 获得转换后图片的宽度、高度和图片通道数

        # 转换回ROS图片消息格式并发布
        # self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))

        # OpenCV创建窗口显示图片
        #cv2.circle(cv_image, (40, 40), 20, (0, 255, 0), 2)  # 画一个圆
        cv2.imshow("cv_image", cv_image)  # OpenCV创建窗口显示图片
        
        k = cv2.waitKey(10)

        if k == ord('s'):  # 按s保存并退出

            image_num += 1
            image_name = '/home/xz/car/src/test13_camera/img/'+str(image_num)+'.jpg'

            cv2.imwrite(image_name, cv_image)
            cv2.destroyAllWindows()

            rospy.loginfo(image_name)
        k = 0
        #cv2.imwrite('dashen_compressed.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])


if __name__ == '__main__':

    rospy.init_node("test13_image_capture_node")

    Image_converter()

    rospy.spin()
