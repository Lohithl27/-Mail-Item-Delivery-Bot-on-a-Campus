#!/usr/bin/env python3
"""Submit a ready-made demo task after Nav2 has time to activate."""

import rclpy
from rclpy.node import Node

from campus_delivery_bot.srv import DeliveryTask


class DemoDeliverySequence(Node):
    def __init__(self) -> None:
        super().__init__("demo_delivery_sequence")
        self.declare_parameter("pickup", "mail_room")
        self.declare_parameter("destination", "library")
        self.declare_parameter("startup_delay_sec", 15.0)
        self.client = self.create_client(DeliveryTask, "delivery/request")
        delay = self.get_parameter("startup_delay_sec").value
        self.timer = self.create_timer(delay, self.submit_once)

    def submit_once(self) -> None:
        self.timer.cancel()
        pickup = self.get_parameter("pickup").value
        destination = self.get_parameter("destination").value
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("delivery/request service is not available.")
            return
        request = DeliveryTask.Request()
        request.pickup = pickup
        request.destination = destination
        self.get_logger().info(f"Submitting demo delivery {pickup} -> {destination}")
        future = self.client.call_async(request)
        future.add_done_callback(self._done)

    def _done(self, future) -> None:
        response = future.result()
        self.get_logger().info(f"Demo request accepted={response.accepted}: {response.message}")


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DemoDeliverySequence()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
