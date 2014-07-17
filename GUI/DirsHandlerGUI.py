# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *
from os import path
"""
Interstitial Directory GUI Manager
"""
class DirsHandlerGUI(QWidget):


    def __init__(self):
        """
        Constructor
        """
        super(DirsHandlerGUI, self).__init__()
        pass

    def createDirectoriesInfo(self):
        """
        Create Directories
        """
        self.daw_dir_selector = QPushButton("...", self)
        self.ref_dir_selector = QPushButton("...", self)
        self.manifest_dir_selector = QPushButton("...", self)

        self.daw_dir_text = QLineEdit()
        self.ref_dir_text = QLineEdit()

    def AddWidgets(self, layout):
        """
        Add Widget To Layout
        """
        layout.addWidget(self.daw_dir_text, 0, 1)
        layout.addWidget(self.ref_dir_text, 1, 1)

        layout.addWidget(self.daw_dir_selector, 0, 2)
        layout.addWidget(self.ref_dir_selector, 1, 2)
        layout.addWidget(self.manifest_dir_selector, 2, 2)

        layout.addWidget(QLabel("DAW Directory"), 0, 0)
        layout.addWidget(QLabel("Reference Directory"), 1, 0)
        return layout

    def setTriggers(self):
        """
        Set GUI Triggers
        """
        self.daw_dir_selector.clicked.connect(self.dawDirTrigger)
        self.ref_dir_selector.clicked.connect(self.refDirTrigger)
        self.manifest_dir_selector.clicked.connect(self.manifestTrigger)

        self.daw_dir_text.setReadOnly(True)
        self.ref_dir_text.setReadOnly(True)

    def dawDirTrigger(self):
        """
        DAW Directory Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=path.expanduser('~'))
        self.daw_dir_text.setText(path_selected)

    def refDirTrigger(self):
        """
        Get Reference Directory Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=path.expanduser('~'))
        self.ref_dir_text.setText(path_selected)

    def manifestTrigger(self):
        """
        get Manifest Trigger
        """
        path_selected = QFileDialog.getExistingDirectory(directory=path.expanduser('~'))
        self.manifest_dir_text.setText(path_selected)
