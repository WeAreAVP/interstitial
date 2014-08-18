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

from Core import SharedApp, DAWDirsCore
from GUI import SharedAppGUI


class DAWDirsGUI(QWidget, DAWDirsCore.DAWDirsCore):

    def __init__(self):
        """
        Constructor
        """
        super(DAWDirsGUI, self).__init__()
        self.Interstitial = SharedApp.SharedApp.App
        self.Interstitial_GUI = SharedAppGUI.SharedAppGUI.GUIApp

    def createDirectoriesInfo(self, number_of_daw_dirs=2):
        """
        Create Directories

        @return: None
        """
        self.daw_dir_text = QLineEdit()
        self.daw_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)

        if number_of_daw_dirs > 1:
            self.bin_of_dirs = QPushButton('X')
            self.bin_of_dirs.setMaximumSize(30, 20)
            self.bin_of_dirs.setStyleSheet('QPushButton {color: red; font: bold;}')
            self.bin_of_dirs.clicked.connect(self.removeDAWDirectory)

        self.daw_dir_selector.setMaximumSize(50, 20)
        self.daw_dir_selector.setMinimumSize(50, 20)

        self.daw_dir_text.setMaximumSize(460, 20)
        self.daw_dir_text.setMinimumSize(460, 20)

    def getGuiDawText(self):
        """
        Get Gui Daw Text

        @return:daw_dir_text
        """

        try:

            return self.daw_dir_text.text()
        except:
            print(Exception.message)
            pass

    def AddWidgets(self, layout):
        """
        Add Widget To Layout

        @return:Layout
        """

        self.single_line_hanlder = QHBoxLayout()

        if self.Interstitial.Configuration.getOsType() == 'linux':
            self.single_line_hanlder.setSpacing(10)

        self.single_line_hanlder .addWidget(self.daw_dir_text)
        self.single_line_hanlder .addWidget(self.daw_dir_selector)

        try:
            self.single_line_hanlder.addWidget(self.bin_of_dirs)
        except:
            pass

        layout.addRow(self.single_line_hanlder)

        return layout

    def setTriggers(self):
        """
        Set GUI Triggers

        @return: None
        """

        self.daw_dir_selector.clicked.connect(self.dawDirTrigger)

        #self.daw_dir_text.setReadOnly(True)

    def dawDirTrigger(self):
        """
        DAW Directory Trigger

        @return: None
        """
        daw_path_selector = QFileDialog()
        daw_path_selector.setDirectory(self.Interstitial.Configuration.getUserHomePath())
        path_selected = daw_path_selector.getExistingDirectory()

        self.daw_dir_text.setText(path_selected)

    def removeDAWDirectory(self):
        """
        Remove DAW Directory Trigger
        Destroy this Daw directory's Path Selector , Delete button and path text field

        @return: None
        """
        self.Interstitial_GUI.dirs_handler_gui.loading_daw_label.setHidden(False)
        QCoreApplication.processEvents()
        
        self.single_line_hanlder.deleteLater()
        self.daw_dir_text.deleteLater()
        self.bin_of_dirs.deleteLater()
        self.daw_dir_selector.deleteLater()

        self.Interstitial_GUI.dirs_handler_gui.daw_qh_box.removeWidget(self.daw_dir_selector)
        self.Interstitial_GUI.dirs_handler_gui.daw_qh_box.removeWidget(self.daw_dir_text)
        self.Interstitial_GUI.dirs_handler_gui.daw_qh_box.removeWidget(self.bin_of_dirs)

        QCoreApplication.processEvents()

        self.daw_dir_selector.destroy()
        self.daw_dir_text.destroy()
        self.bin_of_dirs.destroy()

        # DAW Directory Text Removing
        del self.daw_dir_selector

        # Delete Layout For One Directory
        del self.single_line_hanlder

        # DAW Directory Text Delete button
        del self.daw_dir_text

        # DAW Directory Text Delete button
        del self.bin_of_dirs

        self.Interstitial_GUI.dirs_handler_gui.number_of_daw_dirs -= 1

        SharedAppGUI.SharedAppGUI.GUIApp = self.Interstitial_GUI
        SharedAppGUI.SharedAppGUI.GUIApp.updateGeometry()
        SharedAppGUI.SharedAppGUI.GUIApp.adjustSize()

        if self.Interstitial_GUI.dirs_handler_gui.number_of_daw_dirs < 7:
            self.Interstitial_GUI.dirs_handler_gui.add_new_daw.setDisabled(False)

        self.Interstitial_GUI.dirs_handler_gui.loading_daw_label.setHidden(True)
        QCoreApplication.processEvents()
        del self