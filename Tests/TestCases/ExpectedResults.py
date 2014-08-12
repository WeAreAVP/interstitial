# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on Aug 12, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

ProjectTestCaseExpectedResult = {}
CheckRequiredTestCaseExpectedResult = {}

ProjectTestCaseExpectedResult['run_project_single_dir_with_error'] = {'report_generated': True, 'error_files': 1}
ProjectTestCaseExpectedResult['run_project_multiple_dir_with_error'] = {'report_generated': True, 'error_files': 4}

CheckRequiredTestCaseExpectedResult['check_for_template'] = {'is_template_file_exists': True, 'is_report_file_exists': True}

