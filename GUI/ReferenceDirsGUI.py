# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *

from Core import SharedApp, ReferenceDirsCore
from GUI import SharedAppGUI


class ReferenceDirsGUI(QWidget, ReferenceDirsCore.ReferenceDirsCore):

    def __init__(self):
        super(ReferenceDirsGUI, self).__init__()
        self.Interstitial = SharedApp.SharedApp.App
        self.Interstitial_GUI = SharedAppGUI.SharedAppGUI.GUIApp

    def createDirectoriesInfo(self, number_of_ref_dirs=2):
        """
        Create Directories

        @return: None
        """
        self.ref_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)
        self.ref_dir_text = QLineEdit()

        if number_of_ref_dirs > 1:
            self.bin_of_dirs = QPushButton('X')
            self.bin_of_dirs.setStyleSheet('QPushButton {color: red; font: bold;}')
            self.bin_of_dirs.setMaximumSize(30, 20)
        try:
            self.bin_of_dirs.clicked.connect(self.removeReferenceDirectory)
        except:
            pass

        self.ref_dir_selector.setMaximumSize(50, 20)
        self.ref_dir_selector.setMinimumSize(50, 20)
        self.ref_dir_selector.setContentsMargins(0,0,0,0)

        self.ref_dir_text.setMaximumSize(460, 20)
        self.ref_dir_text.setMinimumSize(460, 20)
        self.ref_dir_text.setContentsMargins(0,0,0,0)

        try:
            self.bin_of_dirs.setContentsMargins(0,0,0,0)
        except:
            pass


    def getGuiRefText(self):
        """
        Get Gui Ref Text

        @return:ref_dir_text
        """

        try:
            return str(self.ref_dir_text.text())
        except:
            return str(self.ref_dir_text)
            pass

    def AddWidgets(self, layout):
        """
        Add Widget To Layout

        @return:Layout
        """
        self.single_line_hanlder = QHBoxLayout()
        self.single_line_hanlder .addWidget(self.ref_dir_text)
        self.single_line_hanlder .addWidget(self.ref_dir_selector)

        try:
            self.single_line_hanlder .addWidget(self.bin_of_dirs)
        except:
            pass
        layout.addRow(self.single_line_hanlder)

        return layout

    def setTriggers(self):
        """
        Set GUI Triggers

        @return: None
        """

        self.ref_dir_selector.clicked.connect(self.refDirTrigger)
        #self.ref_dir_text.setReadOnly(True)

    def refDirTrigger(self):
        """
        Get Reference Directory Trigger

        @return: None
        """

        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.ref_dir_text.setText(path_selected)

    def removeReferenceDirectory(self):
        """
        Remove Reference Directory

        @return: None
        """

        try:
            self.Interstitial_GUI.dirs_handler_gui.daw_qh_box.removeWidget(self.ref_dir_selector)
        except:
            pass

        try:
            self.Interstitial_GUI.dirs_handler_gui.daw_qh_box.removeWidget(self.ref_dir_text)
        except:
            pass

        try:
            self.Interstitial_GUI.dirs_handler_gui.daw_qh_box.removeWidget(self.bin_of_dirs)
        except:
            pass

        try:
            self.ref_dir_selector.deleteLater()
            self.ref_dir_selector.destroy()
            del self.ref_dir_selector
        except:
            pass

        try:
            self.ref_dir_text.deleteLater()
            self.ref_dir_text.destroy()
            del self.ref_dir_text
        except:
            pass

        try:
            self.bin_of_dirs.deleteLater()
            self.bin_of_dirs.destroy()
            del self.bin_of_dirs
        except:
            pass

        try:
            self.single_line_hanlder.deleteLater()
            self.single_line_hanlder.destroy()
            del self.single_line_hanlder
        except:
            pass

        self.Interstitial_GUI.dirs_handler_gui.number_of_ref_dirs -= 1

        SharedAppGUI.SharedAppGUI.GUIApp = self.Interstitial_GUI
        SharedAppGUI.SharedAppGUI.GUIApp.updateGeometry()
        SharedAppGUI.SharedAppGUI.GUIApp.adjustSize()

        if self.Interstitial_GUI.dirs_handler_gui.number_of_ref_dirs < 7:
            self.Interstitial_GUI.dirs_handler_gui.add_new_ref.setDisabled(False)

        QCoreApplication.processEvents()
        del self