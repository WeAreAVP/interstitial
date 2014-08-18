# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

# built-in libraries
import os
import random
import shutil
import sys

# Custom libraries
import helper
sys.path.append(helper.setImportBaseBath())

from App import App
class Fixtures(object):

    def __init__(self):
        self.Interstitial = App.getInstance()

        self.unit_test_folder = self.Interstitial.Configuration.getUnit_test_folder()
        self.fixtures_folder = self.Interstitial.Configuration.getFixturesFolder()

        self.project_name = 'New_Project'
        self.test_folder_one = self.fixtures_folder + 'DAW' + os.sep
        self.test_folder_two = self.fixtures_folder + 'Reference' + os.sep

        pass