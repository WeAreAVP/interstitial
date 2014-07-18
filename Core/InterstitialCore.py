# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import numpy as np
from scikits.audiolab import Sndfile
from sys import argv, exit
from math import fabs, floor
from re import compile
from os import walk, path, stat
from time import strftime, time
import datetime

#custome libs
from Core import SharedApp

class InterstitialCore(object):
    def __init__(self):
        self.Interstitial = SharedApp.SharedApp.App
        pass



