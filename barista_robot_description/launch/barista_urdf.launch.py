from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg = get_package_share_directory('barista_robot_description')
    urdf = os.path.join(pkg, 'urdf', 'barista_robot_model.urdf')

    robot_description = Command(['cat ', urdf])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'barista_robot',
            '-topic', 'robot_description',
            '-z', '1.0'
        ],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn,
        rviz
    ])
