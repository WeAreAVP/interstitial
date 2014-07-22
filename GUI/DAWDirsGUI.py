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

    def setupDAWGUI(self):
        group_box = QGroupBox("Exclusive Radio Buttons")
        vbox = QVBoxLayout()
        self.createDirectoriesInfo()

        vbox = self.AddWidgets(vbox)
        vbox.addStretch(1)

        group_box.setLayout(vbox)

        return group_box

    def createDirectoriesInfo(self):
        """
        Create Directories

        @return: None
        """

        self.daw_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)

        self.daw_dir_text = QLineEdit()

    def getGuiDawText(self):
        """
        Get Gui Daw Text

        @return:daw_dir_text
        """

        return self.daw_dir_text.text()


    def AddWidgets(self, layout):
        """
        Add Widget To Layout

        @return:Layout
        """

        layout.addWidget(self.daw_dir_text, 0, 1)

        layout.addWidget(self.daw_dir_selector, 0, 2)

        layout.addWidget(QLabel(self.Interstitial.label['DAWDir']), 0, 0)
        return layout

    def setTriggers(self):
        """
        Set GUI Triggers

        @return: None
        """

        self.daw_dir_selector.clicked.connect(self.dawDirTrigger)

        self.daw_dir_text.setReadOnly(True)

    def dawDirTrigger(self):
        """
        DAW Directory Trigger

        @return: None
        """

        path_selected = QFileDialog.getExistingDirectory(directory=self.Interstitial.Configuration.getUserHomePath())
        self.daw_dir_text.setText(path_selected)
        #self.dirs_handler_core