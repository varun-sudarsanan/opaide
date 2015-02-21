__author__ = 'Varun S S'
import data

class AircraftRequirements:
    # Performance Requirements

    def __init__(self):
        self.v_stall_max = 25.722    # m/s

        # v_cruise =
        self.roc = 8.5   # m/s
        self.design_range = 2500.0    # km
        self.loiter_time = 0.5   # hr

        self.min_pass = 20
        self.max_pass = 30
        self.cargo_wt = 200.0
        self.pilots_n = 2

        self.to_distance = 0.0
        self.la_distance = 0.0
        self.attend_n = self.attend_num(self.max_pass)
        self.payload_wt = 2600.0
        self.crew_wt = 300.0

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
