import pygame as pg
import threading
import math
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

from Scripts.audio_manager import AudioManager
from Scripts.graphics_manager import GraphicsManager
from Scripts.physics_manager import PhysicsManager
from Scripts.event_manager import EventManager
from Scripts.scheduler import Scheduler
from Scripts.entities import *
from game_objects import *


class GameEngine(object):
    
    def __init__(self):
        
        pg.init()
        
        self.size = (800, 600)
        self.window_resize(self.size)
        
        self.AM = AudioManager()
        self.GM = GraphicsManager()
        self.PM = PhysicsManager()
        self.EM = EventManager()
        self.SC = Scheduler()

        self.running = True

    def confirmation(self, msg):
        return True

    def close(self):
        print('closing...')
        #self.AM.load_sound('default.mp3')
        pg.quit()
        sys.exit()

    def window_resize(self, size):
        self.size = (max(800, size[0]), max(600, size[1]))
        self.screen = pg.display.set_mode(
            self.size,
            pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE
        )

    def run(self):
        import time
        loader = LoadingImage(self, (pg.Vector2(.9, .9)))

        #Test for loader
        for i in range(20):
            self.SC.add_to_queue(['sound', str(i)+'default.ogg', 1.0, False])

        load_thread = threading.Thread(
            target=self.SC.loop, args=[self,]
        )
        load_thread.start()
        #End of test for loader
        
        s, e = time.time(), time.time()
        while self.running:
            
            self.EM.loop_capture()
            self.EM.loop_process(self)

            if any(self.EM.controller.values()):
                self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((0, 0, 255))

            loader.update(e-s)
            pg.display.set_caption(f'{self.SC.get_done()*100}')
            
            loader.draw(self.screen)
            pg.display.flip()
            s, e = e, time.time()


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


if __name__ == "__main__":
    GE = GameEngine()
    GE.run()
    pg.quit()

