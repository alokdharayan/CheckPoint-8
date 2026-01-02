from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_path = get_package_share_directory('barista_robot_description')
    xacro_file = os.path.join(
        pkg_path,
        'urdf',
        'barista_robot_model.urdf.xacro'
    )

    rick_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='rick',
        parameters=[{
            'robot_description': Command(['xacro ', xacro_file])
        }]
    )

    morty_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='morty',
        parameters=[{
            'robot_description': Command(['xacro ', xacro_file])
        }]
    )

    rick_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'rick',
            '-topic', '/rick/robot_description',
            '-x', '0.0', '-y', '0.0'
        ]
    )

    morty_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'morty',
            '-topic', '/morty/robot_description',
            '-x', '2.0', '-y', '0.0'
        ]
    )

    return LaunchDescription([
        rick_rsp,
        morty_rsp,
        rick_spawn,
        morty_spawn
    ])
