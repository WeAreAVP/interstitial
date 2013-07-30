import numpy as np
from scikits.audiolab import Sndfile
from sys import argv, exit
from math import fabs, floor
from re import compile
from os import walk, path, stat
from time import strftime, time
import datetime

# mono(numpy matrix ar)
# reduces an n-dimensional matrix to a 1-dimensional list if n > 1
# if n = 1, returns it
def mono(ar):
	if ar.ndim > 1:
		return ar[:,0]
	else:
		return ar

# inRange (1d numpy matrix x, 1d numpy matrix y y)
# returns if x is approximately one-half to twice the value of y
# this is done to accomodate for up to 6dB differences between workstation and reference devices
def inRange(x, y):
	return (np.absolute(x) <= (2.1 * np.absolute(y))).all() and (np.absolute(x) >= (0.4 * np.absolute(y))).all()

# offs(audiofile track1, audiofile track2)
# calculates the head offset between two (supposedly) otherwise identitical audio files
# this is achieved via finding the peak-to-peak difference of the waveform heads
def offs(track1, track2):
	# opens files for reading
	s1 = Sndfile(track1, 'r')
	s2 = Sndfile(track2, 'r')

	# calculates the head of each file (first twentieth of the waveform)
	# if this is less than 5 seconds of audio (that is, the waveform is under 100 seconds long)
	# then the head is the first five seconds of the waveform
	s1head = floor(.05 * s1.nframes)
	if s1head < (s1.samplerate * 5):
		s1head = s1.nframes
	s2head = floor(.05 * s2.nframes)
	if s2head < (s2.samplerate * 5):
		s2head = s2.nframes
	
	# reads the head of each file (as absolute values, accounting for reversed waveforms)
	# into a 1-dimensional numpy matrix (via mono function)
	t1 = mono(np.absolute(s1.read_frames(s1head)))
	t2 = mono(np.absolute(s2.read_frames(s2head)))
	
	# returns the difference between the peak of each list
	return np.argmax(t1) - np.argmax(t2)

# populate (filepath dir)
# walks the file tree under dir recursively and returns all .wav files in it
def populate(dir):
	l = []
	wav = compile('.[Ww][Aa][Vv]$')
	for root, subFolders, files in walk(dir):
		for file in files:
			if wav.search(file):
				l.append(path.join(root, file))
	return l

# execute (wavefile a, wavefile b, directory d, QAction qa)
# the heart of interstitial - performs a null test on two wav files and returns the first difference
def execute(a, b, d, qa):
	# initialize useful variables
	filename = "manifest_" + strftime("%Y%m%d%H%M%S") + ".csv"
	testdone = []
	targdone = []
	table = "Test File,Reference File,Creation Date,Size,Channels,Sample Rate,Length,First Error Sample,Error At"
	meta = "Interstitial Error Report\n"
	timer = time()
	initiated = strftime("%H:%M:%S")
	count = 0

	# ensures that we have legitimate directories to walk down
	# and populates the list of files to test
	if not path.isdir(path.abspath(a)) or not path.isdir(path.abspath(b)):
		print "Illegal paths given - exiting..."
		return
	testers = populate(a)
	print str(len(testers)) + " WAV files found: " + path.abspath(a)
	targets = populate(b)
	print str(len(targets)) + " WAV files found: " + path.abspath(b)
	qa.processEvents()
	
	# process each file in the tester array
	for t in xrange(len(testers)):
		found = False
		for e in xrange(len(targets)):
			qa.processEvents()
			# if we haven't already processed this file, process it
			if str(targets[e]) not in targdone:
				# find the offset and align the waveforms
				toff = offs(testers[t], targets[e], 0, 0)
				tX = Sndfile(testers[t], 'r')
				tY = Sndfile(targets[e], 'r')
				if toff > 0:
					tX.seek(toff)
				else:
					tY.seek(fabs(toff))
				# read the first 1000 samples of each file
				# if each sample is within 6dB of the other, we have a match and can begin processing
				t1 = mono(tX.read_frames(1000))
				t2 = mono(tY.read_frames(1000))
				if inRange(t1, t2):
					print "MATCH: " + str(testers[t]) + " matches " + str(targets[e])
					qa.processEvents()
					
					# mark files as done
					testdone.append(str(testers[t]))
					targdone.append(str(targets[e]))
					
					# we can't read the entire file into RAM at once
					# so instead we're breaking it into one-second parts
					l = min((tX.nframes - toff), (tY.nframes - toff)) / tX.samplerate
					for n in xrange(0, l, 1):
						errs = 0
						try:
							# drop all but the first channel
							a1 = mono(tX.read_frames(tX.samplerate))
							a2 = mono(tY.read_frames(tY.samplerate))
							
							# is this second of audio within 6dB of the other?
							# if not, there's an error!
							if not inRange(a1, a2):
								count += 1
								# where's the error?
								# we find it by comparing sample by sample across this second of audio
								for m in xrange(len(a1)):
									if not inRange(a1[m], a2[m]):
										# we found it! print a message and we're done with these files
										errs = (n * tX.samplerate) + m + 1000
										print "ERROR: Interstitial error found between " + str(testers[t]) + " and " + str(targets[e]) + " at sample " + str(errs)
										qa.processEvents()
										break
							if errs != 0:
								break
						except RuntimeError:
							break
					# append metadata for output
					table += "\n" + path.abspath(testers[t]) + "," + path.abspath(str(targets[e])) + ","
					table += datetime.datetime.fromtimestamp(stat(testers[t]).st_ctime).strftime("%Y-%m-%d %H:%M:%S") + ","
					table += str(stat(testers[t]).st_size) + "," + str(tX.channels) + "," + str(tX.samplerate) + ","
					table += str(datetime.timedelta(seconds=int(tX.nframes / tX.samplerate))) + "," + str(errs) + ","
					table += str(datetime.timedelta(seconds=int(errs/tX.samplerate)))
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
			f = open(d + "/" + filename, 'w')
			f.write(meta + table)
			print "Wrote manifest to " + path.abspath(f.name)
			f.close()
		except:
			print "Illegal path: " + d + filename

if __name__ == '__main__':
	execute(argv[1], argv[2])
