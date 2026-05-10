cmake_minimum_required(VERSION 3.0.2)
project(taxi_sim_bringup)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  std_srvs
  geometry_msgs
  topic_tools
)

catkin_package()

# Mark Python scripts as executable
catkin_install_python(PROGRAMS
  nodes/drive_mode_toggle.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Install launch files
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

# Install rviz configs
install(DIRECTORY rviz/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
)