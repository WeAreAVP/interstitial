# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
import traceback
from os import path
from Core import SharedApp
import xml.etree.cElementTree as XmlHanlder


class Setup(object):
    """
        Application Setup Handler Class
    """

    def __init__(self):
        self.Interstitial = SharedApp.SharedApp.App
        pass

    def setupApp(self):
        """
        Create Config file

        @return: None
        """

        if not path.isfile(self.Interstitial.Configuration.getConfigFilePath()):
            try:
                status = 'true'
                Interstitial = XmlHanlder.Element("Interstitial")

                configuration = XmlHanlder.SubElement(Interstitial, "Configuration")
                debugging = XmlHanlder.SubElement(configuration, "debugging")

                debugging.set("status", status)

                xml_obj = XmlHanlder.ElementTree(Interstitial)
                if status == 'true':
                    self.is_debugger_on = True
                else:
                    self.is_debugger_on = False
                xml_obj.write(self.Interstitial.Configuration.getConfigFilePath())

            except:
                traceback.print_stack()
                pass
        pass