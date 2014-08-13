# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from time import strftime
from os import path, getcwd, sep, name
import sys

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
        self.user_guide_url = 'http://www.avpreserve.com/wp-content/uploads/2013/09/Interstitial-User-Guide-v1-2013-08-27.pdf'
        self.is_debugging_on = True
        self.config_file_path = self.getBasePath()+'conf.xml'
        self.columns = "Test File,Reference File,Creation Date,Size,Channels,Sample Rate,Length,First Error Sample,Error At"

        self.logo_sign_small = 'logo_sign_small.png'
        self.unit_test_folder = self.base_path
        self.fixtures_folder = self.unit_test_folder + 'assets' + sep + 'tests' + sep

        if name == 'posix':
            self.os_type = 'linux'

        elif name == 'nt':
            self.os_type = 'windows'

        else:
            self.os_type = 'check'

        if self.os_type == 'windows':
            self.main_window_width = 600

        else:
            self.base_path = str(getcwd()).replace(str(sep)+'Contents'+str(sep)+'Resources', '')

            self.base_path = str(self.base_path).replace('Resources'+str(sep), '')
            self.base_path = str(self.base_path).replace('Contents'+str(sep), '')
            self.base_path = str(self.base_path).replace('Interstitial.app', '')
            self.base_path = str(self.base_path).replace(str(sep) + str(sep), '')
            self.base_path = str(self.base_path).replace('Main.app', '')

            self.main_window_width = 630

    def getAppBasePath(self):
        """
        Get App Base Path

        @reture app_base_path: path
        """

        return self.app_base_path

    def getUserGuideUrl(self):
        """
        Get User Guide Url

        @return user_guide_url: string
        """
        return self.user_guide_url

    def getFixturesFolder(self):
        """
        Get Fixture Folder

        @return fixtures_folder: string
        """
        return self.fixtures_folder

    def getLogoSignSmall(self):
        """
        Get Windows icon

        @return windows_icon_path: string
        """

        if self.getOsType() == 'windows':
            try:
                return path.join(sys._MEIPASS, 'assets' + (str(sep)) + str(self.logo_sign_small))
            except:
                return path.join(self.assets_path, str(self.logo_sign_small))
                pass
        else:
            return path.join(self.assets_path, str(self.logo_sign_small))

    def getMainWindowWidth(self):
        """
        Get Main Window Width

        @return:Windows Width
        """
        return self.main_window_width

    def getUnit_test_folder(self):
        """
        Get Unit Test Folder

        @return:unit_test_folder
        """

        return self.unit_test_folder

    def getOsType(self):
        """
        Get Os Type

        @return:Os Type
        """
        return self.os_type

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