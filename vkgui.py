#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
from playerGui import MainWindow
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)
qb = MainWindow()
qb.show()

app.exec_()
qb.player.stop_play()