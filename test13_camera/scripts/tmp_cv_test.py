#!/usr/bin/env python

##测试轮廓中心矩的坐标变换

import cv2
import numpy as np

img = cv2.imread('/home/xz/Pictures/1.png')

grayl = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
print(grayl)

ret1l,andMaskBil = cv2.threshold(grayl,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

operation_kernel = np.ones((3,3), np.uint8)
andMaskBil = cv2.morphologyEx(andMaskBil, cv2.MORPH_CLOSE, operation_kernel,iterations=5)

contoursl, hierarchyl = cv2.findContours(andMaskBil.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cntl = contoursl[0]
Ml = cv2.moments(cntl)
cxl_f=((Ml['m10']/Ml['m00']))
cyl_f=((Ml['m01']/Ml['m00']))

print(cxl_f,cyl_f)

point_size = 1
point_color = (0, 0, 255) # BGR
thickness = 4 # 可以为 0 、4、8

cv2.circle(img, (int(cxl_f), int(cyl_f)), 5, (0, 0, 255), 0)

cv2.imshow('andMaskBil',img)
key =cv2.waitKey(0)