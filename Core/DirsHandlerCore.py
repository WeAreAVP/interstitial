# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

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

    def __init__(self):
        self.Interstitial = SharedApp.SharedApp.App

        self.daw_dir_id = ''
        self.daw_dir_text = ''
        self.ref_dir_id = ''
        self.ref_dir_text = ''

        pass

    def setCoreDawId(self, daw_dir_id):
        """
        Set Core DAW ID
        @param daw_dir_id: this DAW Directory ID
        """
        self.daw_dir_id = daw_dir_id

    def getCoreDawId(self):
        """
        Get Core DAW ID
        @return string
        """
        return self.daw_dir_id

    def setCoreRefId(self, ref_dir_id):
        """
        Set Core Reference ID
        @param ref_dir_id: this Reference Directory ID
        """
        self.ref_dir_id = ref_dir_id

    def getCoreRefId(self):
        """
        Get Core Reference ID

        @return string
        """
        return self.daw_dir_id

    def setCoreDawText(self, daw_dir_text):
        """
        Set Core DAW Text
        """
        self.daw_dir_text = daw_dir_text

    def getCoreDawText(self):
        """
        Get Core DAW Text

        @return string
        """
        return self.daw_dir_text

    def setCoreRefText(self, ref_dir_text):
        """
        Set Core Reference Text
        """
        self.ref_dir_text = ref_dir_text

    def getCoreRefText(self):
        """
        Get Core Reference Text
        @param ref_dir_text: this Reference Directory Text

        @return string
        """
        return self.ref_dir_text

    def mono(self, numpy_matrix):
        """
        mono(numpy matrix ar)
        reduces an n-dimensional matrix to a 1-dimensional list if n > 1
        if n = 1, returns it
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
        track_one_file_obj = Sndfile(track1, 'r')
        track_two_file_obj = Sndfile(track2, 'r')

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
        populate (filepath dir)
        walks the file tree under dir recursively and returns all .wav files in it
        """
        populated_list = []
        wav = compile('.[Ww][Aa][Vv]$')
        for root, subFolders, files in walk(dir):
            for singleFile in files:
                if wav.search(singleFile):
                    populated_list.append(path.join(root, singleFile))

        return populated_list

    def execute(self, directory, q_action):
        """
        execute (wavefile first_wave_file, wavefile second_wave_file, directory d, QAction qa)
        the heart of interstitial - performs a null test on two wav files and returns the first difference
        """
        # initialize useful variables

        values = ''
        file_count = 0
        test_done = []
        targ_done = []
        timer = time()

        filename = self.Interstitial.Configuration.getManifestFileName()
        columns = self.Interstitial.Configuration.getColumnsOfManifest()

        initiated = self.Interstitial.Configuration.getCurrentTime()

        print(self.getCoreDawText())
        print(self.getCoreRefText())

        # ensures that we have legitimate directories to walk down
        # and populates the list of files to test
        if not path.isdir(path.abspath(self.getCoreDawText())) or not path.isdir(path.abspath(self.getCoreRefText())):
            print self.Interstitial.messages['illegalPaths']
            return

        testers = self.populate(self.getCoreDawText())
        print str(len(testers)) + self.Interstitial.messages['WAVfound'] + path.abspath(self.getCoreDawText())
        targets = self.populate(self.getCoreRefText())
        print str(len(targets)) + self.Interstitial.messages['WAVfound'] + path.abspath(self.getCoreRefText())
        q_action.processEvents()

        # process each file in the tester array
        for index in xrange(len(testers)):
            found = False
            for e in xrange(len(targets)):
                q_action.processEvents()
                # if we haven't already processed this file, process it
                if str(targets[e]) not in targ_done:
                    # find the offset and align the waveforms
                    toff = self.offs(testers[index], targets[e])
                    tester_file_obj = Sndfile(testers[index], 'r')
                    target_file_obj = Sndfile(targets[e], 'r')

                    if toff > 0:
                        tester_file_obj.seek(toff)
                    else:
                        target_file_obj.seek(fabs(toff))

                    # read the first 1000 samples of each file
                    # if each sample is within 6dB of the other, we have a match and can begin processing
                    numpy_matrix_of_track1 = self.mono(tester_file_obj.read_frames(1000))
                    numpy_matrix_of_track2 = self.mono(target_file_obj.read_frames(1000))

                    if np.array_equal(numpy_matrix_of_track1, numpy_matrix_of_track2):
                        print "MATCH: " + str(testers[index]) + " matches " + str(targets[e])
                        q_action.processEvents()

                        # mark files as done
                        test_done.append(str(testers[index]))
                        targ_done.append(str(targets[e]))

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
                                            print self.Interstitial.messages['errorfoundbw'] + str(testers[index]) + " and " + str(targets[e]) + " at sample " + str(errs)
                                            q_action.processEvents()
                                            break

                                if errs != 0:
                                    break

                            except RuntimeError:
                                break

                        # append metadata for output
                        values += path.abspath(testers[index]) + "," + path.abspath(str(targets[e])) + ","
                        values += datetime.datetime.fromtimestamp(stat(testers[index]).st_ctime).strftime("%Y-%m-%d %H:%M:%S") + ","
                        values += str(stat(testers[index]).st_size) + "," + str(tester_file_obj.channels) + "," + str(tester_file_obj.samplerate) + ","
                        values += str(datetime.timedelta(seconds=int(tester_file_obj.nframes / tester_file_obj.samplerate))) + "," + str(errs) + ","
                        values += str(datetime.timedelta(seconds=int(errs/tester_file_obj.samplerate)))
                        values += "\n"

                        found = True

                    if found:
                        break

        # create header information for manifest
        current_date = strftime("%Y-%m-%d")
        seconds_content = str(floor(time() - timer))

        manifest_info = {}
        manifest_info['current_date'] = current_date
        manifest_info['initiated'] = initiated
        manifest_info['seconds_content'] = seconds_content
        manifest_info['testers'] = len(testers)
        manifest_info['file_count'] = file_count
        manifest_info['columns'] = columns
        manifest_info['values'] = values

        # Open template file and get manifest template content to manifest file creation
        template_of_manifest_file = open(self.Interstitial.Configuration.getManifestTemplatePath(), "r")
        template_of_manifest_file_lines = template_of_manifest_file.readlines()
        template_of_manifest_file.close()

        manifest_content = self.generateManifestContent(template_of_manifest_file_lines, manifest_info)

        # do we have metadata? if so, write a manifest
        # Write Manifest File
        if len((values + columns)) > 110:

            manifest_file_path = directory + "/" + filename
            self.writeManifestFile(manifest_file_path, manifest_content)
            return manifest_file_path


    def writeManifestFile(self, file_path, manifest_content):
        """
        Write Manifest File
        @param file_path: Manifest File Path(String)
        @param manifest_content: Manifest Content (Tuple)

        @return Manifest Content(String)
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

        @return manifest_content
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
               # if no value found to replace
                manifest_content += str(template_of_manifest_single_line)
            else:
                manifest_content += response

        return manifest_content

    def setValuesForScheduler(self, string, find_string, replace_with_string):
        """
        @param string: Template String
        @param find_string: Find String string to be replaced with
        @param replace_with_string: String to be replaced with

        @return String
        """

        try:self.Interstitial = SharedApp.SharedApp.App
        except:pass

        string = str(string)
        find_string = str(find_string)
        replace_with_string = str(replace_with_string)
        if find_string in string:
            return str(string).replace(find_string, replace_with_string)
        return False