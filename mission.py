__author__ = 'Varun S S'
import math

class MissionPhase:
    def __init__(self):
        self.type = "takeoff"
        self.x_pos_start = 0.0
        self.x_pos_end = 0.0
        self.y_pos_start = 0.0
        self.y_pos_end  = 0.0
        self.range = 0.0
        self.height = 0.0
        self.time = 0.0
        self.wf = 1.0


class MissionDef:
    def __init__(self):
        self.name = "Mission 1"
        self.segments_num = 6
        self.segments = []
        self.fuel_fraction = 1.0
        self.h_obs = 15.24          # m
        self.app_ang = 9.0            # degree
        self.app_dist = self.h_obs*math.tan(self.app_ang*180/math.pi)
        self.define_mission(self.segments_num)

    def define_mission(self,num):
        self.segments_num = num
        for i in range(self.segments_num):
            self.segments.append(MissionPhase())

    def update_mission(self):
        for i in range(self.segments_num):
            se_now = self.segments[i]
            se_prev = self.segments[i-1]
            if i != 0:
                se_now.x_pos_start = se_prev.x_pos_end
                se_now.y_pos_start = se_prev.y_pos_end
            se_now.x_pos_end = se_now.x_pos_start + se_now.range
            se_now.y_pos_end = se_now.y_pos_start + se_now.height
            if i == 0:
                se_now.y_pos_start = se_now.y_pos_end


