from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

from z1_pro_msgs.msg import Topics as Z1ProTopics


def generate_launch_description():
    cmd_topic = Z1ProTopics.CMD_TOPIC
    
    # Namespace as command line argument.
    namespace_arg = DeclareLaunchArgument(
        "namespace", default_value="", description="Namespace for the nodes.")
    ns = LaunchConfiguration("namespace")

    sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value='False', description="Use simulation time.")
    use_sim_time = LaunchConfiguration("use_sim_time")

    # And finally, launch the action server for gimbal control.
    gimbal_action_server_node = Node(
        package="z1_pro_driver",
        executable="gimbal_action.py",
        namespace=ns,
        output="screen",
        parameters=[{
            "cmd_topic": cmd_topic,
            "use_sim_time": use_sim_time
        }]
    )

    return LaunchDescription([
        namespace_arg,
        sim_time_arg,
        gimbal_action_server_node 
    ])
