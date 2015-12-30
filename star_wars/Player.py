import os
import math
import sys
import pygame as pg
from time import sleep
from blocks import Blaster

COLOR_KEY = (255, 0, 255)
BS = 40
class Player(pg.sprite.Sprite):
    def __init__(self,location,speed):
        pg.sprite.Sprite.__init__(self)
        self.locked_height = 47
        LUKE_SPRITES = pg.image.load("luke_sprites0.png").convert() 
        LUKE_SPRITES.set_colorkey(COLOR_KEY)
        self.luke_stand_ls = LUKE_SPRITES.subsurface((274,27,29,self.locked_height))
        self.luke_stand_gun_right = LUKE_SPRITES.subsurface((6,276,34,self.locked_height))
        self.luke_stand_gun_left = pg.transform.flip(self.luke_stand_gun_right,True,False)
        self.luke_jump_gun_right = LUKE_SPRITES.subsurface((2,348,33,self.locked_height))
        self.luke_jump_gun_left = pg.transform.flip(self.luke_jump_gun_right,True,False)
        self.image = self.luke_stand_ls
        self.rect = self.image.get_rect(topleft=location,width=29,height=self.locked_height)
        self.speed = speed
        self.jump_power = -10.0
        self.jump_cut_magnitude = -3.0
        self.on_moving = False
        self.collide_below = False
        self.dead = False
        self.lastHit = "right"
        self.fire = False

        self.x_vel = self.y_vel = 0
        self.grav = 0.4
        self.fall = False
        self.going_down = False

    def Fire_blaster(self,obstacles):
        if(self.fire):
            if(self.lastHit == "right"):
                self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2], self.rect[1] + 12, BS, 2),axis=0,speed=20,move_dist=22,direction=1)

            if(self.lastHit == "left"):
                self.blast = Blaster(pg.Color("red"), (self.rect[0] - 40, self.rect[1] + 12, BS, 2),axis=0,speed=15,move_dist=22,direction=-1)
                #self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2], self.rect[1] + 12, BS, 2),axis=0,speed=20,move_dist=22,direction=-1)
            obstacles.add(self.blast)
            self.fire = False
    # when the player jumps
    #
    def jump(self, obstacles):
        if not self.fall and not self.check_above(obstacles):
            self.y_vel = self.jump_power
            self.fall = True
            self.on_moving = False

    # check if player is in contact with a block above it
    #
    def check_above(self, obstacles):
        self.rect.move_ip(0, -1)
        collide = pg.sprite.spritecollideany(self, obstacles)
        self.rect.move_ip(0, 1)
        return collide

    # when the user releases the space bar early
    #
    def jump_cut(self):
        if self.fall:
            if self.y_vel < self.jump_cut_magnitude:
                self.y_vel = self.jump_cut_magnitude

    # run before the update
    #
    def pre_update(self, obstacles):
        self.collide_below = self.check_below(obstacles)

    # see if player is in contact with the ground.
    # If standing on platform, update x_vel and y_vel
    #
    def check_below(self, obstacles):
        self.rect.move_ip((0,1))
        self.collide = pg.sprite.spritecollideany(self, obstacles)
        self.rect.move_ip((0,-1))
        self.x_vel = 0
        if self.collide and (self.collide.type == "platform"):
            if(self.collide.axis == 0):
                self.x_vel += self.collide.speed*self.collide.direction
            else:
                if(self.collide.direction > 0) and not self.fall:
                    self.going_down = True
                    self.y_vel += self.collide.speed*self.collide.direction
                else:
                    self.going_down = False

        if self.collide and (self.collide.type == "danger"):
            self.dead = True

        return self.collide

    # updates player
    #
    def update(self, obstacles, keys):
        self.check_keys(keys)
        self.plat_collision(obstacles)
        self.get_position(obstacles)
        self.physics_update()
        self.Fire_blaster(obstacles)
        return self.dead
        #self.dead = False

    # checks if left or right move key is pressed, and adds to self.x_vel
    #
    def check_keys(self,keys):
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.lastHit = "left"
            self.x_vel -= self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.x_vel += self.speed
            self.lastHit = "right"

    # check if in contact with moving platform
    #
    def plat_collision(self, obstacles):
        self.check_collisions_plat(obstacles)

    # move player until no longer in contact with platform
    #
    def check_collisions_plat(self, obstacles):
        self.count = 0
        platform = pg.sprite.spritecollideany(self, obstacles)
        if(platform):
            if(platform.type == "platform"):
                while pg.sprite.spritecollideany(self, obstacles):
                    self.count += 1
                    self.rect[platform.axis] += platform.direction
                    if (platform.max_speed) < self.count:
                        self.dead = True

            if(platform.type == "danger"):
                self.dead = True

    # puts player in the correct position
    #
    def get_position(self, obstacles):
        if self.x_vel:
            self.check_collisions((self.x_vel,0), 0, obstacles)
        if not self.fall:
            self.check_falling(obstacles)
            if self.going_down:
                self.check_collisions((0,self.y_vel), 1, obstacles)
        else:
            self.fall = self.check_collisions((0,self.y_vel), 1, obstacles)

    # after moving prescribed distance, check if there are any collisions.
    # if there are, step back one pixel and try again.
    #
    def check_collisions(self, offset, index, obstacles):
        unaltered = True
        self.rect[index] += offset[index]
        self.obj = pg.sprite.spritecollideany(self, obstacles)
        if(self.obj):
            if (self.obj.type == "danger"):
                self.dead = True
        while pg.sprite.spritecollideany(self, obstacles):
            self.obj = pg.sprite.spritecollideany(self, obstacles)
            self.rect[index] += (1 if offset[index]<0 else -1)
            unaltered = False
        return unaltered

    # checks if the player is falling
    #
    def check_falling(self, obstacles):
        if not self.collide_below:
            self.fall = True
            self.on_moving = False

    # slows fall by adding gravity to self.y_vel
    #
    def physics_update(self):
        if self.fall:
            self.y_vel += self.grav
        else:
            self.y_vel = 0


    # blit player to surface
    #
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def change_image(self):
        if self.fall:
            if self.lastHit == "right":
                self.image = self.luke_jump_gun_right
            elif self.lastHit == "left":
                self.image = self.luke_jump_gun_left
        else:
            if self.lastHit == "right":
                self.image = self.luke_stand_gun_right
            elif self.lastHit == "left":
                self.image = self.luke_stand_gun_left
