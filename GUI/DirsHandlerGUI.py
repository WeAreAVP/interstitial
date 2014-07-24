# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *

from Core import DirsHandlerCore, SharedApp
from GUI import DAWDirsGUI, ReferenceDirsGUI

import time


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

        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw] = DAWDirsGUI.DAWDirsGUI()

        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref] = ReferenceDirsGUI.ReferenceDirsGUI()

        self.ref_group_box.setMinimumSize(350, self.add_height_ref)
        self.daw_group_box.setMinimumSize(350, self.add_height_daw)

        self.daw_qh_box = QFormLayout()
        self.ref_qh_box = QFormLayout()

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
            self.daw_dirs_gui[index_daw].createDirectoriesInfo(self.number_of_daw_dirs)
            self.daw_dirs_gui[index_daw].setTriggers()
            self.daw_qh_box = self.daw_dirs_gui[index_daw].AddWidgets(self.daw_qh_box)

        # Load New Add Buttons Widget , Trigger
        self.add_new_daw = QPushButton(self.Interstitial.label['addNewDAW'], self)
        self.add_new_daw.clicked.connect(self.addNewDawDirectory)

        self.add_new_daw.setMaximumSize(140, 30)
        self.add_new_daw.setMinimumSize(140, 30)


        self.daw_qh_box.addWidget(self.add_new_daw)

        self.daw_group_box.setLayout(self.daw_qh_box)
        print(self.daw_group_box.height())
        return self.daw_group_box

    def setupReferenceGUI(self):
        """
        Setup Reference GUI Box Layout

        @return: reference_group_box
        """

        # Create & Load Widgets and Triggers for Reference GUI
        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref].createDirectoriesInfo(self.number_of_ref_dirs)
            self.reference_dirs_gui[index_ref].setTriggers()
            self.ref_qh_box = self.reference_dirs_gui[index_ref].AddWidgets(self.ref_qh_box)

        # Load New Add Buttons Widget , Trigger
        self.add_new_ref = QPushButton(self.Interstitial.label['addNewRef'], self)
        self.add_new_ref.clicked.connect(self.addNewReferenceDirectory)
        self.add_new_ref.setMaximumSize(170, 100)
        self.ref_qh_box.addWidget(self.add_new_ref)

        self.add_new_ref.setMaximumSize(170, 30)
        self.add_new_ref.setMinimumSize(170, 30)


        self.ref_group_box.setLayout(self.ref_qh_box)

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
        self.daw_qh_box = self.daw_dirs_gui[self.number_of_daw_dirs].AddWidgets(self.daw_qh_box)

        # Adding Space for new Directories in Group Box
        self.add_height_daw += 30

        self.daw_group_box.setMinimumSize(350, self.add_height_daw)
        self.ref_group_box.setMinimumSize(350, self.add_height_ref)

        self.daw_group_box.setLayout(self.daw_qh_box)

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

        self.ref_qh_box = self.reference_dirs_gui[self.number_of_ref_dirs].AddWidgets(self.ref_qh_box)

        # Adding Space for new Directories in Group Box
        self.add_height_ref += 30

        self.ref_group_box.setMinimumSize(350, self.add_height_ref)
        self.daw_group_box.setMinimumSize(350, self.add_height_daw)

        self.ref_vh_box = QVBoxLayout()
        self.ref_group_box.setLayout(self.ref_qh_box)

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
                self.reference_dirs_gui[index_ref].setCoreRefId('ref' + str(index_ref))
                self.reference_dirs_gui[index_ref].setCoreRefText(self.reference_dirs_gui[index_ref].getGuiRefText())

                # Set Directories Core Information to be used for executor
                self.dirs_handler_core.setCoreDawText(self.daw_dirs_gui[index_daw].getGuiDawText())
                self.dirs_handler_core.setCoreRefText(self.reference_dirs_gui[index_ref].getGuiRefText())

                # Launch The Scanner to Test Audio Files
                self.dirs_handler_core.execute(manifest_path, QCoreApplication.instance())
                time.sleep(2)