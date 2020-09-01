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
        grid = GridBackground(self)

        #Test for loader
        for i in range(20):
            self.SC.add_to_queue(['sound', str(i)+'default.ogg', 1.0, False])

        load_thread = threading.Thread(
            target=self.SC.loop, args=[self,]
        )
        load_thread.start()
        #End of test for loader
        
        self.PM.add_entity(loader)
        self.PM.add_entity(grid)
        
        while self.running:
            
            self.EM.loop_capture()
            self.EM.loop_process(self)

            self.PM.update()

            if any(self.EM.controller.values()):
                self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((0, 0, 255))
                
            #loader.update(self.PM.dt)
            pg.display.set_caption(
                f'{self.SC.get_done()*100}% fps={self.PM.timer.get_fps()}'
            )
            
            grid.draw(self.screen)
            #loader.draw(self.screen)
            
            pg.display.flip()


if __name__ == "__main__":
    GE = GameEngine()
    GE.run()

