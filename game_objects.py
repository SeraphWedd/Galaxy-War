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


class GridBackground(pg.sprite.Sprite):

    def __init__(self, ge):
        pg.sprite.Sprite.__init__(self)
        self.GE = ge
        self.angle = 0
        self.timer = 0
        self.bg_rect = self.GE.GM.get('grid_bg.png').get_rect()
        self.bg_rect.center = pg.Vector2(self.GE.size)/2
        self.color = (0, 150, 20)
        self.vkey = 0
        self.hkey = 0

    '''
    
    #Commented out
    #Code for recreating images for the grid
    
        self.create_backdrop()
        self.draw_backdrop()
    
    def create_backdrop(self):
        w, h = self.GE.size
        self.screen_0 = pg.surface.Surface((w, h)).convert_alpha()
        self.screen_0.fill((0, 0, 0, 0))
        self.screen_1 = pg.surface.Surface((w, h)).convert_alpha()
        self.screen_1.fill((0, 0, 0, 0))
        self.screen_2 = pg.surface.Surface((w, int(h*0.5))).convert_alpha()
        self.screen_2.fill((0, 0, 0, 0))
        self.screen_3 = pg.surface.Surface((2*w, 2*w)).convert_alpha()
        self.screen_3.fill((0, 0, 0, 255))
        self.bg_rect = self.screen_3.get_rect()

        from random import randint as ri
        for i in range(200):
            x = ri(0, 2*w)
            y = ri(0, 2*w)
            r = ri(1, 3)
            pg.draw.circle(self.screen_3, (255, 255, 255, 155), (x, y), r)
        pg.image.save(self.screen_3, 'Resources/Images/grid_bg.png')
            

    def draw_backdrop(self):
        w, h = self.GE.size
        start = pg.Vector2(int(w/2), int(h/2)-10)
        end = pg.Vector2(2*w, int(h/2)-10)
        diff = end - start

        for i in range(6):
            self.screen_0.fill((0, 0, 0, 0))
            self.screen_2.fill((0, 0, 0, 0))
            for angle in range(0, 360, 6):
                x, y = diff.rotate(i+angle) + start
                pg.draw.line(self.screen_0, self.color, start, (x, y), 1)
                pg.draw.aaline(self.screen_0, self.color, start, (x, y), 1)
            
            self.screen_2.blit(self.screen_0, (0, -h//2))
            pg.draw.line(self.screen_2, self.color, (0, 0), (w, 0), 2)
            pg.draw.aaline(self.screen_2, self.color, (0, 0), (w, 0), 2)
            pg.image.save(self.screen_2, f'Resources/Images/{i}gridv.png')

        
        for i in range(1, 7):
            self.screen_0.fill((0, 0, 0, 0))
            self.screen_1.fill((0, 0, 0, 0))
            dr = i/6
            dy = 1
            c = 0
            ay = h//2
            while dy*dr + ay < h:
                pg.draw.line(self.screen_0, self.color,
                             (0, ay+dy*dr), (w, ay+dy*dr), 1)
                pg.draw.aaline(self.screen_0, self.color,
                               (0, ay+dy*dr), (w, ay+dy*dr), 1)
                ay += dy
                c += 1
                dy = 1.5**c
            self.screen_1.blit(self.screen_0, (0, 0))
            pg.draw.line(self.screen_2, self.color, (0, h//2), (w, h//2), 2)
            pg.draw.aaline(self.screen_1, self.color, (0, h//2), (w, h//2), 2)
            pg.image.save(self.screen_1, f'Resources/Images/{i-1}gridh.png')
            
                
        self.screen_1.fill((0, 0, 0))
        self.screen_1.blit(self.screen_3, (0, 0))
        self.screen_2.blit(self.screen_0, (0, -h//2))
        self.screen_1.blit(self.screen_2, (0, h//2))
    '''

    def update(self, dt):
        if int(10*self.angle) != int(10*self.angle + dt):
            self.angle = (self.angle + dt/10)%360
            self.GE.GM.rotate('grid_bg.png', self.angle, False, 'rotated_bg')
            self.bg_rect = self.GE.GM.get('rotated_bg').get_rect()
            self.bg_rect.center = pg.Vector2(self.GE.size)/2
        else:
            self.angle = (self.angle + dt/10)%360

        speed = 24 * dt
        if self.GE.EM.controller[pg.K_UP]:
            self.hkey = (self.hkey + speed)%6

        elif self.GE.EM.controller[pg.K_DOWN]:
            self.hkey = (self.hkey - speed)%6

        if self.GE.EM.controller[pg.K_LEFT]:
            self.vkey = (self.vkey + speed)%6

        elif self.GE.EM.controller[pg.K_RIGHT]:
            self.vkey = (self.vkey - speed)%6

    def draw(self, screen):
        screen.blit(self.GE.GM.get('rotated_bg'),
                                   self.bg_rect)
        screen.blit(self.GE.GM.get(f'{int(self.vkey)}gridv.png'),
                                   (0, self.GE.size[1]//2))
        screen.blit(self.GE.GM.get(f'{int(self.hkey)}gridh.png'),
                                   (0, 0))


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
