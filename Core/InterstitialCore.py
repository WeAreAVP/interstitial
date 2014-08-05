# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>
#custome libs
from Core import SharedApp

class InterstitialCore(object):
    """
        Application Interstitial Core Class
    """

    def __init__(self):
        """
        Constructor
        """
        self.Interstitial = SharedApp.SharedApp.App
        pass



