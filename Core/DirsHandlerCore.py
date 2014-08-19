# -*- coding: UTF-8 -*-
# Interstitial Error Detector
# Version 0.2, 2013-08-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
# Created on May 14, 2014
# @author: Furqan Wasi <furqan@avpreserve.com>

import numpy as np
from scikits.audiolab import Sndfile
from math import fabs, floor
from re import compile
from os import walk, path, stat
from time import strftime, time, sleep
import datetime

from Core import SharedApp
from Core import DAWDirsCore, ReferenceDirsCore

class DirsHandlerCore(object):
    """
        Application Directories Handler Core  Class
    """

    def __init__(self):
        """
        Constructor
        """
        self.Interstitial = SharedApp.SharedApp.App

        self.number_of_daw_core = 1
        self.number_of_ref_core = 1

        self.daw_dirs_core = {}
        self.reference_dirs_core = {}

        for index_daw in xrange(0, self.number_of_daw_core):
            self.daw_dirs_core[index_daw] = DAWDirsCore.DAWDirsCore()

        for index_ref in xrange(0, self.number_of_ref_core):
            self.reference_dirs_core[index_ref] = ReferenceDirsCore.ReferenceDirsCore()

        pass

    def setNumberOfDawCore(self, number_of_dirs_daw):
        """
        Set Number Of Reference Dirs

        @return daw_dirs_core:String
        """
        self.number_of_daw_core = number_of_dirs_daw


    def setNumberOfRefCore(self, number_of_dirs_ref):
        """
        Set Number Of Daw Dirs

        @return number_of_ref_core:String
        """
        self.number_of_ref_core = number_of_dirs_ref

    def getDawDirsCore(self, index):
        """
        Set Daw Dirs Core

        @return None
        """
        return self.daw_dirs_core[index]

    def setDawDirsCore(self, text, index):
        """
        Set Daw Dirs Core

        @return None
        """
        new_daw = DAWDirsCore.DAWDirsCore()

        new_daw.setCoreDawText(text)
        new_daw.setCoreDawId(index)

        self.daw_dirs_core[index] = new_daw

    def setRefDirsCore(self, text, index):
        """
        Set Ref Dirs Core

        @return None
        """
        new_ref = ReferenceDirsCore.ReferenceDirsCore()

        new_ref.setCoreRefText(text)
        new_ref.setCoreRefId(index)

        self.reference_dirs_core[index] = new_ref

    def getRefDirsCore(self, index):
        """
        Set Ref Dirs Core

        @return None
        """
        return self.reference_dirs_core[index]

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
            track_one_file_obj = Sndfile(track1.encode('utf-8'), 'r')
        except:
            print('Corrupted File 1 : '+ track1)
            return
            pass

        try:
            track_two_file_obj = Sndfile(track2, 'r')
        except:
            print('Corrupted File 2 : '+ track2)
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

    def specialCharacterHandler(self, string_to_be_handled):
        """
        Method to handle all special characters

        @param string_to_be_handled: String To Be Handled

        @return:  String - Fixed characters String
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:
            string_to_be_handled = string_to_be_handled.decode('cp1252')
        except:
            pass

        try:
            string_to_be_handled = string_to_be_handled.encode('utf8')
        except:
            pass

        return string_to_be_handled

    def run_executor(self, manifest_path, q_action=None, is_unit_test=False):
        '''
        Run Executor For all Directories

        @param manifest_path: Manifest File Path
        @param q_action: QCoreApplication Object
        @param is_unit_test: Is call generated from Unit test

        @return manifest_file_path/{manifest_info, manifest_file_path}: Sting/List
        '''
        testers = 0
        file_count = 0
        values = ''

        filename = self.Interstitial.Configuration.getManifestFileName()
        columns = self.Interstitial.Configuration.getColumnsOfManifest()

        timer = time()
        initiated = self.Interstitial.Configuration.getCurrentTime()

        current_date = strftime("%Y-%m-%d")

        for index_daw in xrange(0, self.number_of_daw_core):
            for index_ref in xrange(0, self.number_of_ref_core):

                # Launch The Scanner to Test Audio Files
                report_result = self.execute(index_daw, index_ref, q_action)

                try:
                    testers += len(report_result['manifest_info']['testers'])
                except: pass

                try:
                    file_count += int(report_result['manifest_info']['file_count'])
                except: pass

                try:
                    values += report_result['manifest_info']['values']
                except: pass

                sleep(2)

        seconds_content = str(floor(time() - timer))
        manifest_info = {'current_date': current_date, 'initiated': initiated, 'seconds_content': seconds_content,
                        'testers': testers, 'file_count': file_count, 'columns': columns, 'values': values}

        # Open template file and get manifest template content to manifest file creation
        template_of_manifest_file = open(self.Interstitial.Configuration.getManifestTemplatePath(), "r")
        template_of_manifest_file_lines = template_of_manifest_file.readlines()
        template_of_manifest_file.close()

        manifest_content = self.generateManifestContent(template_of_manifest_file_lines, manifest_info)

        # Do We Have Metadata? If So, Write A Manifest
        # Write Manifest File
        if len((values + columns)) > 110:
            manifest_file_path = manifest_path + "/" + filename
            self.writeManifestFile(manifest_file_path, manifest_content)

            if is_unit_test:
                return {'manifest_info': manifest_info, 'manifest_file_path':manifest_file_path}
            else:
                return manifest_file_path

    def execute(self, index_daw, index_ref, q_action=None):
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

        if not path.isdir(path.abspath(self.getDawDirsCore(index_daw).getCoreDawText())) or not path.isdir(path.abspath(self.getRefDirsCore(index_ref).getCoreRefText())):
            print self.Interstitial.messages['illegalPaths']
            return

        daw_directories = self.populate(self.getDawDirsCore(index_daw).getCoreDawText())
        print str(len(daw_directories)) + self.Interstitial.messages['WAV_found'] + path.abspath(self.getDawDirsCore(index_daw).getCoreDawText())

        ref_directories = self.populate(self.getRefDirsCore(index_ref).getCoreRefText())
        print str(len(ref_directories)) + self.Interstitial.messages['WAV_found'] + path.abspath(self.getRefDirsCore(index_ref).getCoreRefText())

        try:
            q_action.processEvents()
        except:
            pass

        all_ref_files = []
        all_daw_files = []

        for index in xrange(len(daw_directories)):
            all_daw_files.append(daw_directories[index])

        for index in xrange(len(ref_directories)):
            all_ref_files.append(ref_directories[index])

        scanned_daw_files = []
        scanned_ref_files = []

        # Process Each File In The Tester Array
        for index in xrange(len(daw_directories)):
            found = False
            unmatched_flag = False
            if daw_directories[index] in scanned_daw_files:
                continue

            for e in xrange(len(ref_directories)):
                if ref_directories[e] in scanned_ref_files:
                    continue
                try:
                    q_action.processEvents()
                except:
                    pass

                # If We Haven't Already Processed This File, Process It

                if ref_directories[e] not in targeted_done:

                    # find the offset and align the waveforms
                    toff = self.offs(daw_directories[index], ref_directories[e])

                    try:
                        tester_file_obj = Sndfile(daw_directories[index], 'r')
                    except:
                        print('Corrupted File : '+ daw_directories[index])
                        return
                        pass

                    try:
                        target_file_obj = Sndfile(ref_directories[e], 'r')
                    except:
                        print('Corrupted File : ' + ref_directories[e])
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
                        print('')
                        print "MATCH: " + daw_directories[index] + " matches " + ref_directories[e]

                        try:
                            q_action.processEvents()
                        except:
                            pass
                        # mark files as done
                        test_done_for_files.append(daw_directories[index])
                        targeted_done.append(ref_directories[e])

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
                                            print self.Interstitial.messages['errorFoundBw'] + daw_directories[index] + " and " + ref_directories[e] + " at sample " + str(errs)

                                            try:
                                                q_action.processEvents()
                                            except:
                                                pass

                                            break

                                if errs != 0:
                                    break

                            except RuntimeError:
                                break

                        # Append Metadata For Output
                        values += path.abspath(daw_directories[index]) + "," + path.abspath(ref_directories[e]) + ","
                        values += datetime.datetime.fromtimestamp(stat(daw_directories[index]).st_ctime).strftime("%Y-%m-%d %H:%M:%S") + ","
                        values += str(stat(daw_directories[index]).st_size) + "," + str(tester_file_obj.channels) + "," + str(tester_file_obj.samplerate) + ","
                        values += str(datetime.timedelta(seconds=int(tester_file_obj.nframes / tester_file_obj.samplerate))) + "," + str(errs) + ","
                        values += str(datetime.timedelta(seconds=int(errs/tester_file_obj.samplerate)))

                        values += "\n"
                        found = True
                        unmatched_flag = False

                        scanned_daw_files.append(daw_directories[index])
                        scanned_ref_files.append(ref_directories[e])

                    else:
                        unmatched_flag = True
                        pass

                    if found:
                        break

            if unmatched_flag:
                values += path.abspath(daw_directories[index]) + ", NONE " + ","
                values += "," + "," + "," + ''
                values += "\n"

                scanned_daw_files.append(daw_directories[index])
                print('')
                print "COULD NOT MATCH FILES: " + daw_directories[index]
                print('')

        for single_daw_file in all_daw_files:
            if single_daw_file not in scanned_daw_files:
                values += path.abspath(single_daw_file) + ", NONE "
                values += "," + "," + "," + "," + ''
                values += "\n"
                print('')
                print "COULD NOT MATCH FILES: " + single_daw_file
                print('')
                scanned_daw_files.append(single_daw_file)

        for single_ref_file in all_ref_files:
            if single_ref_file not in scanned_ref_files:
                values += "NONE ," + path.abspath(single_ref_file)
                values += "," + "," + "," + "," + ''
                values += "\n"
                print('')
                print "COULD NOT MATCH FILES: " + single_ref_file
                print('')
                scanned_ref_files.append(single_ref_file)

        # Create Header Information For Manifest
        manifest_info = {'testers': daw_directories, 'file_count': file_count, 'values': values}
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

            response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{current_date}}',
                                                str(manifest_info['current_date']))

            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{initiated}}',
                                                str(manifest_info['initiated']))

            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{seconds}}',
                                                str(manifest_info['seconds_content']))

            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{testers}}',
                                                str(manifest_info['testers']))

            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{bad_files}}',
                                                str(manifest_info['file_count']))

            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{columns}}',
                                                str(manifest_info['columns']))

            if response is False:
                response = self.setValuesForScheduler(template_of_manifest_single_line,
                                                '{{values}}',
                                                manifest_info['values'])

            if response is False:
               # If No Value Found To Replace
                manifest_content += template_of_manifest_single_line
            else:
                manifest_content += response

        return manifest_content

    def setValuesForScheduler(self, string, find_string, replace_with_string):
        """
        @param string: Template String
        @param find_string: Find String string to be replaced with
        @param replace_with_string: String to be replaced with

        @return: String
        """

        try:self.Interstitial = SharedApp.SharedApp.App
        except:pass

        string = string
        find_string = find_string
        replace_with_string = replace_with_string

        if find_string in string:
            return string.replace(find_string, replace_with_string)

        return False