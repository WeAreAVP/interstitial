# -*- coding: UTF-8 -*-
from scikits.audiolab import Sndfile
from os import walk, path, stat

track1 =  r'C:\Users\Furqan\Desktop\test\查找問題daw\1.wav'

try:
    test = Sndfile(track1, 'r')
except:
    print('Simple didnt work')
    pass

try:

    track_one_file_obj = Sndfile(track1.decode('cp1252'), 'r')
except:
    print('cp1252 didnt work')
    pass
try:
    track_one_file_obj = Sndfile(track1.encode('utf-8'), 'r')
    print(track_one_file_obj)
except:
    print('encode didnt work')
    pass

try:
    track_one_file_obj = Sndfile(track1.decode('utf-8'), 'r')
    print(track_one_file_obj)
except:
    print('decode didnt work')
    pass


print(track_one_file_obj.readline())
print(track_one_file_obj.nframes)
testing1 = []

def testing():
    asdasd = ''
test


