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


    def createDirectoriesInfo(self):
        """
        Create Directories

        @return: None
        """
        
        self.daw_dirs_gui.createDirectoriesInfo()
        self.reference_dirs_gui.createDirectoriesInfo()

    def AddWidgets(self, layout):
        """
        Add Widget To Layout

        @return:Layout
        """
        self.daw_dirs_gui.AddWidgets(layout)
        self.reference_dirs_gui.AddWidgets(layout)

        return layout

    def setTriggers(self):
        """
        Set GUI Triggers

        @return: None
        """

        self.daw_dirs_gui.setTriggers()
        self.reference_dirs_gui.setTriggers()