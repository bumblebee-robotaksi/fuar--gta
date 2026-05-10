#!/usr/bin/env python
"""
drive_mode_toggle.py

Toggles the taxi between MANUAL and AUTO drive mode by
switching the topic_tools/mux input topic.

Services exposed:
  /set_drive_mode  (std_srvs/SetBool)
    request.data = True  → AUTO  mode (/nav/cmd_vel)
    request.data = False → MANUAL mode (/teleop/cmd_vel)

Topics published:
  /drive_mode (std_msgs/String) → "manual" or "auto"
"""

import rospy
from std_srvs.srv import SetBool, SetBoolResponse
from std_msgs.msg import String
from topic_tools.srv import MuxSelect


class DriveModeToggle:
    def __init__(self):
        rospy.init_node("drive_mode_toggle")

        self.mode = rospy.get_param("~initial_mode", "manual")

        # Publisher so other nodes / UI can see current mode
        self.mode_pub = rospy.Publisher("/drive_mode", String, queue_size=1, latch=True)

        # Wait for mux select service
        rospy.loginfo("[DriveModeToggle] Waiting for drive_mux/select...")
        rospy.wait_for_service("/drive_mux/select")
        self.mux_select = rospy.ServiceProxy("/drive_mux/select", MuxSelect)

        # Service to switch mode
        rospy.Service("/set_drive_mode", SetBool, self.handle_set_mode)

        # Apply initial mode
        self._apply_mode(self.mode)
        rospy.loginfo("[DriveModeToggle] Ready. Initial mode: %s", self.mode)

    def handle_set_mode(self, req):
        new_mode = "auto" if req.data else "manual"
        self._apply_mode(new_mode)
        return SetBoolResponse(
            success=True,
            message="Switched to {} mode".format(new_mode)
        )

    def _apply_mode(self, mode):
        topic = "/nav/cmd_vel" if mode == "auto" else "/teleop/cmd_vel"
        try:
            self.mux_select(topic)
            self.mode = mode
            self.mode_pub.publish(String(data=mode))
            rospy.loginfo("[DriveModeToggle] Switched to %s mode → %s", mode, topic)
        except rospy.ServiceException as e:
            rospy.logerr("[DriveModeToggle] Failed to switch mux: %s", e)

    def spin(self):
        rospy.spin()


if __name__ == "__main__":
    DriveModeToggle().spin()