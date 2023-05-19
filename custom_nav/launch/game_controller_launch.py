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
    
    # initfile = LaunchConfiguration('initpose')

    DeclareLaunchArgument(
        'initpose',
        default_value=os.path.join(get_package_share_directory("custom_nav"),'params',"initpose.yaml"),
        description='Full path to init_pose yaml file to load'),
    
    initial_node = Node(
            package='custom_nav',
            executable='initial_pose.py',
            name='game_controller',
            output='screen',
            # parameters=[initfile]
        )
    custom_node = Node(
        package='custom_nav',
        executable='game_controller.py',
        # arguments=['arg1', 'arg2'],
        output='screen',
    )

    # Create the launch description and add the custom node
    ld = LaunchDescription()
    ld.add_action(initial_node)
    # ld.add_action(custom_node)

    return ld