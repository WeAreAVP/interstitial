# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on Aug 12, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

import os

def setImportBaseBath():
    base_path = os.getcwd()
    base_path = base_path.replace(r'\Tests', '')
    base_path = base_path.replace(r'\Fixtures', '')
    base_path = base_path.replace(r'/Tests', '')
    base_path = base_path.replace(r'/Fixtures', '')
    return os.path.join(base_path,'')