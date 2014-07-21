# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>

'''
import os, logging, datetime
from Core import SharedApp
import xml.etree.cElementTree as XmlHanlder

class Debugger(object):
    """
        Application Debugger Handler Class
    """

    _instance = None
    def __init__(self):
        Debugger._instance.setUp()

    @staticmethod
    def getInstance():
        if not isinstance(Debugger._instance, Debugger):
            Debugger._instance = object.__new__(Debugger)
            Debugger._instance.setUp()
        return Debugger._instance

    def selfDestruct(self):
        del self

    def setUp(self):
        """
        Setup Application

        @return: None
        """

        self.Interstitial = SharedApp.SharedApp.App

        self.debug_file_path = self.Interstitial.Configuration.getDebugFilePath()
        self.config_file_path = self.Interstitial.Configuration.getConfigFilePath()
        self.loger = logging

        # Create debug file
        try:
            self.loger.basicConfig(filename=self.debug_file_path, level=logging.DEBUG)
        except:
            pass

        if self.get() == 'true':
            self.is_debugger_on = False
        else:
            self.is_debugger_on = True


    #@param msg
    #@param more_information

    def logError(self,msg,more_information = None):
        """
        Function to Log Errors

        @param msg: Message to log
        @param more_information: More information For Logging

        @return: None
        """

        try:
            if self.is_debugger_on:
                self.addTimeStamp()
                self.loger.debug('')
                self.loger.debug(msg)
                if len(more_information) > 0:

                    for key in more_information:

                        self.loger.debug(str(key) + '::' + str(more_information[key])+"\n")

        except:
            pass



    def logInfo(self,msg ,more_information = None):
        """
        Function to Log Information

        @param msg:Message to log
        @param more_information:More information For Logging

        @return: None
        """

        try:
            if self.is_debugger_on:
                self.addTimeStamp()
                self.loger.info(msg)
                if more_information:
                    for key in more_information:
                        self.loger.info(key + '::' + more_information[key]+"\n")
        except:

            self.is_debugger_on = False
            pass

    def logWarning(self,msg,more_information = None):
        """
        Function to Log Warning

        @param msg:Message to log
        @param more_information:More information For Logging

        @return: None
        """

        try:
            if self.is_debugger_on:
                self.addTimeStamp()
                self.loger.warning(msg)
                if more_information:
                    for key in more_information:
                        self.loger.warning(key + '::' + more_information[key]+"\n")

        except:

            self.is_debugger_on = False
            pass

    def set(self, status):
        """
        Set Debugging Information

        @param status:

        @return: None
        """

        os.remove(self.config_file_path)
        fixity = XmlHanlder.Element("Interstitial")

        configuration = XmlHanlder.SubElement(fixity, "Configuration")
        debugging = XmlHanlder.SubElement(configuration, "debugging")

        debugging.set("status", status)

        xml_obj = XmlHanlder.ElementTree(fixity)
        if status == 'true':
            self.is_debugger_on = True
        else:
            self.is_debugger_on = False

        return xml_obj.write(self.config_file_path)

    def get(self):
        """
        Get Status
        @return: int
        """

        tree = XmlHanlder.parse(self.config_file_path)
        root = tree.getroot()
        for child in root:
            for child1 in child:
                return child1.attrib['status']

    def getCurrentTime(self):
        """
        Get Current Time

        @return: None
        """

        return str(datetime.datetime.now()).rpartition('.')[0]

    def addTimeStamp(self):
        """
        Add Time Stamp

        @return: None
        """

        self.loger.warning('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        self.loger.warning('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        self.loger.warning(str(self.getCurrentTime()))
        self.loger.warning('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        self.loger.warning('')

    def LogException(self, message=''):
        """
        Log Exception

        @param message: Message of Exception

        @return: None
        """

        self.Interstitial = SharedApp.SharedApp.App

        ExceptionDetail = {}
        try:
            ExceptionDetail = self.Interstitial.ExceptionHandler.getExceptionDetails()
        except:
            pass

        # print('========================== Exception Message ======================')
        # print(ExceptionDetail)
        # print('========================== Exception Message ======================')

        try:
            ExceptionDetail['trace_back'] = self.Interstitial.ExceptionHandler.getTraceBack()
        except:
            pass

        self.logError(message, ExceptionDetail)