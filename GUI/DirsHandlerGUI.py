# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtCore import *

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

        self.Interstitial = SharedApp.SharedApp.App

        self.daw_dirs_gui = {}
        self.reference_dirs_gui = {}

        self.number_of_daw_dirs = 1
        self.number_of_ref_dirs = 1

        self.daw_group_box = QGroupBox(self.Interstitial.label['DAWDir'])
        self.ref_group_box = QGroupBox(self.Interstitial.label['refDir'])

        self.add_height_daw = 100
        self.add_height_ref = 100

        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw] = DAWDirsGUI.DAWDirsGUI()
            self.add_height_daw = self.add_height_daw + 55

        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref] = ReferenceDirsGUI.ReferenceDirsGUI()
            self.add_height_ref = self.add_height_ref + 55

        self.ref_group_box.setMinimumSize(520, self.add_height_ref)
        self.daw_group_box.setMinimumSize(520, self.add_height_daw)

        self.daw_qv_box = QVBoxLayout()
        self.ref_qv_box = QVBoxLayout()

    def createDAWDirectories(self):
        """
        Create DAW Directories

        @return: None
        """

        return self.setupDAWGUI()

    def setupDAWGUI(self):
        """
        Setup Reference DAW Box Layout

        @return: daw_group_box
        """

        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw].createDirectoriesInfo()
            self.daw_dirs_gui[index_daw].setTriggers()

        self.add_new_daw = QPushButton(self.Interstitial.label['addnew'], self)
        self.add_new_daw.setMaximumSize(100, 100)

        self.add_new_daw.clicked.connect(self.addNewDawDirectory)

        for index_ref in xrange(0, self.number_of_daw_dirs):
            self.daw_qv_box = self.daw_dirs_gui[index_ref].AddWidgets(self.daw_qv_box)

        self.daw_qv_box.addWidget(self.add_new_daw, 0, 3)
        self.daw_qv_box.addStretch(1)
        self.daw_group_box.setLayout(self.daw_qv_box)

        return self.daw_group_box

    def setupReferenceGUI(self):
        """
        Setup Reference GUI Box Layout

        @return: reference_group_box
        """

        self.add_new_ref = QPushButton(self.Interstitial.label['addnew'], self)
        self.add_new_ref.setMaximumSize(100, 100)

        self.add_new_ref.clicked.connect(self.addNewRefDirectory)

        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref].createDirectoriesInfo()
            self.reference_dirs_gui[index_ref].setTriggers()
            self.ref_qv_box = self.reference_dirs_gui[index_ref].AddWidgets(self.ref_qv_box)

        self.ref_qv_box.addWidget(self.add_new_ref, 0, 3)
        self.ref_qv_box.addStretch(1)
        self.ref_group_box.setLayout(self.ref_qv_box)

        return self.ref_group_box

    def createRefDirectories(self):
        """
        Create Reference Directories

        @return: None
        """
        return self.setupReferenceGUI()

    def addNewDawDirectory(self):
        print('addNewDawDirectory')
        pass

    def addNewRefDirectory(self):
        print('addNewRefDirectory')
        pass
