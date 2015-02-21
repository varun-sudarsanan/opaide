import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSignal,QObject,pyqtSlot,QString
import req
import config
import mission
import analysis

from gui import window
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        self.mw = window.Ui_MainWindow()
        super(MyWindow, self).__init__()
        self.mw.setupUi(self)
        self.create_objects()

        self.update_gui()
        self.connect(self.mw.pass_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")),self.change_gross_wt)
        self.show()
    @pyqtSlot()
    def change_gross_wt(self,pos):
        self.aircraft1.pass_n = self.req1.min_pass + int(pos/(self.req1.max_pass- self.req1.min_pass))
        print self.aircraft1.pass_n
        se = analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        self.mw.pass_label.setText("Passengers:\n"+QString.number(self.aircraft1.pass_n)) #lf.aircraft1.gross_weight))
        self.mw.wt_estimate_label.setText("Gross Weight:\n"+QString.number(se)) #lf.aircraft1.gross_weight))

    def update_gui(self):
        self.mw.min_pass.setText("Min_pass\n"+QString.number(self.req1.min_pass))
        self.mw.max_pass.setText("Min_pass\n"+QString.number(self.req1.max_pass))

        self.mw.pass_label.setText("Passengers:\n"+QString.number(self.req1.min_pass))
        self.aircraft1.pass_n = self.req1.min_pass
        se = analysis.class1_estimation(self.req1,self.aircraft1,self.mission1)
        self.mw.wt_estimate_label.setText("Gross Weight:\n"+QString.number(se))

    def create_objects(self):
        self.req1 = req.AircraftRequirements()
        self.aircraft1 = config.Aircraft()
        self.mission1 = mission.MissionDef()

        for i in range(self.mission1.num_segments):
            self.mission1.segments[i].ref=i
            if self.mission1.segments[i].type==3:
               self.mission1.segments[i].range=self.req1.design_range
            elif self.mission1.segments[i].type==4:
                self.mission1.segments[i].time=self.req1.loiter_time

app = QtGui.QApplication(sys.argv)
win = MyWindow()

sys.exit(app.exec_())