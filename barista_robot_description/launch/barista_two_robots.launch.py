from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg = get_package_share_directory('barista_robot_description')
    urdf_file = os.path.join(pkg, 'urdf', 'barista_robot_model.urdf')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # 🔴 START GAZEBO WITH FACTORY PLUGIN (THIS IS THE KEY)
    gazebo = ExecuteProcess(
        cmd=[
            'gazebo',
            '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so'
        ],
        output='screen'
    )

    rick_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='rick',
        parameters=[{'robot_description': robot_description}]
    )

    morty_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='morty',
        parameters=[{'robot_description': robot_description}]
    )

    rick_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'rick',
            '-topic', '/rick/robot_description'
        ]
    )

    morty_spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'morty',
            '-topic', '/morty/robot_description',
            '-x', '2.0'
        ]
    )

    return LaunchDescription([
        gazebo,
        rick_rsp,
        morty_rsp,
        rick_spawn,
        morty_spawn
    ])
