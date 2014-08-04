# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>


from Config import Configuration, Setup, Laguage
from Core import SharedApp, CustomException, Debugger


class App(object):
    """
        Application Interstitial Class
    """

    _instance = None

    @staticmethod
    def getInstance():
        """
        Get Instance of the Application

        @return: Interstitial Instance
        """

        if not isinstance(App._instance, App):
            App._instance = object.__new__(App)
            SharedApp.SharedApp.App = App._instance
            App._instance.setUp()

        return App._instance

    def setUp(self):
        """
        Set Up Application Static Contents

        @return: None
        """

        self.ExceptionHandler = CustomException.CustomException.getInstance()
        self.Configuration = Configuration.Configuration()
        self.Setup = Setup.Setup()
        self.Setup.setupApp()
        self.logger = Debugger.Debugger.getInstance()
        self.messages = Laguage.message
        self.label = Laguage.label
