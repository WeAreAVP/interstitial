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
    """
        Application Interstitial GUI Class
    """

    def __init__(self):
        """
        Constructor
        """
        QWidget.__init__(self)
        self.inters_core = InterstitialCore.InterstitialCore()
        self.Interstitial = SharedApp.SharedApp.App
        self.grid_layout = QGridLayout(self)
        self.dirs_handler_gui = {}

        self.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
        self.setMaximumWidth(550)

        self.number_of_scans = 1

        self.dirs_handler_gui = DirsHandlerGUI.DirsHandlerGUI()

        self.createDirectories()
        self.go = QPushButton(self.Interstitial.label['runLabel'], self)
        self.addWidgetToLayout()
        self.setTriggers()

    def createDirectories(self):
        """
        Create Gui

        @return: None
        """
        self.manifest_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)
        self.manifest_dir_text = QLineEdit()

        self.manifest_dir_selector.setMaximumSize(50, 100)
        self.manifest_dir_text.setMaximumSize(410, 100)
        self.manifest_dir_text.setReadOnly(True)

        self.grid_layout.addWidget(self.dirs_handler_gui.createDAWDirectories())
        self.grid_layout.addWidget(self.dirs_handler_gui.add_new_daw)

        self.grid_layout.addWidget(self.dirs_handler_gui.createRefDirectories())
        self.grid_layout.addWidget(self.dirs_handler_gui.add_new_ref)
        self.setLayout(self.grid_layout)

    def addWidgetToLayout(self):
        """
        Add Widget To Layout

        @return: None
        """
        group_box = QGroupBox(self.Interstitial.label['manifestDest'])
        vbox = QVBoxLayout()

        vbox.addWidget(self.manifest_dir_text)
        vbox.addWidget(self.manifest_dir_selector, 0, 2)
        vbox.addWidget(self.go, 0, 1)

        vbox.addStretch(1)

        group_box.setLayout(vbox)

        self.grid_layout.addWidget(group_box)

    def setTriggers(self):
        """
        Set GUI Triggers

        @return: None
        """

        self.go.clicked.connect(self.ErrorVerifier)
        self.manifest_dir_text.setText(path.expanduser('~/'))

        self.manifest_dir_selector.clicked.connect(self.manifestTrigger)

    def manifestTrigger(self):
        """
        get Manifest Trigger

        @return: None
        """

        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.manifest_dir_text.setText(path_selected)

    def ErrorVerifier(self):
        """
        Look For Errors in Proveded Wav Files

        @return: None
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

        self.dirs_handler_gui.RunExecutor(str(self.manifest_dir_text.text()))

        report_detail_exit_btn.setEnabled(True)

# printer
# allows for writing to a QWindow


class Printer():


    def __init__(self, t):
        self.t = t

    def write(self, m):
        self.t.moveCursor(QTextCursor.End)
        self.t.insertPlainText(m)