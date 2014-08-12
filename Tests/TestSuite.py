# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on Aug 12, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

# built-in libraries
import unittest
import os
import sys

# Custom libraries
from TestCases.ProjectTestCase import ProjectTestCase
from TestCases.CheckRequiredTestCase import CheckRequiredTestCase

base_path = os.getcwd()
base_path = base_path.replace(r'\tests', '')
sys.path.append(base_path+os.sep)

class TestSuite(unittest.TestCase):

    def setUp(self):
        """
        Set Up

        @return: None
        """
        print('Start Up')
        self.project_test_case = ProjectTestCase()
        self.check_required_test_case = CheckRequiredTestCase()
        pass

    def testAProject(self):


        # Launch The Scanner to Test Audio Files unit test
        result_run_project_single_dir_with_error = self.project_test_case.run_project_single_dir_with_error()
        self.assertEqual(result_run_project_single_dir_with_error[0],
                         result_run_project_single_dir_with_error[1],
                         result_run_project_single_dir_with_error[2])

        result_run_project_multiple_dir_with_error = self.project_test_case.run_project_multiple_dir_with_error()
        self.assertEqual(result_run_project_multiple_dir_with_error[0],
                         result_run_project_multiple_dir_with_error[1],
                         result_run_project_multiple_dir_with_error[2])

        result_check_for_template = self.check_required_test_case.checkForTemplate()
        self.assertEqual(result_check_for_template[0],
                         result_check_for_template[1],
                         result_check_for_template[2])
        pass

    def tearDown(self):
        """
        Tear Down Unit Test
        """
        print('Tear Down!')

        pass

if __name__ == '__main__':
    unittest.main()

