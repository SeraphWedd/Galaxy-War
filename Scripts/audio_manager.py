'''
'''
import pygame as pg

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
