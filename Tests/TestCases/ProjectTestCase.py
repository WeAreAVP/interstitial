# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''


# built-in libraries
import unittest
import os
import sys

# Custom libraries


import ExpectedResults as ExpectedResults
import FailedMessages as FailedMessages

import Fixtures.helper as helper
sys.path.append(helper.setImportBaseBath())

import Main

class ProjectTestCase(object):


    def __init__(self):
        self.App = Main.Main()
        pass

    def run_project_single_dir(self):
        '''
        Run Project using Single Directory for DAW and Reference
        '''
        print('run_project_single_dir')
        pass