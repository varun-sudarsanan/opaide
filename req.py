__author__ = 'Varun S S'
import data

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

        self.loiter_time = 0.5   # hr

        self.min_pass = 20
        self.max_pass = 30
        self.cargo_wt = 200.0
        self.pilots_n = 2

        self.to_distance = 0.0
        self.la_distance = 0.0
        self.attend_n = self.attend_num(self.max_pass)
        self.payload_wt = 2600.0        # kg
        self.crew_wt = 300.0            # kg
        self.fuel_res_rang = 100        # km
        self.des_rang_payload = 1000    # kg

        self.inst_turn = 0  # deg/s
        self.sus_turn = 0   # deg/s
        self.bank_ang = 0   # deg


        self.regulation = 23

    def attend_num(self,pas):
        return (pas-1)/30 + 1

    def update_req(self,a):
        self.attend_n = self.attend_num(a.pass_n)

    # Determined values

    # def climb_constr(t_by_w):
    # "Function to determine wing-loading constraint imposed by thrust to weight ratio"
    #
    # climb_grad = roc/v_climb
