# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *
from os import path

from Core import DirsHandlerCore, SharedApp
"""
Interstitial Directory GUI Manager
"""


class DirsHandlerGUI(QWidget):


    def __init__(self):
        """
        Constructor
        """
        super(DirsHandlerGUI, self).__init__()
        self.dirs_handler_core = DirsHandlerCore.DirsHandlerCore()
        self.Interstitial = SharedApp.SharedApp.App

        pass

    def createDirectoriesInfo(self):
        """
        Create Directories
        """
        self.daw_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)
        self.ref_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)

        self.daw_dir_text = QLineEdit()
        self.ref_dir_text = QLineEdit()

    def getGuiDawText(self):
        """
        Get Gui Daw Text

        @return daw_dir_text
        """
        return self.daw_dir_text.text()

    def getGuiRefText(self):
        """
        Get Gui Ref Text

        @return ref_dir_text
        """
        return self.ref_dir_text.text()

    def AddWidgets(self, layout):
        """
        Add Widget To Layout

        @return Layout
        """
        layout.addWidget(self.daw_dir_text, 0, 1)
        layout.addWidget(self.ref_dir_text, 1, 1)

        layout.addWidget(self.daw_dir_selector, 0, 2)
        layout.addWidget(self.ref_dir_selector, 1, 2)

        layout.addWidget(QLabel(self.Interstitial.label['DAWDir']), 0, 0)
        layout.addWidget(QLabel(self.Interstitial.label['refDir']), 1, 0)
        return layout

    def setTriggers(self):
        """
        Set GUI Triggers
        """
        self.daw_dir_selector.clicked.connect(self.dawDirTrigger)
        self.ref_dir_selector.clicked.connect(self.refDirTrigger)

        self.daw_dir_text.setReadOnly(True)
        self.ref_dir_text.setReadOnly(True)

    def dawDirTrigger(self):
        """
        DAW Directory Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.daw_dir_text.setText(path_selected)
        #self.dirs_handler_core

    def refDirTrigger(self):
        """
        Get Reference Directory Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.ref_dir_text.setText(path_selected)

