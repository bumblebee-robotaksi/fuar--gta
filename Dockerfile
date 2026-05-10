FROM ubuntu:18.04

# ─────────────────────────────────────────────
# 1. Basic deps + ROS Melodic + Gazebo 9
# ─────────────────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=melodic

RUN apt-get update && apt-get install -y \
    curl gnupg2 lsb-release \
    && rm -rf /var/lib/apt/lists/*

# ROS repo
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros/ubuntu $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/ros.list

# Gazebo repo
RUN curl -sSL http://packages.osrfoundation.org/gazebo.key | apt-key add - && \
    echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/gazebo-stable.list

RUN apt-get update && apt-get install -y \
    # ROS Melodic desktop (includes rviz, rqt, etc.)
    ros-melodic-desktop-full \
    # Gazebo 9
    gazebo9 \
    libgazebo9-dev \
    ros-melodic-gazebo-ros-pkgs \
    ros-melodic-gazebo-ros-control \
    # Build tools
    python-catkin-tools \
    python-rosdep \
    python-rosinstall \
    python-rosinstall-generator \
    python-wstool \
    build-essential \
    # car_demo specific deps
    ros-melodic-robot-state-publisher \
    ros-melodic-joint-state-publisher \
    ros-melodic-joy \
    ros-melodic-teleop-twist-keyboard \
    ros-melodic-topic-tools \
    # Display (software fallback, works without NVIDIA)
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────
# 2. rosdep init
# ─────────────────────────────────────────────
RUN rosdep init && rosdep update

# ─────────────────────────────────────────────
# 3. Copy workspace into container
# ─────────────────────────────────────────────
WORKDIR /taxi_ws
COPY src/ src/

# ─────────────────────────────────────────────
# 4. Install deps and build
# ─────────────────────────────────────────────
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && \
    rosdep install --from-paths src --ignore-src -r -y && \
    catkin_make"

# ─────────────────────────────────────────────
# 5. Entrypoint — source everything, launch sim
# ─────────────────────────────────────────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
