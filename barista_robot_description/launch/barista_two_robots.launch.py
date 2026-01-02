from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_path = get_package_share_directory('barista_robot_description')
    urdf_file = os.path.join(
        pkg_path,
        'urdf',
        'barista_robot_model.urdf'
    )

    # -------------------------------
    # START GAZEBO WITH FACTORY PLUGIN
    # -------------------------------
    gazebo = ExecuteProcess(
        cmd=[
            'gazebo',
            '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so'
        ],
        output='screen'
    )

    # -------------------------------
    # RICK ROBOT STATE PUBLISHER
    # -------------------------------
    rick_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='rick',
        parameters=[{
            'robot_description': Command(['cat ', urdf_file])
        }],
        output='screen'
    )

    # -------------------------------
    # MORTY ROBOT STATE PUBLISHER
    # -------------------------------
    morty_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='morty',
        parameters=[{
            'robot_description': Command(['cat ', urdf_file])
        }],
        output='screen'
    )

    # -------------------------------
    # SPAWN RICK
    # -------------------------------
    rick_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'rick',
            '-topic', '/rick/robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )

    # -------------------------------
    # SPAWN MORTY
    # -------------------------------
    morty_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'morty',
            '-topic', '/morty/robot_description',
            '-x', '2.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rick_rsp,
        morty_rsp,
        rick_spawn,
        morty_spawn
    ])
