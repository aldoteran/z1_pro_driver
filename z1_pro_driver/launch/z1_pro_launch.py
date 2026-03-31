from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

from smarc_msgs.msg import Topics as SmarcTopics
from z1_pro_msgs.msg import Topics as Z1ProTopics


def generate_launch_description():
    cmd_topic = Z1ProTopics.CMD_TOPIC
    gimbal_ctrl_topic = Z1ProTopics.GIMBAL_CTRL_TOPIC
    gimbal_feedback_topic = Z1ProTopics.GIMBAL_FEEDBACK_TOPIC
    odom_topic = SmarcTopics.ODOM_TOPIC
    geopoint_topic = SmarcTopics.POS_LATLON_TOPIC

    # Namespace as command line argument.
    namespace_arg = DeclareLaunchArgument(
        "namespace", default_value="", description="Namespace for the nodes.")
    ns = LaunchConfiguration("namespace")
    frame_prefix_arg = DeclareLaunchArgument(
        "tf_frame_prefix", default_value="", description="Prefix for TF frames.")
    frame_prefix = LaunchConfiguration("tf_frame_prefix")

    # IP:PORT of the camera
    ip_arg = DeclareLaunchArgument(
        "camera_ip", default_value="192.168.1.108", description="IP address of the camera.")
    port_arg = DeclareLaunchArgument(
        "camera_port", default_value="2332", description="TCP port of the camera.")
    port = LaunchConfiguration("camera_port")
    ip = LaunchConfiguration("camera_ip")

    # Whether to use the vehicles altitude or constrain it to the 2d plane.
    altitude_arg = DeclareLaunchArgument(
        "use_vehicle_altitude", default_value='False', description="2D or 3D odom.")
    use_altitude = LaunchConfiguration("use_vehicle_altitude")

    pkg_share = get_package_share_directory("z1_pro_driver")
    urdf_path = os.path.join(pkg_share, "urdf", "z1_pro_camera.urdf")

    with open(urdf_path, "r") as f:
        robot_description = f.read()

    return LaunchDescription([
        namespace_arg,
        altitude_arg,
        frame_prefix_arg,
        ip_arg,
        port_arg,
        # Launch robot state publisher and gimbal joint publisher,
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=ns,
            output="screen",
            parameters=[{
                "robot_description": robot_description,
                "frame_prefix": frame_prefix
            }],
        ),
        Node(
            package="z1_pro_driver",
            executable="gimbal_joint_publisher",
            namespace=ns,
            output="screen",
            parameters=[{
                "gimbal_feedback_topic": gimbal_feedback_topic,
                "use_vehicle_altitude": use_altitude
            }],
        ),

        # Launch low-level driver and high-level interface.
        Node(
            package="z1_pro_driver",
            executable="read_and_publish.py",
            namespace=ns,
            output="screen",
            parameters=[{
                "gimbal_ctrl_topic": gimbal_ctrl_topic,
                "gimbal_feedback_topic": gimbal_feedback_topic,
                "camera_ip": ip,
                "camera_port": port
            }],
        ),
        Node(
            package="z1_pro_driver",
            executable="gimbal_interface_node",
            namespace=ns,
            output="screen",
            parameters=[{
                "cmd_topic": cmd_topic,
                "gimbal_ctrl_topic": gimbal_ctrl_topic,
                "odom_topic": odom_topic,
                "geopoint_topic": geopoint_topic
            }],
        ),
    ])
