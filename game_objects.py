'''
Objects specific to one game.

Codes can be modified and recycled for another game.

'''

import pygame as pg

from Scripts.entities import *


class LoadingImage(pg.sprite.Sprite):

    def __init__(self, ge, pos, rad_angle=0, rps=0.5):
        pg.sprite.Sprite.__init__(self)
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

        
class Resources(object):

    def __init__(self, name, cur=500, mx=1000, pps=10, cps=0):
        """
        Base Resource class.
        Resources(name, current_amt, max_amount, production per sec,
                  consumption per sec)
                  
        """
        
        self.name = name
        
        self.cur_amt = cur
        self.max_amt = mx
        
        self.prod_per_sec = pps
        self.cons_per_sec = cps

    def update(self, dt):
        self.cur_amt = min(self.max_amt, self.cur_amt + dt* (
            self.prod_per_sec - self.cons_per_sec))


class Research(object):

    def __init__(self):
        self.weapon = 0
        self.defense = 0
        self.travel = 0
        self.power = 0
        self.storage = 0

        self.levels = [
            1, #Base Level
            1.1, 1.2, 1.3, 1.4, 1.5, #Rank 1 research
            1.6, 1.8, 2.0, 2.2, 2.5, #Rank 2 research
            3.0, 3.5, 4.0, 4.5, 5.0, #Rank 3 Research
            6.0, 7.0, 8.0, 9.0, 10.0 #Final Rank Research
            ]
        

    def get_research(self):
        return {
            'weapon':self.levels[self.weapon],
            'defense':self.levels[self.defense],
            'travel':self.levels[self.travel],
            'power':self.levels[self.power],
            'storage':self.levels[self.storage],
            }


class Ship(object):

    def __init__(self, name, atk, dur, dfn, spd, cap, nrg, rank=0):
        """
        Base Ship class.
        Ship(name, attack, durability, defense, speed,
             capacity, energy level, rank)
        
        """
        self.name = name
        self.attack = atk
        self.durability = dur
        self.defense = dfn
        self.speed = spd
        self.capacity = cap
        self.power = nrg
        self.rank = 0

        self.rank_multiplier = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 2.0]
        self.total_damage = 0

    def get_attack(self):
        return self.rank_multiplier[self.rank] * self.attack

    def get_defense(self):
        return self.rank_multiplier[self.rank] * self.defense

    def apply_research_bonus(self, research):
        for key in research.keys():
            if key == 'weapon':
                self.attack *= research[key]
            elif key == 'defense':
                self.defense *= research[key]
            elif key == 'travel':
                self.speed *= research[key]
            elif key == 'power':
                self.power *= research[key]
            elif key == 'storage':
                self.capacity *= research[key]

    def compute_dmg_output(self, enemy):
        """
        Computes actual battle damage to enemy ship.
        
        """
        
        damage = min(enemy.durability, (
            self.get_attack() - enemy.get_defense()
            ) * self.rank_multiplier[max(0, self.rank-enemy.rank)]
                     )
        self.total_damage += damage
        
        return damage
