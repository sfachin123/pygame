# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:15:23 2023

@author: stefa
"""
import pygame
import pygame.locals as loc
import random, time
import sys
 
#freesound.org 
#flaticon.com
#freepik.com

#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 120
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
SPEED_DROP = 50
SCORE = 0
MAX_LEVEL=3
MAX_SCORE=5
SCORE_STEP=5
LEVEL=1

#User event for missile firing: only one missile per sec at most
MISSILE_LAUNCH_OK = pygame.USEREVENT + 2
pygame.time.set_timer(MISSILE_LAUNCH_OK, 1000)
CANFIRE=False
#Adding a new User event for creating Aliens
ALIEN_SPAWNING = pygame.USEREVENT + 1
pygame.time.set_timer(ALIEN_SPAWNING, 2000)

 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = pygame.image.load(".//Data//GameOver.png")
game_over = pygame.transform.scale(game_over, (SCREEN_WIDTH, SCREEN_HEIGHT))
#font.render("Game Over", True, BLACK)
level_over = font.render("Level Completed!", True, BLACK)
game_over_win = pygame.image.load(".//Data//LevelUp.png")
game_over_win = pygame.transform.scale(game_over_win, (SCREEN_WIDTH, SCREEN_HEIGHT))
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
background = pygame.image.load(".//Data//spacebkg.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
 
# caption and icon
pygame.display.set_caption("Welcome to My First\
Game: Alien Invasion by Stefano")
#flaticon.com
icon = pygame.image.load(".//Data//battleship.png")
pygame.display.set_icon(icon)

#Creating Sprites Groups
all_sprites = pygame.sprite.Group()
all_missiles = pygame.sprite.Group()
all_aliens = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):   
    def __init__(self):
        super().__init__() 
        rawimage = pygame.image.load(".//Data//battleship.png")
        self.image = pygame.transform.scale(rawimage, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (370, SCREEN_HEIGHT-self.rect.height)
        
    def move(self):
        global CANFIRE
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[loc.K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[loc.K_RIGHT]:
                  self.rect.move_ip(5, 0)
        if pressed_keys[loc.K_SPACE] and CANFIRE:
                pygame.mixer.Sound('.//Data//retro_shoot.mp3').play()
                missile = Missile(self)
                all_sprites.add(missile)
                all_missiles.add(missile)
                CANFIRE = False
         
        if pressed_keys[loc.K_UP]:
            alien = Alien()
            all_sprites.add(alien)
            
class Missile(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        rawimage = pygame.image.load(".//Data/missile.png")
        self.image = pygame.transform.scale(rawimage, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (player.rect.centerx,  SCREEN_HEIGHT-player.rect.height)
    
    def move(self):
        self.rect.move_ip(0, -5)

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #alien
        rawimage = pygame.image.load(".//Data/ufo.png")
        self.image = pygame.transform.scale(rawimage, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), self.rect.height) 
        #alien exploding
        rawimage = pygame.image.load(".//Data/explosion.png")
        self.imagedone = pygame.transform.scale(rawimage, (70, 70))
        
    def move(self):
        self.rect.move_ip(5,0)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
            self.rect.center = (0,self.rect.centery+SPEED_DROP)
    
    
#Setting up Player        
P1 = Player()
all_sprites.add(P1)


def the_end():
    for entity in all_sprites:
          entity.kill() 
    time.sleep(5)
    pygame.quit()
    sys.exit()  
         
#main game loop
while True:   
    DISPLAYSURF.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == ALIEN_SPAWNING:
            A = Alien()
            all_sprites.add(A)
            all_aliens.add(A)    
        
        if event.type == MISSILE_LAUNCH_OK:
            CANFIRE=True
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #Detect collisions between Missile and Alien 
    coll = pygame.sprite.groupcollide(all_aliens, all_missiles, True, True)
    if coll:
        #visualize explosion at location of dead alien
        deadalien = list(coll.keys())[0]
        DISPLAYSURF.blit(deadalien.imagedone,deadalien.rect.center)
        pygame.display.update()        
        pygame.mixer.Sound('.//Data//retro_explosion.wav').play()
        time.sleep(0.2)
        SCORE +=1
        if SCORE > MAX_SCORE:
            DISPLAYSURF.fill(GREEN)
            DISPLAYSURF.blit(level_over, (30,250))
        
            pygame.display.update()
            #start new level
            LEVEL+=1
            SCORE=0
            #need more kills to clear next level
            MAX_SCORE += SCORE_STEP   
            for entity in all_aliens:
                  entity.kill()
            #TO DO: change background
            time.sleep(5)
            
            if LEVEL>MAX_LEVEL:
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(game_over_win, (0,0))
                pygame.display.update()
                pygame.mixer.Sound('.//Data//jingle_win.wav').play()
                time.sleep(1)
               
                the_end()                
        
    for missile in all_missiles:
        if missile.rect.top < 0:
            all_missiles.remove(missile)
            missile.kill()
            
    #Detect if Alien lands and it's game over!
    if pygame.sprite.spritecollideany(P1, all_aliens):
          pygame.mixer.Sound('.//Data//gameover.wav').play()
          time.sleep(1)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (0,0))
           
          pygame.display.update()
          the_end()   
    
    scores = font_small.render("KILLS: " + str(SCORE), True, RED)
    DISPLAYSURF.blit(scores, (10,10))
        
    pygame.display.update()
    FramePerSec.tick(FPS)