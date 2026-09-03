#!/usr/bin/env python3
"""Command-line client for creating a delivery request."""

import sys

import rclpy
from rclpy.node import Node

from campus_delivery_bot.srv import DeliveryTask


class DeliveryClient(Node):
    def __init__(self) -> None:
        super().__init__("delivery_client")
        self.client = self.create_client(DeliveryTask, "delivery/request")

    def request_delivery(self, pickup: str, destination: str) -> None:
        if not self.client.wait_for_service(timeout_sec=10.0):
            self.get_logger().error("delivery/request service is not available.")
            return
        request = DeliveryTask.Request()
        request.pickup = pickup
        request.destination = destination
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        self.get_logger().info(f"accepted={response.accepted} message='{response.message}'")


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DeliveryClient()
    try:
        if len(sys.argv) != 3:
            node.get_logger().error("Usage: ros2 run campus_delivery_bot delivery_client.py PICKUP DESTINATION")
            return
        node.request_delivery(sys.argv[1], sys.argv[2])
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
