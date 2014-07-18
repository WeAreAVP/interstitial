# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import sys
from os import path

from PySide.QtCore import *
from PySide.QtGui import *
from Config import messages
from Config import Configuration
from Core import InterstitialCore
from GUI import DirsHandlerGUI


class InterstitialGUI(QWidget):


    """
    Interstitial GUI Manager
    """
    def __init__(self):
        """
        Constructor
        """
        QWidget.__init__(self)

        self.number_of_scans = 2
        self.configuration = Configuration.Configuration()
        self.inters_core = InterstitialCore.InterstitialCore()
        self.dirs_handler_gui = {}

        for index in xrange(0, self.number_of_scans):
            self.dirs_handler_gui[index] = DirsHandlerGUI.DirsHandlerGUI()

        self.setUpView()

    def setUpView(self):
        """
        Set interstitial View Up
        """
        self.setWindowTitle(messages.message['InterErrorDetectTitle'])
        self.layout = QGridLayout(self)

        self.createDirectories()

        self.go = QPushButton("Run!", self)

        self.addWidgetToLayout()
        self.setTriggers()
        #self.setLayout(self.layout)
        pass

    def setUpDirs(self):
        """
        Set Up Dirs
        """
        pass

    def createDirectories(self):
        """
        Create Gui
        """
        self.manifest_dir_text = QLineEdit()
        self.manifest_dir_text.setReadOnly(True)
        self.manifest_dir_selector_gui = QPushButton("...", self)

        #for index in xrange(0, self.number_of_scans):
        #    self.dirs_handler_gui[index].createDirectoriesInfo()

    def addWidgetToLayout(self):

        """
        Add Widget To Layout
        """

        self.widget = QWidget(self)
        self.main = QHBoxLayout()

        #for index in xrange(0, self.number_of_scans):
        #    single_dirs_layout = QVBoxLayout()
        #
        #    outer_box = QGroupBox("Recipient Email Addresses")
        #
        #    outer_box.setFixedSize(400, 400)
        #
        #    single_dirs_layout = self.dirs_handler_gui[index].AddWidgets(single_dirs_layout)
        #
        #    outer_box.setLayout(single_dirs_layout)
        #
        #    self.main.addWidget(outer_box)

        self.layout.addWidget(QLabel("Manifest Destination"))#, 2, 0
        self.layout.addWidget(self.manifest_dir_text)#, 2, 1
        self.layout.addWidget(self.manifest_dir_selector_gui)#, 2, 2
        self.layout.addWidget(self.go)#, 4, 1

    def setTriggers(self):
        """
        Set GUI Triggers
        """
        self.go.clicked.connect(self.newWin)
        self.manifest_dir_text.setText(path.expanduser('~/'))
        self.manifest_dir_selector_gui.clicked.connect(self.manifestTrigger)

        grid = QGridLayout()
        for index in xrange(0, self.number_of_scans):
            layout = self.dirs_handler_gui[index].addNewDirSet()
            grid.addWidget(layout)

        self.setLayout(grid)
        #self.setWindowTitle("Group Box")
        self.resize(480, 320)

    def newWin(self):
        """
        Open New Window
        """
        report_detail_dialog_box = QDialog(self)
        report_detail_exit_btn = QPushButton("Exit", self)
        report_detail_text = QTextEdit(self)
        report_detail_layout = QVBoxLayout(report_detail_dialog_box)

        report_detail_dialog_box.setWindowTitle(messages.message['InterErrorDetectTitle'])

        report_detail_exit_btn.setEnabled(False)
        report_detail_text.setReadOnly(True)

        report_detail_exit_btn.clicked.connect(self.close)

        report_detail_layout.addWidget(report_detail_text)
        report_detail_layout.addWidget(report_detail_exit_btn)

        report_detail_dialog_box.setLayout(report_detail_layout)

        sys.stdout = printer(report_detail_text)
        report_detail_dialog_box.resize(1000, 300)
        report_detail_dialog_box.show()

        self.inters_core.execute(str(self.dirs_handler_gui.getDaw()), str(self.dirs_handler_gui.getRefDir()), str(self.manifest_dir_text.text()), QCoreApplication.instance())

        report_detail_exit_btn.setEnabled(True)

    def manifestTrigger(self):
        """
        Get Manifest Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=self.configuration.getUserHomePath())
        self.manifest_dir_text.setText(path_selected)


class printer():


    """
    printer
    allows for writing to a QWindow
    """
    def __init__(self, target):
        self.target = target

    def write(self, message):
        """
        @param message: Message to be logged
        """
        self.target.moveCursor(QTextCursor.End)
        self.target.insertPlainText(message)