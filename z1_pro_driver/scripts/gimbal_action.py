#!/usr/bin/env python3

import rclpy
from rclpy.node import Node, Optional
from rclpy.executors import Future, MultiThreadedExecutor

from smarc_action_base.gentler_action_server import GentlerActionServer
from z1_pro_msgs.msg import CamCmd
from z1_pro_msgs.msg import Topics

class GimbalActionServer:
    def __init__(self, node: Node):
        self._node = node

        node.declare_parameter("cmd_topic", Topics.CMD_TOPIC)
        self._cmd_topic : str = node.get_parameter("cmd_topic").get_parameter_value().string_value

        self._publisher = node.create_publisher(CamCmd, self._cmd_topic, 10)

        self._as = GentlerActionServer(
            self._node,
            "gimbal_action_server",
            self._on_goal_received,
            lambda: True,
            lambda: None,
            lambda: True,
            lambda: "No feedback",
            loop_frequency = 10.0
        )

        node.get_logger().info(f"GimbalActionServer initialized, publishing to {self._cmd_topic}")

    def _on_goal_received(self, goal_request: dict) -> bool:
        try:
            cmd_msg = CamCmd()
            cmd_msg.pitch = float(goal_request["pitch"])
            cmd_msg.yaw = float(goal_request["yaw"])
            cmd_msg.roll = float(goal_request["roll"])
            self._publisher.publish(cmd_msg)
            self._node.get_logger().info(f"Received goal, published CamCmd: {cmd_msg}")
            return True
        except KeyError as e:
            self._node.get_logger().error(f"Missing key in goal request: {e}")
            return False
        except ValueError as e:
            self._node.get_logger().error(f"Invalid value in goal request: {e}")
            return False

def main():
    rclpy.init()
    
    node = Node("gimbal_action_server_node")
    action_server = GimbalActionServer(node)
    
    executor = MultiThreadedExecutor()
    rclpy.spin(node, executor=executor)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()