__author__ = 'Varun S S'
import data
import math


def class1_estimation(r, a, m):
    calc_payload(r)
    r.crew_wt = data.Historic_param.PILOT_WEIGHT*r.pilots_n + data.Historic_param.CABIN_CREW_WEIGHT*r.attend_n + data.Historic_param.CREW_BAG_WEIGHT*(r.pilots_n+r.attend_n)  # kg --> For Tourism ops

    wt = 4*r.payload_wt

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
        f = f*m.segments[i].wf
    temp = 0

    m.fuel_fraction = (1+a.rff)*(1-f)

    ew_f = data.Historic_param.WEIGHT_A*math.pow(wt,(data.Historic_param.WEIGHT_C*data.Historic_param.WEIGHT_K))
    wt = (r.payload_wt+r.crew_wt)/(1-ew_f-m.fuel_fraction)

    count = 0
    while math.fabs(wt-temp) > 5:
        temp = wt
        ew_f = data.Historic_param.WEIGHT_A*math.pow(wt,(data.Historic_param.WEIGHT_C*data.Historic_param.WEIGHT_K))
        wt = (r.payload_wt+r.crew_wt)/(1-ew_f-m.fuel_fraction)
        count += 1
    a.gross_weight = wt

def constraint(r, a, m):
    eng_n = a.prop.engines_num
    # Take-off ground roll
    tak = PlotConst()
    tak.name = "togr"
    # SSCG
    sscg = PlotConst()
    sscg.name = "sscg"

    for j in range(sscg.num_data):
        sscg.t_by_w[j] = (eng_n/(eng_n-1))*(1/a.l_by_d_cruise+data.Regulations.SSCG(r.regulation,eng_n))

    # MAG;
    mag = PlotConst()
    mag.name = "mag"
    for j in range(mag.num_data):
        mag.t_by_w[j] = (eng_n/(eng_n-1))*(1/a.l_by_d_cruise+data.Regulations.MAG(r.regulation,eng_n))

    # Rate of Climb
    roc = PlotConst()

    roc.name = "roc"
    g = r.roc/a.v_climb


    for j in range(roc.num_data):
        q = 0.5*data.Atmospheric_param.rho(m.segments[0].height)*math.pow(a.v_climb,2)
        k = math.pi*a.wing.a_r*a.wing.e
        exp = math.pow((roc.t_by_w[j] - g), 2) - 4*a.cd0/k
        if exp >= 0:
            term = roc.t_by_w[j] - g
            if term+math.sqrt(exp) >= 0 and term-math.sqrt(exp) >= 0:
                roc.w_by_s[j] = min(term+math.sqrt(exp),term-math.sqrt(exp))*q*k/2
            elif term+math.sqrt(exp) >= 0:
                roc.w_by_s[j] = (term+math.sqrt(exp))*q*k/2
            else:
                roc.w_by_s[j] = 0
                roc.t_by_w[j] = 0
        else:
                roc.w_by_s[j] = 0
                roc.t_by_w[j] = 0

    # Landing Constraint
    lan = PlotConst()
    lan.name = "lfl"
    s_land_ft = r.la_distance_land*data.Conversion.M_2_FT/data.Historic_param.LAND_FRACT

    for j in range(lan.num_data):
        t = a.cl_max*data.Atmospheric_param.rho(m.segments[0].height)*(s_land_ft - r.app_dist)/80
        lan.w_by_s[j] = t*data.Conversion.LBFT2_2_KGM2


    r.constraints = [tak,sscg,mag,roc,lan]

class PlotConst:
    tbyw_start = 0.1
    tbyw_end = 1.5
    wbys_start = 75
    wbys_end = 800

    def __init__(self):
        self.name = ""
        self.t_by_w = [PlotConst.tbyw_start]
        i = 0
        while self.t_by_w[i] <= PlotConst.tbyw_end:
            temp = self.t_by_w[i]+0.05
            self.t_by_w.append(temp)
            i += 1
        self.num_data = len(self.t_by_w)
        self.w_by_s = [PlotConst.wbys_start]
        for j in range(self.num_data):
            if j != 0:
                self.w_by_s.append(PlotConst.wbys_start + 10*j)

def calc_payload(r):
    r.payload_wt = (data.Historic_param.PASS_WEIGHT+data.Historic_param.PASS_BAG_WEIGHT)*r.pass_num + r.cargo_wt
