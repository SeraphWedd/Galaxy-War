'''
'''

import pygame as pg


class GraphicsManager(object):

    """
    Graphics Manager

    Main class for handling all graphics related events on the game.
    Mainly applied for loading/unloading of images and animation.

    """

    def __init__(self):
        
        self.persistent = {}
        self.current = {}
        self.fonts = {}
        self.default = 'Resources/Images/default.png'
        self.path = 'Resources/Images/'
        self.font_path = 'Resources/Fonts/'


    def load(self, fname, persist=False):
        """
        Loading images for quick usage.

        """
        
        try:
            image = pg.image.load(self.path + fname).convert_alpha()
            
        except Exception as e:
            print(e)
            print(f'ERROR on Loading Image file {fname}')
            image = pg.image.load(self.default).convert_alpha()
            
        if persist:
            self.persistent[fname] = image
            
        else:
            self.current[fname] = image

    def unload(self, fname=None):
        """
        Unloads image from memory. If fname is None, clear self.current.

        """
        
        if fname:
            self.current[fname] = None
            
        else:
            self.current = {}

    def get(self, fname, persist=False):
        """
        Gets the image from memory. If not loaded, reads from disk.

        """
        
        try:
            if persist:
                return self.persistent[fname]
            else:
                return self.current[fname]
        
        except KeyError:
            self.load(fname, persist)
            return self.get(fname, persist)

    def resize(self, fname, width, height, overwrite=False, nname=None):
        """
        Resizes the image and overwrites value or creates a new key.

        """
        
        try:
            image = self.current[fname]
            
        except KeyError:
            self.load(fname)
            image = self.current[fname]

        if overwrite:
            self.current[fname] = pg.transform.scale(image, (width, height))
            
        else:
            self.current[nname] = pg.transform.scale(image, (width, height))

    def rotate(self, fname, angle, overwrite=False, nname=None):
        """
        Rotates the image and overwrites value or creates a new key.

        """
        
        try:
            image = self.current[fname]
            
        except KeyError:
            self.load(fname)
            image = self.current[fname]

        if overwrite:
            self.current[fname] = pg.transform.rotate(image, angle)
            
        else:
            self.current[nname] = pg.transform.rotate(image, angle)

    def crop(self, fname, x, y, width, height, code, persist=False):
        """
        Crops the image file <fname> and stores it to memory key <code>.

        """
        
        image = pygame.Surface((width, height)).convert_alpha()
        source = self.get(fname, persist)
        image.blit(source, (0, 0), (x, y, width, height))

        self.current[code] = image

    def load_font(self, name, size):
        """
        Loads a font to memory for quick rendering.

        """
        
        try:
            self.fonts[
                '@'.join([name, str(size)])] = pg.font.Font(
                    self.font_path + name, size
                )
            
        except Exception as e:
            print(e)
            print(f'Error on loading font file {name}')
            print('Fix: Loaded system font as placeholder.')
            self.fonts[
                '@'.join([name, str(size)])] = pg.font.SysFont(
                    'Arial', size
                )

    def font_render(self, name, size, text, color, antialias=False):
        """
        Renders a text using the provided font style and size.

        """
        
        fname = '@'.join([name, str(size)])
        
        try:
            font = self.fonts[fname]
            
        except KeyError:
            self.load_font(name, size)
            font = self.fonts[fname]
            
        self.current[fname+text] = font.render(text, antialias, color)

    def font_unload(self, fname=None):
        """
        Removes font from memory. If fname is None, clear self.fonts.

        """
        
        if fname:
            
            try:
                self.fonts[fname] = None
                
            except Exception as e:
                print(e)
                
        else:
            self.fonts = {}
