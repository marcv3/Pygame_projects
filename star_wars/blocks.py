import os
import math
import sys
import pygame as pg
from time import sleep
import config

class Block(pg.sprite.Sprite):
    def __init__(self,color,rect,kind = "normal"):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = kind

class Lightsaber(Block):
    def __init__(self,color,rect,kind , image ):
        Block.__init__(self, color, rect, kind)
        self.timer = 0
        #ls_sprites = pg.image.load("images/luke_sprites0.png").convert()
        #ls_sprites.set_colorkey(config.COLOR_KEY)
        #self.image = ls_sprites.subsurface((440,288,config.BS,7))
        self.image = image

    def update(self,storm_troopers,obstacles):
        self.swing()

    def swing(self):
        self.timer += 1
        if(self.timer == 5):
            self.kill()

    #def draw(self, surface):
    #    surface.blit(self.image, self.rect)

class Platform(Block):
    def __init__(self,color,rect,speed=4,axis=0,delay=30,move_dist=40*4,direction=1,kind="platform"): 
        Block.__init__(self, color, rect,kind)
        self.speed = speed
        self.max_speed = speed
        self.axis = axis# 0 - left/right, 1 - up/down
        self.delay = delay# delay at end of move
        self.move_dist = move_dist# distance to move before changing direction
        self.moving = True
        self.direction = direction# 1 - move to the right, -1 - move to the left
        self.dist_moved = 0
        self.timer = 0
        self.type = kind

    # move platform
    #
    def move_platform(self):
        if self.moving:
            self.rect[self.axis] += self.direction*self.speed
            #self.old_data = self.direction*self.speed
            #self.dist_moved += 1
            self.dist_moved += abs(self.direction*self.speed)

            if self.dist_moved >= self.move_dist:
                self.dist_moved = 0
                self.moving = False
                self.speed = 0
        else:
            self.timer += 1
            if (self.timer >= self.delay):
                self.direction *= -1
                self.moving = True
                self.timer = 0
                self.speed = self.max_speed

    def update(self,storm_troopers,obstacles):
        self.move_platform()    

class Blaster(Platform):
    def __init__(self,color,rect,speed=10,axis=0,delay=1,move_dist=40*5,direction=0,kind="danger"):
        Platform.__init__(self,color,rect,speed,axis,delay,move_dist,direction,kind)

    def update(self,storm_troopers,obstacles):
        self.move_platform(storm_troopers,obstacles)    

    def move_platform(self,storm_troopers,obstacles):
        if self.moving:
            self.rect[self.axis] += self.direction*self.speed
            #self.old_data = self.direction*self.speed
            self.dist_moved += abs(self.direction*self.speed)

            self.sprite_coll = pg.sprite.spritecollideany(self, obstacles) # check if a sprite colledes with its own group?
            #print(self.sprite_coll.type)

            # find a way to keep bullet moving through storm troopers
            if(self.type == "player_blast"):
                if (self.dist_moved >= self.move_dist)or(pg.sprite.spritecollideany(self, storm_troopers))or(pg.sprite.spritecollideany(self, obstacles)):
                    #if (self.dist_moved >= self.move_dist)or(pg.sprite.spritecollideany(self, storm_troopers)or(self.sprite_coll.type != self.type)):
                        #self.dist_moved = 0
                        self.moving = False
                        #self.speed = 0

            elif(self.type == "storm_blast"):
                if (self.dist_moved >= self.move_dist)or(pg.sprite.spritecollideany(self, obstacles)):
                    #if (self.dist_moved >= self.move_dist)or(pg.sprite.spritecollideany(self, storm_troopers)or(self.sprite_coll.type != self.type)):
                        #self.dist_moved = 0
                        self.moving = False
                        #self.speed = 0
        else:
            self.kill()

