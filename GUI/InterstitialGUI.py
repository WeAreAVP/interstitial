# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import sys
from os import path

from PySide.QtCore import *
from PySide.QtGui import *

#Custom Libs

from Core import InterstitialCore, SharedApp
from GUI import DirsHandlerGUI

"""
Interstitial GUI Manager
"""


class InterstitialGUI(QWidget):


    def __init__(self):
        """
        Constructor
        """
        QWidget.__init__(self)
        self.IntersCore = InterstitialCore.InterstitialCore()
        self.Interstitial = SharedApp.SharedApp.App
        self.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
        self.layout = QGridLayout(self)

        self.dirsHandlerGuiList = {}

        self.number_of_scans = 1

        for index in xrange(0, self.number_of_scans):
            self.dirsHandlerGuiList[index] = DirsHandlerGUI.DirsHandlerGUI()

        self.createDirectories()
        self.go = QPushButton(self.Interstitial.label['runLable'], self)
        self.addWidgetToLayout()
        self.setTriggers()
        self.setLayout(self.layout)

    def createDirectories(self):
        """
        Create Gui
        """
        self.manifest_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)

        self.manifest_dir_text = QLineEdit()
        self.manifest_dir_text.setReadOnly(True)

        for index in xrange(0, self.number_of_scans):
            self.dirsHandlerGuiList[index].createDirectoriesInfo()

    def addWidgetToLayout(self):
        """
        Add Widget To Layout
        """
        self.layout.addWidget(self.go, 4, 1)
        self.layout.addWidget(self.manifest_dir_text, 2, 1)
        self.layout.addWidget(QLabel(self.Interstitial.label['manifestDest']), 2, 0)
        self.layout.addWidget(self.manifest_dir_selector, 2, 2)

        for index in xrange(0, self.number_of_scans):
            self.layout = self.dirsHandlerGuiList[index].AddWidgets(self.layout)

    def setTriggers(self):
        """
        Set GUI Triggers
        """
        self.go.clicked.connect(self.ErrorVerifier)
        self.manifest_dir_text.setText(path.expanduser('~/'))

        self.manifest_dir_selector.clicked.connect(self.manifestTrigger)
        for index in xrange(0, self.number_of_scans):
            self.dirsHandlerGuiList[index].setTriggers()

    def manifestTrigger(self):
        """
        get Manifest Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.manifest_dir_text.setText(path_selected)

    def ErrorVerifier(self):
        """
        Look For Errors in Proveded Wav Files

        @retrun None
        """
        report_detail_dialog_box = QDialog(self)
        report_detail_exit_btn = QPushButton(self.Interstitial.label['exit'], self)
        report_detail_text = QTextEdit(self)
        report_detail_layout = QVBoxLayout(report_detail_dialog_box)

        report_detail_dialog_box.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])

        report_detail_exit_btn.setEnabled(False)
        report_detail_text.setReadOnly(True)

        report_detail_exit_btn.clicked.connect(self.close)

        report_detail_layout.addWidget(report_detail_text)
        report_detail_layout.addWidget(report_detail_exit_btn)

        report_detail_dialog_box.setLayout(report_detail_layout)

        sys.stdout = Printer(report_detail_text)
        report_detail_dialog_box.resize(1000, 300)
        report_detail_dialog_box.show()

        for index in xrange(0, self.number_of_scans):

            self.dirsHandlerGuiList[index].dirs_handler_core.setCoreDawText(self.dirsHandlerGuiList[index].getGuiDawText())

            self.dirsHandlerGuiList[index].dirs_handler_core.setCoreRefText(self.dirsHandlerGuiList[index].getGuiRefText())

            self.dirsHandlerGuiList[index].dirs_handler_core.execute(str(self.manifest_dir_text.text()), QCoreApplication.instance())

        report_detail_exit_btn.setEnabled(True)


# printer
# allows for writing to a QWindow


class Printer():


    def __init__(self, t):
        self.t = t

    def write(self, m):
        self.t.moveCursor(QTextCursor.End)
        self.t.insertPlainText(m)
