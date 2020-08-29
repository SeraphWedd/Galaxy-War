'''
'''

import pygame as pg


class PhysicsManager(object):

    """
    Physics Manager

    Main class for handling all physics related events on the game.
    Mainly applied for gravity, collision, movement and others.

    """

    def __init__(self):

        self.fps = 60
        self.timer = pg.time.Clock()
        
        self.entity_group = pg.sprite.Group()
        self.running_threads = []
    
    def update(self, alpha=1.0):
        """
        Updates all entities. Alpha as time dilation.

        """
        
        dt = self.timer.get_time() * alpha
        
        for entity in self.entity_group:
            thread = threading.Thread(
                target=entity.update,
                args=dt
            )
            self.running_threads.append(thread)

        for thread in self.running_threads:
            thread.start()
