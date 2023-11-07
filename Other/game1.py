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
import soundManager as sm
from soundManager import getVolume, volumeUp, volumeDown
#python D:\stefano\bin\tmp\ESTIM\PROGRAMMING\PROGRAMS\RollTheDice\game1.py

pictRootDir1 = "I:\\bin\\tmp\\ESTIM\\PROGRAMMING\\PICTS\\"
pictRootDir2 = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\\"
pictRootDir3 = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\\"
pictRootDir4 = r"I:\bin\tmp\Pics\\"
PICTROOTDIRLIST = [pictRootDir1,pictRootDir2, pictRootDir3, pictRootDir4]

#MANUAL SETTINGS
NUMDIRS = None
RESCALE=True
pictExt=".jpg"


#sound settings
SOUND_OUTPUT = "Speakers"
SUBCAT="Bryci1" #for floor file loading
ROOTDIR = "I:\\bin\\tmp\\ESTIM\\"

#Initialzing 
pygame.init()
 
#USER-DEFINED EVENTS
PRESS_KEY_OK = pygame.USEREVENT + 1
pygame.time.set_timer(PRESS_KEY_OK, 2000)
KEYACTIVE=False

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
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
DISPLAYSURF.fill(WHITE)

 
# caption and icon
pygame.display.set_caption("Dirty Secrets")
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
   
    def getRnd(self):
        counter = random.randint(0,len(self.imgfiles)-1)
        imgpath=self.imgfiles[counter]
        img=pygame.image.load(imgpath) 
        return img

#check if I: drive is there
if not os.path.exists(ROOTDIR):
    print("Missing " + ROOTDIR)
    sys.exit()
    
AllImages=[]
for pictdir in PICTROOTDIRLIST:
    AllImages.append(Images(pictdir))
igmdiridx=0
 
soundManager = sm.soundData(SOUND_OUTPUT)


while True:   
    background = AllImages[igmdiridx].getRnd()
    ow = background.get_width()
    oh = background.get_height()
    w, h = pygame.display.get_surface().get_size()
    ratio = 1
    if RESCALE:
        ratio = min(w/ow, h/oh)
        background = pygame.transform.scale(background, (ow*ratio, oh*ratio))
    rndx = random.uniform(0, w-ow*ratio)
    rndy = random.uniform(0,h-oh*ratio)
    DISPLAYSURF.blit(background, (rndx,rndy))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            soundManager.stop()
            pygame.quit()
            sys.exit()
        if PRESS_KEY_OK:
            KEYACTIVE= True
            
    pressed_keys = pygame.key.get_pressed()
    #speed up or slow down displaying of images
    if pressed_keys[loc.K_LEFT]:
        FPS -= FPS/2
        volumeDown()
    elif pressed_keys[loc.K_RIGHT]:
        FPS += 1
        volumeUp()
    elif pressed_keys[loc.K_UP]:
        volumeUp()
    elif pressed_keys[loc.K_DOWN]:
        volumeDown()
        
    elif pressed_keys[loc.K_KP_PERIOD]:
         soundManager.playSoundFiles(cat="Calibration", subcat="CalibrateBryci1")
    elif pressed_keys[loc.K_KP1]:
        soundManager.playSoundFiles(cat="Pain",subcat="PainBryciLow")
    elif pressed_keys[loc.K_KP2]:
        soundManager.playSoundFiles(cat="Pain",subcat="PainBryciHigh")
    elif pressed_keys[loc.K_KP3]:
        soundManager.playSoundFiles(cat="Pain",subcat="PainETowerLow")
    elif pressed_keys[loc.K_KP0]:
        soundManager.playSoundFiles(cat="Pain",subcat="PainETowerHigh")
    elif pressed_keys[loc.K_1]:        
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=1)        
    elif pressed_keys[loc.K_2]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=2)
    elif pressed_keys[loc.K_3]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=3)
    elif pressed_keys[loc.K_4]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=4) 
    elif pressed_keys[loc.K_5]:
            soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=5) 
    elif pressed_keys[loc.K_6]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=6) 
    elif pressed_keys[loc.K_7]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=7) 
    elif pressed_keys[loc.K_8]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=8) 
    elif pressed_keys[loc.K_9]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=9) 
    elif pressed_keys[loc.K_0]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=10)
    elif pressed_keys[loc.K_KP4]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=11)
    elif pressed_keys[loc.K_KP5]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=12)
    elif pressed_keys[loc.K_KP6]:
        soundManager.playSoundFiles(cat="Floors",subcat=SUBCAT,floor=13)
    elif pressed_keys[loc.K_KP_PLUS]:
          igmdiridx += 1
          igmdiridx = igmdiridx % len(AllImages)
    elif pressed_keys[loc.K_KP_ENTER] and KEYACTIVE:
           soundManager.stop()
          
    fps = font_small.render("FPS: "+ str(round(FPS,1)) , True, RED)
    vol = font_small.render("Volume: "+ str(round(getVolume(),3)) , True, RED)
    curdir =font_small.render("Directory index: "+ str(igmdiridx) , True, RED)
    
    DISPLAYSURF.blit(fps, (50,h-50))
    DISPLAYSURF.blit(vol, (150,h-50))
    DISPLAYSURF.blit(curdir, (550,h-50))
            
    pygame.display.update()
    FramePerSec.tick(FPS)
