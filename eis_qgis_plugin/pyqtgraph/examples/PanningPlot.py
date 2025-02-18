"""
Shows use of PlotWidget to display panning data
"""

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle("pyqtgraph example: PanningPlot")

plt = win.addPlot()
# plt.setAutoVisibleOnly(y=True)
curve = plt.plot()

data = []
count = 0


def update():
    global data, curve, count
    data.append(np.random.normal(size=10) + np.sin(count * 0.1) * 5)
    if len(data) > 100:
        data.pop(0)
    curve.setData(np.hstack(data))
    count += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if __name__ == "__main__":
    pg.exec()
