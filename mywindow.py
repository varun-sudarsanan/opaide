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
        self.mw.tabWidget.setCurrentIndex(0)

        self.update_gui()

        self.update_objects()


        #self.connect(self.mw.pass_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.change_gross_wt)

        self.show()

    def update_gui(self):
        self.requirements()
        self.mission()
        self.design_space()

    def create_objects(self):
        self.req1 = req.AircraftRequirements()
        self.aircraft1 = config.Aircraft()

        self.mission1 = mission.MissionDef()

    def update_objects(self):
        self.req1.update_req(self.aircraft1)
        self.aircraft1.update_config()
        self.mission1.update_mission()

    def requirements(self):
        self.req_set_defaults()
        self.req_unit_conversions()
        self.req_data_input()

    def mission(self):
        self.miss_set_defaults()
        self.miss_segments()
        self.miss_unit_conversions()
        self.miss_data_inputs()
        self.mission_profile()
        self.connect(self.mw.add_seg_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add_seg_push)
        self.connect(self.mw.rem_seg_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rem_seg_push)

    def design_space(self):
        p = self.req1.pass_num
        c = self.req1.cargo_wt
        p_min = p-5
        p_max = p+5
        c_min = c-100
        c_max = c+100

        self.mw.max_pass_lab.setText(QString.number(p_max))
        self.mw.min_pass_lab.setText(QString.number(p_min))

        self.mw.pass_slider.setMinimum(p_min)
        self.mw.pass_slider.setMaximum(p_max)
        self.mw.pass_slider.setValue(p)

        self.mw.current_pass_num.setText(QString.number(self.mw.pass_slider.value()))

        self.mw.max_cargo_lab.setText(QString.number(c_max))
        self.mw.min_cargo_lab.setText(QString.number(c_min))

        self.mw.cargo_slider.setMinimum(c_min)
        self.mw.cargo_slider.setMaximum(c_max)
        self.mw.cargo_slider.setSingleStep(20)
        self.mw.cargo_slider.setValue(c)

        self.mw.current_cargo_wt.setText(QString.number(self.mw.cargo_slider.value()))

        self.connect(self.mw.cargo_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.cargo_w_gross)
        self.connect(self.mw.pass_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.pass_w_gross)

        self.graph_controls()

    def req_set_defaults(self):

        # Requirements Tab
        self.mw.des_rang_inp.setText(QString.number(self.req1.design_range))
        self.mw.des_rang_payload_inp.setText(QString.number(self.req1.des_rang_payload))
        self.mw.serv_ceil_inp.setText(QString.number(self.req1.service_ceil))
        self.mw.roc_inp.setText(QString.number(self.req1.roc))
        self.mw.cruise_m_inp.setText(QString.number(self.req1.cruise_mach))
        self.mw.tod_land_inp.setText(QString.number(self.req1.to_distance_land))
        self.mw.tod_water_inp.setText(QString.number(self.req1.to_distance_water))
        self.mw.lan_land_inp.setText(QString.number(self.req1.la_distance_land))
        self.mw.lan_water_inp.setText(QString.number(self.req1.la_distance_water))
        self.mw.max_run_alt_inp.setText(QString.number(self.req1.max_run_alt))
        self.mw.inst_inp.setText(QString.number(self.req1.inst_turn))
        self.mw.sus_inp.setText(QString.number(self.req1.sus_turn))
        self.mw.bank_ang_inp.setText(QString.number(self.req1.bank_ang))
        self.mw.fuel_res_inp.setText(QString.number(self.req1.fuel_res_rang))
        self.mw.pass_inp.setText(QString.number(self.req1.pass_num))
        self.mw.cargo_inp.setText(QString.number(self.req1.cargo_wt))
        analysis.calc_payload(self.req1)
        self.mw.pay_wt_inplab.setText(QString.number(self.req1.payload_wt))
        self.mw.atm_alt_lab.setText("Atmospheric Compliance at "+QString.number(self.req1.max_run_alt)+" m")
        self.mw.engine_inp.setText(QString.number(self.aircraft1.prop.engines_num))
        # Mission Definition Tab

        self.mw.miss_nam_inp.setText(self.mission1.name)
        self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[0].y_pos_start))
        self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[0].range))
        self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[0].height))
        self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[0].time))

    def req_unit_conversions(self):
        self.connect(self.mw.des_rang_km_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.des_rang_km_comb)
        self.connect(self.mw.des_rang_payload_kg_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.des_rang_payload_kg_comb)
        self.connect(self.mw.ser_ceil_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.ser_ceil_m_comb)
        self.connect(self.mw.roc_mpers_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.roc_mpers_comb)

        self.connect(self.mw.tod_lan_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.tod_lan_m_comb)
        self.connect(self.mw.tod_water_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.tod_water_m_comb)
        self.connect(self.mw.lan_land_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.lan_land_m_comb)
        self.connect(self.mw.lan_water_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.lan_water_m_comb)
        self.connect(self.mw.max_run_alt_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.max_run_alt_m_comb)

        self.connect(self.mw.inst_degpers_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.inst_degpers_comb)
        self.connect(self.mw.sus_degpers_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.sus_degpers_comb)
        self.connect(self.mw.bank_ang_deg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.bank_ang_comb)

        self.connect(self.mw.fuel_res_km_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.fuel_res_km_comb)
        self.connect(self.mw.cargo_kg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.cargo_kg_comb)

    def req_data_input(self):
        self.connect(self.mw.des_rang_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.des_rang_inp)
        self.connect(self.mw.des_rang_payload_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.des_rang_payload_inp)
        self.connect(self.mw.serv_ceil_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.serv_ceil_inp)
        self.connect(self.mw.roc_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.roc_inp)
        self.connect(self.mw.cruise_m_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cruise_m_inp)

        self.connect(self.mw.tod_land_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.tod_land_inp)
        self.connect(self.mw.tod_water_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.tod_water_inp)
        self.connect(self.mw.lan_land_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.lan_land_inp)
        self.connect(self.mw.lan_water_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.lan_water_inp)
        self.connect(self.mw.max_run_alt_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.max_run_alt_inp)

        self.connect(self.mw.inst_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.inst_inp)
        self.connect(self.mw.sus_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.sus_inp)
        self.connect(self.mw.bank_ang_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.bank_ang_inp)

        self.connect(self.mw.fuel_res_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.fuel_res_inp)
        self.connect(self.mw.pass_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.pass_inp)
        self.connect(self.mw.cargo_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cargo_inp)
        self.connect(self.mw.engine_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.engine_inp)
        # Spin boxes
        self.connect(self.mw.roc_isa_t_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.roc_isa_t_sb)
        self.connect(self.mw.run_msl_isa_t_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.run_msl_isa_t_sb)
        self.connect(self.mw.run_alt_isa_t_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.run_alt_isa_t_sb)

        # Combo Boxes
        self.connect(self.mw.set_req_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.set_req_push)
        #self.connect(self.mw.reg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.reg_comb)

    def miss_set_defaults(self):
        self.counter = 0
        self.mw.miss_nam_inp.setText(self.mission1.name)
        self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[self.counter].y_pos_start))

    def miss_segments(self):
        i = self.counter % 6
        self.mw.typ_seg_comb.setCurrentIndex(i)
        self.mw.rang_seg_m_comb.setCurrentIndex(0)
        self.mw.ht_seg_m_comb.setCurrentIndex(0)
        self.mw.time_seg_hr_comb.setCurrentIndex(0)

        self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[self.counter].range))
        self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[self.counter].height))
        self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[self.counter].time))

    def miss_data_inputs(self):
        self.connect(self.mw.miss_nam_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.miss_nam_inp)
        self.connect(self.mw.alt_beg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.alt_beg_inp)

        self.connect(self.mw.typ_seg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.typ_seg_comb)
        self.connect(self.mw.rang_seg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.rang_seg_inp)
        self.connect(self.mw.ht_seg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.ht_seg_inp)
        self.connect(self.mw.time_seg_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.time_seg_inp)

        self.connect(self.mw.ana_miss_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ana_miss_push)

    def miss_unit_conversions(self):
        self.connect(self.mw.alt_beg_seg_m_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.alt_beg_seg_m_comb)
        self.connect(self.mw.rang_seg_m_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.rang_seg_m_comb)
        self.connect(self.mw.ht_seg_m_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.ht_seg_m_comb)
        self.connect(self.mw.time_seg_hr_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.time_seg_hr_comb)

    def mission_profile(self):
        self.mw.time_seg_inp.setDisabled(True)
        self.profile = self.mw.mission_graphics
        self.scene = QtGui.QGraphicsScene()

        w = 200
        h = 60

        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        self.horiz_pos = w/2
        self.vert_pos = h*2
        self.current_horiz = -w/2
        self.current_vert = (h/2 - self.vert_pos)

        self.lines = []
        self.loiter_count = 0
        self.elipses = []

    def graph_controls(self):
        # Constants

        self.setup_graph_controls()

        self.connect(self.mw.sscg_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.sscg_check)
        self.connect(self.mw.missedapp_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.missedapp_check)
        self.connect(self.mw.landing_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.landing_check)
        self.connect(self.mw.takeoff_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.takeoff_check)
        self.connect(self.mw.roc_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.roc_check)


        self.connect(self.mw.roc_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.roc_slider)

    def setup_graph_controls(self):
        self.mw.sscg_check.setCheckState(2)
        self.mw.missedapp_check.setCheckState(2)
        self.mw.landing_check.setCheckState(2)
        self.mw.roc_check.setCheckState(2)
        self.mw.stall_check.setCheckState(2)
        self.mw.takeoff_check.setCheckState(2)

        # Roc slider
        roc_curr = self.req1.roc
        roc_min = roc_curr - 4
        roc_max = roc_curr + 4

        self.mw.roc_slider.setMinimum(roc_min)
        self.mw.roc_slider.setMaximum(roc_max)
        self.mw.roc_slider.setValue(roc_curr)
        self.mw.roc_max_lab.setText(QString.number(roc_max))
        self.mw.roc_min_lab.setText(QString.number(roc_min))
        self.mw.roc_current_lab.setText(QString.number(roc_curr))

        #Landing Slider
        land_curr = self.req1.la_distance_land
        land_min = land_curr - 200
        land_max = land_curr + 200

        self.mw.landing_slider.setMinimum(land_min)
        self.mw.landing_slider.setMaximum(land_max)
        self.mw.landing_slider.setValue(land_curr)
        self.mw.landing_max_lab.setText(QString.number(land_max))
        self.mw.landing_min_lab.setText(QString.number(land_min))
        self.mw.landing_current_lab.setText(QString.number(land_curr))

        #Takeoff Slider
        takeoff_curr = self.req1.to_distance_land
        takeoff_min = takeoff_curr - 200
        takeoff_max = takeoff_curr + 200

        self.mw.takeoff_slider.setMinimum(takeoff_min)
        self.mw.takeoff_slider.setMaximum(takeoff_max)
        self.mw.takeoff_slider.setValue(takeoff_curr)
        self.mw.takeoff_max_lab.setText(QString.number(takeoff_max))
        self.mw.takeoff_min_lab.setText(QString.number(takeoff_min))
        self.mw.takeoff_current_lab.setText(QString.number(takeoff_curr))

        #Stall Velocity
        stall_curr = self.req1.la_distance_land
        stall_min = stall_curr - 200
        stall_max = stall_curr + 200

        self.mw.stall_slider.setMinimum(stall_min)
        self.mw.stall_slider.setMaximum(stall_max)
        self.mw.stall_slider.setValue(stall_curr)
        self.mw.stall_max_lab.setText(QString.number(stall_max))
        self.mw.stall_min_lab.setText(QString.number(stall_min))
        self.mw.stall_current_lab.setText(QString.number(stall_curr))

    #Graph Sliders
    def roc_slider(self,val):
        actual = self.req1.roc
        self.req1.roc = val
        self.mw.roc_current_lab.setText(QString.number(val))
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        self.plot_constraints()
        self.req1.roc = actual

    # Checkboxes
    @pyqtSlot()
    def sscg_check(self,val):
        if val == 2:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "sscg":
                    break
            self.constraint_plots[i].setPen(0,255,0)
        elif val == 0:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "sscg":
                    break
            self.constraint_plots[i].setPen(0,0,0)

    @pyqtSlot()
    def missedapp_check(self,val):
        if val == 2:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "mag":
                    break
            self.constraint_plots[i].setPen(255,0,0)
        elif val == 0:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "mag":
                    break
            self.constraint_plots[i].setPen(0,0,0)

    @pyqtSlot()
    def landing_check(self,val):
        if val == 2:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "lan":
                    break
            self.constraint_plots[i].setPen(0,255,0)
        elif val == 0:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "lan":
                    break
            self.constraint_plots[i].setPen(0,0,0)

    @pyqtSlot()
    def takeoff_check(self,val):
        if val == 2:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "tak":
                    break
            self.constraint_plots[i].setPen(255,0,0)
        elif val == 0:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "tak":
                    break
            self.constraint_plots[i].setPen(0,0,0)
    @pyqtSlot()
    def roc_check(self,val):
        if val == 2:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "roc":
                    break
            self.constraint_plots[i].setPen(0,255,255)
        elif val == 0:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "roc":
                    break
            self.constraint_plots[i].setPen(0,0,0)

    @pyqtSlot()
    def stall_check(self,val):
        if val == 2:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "mag":
                    break
            self.constraint_plots[i].setPen(255,0,0)
        elif val == 0:
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "mag":
                    break
            self.constraint_plots[i].setPen(0,0,0)


    # Push Buttons
    @pyqtSlot()
    def add_seg_push(self):
        self.mission1.segments[self.counter].type = self.mw.typ_seg_comb.currentText()
        self.draw_segment()
        self.counter += 1
        if self.counter >= self.mission1.segments_num:
            self.mission1.segments.append(mission.MissionPhase())
            self.mission1.segments_num += 1
        self.miss_segments()
        self.add_seg_clicked = 1

    @pyqtSlot()
    def rem_seg_push(self):
        if self.counter == 0:
            pass
        else:
            self.counter -= 1
            self.mission1.segments_num -= 1
            self.delete_segment()
            self.miss_segments()

    @pyqtSlot()
    def ana_miss_push(self):
        if (self.add_seg_clicked):
            self.mission1.segments_num -= 1
        self.update_objects()
        analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        self.mw.ds_gross_out.setText(QString.number(self.aircraft1.gross_weight))
        self.add_seg_clicked = 0

        # Setting Design Space
        self.design_space()
        self.mw.tabWidget.setCurrentIndex(3)

    # Graphics View
    def delete_segment(self):
        phase = self.mission1.segments[self.counter].type
        if phase == "Takeoff":
            self.current_horiz = self.current_horiz - self.horiz_pos/2
        elif phase == "Climb":
            self.current_horiz = self.current_horiz - self.horiz_pos/2
            self.current_vert = self.current_vert + self.vert_pos
        elif phase == "Cruise":
            self.current_horiz = self.current_horiz - self.horiz_pos
        elif phase == "Loiter":
            self.current_horiz = self.current_horiz - self.horiz_pos/4
            self.current_vert = self.current_vert - self.vert_pos/2
            self.loiter_count -= 1
            self.scene.removeItem(self.elipses[self.loiter_count])
        elif phase == "Descent":
            self.current_horiz = self.current_horiz - self.horiz_pos/4
            self.current_vert = self.current_vert - self.vert_pos/2
        elif phase == "Landing":
            self.current_horiz = self.current_horiz - self.horiz_pos/2
        self.scene.removeItem(self.lines[self.counter])

    def draw_segment(self):
        self.lines.append(QtGui.QGraphicsLineItem())
        phase = self.mission1.segments[self.counter].type

        if phase == "Takeoff":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/2
            self.y1 = self.current_vert
            self.y2 = self.current_vert
        elif phase == "Climb":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/2
            self.y1 = self.current_vert
            self.y2 = self.current_vert - self.vert_pos
        elif phase == "Cruise":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos
            self.y1 = self.current_vert
            self.y2 = self.current_vert
        elif phase == "Loiter":
            self.elipses.append(QtGui.QGraphicsEllipseItem())
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/4
            self.y1 = self.current_vert
            self.y2 = self.current_vert + self.vert_pos/2
            self.elipses[self.loiter_count].setRect((self.x1+self.x2+25)/2,(self.y1+self.y2+10)/2, (self.y1-self.y2)/2,(self.x1-self.x2)/2)
            self.scene.addItem(self.elipses[self.loiter_count])
            self.loiter_count += 1
        elif phase == "Descent":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/4
            self.y1 = self.current_vert
            self.y2 = self.current_vert + self.vert_pos/2
        elif phase == "Landing":
            self.x1 = self.current_horiz
            self.x2 = self.current_horiz + self.horiz_pos/2
            self.y1 = self.current_vert
            self.y2 = self.current_vert
        self.lines[self.counter].setLine(self.x1,self.y1,self.x2,self.y2)
        self.current_horiz = self.x2
        self.current_vert = self.y2

        self.scene.addItem(self.lines[self.counter])
        self.profile.setScene(self.scene)

    def plot_constraints(self):
        for i in range(len(self.req1.constraints)):
            self.constraint_plots.append(self.mw.pw.plot())
            if self.req1.constraints[i].name == "togr":
                self.constraint_plots[i].setPen((255,222,20))
            elif self.req1.constraints[i].name == "roc":
                self.constraint_plots[i].setPen((255,0,0))
            elif self.req1.constraints[i].name == "sscg":
                self.constraint_plots[i].setPen((0,0,255))
            elif self.req1.constraints[i].name == "mag":
                self.constraint_plots[i].setPen((255,0,0))
            elif self.req1.constraints[i].name == "lfl":
                self.constraint_plots[i].setPen((255,255,255))
            self.constraint_plots[i].setData(y = self.req1.constraints[i].t_by_w, x = self.req1.constraints[i].w_by_s)

    # Data Input Slots

    # Requirements Tab
    @pyqtSlot()
    def des_rang_inp(self, text):
        if self.isfloat(text):
            if self.mw.des_rang_km_comb.currentText() == "km":
                self.req1.design_range = float(text)
            elif self.mw.des_rang_km_comb.currentText() == "mi":
                self.req1.design_range = float(text)/data.Conversion.KM_2_MI
            else:
                self.req1.design_range = float(text)/data.Conversion.KM_2_NM
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.des_rang_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def des_rang_payload_inp(self, text):
        if self.isfloat(text):
            if self.mw.des_rang_payload_kg_comb.currentText() == "kg":
                self.req1.des_rang_payload = float(text)
            else:
                self.req1.des_rang_payload = data.Conversion.LB_2_KG*float(text)
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.des_rang_payload_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def serv_ceil_inp(self, text):
        if self.isfloat(text):
            if self.mw.ser_ceil_m_comb.currentText() == "m":
                self.req1.service_ceil = float(text)
            else:
                self.req1.service_ceil = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.serv_ceil_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def roc_inp(self, text):
        if self.isfloat(text):
            if self.mw.roc_mpers_comb.currentText() == "m/s":
                self.req1.roc = float(text)
            else:
                self.req1.roc = float(text)/data.Conversion.MPERS_2_FTPERMIN
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.roc_lab.text())
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
            input_warn.exec_()

    @pyqtSlot()
    def roc_isa_t_sb(self, temp):
        self.req1.roc_isa_t = temp

    @pyqtSlot()
    def tod_land_inp(self, text):
        if self.isfloat(text):
            if self.mw.tod_lan_m_comb.currentText() == "m":
                self.req1.to_distance_land = float(text)
            else:
                self.req1.to_distance_land = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.tod_land_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def tod_water_inp(self, text):
        if self.isfloat(text):
            if self.mw.tod_water_m_comb.currentText() == "m":
                self.req1.to_distance_water = float(text)
            else:
                self.req1.to_distance_water = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.tod_water_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def lan_land_inp(self, text):
        if self.isfloat(text):
            if self.mw.lan_land_m_comb.currentText() == "m":
                self.req1.la_distance_land = float(text)
            else:
                self.req1.la_distance_land = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.lan_land_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def lan_water_inp(self, text):
        if self.isfloat(text):
            if self.mw.lan_water_m_comb.currentText() == "m":
                self.req1.la_distance_water = float(text)
            else:
                self.req1.la_distance_water = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.lan_water_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def max_run_alt_inp(self, text):
        if self.isfloat(text):
            if self.mw.max_run_alt_m_comb.currentText() == "m":
                self.req1.max_run_alt = float(text)
                self.mw.atm_alt_lab.setText("Atmospheric compliance at "+text+" m")
            else:
                f = float(text)/data.Conversion.M_2_FT
                self.req1.max_run_alt = f
                self.mw.atm_alt_lab.setText("Atmospheric compliance at "+QString.number(f)+" m")
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.max_run_alt_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def run_msl_isa_t_sb(self, temp):
        self.req1.run_msl_isa_t = temp

    @pyqtSlot()
    def run_alt_isa_t_sb(self, temp):
        self.req1.run_alt_isa_t = temp

    @pyqtSlot()
    def inst_inp(self, text):
        if self.isfloat(text):
            if self.mw.inst_degpers_comb.currentText() == "deg/s":
                self.req1.inst_turn = float(text)
            else:
                self.req1.inst_turn = float(text)/data.Conversion.DEG_2_RAD
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.inst_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def sus_inp(self, text):
        if self.isfloat(text):
            if self.mw.sus_degpers_comb.currentText() == "deg/s":
                self.req1.sus_turn = float(text)
            else:
                self.req1.sus_turn = float(text)/data.Conversion.DEG_2_RAD
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.sus_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def bank_ang_inp(self, text):
        if self.isfloat(text):
            if self.mw.bank_ang_deg_comb.currentText() == "deg":
                self.req1.bank_ang = float(text)
            else:
                self.req1.bank_ang = float(text)/data.Conversion.DEG_2_RAD
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.bank_ang_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def fuel_res_inp(self, text):
        if self.isfloat(text):
            if self.mw.fuel_res_km_comb.currentText() == "km":
                self.req1.fuel_res_rang = float(text)
            elif self.mw.fuel_res_km_comb.currentText() == "mi":
                self.req1.fuel_res_rang = float(text)/data.Conversion.KM_2_MI
            else:
                self.req1.fuel_res_rang = float(text)/data.Conversion.KM_2_NM
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.fuel_res_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def pass_inp(self, num):
        print num
        if self.isdigit(num):
            self.req1.pass_num = int(num)
            analysis.calc_payload(self.req1)
            self.mw.pay_wt_inplab.setText(QString.number(self.req1.payload_wt))
        elif num == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.pass_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def cargo_inp(self, wt):
         if self.isfloat(wt):
            if self.mw.cargo_kg_comb.currentText() == "kg":
                self.req1.cargo_wt = float(wt)
            else:
                self.req1.cargo_wt = data.Conversion.LB_2_KG*float(wt)
            analysis.calc_payload(self.req1)
            self.mw.pay_wt_inplab.setText(QString.number(self.req1.payload_wt))
         elif wt == "":
            pass
         else:
             input_warn = QtGui.QMessageBox()
             input_warn.setText("Please enter a number"+" in "+self.mw.cargo_lab.text())
             input_warn.exec_()

    @pyqtSlot()
    def engine_inp(self, num):
        if self.isdigit(num):
            self.aircraft1.prop.engines_num = int(num)
        elif num == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.engine_lab.text())
            input_warn.exec_()

    # Mission Tab
    @pyqtSlot()
    def miss_nam_inp(self, text):
        self.mission1.name = text

    @pyqtSlot()
    def alt_beg_inp(self, alt):
        if self.isfloat(alt):
            if self.mw.alt_beg_seg_m_comb.currentText() == "m":
                self.mission1.segments[self.counter].y_pos_start = float(alt)
            else:
                self.mission1.segments[self.counter].y_pos_start = float(alt)/data.Conversion.M_2_FT
        elif alt == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.alt_beg_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def rang_seg_inp(self, dist):
        if self.isfloat(dist):
            if self.mw.rang_seg_m_comb.currentText() == "m":
                self.mission1.segments[self.counter].range = float(dist)
            elif self.mw.rang_seg_m_comb.currentText() == "ft":
                self.mission1.segments[self.counter].range = float(dist)/data.Conversion.M_2_FT
            else:
                self.mission1.segments[self.counter].range = float(dist)*data.Conversion.KM_2_M
        elif dist == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.rang_seg_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def ht_seg_inp(self, ht):
        if self.isfloat(ht):
            if self.mw.ht_seg_m_comb.currentText() == "m":
                self.mission1.segments[self.counter].height = float(ht)
            elif self.mw.ht_seg_m_comb.currentText() == "ft":
                self.mission1.segments[self.counter].height = float(ht)/data.Conversion.M_2_FT
            else:
                self.mission1.segments[self.counter].height = float(ht)*data.Conversion.KM_2_M
        elif ht == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.ht_seg_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def time_seg_inp(self, t):
        if self.isfloat(t):
            if self.mw.time_seg_hr_comb.currentText() == "hr":
                self.mission1.segments[self.counter].time = float(t)
            else:
                self.mission1.segments[self.counter].time = float(t)/data.Conversion.HR_2_MIN
        elif t == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number"+" in "+self.mw.time_seg_lab.text())
            input_warn.exec_()

    @pyqtSlot()
    def typ_seg_comb(self, segment):
        if segment == "Takeoff":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Climb":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Cruise":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Loiter":
            self.mw.rang_seg_inp.setDisabled(True)
            self.mw.ht_seg_inp.setDisabled(True)
            self.mw.time_seg_inp.setDisabled(False)
        elif segment == "Descent":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
        elif segment == "Landing":
            self.mw.rang_seg_inp.setDisabled(False)
            self.mw.ht_seg_inp.setDisabled(False)
            self.mw.time_seg_inp.setDisabled(True)
    # Unit conversion Slots
    # ========****=========

    # Requirements Tab
    @pyqtSlot()
    def set_req_push(self):
        self.req1.regulation = self.mw.reg_comb.currentText()
        print "Before"
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        self.constraint_plots = []
        self.plot_constraints()

        self.design_space()
        self.mw.tabWidget.setCurrentIndex(1)

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

    @pyqtSlot()
    def roc_mpers_comb(self, speed):
        if speed == "ft/min":
            g = self.req1.roc*data.Conversion.MPERS_2_FTPERMIN
            self.mw.roc_inp.setText(QString.number(g))
        else:
            self.mw.roc_inp.setText(QString.number(self.req1.roc))

    @pyqtSlot()
    def tod_lan_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.to_distance_land*data.Conversion.M_2_FT
            self.mw.tod_land_inp.setText(QString.number(g))
        else:
            self.mw.tod_land_inp.setText(QString.number(self.req1.to_distance_land))

    @pyqtSlot()
    def tod_water_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.to_distance_water*data.Conversion.M_2_FT
            self.mw.tod_water_inp.setText(QString.number(g))
        else:
            self.mw.tod_water_inp.setText(QString.number(self.req1.to_distance_water))

    @pyqtSlot()
    def lan_land_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.la_distance_land*data.Conversion.M_2_FT
            self.mw.lan_land_inp.setText(QString.number(g))
        else:
            self.mw.lan_land_inp.setText(QString.number(self.req1.la_distance_land))

    @pyqtSlot()
    def lan_water_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.la_distance_water*data.Conversion.M_2_FT
            self.mw.lan_water_inp.setText(QString.number(g))
        else:
            self.mw.lan_water_inp.setText(QString.number(self.req1.la_distance_water))

    @pyqtSlot()
    def max_run_alt_m_comb(self, dist):
        if dist == "ft":
            g = self.req1.max_run_alt*data.Conversion.M_2_FT
            self.mw.max_run_alt_inp.setText(QString.number(g))
        else:
            self.mw.max_run_alt_inp.setText(QString.number(self.req1.max_run_alt))

    @pyqtSlot()
    def inst_degpers_comb(self, rate):
        if rate == "rad/s":
            g = self.req1.inst_turn*data.Conversion.DEG_2_RAD
            self.mw.inst_inp.setText(QString.number(g))
        else:
            self.mw.inst_inp.setText(QString.number(self.req1.inst_turn))

    @pyqtSlot()
    def sus_degpers_comb(self, rate):
        if rate == "rad/s":
            g = self.req1.sus_turn*data.Conversion.DEG_2_RAD
            self.mw.sus_inp.setText(QString.number(g))
        else:
            self.mw.sus_inp.setText(QString.number(self.req1.sus_turn))

    @pyqtSlot()
    def bank_ang_comb(self, ang):
        if ang == "rad":
            g = self.req1.bank_ang*data.Conversion.DEG_2_RAD
            self.mw.bank_ang_inp.setText(QString.number(g))
        else:
            self.mw.bank_ang_inp.setText(QString.number(self.req1.bank_ang))

    @pyqtSlot()
    def fuel_res_km_comb(self, dist):
        if dist == "mi":
            g = self.req1.fuel_res_rang*data.Conversion.KM_2_MI
            self.mw.fuel_res_inp.setText(QString.number(g))
        elif dist == "km":
            self.mw.fuel_res_inp.setText(QString.number(self.req1.fuel_res_rang))
        else:
            g = self.req1.fuel_res_rang*data.Conversion.KM_2_NM
            self.mw.fuel_res_inp.setText(QString.number(g))

    @pyqtSlot()
    def cargo_kg_comb(self, wt):
         if wt == "lb":
            g = self.req1.cargo_wt/data.Conversion.LB_2_KG
            self.mw.cargo_inp.setText(QString.number(g))
         else:
            self.mw.cargo_inp.setText(QString.number(self.req1.cargo_wt))
    # Mission Tab

    @pyqtSlot()
    def alt_beg_seg_m_comb(self, dist):
        if dist == "ft":
            g = self.mission1.segments[0].y_pos_start*data.Conversion.M_2_FT
            self.mw.alt_beg_inp.setText(QString.number(g))
        else:
            self.mw.alt_beg_inp.setText(QString.number(self.mission1.segments[0].y_pos_start))

    @pyqtSlot()
    def rang_seg_m_comb(self, dist):
        if dist == "ft":
            g = self.mission1.segments[self.counter].range*data.Conversion.M_2_FT
            self.mw.rang_seg_inp.setText(QString.number(g))
        elif dist == "km":
            g = self.mission1.segments[self.counter].range/data.Conversion.KM_2_M
            self.mw.rang_seg_inp.setText(QString.number(g))
        else:
            self.mw.rang_seg_inp.setText(QString.number(self.mission1.segments[self.counter].range))

    @pyqtSlot()
    def ht_seg_m_comb(self, ht):
        if ht == "ft":
            g = self.mission1.segments[self.counter].height*data.Conversion.M_2_FT
            self.mw.ht_seg_inp.setText(QString.number(g))
        elif ht == "m":
            self.mw.ht_seg_inp.setText(QString.number(self.mission1.segments[self.counter].height))
        else:
            g = self.mission1.segments[self.counter].height/data.Conversion.KM_2_M
            self.mw.ht_seg_inp.setText(QString.number(g))

    @pyqtSlot()
    def time_seg_hr_comb(self, t):
        if t == "hr":
            self.mw.time_seg_inp.setText(QString.number(self.mission1.segments[self.counter].time))
        else:
            g = self.mission1.segments[self.counter].time*data.Conversion.HR_2_MIN
            self.mw.time_seg_inp.setText(QString.number(g))

    # Gross Weight Visualisation Slots

    @pyqtSlot()
    def pass_w_gross(self,pos):
        init_pass = self.req1.pass_num
        init_gross = self.aircraft1.gross_weight
        self.req1.pass_num = pos
        analysis.class1_estimation(self.req1, self.aircraft1, self.mission1)

        self.mw.ds_gross_out.setText(QString.number(self.aircraft1.gross_weight))
        self.mw.current_pass_num.setText(QString.number(pos))

        #reset values
        self.req1.pass_num = init_pass
        self.aircraft1.gross_weight = init_gross

    @pyqtSlot()
    def cargo_w_gross(self,pos):
        init_cargo = self.req1.cargo_wt
        init_gross = self.aircraft1.gross_weight
        self.req1.cargo_wt = pos
        analysis.class1_estimation(self.req1, self.aircraft1, self.mission1)

        self.mw.ds_gross_out.setText(QString.number(self.aircraft1.gross_weight))
        self.mw.current_cargo_wt.setText(QString.number(pos))

        #reset values
        self.req1.cargo_wt = init_cargo
        self.aircraft1.gross_weight = init_gross


    # Assisting Functions


    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def isdigit(self,value):
        try:
            int(value)
            return True
        except ValueError:
            return False


    # Graph for constraint analysis




