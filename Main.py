# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *
import sys, os.path as path

from argparse import ArgumentParser

from GUI import InterstitialGUI
from Core import InterstitialCore, SharedApp
from App import App

class Main(object):

    def __init__(self):
        pass

    def LaunchGUI(self, param):
        """
        Launch GUI Application
        """
        SharedApp.SharedApp.App = App.getInstance()

        app = QApplication(param)
        interstitialGUIApp = InterstitialGUI.InterstitialGUI()
        interstitialGUIApp.show()
        interstitialGUIApp.raise_()
        sys.exit(app.exec_())

    def RunCoreExecutor(self, param1, param2):
        """
        Run Core Executor Independently
        """
        SharedApp.SharedApp.App = App.App.getInstance()
        IntersCore = InterstitialCore()
        IntersCore.execute(param1, param2)

    def LaunchCLI(self):
        SharedApp.SharedApp.App = App.App.getInstance()
        """
        Lunch CLI Application
        """
        pass

# Main Application
if __name__ == '__main__':
    InterstitialApp = Main()

    try:
        InterstitialApp.LaunchGUI(sys.argv)
    except:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           file_name = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
           print("Could not run this Project "+str(Exception.message))