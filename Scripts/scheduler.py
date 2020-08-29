'''
'''

import pygame as pg
from collections import OrderedDict


class Scheduler(object):

    """
    Scheduler

    Main class for handling of scheduling of tasks.
    Mainly for parallel reading and loading of resources to memory.

    """

    def __init__(self):
        self.load_queue = OrderedDict()
        self.max_counter = 0
        self.cur_counter = 0

    def add_to_queue(self, item):
        """
        Add item to loading queue.
        format of [<type> <fname> <args...>]

        """
        
        self.load_queue[self.max_counter] = item
        self.max_counter += 1

    def get_done(self):
        """
        Returns percentage of loading done as float.

        """
        
        try:
            return self.cur_counter / self.max_counter
        
        except ZeroDivisionError:
            return 1.0

    def loop(self, ge):
        """
        Loading loop.
        Must be run in a different thread than main thread.

        """
        
        while self.cur_counter < self.max_counter:
            try:
                for key in self.load_queue.keys():
                    msg = self.load_queue[key]

                    if msg[0] == 'image':
                        ge.GM.load(msg[1], msg[2])
                        
                    elif msg[0] == 'font':
                        ge.GM.load_font(msg[1], msg[2])
                        
                    elif msg[0] == 'sound':
                        ge.AM.load_sound(msg[1], msg[2], msg[3])
                        
                    elif msg[0] == 'music':
                        ge.AM.load_music(msg[1]. msg[2], msg[3])

                    self.cur_counter += 1
                    
                self.load_queue.clear()
                
            except Exception as e:
                print(e)
                
        self.cur_counter, self.max_counter = 0, 0
