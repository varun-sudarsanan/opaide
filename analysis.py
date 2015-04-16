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
    tak.w_by_s[0] = r.to_disance_land*data.sigma(r.max_run_alt)*a.cl_lo*tak.t_by_w[0]*data.Atmospheric_param.g*data.Atmospheric_param.RHO_SL
    j=1
    while tak.w_by_s[j-1] < tak.wbys_end:
        tak.t_by_w.append(tak.t_by_w[0]+0.05*j)
        t = r.to_disance_land*data.sigma(r.max_run_alt)*a.cl_lo*tak.t_by_w[0]*data.Atmospheric_param.g*data.Atmospheric_param.RHO_SL
        tak.w_by_s.append(t)
        j += 1
    tak.num_data = len(tak.w_by_s)


    # SSCG
    sscg = PlotConst()
    sscg.name = "sscg"
    thrust_load = (eng_n/(eng_n-1))*(1/a.l_by_d_cruise+data.Regulations.SSCG(r.regulation,eng_n))

    sscg.t_by_w[0] = thrust_load
    j=1
    while sscg.w_by_s[j-1] < sscg.wbys_end:
        sscg.w_by_s.append(sscg.w_by_s[0]+10*j)
        sscg.t_by_w.append(thrust_load)
        j += 1
    sscg.num_data = len(sscg.t_by_w)


    # MAG;
    mag = PlotConst()
    mag.name = "mag"

    thrust_load = (eng_n/(eng_n-1))*(1/a.l_by_d_cruise+data.Regulations.MAG(r.regulation,eng_n))

    mag.t_by_w[0] = thrust_load
    j=1
    while mag.w_by_s[j-1] < mag.wbys_end:
        mag.w_by_s.append(mag.w_by_s[0]+10*j)
        mag.t_by_w.append(thrust_load)
        j += 1
    mag.num_data = len(mag.t_by_w)


    # Rate of Climb
    roc = PlotConst()

    roc.name = "roc"
    g = r.roc/a.v_climb
    c=0
    j=0
    i=0
    roc.t_by_w[0] = 0.4

    while roc.t_by_w[i] < roc.tbyw_end:
        if j==0:
            roc.t_by_w[0] = 0.4 + c
        else:
            roc.t_by_w.append(roc.t_by_w[0]+c)
            i += 1
        q = 0.5*data.Atmospheric_param.rho(m.segments[0].height,r.roc_isa_t)*math.pow(a.v_climb,2)
        k = math.pi*a.wing.a_r*a.wing.e
        exp = math.pow((roc.t_by_w[j] - g), 2) - 4*a.cd0/k

        if exp >= 0:
            term = roc.t_by_w[j] - g
            if term-math.sqrt(exp) >= 0:
                if j == 0:
                    roc.w_by_s[j] = min(term+math.sqrt(exp),term-math.sqrt(exp))*q*k/2
                else:
                    roc.w_by_s.append(min(term+math.sqrt(exp),term-math.sqrt(exp))*q*k/2)
                j += 1
            elif term+math.sqrt(exp) >= 0:
                if j == 0:
                    roc.w_by_s[j] = (term+math.sqrt(exp))*q*k/2
                else:
                    roc.w_by_s.append((term+math.sqrt(exp))*q*k/2)
                j += 1

        c += 0.005

    roc.num_data = len(roc.w_by_s)
    # Landing Constraint
    lan = PlotConst()

    s_land_ft = r.la_distance_land*data.Conversion.M_2_FT/data.Historic_param.LAND_FRACT
    t = data.Conversion.LBFT2_2_KGM2*a.cl_max*data.Atmospheric_param.rho(m.segments[0].height,r.run_msl_isa_t)*(s_land_ft - r.app_dist)/80
    lan.w_by_s[0] = t
    j=1
    while lan.w_by_s[j-1] < lan.wbys_end:
        lan.w_by_s.append(t)
        lan.t_by_w.append(lan.t_by_w[0]+0.05*j)
        j += 1
    lan.num_data = len(lan.w_by_s)

    #Stall Velocity
    stall = PlotConst()
    t = 0.5*data.Atmospheric_param.rho(0,0)*math.pow(r.v_stall_max,2)*a.cl_max
    stall.w_by_s[0] = t
    j=1
    while stall.w_by_s[j-1] < stall.w_by_s:
        stall.w_by_s.append(t)
        stall.t_by_w.append(stall.t_by_w[0]+0.05*j)
        j += 1

    #Turn Rate

    r.constraints = [tak,sscg,mag,roc,lan,stall]

class PlotConst:
    tbyw_start = 0.1
    tbyw_end = 1.5
    wbys_start = 75
    wbys_end = 500

    def __init__(self):
        self.name = ""
        self.t_by_w = [PlotConst.tbyw_start]
        self.w_by_s = [PlotConst.wbys_start]
        self.num_data = 1

def calc_payload(r):
    r.payload_wt = (data.Historic_param.Fuselage.PASS_WEIGHT+data.Historic_param.Fuselage.PASS_BAG_WEIGHT)*r.pass_num + r.cargo_wt

def cabin_length_sizing(a):
    len = 0
    if a.fuse.cabin.type == "Passenger":
        for i in range(a.fuse.cabin.class_num):
            print i
            if a.fuse.cabin.avg_seats_abr[i]!=0:
                a.fuse.cabin.rows_num[i] = a.fuse.cabin.seats_num[i]/a.fuse.cabin.avg_seats_abr[i]
            print "rows"
            print a.fuse.cabin.rows_num[i]
            lav_even = 0
            galley_len = 0
            # lavatory length
            if a.fuse.cabin.lav_num[i]%2 == 0:
                lav_even = 1
                lav_len = a.fuse.cabin.lav_num[i]*data.Historic_param.Fuselage.LAVATORY_LENGTH/2
            else:
                if a.fuse.cabin.galley[i] == 1:
                    l = max(data.Historic_param.Fuselage.LAVATORY_LENGTH,data.Historic_param.Fuselage.GALLEY_LENGTH)
                    lav_len = a.fuse.cabin.lav_num[i]*data.Historic_param.Fuselage.LAVATORY_LENGTH/2+l
                else:
                    lav_len = (a.fuse.cabin.lav_num[i]/2+1)*data.Historic_param.Fuselage.LAVATORY_LENGTH
            if a.fuse.cabin.galley[i] == 1:
                if lav_even == 1:
                    galley_len = data.Historic_param.Fuselage.GALLEY_LENGTH
            else:
                galley_len = 0
            len = len + a.fuse.cabin.rows_num[i]*a.fuse.cabin.seat_pitch[i]+lav_len+galley_len
    a.fuse.cabin.length = len

def cabin_cs_sizing(a):
    seat_width = 0
    for i in range(a.fuse.cabin.class_num):
        seat = a.fuse.cabin.avg_seats_abr[i]
        aisle = a.fuse.cabin.aisle_num[i]
        w = seat*data.Historic_param.Fuselage.SEAT_WIDTH + aisle*data.Historic_param.Fuselage.AISLE_WIDTH
        print w
        if w>seat_width:
            seat_width = w
    print seat_width
    container_width_top = a.fuse.container.width_top*(a.fuse.container.double+1) # Double the width for two half containers
    container_width_bot = a.fuse.container.width_bot*(a.fuse.container.double+1) # Double the width for two half containers
    floor_width = max(seat_width,container_width_top)
    h = a.fuse.container.height+a.fuse.cabin.floor_thickness+data.Historic_param.Passenger.HEIGHT+data.Historic_param.Passenger.HEAD2WALL_CLEARANCE
    r = a.fuse.cabin.cabin_h2w_ratio
    floor_lower = a.fuse.cabin.floor_lowering
    a.fuse.cabin.inner_width = math.sqrt(math.pow((r*floor_width/2),2)+math.pow(floor_lower,2))/r
    a.fuse.cabin.inner_height = r*a.fuse.cabin.inner_width
    if h > a.fuse.cabin.inner_height:
        print "Height not sufficient"
    else:
        print "Height sufficient"

class Fuselage_data:
    a_ell = 0

