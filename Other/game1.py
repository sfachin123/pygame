# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 16:01:21 2023

@author: stefa
"""
import pygame
import pygame.locals as loc
import random, time, os
import sys
from glob import glob
import multisound2 as ms2
import tkinter as tk 

pictRootDir1 = "I:\\bin\\tmp\\ESTIM\\PROGRAMMING\\PICTS\\"
pictRootDir2 = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\BrycisEstimExperience\\"
pictRootDir3 = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\\"

#MANUAL SETTINGS
NUMDIRS = 1
RESCALE=True
pictRootDir = pictRootDir1 
pictExt=".jpg"

#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 2
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

class Window:
	def __init__(self):
		root = tk.Tk()
		root.title("SOUND CONTROL")

		hello = tk.Toplevel(root)
		hello.title("Hello")
		hello.but1 = tk.Button(hello,
			text="Hello Button",
			command= lambda : tk.messagebox.showinfo("Hello and attention",
				"A button in a secundary window has been pressed abruptely!")
			)
		hello.but1.pack()

		root.mainloop()

class Images():
    def __init__(self, *args, **kwargs):
        
        #pick random picture directory and load all pictures from there
        pictDirs = glob(pictRootDir+"/*/")
        self.imglist=[]
        #pick random NUMDIRS directories from  pictDirs
        selectedPictDirs = []
        rndidxs = list(range(0,len(pictDirs)-1))
        random.shuffle(rndidxs)
        for rn in rndidxs[0:NUMDIRS]:
            selectedPictDirs.append(pictDirs[rn])
            
        for pictDir in selectedPictDirs:        
            files=os.listdir(pictDir)
            self.imgfiles = [ os.path.join(pictDir,f) for f in files if f.endswith(pictExt)]
            self.imglist.extend([pygame.image.load(f) for f in self.imgfiles])
   
    def getRnd(self):
        counter = random.randint(0,len(self.imglist)-1)
        img=self.imglist[counter]
        return img
 

AllImages = Images()    
#ms2.main()
rect = pygame.Rect(100,100,100,50)
click = font.render("Open Sound Window", 1, (0,0,0))
       
while True:   
    background = AllImages.getRnd()
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
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if rect.collidepoint(pygame.mouse.get_pos()):
               Window()

    pygame.draw.rect(DISPLAYSURF, (255, 255,255), rect)
    DISPLAYSURF.blit(click, rect)
                 
    pressed_keys = pygame.key.get_pressed()
    #speed up or slow down displaying of images
    if pressed_keys[loc.K_LEFT]:
        FPS -= FPS/2
    elif pressed_keys[loc.K_RIGHT]:
        FPS += 3
            
    level = font_small.render("LEVEL: 1" , True, RED)
    DISPLAYSURF.blit(level, (150,10))
                
    pygame.display.update()
    FramePerSec.tick(FPS)
