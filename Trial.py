__author__ = 'Varun S S'
import pyqtgraph.examples

pyqtgraph.examples.run()


pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
self.graphs_hlayout.addWidget(pw)
