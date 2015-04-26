__author__ = 'Varun S S'
import data
import math


class Airfoil:
    def __init__(self):
        self.name = "None"
        self.cruise_cl = 1
        self.cruise_cl_alpha = 0
        self.max_cl = 2
        self.max_cl_alpha = 15
        self.max_thickness = 0
        self.max_thick_loc = 0
        self.cd0 = 0
        self.max_clbycd = 0
        self.max_clbycd_alpha = 0

class Flap:
    def __init__(self):
        self.type = "None"
        self.flap_factor = 1
class Aircraft:
    def __init__(self):
        self.gross_weight = 0.0
        self.oew = 0.0
        self.t_by_w = 0.0
        self.w_by_s = 0.0
        self.cg_location = 0.0      # Distance from the nose

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
        self.cl_lo = 1.5

        self.pass_n = 0

        # Defining parts of the aircraft
        self.wing = Aircraft.Wing()
        self.fuse = Aircraft.Fuselage()
        self.stab = Aircraft.Stabilizer()
        self.prop = Aircraft.PowerPlant()
    class Container:
        def __init__(self):
            self.type = "None"
            self.width_bot = 0
            self.width_top = 0
            self.height = 0
            self.double = 0

    class Cabin:
        def __init__(self):
            self.type = "Passenger"
            self.class_num = 1
            self.avg_seats_abr = [0,0,0]
            self.aisle_num = [0,0,0]
            self.seat_pitch = [0.81,0.81,0.81]
            self.seats_num = [0,0,0]
            self.rows_num = [0,0,0]
            self.lav_num = [0,0,0]
            self.galley = [0,0,0]
            self.length = 12.56
            self.seats = 24
            self.cargo_length = 0
            self.cargo_width = 0
            self.cargo_height = 0

            self.cabin_h2w_ratio = 1.237
            self.floor_lowering = 0.88
            self.floor_thickness = 0
            self.inner_height = 2.61
            self.inner_width = self.inner_height/self.cabin_h2w_ratio
            self.inner_eq_dia = math.sqrt(self.inner_height*self.inner_width)
            self.update_fuse_thickness()

            self.outer_height = self.inner_height+2*self.fuselage_thickness
            self.outer_width = self.inner_width+2*self.fuselage_thickness
            self.outer_eq_dia = self.inner_eq_dia+2*self.fuselage_thickness

        def update_fuse_thickness(self):
            self.fuselage_thickness = (0.084 + 0.045*self.inner_eq_dia)/2

    class Wing(object):
        """Class for defining the wing configuration"""

        def __init__(self):
            self.a_r = 7            # Aspect Ratio = Span/Mean chord
            self.t_r = 0.5          # Taper Ratio = Tip Chord/Root Chord
            self.sweep_le = 0       # Sweep angle at chord position with maximum t/c
            self.ref_area = 81.03   # m2
            self.dihedral = 0       # deg
            self.dist_CG = 0        # m
            self.vert_dist_CG = 0   # m

            self.span = math.sqrt(self.a_r*self.ref_area)   # Span of the wing planform
            self.root_chord = 2*self.ref_area/(self.span*(1+self.t_r))
            self.tip_chord = self.root_chord*self.t_r
            self.mean_chord = (self.tip_chord+self.root_chord)/2
            self.sweep = math.atan((self.a_r*math.tan(self.sweep_le)-4*data.Historic_param.MAX_T_BY_C_POS*(1-self.t_r)/(1+self.t_r))/self.a_r)

            self.e = 2/(2-self.a_r+math.sqrt(4+math.pow(self.a_r,2)*(1+math.pow(math.tan(self.sweep),2))))

            self.root_airfoil = Airfoil()
            self.tip_airfoil = Airfoil()
            self.airfoil = Airfoil()
            self.flap = Flap()

        def calc_ref_area(self,a):
            if a.w_by_s!=0:
                self.ref_area = a.gross_weight/a.w_by_s
        def calc_span(self):
            self.span = math.sqrt(self.a_r*self.ref_area)   # Span of the wing planform
        def calc_chord(self):
            if self.span!=0:
                self.root_chord = 2*self.ref_area/(self.span*(1+self.t_r))
                self.tip_chord = self.root_chord*self.t_r
                self.mean_chord = (self.tip_chord+self.root_chord)/2
        def calc_sweep(self):
            if self.a_r!=0:
                self.sweep = math.atan((self.a_r*math.tan(self.sweep_le)-4*data.Historic_param.MAX_T_BY_C_POS*(1-self.t_r)/(1+self.t_r))/self.a_r)
        def calc_e(self):
            self.e = 2/(2-self.a_r+math.sqrt(4+math.pow(self.a_r,2)*(1+math.pow(math.tan(self.sweep),2))))

        def calc_area(self):
            if self.a_r!=0:
                self.ref_area = math.pow(self.span,2)/self.a_r

    class Fuselage:
        def __init__(self):
            self.cabin = Aircraft.Cabin()
            self.container = Aircraft.Container()
            self.pilots = 2
            self.attendants = 1
            self.nose_length2dia = data.Historic_param.Fuselage.NOSE_LENGTH_2_DIA
            self.nose_offset = data.Historic_param.Fuselage.NOSE_OFFSET
            self.tail_length2dia = data.Historic_param.Fuselage.TAIL_LENGTH_2_DIA
            self.tail_offset2dia = data.Historic_param.Fuselage.TAIL_OFFSET_2_DIA
            self.length = 0
            self.update_fuse_length()

        def update_fuse_length(self):
            self.nose_length = self.nose_length2dia*self.cabin.outer_eq_dia/2
            self.tail_length = self.tail_length2dia*self.cabin.outer_eq_dia/2
            self.tail_offset = self.tail_offset2dia*self.cabin.outer_eq_dia/2
            self.length = self.cabin.length + self.nose_length - self.nose_offset + self.tail_length - self.tail_offset

    class HorizontalTail(Wing):
        def __init__(self):
            Aircraft.Wing.__init__(self)
            self.a_r = 4
            self.t_r = 0.5
            self.long_dist_CG = 1.8
            self.ref_area = 17.41

    class VerticalTail(Wing):
        def __init__(self):
            Aircraft.Wing.__init__(self)
            self.a_r = 1.5
            self.t_r = 0.4
            self.ref_area = 9.07
            self.long_dist_CG = 1.8
            self.lat_dist_CG = 0
            self.fuse_symm = 0

    class Stabilizer:
        def __init__(self):
            self.config = 1
            self.vt_num = 0
            self.ht_num = 0
            self.horiz_vol_coeff = 0
            self.vert_vol_coeff = 0
            self.ht = [Aircraft.HorizontalTail()]
            self.ht[0].calc_span()
            self.ht[0].calc_chord()

            self.vt = [Aircraft.VerticalTail()]
            self.vt[0].calc_span()
            self.vt[0].calc_chord()

    class PowerPlant:
        def __init__(self):
            self.engines_num = 2

