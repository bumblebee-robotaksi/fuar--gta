#!/usr/bin/env python
# -*- coding: utf-8 -*-
# drive_mode_toggle.py
# Switches between manual and auto drive mode
#
# Services:
#   /set_drive_mode (std_srvs/SetBool)
#     True  -> AUTO  (/nav/cmd_vel)
#     False -> MANUAL (/teleop/cmd_vel)
#
# Topics published:
#   /drive_mode (std_msgs/String) -> "manual" or "auto"

import rospy
from std_srvs.srv import SetBool, SetBoolResponse
from std_msgs.msg import String
from topic_tools.srv import MuxSelect

class DriveModeToggle:
    def __init__(self):
        rospy.init_node('drive_mode_toggle')
        self.mode = rospy.get_param('~initial_mode', 'manual')

        self.mode_pub = rospy.Publisher(
            '/drive_mode', String, queue_size=1, latch=True)

        rospy.loginfo('[DriveModeToggle] Waiting for drive_mux/select...')
        try:
            rospy.wait_for_service('/drive_mux/select', timeout=10.0)
            self.mux_select = rospy.ServiceProxy('/drive_mux/select', MuxSelect)
            rospy.loginfo('[DriveModeToggle] Mux found!')
        except rospy.ROSException:
            rospy.logwarn('[DriveModeToggle] Mux not found, will retry on use')
            self.mux_select = None

        rospy.Service('/set_drive_mode', SetBool, self.handle_set_mode)
        self._apply_mode(self.mode)
        rospy.loginfo('[DriveModeToggle] Ready. Mode: %s', self.mode)

    def handle_set_mode(self, req):
        new_mode = 'auto' if req.data else 'manual'
        self._apply_mode(new_mode)
        return SetBoolResponse(success=True, message='Switched to ' + new_mode)

    def _apply_mode(self, mode):
        topic = '/nav/cmd_vel' if mode == 'auto' else '/teleop/cmd_vel'
        if self.mux_select is None:
            try:
                rospy.wait_for_service('/drive_mux/select', timeout=3.0)
                self.mux_select = rospy.ServiceProxy('/drive_mux/select', MuxSelect)
            except Exception as e:
                rospy.logerr('[DriveModeToggle] Could not reach mux: %s', e)
                return
        try:
            self.mux_select(topic)
            self.mode = mode
            self.mode_pub.publish(String(data=mode))
            rospy.loginfo('[DriveModeToggle] Switched to %s mode', mode)
        except rospy.ServiceException as e:
            rospy.logerr('[DriveModeToggle] Mux switch failed: %s', e)

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    DriveModeToggle().spin()