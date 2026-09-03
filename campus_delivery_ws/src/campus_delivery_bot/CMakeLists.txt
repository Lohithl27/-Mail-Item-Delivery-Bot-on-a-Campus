cmake_minimum_required(VERSION 3.8)
project(campus_delivery_bot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/DeliveryTask.srv"
  DEPENDENCIES geometry_msgs std_msgs
)

install(PROGRAMS
  campus_delivery_bot/delivery_dispatcher.py
  campus_delivery_bot/delivery_client.py
  campus_delivery_bot/demo_delivery_sequence.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  config
  docs
  launch
  rviz
  urdf
  worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
