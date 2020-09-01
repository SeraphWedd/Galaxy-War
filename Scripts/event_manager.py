'''
'''

import pygame as pg
from collections import OrderedDict


class EventManager(object):

    """
    Event Manager

    Main Class for handling the succession and quick processing of all events.
    Applied for generally all events that occur in the game's runtime.

    """

    def __init__(self):
        
        self.event_queue = OrderedDict()
        self.controller = {
            pg.K_UP:0, pg.K_DOWN:0, pg.K_LEFT:0, pg.K_RIGHT:0,
            pg.K_w:0, pg.K_s:0, pg.K_a:0, pg.K_d:0, pg.K_ESCAPE:0,
            pg.K_RETURN:0, pg.K_SPACE:0, pg.K_LSHIFT:0, pg.K_LCTRL:0,
            pg.K_LALT:0,pg.K_RSHIFT:0, pg.K_RCTRL:0, pg.K_RALT:0,
            pg.K_F1:0, pg.K_F2:0, pg.K_F3:0, pg.K_F4:0, pg.K_0:0, pg.K_1:0,
            pg.K_2:0, pg.K_3:0, pg.K_4:0, pg.K_5:0, pg.K_6:0, pg.K_7:0,
            pg.K_8:0, pg.K_9:0, pg.K_z:0, pg.K_x:0, pg.K_c:0, pg.K_q:0,
            pg.K_e:0, pg.K_b:0, pg.K_i:0, pg.K_k:0, pg.K_p:0, pg.K_t:0
        }
        self.mouse = [0, 0, 0] #Left, middle, right click
        self.pos = (0, 0)

    def loop_capture(self):
        """
        Event loop.
        Must be run on a different thread than the main thread.

        """
        #print('capture...')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.event_queue['quit'] = event
                
            elif event.type == pg.KEYDOWN:
                self.controller[event.key] = 1
                
            elif event.type == pg.KEYUP:
                self.controller[event.key] = 0
                
            elif event.type == pg.VIDEORESIZE:
                self.event_queue['resize'] = event
                
            elif event.type == pg.MOUSEMOTION:
                self.event_queue['motion'] = event

            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse = pg.mouse.get_pressed()

            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse = pg.mouse.get_pressed()

    def loop_process(self, ge):
        """
        Processing the captured event.
        Must be run on a different thread than the main thread.

        """
        #print('process...')
        try:
            for key in self.event_queue.keys():
                event = self.event_queue[key]
            
                if event.type == pg.QUIT:
                    response = ge.confirmation('quit')
                    if response:
                        ge.close()

                if event.type == pg.VIDEORESIZE:
                    ge.window_resize(event.dict['size'])

                if event.type == pg.MOUSEMOTION:
                    self.pos = pg.mouse.get_pos()
            self.event_queue.clear()
                
        except Exception as e:
            print(e)
