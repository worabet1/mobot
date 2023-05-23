#!/usr/bin/env python3

import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
offsetx = 1.00
offsety = 3.00
offsetyaw = 5.0
def generate_launch_description():
    
    initial_node = Node(
            package='custom_nav',
            executable='initial_pose.py',
            name='initPose',
            output='screen',
        )
    gamecontroller_node = Node(
        package='custom_nav',
        executable='game_controller.py',
        name='gameController',
        output='screen',
    )
    robot0_node = Node(
        package='custom_nav',
        executable='robot0.py',
        name='robot0Node',
        output='screen',
    )
    robot1_node = Node(
        package='custom_nav',
        executable='robot1.py',
        name='robot1Node',
        output='screen',
    )
    # Create the launch description and add the custom node
    ld = LaunchDescription()
    ld.add_action(initial_node)
    ld.add_action(gamecontroller_node)
    # ld.add_action(robot0_node)
    # ld.add_action(robot1_node)

    return ld