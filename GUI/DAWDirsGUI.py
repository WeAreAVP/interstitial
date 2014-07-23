# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtGui import *

from Core import SharedApp, DAWDirsCore


class DAWDirsGUI(QWidget, DAWDirsCore.DAWDirsCore):

    def __init__(self):

        super(DAWDirsGUI, self).__init__()
        self.Interstitial = SharedApp.SharedApp.App
        pass

    def createDirectoriesInfo(self):
        """
        Create Directories

        @return: None
        """

        self.daw_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)
        self.daw_dir_text = QLineEdit()

        self.daw_dir_selector.setMaximumSize(50, 100)
        self.daw_dir_text.setMaximumSize(410, 100)

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

        layout.addWidget(self.daw_dir_text)
        layout.addWidget(self.daw_dir_selector, 0, 2)

        separator = QLabel('_______________________________________________________________________________________')
        separator.setStyleSheet("QLabel { color : #FBFBF9; }")
        layout.addWidget(separator, 0, 1)

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
