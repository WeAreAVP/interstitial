# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
import traceback
from os import path
from Core import SharedApp
import xml.etree.cElementTree as XmlHanlder


class Setup(object):
    """
        Application Setup Handler Class
    """

    def __init__(self):
        """
        Constructor
        """
        self.Interstitial = SharedApp.SharedApp.App
        pass