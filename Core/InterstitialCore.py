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

#custome libs
from Config import messages
from Config import Configuration

class InterstitialCore(object):
    def __init__(self):
        self.configuration = Configuration.Configuration()
        pass

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

    def execute(self, first_wave_file, second_wave_file, directory, q_action):
        """
        execute (wavefile first_wave_file, wavefile second_wave_file, directory d, QAction qa)
        the heart of interstitial - performs a null test on two wav files and returns the first difference
        """

        # initialize useful variables
        #"manifest_" + strftime("%Y%m%d%H%M%S") + ".csv"
        filename = self.configuration.getManifestFileName()
        test_done = []
        targ_done = []
        table = messages.message['table']
        meta = messages.message['meta']
        timer = time()
        #strftime("%H:%M:%S")
        initiated = self.configuration.getCurrentTime()
        count = 0

        # ensures that we have legitimate directories to walk down
        # and populates the list of files to test
        if not path.isdir(path.abspath(first_wave_file)) or not path.isdir(path.abspath(second_wave_file)):
            print messages.message['illegalPaths']
            return

        testers = self.populate(first_wave_file)
        print str(len(testers)) + messages.message['WAVfound'] + path.abspath(first_wave_file)
        targets = self.populate(second_wave_file)
        print str(len(targets)) + messages.message['WAVfound'] + path.abspath(second_wave_file)
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
                                    count += 1
                                    # where's the error?
                                    # we find it by comparing sample by sample across this second of audio
                                    for m in xrange(len(track_one_response)):
                                        if not np.array_equal(track_one_response[m], track_two_response[m]):
                                            # we found it! print a message and we're done with these files
                                            errs = (n * tester_file_obj.samplerate) + m + 1000
                                            print messages.message['errorfoundbw'] + str(testers[index]) + " and " + str(targets[e]) + " at sample " + str(errs)
                                            q_action.processEvents()
                                            break
                                if errs != 0:
                                    break
                            except RuntimeError:
                                break

                        # append metadata for output
                        table += "\n" + path.abspath(testers[index]) + "," + path.abspath(str(targets[e])) + ","
                        table += datetime.datetime.fromtimestamp(stat(testers[index]).st_ctime).strftime("%Y-%m-%d %H:%M:%S") + ","
                        table += str(stat(testers[index]).st_size) + "," + str(tester_file_obj.channels) + "," + str(tester_file_obj.samplerate) + ","
                        table += str(datetime.timedelta(seconds=int(tester_file_obj.nframes / tester_file_obj.samplerate))) + "," + str(errs) + ","
                        table += str(datetime.timedelta(seconds=int(errs/tester_file_obj.samplerate)))
                        found = True

                    if found:
                        break

        # create header information for manifest
        meta += "Date," + strftime("%Y-%m-%d") + "\n"
        meta += "Time initiated," + initiated + "\n"
        meta += "Duration (seconds)," + str(floor(time() - timer)) + "\n"
        meta += "Files analyzed," + str(len(testers)) + "\n"
        meta += "Bad files found," + str(count) + "\n"

        # do we have metadata? if so, write a manifest
        if len(table) > 110:
            try:
                f = open(directory + "/" + filename, 'w')
                f.write(meta + table)
                print messages.message['wroteManifest'] + path.abspath(f.name)
                f.close()
            except:
                print messages.message['illegalPath'] + directory + filename