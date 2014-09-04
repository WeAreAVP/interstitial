# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

class DAWDirsCore(object):

    def __init__(self):
        self.daw_dir_id = ''
        self.daw_dir_text = ''
        pass

    def setCoreDawId(self, daw_dir_id):
        """
        Set Core DAW ID
        @param daw_dir_id: this DAW Directory ID

        @return: None
        """

        self.daw_dir_id = daw_dir_id

    def getCoreDawId(self):
        """
        Get Core DAW ID

        @return:string
        """

        return self.daw_dir_id

    def setCoreDawText(self, daw_dir_text):
        """
        Set Core DAW Text

        @return: None
        """

        self.daw_dir_text = daw_dir_text

    def getCoreDawText(self):
        """
        Get Core DAW Text

        @return:string
        """

        return self.daw_dir_text