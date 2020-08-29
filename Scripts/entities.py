'''
'''

import pygame as pg


class Entity(pg.sprite.Sprite):

    """
    Entity

    The base class for handling the data for each individual entity present
    within the whole game runtime.

    """

    def __init__(self, ge):
        
        pg.sprite.Sprite.__init__(self)
        self.ge = ge
        self.pos = (0, 0)

    def set_pos(self, x, y, center=False):
        """
        Sets the position of the entity.

        """
        
        self.pos = (x, y)
        
        try:
            if center:
                self.rect.center = self.pos
                
            else:
                self.rect.topleft = self.pos
                
        except Exception as e:
            print(e)
            #If no rect enabled, create a temp rect
            self.rect = pg.rect.Rect(x, y, 32, 32)
            
            if center:
                self.rect.center = self.pos
                
            else:
                self.rect.topleft = self.pos

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
    

class StaticImage(Entity):

    def __init__(self, ge, fname):
        """
        Class for objects that is static and with one image.

        """
        
        #Initiate Entity
        Entity.__init__(self, ge)
        self.fname = fname

    def init_image_rect(self):
        image = self.ge.GM.get(self.fname)
        self.rect = image.get_rect()
        self.rect.topleft = self.pos
        del image

    def draw(self, screen):
        screen.blit(self.ge.GM.get(self.fname), self.rect)

    
class StaticAnimated(Entity):

    def __init__(self, ge, fnames, fps=5):
        """
        Class for objects that is static and with multiple/animated image.

        """
        
        Entity.__init__(self, ge)
        self.fnames = fnames
        self.max_i = len(fnames)
        self.cur_i = 0
        self.fps = fps

    def init_image_rect(self):
        image = self.ge.GM.get(self.fnames[0])
        self.rect = image.get_rect()
        del image

    def update(self, dt):
        """
        Updates the number of current frame based on elapsed time.

        """
        
        self.cur_i = (self.cur_i + self.fps*dt) % self.max_i

    def draw(self, screen):
        screen.blit(self.ge.GM.get(self.fnames[int(self.cur_i)]), self.rect)


class DynamicImage(StaticImage):

    def __init__(self, ge, fname):
        """
        Class for moving objects that have a single image.

        """
        
        StaticImage.__init__(self, ge, fname)


    def move_behavior(self):
        """
        Movement pattern of the entity.

        """
        
        pass

    
    def update(self, dt):
        """
        Moves the image based on the imprinted behavior.

        """
        
        self.move_behavior()


class DynamicAnimation(StaticAnimated):

    def __init__(self, ge, fnames, fps=5):
        """
        Class for moving objects that have multiple/animated image.

        """

        StaticAnimated.__init__(self, ge, fnames, fps)


    def move_behavior(self):
        """
        Movement pattern of the entity.

        """
        
        pass


    def update(self, dt):
        """
        Performs all per frame updates for the entity.

        """
        
        self.cur_i = (self.cur_i + self.fps*dt) % self.max_i
        self.move_behavior()


class Button(StaticImage):

    def __init__(self, ge, fname):
        """
        Base class for click-able objects.

        """
        
        StaticImage.__init__(self, ge, fname)
        self.hover = False
        self.clicked = False

    def check_clicked(self, pos):
        """
        Checks whether the button is clicked.

        """
        
        self.check_hover(pos)

        if self.hover:
            self.clicked = True
        else:
            self.clicked = False

    def is_clicked(self):
        """
        Returns True if the button is clicked. Else, False.

        """
        
        return self.clicked

    def check_hover(self, pos):
        """
        Checks whether the pointer is hovering over the button.

        """
        
        x, y, w, h = self.rect
        a, b = pos

        if (x <= a <= x+w) and (y <= b <= y+h):
            self.hover =  True
        else:
            self.hover = False
            self.clicked = False

    def draw(self, screen):
        if self.hover:
            screen.blit(self.ge.GM.get('hover_'+self.fname), self.rect)
        else:
            screen.blit(self.ge.GM.get(self.fname), self.rect)

