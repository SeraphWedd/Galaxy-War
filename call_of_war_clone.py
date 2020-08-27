import pygame as pg
import threading
import math
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

from collections import OrderedDict

class AudioManager(object):
    
    """
    Audio Manager

    Main class for handling all audio/sound related events on the game.
    Mainly applied for loading/unloading of audio, audio playback and others.

    """

    def __init__(self):
        
        pg.mixer.quit() #Stop mixer once before reinitializing
        
        pg.mixer.init(
            frequency=44100,
            size=-16,
            channels=4,
            buffer=2048
        )
        
        self.num_channels = 10
        pg.mixer.set_num_channels(self.num_channels)
        self.audio_channels = [
            pg.mixer.Channel(i) for i in range(self.num_channels)
        ] #Channel 1:BGM, Channel 2: Ambient, Channel 3-n: Misc.
        
        self.persistent = {}
        self.current = {}
        self.fonts = {}
        
        self.default = 'Resources/Audio/default.ogg'
        self.path = 'Resources/Audio/'

    def load_sound(self, fname, volume=1.0, persist=False):
        """
        Loads Sound Effects for quick playback.

        """
        
        try:
            audio = pg.mixer.Sound(self.path+fname)
            audio.set_volume(volume)
            
        except Exception as e:
            print(e)
            print(f'ERROR on loading Sound object file {fname}.')
            audio = pg.mixer.Sound(self.default)
            audio.set_volume(volume)

        if persist:
            self.persistent[fname] = audio
            
        else:
            self.current[fname] = audio

    def load_music(self, fname, volume=1.0, persist=False):
        """
        Loads Music for background, ambient noise, etc.

        """
        
        try:
            audio = pg.mixer.Sound(self.path+fname)
            audio.set_volume(volume)
            
        except Exception as e:
            print(e)
            print(f'ERROR on loading Music audio file {fname}.')
            audio = pg.mixer.Sound(self.default)
            audio.set_volume(volume)

        if persist:
            self.persistent[fname] = audio
            
        else:
            self.current[fname] = audio
            
    def unload(self, fname=None):
        """
        Unloads audio from memory. If fname is None, clear self.current.

        """
        
        if fname:
            self.current[fname] = None
        else:
            self.current = {}


    def play_sound(self, fname, loops=0, maxtime=0, fade_ms=0):
        """
        Plays the sound from memory.
        Assumes that sound is already loaded to memory.
        
        """
        
        no_channel = True
        for i in range(2, self.num_channels):
            if self.audio_channels[i].get_busy():
                pass
            else:
                no_channel = False
                break
            
        if no_channel: #If no vacant, override oldest playback
            try:
                pg.mixer.find_channel(True).play(
                    self.persistent[fname],
                    maxtime,
                    fade_ms
                )
                    
            except KeyError:
                pg.mixer.find_channel(True).play(
                    self.current[fname],
                    maxtime,
                    fade_ms
                )
                
        else:
            try:
                self.audio_channels[i].play(
                    self.persistent[fname],
                    maxtime,
                    fade_ms
                )
                
            except KeyError:
                self.audio_channels[i].play(
                    self.current[fname],
                    maxtime,
                    fade_ms
                )

    def play_music(self, fname, loops=-1, maxtime=0, fade_ms=0):
        """
        Plays the music from memory.
        Assumes that music is already loaded to memory.
        
        """
        
        if fname.startswith('bgm'):
            i = 0
            
        else:
            i = 1
            
        try:
            self.audio_channels[i].play(
                self.persistent[fname],
                maxtime,
                fade_ms
            )
            
        except KeyError:
            self.audio_channels[i].play(
                self.current[fname],
                maxtime,
                fade_ms
            )
        
    def stop(self, fname):
        """
        Stops the playback of sound/music.

        """
        
        try:
            sound = self.persistent[fname]
            
        except KeyError:
            sound = self.current[fname]

        for i in range(self.num_channels):
            if self.audio_channels[i].get_sound() == sound:
                self.audio_channels[i].fadeout(500)
                break


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
                event = self.event_queue.pop(key)
            
                if event.type == pg.QUIT:
                    response = ge.confirmation('quit')
                    if response:
                        ge.close()

                if event.type == pg.VIDEORESIZE:
                    ge.window_resize(event.dict['size'])

                if event.type == pg.MOUSEMOTION:
                    self.pos = pg.mouse.get_pos()
                
        except Exception as e:
            print(e)


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
DynamicImage.set_pos
