__author__ = 'Varun S S'

import math

class Atmospheric_param:
    # Constants
    RHO_SL = 1.2252139  # kg/m3
    P_ISA = 101325      # Pa
    T_ISA = 288.15      # K
    GAMMA_AIR = 1.401   # ratio
    SIGMA = 1           # ratio

    R = 8.31447     # J/mol.K
    g = 9.80665     # m/s2
    M_air = 28.97   # g/mol

    # Temperature Lapse Rates for ISA
    TROP_LAPSE = -0.0065    # K/m Upto 11km
    STRAT_LAPSE1 = 0.001    # K/m for 20km - 32km
    STRAT_LAPSE2 = 0.0028   # K/m for 32km - 47km
    STRAT_PAUSE = 0         # K/m or 47km - 51km
    MESO_LAPSE1 = -0.0028   # K/m for 51km - 71km
    MESO_LAPSE2 = -0.002    # K/m for 71km to 81.852km

    @staticmethod
    def temp(alt):
        if alt <= 11000:
            return Atmospheric_param.T_ISA + Atmospheric_param.TROP_LAPSE^alt
        elif alt <=20000:
            return Atmospheric_param.T_ISA + Atmospheric_param.TROP_LAPSE*11000
        else:
            return 0
    def pres(self,alt):
        return (Atmospheric_param.P_ISA*math.pow((self.temp(alt)/self.T_ISA),(self.g*self.M_air/(self.R*self.TROP_LAPSE*1000))))

    def rho(self,alt):
        return (self.pres(alt)*self.M_air/(self.R*self.temp(alt)))

    def speed_sound(self,alt):
        return (math.sqrt(self.GAMMA_AIR*self.R*self.temp(alt)))

class Historic_param:
    # Constants from historic data

    # Design Parameters
    MAX_T_BY_C_POS = 0.3    # ratio  -- For subsonic aircraft
    VT_COEFF = 0.06         # vertical tail volume coefficient
    HT_COEFF = 0.7          # horizontal tail volume coefficient
    C_POW_CRUISE = 0.085    # mg/Ws  --> Value for a flying boat
    C_POW_LOITER = 0.101    # mg/Ws  --> Value for a flying boat
    L_BY_D_MAX = 16.3       # ratio --> For flying boats
    CD0 = 0.03              # number --> Skin friction coefficient for flying boat
    RFF = 0.1               # number --> Reserve Fuel Fraction
    PROP_EFF = 0.85         # % --> Efficiency of turboprops
    TP_CRUISE = 550         # km/h

    CRUISE_MAX = 0.866      # ratio --> Ratio between cruise & max L/D Ratio for Turboprop

    # Weight parameters
    WEIGHT_A = 1.05
    WEIGHT_C = -0.05
    WEIGHT_K = 1
    TAKEOFF_WF = 0.97
    CLIMB_WF = 0.985
    DESCENT_WF = 1
    LANDING_WF = 0.995

    # Performance Parameters
    # ______________*_________________
    CLIMB_STALL = 1.3   # Relation between climb velocity and stall speed

    # Safety Parameters
    LAND_FRACT = 1.67

    # Fuselage Parameters
    # ______________*_________________

    NOSE_LENGTH_2_DIA = 2.5     # ratio
    NOSE_OFFSET = 2.8           # m
    TAIL_LENGTH_2_DIA = 2.4     # ratio
    TAIL_OFFSET_2_DIA = 1.2     # ratio

    FUSELAGE_THICKNESS = 0.091  # m
    AISLE_WIDTH = 0.508         # m
    AISLE_HEIGHT = 1.93         # m
    SEAT_PITCH = 0.81           # m

    # Seat Parameters
    SEAT_WIDTH = 0.51           # m
    SEAT_LENGTH = 0.64          # m
    SEAT_HEIGHT = 1             # m

    # Lavatory Parameters
    LAVATORY_LENGTH = 1         # m
    LAVATORY_WIDTH = 1          # m

    # Galley Parameters
    GALLEY_LENGTH = 1           # m
    GALLEY_WIDTH = 1            # m

    # Passenger parameters
    PILOT_WEIGHT = 86           # kg
    CABIN_CREW_WEIGHT = 86      # kg
    PASS_WEIGHT = 86            # kg
    CREW_BAG_WEIGHT = 14        # kg
    PASS_BAG_WEIGHT = 14        # kg
    # =============================================XX================================

class Regulations:
    # Climb Gradients
    def SSCG(self,n):
        if n >= 4:
            return 0.030
        elif n == 3:
            return 0.027
        else:
            return 0.024

    def MAG(self,n):
        if n >= 4:
            return 0.027
        elif n == 3:
            return 0.024
        else:
            return 0.021

class Conversion:
    LB_2_KG = 0.4536

    M_2_FT = 3.28084
    KM_2_MI = 0.62137
    KM_2_NM = 0.539957
    KM_2_M = 1000

    MPERS_2_FTPERMIN = M_2_FT*60
    DEG_2_RAD = math.pi/180
    HR_2_MIN = 60

