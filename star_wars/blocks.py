import os
import math
import sys
import pygame as pg
from time import sleep

class Block(pg.sprite.Sprite):
    def __init__(self,color,rect,kind = "normal"):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = kind

class Platform(Block):
    def __init__(self,color,rect,speed=4,axis=0,delay=30,move_dist=50,direction=1,kind="platform"): 
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
            self.dist_moved += 1

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
    def __init__(self,color,rect,speed=10,axis=0,delay=1,move_dist=10,direction=0,kind="danger"):
        Platform.__init__(self,color,rect,speed,axis,delay,move_dist,direction,kind)

    def update(self,storm_troopers,obstacles):
        self.move_platform(storm_troopers,obstacles)    

    def move_platform(self,storm_troopers,obstacles):
        if self.moving:
            self.rect[self.axis] += self.direction*self.speed
            #self.old_data = self.direction*self.speed
            self.dist_moved += 1

            #print(pg.sprite.spritecollideany(self, obstacles)) # check if a sprite colledes with its own group?
            if (self.dist_moved >= self.move_dist)or(pg.sprite.spritecollideany(self, storm_troopers)):
                #self.dist_moved = 0
                self.moving = False
                #self.speed = 0
        else:
            self.kill()

