__author__ = 'Varun S S'
from PyQt4.QtCore import pyqtSignal,QObject,pyqtSlot,QString
from PyQt4 import QtGui, uic, QtCore

import data
import math
import req
import config
import mission
import analysis
import pyqtgraph

from gui import Window3

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        self.create_objects()

        # self.requirements()
        # self.mission()

        self.mw = Window3.Ui_MainWindow()
        super(MyWindow, self).__init__()
        self.mw.setupUi(self)
        self.update_gui()

        self.update_objects()


        #self.connect(self.mw.pass_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.change_gross_wt)

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
        self.set_defaults()
        self.unit_conversions()
        self.data_input()
        # #self.mw.min_pass.setText("Min_pass\n"+QString.number(self.req1.min_pass))
        # self.mw.max_pass.setText("Max_pass\n"+QString.number(self.req1.max_pass))
        #
        # self.mw.pass_slider.minimum = self.req1.min_pass
        # self.mw.pass_slider.maximum = self.req1.max_pass
        #
        # self.mw.pass_label.setText("Passengers:\n"+QString.number(self.req1.min_pass))
        # se = analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        # self.mw.wt_estimate_label.setText("Gross Weight:\n"+QString.number(se))
        # self.aircraft1.gross_weight = se
        # self.update_objects()

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

    def set_defaults(self):

        # Requirements Tab
        self.mw.des_rang_inp.setText(QString.number(self.req1.design_range))
        self.mw.des_rang_payload_inp.setText(QString.number(self.req1.des_rang_payload))
        self.mw.serv_ceil_inp.setText(QString.number(self.req1.service_ceil))
        self.mw.roc_inp.setText(QString.number(self.req1.roc))
        self.mw.cruise_m_inp.setText(QString.number(self.req1.cruise_mach))
        self.mw.tod_land_inp.setText(QString.number(self.req1.to_distance))
        self.mw.tod_water_inp.setText(QString.number(self.req1.to_distance))
        self.mw.lan_land_inp.setText(QString.number(self.req1.la_distance))
        self.mw.lan_water_inp.setText(QString.number(self.req1.la_distance))
        self.mw.max_run_alt_inp.setText(QString.number(self.req1.max_run_alt))
        self.mw.inst_inp.setText(QString.number(self.req1.inst_turn))
        self.mw.sus_inp.setText(QString.number(self.req1.sus_turn))
        self.mw.bank_ang_inp.setText(QString.number(self.req1.bank_ang))
        self.mw.fuel_res_inp.setText(QString.number(self.req1.fuel_res_rang))
        self.mw.pass_inp.setText(QString.number(self.req1.min_pass))
        self.mw.cargo_inp.setText(QString.number(self.req1.cargo_wt))
        self.mw.pay_wt_inp.setText(QString.number(self.req1.payload_wt))

        # Mission Definition Tab

        self.mw.miss_nam_inp.setText(self.mission1.name)
        self.mw.num_miss_inp.setText(QString.number(self.mission1.segments_num))
        self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[0].y_pos_start))
        self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[0].range))
        self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[0].height))
        self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[0].time))

    def unit_conversions(self):
        self.connect(self.mw.des_rang_km_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.des_rang_km_comb)
        self.connect(self.mw.des_rang_payload_kg_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.des_rang_payload_kg_comb)
        self.connect(self.mw.ser_ceil_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.ser_ceil_m_comb)

    def data_input(self):
        self.connect(self.mw.des_rang_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.des_rang_inp)
        self.connect(self.mw.des_rang_payload_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.des_rang_payload_inp)
        self.connect(self.mw.serv_ceil_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.serv_ceil_inp)
        self.connect(self.mw.roc_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.roc_inp)
        self.connect(self.mw.cruise_m_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cruise_m_inp)

    # Data Input Slots
    @pyqtSlot()
    def des_rang_inp(self, text):
        if self.isfloat(text):
            self.req1.design_range = float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.des_rang_lab.text())
            self.mw.des_rang_inp.setText("0")
            self.req1.design_range = 0
            input_warn.exec_()

    @pyqtSlot()
    def des_rang_payload_inp(self, text):
        if self.isfloat(text):
            self.req1.des_rang_payload = float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.des_rang_payload_lab.text())
            self.mw.des_rang_payload_inp.setText("0")
            self.req1.des_rang_payload = 0
            input_warn.exec_()

    @pyqtSlot()
    def serv_ceil_inp(self, text):
        if self.isfloat(text):
            self.req1.service_ceil = float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.serv_ceil_lab.text())
            self.mw.serv_ceil_inp.setText("0")
            self.req1.service_ceil = 0
            input_warn.exec_()

    @pyqtSlot()
    def roc_inp(self, text):
        if self.isfloat(text):
            self.req1.roc = float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.roc_lab.text())
            self.mw.roc_inp.setText("0")
            self.req1.roc = 0
            input_warn.exec_()

    @pyqtSlot()
    def cruise_m_inp(self, text):
        if self.isfloat(text):
            self.req1.cruise_mach = float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.cruise_m_lab.text())
            self.mw.cruise_m_inp.setText("0")
            self.req1.cruise_mach = 0
            input_warn.exec_()

    # Unit conversion Slots
    @pyqtSlot()
    def des_rang_km_comb(self, dist):
        if dist == "mi":
            g = data.Conversion.KM_2_MI*self.req1.design_range
            self.mw.des_rang_inp.setText(QString.number(g))
        elif dist == "nm":
            g = data.Conversion.KM_2_NM*self.req1.design_range
            self.mw.des_rang_inp.setText(QString.number(g))
        else:
            self.mw.des_rang_inp.setText(QString.number(self.req1.design_range))

    @pyqtSlot()
    def des_rang_payload_kg_comb(self, wt):
        if wt == "lb":
            g = self.req1.des_rang_payload/data.Conversion.LB_2_KG
            self.mw.des_rang_payload_inp.setText(QString.number(g))
        else:
            self.mw.des_rang_payload_inp.setText(QString.number(self.req1.payload_wt))

    @pyqtSlot()
    def ser_ceil_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.service_ceil*data.Conversion.M_2_FT
            self.mw.serv_ceil_inp.setText(QString.number(g))
        else:
            self.mw.serv_ceil_inp.setText(QString.number(self.req1.service_ceil))

    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False


