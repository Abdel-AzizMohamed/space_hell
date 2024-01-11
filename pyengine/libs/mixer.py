"""Define game Sound handler"""
#### Python Packages ####
import pygame

#### My Packages ####


class Sound:
    """Define game sound effect class"""

    sounds = {}

    @staticmethod
    def load_sounds(sounds: dict) -> None:
        """
        Load all sounds from config file

        Arguments:
            sounds: dict contains sounds {sound_path, sound_volume}
        """

        for name, data in sounds.items():
            sound = pygame.mixer.Sound(data.get("sound_path"))
            sound.set_volume(data.get("sound_volume"))
            Sound.sounds[name] = sound

    @staticmethod
    def play_sound(sound_name: str) -> None:
        """
        Play the given sound

        Arguments:
            sound_name: wanted sound name that are stored in sounds dict
        """
        sound = Sound.sounds.get(sound_name)
        sound.play()


class Music:
    """Define game sound effect class"""

    music = {}

    @staticmethod
    def load_music(music: dict) -> None:
        """
        Load all music from config file

        Arguments:
            music: dict contains sounds {music_path, music_volume}
        """

        for name, data in music.items():
            Music.music[name] = data

    @staticmethod
    def play_music(music_name: str) -> None:
        """
        Play the given music

        Arguments:
            music_name: wanted music name that are stored in music dict
        """
        music_data = Music.music.get(music_name)
        music_path = music_data.get("music_path")
        music_volume = music_data.get("music_volume")

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
