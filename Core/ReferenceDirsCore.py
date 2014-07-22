# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

class ReferenceDirsCore(object):

    def __init__(self):
        self.ref_dir_id = ''
        self.ref_dir_text = ''
        pass

    def setCoreRefId(self, ref_dir_id):
        """
        Set Core Reference ID
        @param ref_dir_id: this Reference Directory ID

        @return: None
        """

        self.ref_dir_id = ref_dir_id

    def getCoreRefId(self):
        """
        Get Core Reference ID

        @return:string
        """

        return self.daw_dir_id

    def setCoreRefText(self, ref_dir_text):
        """
        Set Core Reference Text

        @return: None
        """
        self.ref_dir_text = ref_dir_text

    def getCoreRefText(self):
        """
        Get Core Reference Text
        @param ref_dir_text: this Reference Directory Text

        @return:string
        """

        return self.ref_dir_text