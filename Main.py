# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

from PySide.QtGui import *
import sys
from os import path

from GUI import InterstitialGUI
from Core import SharedApp
from App import App

class Main(object):
    """
        Application Main Launcher Class
    """

    def __init__(self):
        SharedApp.SharedApp.App = App.getInstance()
        pass

    def LaunchGUI(self, param):
        """
        Launch GUI Application

        @return: None
        """
        app = QApplication(param)
        interstitialGUIApp = InterstitialGUI.InterstitialGUI.getInstance()

        interstitialGUIApp.show()
        interstitialGUIApp.raise_()

        sys.exit(app.exec_())

    def RunCoreExecutor(self, param1, param2):
        """
        Run Core Executor Independently

        @return: None
        """



    def LaunchCLI(self):
        """
        Launch CLI Application on demand

        @return: None
        """
        """
        Lunch CLI Application
        """
        pass

# Main Application
if __name__ == '__main__':

    InterstitialApp = Main()
    #try:
    InterstitialApp.LaunchGUI(sys.argv)
    #except:
    #   exc_type, exc_obj, exc_tb = sys.exc_info()
    #   file_name = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #   print("Could not run this Project "+str(Exception.message))