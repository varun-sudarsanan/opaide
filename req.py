__author__ = 'Varun S S'
import data
import math

class AircraftRequirements:
    # Performance Requirements

    def __init__(self):
        self.v_stall_max = 25.722    # m/s

        # v_cruise =
        self.roc = 8.5   # m/s
        self.roc_isa_t = 0 # degree C
        self.service_ceil = 7500  #m

        self.design_range = 2500.0    # km
        self.cruise_mach = 0.55  # Mach No
        self.max_run_alt = 3000  # m

        self.run_msl_isa_t = 0      # degree C
        self.run_alt_isa_t = 0      # degree C

        self.loiter_time = 0.5   # hr

        self.pass_num = 20
        self.cargo_wt = 200.0
        self.pilots_n = 2

        self.to_distance_land = 0.0
        self.to_distance_water = 0.0

        self.la_distance_land = 0.0
        self.la_distance_water = 0.0

        self.attend_n = self.attend_num(self.pass_num)
        self.payload_wt = 2200        # kg
        self.crew_wt = 300.0            # kg
        self.fuel_res_rang = 100        # km
        self.des_rang_payload = 1000    # kg

        self.inst_turn = 0.0  # deg/s
        self.sus_turn = 0.0   # deg/s
        self.bank_ang = 0.0   # deg


        self.regulation = "FAR 23"
        self.constraints = []

        self.h_obs = 15.24          # m
        self.app_ang = 9.0            # degree
        self.app_dist = self.h_obs*math.tan(self.app_ang*180/math.pi)


    def attend_num(self,pas):
        return (pas-1)/30 + 1

    def update_req(self,a):
        self.attend_n = self.attend_num(a.pass_n)
