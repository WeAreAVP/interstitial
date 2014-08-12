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
import sys

# Custom libraries

import ExpectedResults as ExpectedResults
import FailedMessages as FailedMessages

import Fixtures.helper as helper
from Fixtures import Fixture

sys.path.append(helper.setImportBaseBath())

from Core import DirsHandlerCore

class ProjectTestCase(object):

    def __init__(self):
        self.fixture = Fixture.Fixtures()
        pass

    def is_report_created(self, report_file_path):
        '''
        Report Created

        @return is_file_exists: Boolean
        '''
        return os.path.isfile(report_file_path)

    def run_project_single_dir_with_error(self):
        '''
        Run Project Using Single Directory for DAW and Reference

        @return List:Response
        '''
        print('')
        print('===============================================================')
        print('')

        print('Run Project Single Dir With Error .......... !')
        print('')

        dirs_handler_core = DirsHandlerCore.DirsHandlerCore()

        dirs_handler_core.setNumberOfDawCore(1)
        dirs_handler_core.setNumberOfRefCore(1)

        dirs_handler_core.setDawDirsCore(self.fixture.test_folder_one, 0)
        dirs_handler_core.setRefDirsCore(self.fixture.test_folder_two, 0)

        response = dirs_handler_core.run_executor(self.fixture.fixtures_folder, None, True)

        is_report_generated = self.is_report_created(response['manifest_file_path'])

        return [{'report_generated': is_report_generated, 'error_files': int(response['manifest_info']['file_count'])}, ExpectedResults.ProjectTestCaseExpectedResult['run_project_single_dir_with_error'], FailedMessages.ProjectTestCaseFailMessages['run_project_single_dir_with_error']]

    def run_project_multiple_dir_with_error(self):
        '''
        Run Project Using Multiple Directory for DAW and Reference

        @return List:Response
        '''

        print('')
        print('===============================================================')
        print('')

        print('Run Project Multiple Dir With Error .......... !')
        print('')
        dirs_handler_core = DirsHandlerCore.DirsHandlerCore()

        #dirs_handler_core.setNumberOfDawCore(2)
        #dirs_handler_core.setNumberOfRefCore(2)

        for index_raw in xrange(0, dirs_handler_core.number_of_daw_core):
            for index_ref in xrange(0, dirs_handler_core.number_of_ref_core):
                dirs_handler_core.setDawDirsCore(self.fixture.test_folder_one, index_raw)
                dirs_handler_core.setRefDirsCore(self.fixture.test_folder_two, index_ref)

        response = dirs_handler_core.run_executor(self.fixture.fixtures_folder, None, True)

        is_report_generated = self.is_report_created(response['manifest_file_path'])

        return [{'report_generated': is_report_generated, 'error_files': int(response['manifest_info']['file_count'])}, ExpectedResults.ProjectTestCaseExpectedResult['run_project_multiple_dir_with_error'], FailedMessages.ProjectTestCaseFailMessages['run_project_multiple_dir_with_error']]