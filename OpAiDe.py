import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSignal,QObject,pyqtSlot,QString

import data
import math
import req
import config
import mission
import analysis
import pyqtgraph



from gui import window
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        self.create_objects()

        self.requirements()
        self.mission()

        self.mw = window.Ui_MainWindow()
        super(MyWindow, self).__init__()
        self.mw.setupUi(self)

        self.update_objects()
        self.update_gui()
        # print "Payload Weight", self.req1.payload_wt
        # print "Crew Weight", self.req1.crew_wt
        # print "Cruise Speed", self.aircraft1.v_cruise
        # print "Loiter Time 1", self.mission1.segments[3].time
        # print "Loiter TIme 2", self.mission1.segments[9].time
        # print "Cruise Range 1", self.mission1.segments[2].range
        # print "Cruise Range 2", self.mission1.segments[8].range
        # print "A", data.Historic_param.WEIGHT_A
        # print "C", data.Historic_param.WEIGHT_C
        # print "K", data.Historic_param.WEIGHT_K
        # print "C Power TP Cruise", data.Historic_param.C_POW_CRUISE
        # print "C Power TP Loiter", data.Historic_param.C_POW_LOITER
        # print "Propeller Efficiency", data.Historic_param.PROP_EFF
        # print "L/D max", data.Historic_param.L_BY_D_MAX
        # print "RFF", self.aircraft1.rff
        # print "W1/W0", data.Historic_param.TAKEOFF_WF
        # print "W2/W1", data.Historic_param.CLIMB_WF
        # print "W4/W3 1"
        # print "W6/W5", data.Historic_param.DESCENT_WF
        # print "W7/W6", data.Historic_param.LANDING_WF
        #
        # print "Propeller Efficiency", data.Historic_param.PROP_EFF
        # print "Payload Weight", self.req1.payload_wt
        #
        # print "L/D cruise", self.aircraft1.l_by_d_cruise
        # print "L/D loiter", self.aircraft1.l_by_d_loiter
        # print "C Jet cruise", self.aircraft1.c_jet_cruise
        # print "C Jet Loiter", self.aircraft1.c_jet_loiter
        # print "Wf", self.mission1.fuel_fraction
        # print "Gross Weight", self.aircraft1.gross_weight

        self.connect(self.mw.pass_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.change_gross_wt)

        self.show()
    @pyqtSlot()
    def change_gross_wt(self,pos):
        n = self.req1.min_pass + 1
        if n <= self.req1.max_pass:
            self.aircraft1.pass_n = n # int(pos/(self.req1.max_pass- self.req1.min_pass))
        se = analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        self.mw.pass_label.setText("Passengers:\n"+QString.number(self.aircraft1.pass_n)) #lf.aircraft1.gross_weight))
        self.mw.wt_estimate_label.setText("Gross Weight:\n"+QString.number(se)) #lf.aircraft1.gross_weight))

    def update_gui(self):
        self.mw.min_pass.setText("Min_pass\n"+QString.number(self.req1.min_pass))
        self.mw.max_pass.setText("Max_pass\n"+QString.number(self.req1.max_pass))

        self.mw.pass_slider.minimum = self.req1.min_pass
        self.mw.pass_slider.maximum = self.req1.max_pass

        self.mw.pass_label.setText("Passengers:\n"+QString.number(self.req1.min_pass))
        se = analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        self.mw.wt_estimate_label.setText("Gross Weight:\n"+QString.number(se))
        self.aircraft1.gross_weight = se
        self.update_objects()

    def create_objects(self):
        self.req1 = req.AircraftRequirements()
        self.aircraft1 = config.Aircraft()

        self.mission1 = mission.MissionDef()

        # for i in range(self.mission1.num_segments):
        #     self.mission1.segments[i].ref=i
        #     if self.mission1.segments[i].type==3:
        #        self.mission1.segments[i].range=self.req1.design_range
        #     elif self.mission1.segments[i].type==4:
        #         self.mission1.segments[i].time=self.req1.loiter_time

    def update_objects(self):
        self.req1.update_req(self.aircraft1)
        self.aircraft1.update_config()
        self.mission1.update_mission()

    def requirements(self):
        print "Requirements"
        print "=====**====="
        t = 0
        while t ==0:
            st = raw_input("Enter design range: (km) ")
            if self.isfloat(st):
                self.req1.design_range = float(st)
                t = 1
            else:
                print "Please enter a number"
        t = 0
        while t ==0:
            st = raw_input("Enter max. stall velocity: (m/s) ")
            if self.isfloat(st):
                self.req1.v_stall_max = float(st)
                t = 1
            else:
                print "Please enter a number"

        t = 0
        while t == 0:
            st = raw_input("Enter minimum number of passengers:")
            if st.isdigit():
                self.req1.min_pass = int(st)
                self.aircraft1.pass_n = self.req1.min_pass
                t = 1
            else:
                print "Please enter a valid number"

        t = 0
        while t ==0:
            st = raw_input("Enter maximum number of passengers:")
            if st.isdigit():
                self.req1.max_pass = int(st)
                t = 1
            else:
                print "Please enter a valid number"

        t = 0
        while t ==0:
            st = raw_input("Enter the cargo weight to be carried: (kg)")
            if self.isfloat(st):
                self.req1.cargo_wt = float(st)
                t = 1
            else:
                print "Please enter a number"

        t = 0
        while t == 0:
            st = raw_input("Enter the maximum takeoff distance available: (m)")
            if self.isfloat(st):
                self.req1.to_distance = float(st)
                t = 1
            else:
                print "Please enter a number"

        t = 0
        while t ==0:
            st = raw_input("Enter the maximum landing distance available: (m)")
            if self.isfloat(st):
                self.req1.la_distance = float(st)
                t = 1
            else:
                print "Please enter a number"
        print "\n"


    def mission(self):
        print "Mission Definition"
        print "========**========"
        t=0
        while t==0:
            num = raw_input("Enter the number of mission segments:")
            if num.isdigit():
                self.mission1.define_mission(int(num))
                t = 1
            else:
                print "Please enter a number"
        i=0
        while i < self.mission1.segments_num:
            segment = self.mission1.segments[i]
            segment.type = raw_input("Enter the type of segment for segment "+str(i+1) + " (takeoff, climb, cruise, loiter, descent, landing)")
            if segment.type == "takeoff":
                t = 0
                while t == 0:
                    st = raw_input("Enter runway altitude: (m)")
                    if self.isfloat(st):
                        segment.altitude = float(st)
                        t = 1
                        segment.range = self.req1.to_distance
                    else:
                        print "Please enter a number"
            elif segment.type == "climb":
                t = 0
                while t == 0:
                    st = raw_input("Enter the altitude to which it climbs: (m)")
                    if self.isfloat(st):
                        segment.altitude = float(st)
                        t = 1
                    else:
                        print "Please enter a number"
            elif segment.type == "cruise":
                t = 0
                while t == 0:
                    st = raw_input("Enter the distance traversed during this segment: (km)")
                    if self.isfloat(st):
                        segment.range = float(st)
                        t = 1
                    else:
                        print "Please enter a number"
            elif segment.type == "loiter":
                t = 0
                while t == 0:
                    st = raw_input("Enter the loiter duration: (hr)")
                    if self.isfloat(st): #(st.isdigit()):
                        segment.time = float(st)
                        t = 1
                    else:
                        print "Please enter a number"
            elif segment.type == "descent":
                t = 0
                while t == 0:
                    st = raw_input("Enter the altitude at the end of segment: (m)")
                    if self.isfloat(st):
                        segment.altitude = float(st)
                        t = 1
                    else:
                        print "Please enter a number"
            elif segment.type == "landing":
                t = 0
                while t == 0:
                    st = raw_input("Enter the altitude of the runway: (m)")
                    if self.isfloat(st):
                        segment.altitude = float(st)
                        t = 1
                        segment.range = self.req1.la_distance
                    else:
                        print "Please enter a number"
                t=0
                while t == 0:
                    st = raw_input("Enter the max. obstacle height near the runway: (m)")
                    if self.isfloat(st):
                        self.mission1.h_obs = float(st)
                        t = 1
                    else:
                        print "Please enter a number"
                t=0
                while t == 0:
                    st = raw_input("Enter the approach angle: (deg)")
                    if self.isfloat(st):
                        self.mission1.app_ang = float(st)
                        t = 1
                        self.mission1.app_dist = self.mission1.h_obs/math.tan(self.mission1.app_ang*math.pi/180)
                    else:
                        print "Please enter a number"
            else:
                i -= 1
                print "Incorrect segment type"
            i += 1
            print i

    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False


app = QtGui.QApplication(sys.argv)
win = MyWindow()

sys.exit(app.exec_())