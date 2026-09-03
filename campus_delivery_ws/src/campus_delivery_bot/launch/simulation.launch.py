"""Launch the campus delivery robot in Gazebo with optional Nav2 and RViz."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("campus_delivery_bot")
    gazebo_share = get_package_share_directory("gazebo_ros")
    nav2_share = get_package_share_directory("nav2_bringup")

    world = os.path.join(pkg_share, "worlds", "campus.world")
    robot_urdf = os.path.join(pkg_share, "urdf", "campus_delivery_bot.urdf")
    nav2_params = os.path.join(pkg_share, "config", "nav2_params.yaml")
    slam_params = os.path.join(pkg_share, "config", "slam_toolbox.yaml")
    rviz_config = os.path.join(pkg_share, "rviz", "campus_delivery.rviz")

    with open(robot_urdf, "r", encoding="utf-8") as urdf_file:
        robot_description = urdf_file.read()

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_nav2 = LaunchConfiguration("use_nav2")
    use_rviz = LaunchConfiguration("use_rviz")
    demo = LaunchConfiguration("demo")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_share, "launch", "gazebo.launch.py")),
        launch_arguments={"world": world, "verbose": "false"}.items(),
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_share, "launch", "bringup_launch.py")),
        condition=IfCondition(use_nav2),
        launch_arguments={
	    "map":"",
            "use_sim_time": use_sim_time,
            "slam": "True",
            "params_file": nav2_params,
            "slam_params_file": slam_params,
            "autostart": "True",
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="true"),
        DeclareLaunchArgument("use_nav2", default_value="true"),
        DeclareLaunchArgument("use_rviz", default_value="true"),
        DeclareLaunchArgument("demo", default_value="false"),
        SetEnvironmentVariable(
            "GAZEBO_MODEL_PATH",
            os.path.join(pkg_share, "urdf") + os.pathsep + os.environ.get("GAZEBO_MODEL_PATH", ""),
        ),
        gazebo,
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description, "use_sim_time": use_sim_time}],
        ),
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=["-topic", "robot_description", "-entity", "campus_delivery_bot", "-x", "0", "-y", "0", "-z", "0.08"],
            output="screen",
        ),
        nav2,
        Node(
            package="campus_delivery_bot",
            executable="delivery_dispatcher.py",
            output="screen",
            parameters=[
                os.path.join(pkg_share, "config", "locations.yaml"),
                {"use_sim_time": use_sim_time},
            ],
        ),
        Node(
            package="campus_delivery_bot",
            executable="demo_delivery_sequence.py",
            condition=IfCondition(demo),
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            condition=IfCondition(use_rviz),
            arguments=["-d", rviz_config],
            parameters=[{"use_sim_time": use_sim_time}],
            output="screen",
        ),
    ])
