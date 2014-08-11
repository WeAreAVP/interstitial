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
print(helper.setImportBaseBath())
sys.path.append(helper.setImportBaseBath())
import Main


class Fixtures(object):


    def __init__(self):
        self.App = Main.Main()

        self.unit_test_folder = self.App.Fixity.Configuration.getUnit_test_folder()
        self.fixtures_folder = self.App.Fixity.Configuration.getFixturesFolder()

        self.project_name = 'New_Project'
        self.test_folder_one = self.fixtures_folder + 'DAW' + os.sep
        self.test_folder_one = self.fixtures_folder + 'Reference' + os.sep

        pass