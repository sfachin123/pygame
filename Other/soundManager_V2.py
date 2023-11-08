# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 14:58:40 2023

@author: stefa
"""
import os
import time
import glob
import random
import sounddevice as sd
import threading
import soundfile as sf
import enum 

#for git commit
#copy D:\stefano\bin\tmp\ESTIM\PROGRAMMING\PROGRAMS\RollTheDice\soundManager.py D:\stefano\Learning\Programming\Python\pygame\Other\

    #sound settings
ROOTDIR = "I:\\bin\\tmp\\ESTIM\\"
soundExt = [".mp3", ".wav"]

DATA_TYPE = "int16"

OUTPUT_DICT = {
    "Speakers" : 3,
    "OculusRift" : 6
    }

DEVICE = OUTPUT_DICT["Speakers"]

OUTPUT_DICT_REV = {y:x for x,y in OUTPUT_DICT.items()}

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
        

class Status(enum.Enum):
    NONE = "NONE"
    PLAYING = "PLAYING"


class AudioController:
    def __init__(self):
        self._status = Status.NONE
        self.multiplier=1.0

    def set_file_name(self,filename):
        self.filename = filename
    
    def get_file_name(self):
        return self. filename
    
    def set_multiplier(self,multiplier):
        self.multiplier = multiplier
    
    def get_multiplier(self):
        return self. multiplier
    
    def stop(self) -> None:
        self._status = Status.NONE
        print("Stopping playback.")
        sd.stop()

    def play_file_async(self, filepath: str, loop: bool = False, device: int = 3, multiplier: float = 1.0) -> None:
        def play_with_callback() -> None:
            self._play(filepath, loop=loop, device=device, multiplier=multiplier)
            print("Device = " + OUTPUT_DICT_REV[device]  + ". Playing " + filepath )
            #callback()
        thread = threading.Thread(target=play_with_callback)
        thread.start()

    def _play(self, filepath: str, loop: bool = False, device: int = 3,  multiplier: float = 1.0) -> None:
        data, fs = sf.read(filepath)
        self._status = Status.PLAYING
        sd.play(data, samplerate=int(fs*multiplier), loop=loop, device=device)

audiocontroller = AudioController()
        
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
        audiocontroller.set_file_name(filename)
        multiplier= audiocontroller.get_multiplier()
        audiocontroller.play_file_async(filename, loop=True, device=DEVICE, multiplier=multiplier)           
 
    def fasterPlayback(self):
        filename=audiocontroller.get_file_name()
        multiplier= audiocontroller.get_multiplier()*1.1 
        audiocontroller.set_multiplier(multiplier)
        audiocontroller.play_file_async(filename, loop=True, device=DEVICE, multiplier=multiplier)  
        
    def slowerPlayback(self):
        filename=audiocontroller.get_file_name()
        multiplier= audiocontroller.get_multiplier()*0.9
        audiocontroller.set_multiplier(multiplier)
        audiocontroller.play_file_async(filename, loop=True, device=DEVICE, multiplier=multiplier)  
        
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
        #filename=r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio\xxh020a.wav"
        return filename
    
    def getnext(self,filelist):
        for f in filelist:
            yield f
        
    def stop(self):
        audiocontroller.stop()
 
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
    testOculus=False
       
    sd = soundData("Speakers")
    sd.playSoundFiles()
    time.sleep(5)
    sd.stop()
    sd.playSoundFiles()
    time.sleep(5)
    sd.stop()
    if testOculus:
        sd2=soundData("OculusRift")
        sd2.playSoundFiles()
        time.sleep(5)
        sd2.stop()
        
    
if __name__ == "__main__":
    testing()
    #testing2()