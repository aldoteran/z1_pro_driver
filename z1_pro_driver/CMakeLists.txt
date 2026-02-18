cmake_minimum_required(VERSION 3.8)
project(z1_pro_driver)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(PkgConfig)

# Eigen.
pkg_search_module(Eigen3 REQUIRED eigen3)
find_package(Eigen3 REQUIRED NO_MODULE)

# Geographic lib.
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};/usr/share/cmake/geographiclib")
find_package(GeographicLib REQUIRED)

# ROS2 dependencies.
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(geographic_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(z1_pro_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(ament_cmake_python REQUIRED)

add_executable(gimbal_interface_node src/gimbal_interface_node.cpp)
target_include_directories(gimbal_interface_node PUBLIC ./include/${GeographicLib_INCLUDE_DIRS})
target_link_libraries(gimbal_interface_node
  rclcpp::rclcpp
  Eigen3::Eigen
  ${nav_msgs_TARGETS}
  ${geometry_msgs_TARGETS}
  ${std_msgs_TARGETS}
  ${tf2_TARGETS}
  ${tf2_ros_TARGETS}
  ${geographic_msgs_TARGETS}
  ${GeographicLib_LIBRARIES}
  ${z1_pro_msgs_TARGETS}
)

add_executable(gimbal_joint_publisher src/gimbal_joint_publisher.cpp)
target_include_directories(gimbal_joint_publisher PUBLIC)
target_link_libraries(gimbal_joint_publisher
  rclcpp::rclcpp
  ${sensor_msgs_TARGETS}
  ${z1_pro_msgs_TARGETS}
)

install(TARGETS
  gimbal_interface_node
  gimbal_joint_publisher
  DESTINATION lib/${PROJECT_NAME}
)

# To install python nodes.
install(PROGRAMS 
  scripts/read_and_publish.py 
  scripts/order_test_euler.py 
  DESTINATION lib/${PROJECT_NAME}
)

# To install launch and urdf directory. 
install(DIRECTORY
  launch
  urdf
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
