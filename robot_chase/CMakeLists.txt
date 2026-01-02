cmake_minimum_required(VERSION 3.5)
project(robot_chase)

# Compiler warnings (good practice)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

# Executable
add_executable(robot_chase src/robot_chase.cpp)

ament_target_dependencies(
  robot_chase
  rclcpp
  geometry_msgs
  tf2
  tf2_ros
  tf2_geometry_msgs
)

# Install
install(TARGETS
  robot_chase
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
