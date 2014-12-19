# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

message = {}

message['InterErrorDetectTitle'] = 'Interstitial Error Detector'
message['illegalPaths'] = " Illegal paths given - exiting... "
message['WAV_found'] = " WAV files found: "
message['errorFoundBw'] = "ERROR: Interstitial error found between "
message['wroteManifest'] = 'Wrote manifest to: '
message['illegalPath'] = "Illegal path: "
message['daw_empty_msg'] = 'One or more "DAW" Field(s) are empty.Please provide valid path and try again.'
message['ref_empty_msg'] = 'One or more "Reference" Field(s) are empty.Please provide valid path and try again.'
message['invalid_path_daw'] = 'One or more given DAW Path(s) are invalid or does not exist.'
message['invalid_path_ref'] = 'One or more given REF Path(s) are invalid or does not exist.'
message['invalid_path_destination'] = 'Manifest Destination path is invalid or does not exist.'

# Widgets labels

label = {}

label['runLabel'] = "Run!"
label['dirSelector'] = "..."
label['manifestDest'] = "Manifest Destination"
label['exit'] = "Exit"
label['DAWDir'] = "DAW Directory"
label['refDir'] = "Reference Directory"
label['addnew'] = "Add New"
label['addNewRef'] = "Add New Reference Directory ..."
label['addNewDAW'] = "Add New DAW Directory ..."

label['description_heading'] = '''<h1>Interstitial Error Detector</h1>'''
label['description_content'] = '''
                                <center><h2>Interstitial needs an About window, similar to Fixity. This should contain a description and license info (from the LICENSE file).</h2></center></br>

                                <center><p>AVPreserve Interstitial 0.2</p></center> </br>

                                <center><p>Interstitial was developed by AVPreserve and can be found at www.avpreserve.com/tools/.</p> </center> </br>

                                <p>The GitHub repository for Interstitial can be found at https://www.github.com/avpreserve/interstitial</p> </br>

                                <p>Interstitial is a utility for detecting interstitial errors in digitized audio files. The tool compares two sets of audio files - one generated by the DAW, and one saved to a secondary reference device - and reports any discrepancies between them. Interstitial will report any DAW-generated files with errors, as well as the time and sample at which the error occurred.</p> </br>
                                '''

label['description_content'] += """ <p> More information on interstitial errors and how to use Interstitial can be found in the <a href='http://www.avpreserve.com/wp-content/uploads/2013/09/Interstitial-User-Guide-v1-2013-08-27.pdf'>Interstitial manual</a>.</p> </br>"""




