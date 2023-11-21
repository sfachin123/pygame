# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:45:24 2023

@author: stefa

REFERENCE: https://github.com/ppizarror/pygame-menu/blob/master/pygame_menu/examples/
"""
import sys
import pygame
import pygame_menu
from pygame_menu import themes
#from game_stepup import game_loop, PAINPROB
import game_stepup as gsu

CALIBRATE_NORMAL = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\calibrate2.mp3" 
CALIBRATE_PAIN = r"I:\bin\tmp\ESTIM\PROGRAMMING\GuideMe-v0.4.3-Windows.64-bit\The-Estim-Tower\AAaudio\calibrate-pain.mp3"

pygame.init()
menusurface = gsu.DISPLAYSURF #pygame.display.set_mode((600, 400))
 
update_loading = pygame.USEREVENT + 0


class Menu():
    def defineMenuOptions(self):
        # Selectable items
        self.sound_dd = [('Speakers', 'Speakers'),
             ('Oculus Rift', 'Oculus Rift'),
             ]
    
    def __init__(self, *args, **kwargs):
        self.defineMenuOptions()
        self.originalVolume = gsu.sm.getVolume()
        
        #set up main menu
        self.mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_SOLARIZED)
        self.painprob = self.mainmenu.add.range_slider("Pain Probability (in %)", default=int(25), 
                                                       onchange=self.setPainProb,
                                                       range_values=[1,99], 
                                                       increment=1, 
                                                       value_format=lambda x: str(int(x)))
        
        self.audiooutput = self.mainmenu.add.dropselect(
            'Select Audio Output',
            self.sound_dd,
            default=0,
            dropselect_id='audio_output_drop',
            onchange=self.setAudioOutput
        ),
        
        # Create discrete range for FLOOR SELECTION
        k=range(0,gsu.TOP_FLOOR-1)
        v=range(1,gsu.TOP_FLOOR)
        range_values_discrete = dict(zip(k,v))
        self.startingFloor = self.mainmenu.add.range_slider('Starting Floor', 0, list(range_values_discrete.keys()),
                                       rangeslider_id='range_slider_discrete',
                                       slider_text_value_enabled=False,
                                       width = 300,
                                       onchange = self.setStartingFloor,
                                       value_format=lambda x: str(range_values_discrete[x]))
        
        self.mainmenu.add.button('Calibrate Sound', self.calibrate_sound)        
        self.mainmenu.add.button('Play', self.start_the_game)
        self.mainmenu.add.button('Quit', pygame_menu.events.EXIT)
        
        self.setUpSoundSubmenu()
        self.loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
        self.loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
    
    def setPainProb(self, value):
        gsu.PAINPROB = int(self.painprob.get_value())
    
    def setAudioOutput(self, value1, value2):
        gsu.SOUND_OUTPUT =  self.audiooutput[0].get_value()[0][1]
        #NOT HOOKED UP IN SOUNDMANAGER YET!
    
    def setStartingFloor(self, value):
        gsu.FLOOR = int(self.startingFloor.get_value())
        
    def calibrateSound(self):
        gsu.soundManager.playSoundFiles(filename=CALIBRATE_NORMAL)
    
    def calibrateSoundPain(self):
        gsu.soundManager.playSoundFiles(filename=CALIBRATE_PAIN)
        
    def increaseVolumePain(self):
        gsu.sm.volumeUp(1.0)
        gsu.PAIN_VOLUME =  gsu.sm.getVolume()
        print("vol = " + str(gsu.PAIN_VOLUME))
     
    def decreaseVolumePain(self):
        gsu.sm.volumeDown(1.0)
        gsu.PAIN_VOLUME =  gsu.sm.getVolume()
        print("vol = " + str(gsu.PAIN_VOLUME))
    
    def stopSoundCalibration(self):
         gsu.soundManager.stop()
         
     
    def start_the_game(self):
        self.mainmenu._open(self.loading)
        pygame.time.set_timer(update_loading, 30)       
        gsu.game_loop()
        
    
    def calibrate_sound(self):
        self.mainmenu._open(self.calibrate_sound)
        
    
    def setUpSoundSubmenu(self):
        self.calibrate_sound = pygame_menu.Menu('Calibrate Sound for Pain', 600, 400, theme=themes.THEME_BLUE)
        self.calibrate_sound.add.button('Calibrate Sound', self.calibrateSound)
        self.calibrate_sound.add.button('Calibrate Pain Sound', self.calibrateSoundPain)        
        self.calibrate_sound.add.button('Higher Volume', self.increaseVolumePain)
        self.calibrate_sound.add.button('Decrease Volume', self.decreaseVolumePain)  
        self.calibrate_sound.add.button('Stop Calibration', self.stopSoundCalibration)                
        self.arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
        
if __name__ == "__main__":         
    menu=Menu()
     
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = menu.loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
            if event.type == pygame.QUIT:
               gsu.sm.setVolume(menu.originalVolume)
               print("EXIT VOLUME = " + str(gsu.sm.getVolume()))
               gsu.soundManager.stop()
               pygame.quit()
               sys.exit()
     
        if menu.mainmenu.is_enabled():
            menu.mainmenu.update(events)
            menu.mainmenu.draw(menusurface)
            if ( menu.mainmenu.get_current().get_selected_widget()):
                menu.arrow.draw(menusurface,  menu.mainmenu.get_current().get_selected_widget())
     
        pygame.display.update()
    