# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:54:33 2023

@author: stefa
"""
 # -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 16:01:21 2023

@author: stefa
"""
import pygame
import pygame.locals as loc
import random, os
import sys
from glob import glob
#mport game1_sound as sound
import soundManager_V2 as sm
import cv2

#python D:\stefano\bin\tmp\ESTIM\PROGRAMMING\PROGRAMS\RollTheDice\game1.py

#Picture Directories
pictRootDir1 = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\\"
pictRootDir2 = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\\"
PICTROOTDIRLIST = [pictRootDir1,pictRootDir2]
SUBCATS = ["Bryci1", "Bryci2", "ETower"]
PAINSUBCATS = ["PainBryciLow", "PainBryciHigh", "PainETowerHigh"]

#sound settings
SOUND_OUTPUT = "Speakers"
ROOTDIR = "I:\\bin\\tmp\\ESTIM\\"

#MANUAL SETTINGS
NUMDIRS = None
RESCALE=True
pictExt=".jpg"

#Pick SUBCAT
IDX=1

#GLOBALS
PAINONLY=False
PLAY_VIDEO=False
SUBCAT = SUBCATS[IDX]
PAINSUBCAT= PAINSUBCATS[IDX]
fileMMCN=r"I:\bin\tmp\ESTIM\OLDMP3\Butterfly Effect\Butterfly Effect\01 Butterfly flight.mp3"
ENDGAME_FLOOR=16
PLAYBACKSPEED_STEPUP=1.10 #for sound playback
VOLUME_STEPUP=1.0  # in dB. NOTE: -6.0 dB = half volume !
ORIG_VOLUME = sm.getVolume()
#
print("ORIGINAL VOLUME = " +str(ORIG_VOLUME))

#Initialzing 
pygame.init()
 
#USER-DEFINED EVENTS
PRESS_KEY_OK = pygame.USEREVENT + 1
pygame.time.set_timer(PRESS_KEY_OK, 2000)
KEYACTIVE=False

GOTO_NEXT_FLOOR = pygame.USEREVENT  + 2 
pygame.time.set_timer(GOTO_NEXT_FLOOR, 10000)
FLOOR=1

PAINPROB=25 #10%

#Setting up FPS 
FPS = 3
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

#Setting up Fonts
font_big = pygame.font.SysFont("Verdana", 180)
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
DISPLAYSURF.fill(WHITE)

###########    VIDEO SETUP ##############
#USER-DEFINED EVENTS
NEW_MOVIE_CLIP = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_MOVIE_CLIP, 4000)

#moviefile = r"I:\bin\tmp\ESTIM\ESTIMHERO\CH JOI Addicted Zombie Goon TS Redux-1.m4v"
#moviefile =r"I:\bin\tmp\ESTIM\ESTIMHERO\PEP10\PEP10-stim audio.mp4"
#moviefile=r"I:\bin\tmp\VR\Adriana\adriana.mp4"
moviefile=r"I:\bin\tmp\ESTIM\ESTIMHERO\CH RLGL JOI Amyl Zombie Redux-1.m4v"
video = cv2.VideoCapture(moviefile)
VIDEO_FPS = video.get(cv2.CAP_PROP_FPS)
# get total number of frames
totalFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)

#########################################

#check if I: drive is there
if not os.path.exists(ROOTDIR):
    print("Missing " + ROOTDIR)
    sys.exit()
    
# caption and icon
pygame.display.set_caption("Dirty Secrets Automated, with movie")
icon = pygame.image.load(r"I:\bin\tmp\Pics\659 Nina James Large\659_060.jpg")
pygame.display.set_icon(icon)

        
class Images():
    def __init__(self, rootdir, *args, **kwargs):
        
        #pick random picture directory and load all pictures from there
        pictDirs = glob(rootdir+"/*/")
        self.imglist=[]
        self.imgfiles=[]
        if NUMDIRS:
            #pick random NUMDIRS directories from  pictDirs
            selectedPictDirs = []
            rndidxs = list(range(0,len(pictDirs)))
            random.shuffle(rndidxs)
            for rn in rndidxs[0:NUMDIRS]:
                selectedPictDirs.append(pictDirs[rn])
        else:
            selectedPictDirs = pictDirs
            
        for pictDir in selectedPictDirs:        
            files=os.listdir(pictDir)
            self.imgfiles.extend([ os.path.join(pictDir,f) for f in files if f.endswith(pictExt)])
   
    def getRnd(self,filterw=None, exclude=True):
        counter = random.randint(0,len(self.imgfiles)-1)
        imgpath=self.imgfiles[counter]
        #print(imgpath)
        if filterw:
            skip = (filterw in imgpath) if exclude else (filterw not in imgpath)
            while skip:
                #print("Skipping: " + imgpath  )
                counter = random.randint(0,len(self.imgfiles)-1)
                imgpath=self.imgfiles[counter]
                skip = (filterw in imgpath) if exclude else (filterw not in imgpath)
        #print(imgpath)
        img=pygame.image.load(imgpath) 
        return img
    
    
AllImages=[]
for pictdir in PICTROOTDIRLIST:
    AllImages.append(Images(pictdir))
#image directory index. Used to loop through different picture directory via key action
IMGDIRIDX=0 
 
soundManager = sm.soundData(SOUND_OUTPUT)

def playSoundfile(excludepain):
    global FLOOR, PLAY_VIDEO
    if excludepain:
        if FLOOR  < ENDGAME_FLOOR:
            print("FLOOR: " + str(FLOOR))
            soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=FLOOR)
            #FLOOR += 1
        else:        
            print("NOW!")
            print("FLOOR: " + str(FLOOR))
            print("ENDGAME_FLOOR: " + str(ENDGAME_FLOOR))
            if FLOOR==ENDGAME_FLOOR:
                print("LAST SONG")
                soundManager.playSoundFiles(filename=fileMMCN)
                #FLOOR +=1 #only increase speed and volume after end game is reached                
                PLAY_VIDEO = True    
            #this can be moved to user event if different timing is desired
            #randomly either increase volume of playback speed
            rnd = random.randint(0, 1)
            if rnd == 1: 
                soundManager.fasterPlayback(PLAYBACKSPEED_STEPUP)
                print(round(soundManager.audioController.get_multiplier(),2))
            else:
                sm.volumeUp(VOLUME_STEPUP)
                print("VOLUME = " + str(sm.getVolume()))
    else:
        print("PAIN on FLOOR " + str(FLOOR))       
        soundManager.playSoundFiles(cat="Pain",subcat=PAINSUBCAT)
        #if FLOOR <= 13: #stay on same floor
        #    FLOOR -= 1

def excludepain(floor):
   if floor == 1:
        return True
   elif floor <=13:
       return True if random.randint(0,100) > PAINPROB else False
   elif floor < ENDGAME_FLOOR:
       return False
   else:
       return True

def exitAndCleanup():
    sm.setVolume(ORIG_VOLUME)
    print("EXIT VOLUME = " + str(sm.getVolume()))
    soundManager.stop()
    cv2.destroyAllWindows() 
    pygame.quit()
    sys.exit()
 
class PictureForDisplaying():
    def __init__(self, bexcludepain, *args, **kwargs):
        #print("bexcludepain inPictureForDisplaying:" + str(bexcludepain))
        background = AllImages[IMGDIRIDX].getRnd(filterw="pain",exclude=bexcludepain)
        ow = background.get_width()
        oh = background.get_height()
        w, h = pygame.display.get_surface().get_size()
        ratio = 1
        if RESCALE:
            ratio = min(w/ow, h/oh)
            background = pygame.transform.scale(background, (ow*ratio, oh*ratio))
        rndx = random.uniform(0, w-ow*ratio)
        rndy = random.uniform(0,h-oh*ratio)
        position = (rndx, rndy)
        self.background = background
        self.position = position

#start sound for first floor
soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=1)
bexcludepain=True

#MAIN LOOP
while True:      
    floor = font_small.render("Floor: " + str(FLOOR) , True, RED)          
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitAndCleanup()
        if event.type == PRESS_KEY_OK:
            KEYACTIVE= True
        if event.type == GOTO_NEXT_FLOOR:
            FLOOR +=1
            bexcludepain = excludepain(FLOOR) 
            #print("Exclude pain: "+str(bexcludepain))
            playSoundfile(bexcludepain)            
        if event.type == NEW_MOVIE_CLIP:
            randomFrameNumber=random.randint(0, totalFrames)
            # set frame position at random start  
            video.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber)
    
    if PLAY_VIDEO:
        success, video_image = video.read()
        #print("VIDEO OK:" +str(success))
        if success:
            #print("Playing Video")
            video_surf = pygame.image.frombuffer(
                 video_image.tobytes(), video_image.shape[1::-1], "BGR")
        DISPLAYSURF.blit(video_surf, (0, 0))
    else:  
        picture =  PictureForDisplaying(bexcludepain)
        DISPLAYSURF.blit(picture.background, picture.position)
        
    pressed_keys = pygame.key.get_pressed()
    #speed up or slow down displaying of images
    if pressed_keys[loc.K_LEFT]:
        FPS -= FPS/2
        sm.volumeDown()
    elif pressed_keys[loc.K_RIGHT]:
        FPS += 1
        sm.volumeUp()
    elif pressed_keys[loc.K_UP]:
        sm.volumeUp()
    elif pressed_keys[loc.K_DOWN]:
        sm.volumeDown()
        
    elif pressed_keys[loc.K_KP_PLUS]:
          IMGDIRIDX += 1
          IMGDIRIDX = IMGDIRIDX % len(AllImages)
    elif pressed_keys[loc.K_KP_ENTER] and KEYACTIVE:
           soundManager.stop()
    elif pressed_keys[loc.K_INSERT]:
            soundManager.fasterPlayback()
    elif pressed_keys[loc.K_DELETE]:
             soundManager.slowerPlayback()   
          
    fps = font_small.render("FPS: "+ str(round(FPS,1)) , True, RED)
    vol = font_small.render("Volume: "+ str(round(sm.getVolume(),3)) , True, RED)
    curdir =font_small.render("Directory index: "+ str(IMGDIRIDX) , True, RED)
    mult = round(soundManager.audioController.get_multiplier(),2)
    dispmult = font_small.render("Multiplier: "+ str(mult) , True, RED)    
    
    w, h = pygame.display.get_surface().get_size()
    DISPLAYSURF.blit(fps, (50,h-50))
    DISPLAYSURF.blit(vol, (150,h-50))
    DISPLAYSURF.blit(curdir, (550,h-50))
    DISPLAYSURF.blit(dispmult, (350,h-50))        
    
    
    if  bexcludepain:
         DISPLAYSURF.blit(floor, (20,h-SCREEN_HEIGHT+10))  
    else:
         pain = font_big.render("PAIN!", True, RED)
         DISPLAYSURF.blit(pain, (SCREEN_WIDTH/2, h-SCREEN_HEIGHT + 50)) 
        
    pygame.display.update()
    if PLAY_VIDEO:
        FramePerSec.tick(VIDEO_FPS)
    else:
        FramePerSec.tick(FPS)
