# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on Aug 12, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

# built-in libraries
import os

# Custom libraries
import ExpectedResults as ExpectedResults
import FailedMessages as FailedMessages

import Fixtures.helper as helper
from Fixtures import Fixture

class CheckRequiredTestCase(object):

    def __init__(self):
        self.fixture = Fixture.Fixtures()
        self.manifest_templates = 'manifestTemplate.txt'
        self.report_template = 'reportTemplate.txt'
        pass

    def checkForTemplate(self):
        print('')
        print('===============================================================')
        print('')

        print('Check For Templates .......... !')
        print('')
        bast_app_path = self.fixture.unit_test_folder.replace((os.sep + 'Tests' + os.sep), '')

        is_template_file_exists = os.path.isfile(bast_app_path + os.sep + 'assets' + os.sep + 'templates' + os.sep + self.manifest_templates)
        is_report_file_exists = os.path.isfile(bast_app_path + os.sep + 'assets' + os.sep + 'templates' + os.sep + self.report_template)

        return [
                {'is_template_file_exists': is_template_file_exists, 'is_report_file_exists': is_report_file_exists},
                ExpectedResults.CheckRequiredTestCaseExpectedResult['check_for_template'],
                FailedMessages.CheckRequiredTestCaseFailMessages['check_for_template']
                ]