import os
import math
import sys
import pygame as pg
from time import sleep
from blocks import Blaster
from blocks import Lightsaber
import config

COLOR_KEY = config.COLOR_KEY
BS = config.BS

class Player(pg.sprite.Sprite):
    def __init__(self,location,speed,type="player"):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        luke_sprites = pg.image.load("images/luke_sprites0.png").convert() 
        luke_sprites.set_colorkey(COLOR_KEY)
        self.luke_stand_ls_right = luke_sprites.subsurface((274,27,29,config.AVATAR_HEIGHT))
        self.luke_stand_ls_left = pg.transform.flip(self.luke_stand_ls_right,True,False)

        self.luke_swing_ls_right = []
        self.luke_swing_ls_right.append(luke_sprites.subsurface((352,276,54,config.AVATAR_HEIGHT)))
        self.luke_swing_ls_right.append(luke_sprites.subsurface((410,276,65,config.AVATAR_HEIGHT)))
        self.luke_swing_ls_right.append(luke_sprites.subsurface((567,276,60,config.AVATAR_HEIGHT)))
        self.luke_swing_ls_right.append(luke_sprites.subsurface((654,276,54,config.AVATAR_HEIGHT)))

        self.luke_swing_ls_left = []
        self.luke_swing_ls_left.append(pg.transform.flip(luke_sprites.subsurface((352,276,54,config.AVATAR_HEIGHT)),True,False))
        self.luke_swing_ls_left.append(pg.transform.flip(luke_sprites.subsurface((410,276,65,config.AVATAR_HEIGHT)),True,False))
        self.luke_swing_ls_left.append(pg.transform.flip(luke_sprites.subsurface((567,276,60,config.AVATAR_HEIGHT)),True,False))
        self.luke_swing_ls_left.append(pg.transform.flip(luke_sprites.subsurface((654,276,54,config.AVATAR_HEIGHT)),True,False))
        #self.luke_swing_ls_left.append(luke_sprites.subsurface((410,276,65,config.AVATAR_HEIGHT)))
        #self.luke_swing_ls_left.append(luke_sprites.subsurface((567,276,60,config.AVATAR_HEIGHT)))
        #self.luke_swing_ls_left.append(luke_sprites.subsurface((654,276,54,config.AVATAR_HEIGHT)))

        self.luke_stand_gun_right = luke_sprites.subsurface((6,276,34,config.AVATAR_HEIGHT))
        self.luke_stand_gun_left = pg.transform.flip(self.luke_stand_gun_right,True,False)

        self.luke_jump_gun_right = luke_sprites.subsurface((2,348,33,config.AVATAR_HEIGHT))
        self.luke_jump_gun_left = pg.transform.flip(self.luke_jump_gun_right,True,False)

        self.image = self.luke_stand_ls_right
        self.rect = self.image.get_rect(topleft=location,width=config.AVATAR_WIDTH,height=config.AVATAR_HEIGHT)
        self.speed = speed
        self.jump_power = -10.0
        self.jump_cut_magnitude = -3.0
        self.on_moving = False
        self.collide_below = False
        self.dead = False
        self.lastHit = "right"
        self.fire = False
        self.melee = True
        self.animation = False
        self.ani_cnt = 0

        self.x_vel = self.y_vel = 0
        self.grav = 0.4
        self.fall = False
        self.going_down = False

        self.ls_sprites = pg.image.load("images/luke_sprites0.png").convert()
        self.ls_sprites.set_colorkey(config.COLOR_KEY)
        self.ls_image = self.ls_sprites.subsurface((440,288,config.BS,7))
        

    def Fire_blaster(self,obstacles,player_blaster):
        if(self.fire and not self.melee):
            if(self.lastHit == "right"):
                self.blast = Blaster(pg.Color("blue"), (self.rect[0] + self.rect[2], self.rect[1] + 12, BS/2, 2),axis=0,speed=20,move_dist=BS*8,direction=1,kind="player_blast")

            if(self.lastHit == "left"):
                self.blast = Blaster(pg.Color("blue"), (self.rect[0] - 40, self.rect[1] + 12, BS/2, 2),axis=0,speed=15,move_dist=BS*8,direction=-1,kind="player_blast")
                #self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2], self.rect[1] + 12, BS, 2),axis=0,speed=20,move_dist=22,direction=-1)
            player_blaster.add(self.blast)
            self.fire = False

        if(self.fire and self.melee):
            if(self.lastHit == "right"):
                #self.blast = Blaster(pg.Color("red"), (self.rect[0] + self.rect[2], self.rect[1] + 12, BS/2, 2),axis=0,speed=20,move_dist=BS*1,direction=1,kind="player_blast")
                self.saber = Lightsaber(pg.Color("green"), (self.rect[0] + self.rect[2], self.rect[1] + 12, BS, 7), "player_blast", self.ls_image)

            if(self.lastHit == "left"):
                #self.blast = Blaster(pg.Color("red"), (self.rect[0] -30 , self.rect[1] + 12, BS/2, 2),axis=0,speed=15,move_dist=0,direction=-1,kind="player_blast")
                #self.blast = Blaster(pg.Color("red"), (self.rect[0] - 40, self.rect[1] + 12, BS/2, 2),axis=0,speed=15,move_dist=BS*1,direction=-1,kind="player_blast")
                self.saber = Lightsaber(pg.Color("green"), (self.rect[0] - self.rect[2] - 11, self.rect[1] + 12, BS, 7), "player_blast",self.ls_image)

            player_blaster.add(self.saber)
            #self.animation = True
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
        if (self.collide):
            self.check_death(self.collide)
        if self.collide and ((self.collide.type == "danger")or(self.collide.type == "storm_blast")):
            self.dead = True

        return self.collide

    # updates player
    #
    def update(self, obstacles, player_blaster, enemy_blaster, keys):
        if(pg.sprite.spritecollideany(self,enemy_blaster)):
            self.dead = True
        self.check_keys(keys)
        self.plat_collision(obstacles)
        self.get_position(obstacles)
        self.physics_update()
        self.Fire_blaster(obstacles, player_blaster)
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
        self.platform = pg.sprite.spritecollideany(self, obstacles)
        if(self.platform):
            if(self.platform.type == "platform"):
                while pg.sprite.spritecollideany(self, obstacles):
                    self.count += 1
                    self.rect[self.platform.axis] += self.platform.direction
                    if (self.platform.max_speed) < self.count:
                        self.dead = True

            self.check_death(self.platform)
            #if(self.type == "player"):
            #    if((self.platform.type == "danger")or(platform.type == "storm_blast")):
            #        self.dead = True

            #elif(self.type == "storm_trooper"):
            #    if((platform.type == "danger")or(platform.type == "player_blast")):
            #        self.dead = True

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
            self.check_death(self.obj)

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


        if self.animation == True and self.lastHit == "right":
            self.ani_cnt = self.ani_cnt + 1
            if self.ani_cnt <= 5:
                self.image = self.luke_swing_ls_right[0]

            elif self.ani_cnt <= 10:
                self.image = self.luke_swing_ls_right[1]

            elif self.ani_cnt <= 15:
                self.image = self.luke_swing_ls_right[2]

            elif self.ani_cnt <= 20:
                self.image = self.luke_swing_ls_right[3]

            elif self.ani_cnt > 20:
                self.animation = False
                self.ani_cnt = 0


        elif self.animation == True and self.lastHit == "left":
            self.ani_cnt = self.ani_cnt + 1
            if self.ani_cnt <= 5:
                self.image = self.luke_swing_ls_left[0]

            elif self.ani_cnt <= 10:
                self.image = self.luke_swing_ls_left[1]

            elif self.ani_cnt <= 15:
                self.image = self.luke_swing_ls_left[2]

            elif self.ani_cnt <= 20:
                self.image = self.luke_swing_ls_left[3]

            elif self.ani_cnt > 20:
                self.animation = False
                self.ani_cnt = 0

        else:
            if self.fall:
                if self.lastHit == "right":
                    self.image = self.luke_jump_gun_right
                elif self.lastHit == "left":
                    self.image = self.luke_jump_gun_left
            else:
                if self.lastHit == "right":
                    self.image = self.luke_stand_ls_right
                elif self.lastHit == "left":
                    self.image = self.luke_stand_ls_left


    def check_death(self,thing):
        #if(self.type == "player"):
        #    if ((thing.type == "danger")or(thing.type == "storm_blast")):
        #        self.dead = True

        #elif(self.type == "storm_trooper"):
        #    if ((thing.type == "danger")or(thing.type == "player_blast")):
        #        self.dead = True
        if ((thing.type == "danger")):
            self.dead = True
