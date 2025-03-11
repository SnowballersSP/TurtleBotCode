#!/bin/bash

# Start SLAM Toolbox
ros2 launch turtlebot4_navigation slam_toolbox.launch.py &

# Give it time to start
sleep 5

# Start autonomous exploration
ros2 run explore_lite explore &

# Run for 5 minutes (adjust as needed)
sleep 300

# Save the map
ros2 run nav2_map_server map_saver_cli -f ~/my_driveway_map

echo "Mapping complete. Map saved as my_driveway_map.yaml"

# Build it using chmod +x map_driveway.sh
# Run it with ./map_driveway.sh