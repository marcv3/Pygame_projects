import os
import math
import sys
import pygame as pg
from time import sleep
from Player import Player
from blocks import Blaster
import config

COLOR_KEY = config.COLOR_KEY
BS = config.BS

class Stormtrooper(Player):
    def __init__(self,location,speed,type="storm_trooper"):
        Player.__init__(self,location,speed,type)
        self.storm_standing_right = pg.image.load("images/storm_standing_right.png").convert()
        self.storm_standing_right.set_colorkey(COLOR_KEY)
        #self.storm_standing_left = pg.image.load("storm_standing_left.png").convert()
        self.storm_standing_left = pg.transform.flip(self.storm_standing_right,True,False)
        self.storm_standing_left.set_colorkey(COLOR_KEY)
        self.storm_marching_right = pg.image.load("images/storm_marching_right.png").convert()
        self.storm_marching_right.set_colorkey(COLOR_KEY)
        #self.storm_marching_left = pg.image.load("storm_marching_left.png").convert()
        self.storm_marching_left = pg.transform.flip(self.storm_marching_right,True,False)
        self.storm_marching_left.set_colorkey(COLOR_KEY)
        self.image = self.storm_standing_right
        self.rect = self.image.get_rect(topleft=location,width=29,height=config.AVATAR_HEIGHT)
        self.speed = speed
        self.pre_update_flag = 1
        self.counter = 0
        self.jump_power = -8.0

    def update(self, obstacles, enemy_blaster, player_blaster, keys, player):
        if(self.pre_update_flag == 0):
            if(player.rect[0] > self.rect[0]):
                self.image = self.storm_marching_right
                self.x_vel = self.speed
            elif(player.rect[0] < self.rect[0]):
                self.image = self.storm_marching_left
                self.x_vel = -self.speed
            elif(player.rect[0] == self.rect[0]):
                self.image = self.storm_standing_right
                self.x_vel = 0

            self.counter += 1

            if((player.rect[1] < self.rect[1])and(self.counter == 120-15)):
                self.jump(obstacles)
            if(self.counter == 120):
                if(self.x_vel > 0):
                    self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2] + 10, self.rect[1] + 12, BS/2, 2),axis=0,speed=20,move_dist=BS*8,direction=1,kind="storm_blast")
                elif(self.x_vel < 0):
                    self.blast = Blaster(pg.Color("red"), (self.rect[0] - 45, self.rect[1] + 12, BS/2, 2),axis=0,speed=20,move_dist=BS*8,direction=-1,kind="storm_blast")
                elif(self.x_vel == 0):
                    self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2] + 10, self.rect[1] + 12, BS/2, 2),axis=0,speed=20,move_dist=BS*8,direction=1,kind="storm_blast")
                enemy_blaster.add(self.blast)
                self.counter = 0

        if(self.pre_update_flag == 1):
            self.dead = pg.sprite.spritecollideany(self, player_blaster)
            self.pre_update(obstacles)
            self.pre_update_flag = 0
        else:
            self.pre_update_flag = 1
            #self.check_keys(keys)
            self.plat_collision(obstacles)
            self.get_position(obstacles)
            self.physics_update()
            if(self.dead):
                self.kill()

    #def check_collisions(self, offset, index, obstacles):
    #    unaltered = True
    #    self.rect[index] += offset[index]
    #    self.obj = pg.sprite.spritecollideany(self, obstacles)
    #    if(self.obj):
    #        self.check_death(self.obj)

    #    while pg.sprite.spritecollideany(self, obstacles):
    #        self.obj = pg.sprite.spritecollideany(self, obstacles)
    #        if(self.obj.type == "storm_blast"):
    #            break
    #        self.rect[index] += (1 if offset[index]<0 else -1)
    #        unaltered = False
    #    return unaltered


