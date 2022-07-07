## Description
A 3D collision-free path planning algorithm based on RRT and SP-RRT specialized for 8-link hyper-redundant robot implemented using ROS.

**Distro:**
  Ros neotic <br  />

The algorithm find an 3D optimized path for a one obstacle environment. The visualtization is done in **RVIZ** and the code is written in **C++**.  <br  />

The package has **three** executables: <br  />
1. rrt_node <br  />
2. sp_rrt node <br />
3. env_node <br  /><br  />

## RVIZ parameters:  <br  />
1. Frame_id = "/path_planner"  <br  />
2. marker_topic = "path_planner_rrt"  <br  />

## Instructions:  <br  />

1. Open terminal and type  <br  />
  $roscore  <br  />
2. Open new terminal and go to the the root of your catkin workspace  <br  />
  $catkin_make  <br  />
  $source ./devel/setup.bash  <br  />
  $rosrun path_planning env_node  <br  />
3. open new terminal  <br  />
  $rosrun rviz rviz  <br  />
4. In the RVIZ window, change:  <br  />
  fixed frame under global option to "/path_planner"  <br  />
  add a marker and change marker topic to "path_planner_rrt"  <br  />
5. Open new terminal  <br  />
  To run RRT algorithm:
  $rosrun path_planning rrt_node  <br  /> 
  To run SP_RRT algorithm:
  $rosrun path_planning sp_rrt_node <br />

## Reference:<br />
**Code:** based on a planar RRT implementation from https://github.com/nalin1096/path_planning. <br />
**SP-RRT:** H. Wei, Y. Zheng and G. Gu, "RRT-Based Path Planning for Follow-the-Leader Motion of Hyper-Redundant Manipulators," 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2021, pp. 3198-3204.<br />

## Visualization
![Alt text](figure/sp-rrt.png  "sp-rrt for one source node") <br  />
