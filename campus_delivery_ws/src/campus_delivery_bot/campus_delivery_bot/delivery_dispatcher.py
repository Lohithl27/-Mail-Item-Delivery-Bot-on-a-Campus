#!/usr/bin/env python3
"""Dispatch campus delivery tasks through Nav2 NavigateToPose goals."""

import math
from typing import Dict, Tuple

import rclpy
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from campus_delivery_bot.srv import DeliveryTask


Location = Tuple[float, float, float]


class DeliveryDispatcher(Node):
    """Accepts pickup/drop-off service calls and sends the robot via Nav2."""

    def __init__(self) -> None:
        super().__init__("delivery_dispatcher")
        self.declare_parameter("locations", [
            "mail_room:-0.7,-1.0,0.0",
            "library:3.6,1.2,0.0",
            "lab:-2.8,2.5,1.57",
            "admin:2.0,-2.8,-1.57",
            "hostel:-3.8,-2.0,3.14",
            "cafeteria:0.0,3.6,0.0",
        ])
        self.locations = self._parse_locations(
            self.get_parameter("locations").get_parameter_value().string_array_value
        )
        self.status_pub = self.create_publisher(String, "delivery/status", 10)
        self.task_srv = self.create_service(DeliveryTask, "delivery/request", self.handle_request)
        self.nav_client = ActionClient(self, NavigateToPose, "navigate_to_pose")
        self.busy = False
        self.get_logger().info(
            "Delivery dispatcher ready. Known locations: "
            + ", ".join(sorted(self.locations.keys()))
        )

    def _parse_locations(self, raw_locations) -> Dict[str, Location]:
        locations: Dict[str, Location] = {}
        for raw in raw_locations:
            name, coords = raw.split(":", 1)
            x_str, y_str, yaw_str = coords.split(",", 2)
            locations[name.strip().lower()] = (float(x_str), float(y_str), float(yaw_str))
        return locations

    def handle_request(self, request, response):
        pickup = request.pickup.strip().lower()
        destination = request.destination.strip().lower()

        if self.busy:
            response.accepted = False
            response.message = "Robot is already handling a delivery task."
            return response
        if pickup not in self.locations or destination not in self.locations:
            response.accepted = False
            response.message = self._unknown_location_message(pickup, destination)
            return response
        if pickup == destination:
            response.accepted = False
            response.message = "Pickup and destination must be different campus locations."
            return response

        self.busy = True
        self._publish_status(f"Accepted delivery: pickup={pickup}, destination={destination}")
        self._send_nav_goal(pickup, "pickup", lambda: self._after_pickup(pickup, destination))
        response.accepted = True
        response.message = f"Delivery accepted from {pickup} to {destination}."
        return response

    def _after_pickup(self, pickup: str, destination: str) -> None:
        self._publish_status(f"Parcel collected at {pickup}")
        self.get_logger().info("Simulating parcel loading.")
        self.load_timer = self.create_timer(
            2.0,
            lambda: self._leave_pickup(destination),
        )

    def _leave_pickup(self, destination: str) -> None:
        self.destroy_timer(self.load_timer)
        self._send_nav_goal(destination, "drop_off", lambda: self._finish_delivery(destination))

    def _finish_delivery(self, destination: str) -> None:
        self._publish_status(f"Parcel delivered at {destination}")
        self.busy = False

    def _send_nav_goal(self, location_name: str, phase: str, on_success) -> None:
        if not self.nav_client.wait_for_server(timeout_sec=10.0):
            self._fail_delivery("Nav2 navigate_to_pose action server is not available.")
            return

        pose = self._pose_for(location_name)
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        self._publish_status(f"Navigating to {location_name} for {phase}")

        send_future = self.nav_client.send_goal_async(goal_msg, feedback_callback=self._feedback_cb)
        send_future.add_done_callback(lambda future: self._goal_response_cb(future, location_name, on_success))

    def _goal_response_cb(self, future, location_name: str, on_success) -> None:
        goal_handle = future.result()
        if not goal_handle.accepted:
            self._fail_delivery(f"Nav2 rejected goal for {location_name}.")
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(lambda result: self._goal_result_cb(result, location_name, on_success))

    def _goal_result_cb(self, future, location_name: str, on_success) -> None:
        result = future.result()
        if result.status != GoalStatus.STATUS_SUCCEEDED:
            self._fail_delivery(f"Navigation to {location_name} ended with status {result.status}.")
            return
        on_success()

    def _pose_for(self, location_name: str) -> PoseStamped:
        x, y, yaw = self.locations[location_name]
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        return pose

    def _feedback_cb(self, feedback_msg) -> None:
        remaining = feedback_msg.feedback.distance_remaining
        self.get_logger().info(f"Distance remaining: {remaining:.2f} m")

    def _unknown_location_message(self, pickup: str, destination: str) -> str:
        requested = [name for name in (pickup, destination) if name not in self.locations]
        known = ", ".join(sorted(self.locations.keys()))
        return f"Unknown location(s): {', '.join(requested)}. Known locations: {known}."

    def _fail_delivery(self, message: str) -> None:
        self.get_logger().error(message)
        self._publish_status(f"Delivery failed: {message}")
        self.busy = False

    def _publish_status(self, text: str) -> None:
        self.get_logger().info(text)
        self.status_pub.publish(String(data=text))


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DeliveryDispatcher()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
