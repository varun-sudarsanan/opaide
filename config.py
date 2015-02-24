__author__ = 'Varun S S'
import data
import math


class Airfoil:
    def __init__(self):
        self.cruise_cl =1
        self.max_cl = 2


class Aircraft:
    def __init__(self):
        self.gross_weight = 0.0
        self.oew = 0.0
        self.t_by_w = 0.0
        self.w_by_s = 0.0

        self.rff = data.Historic_param.RFF
        c_pow_cruise = data.Historic_param.C_POW_CRUISE
        c_pow_loiter = data.Historic_param.C_POW_LOITER
        self.c_jet_cruise = (c_pow_cruise*data.Historic_param.TP_CRUISE*5)/(data.Historic_param.PROP_EFF*18)
        self.c_jet_loiter = (c_pow_loiter*data.Historic_param.TP_CRUISE*5)/(data.Historic_param.PROP_EFF*18)

        self.v_stall = 25.2
        self.v_cruise = data.Historic_param.TP_CRUISE*5/18
        self.v_climb = data.Historic_param.CLIMB_STALL*self.v_stall

        self.l_by_d_cruise = data.Historic_param.CRUISE_MAX*data.Historic_param.L_BY_D_MAX
        self.l_by_d_loiter = data.Historic_param.L_BY_D_MAX
        self.cd0 = data.Historic_param.CD0
        self.cl_max = 2.97

        self.pass_n = 0

        # Defining parts of the aircraft
        self.wing = Aircraft.Wing()
        self.fuse = Aircraft.Fuselage()
        self.stab = Aircraft.Stabilizer(self.fuse, self.wing)
        self.prop = Aircraft.PowerPlant()

    class Cabin:
        def __init__(self):
            self.length = 12.56
            self.seats = 24
            self.aisle_num = 1
            self.lavatory = 1
            self.galley = 1
            self.width = 2.11
            self.height = 2.61

    class Wing:
        """Class for defining the wing configuration"""

        def __init__(self):
            self.a_r = 7    # Aspect Ratio = Span/Mean chord
            self.t_r = 0.5  # Taper Ratio = Tip Chord/Root Chord
            self.sweep = 0  # Sweep angle at chord position with maximum t/c
            self.ref_area = 81.03   # m2

            self.span = math.sqrt(self.a_r*self.ref_area)   # Span of the wing planform
            self.root_chord = 2*self.ref_area/(self.span*(1+self.t_r))
            self.tip_chord = self.root_chord*self.t_r
            self.mean_chord = (self.tip_chord+self.root_chord)/2
            self.sweep_le = math.atan((math.tan(self.sweep)*self.a_r + 4*data.Historic_param.MAX_T_BY_C_POS*(1-self.t_r)/(1+self.t_r))/self.a_r)
            self.e = 2/(2-self.a_r+math.sqrt(4+math.pow(self.a_r,2)*(1+math.pow(math.tan(self.sweep),2))))

            self.root_airfoil = Airfoil()
            self.tip_airfoil = Airfoil()


    class Fuselage:
        def __init__(self):
            self.cabin = Aircraft.Cabin()
            self.pilots = 2
            self.attendants = 1
            self.nose_length = data.Historic_param.NOSE_LENGTH_2_DIA*(self.cabin.width+self.cabin.height)/2
            self.tail_length = data.Historic_param.TAIL_LENGTH_2_DIA*(self.cabin.width+self.cabin.height)/2
            self.length = self.cabin.length+self.nose_length+self.tail_length

    class Stabilizer:
        def __init__(self,fuse,wing):
            self.config = 1
            self.vt_num = 1
            self.arm_length = fuse.cabin.length/2 + fuse.tail_length

            self.ht = Aircraft.Wing()
            self.ht.a_r = 4
            self.ht.t_r = 0.5
            self.ht_ref_area = data.Historic_param.HT_COEFF*wing.mean_chord*wing.ref_area/self.arm_length

            self.vt = Aircraft.Wing()
            self.vt.a_r = 1.5
            self.vt.t_r = 0.4
            self.ht_ref_area = data.Historic_param.VT_COEFF*wing.span*wing.ref_area/self.arm_length

    class PowerPlant:
        def __init__(self):
            self.engines_num = 2

    def update_config(self):
        print "update_config"
        if self.pass_n > 9:
            self.engines_num = 2

