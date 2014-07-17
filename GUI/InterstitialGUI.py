# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import sys
from os import path

from PySide.QtCore import *
from PySide.QtGui import *

from Core import InterstitialCore
from GUI import DirsHandlerGUI
# printer
# allows for writing to a QWindow


class printer():


    def __init__(self, t):
        self.t = t

    def write(self, m):
        self.t.moveCursor(QTextCursor.End)
        self.t.insertPlainText(m)

'''
Interstitial GUI Manager
'''
class InterstitialGUI(QWidget):


    def __init__(self):
        """
        Constructor
        """
        QWidget.__init__(self)
        self.IntersCore = InterstitialCore.InterstitialCore()
        self.setWindowTitle('Interstitial Error Detector')
        self.layout = QGridLayout(self)
        self.dirsHandlerGui = DirsHandlerGUI.DirsHandlerGUI()
        self.createDirectories()
        self.go = QPushButton("Run!", self)

        self.addWidgetToLayout()
        self.setTriggers()
        self.setLayout(self.layout)

    def createDirectories(self):
        """
        Create Gui
        """
        self.manifest_dir_text = QLineEdit()
        self.manifest_dir_text.setReadOnly(True)
        self.dirsHandlerGui.createDirectoriesInfo()

    def addWidgetToLayout(self):
        """
        Add Widget To Layout
        """
        self.layout.addWidget(self.go, 4, 1)
        self.layout.addWidget(self.manifest_dir_text, 2, 1)
        self.layout.addWidget(QLabel("Manifest Destination"), 2, 0)
        self.layout = self.dirsHandlerGui.AddWidgets(self.layout)

    def setTriggers(self):
        """
        Set GUI Triggers
        """
        self.go.clicked.connect(self.newWin)
        self.manifest_dir_text.setText(path.expanduser('~/'))
        self.dirsHandlerGui.setTriggers()

    def newWin(self):
        """
        Open New Window
        """
        ReportDetailDialogBox = QDialog(self)
        ReportDetailexitBtn = QPushButton("Exit", self)
        ReportDetailText = QTextEdit(self)
        ReportDetailLayout = QVBoxLayout(ReportDetailDialogBox)

        ReportDetailDialogBox.setWindowTitle('Interstitial Error Detector')

        ReportDetailexitBtn.setEnabled(False)
        ReportDetailText.setReadOnly(True)

        ReportDetailexitBtn.clicked.connect(self.close)

        ReportDetailLayout.addWidget(ReportDetailText)
        ReportDetailLayout.addWidget(ReportDetailexitBtn)

        ReportDetailDialogBox.setLayout(ReportDetailLayout)

        sys.stdout = printer(ReportDetailText)
        ReportDetailDialogBox.resize(1000, 300)
        ReportDetailDialogBox.show()

        self.IntersCore.execute(str(self.daw_dir_text.text()), str(self.ref_dir_text.text()), str(self.manifest_dir_text.text()), QCoreApplication.instance())

        ReportDetailexitBtn.setEnabled(True)

