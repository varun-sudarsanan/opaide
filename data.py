__author__ = 'Varun S S'
import math

class Atmospheric_param:
    # Constants
    RHO_SL = 1.2252139  # kg/m3
    P_ISA = 101.325     # KPa
    T_ISA = 288.15      # K
    GAMMA_AIR = 1.401   # ratio

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
            return Atmospheric_param.T_ISA + Atmospheric_param.TROP_LAPSE*alt
        elif alt <=20000:
            return Atmospheric_param.T_ISA + Atmospheric_param.TROP_LAPSE*11000
        else:
            return 0
    @staticmethod
    def pres(alt):
        return (Atmospheric_param.P_ISA*math.pow((Atmospheric_param.temp(alt)/Atmospheric_param.T_ISA),(Atmospheric_param.g*Atmospheric_param.M_air/(Atmospheric_param.R*Atmospheric_param.TROP_LAPSE*1000))))

    @staticmethod
    def rho(alt,temp):
        t = Atmospheric_param.temp(alt)+temp
        return (Atmospheric_param.pres(alt)*Atmospheric_param.M_air/(Atmospheric_param.R*t))

    @staticmethod
    def speed_sound(alt):
        return (math.sqrt(Atmospheric_param.GAMMA_AIR*Atmospheric_param.R*Atmospheric_param.temp(alt)))

    @staticmethod
    def sigma(alt):
        return (Atmospheric_param.rho(alt)/Atmospheric_param.RHO_SL)

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

    class Fuselage:
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

        def cargo_containers(type,index):
            if type == "LD1":
                dimensions = [1.56,2.44,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD11":
                dimensions = [3.18,3.28,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD2":
                dimensions = [1.19,1.66,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD26":
                dimensions = [3.18,4.16,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD29":
                dimensions = [3.18,4.82,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD3":
                dimensions = [1.56,2.11,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD3-45":
                dimensions = [1.56,2.11,1.19] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD3-45(Rect)":
                dimensions = [1.56,1.66,1.19] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD3-45W":
                dimensions = [1.43,2.53,1.14] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD39":
                dimensions = [3.18,4.82,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD4":
                dimensions = [2.44,2.54,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD6":
                dimensions = [3.18,4.16,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD7":
                dimensions = [3.18,4.16,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD7(Rect)":
                dimensions = [3.18,3.28,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD8":
                dimensions = [2.44,3.28,1.68] # [bottom width, top width, height]
                return dimensions[index]
            elif type == "LD9":
                dimensions = [3.18,3.28,1.68] # [bottom width, top width, height]
                return dimensions[index]
            else:
                dimensions = [0,0,0] # [bottom width, top width, height]
                return dimensions[index]


        # =============================================XX================================

class Regulations:
    # Climb Gradients
    @staticmethod
    def SSCG(reg,n):
        if reg == "FAR 25":
            if n >= 4:
                return 0.030
            elif n == 3:
                return 0.027
            else:
                return 0.024
        elif reg == "FAR 23":
            if n >= 4:
                return 0.026
            elif n == 3:
                return 0.023
            else:
                return 0.020


    @staticmethod
    def MAG(reg,n):
        if reg == "FAR 25" or reg == "FAR 23":
            if n >= 4:
                return 0.027
            elif n == 3:
                return 0.024
            else:
                return 0.021

class Conversion:
    LB_2_KG = 0.4536

    M_2_FT = 3.28084
    M_2_IN = 39.3701
    KM_2_MI = 0.62137
    KM_2_NM = 0.539957
    KM_2_M = 1000

    DEG_2_RAD = math.pi/180
    HR_2_MIN = 60

    MPERS_2_FTPERMIN = M_2_FT*60

    LBFT2_2_KGM2 = LB_2_KG*math.pow(M_2_FT,2)