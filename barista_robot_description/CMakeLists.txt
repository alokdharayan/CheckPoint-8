cmake_minimum_required(VERSION 3.5)
project(barista_robot_description)

find_package(ament_cmake REQUIRED)

# 🔴 THIS WAS MISSING OR WRONG
install(
  DIRECTORY
    launch
    urdf
    meshes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
