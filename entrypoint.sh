#!/bin/bash
set -e

# Source ROS and our workspace
source /opt/ros/melodic/setup.bash
source /taxi_ws/devel/setup.bash

# Software rendering fallback (for non-NVIDIA machines)
export LIBGL_ALWAYS_SOFTWARE=${LIBGL_ALWAYS_SOFTWARE:-0}
export GAZEBO_MODEL_PATH=/taxi_ws/src/aws-robomaker-racetrack-world/models:$GAZEBO_MODEL_PATH

# Launch whatever was passed as CMD, default to the taxi sim
exec "$@"