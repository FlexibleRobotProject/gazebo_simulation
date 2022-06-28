# gazebo_simulation

:star:6.28更新
---
### 修改 test13_gazebo包

实现键盘控制


:star:6.27更新
---
### 增加 darknet_ros yolov3 元包

**darknet功能包（训练）：**

<img width="527" alt="image" src="https://user-images.githubusercontent.com/82652238/175869546-31e445df-bc96-4201-927b-939b3f03d1d3.png">

**darknet_ros包（ros接口）**

<img width="430" alt="image" src="https://user-images.githubusercontent.com/82652238/175869823-631f2935-73f1-480b-bb36-0e10d938861a.png">

**darknet_ros_message包（自定义话题）**

已经封好节点，别动

**log文件夹（量化脚本）**

<img width="316" alt="image" src="https://user-images.githubusercontent.com/82652238/175871102-4c8608ff-c2a6-4ac7-80d1-1a3ee39ef6ed.png">

### 增加 ar_track_alvar 包

QR识别，调试中

### 修改 test13_moveit_config 包

将joint_state_publisher节点移入test13_gazebo包中，确保环境和controller与moveit控制的完全解耦


### 修改 test13 包

引入深度相机；配置rviz config

### 修改 test13_gazebo 包

引入QR+ISCAS world;增加配套的launch

键盘控制调试中

### 修改 test13_camera 包

test13_stereo_camera_depth_handle.launch：双目测距，与yolo部分结合，已实现，组会中展示

test13_depth_camera_QR_detection.launch：二维码识别，待测试

还用部分零散的脚本，等到完整功能实现后，统一重构优化

:star:6.24更新
---
### 增加 test13_camera 双目包
1.img文件夹：gazebo中采样100张门把手

2.launch文件夹：

test13_gazebo_ISCAS_world_capture.launch：键盘控制(ctrl+s)，ISCAS中采集摄像头照片，保存路径为img文件夹下

3.scripts文件夹：

test13_image_capture.py：双目采样的脚本

test13_stereo_depth_ball.py：双目测距，已实现，暂时用传统检测的小球代替，下一版本和yolo的目标检测组合在一起

### 修改test13 模型包
更改了urdf/sensors文件夹中摄像头参数，添加部分注释
### 修改test13_gazebo gazebo端+HW+controller
1.增加环境test13_gazebo_ISCAS_world.launch，启动test13_bringup_moveit.launch中对应适当更改，原环境文件改为test13_gazebo_empty_world.launch

2.将原初始化中位置初始化，扩展为位姿初始化

3.增加set_gazebo_pose替代差速插件的测试脚本：car_state_control.py

:star:6.23更新
---

### test13 模型包
![image](https://user-images.githubusercontent.com/82652238/175348804-0646e160-45e2-4382-8b94-b0e10ed39330.png)
### test13_moveit_config 机械臂控制
![image](https://user-images.githubusercontent.com/82652238/175349145-b32e048f-345e-44c1-b6fd-e4f54c9a181b.png)
![image](https://user-images.githubusercontent.com/82652238/175349275-406815ce-20e2-4c10-bf0f-530b85fe527a.png)
![image](https://user-images.githubusercontent.com/82652238/175349728-f0e7ea38-c452-4ec2-8892-e569de544773.png)
### test13_gazebo gazebo端+HW+controller 
![image](https://user-images.githubusercontent.com/82652238/175349574-18dfec5e-c594-4ce1-8570-4808947982a9.png)
### test13_demo python接口



