# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

import sys, os, traceback

class CustomException(object):
    """
        Application Exception Handler Class
    """

    _instance = None

    @staticmethod
    def getInstance():
        if not isinstance(CustomException._instance, CustomException):
            CustomException._instance = object.__new__(CustomException)
        return CustomException._instance

    def selfDestruct(self):
        del self

    def getExceptionDetails(self):
        """
        Get Exception Details

        @return: List
        """

        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_information = {}
        try:
            error_information['file_name'] = file_name
        except:
            pass

        try:
            error_information['error_type'] = exc_type
        except:
            pass
        try:
            error_information['line_no'] = exc_tb.tb_lineno
        except:
            pass

        return error_information

    def getTraceBack(self):
        """
        Get Trace Back

        @return: Error Stack
        """

        stack_errro = repr(traceback.extract_stack())
        return stack_errro

