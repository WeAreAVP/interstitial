# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

from PySide.QtCore import *
from PySide.QtGui import *
from time import strftime, time
from math import floor

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

        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw] = DAWDirsGUI.DAWDirsGUI()

        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref] = ReferenceDirsGUI.ReferenceDirsGUI()


        self.daw_qh_box = QFormLayout()
        self.ref_qh_box = QFormLayout()

        if self.Interstitial.Configuration.getOsType() == 'linux':
            self.daw_qh_box.setSpacing(0)
            self.ref_qh_box.setSpacing(0)

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
        self.loading_daw_label = QLabel('Please Wait.....Removing DAW Directory!')
        self.loading_daw_label.setHidden(True)
        self.daw_qh_box.addWidget(self.loading_daw_label)

        # Create & Load Widgets and Triggers for Reference DAW
        for index_daw in xrange(0, self.number_of_daw_dirs):
            self.daw_dirs_gui[index_daw].createDirectoriesInfo(self.number_of_daw_dirs)
            self.daw_dirs_gui[index_daw].setTriggers()
            self.daw_qh_box = self.daw_dirs_gui[index_daw].AddWidgets(self.daw_qh_box)

        # Load New Add Buttons Widget , Trigger
        self.add_new_daw = QPushButton(self.Interstitial.label['addNewDAW'], self)
        self.add_new_daw.clicked.connect(self.addNewDawDirectory)

        if self.Interstitial.Configuration.getOsType() == 'windows':
            self.add_new_daw.setMaximumSize(140, 30)
            self.add_new_daw.setMinimumSize(140, 30)
        else:
            self.add_new_daw.setMaximumSize(200, 30)
            self.add_new_daw.setMinimumSize(200, 30)

        self.daw_qh_box.addWidget(self.add_new_daw)

        self.daw_group_box.setLayout(self.daw_qh_box)

        return self.daw_group_box

    def setupReferenceGUI(self):
        """
        Setup Reference GUI Box Layout

        @return: reference_group_box
        """
        self.loading_ref_label = QLabel('Please Wait.....Removing Reference Directory!')
        self.loading_ref_label.setHidden(True)
        self.ref_qh_box.addWidget(self.loading_ref_label)

        # Create & Load Widgets and Triggers for Reference GUI
        for index_ref in xrange(0, self.number_of_ref_dirs):
            self.reference_dirs_gui[index_ref].createDirectoriesInfo(self.number_of_ref_dirs)
            self.reference_dirs_gui[index_ref].setTriggers()
            self.ref_qh_box = self.reference_dirs_gui[index_ref].AddWidgets(self.ref_qh_box)

        # Load New Add Buttons Widget , Trigger
        self.add_new_ref = QPushButton(self.Interstitial.label['addNewRef'], self)
        self.add_new_ref.clicked.connect(self.addNewReferenceDirectory)
        self.ref_qh_box.addWidget(self.add_new_ref)

        self.add_new_ref.setMaximumSize(220, 30)
        self.add_new_ref.setMinimumSize(220, 30)

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
        self.daw_group_box.setLayout(self.daw_qh_box)

        self.number_of_daw_dirs += 1

        if self.number_of_daw_dirs == 7:
            self.add_new_daw.setDisabled(True)

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
        self.ref_group_box.setLayout(self.ref_qh_box)

        self.number_of_ref_dirs += 1
        if self.number_of_ref_dirs == 7:
            self.add_new_ref.setDisabled(True)

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
                self.dirs_handler_core.setDawDirsCore(self.daw_dirs_gui[index_daw].getGuiDawText(), index_daw)
                self.dirs_handler_core.setRefDirsCore(self.reference_dirs_gui[index_ref].getGuiRefText(), index_ref)

        # Launch The Scanner to Test Audio Files
        self.dirs_handler_core.run_executor(manifest_path, QCoreApplication.instance())