# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from time import strftime
from os import path, getcwd, sep, name


class Configuration(object):
    """
        Application Configuration Handler Class
    """

    def __init__(self):
        """
        Constructor
        """
        self.base_path = str(getcwd())+str(sep)
        self.log_file_path = path.join(self.base_path, 'debug.log')
        self.assets_path = path.join(self.base_path, 'assets'+str(sep))
        self.template_path = path.join(self.assets_path, 'templates')+str(sep)
        self.manifest_template_path = path.join(self.template_path, 'manifestTemplate.txt')
        self.is_debugging_on = True
        self.config_file_path = self.getBasePath()+'conf.xml'
        self.columns = "Test File,Reference File,Creation Date,Size,Channels,Sample Rate,Length,First Error Sample,Error At"

        if name == 'posix':
            self.OsType = 'linux'

        elif name == 'nt':
            self.OsType = 'windows'

        else:
            self.OsType = 'check'

        if self.OsType == 'Windows':
            self.main_window_width = 600

        else:
            self.main_window_width = 630

    def getMainWindowWidth(self):
        """
        Get Main Window Width

        @return:Windows Width
        """
        return self.main_window_width

    def getOsType(self):
        """
        Get Os Type

        @return:Os Type
        """
        return str(self.OsType)

    def getCurrentDateTime(self):
        """
        Get Current Date Time

        @return:datetime
        """

        return strftime("%Y%m%d%H%M%S")

    def getManifestFileName(self):
        """
        Get Manifest File Name

        @return:file_name
        """

        return "manifest_" + str(self.getCurrentDateTime()) + ".csv"

    def getColumnsOfManifest(self):
        """
        Get Columns Of Manifest

        @return:columns
        """

        return self.columns

    def getCurrentTime(self):
        """
        Get Current Time

        @return:date
        """

        return strftime("%H:%M:%S")

    def getUserHomePath(self):
        """
        Get User Home Path

        @return:user_home_path
        """

        return path.expanduser('~')

    def getDebugFilePath(self):
        """
        Get Debug File Path

        @return:debug_file_path
        """

        return str(self.log_file_path)

    def getIsDebuggingOn(self):
        """
        Get Is Debugging On

        @return:Boolean
        """

        return self.is_debugging_on

    def setIsDebuggingOn(self, is_debugging_on):
        """
        Set Is Debugging On
        @param is_debugging_on: Is Debugging On

        @return: None
        """

        self.is_debugging_on = is_debugging_on

    def getBasePath(self):
        """
        Get Base Path

        @return:string
        """

        return str(self.base_path)

    def getTemplatePath(self):
        """
        Get Template Path

        @return:string
        """

        return self.template_path

    def getConfigFilePath(self):
        """
        Get Config File Path

        @return:string
        """

        return self.config_file_path

    def getManifestTemplatePath(self):
        """
        Get Manifest Templates Path

        @return:string
        """

        return self.manifest_template_path