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
        
        loading = self.GM.get('loading.png')
        i = 0
        pos = pg.Vector2(self.size) - pg.Vector2(100, 100)
        self.GM.rotate('loading.png', 0, False, 'l1')
        loader = DynamicImage(self, 'l1')
        loader.set_pos(*pos, True)
        
        for i in range(20):
            self.SC.add_to_queue(['sound', str(i)+'default.ogg', 1.0, False])

        load_thread = threading.Thread(
            target=self.SC.loop, args=[self,]
        )
        load_thread.start()
        while self.running:
            
            self.EM.loop_capture()
            self.EM.loop_process(self)

            if any(self.EM.controller.values()):
                self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((0, 0, 255))

            i -= .3
            self.GM.rotate('loading.png', i, False, 'l1')
            loader.init_image_rect()
            loader.set_pos(*pos, True)
            pg.display.set_caption(f'{self.SC.get_done()*100}')
            
            loader.draw(self.screen)
            pg.display.flip()

if __name__ == "__main__":
    GE = GameEngine()
    GE.run()
    pg.quit()

