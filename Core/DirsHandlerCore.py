# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
#Created on May 14, 2014
#@author: Furqan Wasi <furqan@avpreserve.com>

import numpy as np
from scikits.audiolab import Sndfile
from sys import argv, exit
from math import fabs, floor
from re import compile
from os import walk, path, stat
from time import strftime, time
import datetime

from Core import SharedApp

class DirsHandlerCore(object):
    """
        Application Directories Handler Core  Class
    """

    def __init__(self):
        """
        Constructor
        """
        self.Interstitial = SharedApp.SharedApp.App

        self.number_of_daw_dirs = 1
        self.number_of_ref_dirs = 1
        pass

    def mono(self, numpy_matrix):
        """

        mono(numpy matrix ar)
        reduces an n-dimensional matrix to a 1-dimensional list if n > 1
        if n = 1, returns it
        @param numpy_matrix: Numpy Matrix

        @return: numpy_matrix
        """

        if numpy_matrix.ndim > 1:
            return numpy_matrix[:,0]
        else:
            return numpy_matrix

    def offs(self, track1, track2):
        """
        offs(audiofile track1, audiofile track2)
        calculates the head offset between two (supposedly) otherwise identitical audio files
        this is achieved via finding the peak-to-peak difference of the waveform heads
        """

        # opens files for reading
        try:
            track_one_file_obj = Sndfile(track1, 'r')
        except:
            print('Corrupted file : '+ str(track1))
            return
            pass

        print('123123123')

        try:
            track_two_file_obj = Sndfile(track2, 'r')
        except:
            print('Corrupted File : '+ str(track2))
            return
            pass

        # calculates the head of each file (first twentieth of the waveform)
        # if this is less than 5 seconds of audio (that is, the waveform is under 100 seconds long)
        # then the head is the first five seconds of the waveform
        track_one_file_obj_head = floor(.05 * track_one_file_obj.nframes)
        if track_one_file_obj_head < (track_one_file_obj.samplerate * 5):
            track_one_file_obj_head = track_one_file_obj.nframes

        track_two_file_obj_head = floor(.05 * track_two_file_obj.nframes)
        if track_two_file_obj_head < (track_two_file_obj.samplerate * 5):
            track_two_file_obj_head = track_two_file_obj.nframes

        # reads the head of each file (as absolute values, accounting for reversed waveforms)
        # into a 1-dimensional numpy matrix (via mono function)
        numpy_matrix_of_track1 = self.mono(np.absolute(track_one_file_obj.read_frames(track_one_file_obj_head)))
        numpy_matrix_of_track2 = self.mono(np.absolute(track_two_file_obj.read_frames(track_two_file_obj_head)))

        # returns the difference between the peak of each list
        return np.argmax(numpy_matrix_of_track1) - np.argmax(numpy_matrix_of_track2)

    def populate(self, dir):
        """
        Populate (File Path Dir)
        walks the file tree under dir recursively and returns all .wav files in it
        """

        populated_list = []
        wav = compile('.[Ww][Aa][Vv]$')
        for root, subFolders, files in walk(dir):
            for singleFile in files:
                if wav.search(singleFile):
                    populated_list.append(path.join(root, singleFile))

        return populated_list

    def execute(self, q_action):
        """
        Execute (wavefile first_wave_file, wavefile second_wave_file, directory d, QAction qa)
        The heart of interstitial - performs a null test on two wav files and returns the first difference
        """

        # initialize useful variables

        values = ''
        file_count = 0

        test_done_for_files = []
        targeted_done = []

        # Ensures That We Have Legitimate Directories To Walk Down
        # And Populates The List Of Files To Test
        if not path.isdir(path.abspath(self.getCoreDawText())) or not path.isdir(path.abspath(self.getCoreRefText())):
            print self.Interstitial.messages['illegalPaths']
            return

        testers = self.populate(self.getCoreDawText())
        print str(len(testers)) + self.Interstitial.messages['WAV_found'] + path.abspath(self.getCoreDawText())

        targets = self.populate(self.getCoreRefText())
        print str(len(targets)) + self.Interstitial.messages['WAV_found'] + path.abspath(self.getCoreRefText())

        q_action.processEvents()

        # Process Each File In The Tester Array
        for index in xrange(len(testers)):
            found = False

            for e in xrange(len(targets)):
                q_action.processEvents()
                # If We Haven't Already Processed This File, Process It
                if str(targets[e]) not in targeted_done:

                    # find the offset and align the waveforms
                    toff = self.offs(testers[index], targets[e])

                    try:
                        tester_file_obj = Sndfile(testers[index], 'r')
                    except:
                        print('Corrupted File : '+ str(testers[index]))
                        return
                        pass

                    try:
                        target_file_obj = Sndfile(targets[e], 'r')
                    except:
                        print('Corrupted File : ' + str(targets[e]))
                        return
                        pass

                    if toff > 0:
                        tester_file_obj.seek(toff)
                    else:
                        target_file_obj.seek(fabs(toff))

                    # Read The First 1000 Samples Of Each File
                    # If Each Sample Is Within 6dB Of The Other, We Have A Match And Can Begin Processing
                    numpy_matrix_of_track1 = self.mono(tester_file_obj.read_frames(1000))
                    numpy_matrix_of_track2 = self.mono(target_file_obj.read_frames(1000))

                    if np.array_equal(numpy_matrix_of_track1, numpy_matrix_of_track2):
                        print "MATCH: " + str(testers[index]) + " matches " + str(targets[e])

                        q_action.processEvents()
                        # mark files as done
                        test_done_for_files.append(str(testers[index]))
                        targeted_done.append(str(targets[e]))

                        # we can't read the entire file into RAM at once
                        # so instead we're breaking it into one-second parts
                        l = min((tester_file_obj.nframes - toff), (target_file_obj.nframes - toff)) / tester_file_obj.samplerate
                        for n in xrange(0, l, 1):
                            errs = 0
                            try:
                                # drop all but the first channel
                                track_one_response = self.mono(tester_file_obj.read_frames(tester_file_obj.samplerate))
                                track_two_response = self.mono(target_file_obj.read_frames(target_file_obj.samplerate))

                                # are these arrays equivalent? if not, there's an error
                                if not np.array_equal(track_one_response, track_two_response):
                                    file_count += 1
                                    # where's the error?
                                    # we find it by comparing sample by sample across this second of audio
                                    for m in xrange(len(track_one_response)):
                                        if not np.array_equal(track_one_response[m], track_two_response[m]):
                                            # we found it! print a message and we're done with these files
                                            errs = (n * tester_file_obj.samplerate) + m + 1000
                                            print self.Interstitial.messages['errorFoundBw'] + str(testers[index]) + " and " + str(targets[e]) + " at sample " + str(errs)
                                            q_action.processEvents()
                                            break
                                if errs != 0:
                                    break

                            except RuntimeError:
                                break

                        # Append Metadata For Output
                        values += path.abspath(testers[index]) + "," + path.abspath(str(targets[e])) + ","
                        values += datetime.datetime.fromtimestamp(stat(testers[index]).st_ctime).strftime("%Y-%m-%d %H:%M:%S") + ","
                        values += str(stat(testers[index]).st_size) + "," + str(tester_file_obj.channels) + "," + str(tester_file_obj.samplerate) + ","
                        values += str(datetime.timedelta(seconds=int(tester_file_obj.nframes / tester_file_obj.samplerate))) + "," + str(errs) + ","
                        values += str(datetime.timedelta(seconds=int(errs/tester_file_obj.samplerate)))

                        values += "\n"
                        found = True

                    if found:
                        break

        # Create Header Information For Manifest
        manifest_info = {'testers': testers, 'file_count': file_count, 'values': values}
        return {'manifest_info': manifest_info}

    def writeManifestFile(self, file_path, manifest_content):
        """
        Write Manifest File

        @param file_path: Manifest File Path(String)
        @param manifest_content: Manifest Content (Tuple)

        @return:Manifest Content(String)
        """

        try:
            f = open(file_path, 'w')
            f.write(manifest_content)
            print self.Interstitial.messages['wroteManifest'] + path.abspath(f.name)
            f.close()
        except:
            print self.Interstitial.messages['illegalPath'] + file_path

    def generateManifestContent(self, template_of_manifest_file_lines, manifest_info):
        """
        Generate Manifest Content
        @param template_of_manifest_file_lines: Lines Template Of Manifest File

        @return:manifest_content
        """

        manifest_content = ''
        for template_of_manifest_single_line in template_of_manifest_file_lines:
            response = False
            response = self.setValuesForScheduler(template_of_manifest_single_line, '{{current_date}}',
                                                  str(manifest_info['current_date']))
            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line, '{{initiated}}',
                                                          str(manifest_info['initiated']))
            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line, '{{seconds}}',
                                                          str(manifest_info['seconds_content']))
            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line, '{{testers}}',
                                                          str(manifest_info['testers']))
            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line, '{{bad_files}}',
                                                          str(manifest_info['file_count']))
            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line, '{{columns}}',
                                                          str(manifest_info['columns']))
            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line, '{{values}}',
                                                          str(manifest_info['values']))

            if response is False:
               # If No Value Found To Replace
                manifest_content += str(template_of_manifest_single_line)
            else:
                manifest_content += response

        return manifest_content

    def setValuesForScheduler(self, string, find_string, replace_with_string):
        """
        @param string: Template String
        @param find_string: Find String string to be replaced with
        @param replace_with_string: String to be replaced with

        @return:String
        """

        try:self.Interstitial = SharedApp.SharedApp.App
        except:pass

        string = str(string)
        find_string = str(find_string)
        replace_with_string = str(replace_with_string)
        if find_string in string:
            return str(string).replace(find_string, replace_with_string)
        return False
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