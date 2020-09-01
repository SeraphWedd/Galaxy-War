'''
Objects specific to one game.

Codes can be modified and recycled for another game.

'''

import pygame as pg

from Scripts.entities import *


class LoadingImage(object):

    def __init__(self, ge, pos, rad_angle=0, rps=0.5):

        self.GE = ge
        self.pos = pos
        self.angle = rad_angle
        self.rps = rps
        self.fname = 'loading.png'
        self.object = DynamicImage(self.GE, 'loading_rot_image')        
        self.update()

    def update(self, dt=0):
        self.angle = (self.angle+self.rps*360*dt)%360
        self.GE.GM.rotate(self.fname, self.angle, False, 'loading_rot_image')
        self.object.init_image_rect()
        r1, r2 = self.pos
        x, y = self.GE.size
        self.object.set_pos(int(x*r1), int(y*r2), True)
    
    def draw(self, screen):
        self.object.draw(screen)
        
