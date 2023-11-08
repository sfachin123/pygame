# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 18:15:53 2023

@author: stefa
"""
from pydub import AudioSegment
import os
import glob
from soundManager_V2 import ROOTDIR, soundDirDict

def ogg2wav(ofn):
    wfn = ofn.replace('.ogg','.wav')
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav')    # maybe use original resolution to make smaller
    
filename="I:\\bin\\tmp\\ESTIM\\PROGRAMMING\\GuideMe-v0.4.3-Windows.64-bit\\BrycisEstimExperience\\AAaudio\\xxh018a.ogg"
#ogg2wav(filename)

def ogg2wav_ffmpeg(fn):
    import subprocess
    from subprocess import check_output
    ifn=fn
    ofn = fn.replace('.ogg','.wav')
    print("Writing "+ ofn)
    #return_code=subprocess.run(["ffmpeg", "-i", ifn, "-ac 2",  ofn], shell=True)
    #print(return_code)
    check_output("ffmpeg -i " + ifn + " -ac 2 " + ofn, shell=True)
    return ofn

#ofn=ogg2wav_ffmpeg(filename)
#AudioSegment.from_file(ofn)

soundDir=soundDirDict["Floors"]["Bryci1"]
oggFileList = glob.glob(soundDir +"\\**\*" + ".ogg", recursive=True)
wavFileList = glob.glob(soundDir +"\\**\*" + ".wav", recursive=True)
#print(oggFileList)
print(len(oggFileList))
print(len(wavFileList))
#for fn in oggFileList:
#    ogg2wav_ffmpeg(fn)
    