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
        self.dirs_handler_core = DirsHandlerCore.DirsHandlerCore()

        self.daw_dirs_gui = {}
        self.reference_dirs_gui = {}

        self.number_of_daw_dirs = 1
        self.number_of_ref_dirs = 1

        self.daw_group_box = QGroupBox(self.Interstitial.label['DAWDir'])
        self.ref_group_box = QGroupBox(self.Interstitial.label['refDir'])

        self.add_height_daw = 60
        self.add_height_ref = 60

        # Adding Space for new Directories in Group Box
        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw] = DAWDirsGUI.DAWDirsGUI()
            self.add_height_daw += 90

        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref] = ReferenceDirsGUI.ReferenceDirsGUI()
            self.add_height_ref += 90

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

        # Create & Load Widgets and Triggers for Reference DAW
        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw].createDirectoriesInfo()
            self.daw_dirs_gui[index_daw].setTriggers()
            self.daw_qv_box = self.daw_dirs_gui[index_daw].AddWidgets(self.daw_qv_box)

        # Load New Add Buttons Widget , Trigger
        self.add_new_daw = QPushButton(self.Interstitial.label['addNewDAW'], self)
        self.add_new_daw.clicked.connect(self.addNewDawDirectory)
        self.add_new_daw.setMaximumSize(140, 100)
        self.daw_qv_box.addWidget(self.add_new_daw, 0, 3)

        self.daw_qv_box.addStretch(1)
        self.daw_group_box.setLayout(self.daw_qv_box)

        return self.daw_group_box

    def setupReferenceGUI(self):
        """
        Setup Reference GUI Box Layout

        @return: reference_group_box
        """

        # Create & Load Widgets and Triggers for Reference GUI
        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref].createDirectoriesInfo()
            self.reference_dirs_gui[index_ref].setTriggers()
            self.ref_qv_box = self.reference_dirs_gui[index_ref].AddWidgets(self.ref_qv_box)

        # Load New Add Buttons Widget , Trigger
        self.add_new_ref = QPushButton(self.Interstitial.label['addNewRef'], self)
        self.add_new_ref.clicked.connect(self.addNewReferenceDirectory)
        self.add_new_ref.setMaximumSize(170, 100)
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
        """
        Add New Daw Directory

        @return: None
        """


        self.daw_dirs_gui[self.number_of_daw_dirs] = DAWDirsGUI.DAWDirsGUI()

        self.daw_dirs_gui[self.number_of_daw_dirs].createDirectoriesInfo()
        self.daw_dirs_gui[self.number_of_daw_dirs].setTriggers()
        self.daw_qv_box = self.daw_dirs_gui[self.number_of_daw_dirs].AddWidgets(self.daw_qv_box)
        self.add_height_daw += 60
        self.daw_group_box.setMinimumSize(520, self.add_height_daw)
        self.daw_group_box.setLayout(self.daw_qv_box)

        self.number_of_daw_dirs += 1
        QCoreApplication.processEvents()

    def addNewReferenceDirectory(self):
        """
        Add New Reference Directory

        @return: None
        """


        self.reference_dirs_gui[self.number_of_ref_dirs] = ReferenceDirsGUI.ReferenceDirsGUI()

        self.reference_dirs_gui[self.number_of_ref_dirs].createDirectoriesInfo()
        self.reference_dirs_gui[self.number_of_ref_dirs].setTriggers()

        self.ref_qv_box = self.reference_dirs_gui[self.number_of_ref_dirs].AddWidgets(self.ref_qv_box)

        self.add_height_ref += 60
        self.ref_group_box.setMinimumSize(520, self.add_height_ref)
        self.ref_group_box.setLayout(self.ref_qv_box)
        self.number_of_ref_dirs += 1
        QCoreApplication.processEvents()

    def RunExecutor(self, manifest_path):
        """
        Run  Executor To Test Audio File

        @return: None
        """

        for index_daw in xrange(0, self.number_of_daw_dirs):
            for index_ref in xrange(0, self.number_of_ref_dirs):

                # Set DAW Core Information
                self.daw_dirs_gui[index_daw].setCoreDawId('daw' + str(index_daw))
                self.daw_dirs_gui[index_daw].setCoreDawText(self.daw_dirs_gui[index_daw].getGuiDawText())

                # Set Reference Core Information
                self.reference_dirs_gui[index_ref].setCoreRefId('daw' + str(index_ref))
                self.reference_dirs_gui[index_ref].setCoreRefText(self.reference_dirs_gui[index_ref].getGuiRefText())


                # Set Directories Core Information to be used for executor
                self.dirs_handler_core.setCoreDawText(self.daw_dirs_gui[index_daw].getGuiDawText())
                self.dirs_handler_core.setCoreRefText(self.reference_dirs_gui[index_ref].getGuiRefText())


                # Launch The Scanner to Test Audio Files
                self.dirs_handler_core.execute(manifest_path, QCoreApplication.instance())