import os
import math
import sys
import pygame as pg
from time import sleep
from Player import Player
from blocks import Blaster
import config
#COLOR_KEY = (255, 0, 255)
#BS = 40
COLOR_KEY = config.COLOR_KEY
BS = config.BS

class Stormtrooper(Player):
    def __init__(self,location,speed):
        Player.__init__(self,location,speed)
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
        self.rect = self.image.get_rect(topleft=location,width=29,height=self.locked_height)
        self.speed = speed
        self.pre_update_flag = 1
        self.counter = 0
        self.jump_power = -8.0

    def update(self, obstacles, keys, player):
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
                    self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2] + 10, self.rect[1] + 12, BS, 2),axis=0,speed=20,move_dist=22,direction=1)
                elif(self.x_vel < 0):
                    self.blast = Blaster(pg.Color("red"), (self.rect[0] - 45, self.rect[1] + 12, BS, 2),axis=0,speed=20,move_dist=22,direction=-1)
                elif(self.x_vel == 0):
                    self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2] + 10, self.rect[1] + 12, BS, 2),axis=0,speed=20,move_dist=22,direction=1)
                obstacles.add(self.blast)
                self.counter = 0

        if(self.pre_update_flag == 1):
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

