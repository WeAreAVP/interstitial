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

class InterstitialCore(object):
    def __init__(self):
        pass

    def mono(self, numpyMatrix):
        """
        mono(numpy matrix ar)
        reduces an n-dimensional matrix to a 1-dimensional list if n > 1
        if n = 1, returns it
        """
        if numpyMatrix.ndim > 1:
            return numpyMatrix[:,0]
        else:
            return numpyMatrix

    def offs(self, track1, track2):
        """
        offs(audiofile track1, audiofile track2)
        calculates the head offset between two (supposedly) otherwise identitical audio files
        this is achieved via finding the peak-to-peak difference of the waveform heads
        """

        # opens files for reading
        trackOneFileObj = Sndfile(track1, 'r')
        trackTwoFileObj = Sndfile(track2, 'r')

        # calculates the head of each file (first twentieth of the waveform)
        # if this is less than 5 seconds of audio (that is, the waveform is under 100 seconds long)
        # then the head is the first five seconds of the waveform
        trackOneFileObjhead = floor(.05 * trackOneFileObj.nframes)
        if trackOneFileObjhead < (trackOneFileObj.samplerate * 5):
            trackOneFileObjhead = trackOneFileObj.nframes

        trackTwoFileObjhead = floor(.05 * trackTwoFileObj.nframes)
        if trackTwoFileObjhead < (trackTwoFileObj.samplerate * 5):
            trackTwoFileObjhead = trackTwoFileObj.nframes

        # reads the head of each file (as absolute values, accounting for reversed waveforms)
        # into a 1-dimensional numpy matrix (via mono function)
        numpyMatrixOftrack1 = self.mono(np.absolute(trackOneFileObj.read_frames(trackOneFileObjhead)))
        numpyMatrixOftrack2 = self.mono(np.absolute(trackTwoFileObj.read_frames(trackTwoFileObjhead)))

        # returns the difference between the peak of each list
        return np.argmax(numpyMatrixOftrack1) - np.argmax(numpyMatrixOftrack2)

    def populate(self, dir):
        """
        populate (filepath dir)
        walks the file tree under dir recursively and returns all .wav files in it
        """
        populatedList = []
        wav = compile('.[Ww][Aa][Vv]$')
        for root, subFolders, files in walk(dir):
            for singleFile in files:
                if wav.search(singleFile):
                    populatedList.append(path.join(root, singleFile))

        return populatedList

    def execute(self, firstWavefile, secondWavefile, directory, QAction):
        """
        execute (wavefile firstWavefile, wavefile secondWavefile, directory d, QAction qa)
        the heart of interstitial - performs a null test on two wav files and returns the first difference
        """

        # initialize useful variables
        filename = "manifest_" + strftime("%Y%m%d%H%M%S") + ".csv"
        testDone = []
        targDone = []
        table = "Test File,Reference File,Creation Date,Size,Channels,Sample Rate,Length,First Error Sample,Error At"
        meta = "Interstitial Error Report\n"
        timer = time()
        initiated = strftime("%H:%M:%S")
        count = 0

        # ensures that we have legitimate directories to walk down
        # and populates the list of files to test
        if not path.isdir(path.abspath(firstWavefile)) or not path.isdir(path.abspath(secondWavefile)):
            print "Illegal paths given - exiting..."
            return
        testers = self.populate(firstWavefile)
        print str(len(testers)) + " WAV files found: " + path.abspath(firstWavefile)
        targets = self.populate(secondWavefile)
        print str(len(targets)) + " WAV files found: " + path.abspath(secondWavefile)
        QAction.processEvents()

        # process each file in the tester array
        for index in xrange(len(testers)):
            found = False
            for e in xrange(len(targets)):
                QAction.processEvents()
                # if we haven't already processed this file, process it
                if str(targets[e]) not in targDone:
                    # find the offset and align the waveforms
                    toff = self.offs(testers[index], targets[e])
                    testerFileObj = Sndfile(testers[index], 'r')
                    targetFileObj = Sndfile(targets[e], 'r')
                    if toff > 0:
                        testerFileObj.seek(toff)
                    else:
                        targetFileObj.seek(fabs(toff))
                    # read the first 1000 samples of each file
                    # if each sample is within 6dB of the other, we have a match and can begin processing
                    numpyMatrixOftrack1 = self.mono(testerFileObj.read_frames(1000))
                    numpyMatrixOftrack2 = self.mono(targetFileObj.read_frames(1000))

                    if np.array_equal(numpyMatrixOftrack1, numpyMatrixOftrack2):
                        print "MATCH: " + str(testers[index]) + " matches " + str(targets[e])
                        QAction.processEvents()

                        # mark files as done
                        testDone.append(str(testers[index]))
                        targDone.append(str(targets[e]))

                        # we can't read the entire file into RAM at once
                        # so instead we're breaking it into one-second parts
                        l = min((testerFileObj.nframes - toff), (targetFileObj.nframes - toff)) / testerFileObj.samplerate
                        for n in xrange(0, l, 1):
                            errs = 0
                            try:
                                # drop all but the first channel
                                trackOneResponse = self.mono(testerFileObj.read_frames(testerFileObj.samplerate))
                                trackTwoResponse = self.mono(targetFileObj.read_frames(targetFileObj.samplerate))

                                # are these arrays equivalent? if not, there's an error
                                if not np.array_equal(trackOneResponse, trackTwoResponse):
                                    count += 1
                                    # where's the error?
                                    # we find it by comparing sample by sample across this second of audio
                                    for m in xrange(len(trackOneResponse)):
                                        if not np.array_equal(trackOneResponse[m], trackTwoResponse[m]):
                                            # we found it! print a message and we're done with these files
                                            errs = (n * testerFileObj.samplerate) + m + 1000
                                            print "ERROR: Interstitial error found between " + str(testers[index]) + " and " + str(targets[e]) + " at sample " + str(errs)
                                            QAction.processEvents()
                                            break
                                if errs != 0:
                                    break
                            except RuntimeError:
                                break

                        # append metadata for output
                        table += "\n" + path.abspath(testers[index]) + "," + path.abspath(str(targets[e])) + ","
                        table += datetime.datetime.fromtimestamp(stat(testers[index]).st_ctime).strftime("%Y-%m-%d %H:%M:%S") + ","
                        table += str(stat(testers[index]).st_size) + "," + str(testerFileObj.channels) + "," + str(testerFileObj.samplerate) + ","
                        table += str(datetime.timedelta(seconds=int(testerFileObj.nframes / testerFileObj.samplerate))) + "," + str(errs) + ","
                        table += str(datetime.timedelta(seconds=int(errs/testerFileObj.samplerate)))
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
                print "Wrote manifest to " + path.abspath(f.name)
                f.close()
            except:
                print "Illegal path: " + directory + filename