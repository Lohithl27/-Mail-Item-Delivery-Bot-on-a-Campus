# Major Project 2: Mail / Item Delivery Bot On A Campus

## Introduction

This project simulates a campus delivery robot that transports mail or small parcels between common campus locations. The robot runs in ROS 2 Humble, uses Gazebo for the virtual campus, RViz for visualization, SLAM for map creation, and Nav2 for autonomous navigation.

## Objectives

- Implement autonomous delivery using the ROS 2 navigation stack.
- Build a campus-style Gazebo world with buildings, roads, and obstacles.
- Use ROS 2 topics, actions, and a custom service for delivery requests.
- Demonstrate a complete delivery cycle from dispatch to pickup to drop-off.

## Materials And Tools

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic
- RViz2
- Nav2
- slam_toolbox
- Python 3 and rclpy

## Methodology

The robot is modeled as a compact differential-drive delivery platform with a parcel box and a lidar sensor. Gazebo provides `/odom`, `/scan`, and `/cmd_vel` integration through ROS plugins. The simulated campus world contains named delivery locations: mail room, library, lab, admin block, hostel, and cafeteria.

The `DeliveryTask` service accepts a pickup and destination string. The `delivery_dispatcher.py` node validates the request, sends a Nav2 `NavigateToPose` goal to the pickup location, simulates parcel loading, then sends a second goal to the destination.

## Delivery Flow

```text
User request
  -> delivery/request service
  -> validate pickup and destination
  -> navigate to pickup
  -> publish parcel collected status
  -> navigate to destination
  -> publish parcel delivered status
```

## Campus Layout

```text
                 Cafeteria
                    |
        Lab ---- Mail Room ---- Library
                    |
                 Admin

          Hostel is southwest of the mail room. Delivery goals are placed at building entrances.
```

## Problem-Solving Approach

The project uses SLAM mode so a prebuilt map is not required for first execution. This makes the package easier to run on a fresh ROS 2 Humble install. The Nav2 configuration is tuned for a small differential-drive robot, moderate speed, and a lidar range suitable for a compact campus world.

## Testing And Results

Suggested test cases:

- `mail_room -> library`: verifies a short east/northeast route.
- `mail_room -> cafeteria`: verifies north route completion.
- `cafeteria -> hostel`: verifies longer route planning after the map has expanded.
- Unknown location request: verifies service validation.

Expected result: the robot accepts a valid delivery request, reaches pickup, publishes pickup status, reaches destination, and publishes delivery completion.

## Conclusion

The project demonstrates the core software pattern for a smart-campus delivery robot: environment modeling, robot simulation, localization/mapping, autonomous navigation, and delivery task orchestration. It can be extended with QR-code parcel IDs, battery monitoring, multi-stop delivery queues, dynamic obstacles, or a physical robot base.
