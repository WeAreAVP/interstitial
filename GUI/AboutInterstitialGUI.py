'''
# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on Aug 6, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>
'''

from PySide.QtCore import *
from PySide.QtGui import *
import webbrowser
from Core import SharedApp



class AboutInterstitialGUI(QDialog):
    
      
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''

    def __init__(self, parent_win):
        '''
        Contstructor
        '''

        QDialog.__init__(self, parent_win)
        self.Interstitial = SharedApp.SharedApp.App

        self.setWindowTitle('About Intersitial')
        
        self.parent_win = parent_win
        self.setWindowModality(Qt.WindowModal)

        self.parent_win.setWindowTitle('About Intersitial')

        self.setWindowIcon(QIcon(self.Interstitial.Configuration.getLogoSignSmall()))
        self.AboutInterstitialLayout = QVBoxLayout()

        self.widget = QWidget(self)
        self.pgroup = QGroupBox()
        self.detail_layout = QVBoxLayout()
        self.pgroup.setStyleSheet(" QGroupBox { border-style: none; border: none;}")
        self.close_btn = QPushButton('Close')

        self.about_layout = QGroupBox()
        self.heading = QTextBrowser()
        self.content = QTextEdit()

        self.content.installEventFilter(self)
        self.heading.setReadOnly(True)
        self.content.setReadOnly(False)
        self.content.viewport().setCursor(Qt.PointingHandCursor)

        self.main = QHBoxLayout()

    def openUserGuideUrl(self):
        try:
            QDesktopServices.openUrl(QUrl(self.Interstitial.Configuration.getUserGuideUrl()))
        except:
            webbrowser.open_new_tab(self.Interstitial.Configuration.getUserGuideUrl())
            pass

    def destroy(self):
        ''' Distructor'''
        del self

    def ShowDialog(self):
        ''' Show Dialog'''
        self.show()
        self.exec_()

    def SetLayout(self, layout):
        ''' Set Layout'''
        self.AboutInterstitialLayout = layout

    def showDescription(self):
        ''' Show Description'''
        self.heading.setText(self.Interstitial.label['description_heading'])
        self.content.setHtml(self.Interstitial.label['description_content'])

    def eventFilter(self, target, event):
        """
        Capturing Content Clicked Event
        @param target: Event triggered by Widget Object
        @param event: Event triggered
        @return Boolean: weather to launch
        """

        if event.type() == QEvent.RequestSoftwareInputPanel:
            self.openUserGuideUrl()
            return True;
        return False;

    def SetDesgin(self):
        ''' All design Management Done in Here'''

        self.close_btn = QPushButton('Close')

        pic = QLabel(self)

        pic.setFixedSize(300,400)

        '''use full ABSOLUTE path to the image, not relative'''

        pic.setPixmap(QPixmap(self.Interstitial.Configuration.getLogoSignSmall()))

        self.close_btn.clicked.connect(self.Cancel)

        self.detail_layout.addWidget(pic)
        self.pgroup.setLayout(self.detail_layout)
        slay = QVBoxLayout()
        if self.Interstitial.Configuration.getOsType() == 'windows':
            self.heading.setFixedSize(555, 40)
            self.content.setFixedSize(555, 260)
        else:
            self.heading.setFixedSize(570, 40)
            self.content.setFixedSize(570, 260)

        self.close_btn.setFixedSize(200, 30)

        slay.addWidget(self.heading)
        slay.addWidget(self.content)
        slay.addWidget(self.close_btn)

        if self.Interstitial.Configuration.getOsType() == 'windows':
            self.about_layout.setFixedSize(575, 360)
        else:
            self.about_layout.setFixedSize(585, 360)

        self.pgroup.setFixedSize(40, 360)
        self.main.addWidget(self.pgroup)
        self.main.addWidget(self.about_layout)

        self.about_layout.setLayout(slay)
        self.setLayout(self.main)
        self.showDescription()

    def Cancel(self):
        """
        Close the Dialog Box
        @return:
        """

        try:
            self.Interstitial = SharedApp.SharedApp.App
        except:
            pass

        self.parent_win.setWindowTitle(self.Interstitial.messages['InterErrorDetectTitle'])
        self.destroy()
        self.close()

    def LaunchDialog(self):
        """
        Launch Dialog

        @return:
        """
        self.SetDesgin()
        self.ShowDialog()