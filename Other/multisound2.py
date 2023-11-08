import tkinter as tk
import sounddevice
import threading
import soundfile
import os, random

LOCAL= False
if LOCAL:
    ROOTDIR = r"D:\stefano\bin\tmp\ESTIM\\"
else:
    ROOTDIR = "I:\\bin\\tmp\\ESTIM\\"
    

soundETDir = ROOTDIR + r"PROGRAMMING\2B-ONLY EstimTowerMod\\"
soundExt = [".mp3",".ogg", ".wav"]

soundDirDict={
    "Bryci1": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio\\",
    "Bryci2": ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\AAaudio.2\\",
    "ETower":  ROOTDIR + r"PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\\",
    "Lucifer": ROOTDIR + r"NEWMP3\StLucifer-20230912T204051Z-003\StLucifer\\",
    "OldMp3": ROOTDIR + r"OLDMP3\\",
    }
soundDirDefault = soundDirDict["Bryci1"]

soundDirPainLow=r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\originalpainfiles\\"
soundDirPainHigh=r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\louderpainfiles\\"

channel2=r"I:\bin\tmp\voice\playlist\loop1Blong.mp3"
DATA_TYPE = "int16"
OUTPUT2 = (18, "OculusRift")
OUTPUT1 = (20, "Speakers")

#GUI related
myWindow = tk.Tk()
floor_var = tk.StringVar()
floor_var.set("3") #default

#for looping on calibration files 
counter=0    

class myThread(threading.Thread):
    def __init__(self, args, ffilter=None):
        threading.Thread.__init__(self)        
        self.args=args 
        self.ffilter = ffilter
    def run(self):
        playmp3(self.args, self.ffilter)
        
class streamData:
    def __init__(self, index):
        self.outstream = self.create_running_output_stream(index)
    
    def create_running_output_stream(self, index): 
            output = sounddevice.RawOutputStream(
                device=index,
                dtype=DATA_TYPE
            )
            return output

class musicData:
    def __init__(self, path=None, soundDir=soundDirDefault):
        if path:
            self.music = self.load_sound_file_into_memory(path)
        else:
            if "OLDMP3" in soundDir:
                print("Loading all OLDMP3 files, recursively")
                self.filelist = self.loadOldMP3(soundDir)
            else:
                self.filelist = self.sound_file_paths(soundDir)
            print("Loaded filelist contains " + str(len(self.filelist)) + " files")
            
            self.ETfilelist = self.sound_file_paths(soundETDir)
            self.calibratefilelist = [f for f in self.ETfilelist if os.path.basename(f).startswith("calibrate")]
            self.calibratefilelist.sort()
            
            print("soundDir="+soundDir)
            if "Bryci" in soundDir:
                print("loading pain form Brici")
                self.painfilelist = [f for f in self.filelist if os.path.basename(f).startswith("x")]
            else:
                painDir = selectPainDir()
                painfilelist = self.sound_file_paths(painDir)
                self.painfilelist = [f for f in painfilelist if os.path.basename(f).startswith("x")]
            
            self.floorfilelist=[]
            loadfrom = self.filelist if "Bryci" in soundDir else self.ETfilelist
            for i in range(1,15):
                self.floorfilelist.append([f for f in loadfrom if os.path.basename(f).startswith(str(i))])
            
    def loadOldMP3(self, soundDir):
        import glob
        filelist  = [f for f in glob.glob(soundDir +"\\*\*\*\*") if f.endswith(".mp3")]   
        filelist.extend([f for f in glob.glob(soundDir +"\\*\*\*") if f.endswith(".mp3")])   
        filelist.extend([f for f in glob.glob(soundDir +"\\*\*") if f.endswith(".mp3")])   
        return filelist

    def load_sound_file_into_memory(self,path): 
        audio_data, _ = soundfile.read(path, dtype=DATA_TYPE)
        return audio_data
    
    def sound_file_paths(self,soundDir):
        try :
            files=os.listdir(soundDir)
            return [ os.path.join(soundDir,f) for f in files if os.path.splitext(f)[1] in soundExt]
        except:
            return []
    
    
class soundDevices:
    
    def list_all_soundevices(self):
        return [index_info for index_info in enumerate(sounddevice.query_devices())]
    
    def filter_soundevices(self, hostapi):
        return [x for x in self.list_all_soundevices() if x[1]["hostapi"]==hostapi] 
    
    def list_available_sounddevices(self):
        return self.filter_soundevices(3)


song1 = musicData()
song2 = musicData(channel2)

# Set new sound directory from dropdown 
def selectSoundDir(): 
     global song1
     key = clicked.get() 
     soundDir = soundDirDict[key]
     print("Selected " + soundDir)
     song1 =  musicData(soundDir=soundDir)

def selectPainDir():
    key = clickedPain.get()
    if key == optionsPain[0]: #normal
        painDir = soundDirPainLow
    else:
        painDir = soundDirPainHigh
    print("painDir="+painDir)
    return painDir
        
    
# Dropdown menu options 
options = list(soundDirDict.keys())
optionsPain = ["Normal","Hard"]  

# datatype of menu text 
clicked = tk.StringVar() 
clickedPain = tk.StringVar()
  
# initial menu text 
clicked.set(options[0])
clickedPain.set(optionsPain[0])

stream1 = streamData(OUTPUT1[0])
stream2 = streamData(OUTPUT2[0])

def on_closing():
    stream1.outstream.stop()
    stream2.outstream.stop()
    myWindow.destroy()
        
def playmp3(args, ffilter=None):
    global counter
        
    if args==1:
        if ffilter=="pain":
            filelist = song1.painfilelist
        elif ffilter =="calibrate":
             filelist = song1.calibratefilelist
        elif ffilter  and ffilter.startswith("floor"):
            floor = int(ffilter.split("floor")[1])
            filelist = song1.floorfilelist[floor-1]
        else:
            filelist = song1.filelist
        
        if ffilter != "calibrate":
            file=random.choice(filelist)
        else:
            file=filelist[counter] 
            if counter < 3:
                counter += 1
            else:
                counter = 0               
                       
        song = song1.load_sound_file_into_memory(file)
        print("Playing " + file)
        stream1.outstream.write(song)
    else:
        print("Playing " + channel2)
        stream2.outstream.write(song2.music)

def playRandom():    
    global thread1
    stream1.outstream.stop()
    print("Playing sound on output " + str(OUTPUT1[0]) + ": " + OUTPUT1[1]) 
    thread1 = myThread(1)
    stream1.outstream.start()
    thread1.start()
    
def play2():
    global thread2
    stream2.outstream.stop()
    print("Playing sound on output " + str(OUTPUT2[0]) + ": " + OUTPUT2[1])
    thread2 = myThread(2)
    stream2.outstream.start()
    thread2.start()
    
def stop1():
    print("Stopping sound on output " + str(OUTPUT1[0]) + ": " + OUTPUT1[1])
    stream1.outstream.stop()
    #print(thread1.isAlive())
    
def stop2():
    print("Stopping sound on output " + str(OUTPUT2[0]) + ": " + OUTPUT2[1])
    stream2.outstream.stop()
    #print(thread2.isAlive())

def floor():
    print("Playing sound from floor " + str(floor_var.get()) +" on output " + str(OUTPUT1[0]) + ": " + OUTPUT1[1]) 
    stream1.outstream.stop()
    floor=floor_var.get()
    thread1 = myThread(1,"floor"+str(floor))
    stream1.outstream.start()
    thread1.start()

def pain():
    global thread1
    stream1.outstream.stop()
    print("Playing pain sound on output " + str(OUTPUT1[0]) + ": " + OUTPUT1[1])    
    thread1 = myThread(1,"pain")
    stream1.outstream.start()
    thread1.start()

def calibrate():
    global thread1
    stream1.outstream.stop()
    print("Playing calibration sound on output " + str(OUTPUT1[0]) + ": " + OUTPUT1[1])    
    thread1 = myThread(1,"calibrate")
    stream1.outstream.start()
    thread1.start()
    
 #GUI   

def changeVolume(dbinput):
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    #import math
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume 
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(currentVolumeDb + float(dbinput), None)
     # NOTE: -6.0 dB = half volume !
def volumeUp():
    changeVolume(1.0)

def volumeDown():
    changeVolume(-1.0)
    
def main():
    rowStop=8
    
    myWindow.title('Python MP3 player')
    tk.Label(myWindow, text="").grid(row=0)
    tk.Label(myWindow, text="").grid(row=1)
    tk.Label(myWindow, text="").grid(row=2,column=0,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='random', command=playRandom).grid(row=2, column=1,sticky=tk.W, padx=5, pady=5)
    tk.OptionMenu( myWindow , clicked , *options ).grid(row=2,column=2,sticky=tk.W, padx=15, pady=15) 
    tk.Button( myWindow , text = "Select" , command = selectSoundDir ).grid(row=2,column=3,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='voice', command=play2).grid(row=2, column=6, sticky=tk.W, padx=5, pady=5)
    tk.Label(myWindow, text="").grid(row=2,column=4,sticky=tk.W, padx=15, pady=15)
    tk.Label(myWindow, text="").grid(row=3)
    tk.Label(myWindow, text="").grid(row=4,column=1,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='floor', command=floor).grid(row=4, column=1,sticky=tk.W, padx=5, pady=5)
    tk.Label(myWindow, text="Floor").grid(row=4,column=2,sticky=tk.W, padx=15, pady=15)
    tk.Entry(myWindow,textvariable=floor_var).grid(row=4,column=3,sticky=tk.W, padx=15, pady=15)
    tk.Label(myWindow, text="").grid(row=5)
    tk.Label(myWindow, text="").grid(row=6,column=0,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='pain', command=pain).grid(row=6, column=1,sticky=tk.W, padx=5, pady=5)
    tk.Button(myWindow, text='calibrate', command=calibrate).grid(row=6, column=2,sticky=tk.W, padx=15, pady=15)
    tk.OptionMenu( myWindow , clickedPain , *optionsPain ).grid(row=6,column=3,sticky=tk.W, padx=15, pady=15) 
    tk.Button( myWindow , text = "Select" , command = selectSoundDir ).grid(row=6,column=4,sticky=tk.W, padx=15, pady=15)
    tk.Label(myWindow, text="").grid(row=7)
    tk.Label(myWindow, text="").grid(row=rowStop,column=0,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='stop', command=stop1).grid(row=rowStop, column=1,sticky=tk.W, padx=5, pady=5)
    tk.Label(myWindow, text="").grid(row=rowStop,column=2,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='stop', command=stop2).grid(row=rowStop, column=6, sticky=tk.W, padx=5, pady=5)
    tk.Label(myWindow, text="").grid(row=rowStop,column=3,sticky=tk.W, padx=15, pady=15)
    tk.Button(myWindow, text='volumeUp', command=volumeUp).grid(row=rowStop, column=2,sticky=tk.W, padx=5, pady=5)    
    tk.Button(myWindow, text='volumeDown', command=volumeDown).grid(row=rowStop, column=3,sticky=tk.W, padx=5, pady=5)    
    
    myWindow.protocol("WM_DELETE_WINDOW", on_closing)
    
    #myWindow.mainloop()

if __name__ == "__main__":
    #import sys
    main()