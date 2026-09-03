# Campus Mail / Item Delivery Bot

A ROS 2 Humble simulation project for autonomous mail/item delivery across a campus environment using Gazebo, Nav2, SLAM, and RViz.

## Project Preview

### Screenshot

![Campus delivery bot simulation screenshot](campus_delivery_ws/Screenshot%20from%202026-08-31%2021-05-35.png)

### Short Demo Video

[Watch the short demo video](campus_delivery_ws/Screencast%20from%2008-31-2026%2009%3A05%3A47%20PM.webm)

## What This Project Includes

- Simulated campus world with named delivery locations
- Differential-drive delivery robot with lidar and odometry
- Nav2 + SLAM toolbox for navigation and mapping
- Custom delivery request service (`DeliveryTask.srv`)
- Delivery dispatcher/client Python nodes for pickup → drop-off tasks

## Quick Start

Use the complete setup and run instructions here:

- [`campus_delivery_ws/README.md`](campus_delivery_ws/README.md)

## Main Workspace Layout

```text
campus_delivery_ws/
  src/campus_delivery_bot/
    launch/simulation.launch.py
    worlds/campus.world
    urdf/campus_delivery_bot.urdf
    srv/DeliveryTask.srv
    docs/project_report.md
```