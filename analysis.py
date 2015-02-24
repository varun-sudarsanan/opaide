__author__ = 'Varun S S'
import data
import math


def class1_estimation(r, a, m):
    # r.payload_wt = (data.Historic_param.PASS_WEIGHT+data.Historic_param.PASS_BAG_WEIGHT)*a.pass_n + r.cargo_wt  # kg  --> For Tourism ops
    calc_payload(r)
    r.crew_wt = data.Historic_param.PILOT_WEIGHT*r.pilots_n + data.Historic_param.CABIN_CREW_WEIGHT*r.attend_n + data.Historic_param.CREW_BAG_WEIGHT*(r.pilots_n+r.attend_n)  # kg --> For Tourism ops

    wt = 4*r.payload_wt
    print "Initial Weight Estimate", wt

    f = 1
    for i in range(m.segments_num):
        if m.segments[i].type ==  "Takeoff":
            m.segments[i].wf = data.Historic_param.TAKEOFF_WF
        elif m.segments[i].type == "Climb":
            m.segments[i].wf = data.Historic_param.CLIMB_WF
        elif m.segments[i].type == "Cruise":
            m.segments[i].wf = 1/math.exp(m.segments[i].range*a.c_jet_cruise*math.pow(10,-6)/(a.v_cruise*a.l_by_d_cruise))
        elif m.segments[i].type == "Loiter":
            m.segments[i].wf = 1/math.exp(m.segments[i].time*60*60*a.c_jet_loiter*math.pow(10,-6)/a.l_by_d_loiter)
        elif m.segments[i].type == "Descent":
            m.segments[i].wf = data.Historic_param.DESCENT_WF
        else:
            m.segments[i].wf = data.Historic_param.LANDING_WF
        print m.segments[i].type
        print "Wf : ",  m.segments[i].wf
        f = f*m.segments[i].wf
    temp = 0
    print "Weight fraction f: ", f
    m.fuel_fraction = (1+a.rff)*(1-f)
    print "Fuel fraction", m.fuel_fraction

    ew_f = data.Historic_param.WEIGHT_A*math.pow(wt,(data.Historic_param.WEIGHT_C*data.Historic_param.WEIGHT_K))
    wt = (r.payload_wt+r.crew_wt)/(1-ew_f-m.fuel_fraction)

    count = 0
    while math.fabs(wt-temp) > 5:
        temp = wt
        ew_f = data.Historic_param.WEIGHT_A*math.pow(wt,(data.Historic_param.WEIGHT_C*data.Historic_param.WEIGHT_K))
        wt = (r.payload_wt+r.crew_wt)/(1-ew_f-m.fuel_fraction)
        count += 1
    print "Gross Weight", wt
    a.gross_weight = wt

def constraint(r,a,m):
    eng_n = a.prop.num_engines
    # Take-off ground roll
    tak = PlotConst()



    # SSCG
    sscg = PlotConst()
    for j in range(sscg.num_data):
        sscg.t_by_w = (eng_n/(eng_n-1))*(1/a.l_by_d_cruise+data.Regulations.SSCG(eng_n))

    # MAG;
    mag = PlotConst()
    for j in range(mag.num_data):
        mag.t_by_w = (eng_n/(eng_n-1))*(1/a.l_by_d_cruise+data.Regulations.MAG(eng_n))

    # Rate of Climb
    roc = PlotConst()
    g = r.roc/a.v_climb
    for j in range(roc.num_data):
        q = 0.5*data.Atmospheric_param.rho(m.segments[0].altitude)*math.pow(a.v_climb,2)
        k = math.pi*a.wing.a_r*a.wing.e
        exp = math.pow(roc.t_by_w[j] - g,2) - 4*a.cd0/k
        if exp >= 0:
            term = roc.t_by_w[j] - g
            if term+math.sqrt(exp) >= 0 and term-math.sqrt(exp) >= 0:
                roc.w_by_s[j] = min(term+math.sqrt(exp),term-math.sqrt(exp))
            elif term+math.sqrt(exp) >= 0:
                roc.w_by_s[j] = term+math.sqrt(exp)
            else:
                roc.w_by_s[j] = 0
                roc.t_by_w[j] = 0
        else:
                roc.w_by_s[j] = 0
                roc.t_by_w[j] = 0

    # Landing Constraint
    lan = PlotConst()
    s_land_ft = r.la_distance*data.Conversion.M_2_FT/data.Historic_param.LAND_FRACT

    for j in range(lan.num_data):
        t = a.cl_max*data.Atmospheric_param.rho(m.segments[0].altitude)(s_land_ft - m.app_dist)/80
        lan.w_by_s[j] = t*data.Conversion.LB_2_KG*math.pow(data.Conversion.M_2_FT,2)

class PlotConst:
    tbyw_start = 0.1
    tbyw_end = 1.5
    wbys_start = 75
    wbys_end = 800
    def __init__(self):
        self.t_by_w = []
        i = 0
        self.t_by_w[i] = PlotConst.tbyw_start
        while self.t_by_w[i] <= PlotConst.tbyw_end:
            if i != 0:
                self.t_by_w[i].append(self.t_by_w[i-1]+0.05)
            i += 1
        i = 0

        self.num_data = len(self.t_by_w)
        self.w_by_s = []
        for j in range(self.num_data):
            self.w_by_s.append(PlotConst.wbys_start + 10*j)

def calc_payload(r):
    r.payload_wt = (data.Historic_param.PASS_WEIGHT+data.Historic_param.PASS_BAG_WEIGHT)*r.pass_num + r.cargo_wt
