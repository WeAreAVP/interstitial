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
from GUI import DirsHandlerGUI, SharedAppGUI

"""
Interstitial GUI Manager
"""


class InterstitialGUI(QWidget):
    """
        Application Interstitial GUI Class
    """

    _instance = None

    @staticmethod
    def getInstance():
        """
        Constructor
        """
        if not isinstance(InterstitialGUI._instance, InterstitialGUI):
            InterstitialGUI._instance = QWidget.__new__(InterstitialGUI)
            SharedAppGUI.SharedAppGUI.GUIApp = InterstitialGUI._instance
            SharedAppGUI.SharedAppGUI.GUIApp._instance.setup()

        return InterstitialGUI._instance

    def setup(self):
        QWidget.__init__(self)
        self.inters_core = InterstitialCore.InterstitialCore()
        self.Interstitial = SharedApp.SharedApp.App
        self.grid_layout = QGridLayout(self)
        self.vbox = QHBoxLayout()
        self.group_box = QGroupBox(self.Interstitial.label['manifestDest'])
        self.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
        self.setMaximumWidth(600)
        self.setMinimumWidth(600)


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

        self.manifest_dir_selector.setMaximumSize(50, 25)
        self.manifest_dir_text.setMaximumSize(420, 25)
        self.manifest_dir_text.setMinimumSize(420, 25)

        #self.go.setMaximumSize(50, 25)
        #self.go.setMinimumSize(50, 25)

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
        self.vbox.addWidget(self.manifest_dir_text)
        self.vbox.addWidget(self.manifest_dir_selector)
        self.vbox.addWidget(self.go)

        self.vbox.addStretch(1)

        self.group_box.setLayout(self.vbox)

        self.grid_layout.addWidget(self.group_box)

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
        #teminal = Terminal()
        self.dirs_handler_gui.RunExecutor(str(self.manifest_dir_text.text()))

        report_detail_exit_btn.setEnabled(True)


#class Terminal(QDialog):
#
#    def __init__(self):
#        self.Interstitial_GUI = SharedApp.SharedAppGUI.GUIApp
#        QDialog.__init__(self, SharedApp.SharedAppGUI.GUIApp)
#        self.setWindowModality(Qt.WindowModal)
#
#        self.inters_core = InterstitialCore.InterstitialCore()
#        self.Interstitial = SharedApp.SharedApp.App
#
#        self.report_detail_exit_btn = QPushButton(self.Interstitial.label['exit'], self)
#        self.report_detail_text = QTextEdit(self)
#        self.report_detail_layout = QVBoxLayout(self)
#        self.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
#        self.report_detail_exit_btn.setEnabled(False)
#        self.report_detail_text.setReadOnly(True)
#
#        self.report_detail_exit_btn.clicked.connect(self.close)
#
#        self.report_detail_layout.addWidget(self.report_detail_text)
#        self.report_detail_layout.addWidget(self.report_detail_exit_btn)
#
#        self.setLayout(self.report_detail_layout)
#        sys.stdout = Printer(self.report_detail_text)
#        self.report_detail_layout.addStrut(200)
#        self.resize(1000, 300)
#        self.show()
#        self.exec_()
#        #self.SetWindowLayout()
#        #self.exec_()
#
#    def enable_next(self):
#        self.report_detail_exit_btn.setEnabled(True)


# printer
# allows for writing to a QWindow


class Printer():


    def __init__(self, t):
        self.t = t

    def write(self, m):
        self.t.moveCursor(QTextCursor.End)
        self.t.insertPlainText(m)