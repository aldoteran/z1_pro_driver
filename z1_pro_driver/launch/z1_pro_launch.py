from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Namespace as command line argument.
    namespace_arg = DeclareLaunchArgument(
        "namespace", default_value="", description="Namespace for the nodes.")
    ns = LaunchConfiguration("namespace")

    pkg_share = get_package_share_directory("z1_pro_driver")
    urdf_path = os.path.join(pkg_share, "urdf", "z1_pro_camera.urdf")

    with open(urdf_path, "r") as f:
        robot_description = f.read()

    return LaunchDescription([
        # Launch robot state publisher and gimbal joint publisher,
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=ns,
            output="screen",
            parameters=[{
                "robot_description": robot_description,
                "frame_prefix": ns
            }],
        ),
        Node(
            package="z1_pro_driver",
            executable="gimbal_joint_publisher",
            namespace=ns,
            output="screen",
            parameters=[{
                # TODO: add joint and topic names here.
            }],
        ),

        # Launch low-level driver and high-level interface.
        Node(
            package="z1_pro_driver",
            executable="read_and_publish.py",
            namespace=ns,
            output="screen",
            parameters=[{
                # TODO: add topic names here.
            }],
        ),
        Node(
            package="z1_pro_driver",
            executable="gimbal_interface_node",
            namespace=ns,
            output="screen",
            parameters=[{
                # TODO: add topic names here.
            }],
        ),
    ])
