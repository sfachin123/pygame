# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 14:58:40 2023

@author: stefa
"""
import os
import time
import glob
import random
import sounddevice
import threading
import soundfile

#sound settings
ROOTDIR = "I:\\bin\\tmp\\ESTIM\\"
soundExt = [".mp3",".ogg", ".wav"]

DATA_TYPE = "int16"

OUTPUT_DICT = {
    "Speakers" : 20, #3
    "OculusRift" : 18, #6
    }

class streamData:
    def __init__(self, index):
        self.outstream = self.create_running_output_stream(index)
    
    def create_running_output_stream(self, index): 
            output = sounddevice.RawOutputStream(
                device=index,
                dtype=DATA_TYPE
            )
            return output        

stream1 = streamData(OUTPUT_DICT["Speakers"])

class myThread(threading.Thread):
    def __init__(self, song):
        threading.Thread.__init__(self)        
        self.song = song
    def run(self):
        while True:
            stream1.outstream.write(self.song)        
        

soundDirDict={
    "Floors":
        {
            "Bryci1": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio\\",
            "Bryci2": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio.2\\",
            "ETower":  ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\\",
    },
    "Pain":
        {
            "PainBryciLow": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio\\",
            "PainBryciHigh": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio.2\\",
            "PainETowerLow": ROOTDIR + r"PROGRAMMING\\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\originalpainfiles\\",
            "PainETowerHigh": ROOTDIR + r"PROGRAMMING\\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\louderpainfiles\\",   
            },
    "Calibration":
        {   
            "CalibrateBryci1": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio\\",
            "CalibrateBryci2": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio.2\\",
            "CalibrateETower":  ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\\",
            },
    "Other":
        {        
            "Lucifer": ROOTDIR + r"NEWMP3\StLucifer-20230912T204051Z-003\StLucifer\\",
            "OldMp3": ROOTDIR + r"OLDMP3\\",
        } ,   
    }

class soundData():
    def __init__(self, channel):
        self.channel = channel
        self.soundFileDict = {}
        self.calibfilelist = None
        for k,subdict in soundDirDict.items():
            self.soundFileDict[k]={}
            startsWith = self.startswith(k)
            for k2,item  in subdict.items():                                    
                self.soundFileDict[k][k2] = self.getFileList(item,startsWith)
            
    def startswith(self,k):
        if k == "Pain":
            return "x"
        elif k == "Calibration":
            return "calibrate"
        else:
            return None
            
    def getFileList(self,soundDir,startsWith=None): 
        filelist=[]
        for ext in soundExt:
            l = glob.glob(soundDir +"\\**\*" + ext, recursive=True)
            if not startsWith:
                filelist.extend(l)
            else:
                filelist.extend([f for f in l if os.path.basename(f).startswith(startsWith)])
        #print("Sound file list from " + soundDir + "contains: \n" + str(len(filelist)) + " files") 
        return filelist
      
    def playSoundFiles(self, cat="Floors", subcat=None, floor=1): 
        filename = self.getRandom(cat,subcat,floor)            
        song, fs = soundfile.read(filename, dtype=DATA_TYPE)
        
        print("Playing on " + self.channel + ": "  + filename)               
        
        #NEW
        stream1.outstream.stop()
        
        thread = myThread(song)
        #NEW
        stream1.outstream.start()
        
        thread.start()
        
    def getRandom(self, cat="Pain", subcat=None, floor=1):
        if not subcat:
            subcat = random.choice(list(self.soundFileDict[cat].keys()))
        flist = self.soundFileDict[cat][subcat]
        if cat=="Floors":
            flist = [f for f in flist if os.path.basename(f).startswith(str(floor))]
            if floor==1:
                #to avoid >=10 floors
                flist = [f for f in flist if len(os.path.basename(f))<9]
        if cat == "Calibration":
            if self.calibfilelist:
                try:
                    filename = next(self.calibfilelist)
                except StopIteration:
                    self.calibfilelist =None #to reset iteration
            
            if not self.calibfilelist:
                flist.sort()
                self.calibfilelist = self.getnext(flist)            
                filename = next(self.calibfilelist)
        else:
            filename = random.choice(flist)
        #for testing
        #filename=r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio\xxh045b.wav"
        #to test looping
        #filename=r"I:\bin\tmp\ESTIM\PROGRAMMING\Tease AI 0.54.9\Audio\GNMAudio\Spanking\cane.mp3"
        return filename
    
    def getnext(self,filelist):
        for f in filelist:
            yield f
        
    def stop(self):
        print("stopping playback (stream.stop)")
        stream1.outstream.stop()
 
#VOLUMN CONTROL
def getVolumeObj():
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    #import math
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

def changeVolume(dbinput):
    volume = getVolumeObj()
    # Get current volume 
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(currentVolumeDb + float(dbinput), None)
     # NOTE: -6.0 dB = half volume !

def volumeUp():
    try:
        changeVolume(1.0)
    except:
        pass

def volumeDown():
    try:
        changeVolume(-1.0)
    except:
        pass

def getVolume():
    try:
        volumeObj = getVolumeObj()
        volume = volumeObj.GetMasterVolumeLevel()
    except:
        volume = -999
    return volume
        
def testing():       
    sd = soundData("Speakers")
    sd.playSoundFiles()
    #time.sleep(5)
    sd.stop()
    sd2=soundData("OculusRift")
    #sd2.playSoundFiles()
    #sd.play2()
    time.sleep(5)
    sd2.stop()

if __name__ == "__main__":
    testing()
