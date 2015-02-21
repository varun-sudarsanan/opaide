import sys
import mywindow
from PyQt4 import QtGui, uic, QtCore

app = QtGui.QApplication(sys.argv)
win = mywindow.MyWindow()

sys.exit(app.exec_())


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
