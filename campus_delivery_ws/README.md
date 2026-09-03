# Campus Mail / Item Delivery Bot

ROS 2 Humble project for a simulated campus delivery robot. It includes a Gazebo campus world, a differential-drive delivery robot with lidar, Nav2/SLAM configuration, a custom delivery request service, and Python nodes that run a pickup-to-drop-off task.

## Tested Target

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic
- Nav2
- RViz2

## Complete Command List For Simulation

Use these commands in Ubuntu 22.04 with ROS 2 Humble.

### 1. Install Required Packages

```bash
sudo apt update
sudo apt install -y ros-humble-desktop ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins python3-colcon-common-extensions
```

### 2. Go To Workspace

```bash
cd ~/campus_delivery_ws
```

### 3. Source ROS 2 Humble

```bash
source /opt/ros/humble/setup.bash
```

### 4. Build The Project

```bash
colcon build --symlink-install
```

### 5. Source The Built Workspace

```bash
source install/setup.bash
```

### 6. Launch Gazebo, RViz, Nav2, SLAM, And Robot

```bash
ros2 launch campus_delivery_bot simulation.launch.py
```

This command launches the complete robot simulation.

### 7. Send A Delivery Request In A Second Terminal

Open a new terminal and run:

```bash
cd ~/campus_delivery_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run campus_delivery_bot delivery_client.py mail_room library
```

### 8. Watch Delivery Status In Another Terminal

```bash
cd ~/campus_delivery_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 topic echo /delivery/status
```

### 9. Launch Automatic Demo

Use this instead of step 6 if you want the robot to automatically start one delivery task:

```bash
ros2 launch campus_delivery_bot simulation.launch.py demo:=true
```

### 10. Try Other Delivery Routes

```bash
ros2 run campus_delivery_bot delivery_client.py mail_room admin
ros2 run campus_delivery_bot delivery_client.py cafeteria hostel
ros2 run campus_delivery_bot delivery_client.py mail_room cafeteria
```

### 11. Check ROS Topics

```bash
ros2 topic list
```

### 12. Check Available Services

```bash
ros2 service list
```

### 13. Call The Delivery Service Directly

```bash
ros2 service call /delivery/request campus_delivery_bot/srv/DeliveryTask "{pickup: mail_room, destination: library}"
```

### 14. Stop The Simulation

Press `Ctrl+C` in each terminal that is running ROS commands.

## Install Dependencies

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-gazebo-ros-pkgs \
  python3-colcon-common-extensions
```

## Build

```bash
cd ~/campus_delivery_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

If you use the folder directly from this deliverable, first copy or move `campus_delivery_ws` to your Ubuntu home directory.

## Run The Full Simulation

```bash
source /opt/ros/humble/setup.bash
cd ~/campus_delivery_ws
source install/setup.bash
ros2 launch campus_delivery_bot simulation.launch.py
```

Gazebo opens the campus world and RViz opens the robot/map view. Nav2 uses SLAM so the map is created from lidar while the robot moves.

## Send A Delivery Request

Open a second terminal:

```bash
source /opt/ros/humble/setup.bash
cd ~/campus_delivery_ws
source install/setup.bash
ros2 run campus_delivery_bot delivery_client.py mail_room library
```

Other available locations:

- `mail_room`
- `library`
- `lab`
- `admin`
- `hostel`
- `cafeteria`

Examples:

```bash
ros2 run campus_delivery_bot delivery_client.py mail_room admin
ros2 run campus_delivery_bot delivery_client.py cafeteria hostel
```

Watch status messages:

```bash
ros2 topic echo /delivery/status
```

## One-Command Demo

To automatically request a delivery after startup:

```bash
ros2 launch campus_delivery_bot simulation.launch.py demo:=true
```

## Project Structure

```text
campus_delivery_ws/
  src/campus_delivery_bot/
    campus_delivery_bot/
      delivery_dispatcher.py
      delivery_client.py
      demo_delivery_sequence.py
    srv/DeliveryTask.srv
    launch/simulation.launch.py
    worlds/campus.world
    urdf/campus_delivery_bot.urdf
    config/nav2_params.yaml
    config/slam_toolbox.yaml
    rviz/campus_delivery.rviz
    docs/project_report.md
```

## Notes For Evaluation

- Functionality: the custom `DeliveryTask` service accepts a pickup and destination, then sends two Nav2 `NavigateToPose` goals.
- Creativity: the world contains a campus mail room, library, engineering lab, admin block, hostel, cafeteria, roads, and an obstacle.
- Technical accuracy: the simulation uses ROS 2 topics, a custom service, Nav2 action client, Gazebo robot plugins, lidar, odometry, SLAM, and RViz.
- Documentation: see `src/campus_delivery_bot/docs/project_report.md`.

## Troubleshooting

If Nav2 does not move immediately, wait for SLAM and lifecycle nodes to finish activating. In RViz, confirm that `/scan`, `/map`, `/odom`, and TF are visible.

If Gazebo says a plugin is missing, install:

```bash
sudo apt install -y ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins
```

If the robot cannot reach a location, try a closer destination first so SLAM can build more of the map:

```bash
ros2 run campus_delivery_bot delivery_client.py mail_room cafeteria
```
