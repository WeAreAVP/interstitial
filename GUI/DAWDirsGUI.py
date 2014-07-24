# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *

from Core import SharedApp, DAWDirsCore
from GUI import SharedAppGUI

class DAWDirsGUI(QWidget, DAWDirsCore.DAWDirsCore):

    def __init__(self):

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
        #self.daw_dir_selector.setContentsMargins(100,100,100,100)
        self.daw_dir_text.setMaximumSize(260, 20)
        self.daw_dir_text.setMinimumSize(260, 20)

    def getGuiDawText(self):
        """
        Get Gui Daw Text

        @return:daw_dir_text
        """

        try:
            return str(self.daw_dir_text.text())
        except:
            return str(self.daw_dir_text)
            pass

    def AddWidgets(self, layout):
        """
        Add Widget To Layout

        @return:Layout
        """
        single_line_hanlder = QHBoxLayout()
        single_line_hanlder .addWidget(self.daw_dir_text)
        single_line_hanlder .addWidget(self.daw_dir_selector)

        try:
            single_line_hanlder .addWidget(self.bin_of_dirs)
        except:
            pass
        layout.addRow(single_line_hanlder)

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

        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.daw_dir_text.setText(path_selected)

    def removeDAWDirectory(self):
        """
        Remove DAW Directory Trigger

        @return: None
        """
        try:
            self.daw_dir_selector.deleteLater()
            self.daw_dir_selector.destroy()
            del self.daw_dir_selector
        except:
            pass

        try:
            self.daw_dir_text.deleteLater()
            self.daw_dir_text.destroy()
            del self.daw_dir_text
        except:
            pass

        try:
            self.bin_of_dirs.deleteLater()
            self.bin_of_dirs.destroy()
            del self.bin_of_dirs
        except:
            pass

        self.Interstitial_GUI.dirs_handler_gui.number_of_daw_dirs = self.Interstitial_GUI.dirs_handler_gui.number_of_daw_dirs - 1

        self.Interstitial_GUI.dirs_handler_gui.add_height_daw -= 30
        SharedAppGUI.SharedAppGUI.GUIApp = self.Interstitial_GUI
        SharedAppGUI.SharedAppGUI.GUIApp.updateGeometry()
        QCoreApplication.processEvents()
        del self