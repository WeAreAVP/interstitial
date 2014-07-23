# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtGui import *

from Core import SharedApp, ReferenceDirsCore

class ReferenceDirsGUI(QWidget, ReferenceDirsCore.ReferenceDirsCore):

    def __init__(self):
        super(ReferenceDirsGUI, self).__init__()
        self.Interstitial = SharedApp.SharedApp.App

    def createDirectoriesInfo(self):
        """
        Create Directories

        @return: None
        """

        self.ref_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)
        self.ref_dir_text = QLineEdit()

        self.ref_dir_selector.move(55, 70)
        self.ref_dir_text.move(55, 70)

        self.ref_dir_selector.setMaximumSize(50, 100)
        self.ref_dir_text.setMaximumSize(410, 100)

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

        layout.addWidget(self.ref_dir_text)
        layout.addWidget(self.ref_dir_selector, 0, 2)

        separator = QLabel('________________________________________________________________________________')
        separator.setStyleSheet("QLabel { color : #FBFBF9;}")
        layout.addWidget(separator, 0, 1)

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