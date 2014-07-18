# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from time import strftime
from os import path
class Configuration(object):
    def __init__(self):
        pass

    def getCurrentDateTime(self):
        return strftime("%Y%m%d%H%M%S")

    def getManifestFileName(self):
        return "manifest_" + str(self.getCurrentDateTime()) + ".csv"

    def getCurrentTime(self):
        return strftime("%H:%M:%S")

    def getUserHomePath(self):
        return path.expanduser('~')