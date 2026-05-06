#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# fair_robot workspace scaffold
# Kullanım: bash setup_workspace.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

WORKSPACE_ROOT="$(pwd)"
SRC="${WORKSPACE_ROOT}/src"

echo "════════════════════════════════════════════════"
echo " fair_robot workspace kuruluyor..."
echo " Konum: ${WORKSPACE_ROOT}"
echo "════════════════════════════════════════════════"

# ── 0. Temel dizinler ─────────────────────────────────────────────────────
mkdir -p "${SRC}"
mkdir -p "${WORKSPACE_ROOT}/docker"

# ── 1. ros2 pkg create ile paketleri oluştur ─────────────────────────────
cd "${SRC}"

# Sıla
ros2 pkg create fair_robot_description \
    --build-type ament_cmake \
    --dependencies urdf xacro robot_state_publisher

ros2 pkg create fair_robot_gazebo \
    --build-type ament_cmake \
    --dependencies gazebo_ros gazebo_plugins

ros2 pkg create fair_robot_bringup \
    --build-type ament_cmake \
    --dependencies \
        fair_robot_description \
        fair_robot_gazebo

ros2 pkg create fair_robot_teleop \
    --build-type ament_cmake \
    --dependencies rclpy geometry_msgs teleop_twist_keyboard

# Umut
ros2 pkg create fair_robot_state_machine \
    --build-type ament_cmake \
    --dependencies rclpy std_msgs std_srvs geometry_msgs

# Murat
ros2 pkg create fair_robot_planning \
    --build-type ament_cmake \
    --dependencies rclpy nav_msgs geometry_msgs nav2_msgs

# Beril & Betül
ros2 pkg create fair_robot_perception \
    --build-type ament_cmake \
    --dependencies rclpy sensor_msgs vision_msgs cv_bridge image_transport

# Meryem
ros2 pkg create fair_robot_control \
    --build-type ament_cmake \
    --dependencies rclpy geometry_msgs nav_msgs

echo ""
echo "✔ Paketler oluşturuldu."

# ── 2. Her pakette gerekli alt klasörleri oluştur ─────────────────────────

# description
mkdir -p "${SRC}/fair_robot_description/urdf"
mkdir -p "${SRC}/fair_robot_description/meshes"
mkdir -p "${SRC}/fair_robot_description/rviz"
touch    "${SRC}/fair_robot_description/meshes/.gitkeep"

# gazebo
mkdir -p "${SRC}/fair_robot_gazebo/worlds"
mkdir -p "${SRC}/fair_robot_gazebo/models"
mkdir -p "${SRC}/fair_robot_gazebo/launch"

# bringup
mkdir -p "${SRC}/fair_robot_bringup/launch"
mkdir -p "${SRC}/fair_robot_bringup/rviz"
mkdir -p "${SRC}/fair_robot_bringup/config"

# teleop
mkdir -p "${SRC}/fair_robot_teleop/launch"
mkdir -p "${SRC}/fair_robot_teleop/fair_robot_teleop"
touch    "${SRC}/fair_robot_teleop/fair_robot_teleop/__init__.py"

# state machine (Umut)
mkdir -p "${SRC}/fair_robot_state_machine/launch"
mkdir -p "${SRC}/fair_robot_state_machine/fair_robot_state_machine"
touch    "${SRC}/fair_robot_state_machine/fair_robot_state_machine/__init__.py"

# planning (Murat)
mkdir -p "${SRC}/fair_robot_planning/launch"
mkdir -p "${SRC}/fair_robot_planning/config"
mkdir -p "${SRC}/fair_robot_planning/fair_robot_planning"
touch    "${SRC}/fair_robot_planning/fair_robot_planning/__init__.py"

# perception (Beril & Betül)
mkdir -p "${SRC}/fair_robot_perception/launch"
mkdir -p "${SRC}/fair_robot_perception/config"
mkdir -p "${SRC}/fair_robot_perception/fair_robot_perception"
touch    "${SRC}/fair_robot_perception/fair_robot_perception/__init__.py"

# control (Meryem)
mkdir -p "${SRC}/fair_robot_control/launch"
mkdir -p "${SRC}/fair_robot_control/config"
mkdir -p "${SRC}/fair_robot_control/fair_robot_control"
touch    "${SRC}/fair_robot_control/fair_robot_control/__init__.py"

echo "✔ Alt klasörler oluşturuldu."

# ── 3. .gitkeep ile boş klasörleri git'e ekle ────────────────────────────
find "${SRC}" -type d -empty -exec touch {}/.gitkeep \;

# ── 4. Kök .gitignore ─────────────────────────────────────────────────────
cat > "${WORKSPACE_ROOT}/.gitignore" << 'EOF'
build/
install/
log/
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
*.pt
*.onnx
*.engine
.vscode/
.DS_Store
EOF

echo "✔ .gitignore oluşturuldu."

# ── 5. Özet ───────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo " TAMAMLANDI — Workspace yapısı:"
echo "════════════════════════════════════════════════"
find "${SRC}" -maxdepth 2 -type d | sort | sed 's|'"${WORKSPACE_ROOT}/"'||'
echo ""
echo "Sonraki adım:"
echo "  cd ${WORKSPACE_ROOT}"
echo "  colcon build --symlink-install"
echo "════════════════════════════════════════════════"
