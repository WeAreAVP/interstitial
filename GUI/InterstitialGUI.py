# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

import sys

from PySide.QtCore import *
from PySide.QtGui import *

# Custom Libs

from Core import SharedApp
from GUI import DirsHandlerGUI, SharedAppGUI, AboutInterstitialGUI, NotificationGUI

"""
Interstitial GUI Manager
"""


class InterstitialGUI(QMainWindow):
    """
        Application Interstitial GUI Class
    """

    _instance = None

    @staticmethod
    def getInstance():
        """
        Get Interstitial Gui Instance

        @return :Interstitial Gui Instance
        """
        if not isinstance(InterstitialGUI._instance, InterstitialGUI):
            InterstitialGUI._instance = QWidget.__new__(InterstitialGUI)
            SharedAppGUI.SharedAppGUI.GUIApp = InterstitialGUI._instance
            SharedAppGUI.SharedAppGUI.GUIApp._instance.setup()

        return InterstitialGUI._instance

    def setup(self):
        super(InterstitialGUI, self).__init__()


        self.Interstitial = SharedApp.SharedApp.App
        self.grid_layout = QGridLayout()
        self.vbox = QHBoxLayout()
        self.group_box = QGroupBox(self.Interstitial.label['manifestDest'])

        self.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
        self.setWindowIcon(QIcon(self.Interstitial.Configuration.getLogoSignSmall()))

        self.setMaximumWidth(self.Interstitial.Configuration.getMainWindowWidth())
        self.setMinimumWidth(self.Interstitial.Configuration.getMainWindowWidth())

        # create Menu
        self.createMenu()

        # Set Short Cuts
        self.setShortCuts()

        #Set All Menu
        self.setAllMenus()

        #Set Trigger
        self.setTriggersForMenu()

        self.dirs_handler_gui = DirsHandlerGUI.DirsHandlerGUI()
        self.notification_gui = NotificationGUI.NotificationGUI()

        self.createDirectories()
        self.go = QPushButton(self.Interstitial.label['runLabel'], self)
        self.addWidgetToLayout()
        self.setTriggers()

    def createMenu(self):
         #Creat All Menu
        self.menubar = self.menuBar()
        self.file_manu_fixity = self.menubar.addMenu('&Help')
        self.about_fixity_menu = QAction('&About Interstitial', self)

    def setShortCuts(self):
        #Creat Menu Short Cut
        self.about_fixity_menu.setShortcut('CTRL+,')

    def setAllMenus(self):
        #All Menu to Interstitial
        self.file_manu_fixity.addAction(self.about_fixity_menu)

    def setTriggersForMenu(self):
        #Set Trigger for Menu
        self.about_fixity_menu.triggered.connect(self.AboutInterstitail)

    def AboutInterstitail(self):
        #Launch About Interstitial
        try:
            self.about_fixity_gui.destroy()
        except:
            pass

        self.about_fixity_gui = AboutInterstitialGUI.AboutInterstitialGUI(self)
        self.about_fixity_gui.LaunchDialog()

    def createDirectories(self):
        """
        Create Main Gui

        @return: None
        """

        self.manifest_dir_selector = QPushButton(self.Interstitial.label['dirSelector'], self)
        self.manifest_dir_text = QLineEdit()

        self.manifest_dir_selector.setMaximumSize(50, 20)
        self.manifest_dir_selector.setMinimumSize(50, 20)

        self.manifest_dir_text.setMaximumSize(420, 25)
        self.manifest_dir_text.setMinimumSize(420, 25)

        self.manifest_dir_text.setReadOnly(True)

        self.grid_layout.addWidget(self.dirs_handler_gui.createDAWDirectories())
        self.grid_layout.addWidget(self.dirs_handler_gui.add_new_daw)

        self.grid_layout.addWidget(self.dirs_handler_gui.createRefDirectories())
        self.grid_layout.addWidget(self.dirs_handler_gui.add_new_ref)

        self.qwidget = QWidget()
        self.qwidget.setLayout(self.grid_layout)
        self.setCentralWidget(self.qwidget)

    def addWidgetToLayout(self):
        """
        Add Widget To Layout

        @return: None
        """
        self.vbox.addWidget(self.manifest_dir_text)
        self.vbox.addWidget(self.manifest_dir_selector)
        self.vbox.addWidget(self.go)

        self.vbox.addStretch(1)

        self.group_box.setLayout(self.vbox)
        self.group_box.setMinimumHeight(70)
        self.group_box.setMaximumHeight(70)
        self.grid_layout.addWidget(self.group_box)

    def setTriggers(self):
        """
        Set GUI Triggers

        @return: None
        """

        self.go.clicked.connect(self.ErrorVerifier)
        self.manifest_dir_text.setText(self.Interstitial.Configuration.getBasePath())

        self.manifest_dir_selector.clicked.connect(self.manifestTrigger)

    def manifestTrigger(self):
        """
        get Manifest Trigger

        @return: None
        """
        manifest_path_selector = QFileDialog()
        manifest_path_selector.setDirectory(self.Interstitial.Configuration.getBasePath())
        path_selected = manifest_path_selector.getExistingDirectory()
        self.manifest_dir_text.setText(path_selected)

    def ErrorVerifier(self):
        """
        Look For Errors in Provided Wav Files

        @return: None
        """
        for index_daw in xrange(0, self.dirs_handler_gui.number_of_daw_dirs):
            if self.dirs_handler_gui.daw_dirs_gui[index_daw].getGuiDawText() == '':
                self.notification_gui.showWarning(self,'Invalid Data', self.Interstitial.messages['daw_empty_msg'])
                return
        for index_ref in xrange(0, self.dirs_handler_gui.number_of_ref_dirs):
            if self.dirs_handler_gui.reference_dirs_gui[index_ref].getGuiRefText() == '':
                self.notification_gui.showWarning(self,'Invalid Data', self.Interstitial.messages['ref_empty_msg'])
                return

        report_detail_dialog_box = QDialog(self)

        report_detail_dialog_box.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
        report_detail_dialog_box.setWindowIcon(QIcon(self.Interstitial.Configuration.getLogoSignSmall()))

        report_detail_dialog_box.setWindowModality(Qt.WindowModal)

        report_detail_exit_btn = QPushButton(self.Interstitial.label['exit'], self)
        report_detail_text = QTextEdit(self)
        report_detail_layout = QVBoxLayout(report_detail_dialog_box)

        report_detail_exit_btn.setEnabled(False)
        report_detail_text.setReadOnly(True)

        report_detail_exit_btn.clicked.connect(self.close)

        report_detail_layout.addWidget(report_detail_text)
        report_detail_layout.addWidget(report_detail_exit_btn)

        report_detail_dialog_box.setLayout(report_detail_layout)

        sys.stdout = Printer(report_detail_text)

        report_detail_dialog_box.resize(1000, 300)
        report_detail_dialog_box.show()

        self.dirs_handler_gui.RunExecutor(str(self.manifest_dir_text.text()))

        report_detail_exit_btn.setEnabled(True)

# printer
# allows for writing to a QWindow

class Printer():

    def __init__(self, target):
        self.target = target

    def write(self, message):
        self.target.moveCursor(QTextCursor.End)
        self.target.insertPlainText(message)