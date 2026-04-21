#!/usr/bin/env python3

from enum import Enum

import rclpy
from rclpy.node import Node, Optional
from rclpy.executors import Future, MultiThreadedExecutor

from geographic_msgs.msg import GeoPoint
from geometry_msgs.msg import Vector3

from smarc_action_base.gentler_action_server import GentlerActionServer
from z1_pro_msgs.msg import Topics as Z1Topics
from z1_pro_msgs.msg import GimbalFeedback




class GimbalActionServer:
    def __init__(self, node: Node):
        self._node = node


        node.declare_parameter("rpy_pub_hz", 10.0)
        self._rpy_pub_hz : float = node.get_parameter("rpy_pub_hz").get_parameter_value().double_value

        self.desired_rpy : Vector3 = Vector3()
        self._rpy_publisher = node.create_publisher(Vector3, Z1Topics.GIMBAL_CMD_TOPIC, 10)

        self.feedback : GimbalFeedback = GimbalFeedback()
        self.tracking_mode : str = GimbalFeedback.GIMBAL_MODE_OFF



        self._rpy_as = GentlerActionServer(
            self._node,
            "gimbal_set_rpy",
            self._on_goal_received_rpy,
            lambda: True,
            lambda: None,
            lambda: True,
            lambda: "No feedback",
            loop_frequency = 1.0
        )

        # TODO: When implemented, these will set the desired_rpy and tracking_mode, and all will be well.
        self._geopoint_as = GentlerActionServer(
            self._node,
            "gimbal_set_geopoint",
            lambda goal_request: self._node.get_logger().warn("Geopoint action not implemented yet") and False,
            lambda: True,
            lambda: None,
            lambda: True,
            lambda: "No feedback",
            loop_frequency = 1.0
        )

        self._track_img_poi_as = GentlerActionServer(
            self._node,
            "gimbal_track_img_poi",
            lambda goal_request: self._node.get_logger().warn("Image POI tracking action not implemented yet") and False,
            lambda: True,
            lambda: None,
            lambda: True,
            lambda: "No feedback",
            loop_frequency = 1.0
        )

        self._track_odom_poi_as = GentlerActionServer(
            self._node,
            "gimbal_track_odom_poi",
            lambda goal_request: self._node.get_logger().warn("Odom POI tracking action not implemented yet") and False,
            lambda: True,
            lambda: None,
            lambda: True,
            lambda: "No feedback",
            loop_frequency = 1.0
        )

        self._stop_as = GentlerActionServer(
            self._node,
            "gimbal_stop",
            self._on_goal_received_stop,
            lambda: True,
            lambda: None,
            lambda: True,
            lambda: "No feedback",
            loop_frequency = 1.0
        )

        timer = node.create_timer(1.0 / self._rpy_pub_hz, self.publish_rpy)

        self.log(f"GimbalActionServer initialized.")



    def publish_rpy(self):
        self.feedback.gimbal_mode = self.tracking_mode
        if self.tracking_mode == GimbalFeedback.GIMBAL_MODE_OFF:
            self.log("Gimbal is off, not publishing RPY commands.")
            return
        self._rpy_publisher.publish(self.desired_rpy)
        self.log(f"Published desired RPY: {self.desired_rpy}")


    def log(self, msg:str):
        self._node.get_logger().info(msg)


    def _on_goal_received_stop(self, goal_request: dict) -> bool:
        self.log(f"Received stop goal")
        self.tracking_mode = GimbalFeedback.GIMBAL_MODE_OFF
        return True


    def _on_goal_received_rpy(self, goal_request: dict) -> bool:
        """
        float64 roll  # [deg]
        float64 pitch # [deg]
        float64 yaw   # [deg]
        """
        self.log(f"Received RPY goal: {goal_request}")
        try:
            self.desired_rpy.x = float(goal_request["roll"])
            self.desired_rpy.y = float(goal_request["pitch"])
            self.desired_rpy.z = float(goal_request["yaw"])
            self.tracking_mode = GimbalFeedback.GIMBAL_MODE_RPY
            return True
        except KeyError as e:
            self.log("Missing key in goal request")
            return False
        except ValueError as e:
            self.log("Invalid value in goal request")
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