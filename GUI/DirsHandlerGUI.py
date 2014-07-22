# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
from PySide.QtCore import *
from PySide.QtGui import *

from Core import DirsHandlerCore, SharedApp
from GUI import DAWDirsGUI, ReferenceDirsGUI

"""
Interstitial Directory GUI Manager
"""


class DirsHandlerGUI(QWidget):
    """
        Application Directories Handler GUI Class
    """

    def __init__(self):
        """
        Constructor
        """

        super(DirsHandlerGUI, self).__init__()
        self.dirs_handler_core = DirsHandlerCore.DirsHandlerCore()
        self.Interstitial = SharedApp.SharedApp.App
        self.reference_dirs_gui = ReferenceDirsGUI.ReferenceDirsGUI()
        self.daw_dirs_gui = DAWDirsGUI.DAWDirsGUI()
        self.grid = QGridLayout()


    def createDAWDirectories(self):
        """
        Create DAW Directories

        @return: None
        """

        self.grid.addWidget(self.daw_dirs_gui.setupDAWGUI())


    def createRefDirectories(self):
        """
        Create Reference Directories

        @return: None
        """
        self.grid.addWidget(self.reference_dirs_gui.setupReferenceGUI())

    def getGrid(self):
        """
        Get GUI Grid Layout

        @return: None
        """
        return self.grid