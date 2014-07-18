# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *
from os import path

from Config import Configuration
"""
Interstitial Directory GUI Manager
"""


class DirsHandlerGUI(QWidget):


    def __init__(self):
        """
        Constructor
        """
        super(DirsHandlerGUI, self).__init__()
        self.configuration = Configuration.Configuration()
        pass

    #def createDirectoriesInfo(self):
    #    """
    #    Create Directories
    #    """
    #    self.daw_dir_selector_gui = QPushButton("...", self)
    #    self.ref_dir_selector_gui = QPushButton("...", self)
    #
    #
    #    self.daw_dir_text = QLineEdit()
    #    self.ref_dir_text = QLineEdit()

    def addNewDirSet(self):
        """
        Create Directories
        """
        groupBox = QGroupBox("Exclusive Radio Buttons")

        self.daw_dir_selector_gui = QPushButton("...", self)
        self.ref_dir_selector_gui = QPushButton("...", self)

        self.daw_dir_label = QLabel("DAW Directory")
        self.ref_dir_label = QLabel("Reference Directory")

        self.daw_dir_text = QLineEdit()
        self.ref_dir_text = QLineEdit()

        vBox = QVBoxLayout()

        #self.daw_dir_label.setFixedSize(130, 20)
        #self.ref_dir_label.setFixedSize(130, 20)

        #self.daw_dir_text.setFixedSize(180, 20)
        #self.ref_dir_text.setFixedSize(180, 20)

        #self.daw_dir_selector_gui.setFixedSize(30, 18)
        #self.ref_dir_selector_gui.setFixedSize(30, 18)

        vBox.addWidget(self.daw_dir_label) #, 0, 0
        vBox.addWidget(self.ref_dir_label) #, 1, 0

        vBox.addWidget(self.daw_dir_text) #, 0, 1
        vBox.addWidget(self.ref_dir_text) #, 1, 1

        vBox.addWidget(self.daw_dir_selector_gui) #, 0, 2
        vBox.addWidget(self.ref_dir_selector_gui) #, 1, 2

        vBox.addStretch(1)

        groupBox.setLayout(vBox)

        return groupBox

    #def AddWidgets(self, layout ):
    #    """
    #    Add Widget To Layout
    #    """
    #    self.daw_dir_label = QLabel("DAW Directory")
    #    self.ref_dir_label = QLabel("Reference Directory")
    #
    #    self.daw_dir_label.setFixedSize(130, 20)
    #    self.ref_dir_label.setFixedSize(130, 20)
    #
    #    self.daw_dir_text.setFixedSize(180, 20)
    #    self.ref_dir_text.setFixedSize(180, 20)
    #
    #    self.daw_dir_selector_gui.setFixedSize(30, 18)
    #    self.ref_dir_selector_gui.setFixedSize(30, 18)
    #
    #    layout.addWidget(self.daw_dir_label) #, 0, 0
    #    layout.addWidget(self.ref_dir_label) #, 1, 0
    #
    #    layout.addWidget(self.daw_dir_text) #, 0, 1
    #    layout.addWidget(self.ref_dir_text) #, 1, 1
    #
    #    layout.addWidget(self.daw_dir_selector_gui) #, 0, 2
    #    layout.addWidget(self.ref_dir_selector_gui) #, 1, 2
    #
    #    return layout

    #def setTriggers(self):
    #    """
    #    Set GUI Triggers
    #    """
    #    self.daw_dir_selector_gui.clicked.connect(self.dawDirTrigger)
    #    self.ref_dir_selector_gui.clicked.connect(self.refDirTrigger)
    #
    #    self.daw_dir_text.setReadOnly(True)
    #    self.ref_dir_text.setReadOnly(True)

    def dawDirTrigger(self):
        """
        DAW Directory Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=self.configuration.getUserHomePath())
        self.daw_dir_text.setText(path_selected)

    def refDirTrigger(self):
        """
        Get Reference Directory Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=self.configuration.getUserHomePath())
        self.ref_dir_text.setText(path_selected)

    def getDaw(self):
        """
        Get DAW
        """
        return self.daw_dir_text.text()

    def getRefDir(self):
        """
        Get Reference Directory
        """
        return self.ref_dir_selector_gui.text()