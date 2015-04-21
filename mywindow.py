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
import time

from gui import Window3, airfoil


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
        self.show()

    def update_gui(self):
        self.requirements()
        self.mission()
        self.design_space()
        self.fuse_config()
        self.wing_stab()

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


        #Push buttons
        # self.connect(self.mw.add_data_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.add_data_push)
        self.connect(self.mw.set_req_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.set_req_push)

    def mission(self):
        self.miss_set_defaults()
        self.miss_segments()
        self.miss_unit_conversions()
        self.miss_data_inputs()
        self.mission_profile()
        self.connect(self.mw.add_seg_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add_seg_push)
        self.connect(self.mw.rem_seg_push, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rem_seg_push)

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
    def graph_design_point(self,val):
        print val

    def setup_graph_controls(self):
        self.mw.sscg_check.setCheckState(2)
        self.mw.missedapp_check.setCheckState(2)
        self.mw.landing_check.setCheckState(2)
        self.mw.roc_check.setCheckState(2)
        self.mw.stall_check.setCheckState(2)
        self.mw.takeoff_check.setCheckState(2)
        self.mw.min_mach_check.setCheckState(2)
        self.mw.turn_rate_check.setCheckState(2)

        # Checkboxes
        self.connect(self.mw.roc_isa_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.roc_isa_sb)
        self.connect(self.mw.run_isa_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.run_isa_sb)

        # Roc slider
        roc_curr = self.req1.roc
        roc_min = roc_curr - 4.0
        roc_max = roc_curr + 4.0

        self.mw.roc_slider.setMinimum(roc_min*10)
        self.mw.roc_slider.setMaximum(roc_max*10)
        self.mw.roc_slider.setValue(roc_curr*10)
        self.mw.roc_max_lab.setText(str(roc_max))
        self.mw.roc_min_lab.setText(str(roc_min))
        self.mw.roc_current_out.setText(str(roc_curr))

        #Landing Slider
        land_curr = self.req1.la_distance_land
        land_min = land_curr - 200
        land_max = land_curr + 200

        self.mw.landing_slider.setMinimum(land_min)
        self.mw.landing_slider.setMaximum(land_max)
        self.mw.landing_slider.setValue(land_curr)
        self.mw.landing_max_lab.setText(QString.number(land_max))
        self.mw.landing_min_lab.setText(QString.number(land_min))
        self.mw.landing_current_out.setText(QString.number(land_curr))

        #Takeoff Slider
        takeoff_curr = self.req1.to_distance_land
        takeoff_min = takeoff_curr - 200
        takeoff_max = takeoff_curr + 200

        self.mw.takeoff_slider.setMinimum(takeoff_min)
        self.mw.takeoff_slider.setMaximum(takeoff_max)
        self.mw.takeoff_slider.setValue(takeoff_curr)
        self.mw.takeoff_max_lab.setText(QString.number(takeoff_max))
        self.mw.takeoff_min_lab.setText(QString.number(takeoff_min))
        self.mw.takeoff_current_out.setText(QString.number(takeoff_curr))

        #Stall Velocity
        stall_curr = self.req1.la_distance_land
        stall_min = stall_curr - 200
        stall_max = stall_curr + 200

        self.mw.stall_slider.setMinimum(stall_min)
        self.mw.stall_slider.setMaximum(stall_max)
        self.mw.stall_slider.setValue(stall_curr)
        self.mw.stall_max_lab.setText(QString.number(stall_max))
        self.mw.stall_min_lab.setText(QString.number(stall_min))
        self.mw.stall_current_out.setText(QString.number(stall_curr))

    def design_space(self):

        # Class I weight Estimation
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

        #Push Button
        self.connect(self.mw.set_refined_req_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.set_refined_req_push)

        # Temporarily
        self.aircraft1.t_by_w = 0.48
        self.aircraft1.w_by_s = 160
        self.mw.thrust_loading_out.setText(str(self.aircraft1.t_by_w))
        self.mw.wing_loading_out.setText(str(self.aircraft1.w_by_s))
        self.graph_controls()

    def fuse_config(self):
        self.fuse_set_defaults()

        self.connect(self.mw.cabin_type_comb, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.cabin_type_comb)
        self.connect(self.mw.class_num_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.class_num_sb)

        self.connect(self.mw.avg_seats1_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.avg_seats1_sb)
        self.connect(self.mw.avg_seats2_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.avg_seats2_sb)
        self.connect(self.mw.avg_seats3_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.avg_seats3_sb)

        self.connect(self.mw.aisles1_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.aisles1_sb)
        self.connect(self.mw.aisles2_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.aisles2_sb)
        self.connect(self.mw.aisles3_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.aisles3_sb)

        self.connect(self.mw.seats_num1_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.seats_num1_inp)
        self.connect(self.mw.seats_num2_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.seats_num2_inp)
        self.connect(self.mw.seats_num3_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.seats_num3_inp)

        self.connect(self.mw.seat_pitch_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.seat_pitch_m_comb)
        self.connect(self.mw.seat_pitch1_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.seat_pitch1_inp)
        self.connect(self.mw.seat_pitch2_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.seat_pitch2_inp)
        self.connect(self.mw.seat_pitch3_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.seat_pitch3_inp)

        self.connect(self.mw.lav1_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lav1_sb)
        self.connect(self.mw.lav2_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lav2_sb)
        self.connect(self.mw.lav3_sb, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lav3_sb)

        self.connect(self.mw.gall1_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.gall1_check)
        self.connect(self.mw.gall2_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.gall2_check)
        self.connect(self.mw.gall3_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.gall3_check)

        self.connect(self.mw.lower_deck_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.lower_deck_comb)
        self.connect(self.mw.double_cont_check,QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.double_cont_check)

        self.connect(self.mw.cargo_length_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cargo_length_inp)
        self.connect(self.mw.cargo_width_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cargo_width_inp)
        self.connect(self.mw.cargo_height_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.cargo_height_inp)

        # Cross-section
        self.connect(self.mw.floor_lowering_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.floor_lowering_inp)
        self.connect(self.mw.floor_thickness_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.floor_thickness_inp)
        self.connect(self.mw.cabin_ratio_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.cabin_ratio_slider)

        # Fuselage Length
        self.connect(self.mw.nose_length2diameter_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.nose_length2diameter_inp)
        self.connect(self.mw.nose_offset_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.nose_offset_inp)
        self.connect(self.mw.tail_length2diameter_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.tail_length2diameter_inp)
        self.connect(self.mw.tail_offset2diameter_inp, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.tail_offset2diameter_inp)

        # Unit Conversions
        self.connect(self.mw.nose_offset_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.nose_offset_m_comb)

        self.connect(self.mw.nose_offset_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.nose_offset_m_comb)
        self.connect(self.mw.cabin_length_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.cabin_length_m_comb)
        self.connect(self.mw.fuse_length_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.fuse_length_m_comb)

        # Push Button
        self.connect(self.mw.set_fuse_param_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.set_fuse_param_push)

    def fuse_set_defaults(self):
        self.mw.seat_pitch1_inp.setText(QString.number(self.aircraft1.fuse.cabin.seat_pitch[0]))
        self.mw.seat_pitch2_inp.setText(QString.number(self.aircraft1.fuse.cabin.seat_pitch[1]))
        self.mw.seat_pitch3_inp.setText(QString.number(self.aircraft1.fuse.cabin.seat_pitch[2]))
        self.mw.cabin_ratio_slider.setMinimum(70)
        self.mw.cabin_ratio_slider.setMaximum(130)
        self.mw.cabin_ratio_slider.setValue(100)

        self.mw.cabin_ratio_min_lab.setText(str(70/100.0))
        self.mw.cabin_ratio_max_lab.setText(str(130/100.0))
        self.mw.cabin_ratio_out.setText(str(100/100.0))
        self.fuse_cs_out_update()
        analysis.cabin_length_sizing(self.aircraft1)
        self.mw.nose_length2diameter_inp.setText(str(self.aircraft1.fuse.nose_length2dia))
        self.mw.nose_offset_inp.setText(str(self.aircraft1.fuse.nose_offset))
        self.mw.tail_length2diameter_inp.setText(str(self.aircraft1.fuse.tail_length2dia))
        self.mw.tail_offset2diameter_inp.setText(str(self.aircraft1.fuse.tail_offset2dia))
        self.mw.cabin_length_out.setText(str(self.aircraft1.fuse.cabin.length))
        self.aircraft1.fuse.update_fuse_length()
        self.mw.fuse_length_out.setText(str(self.aircraft1.fuse.length))

    def fuse_cs_out_update(self):
        analysis.cabin_cs_sizing(self.aircraft1)
        n = round(self.aircraft1.fuse.cabin.floor_lowering,2)
        t = str(n)
        self.mw.floor_lowering_inp.setText(t)
        n = round(self.aircraft1.fuse.cabin.inner_height,2)
        t = str(n)
        self.mw.inner_height_out.setText(t)
        n = round(self.aircraft1.fuse.cabin.inner_width,2)
        t = str(n)
        self.mw.inner_width_out.setText(t)
        n = round(self.aircraft1.fuse.cabin.inner_eq_dia,2)
        t = str(n)
        self.mw.inner_eq_diameter_out.setText(t)
        n = round(self.aircraft1.fuse.cabin.fuselage_thickness,2)
        t = str(n)
        self.mw.fuse_thickness_out.setText(t)
        n = round(self.aircraft1.fuse.cabin.outer_eq_dia,2)
        t = str(n)
        self.mw.outer_eq_diameter_out.setText(t)
        n = round(self.aircraft1.fuse.cabin.floor_thickness,2)
        t = str(n)
        self.mw.floor_thickness_inp.setText(t)
        n = round(self.aircraft1.fuse.cabin.outer_height,2)
        t = str(n)
        self.mw.outer_height_out.setText(t)
        n = round(self.aircraft1.fuse.cabin.outer_width,2)
        t = str(n)
        self.mw.outer_width_out.setText(t)

    def fuse_length_out_update(self):
        analysis.cabin_length_sizing(self.aircraft1)
        self.mw.cabin_length_out.setText(str(self.aircraft1.fuse.cabin.length))
        self.aircraft1.fuse.update_fuse_length()
        self.aircraft1.cg_location = self.aircraft1.fuse.length/2
        self.mw.fuse_length_out.setText(str(self.aircraft1.fuse.length))

    def wing_stab(self):
        self.wing_stab_set_defaults()
        # Add airfoil push buttons
        self.connect(self.mw.root_airfoil_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.root_airfoil_push)
        self.connect(self.mw.tip_airfoil_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.tip_airfoil_push)

        self.connect(self.mw.wing_aspect_ratio_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.wing_aspect_ratio_inp)
        self.connect(self.mw.wing_taper_ratio_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.wing_taper_ratio_inp)
        self.connect(self.mw.wing_sweep_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.wing_sweep_inp)
        self.connect(self.mw.wing_dihedral_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.wing_dihedral_inp)

        # Wing Sliders
        d_min = -50
        d_max = 50
        d_curr = 0

        self.mw.wing_dist_CG_slider.setMinimum(d_min)
        self.mw.wing_dist_CG_slider.setMaximum(d_max)
        self.mw.wing_dist_CG_slider.setValue(d_curr)
        self.mw.wing_dist_CG_min_lab.setText(str(d_min/10.0))
        self.mw.wing_dist_CG_max_lab.setText(str(d_max/10.0))
        self.mw.wing_dist_CG_out.setText(str(d_curr/10.0))

        self.connect(self.mw.wing_dist_CG_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.wing_dist_CG_slider)
        self.connect(self.mw.flap_type_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")),self.flap_type_comb)

        # Unit Conversions
        self.connect(self.mw.planform_area_sqm_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.planform_area_sqm_comb)
        self.connect(self.mw.wingspan_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.wingspan_m_comb)
        self.connect(self.mw.wing_chord_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.wing_chord_m_comb)
        self.connect(self.mw.wing_dihedral_deg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.wing_dihedral_deg_comb)
        self.connect(self.mw.wing_sweep_deg_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.wing_sweep_deg_comb)
        self.connect(self.mw.wing_dist_CG_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.wing_dist_CG_m_comb)

        # Vertical Stabilizer
        self.connect(self.mw.vert_aspect_ratio_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.vert_aspect_ratio_inp)
        self.connect(self.mw.vert_taper_ratio_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.vert_taper_ratio_inp)
        self.connect(self.mw.vert_span_inp,QtCore.SIGNAL(_fromUtf8("textChanged(QString)")),self.vert_span_inp)

        #Vert Unit Conversion
        self.connect(self.mw.vert_area_sqm_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.vert_area_sqm_comb)
        self.connect(self.mw.vert_span_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.vert_span_m_comb)
        self.connect(self.mw.vert_chord_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.vert_chord_m_comb)
        self.connect(self.mw.vert_long_dist_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.vert_long_dist_m_comb)
        self.connect(self.mw.vert_lat_dist_m_comb,QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.vert_lat_dist_m_comb)

        # Vertical Sliders
        d_min = -1*self.aircraft1.cg_location*10
        d_max = (self.aircraft1.fuse.length-self.aircraft1.cg_location)*10
        d_curr = d_max

        self.mw.vert_long_dist_slider.setMinimum(d_min)
        self.mw.vert_long_dist_slider.setMaximum(d_max)
        self.mw.vert_long_dist_slider.setValue(d_curr)
        self.mw.vert_long_dist_min_lab.setText(str(d_min/10.0))
        self.mw.vert_long_dist_max_lab.setText(str(d_max/10.0))
        self.mw.vert_long_dist_out.setText(str(d_curr/10.0))

        self.connect(self.mw.vert_long_dist_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.vert_long_dist_slider)

        d_min = (-0.5)*self.aircraft1.wing.span*10
        d_max = 0.5*self.aircraft1.wing.span*10
        d_curr = 0

        self.mw.vert_lat_dist_slider.setMinimum(d_min)
        self.mw.vert_lat_dist_slider.setMaximum(d_max)
        self.mw.vert_lat_dist_slider.setValue(d_curr)
        self.mw.vert_lat_dist_min_lab.setText(str(d_min/10.0))
        self.mw.vert_lat_dist_max_lab.setText(str(d_max/10.0))
        self.mw.vert_lat_dist_out.setText(str(d_curr/10.0))

        self.connect(self.mw.vert_lat_dist_slider,QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.vert_lat_dist_slider)
        # Vertical Push
        self.connect(self.mw.vert_airfoil_push,QtCore.SIGNAL(_fromUtf8("clicked()")),self.vert_airfoil_push)
        # Other Support
        self.vert_surface_added = []
        self.horiz_surface_added = []
        for i in range((self.aircraft1.stab.vt_num+1)):
            self.vert_surface_added.append(0)
        for i in range((self.aircraft1.stab.ht_num)+1):
            self.horiz_surface_added.append(0)

    @pyqtSlot()
    def vert_long_dist_slider(self,val):
        dist = val/10.0
        j = self.mw.vert_surface_comb.currentIndex()
        self.aircraft1.stab.vt[j].long_dist_CG = dist
        if self.mw.vert_long_dist_m_comb.currentText() == "m":
            self.mw.vert_long_dist_out.setText(str(dist))
        else:
            self.mw.vert_long_dist_out.setText(str(dist*data.Conversion.M_2_FT))

    @pyqtSlot()
    def vert_lat_dist_slider(self,val):
        dist = val/10.0
        j = self.mw.vert_surface_comb.currentIndex()
        self.aircraft1.stab.vt[j].lat_dist_CG = dist
        if self.mw.vert_lat_dist_m_comb.currentText() == "m":
            self.mw.vert_lat_dist_out.setText(str(dist))
        else:
            self.mw.vert_lat_dist_out.setText(str(dist*data.Conversion.M_2_FT))


    @pyqtSlot()
    def vert_aspect_ratio_inp(self,text):
        if self.isfloat(text):
            j = self.mw.vert_surface_comb.currentIndex()
            self.aircraft1.stab.vt[j].a_r = float(text)
            self.aircraft1.stab.vt[j].calc_area()
            self.aircraft1.stab.vt[j].calc_chord()
            self.vert_surface_out()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def vert_taper_ratio_inp(self,text):
        if self.isfloat(text):
            j = self.mw.vert_surface_comb.currentIndex()
            self.aircraft1.stab.vt[j].t_r = float(text)
            self.aircraft1.stab.vt[j].calc_area()
            self.aircraft1.stab.vt[j].calc_chord()
            self.vert_surface_out()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def vert_span_inp(self,text):
        if self.isfloat(text):
            j = self.mw.vert_surface_comb.currentIndex()
            self.aircraft1.stab.vt[j].span = float(text)
            self.aircraft1.stab.vt[j].calc_area()
            self.aircraft1.stab.vt[j].calc_chord()
            self.vert_surface_out()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def vert_area_sqm_comb(self,val):
        j = self.mw.vert_surface_comb.currentIndex()
        if val =="sq. m":
            self.mw.vert_area_out.setText(str(self.aircraft1.stab.vt[j].ref_area))
        else:
            t = self.aircraft1.stab.vt[j].ref_area*math.pow(data.Conversion.M_2_FT,2)
            self.mw.vert_area_out.setText(str(t))

    @pyqtSlot()
    def vert_span_m_comb(self,val):
        j = self.mw.vert_surface_comb.currentIndex()
        if val == "m":
            t = self.aircraft1.stab.vt[j].span
            self.mw.vert_span_inp.setText(str(t))
        else:
            t = self.aircraft1.stab.vt[j].span*data.Conversion.M_2_FT
            self.mw.vert_span_inp.setText(str(t))

    @pyqtSlot()
    def vert_chord_m_comb(self,val):
        j = self.mw.vert_surface_comb.currentIndex()
        if val == "m":
            self.mw.vert_chord_out.setText(str(self.aircraft1.stab.vt[j].mean_chord))
        else:
            self.mw.vert_chord_out.setText(str(self.aircraft1.stab.vt[j].mean_chord*data.Conversion.M_2_FT))

    @pyqtSlot()
    def vert_long_dist_m_comb(self,val):
        j = self.mw.vert_surface_comb.currentIndex()
        if val == "m":
            self.mw.vert_long_dist_out.setText(str(self.aircraft1.stab.vt[j].long_dist_CG))
            self.mw.vert_long_dist_min_lab.setText(str(self.mw.vert_long_dist_slider.minimum()/10.0))
            self.mw.vert_long_dist_max_lab.setText(str(self.mw.vert_long_dist_slider.maximum()/10.0))
        else:
            t = round(self.aircraft1.stab.vt[j].long_dist_CG*data.Conversion.M_2_FT,2)
            self.mw.vert_long_dist_out.setText(str(t))
            t = round((self.mw.vert_long_dist_slider.minimum()*data.Conversion.M_2_FT/10.0),2)
            self.mw.vert_long_dist_min_lab.setText(str(t))
            t = round((self.mw.vert_long_dist_slider.maximum()*data.Conversion.M_2_FT/10.0),2)
            self.mw.vert_long_dist_max_lab.setText(str(t))

    @pyqtSlot()
    def vert_lat_dist_m_comb(self,val):
        j = self.mw.vert_surface_comb.currentIndex()
        if val == "m":
            self.mw.vert_lat_dist_out.setText(str(self.aircraft1.stab.vt[j].lat_dist_CG))
            self.mw.vert_lat_dist_min_lab.setText(str(self.mw.vert_lat_dist_slider.minimum()/10.0))
            self.mw.vert_lat_dist_max_lab.setText(str(self.mw.vert_lat_dist_slider.maximum()/10.0))
        else:
            t = round(self.aircraft1.stab.vt[j].lat_dist_CG*data.Conversion.M_2_FT,2)
            self.mw.vert_lat_dist_out.setText(str(t))
            t = round((self.mw.vert_lat_dist_slider.minimum()*data.Conversion.M_2_FT/10.0),2)
            self.mw.vert_lat_dist_min_lab.setText(str(t))
            t = round((self.mw.vert_lat_dist_slider.maximum()*data.Conversion.M_2_FT/10.0),2)
            self.mw.vert_lat_dist_max_lab.setText(str(t))


    @pyqtSlot()
    def flap_type_comb(self,val):
        if self.wing_added == 1:
            self.mw.update_wing_push.setEnabled(True)
        self.aircraft1.wing.flap.type = val
        self.aircraft1.wing.flap.flap_factor = data.Historic_param.Wing.flap_factor(val)

    @pyqtSlot()
    def wing_dist_CG_slider(self,val):
        if self.wing_added == 1:
            self.mw.update_wing_push.setEnabled(True)
        dist = val/10.0
        self.aircraft1.wing.dist_CG = dist
        if self.mw.wing_dist_CG_m_comb.currentText() == "m":
            self.mw.wing_dist_CG_out.setText(str(dist))
        else:
            t = round(dist*data.Conversion.M_2_FT,2)
            self.mw.wing_dist_CG_out.setText(str(t))

    @pyqtSlot()
    def wing_sweep_inp(self,text):
         if self.isfloat(text):
            if self.wing_added == 1:
                self.mw.update_wing_push.setEnabled(True)
            if self.mw.wing_sweep_deg_comb == "deg":
                self.aircraft1.wing.sweep_le = float(text)
            else:
                self.aircraft1.wing.sweep_le = float(text)/data.Conversion.DEG_2_RAD
            self.aircraft1.wing.calc_sweep()
            self.aircraft1.wing.calc_e()
            self.wing_out()
         elif text == "":
            pass
         else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def wing_dihedral_inp(self,text):
         if self.isfloat(text):
            if self.wing_added == 1:
                self.mw.update_wing_push.setEnabled(True)
            if self.mw.wing_dihedral_deg_comb == "deg":
                self.aircraft1.wing.dihedral = float(text)
            else:
                self.aircraft1.wing.dihedral = float(text)/data.Conversion.DEG_2_RAD
         elif text == "":
            pass
         else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def wing_aspect_ratio_inp(self,text):
        if self.isfloat(text):
            if self.wing_added == 1:
                self.mw.update_wing_push.setEnabled(True)
            self.aircraft1.wing.a_r = float(text)
            self.aircraft1.wing.calc_span()
            self.aircraft1.wing.calc_chord()
            self.aircraft1.wing.calc_sweep()
            self.aircraft1.wing.calc_e()
            self.wing_out()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def wing_taper_ratio_inp(self,text):
        if self.isfloat(text):
            if self.wing_added == 1:
                self.mw.update_wing_push.setEnabled(True)
            self.aircraft1.wing.t_r = float(text)
            self.aircraft1.wing.calc_span()
            self.aircraft1.wing.calc_chord()
            self.aircraft1.wing.calc_sweep()
            self.aircraft1.wing.calc_e()
            self.wing_out()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def root_airfoil_push(self):
        root = AirfoilDialog()
        result = root.exec_()
        if result == 1:
            if self.wing_added == 1:
                self.mw.update_wing_push.setEnabled(True)
            root_airfoil = self.aircraft1.wing.root_airfoil
            root_airfoil.max_thickness = float(root.ad.dialog_max_thick_inp.text())
            root_airfoil.max_thick_loc = float(root.ad.dialog_thick_loc_inp.text())
            root_airfoil.max_cl = float(root.ad.dialog_cl_max_inp.text())
            root_airfoil.max_cl_alpha = root.ad.dialog_clmax_alpha_sb.value()
            root_airfoil.cruise_cl = float(root.ad.dialog_clcr_inp.text())
            root_airfoil.cruise_cl_alpha = root.ad.dialog_cl_cr_alpha_sb.value()
            root_airfoil.cd0 = float(root.ad.dialog_cdo_inp.text())
            root_airfoil.max_clbycd = float(root.ad.dialog_max_clcd_inp.text())
            root_airfoil.max_clbycd_alpha = root.ad.dialog_max_clcd_alpha_sb.value
        root.show()

    @pyqtSlot()
    def tip_airfoil_push(self):
        tip = AirfoilDialog()
        result = tip.exec_()
        if result == 1:
            if self.wing_added == 1:
                self.mw.update_wing_push.setEnabled(True)
            tip_airfoil = self.aircraft1.wing.tip_airfoil
            tip_airfoil.max_thickness = float(tip.ad.dialog_max_thick_inp.text())
            tip_airfoil.max_thick_loc = float(tip.ad.dialog_thick_loc_inp.text())
            tip_airfoil.max_cl = float(tip.ad.dialog_cl_max_inp.text())
            tip_airfoil.max_cl_alpha = tip.ad.dialog_clmax_alpha_sb.value()
            tip_airfoil.cruise_cl = float(tip.ad.dialog_clcr_inp.text())
            tip_airfoil.cruise_cl_alpha = tip.ad.dialog_cl_cr_alpha_sb.value()
            tip_airfoil.cd0 = float(tip.ad.dialog_cdo_inp.text())
            tip_airfoil.max_clbycd = float(tip.ad.dialog_max_clcd_inp.text())
            tip_airfoil.max_clbycd_alpha = tip.ad.dialog_max_clcd_alpha_sb.value
        tip.show()

    @pyqtSlot()
    def vert_airfoil_push(self):
        vert = AirfoilDialog()
        result = vert.exec_()
        if result == 1:
            # if self.wing_added == 1:
            #     self.mw.update_wing_push.setEnabled(True)
            j = self.mw.vert_surface_comb.currentIndex()
            vert_airfoil = self.aircraft1.stab.vt[j].airfoil

            vert_airfoil.max_thickness = float(vert.ad.dialog_max_thick_inp.text())
            vert_airfoil.max_thick_loc = float(vert.ad.dialog_thick_loc_inp.text())
            vert_airfoil.max_cl = float(vert.ad.dialog_cl_max_inp.text())
            vert_airfoil.max_cl_alpha = vert.ad.dialog_clmax_alpha_sb.value()
            vert_airfoil.cruise_cl = float(vert.ad.dialog_clcr_inp.text())
            vert_airfoil.cruise_cl_alpha = vert.ad.dialog_cl_cr_alpha_sb.value()
            vert_airfoil.cd0 = float(vert.ad.dialog_cdo_inp.text())
            vert_airfoil.max_clbycd = float(vert.ad.dialog_max_clcd_inp.text())
            vert_airfoil.max_clbycd_alpha = vert.ad.dialog_max_clcd_alpha_sb.value
        vert.show()

    @pyqtSlot()
    def planform_area_sqm_comb(self,val):
        if val =="sq. m":
            self.mw.planform_area_out.setText(str(self.aircraft1.wing.ref_area))
        else:
            t = self.aircraft1.wing.ref_area*math.pow(data.Conversion.M_2_FT,2)
            self.mw.planform_area_out.setText(str(t))

    @pyqtSlot()
    def wingspan_m_comb(self,val):
        if val == "m":
            t = self.aircraft1.wing.span
            self.mw.wingspan_out.setText(str(t))
        else:
            t = self.aircraft1.wing.span*data.Conversion.M_2_FT
            self.mw.wingspan_out.setText(str(t))

    @pyqtSlot()
    def wing_chord_m_comb(self,val):
        if val == "m":
            self.mw.wing_chord_out.setText(str(self.aircraft1.wing.mean_chord))
        else:
            self.mw.wing_chord_out.setText(str(self.aircraft1.wing.mean_chord*data.Conversion.M_2_FT))

    @pyqtSlot()
    def wing_dist_CG_m_comb(self,val):
        if val == "m":
            self.mw.wing_dist_CG_out.setText(str(self.aircraft1.wing.dist_CG))
            self.mw.wing_dist_CG_min_lab.setText(str(self.mw.wing_dist_CG_slider.minimum()/10.0))
            self.mw.wing_dist_CG_max_lab.setText(str(self.mw.wing_dist_CG_slider.maximum()/10.0))
        else:
            t = round(self.aircraft1.wing.dist_CG*data.Conversion.M_2_FT,2)
            self.mw.wing_dist_CG_out.setText(str(t))
            t = round((self.mw.wing_dist_CG_slider.minimum()*data.Conversion.M_2_FT/10.0),2)
            self.mw.wing_dist_CG_min_lab.setText(str(t))
            t = round((self.mw.wing_dist_CG_slider.maximum()*data.Conversion.M_2_FT/10.0),2)
            self.mw.wing_dist_CG_max_lab.setText(str(t))

    @pyqtSlot()
    def wing_dihedral_deg_comb(self,val):
        if val == "deg":
            self.mw.wing_dihedral_inp.setText(str(self.aircraft1.wing.dihedral))
        else:
            self.mw.wing_dihedral_inp.setText(str(self.aircraft1.wing.dihedral*data.Conversion.DEG_2_RAD))

    @pyqtSlot()
    def wing_sweep_deg_comb(self,val):
        if val == "deg":
            self.mw.wing_sweep_inp.setText(str(self.aircraft1.wing.sweep_le))
        else:
            self.mw.wing_sweep_inp.setText(str(self.aircraft1.wing.sweep_le*data.Conversion.DEG_2_RAD))

    def wing_stab_set_defaults(self):
        # Wing Defaults
        self.aircraft1.wing.calc_ref_area(self.aircraft1)
        self.mw.planform_area_out.setText(str(self.aircraft1.wing.ref_area))
        self.mw.wing_aspect_ratio_inp.setText(str(self.aircraft1.wing.a_r))
        self.mw.wing_taper_ratio_inp.setText(str(self.aircraft1.wing.t_r))
        self.mw.wing_dihedral_inp.setText(str(self.aircraft1.wing.dihedral))
        self.mw.wing_sweep_inp.setText(str(self.aircraft1.wing.sweep_le))
        self.wing_out()

        # Vertical Stab
        self.mw.vert_aspect_ratio_inp.setText(str(self.aircraft1.stab.vt[0].a_r))
        self.mw.vert_taper_ratio_inp.setText(str(self.aircraft1.stab.vt[0].t_r))
        self.mw.vert_span_inp.setText(str(self.aircraft1.stab.vt[0].span))
        self.mw.vert_chord_out.setText(str(self.aircraft1.stab.vt[0].mean_chord))
        self.mw.vert_area_out.setText(str(self.aircraft1.stab.vt[0].ref_area))


    def wing_out(self):
        if self.mw.wingspan_m_comb.currentText() == "m":
            t = round(self.aircraft1.wing.span,2)
            self.mw.wingspan_out.setText(str(t))
        else:
            t = round(self.aircraft1.wing.span*data.Conversion.M_2_FT,2)
            self.mw.wingspan_out.setText(str(t))

        if self.mw.wing_chord_m_comb.currentText() == "m":
            t = round(self.aircraft1.wing.mean_chord,2)
            self.mw.wing_chord_out.setText(str(t))
        else:
            t = round(self.aircraft1.wing.mean_chord*data.Conversion.M_2_FT,2)
            self.mw.wing_chord_out.setText(str(t))
        t = round(self.aircraft1.wing.e,3)
        self.mw.wing_e_out.setText(str(t))

    def vert_surface_out(self):
        j = self.mw.vert_surface_comb.currentIndex()
        vt = self.aircraft1.stab.vt[j]
        self.mw.vert_chord_out.setText(str(vt.mean_chord))
        self.mw.vert_area_out.setText(str(vt.ref_area))

    #Graph Sliders
    @pyqtSlot()
    def roc_slider(self,val):
        t1 = time.time()
        actual = self.req1.roc
        self.req1.roc = val/10.0
        self.mw.roc_current_out.setText(str(val/10.0))
        # r = self.req1
        # a = self.aircraft1
        # m = self.mission1
        #
        # # Rate of Climb
        # roc = analysis.PlotConst()
        # roc.name = "roc"
        # g = r.roc/a.v_climb
        # c=0
        # j=0
        # i=0
        # roc.t_by_w[0] = 0.4
        # while roc.t_by_w[i] < roc.tbyw_end:
        #     if j==0:
        #         roc.t_by_w[0] = 0.4 + c
        #     else:
        #         roc.t_by_w.append(roc.t_by_w[0]+c)
        #         i += 1
        #     q = 0.5*data.Atmospheric_param.rho(m.segments[0].height,r.roc_isa_t)*math.pow(a.v_climb,2)
        #     k = math.pi*a.wing.a_r*a.wing.e
        #     exp = math.pow((roc.t_by_w[j] - g), 2) - 4*a.cd0/k
        #
        #     if exp >= 0:
        #         term = roc.t_by_w[j] - g
        #         if term-math.sqrt(exp) >= 0:
        #             if j == 0:
        #                 roc.w_by_s[j] = min(term+math.sqrt(exp),term-math.sqrt(exp))*q*k/2
        #             else:
        #                 roc.w_by_s.append(min(term+math.sqrt(exp),term-math.sqrt(exp))*q*k/2)
        #             j += 1
        #         elif term+math.sqrt(exp) >= 0:
        #             if j == 0:
        #                 roc.w_by_s[j] = (term+math.sqrt(exp))*q*k/2
        #             else:
        #                 roc.w_by_s.append((term+math.sqrt(exp))*q*k/2)
        #             j += 1
        #
        #     c += 0.005
        #
        # roc.num_data = len(roc.w_by_s)
        # r.constraints[3] = roc
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        t2 = time.time()
        print "Process time", (t2-t1)

        self.plot_constraints()
        self.req1.roc = actual

    @pyqtSlot()
    def takeoff_slider(self,val):
        actual = self.req1.to_distance_land
        self.req1.to_distance_land = val
        self.mw.takeoff_current_out.setText(str(val))
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        self.plot_constraints()
        self.req1.to_distance_land = actual

    @pyqtSlot()
    def landing_slider(self,val):
        actual = self.req1.la_distance_land
        self.req1.la_distance_land = val
        self.mw.landing_current_out.setText(str(val))
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        self.plot_constraints()
        self.req1.la_distance_land = actual

    # @pyqtSlot()
    # def stall_slider(self,val):
    #     actual = self.req1.v_stall_max
    #     self.req1.v_stall_max = val
    #     self.mw.landing_current_out.setText(str(val))
    #     analysis.constraint(self.req1,self.aircraft1,self.mission1)
    #     self.plot_constraints()
    #     self.req1.la_distance_land = actual

    @pyqtSlot()
    def set_refined_req_push(self):
        self.mw.tabWidget.setCurrentIndex(3)
        # self.fuse_config()

    # Checkboxes
    @pyqtSlot()
    def roc_isa_sb(self, val):
        temp = self.req1.roc_isa_t
        self.req1.roc_isa_t = val
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        self.req1.roc_isa_t = temp

    @pyqtSlot()
    def run_isa_sb(self,val):
        temp = self.req1.run_msl_isa_t
        self.req1.run_msl_isa_t = val
        analysis.constraint(self.req1,self.aircraft1,self.mission1)
        self.req1.run_msl_isa_t = temp

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
            self.mw.ds_landing_lab.setEnabled(True)
            self.mw.landing_min_lab.setEnabled(True)
            self.mw.landing_max_lab.setEnabled(True)
            self.mw.landing_slider.setEnabled(True)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "lan":
                    break
            self.constraint_plots[i].setPen(0,255,0)
        elif val == 0:
            self.mw.ds_landing_lab.setEnabled(False)
            self.mw.landing_min_lab.setEnabled(False)
            self.mw.landing_max_lab.setEnabled(False)
            self.mw.landing_slider.setEnabled(False)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "lan":
                    break
            self.constraint_plots[i].setPen(0,0,0)

    @pyqtSlot()
    def takeoff_check(self,val):
        if val == 2:
            self.mw.ds_takeoff_lab.setEnabled(True)
            self.mw.takeoff_min_lab.setEnabled(True)
            self.mw.takeoff_max_lab.setEnabled(True)
            self.mw.takeoff_slider.setEnabled(True)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "tak":
                    break
            self.constraint_plots[i].setPen(255,0,0)
        elif val == 0:
            self.mw.ds_takeoff_lab.setEnabled(False)
            self.mw.takeoff_min_lab.setEnabled(False)
            self.mw.takeoff_max_lab.setEnabled(False)
            self.mw.takeoff_slider.setEnabled(False)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "tak":
                    break
            self.constraint_plots[i].setPen(0,0,0)
    @pyqtSlot()
    def roc_check(self,val):
        if val == 2:
            # Enable slider options
            self.mw.ds_roc_lab.setEnabled(True)
            self.mw.roc_min_lab.setEnabled(True)
            self.mw.roc_max_lab.setEnabled(True)
            self.mw.roc_slider.setEnabled(True)
            # Graph plots
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "roc":
                    break
            self.constraint_plots[i].setPen(0,255,255)
        elif val == 0:
            self.mw.ds_roc_lab.setEnabled(False)
            self.mw.roc_min_lab.setEnabled(False)
            self.mw.roc_max_lab.setEnabled(False)
            self.mw.roc_slider.setEnabled(False)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "roc":
                    break
            self.constraint_plots[i].setPen(0,0,0)

    @pyqtSlot()
    def stall_check(self,val):
        if val == 2:
            self.mw.ds_stall_lab.setEnabled(True)
            self.mw.stall_min_lab.setEnabled(True)
            self.mw.stall_max_lab.setEnabled(True)
            self.mw.stall_slider.setEnabled(True)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "stall":
                    break
            self.constraint_plots[i].setPen(255,0,0)
        elif val == 0:
            self.mw.ds_stall_lab.setEnabled(False)
            self.mw.stall_min_lab.setEnabled(False)
            self.mw.stall_max_lab.setEnabled(False)
            self.mw.stall_slider.setEnabled(False)
            for i in range(len(self.req1.constraints)):
                if self.req1.constraints[i].name == "stall":
                    break
            self.constraint_plots[i].setPen(0,0,0)


    # Push Buttons
    # @pyqtSlot()
    # def add_data_push(self):
    #     #Add window to create range payload diagram points

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
        print "Before"
        analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        print "After"
        self.mw.ds_gross_out.setText(QString.number(self.aircraft1.gross_weight))
        self.add_seg_clicked = 0

        # Setting Design Space
        self.design_space()
        self.mw.tabWidget.setCurrentIndex(2)

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
                # self.constraint_plots[i].setPen(r.constr_colors[i])
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
        self.req1.aircraft_type = self.mw.aircraft_type_comb.currentText()
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

    # Fuselage Configuration

    @pyqtSlot()
    def cabin_type_comb(self,val):
        self.aircraft1.fuse.cabin.type = val
        if val == "Passenger":
            self.mw.pass_cabin_gb.setEnabled(True)
            self.mw.cargo_cabin_gb.setEnabled(False)

            self.mw.floor_lowering_lab.setEnabled(True)
            self.mw.floor_lowering_inp.setEnabled(True)
            self.mw.floor_lowering_m_comb.setEnabled(True)

            self.mw.floor_thickness_lab.setEnabled(True)
            self.mw.floor_thickness_inp.setEnabled(True)
            self.mw.floor_thickness_m_comb.setEnabled(True)

        else:
            self.mw.cargo_cabin_gb.setEnabled(True)
            self.mw.pass_cabin_gb.setEnabled(False)

            self.mw.floor_lowering_lab.setEnabled(False)
            self.mw.floor_lowering_inp.setEnabled(False)
            self.mw.floor_lowering_m_comb.setEnabled(False)

            self.mw.floor_thickness_lab.setEnabled(False)
            self.mw.floor_thickness_inp.setEnabled(False)
            self.mw.floor_thickness_m_comb.setEnabled(False)

    @pyqtSlot()
    def class_num_sb(self,val):
        self.aircraft1.fuse.cabin.class_num = val
        if val == 1:
            self.mw.avg_seats2_sb.setEnabled(False)
            self.mw.avg_seats3_sb.setEnabled(False)
            self.mw.aisles2_sb.setEnabled(False)
            self.mw.aisles3_sb.setEnabled(False)
            self.mw.seats_num2_inp.setEnabled(False)
            self.mw.seats_num3_inp.setEnabled(False)
            self.mw.seat_pitch2_inp.setEnabled(False)
            self.mw.seat_pitch3_inp.setEnabled(False)
            self.mw.lav2_sb.setEnabled(False)
            self.mw.lav3_sb.setEnabled(False)
            self.mw.gall2_check.setEnabled(False)
            self.mw.gall3_check.setEnabled(False)
            self.mw.classII_lab.setEnabled(False)
            self.mw.classIII_lab.setEnabled(False)

        elif val == 2:
            self.mw.avg_seats2_sb.setEnabled(True)
            self.mw.avg_seats3_sb.setEnabled(False)
            self.mw.aisles2_sb.setEnabled(True)
            self.mw.aisles3_sb.setEnabled(False)
            self.mw.seats_num2_inp.setEnabled(True)
            self.mw.seats_num3_inp.setEnabled(False)
            self.mw.seat_pitch2_inp.setEnabled(True)
            self.mw.seat_pitch3_inp.setEnabled(False)
            self.mw.lav2_sb.setEnabled(True)
            self.mw.lav3_sb.setEnabled(False)
            self.mw.gall2_check.setEnabled(True)
            self.mw.gall3_check.setEnabled(False)
            self.mw.classII_lab.setEnabled(True)
            self.mw.classIII_lab.setEnabled(False)

        else:
            self.mw.avg_seats2_sb.setEnabled(True)
            self.mw.avg_seats3_sb.setEnabled(True)
            self.mw.aisles2_sb.setEnabled(True)
            self.mw.aisles3_sb.setEnabled(True)
            self.mw.seats_num3_inp.setEnabled(True)
            self.mw.seat_pitch2_inp.setEnabled(True)
            self.mw.seat_pitch3_inp.setEnabled(True)
            self.mw.lav2_sb.setEnabled(True)
            self.mw.lav3_sb.setEnabled(True)
            self.mw.gall2_check.setEnabled(True)
            self.mw.gall3_check.setEnabled(True)
            self.mw.classII_lab.setEnabled(True)
            self.mw.classIII_lab.setEnabled(True)

    @pyqtSlot()
    def avg_seats1_sb(self,seat):
        self.aircraft1.fuse.cabin.avg_seats_abr[0] = seat
        self.fuse_length_out_update()

        self.fuse_cs_out_update()

    @pyqtSlot()
    def avg_seats2_sb(self,seat):
        self.aircraft1.fuse.cabin.avg_seats_abr[1] = seat
        self.fuse_length_out_update()
        self.fuse_cs_out_update()

    @pyqtSlot()
    def avg_seats3_sb(self,seat):
        self.aircraft1.fuse.cabin.avg_seats_abr[2] = seat
        self.fuse_length_out_update()
        self.fuse_cs_out_update()

    @pyqtSlot()
    def aisles1_sb(self,num):
        self.aircraft1.fuse.cabin.aisle_num[0] = num
        self.fuse_length_out_update()
        self.fuse_cs_out_update()

    @pyqtSlot()
    def aisles2_sb(self,num):
        self.aircraft1.fuse.cabin.aisle_num[1] = num
        self.fuse_length_out_update()
        self.fuse_cs_out_update()

    @pyqtSlot()
    def aisles3_sb(self,num):
        self.aircraft1.fuse.cabin.aisle_num[2] = num
        self.fuse_length_out_update()
        self.fuse_cs_out_update()

    @pyqtSlot()
    def seat_pitch1_inp(self,text):
        if self.isfloat(text):
            cab = self.aircraft1.fuse.cabin
            if self.mw.seat_pitch_m_comb.currentText() == "m":
                cab.seat_pitch[0] = float(text)
            elif self.mw.seat_pitch_m_comb.currentText() == "ft":
                cab.seat_pitch[0] = float(text)/data.Conversion.M_2_FT
            else:
                cab.seat_pitch[0] = float(text)/data.Conversion.M_2_IN
            self.fuse_length_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def seat_pitch2_inp(self,text):
        if self.isfloat(text):
            cab = self.aircraft1.fuse.cabin
            if self.mw.seat_pitch_m_comb.currentText() == "m":
                cab.seat_pitch[1] = float(text)
            elif self.mw.seat_pitch_m_comb.currentText() == "ft":
                cab.seat_pitch[1] = float(text)/data.Conversion.M_2_FT
            else:
                cab.seat_pitch[1] = float(text)/data.Conversion.M_2_IN
            self.fuse_length_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def seat_pitch3_inp(self,text):
        if self.isfloat(text):
            cab = self.aircraft1.fuse.cabin
            if self.mw.seat_pitch_m_comb.currentText() == "m":
                cab.seat_pitch[2] = float(text)
            elif self.mw.seat_pitch_m_comb.currentText() == "ft":
                cab.seat_pitch[2] = float(text)/data.Conversion.M_2_FT
            else:
                cab.seat_pitch[2] = float(text)/data.Conversion.M_2_IN
            self.fuse_length_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def seats_num1_inp(self,text):
        print text
        if self.isdigit(text):
            n = int(text)
            self.aircraft1.fuse.cabin.seats_num[0] = n
            self.fuse_length_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def seats_num2_inp(self,text):
        if self.isdigit(text):
            n = int(text)
            self.aircraft1.fuse.cabin.seats_num[1] = n
            self.fuse_length_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()
    @pyqtSlot()
    def seats_num3_inp(self,text):
        if self.isdigit(text):
            n = int(text)
            self.aircraft1.fuse.cabin.seats_num[2] = n
            self.fuse_length_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def lav1_sb(self,val):
        self.aircraft1.fuse.cabin.lav_num[0] = val
        self.fuse_length_out_update()

    @pyqtSlot()
    def lav2_sb(self,val):
        self.aircraft1.fuse.cabin.lav_num[1] = val
        self.fuse_length_out_update()

    @pyqtSlot()
    def lav3_sb(self,val):
        self.aircraft1.fuse.cabin.lav_num[2] = val
        self.fuse_length_out_update()

    @pyqtSlot()
    def gall1_check(self,val):
        if val == 2:
            self.aircraft1.fuse.cabin.galley[0] = val-1
        else:
            self.aircraft1.fuse.cabin.galley[0] = val
        self.fuse_length_out_update()

    @pyqtSlot()
    def gall2_check(self,val):
        if val == 2:
            self.aircraft1.fuse.cabin.galley[1] = val-1
        else:
            self.aircraft1.fuse.cabin.galley[1] = val
        self.fuse_length_out_update()

    @pyqtSlot()
    def gall3_check(self,val):
        if val == 2:
            self.aircraft1.fuse.cabin.galley[2] = val-1
        else:
            self.aircraft1.fuse.cabin.galley[2] = val
        self.fuse_length_out_update()

    @pyqtSlot()
    def lower_deck_comb(self,deck):
        self.aircraft1.fuse.container.width_bot = data.Historic_param.Fuselage.cargo_containers(deck,0)
        self.aircraft1.fuse.container.width_top = data.Historic_param.Fuselage.cargo_containers(deck,1)
        self.aircraft1.fuse.container.height = data.Historic_param.Fuselage.cargo_containers(deck,2)
        if data.Historic_param.Fuselage.cargo_containers(deck,3):
            self.mw.double_cont_check.setEnabled(True)
        else:
            self.mw.double_cont_check.setEnabled(False)
        self.fuse_cs_out_update()

    @pyqtSlot()
    def double_cont_check(self,state):
        if state == 2:
            self.aircraft1.fuse.container.double = 1
        else:
            self.aircraft1.fuse.container.double = 0

    @pyqtSlot()
    def cargo_length_inp(self,text):
        if self.isfloat(text):
            if self.mw.cargo_m_comb.currentText() == "m":
                self.aircraft1.fuse.cabin.cargo_length = float(text)
            else:
                self.aircraft1.fuse.cabin.cargo_length = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def cargo_width_inp(self,text):
        if self.isfloat(text):
            if self.mw.cargo_m_comb.currentText() == "m":
                self.aircraft1.fuse.cabin.cargo_width = float(text)
            else:
                self.aircraft1.fuse.cabin.cargo_width = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def cargo_height_inp(self,text):
        if self.isfloat(text):
            if self.mw.cargo_m_comb.currentText() == "m":
                self.aircraft1.fuse.cabin.cargo_height = float(text)
            else:
                self.aircraft1.fuse.cabin.cargo_height = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def floor_lowering_inp(self,text):
        if self.isfloat(text):
            if self.mw.floor_lowering_m_comb.currentText() == "m":
                self.aircraft1.fuse.cabin.floor_lowering = float(text)
            else:
                self.aircraft1.fuse.cabin.floor_lowering = float(text)/data.Conversion.M_2_FT

            self.fuse_cs_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def floor_thickness_inp(self,text):
        if self.isfloat(text):
            if self.mw.floor_thickness_m_comb.currentText() == "m":
                self.aircraft1.fuse.cabin.floor_thickness = float(text)
            else:
                self.aircraft1.fuse.cabin.floor_thickness = float(text)/data.Conversion.M_2_FT

            self.fuse_cs_out_update()
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def nose_length2diameter_inp(self,text):
        if self.isfloat(text):
            self.aircraft1.fuse.nose_length2dia = float(text)
            self.aircraft1.fuse.update_fuse_length()
            self.mw.fuse_length_out.setText(QString.number(self.aircraft1.fuse.length))
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def nose_offset_inp(self,text):
        if self.isfloat(text):
            if self.mw.nose_offset_m_comb.currentText() == "m":
                self.aircraft1.fuse.nose_offset = float(text)
                self.aircraft1.fuse.update_fuse_length()
                self.mw.fuse_length_out.setText(QString.number(self.aircraft1.fuse.length))
            else:
                self.aircraft1.fuse.nose_offset = float(text)/data.Conversion.M_2_FT
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def tail_length2diameter_inp(self,text):
        if self.isfloat(text):
            self.aircraft1.fuse.tail_length2dia = float(text)
            self.aircraft1.fuse.update_fuse_length()
            self.mw.fuse_length_out.setText(QString.number(self.aircraft1.fuse.length))
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def tail_offset2diameter_inp(self,text):
        if self.isfloat(text):
            self.aircraft1.fuse.tail_offset2dia = float(text)
            self.aircraft1.fuse.update_fuse_length()
            self.mw.fuse_length_out.setText(QString.number(self.aircraft1.fuse.length))
        elif text == "":
            pass
        else:
            input_warn = QtGui.QMessageBox()
            input_warn.setText("Please enter a number")
            input_warn.exec_()

    @pyqtSlot()
    def set_fuse_param_push(self):
        self.wing_stab_set_defaults()
        self.mw.tabWidget.setCurrentIndex(4)

    @pyqtSlot()
    def cabin_ratio_slider(self,val):
        t = val/100.0
        self.mw.cabin_ratio_out.setText(str(t))
        self.aircraft1.fuse.cabin.cabin_h2w_ratio = t
        self.aircraft1.fuse.cabin.inner_height = self.aircraft1.fuse.cabin.inner_width*t
        self.fuse_cs_out_update()

    # Fuselage Configurations - Conversions
    @pyqtSlot()
    def seat_pitch_m_comb(self,pitch):
        if pitch == "ft":
            g = self.aircraft1.fuse.cabin.seat_pitch[0]*data.Conversion.M_2_FT
            self.mw.seat_pitch1_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.seat_pitch[1]*data.Conversion.M_2_FT
            self.mw.seat_pitch2_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.seat_pitch[2]*data.Conversion.M_2_FT
            self.mw.seat_pitch3_inp.setText(QString.number(g))
        elif pitch == "in":
            g = self.aircraft1.fuse.cabin.seat_pitch[0]*data.Conversion.M_2_IN
            self.mw.seat_pitch1_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.seat_pitch[1]*data.Conversion.M_2_IN
            self.mw.seat_pitch2_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.seat_pitch[2]*data.Conversion.M_2_IN
            self.mw.seat_pitch3_inp.setText(QString.number(g))
        else:
            g = self.aircraft1.fuse.cabin.seat_pitch[0]
            self.mw.seat_pitch1_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.seat_pitch[1]
            self.mw.seat_pitch2_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.seat_pitch[2]
            self.mw.seat_pitch3_inp.setText(QString.number(g))

    @pyqtSlot()
    def cargo_m_comb(self,dist):
        if dist == "ft":
            g = self.aircraft1.fuse.cabin.cargo_length*data.Conversion.M_2_FT
            self.mw.cargo_length_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.cargo_width*data.Conversion.M_2_FT
            self.mw.cargo_width_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.cargo_height*data.Conversion.M_2_FT
            self.mw.cargo_height_inp.setText(QString.number(g))
        else:
            g = self.aircraft1.fuse.cabin.cargo_length
            self.mw.cargo_length_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.cargo_width
            self.mw.cargo_width_inp.setText(QString.number(g))
            g = self.aircraft1.fuse.cabin.cargo_height
            self.mw.cargo_height_inp.setText(QString.number(g))

    @pyqtSlot()
    def floor_lowering_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.floor_lowering*data.Conversion.M_2_FT
            self.mw.floor_lowering_inp.setText(str(t))
        else:
            self.mw.floor_lowering_inp.setText(str(self.aircraft1.fuse.cabin.floor_lowering))

    @pyqtSlot()
    def inner_height_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.inner_height*data.Conversion.M_2_FT
            self.mw.inner_height_out.setText(str(t))
        else:
            self.mw.inner_height_out.setText(str(self.aircraft1.fuse.cabin.inner_height))

    @pyqtSlot()
    def inner_width_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.inner_width*data.Conversion.M_2_FT
            self.mw.inner_width_out.setText(str(t))
        else:
            self.mw.inner_width_out.setText(str(self.aircraft1.fuse.cabin.inner_width))

    @pyqtSlot()
    def inner_eq_diameter_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.inner_eq_dia*data.Conversion.M_2_FT
            self.mw.inner_eq_diameter_out.setText(str(t))
        else:
            self.mw.inner_eq_diameter_out.setText(str(self.aircraft1.fuse.cabin.inner_eq_dia))

    @pyqtSlot()
    def fuse_thickness_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.thickness*data.Conversion.M_2_FT
            self.mw.fuse_thickness_out.setText(str(t))
        elif dist == "in":
            t = self.aircraft1.fuse.thickness*data.Conversion.M_2_IN
            self.mw.fuse_thickness_out.setText(str(t))
        else:
            self.mw.fuse_thickness_out.setText(str(self.aircraft1.fuse.thickness))

    @pyqtSlot()
    def outer_eq_diameter_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.outer_eq_dia*data.Conversion.M_2_FT
            self.mw.outer_eq_diameter_out.setText(str(t))
        else:
            self.mw.outer_eq_diameter_out.setText(str(self.aircraft1.fuse.cabin.outer_eq_dia))

    @pyqtSlot()
    def floor_thickness_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.floor_thickness*data.Conversion.M_2_FT
            self.mw.floor_thickness_inp.setText(str(t))
        elif dist == "in":
            t = self.aircraft1.fuse.cabin.floor_thickness*data.Conversion.M_2_IN
            self.mw.floor_thickness_inp.setText(str(t))
        else:
            self.mw.floor_thickness_inp.setText(str(self.aircraft1.fuse.cabin.floor_thickness))

    @pyqtSlot()
    def outer_height_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.outer_height*data.Conversion.M_2_FT
            self.mw.outer_height_out.setText(str(t))
        else:
            self.mw.outer_height_out.setText(str(self.aircraft1.fuse.cabin.outer_height))

    @pyqtSlot()
    def outer_width_m_comb(self,dist):
        if dist == "ft":
            t = self.aircraft1.fuse.cabin.outer_width*data.Conversion.M_2_FT
            self.mw.outer_width_out.setText(str(t))
        else:
            self.mw.outer_width_out.setText(str(self.aircraft1.fuse.cabin.outer_width))

    @pyqtSlot()
    def nose_offset_m_comb(self,val):
        if val == "m":
            self.mw.nose_offset_inp.setText(QString.number(self.aircraft1.fuse.nose_offset))
        else:
            t = self.aircraft1.fuse.nose_offset*data.Conversion.M_2_FT
            self.mw.nose_offset_inp.setText(QString.number(t))

    @pyqtSlot()
    def cabin_length_m_comb(self,val):
        if val == "m":
            self.mw.cabin_length_out.setText(QString.number(self.aircraft1.fuse.cabin.length))
        else:
            t = self.aircraft1.fuse.cabin.length*data.Conversion.M_2_FT
            self.mw.cabin_length_out.setText(QString.number(t))

    @pyqtSlot()
    def fuse_length_m_comb(self,val):
        if val == "m":
            self.mw.fuse_length_out.setText(QString.number(self.aircraft1.fuse.length))
        else:
            t = self.aircraft1.fuse.length*data.Conversion.M_2_FT
            self.mw.fuse_length_out.setText(QString.number(t))

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

class AirfoilDialog(QtGui.QDialog):
    def __init__(self):
        print "Inside"
        self.ad = airfoil.Ui_Dialog()
        print "Second"
        super(AirfoilDialog, self).__init__()
        self.ad.setupUi(self)
        # self.show()


