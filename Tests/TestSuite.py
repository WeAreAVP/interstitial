# -*- coding: UTF-8 -*-
'''
Created on JUNE 30, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

# built-in libraries
import unittest
import os
import sys


# Custom libraries

from TestCases.ProjectTestCase import ProjectTestCase
import shutil

base_path = os.getcwd()
base_path = base_path.replace(r'\tests', '')
sys.path.append(base_path+os.sep)

from Fixtures.Fixture import Fixtures
from TestCases import ProjectTestCase
import Main
import unittest

class TestSuite(unittest.TestCase):

    def setUp(self):
        """
        Set Up

        @return: None
        """
        print('Start Up')
        self.project_test_case = ProjectTestCase.ProjectTestCase()
        pass

    def testAProject(self):
        print('One Test')
        self.project_test_case.run_project_single_dir()
        pass

    def tearDown(self):
        """
        Tear Down Unit Test
        """
        print('Tear Down!')

        pass

if __name__ == '__main__':
    unittest.main()

