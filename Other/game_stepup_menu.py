# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:45:24 2023

@author: stefa
"""
import sys
import pygame
import pygame_menu
from pygame_menu import themes
 
pygame.init()
menusurface = pygame.display.set_mode((600, 400))
 
update_loading = pygame.USEREVENT + 0

class Menu():
    def __init__(self, *args, **kwargs):
        self.mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_SOLARIZED)
        self.mainmenu.add.text_input('Pain Prob (in %): ', default='25',onchange=self.setPainProb)
        self.mainmenu.add.button('Play', self.start_the_game)
        self.mainmenu.add.button('Levels', self.level_menu)
        self.mainmenu.add.button('Quit', pygame_menu.events.EXIT)
        #self.PAINPROB=self.mainmenu.get_value()
        self.run()
    
    def setPainProb(self):
        pass
        #self.PAINPROB=
        
    def set_difficulty(self, value, difficulty):
        print(value)
        print(difficulty)
     
    def start_the_game(self):
        self.mainmenu._open(self.loading)
        pygame.time.set_timer(update_loading, 30)
        from game_stepup import game_loop
        game_loop()
        
    def level_menu(self):
        self.mainmenu._open(self.level)
 
    def run(self):
        self.level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
        self.level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
         
        self.loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
        self.loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
         
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
               pygame.quit()
               sys.exit()
     
        if menu.mainmenu.is_enabled():
            menu.mainmenu.update(events)
            menu.mainmenu.draw(menusurface)
            if ( menu.mainmenu.get_current().get_selected_widget()):
                menu.arrow.draw(menusurface,  menu.mainmenu.get_current().get_selected_widget())
     
        pygame.display.update()
    