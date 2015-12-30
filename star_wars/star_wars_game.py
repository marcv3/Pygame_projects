import os
import math
import sys
import pygame as pg
from time import sleep
#import blocks
from blocks import Block
from blocks import Platform
from blocks import Blaster
from stormtrooper import Stormtrooper
from Player import Player
import config
# make blocks 40x40
# avatar ~ 30x40

CAPTION = config.CAPTION
SCREEN_SIZE = config.SCREEN_SIZE# x by y
FPS = config.FPS
FULL_SCREEN = config.FULL_SCREEN

#BS = 40
BS=config.BS




class Control(object):
    def __init__(self,FPS):
        self.level_height = 25
        self.level_width = 100
        self.levelsize = (self.level_width*BS,self.level_height*BS)
        self.obstacles = pg.sprite.Group()
        self.storm_troopers = pg.sprite.Group()
        self.f = open(config.LEVEL, 'r')
        self.data = []

        for i in range(self.level_height):
            self.data.append(self.f.readline())
        self.level_map = self.data

        self.x = 0
        self.y = 0
        for row in self.level_map:
            for col in row:
                if col == ".":
                    self.obstacles.add(Block(pg.Color("brown"), (self.x*BS, self.y*BS, BS, BS)))
                if col == "!":    
                    self.obstacles.add(Block(pg.Color("red"), (self.x*BS, self.y*BS, BS, BS),kind="danger"))
                if col == "(":
                    self.player = Player((self.x*BS, self.y*BS), 5)
                if col == "I":
                    self.obstacles.add(Platform(pg.Color("olivedrab"), (self.x*BS, self.y*BS, BS, BS),axis=1,speed=9,move_dist=BS*4,direction=1))
                if col == "i":
                    self.obstacles.add(Platform(pg.Color("olivedrab"), (self.x*BS, self.y*BS, BS, BS),axis=1,speed=4,move_dist=BS*4,direction=-1))
                if col == "_":
                    self.obstacles.add(Platform(pg.Color("olivedrab"), (self.x*BS, self.y*BS, BS, BS), move_dist=BS*4))
                if col == "S":
                    self.storm_troopers.add(Stormtrooper((self.x*BS, self.y*BS), 1))

                self.x += 1
            self.y += 1 
            self.x = 0

        self.f.close()
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.viewport = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = FPS
        self.keys = pg.key.get_pressed()
        self.done = False
        self.level = pg.Surface((self.levelsize[0],self.levelsize[1])).convert()
        self.level_rect = self.level.get_rect()
        self.death = False
        self.die = False
        self.direction = 1
        self.level.fill(pg.Color("lightblue"))
        self.obstacles.draw(self.level)

    def event_loop(self):
        for event in pg.event.get():
            #print(event)
            if (event.type == pg.QUIT):
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_z:
                    self.player.jump(self.obstacles)
                    #self.trooper.jump(self.obstacles)
                if event.key == pg.K_x:
                    self.player.fire = True
                  
                if event.key == pg.K_F1:
                    self.die = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE or event.key == pg.K_z:
                    self.player.jump_cut()        
                    #self.trooper.jump_cut()        

    def update(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_ESCAPE]:
            self.done = True
        self.player.pre_update(self.obstacles)
        self.storm_troopers.update(self.obstacles, self.keys, self.player)

        self.obstacles.update(self.storm_troopers,self.obstacles)
        self.death = self.player.update(self.obstacles, self.keys)
        if(pg.sprite.spritecollideany(self.player, self.storm_troopers)):
            self.death = True
        #self.death = self.trooper.update(self.obstacles, self.keys)
        self.storm_troopers.update(self.obstacles, self.keys, self.player)
        #if(self.trooper.update(self.obstacles, self.keys)):
        self.update_viewport()

    def update_viewport(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def draw(self):
        if self.death or self.die:
            textSurface = pg.font.SysFont("comicsansms", 50).render("YOU DIED!", True, pg.Color("red")) # text example
            textRect = textSurface.get_rect() # text example
            #textRect.center = (int(self.levelsize[0]/2), int(self.levelsize[1]/2) ) # text example
            textRect.center = self.viewport.center#(int(self.viewport[0]/2), int(self.viewport[1]/2) ) # text example
            self.level.fill(pg.Color("white"))
            #self.screen.blit(self.level, (0,0))
            self.screen.blit(self.level, (0,0), self.viewport)
            self.screen.blit(textSurface,textRect,self.viewport) # text example
        else:
            # may only have to draw these once per level
            #if not self.player.fall:
            self.level.fill(pg.Color("lightblue"))
            self.obstacles.draw(self.level)
            #self.level.blit(self.win_text, self.win_rect)

            # must draw these
            self.player.draw(self.level)
            self.storm_troopers.draw(self.level)
            #self.trooper.draw(self.level)
            self.screen.blit(self.level, (0,0), self.viewport)

    def player_image(self):
            self.player.change_image()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def check_death(self):
        if self.death or self.die:
            sleep(.25)
            self.death = False
            self.die = False
            Control.__init__(self,FPS)
        

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.player_image()
            self.draw()
            pg.display.update()
            self.check_death()
            self.clock.tick(self.fps)
            self.display_fps()


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    if(FULL_SCREEN):
        pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN)
    else:
        pg.display.set_mode(SCREEN_SIZE)
    #LUKE_SPRITES = pg.image.load("luke_sprites0.png").convert()    
    #LUKE_SPRITES.set_colorkey(COLOR_KEY)
    run_it = Control(FPS)
    run_it.main_loop()
    pg.quit()
    sys.exit()
