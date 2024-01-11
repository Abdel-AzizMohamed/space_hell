"""Contains pygame init & window init"""
# pylint: disable=E1101
###### Python Packages ######
import os
import pygame

###### My Packages ######
from pyengine.window import Window

from pyengine.utils.json_handler import read_json
from pyengine.utils.path_handler import alternate_path

#### Type Hinting ####

#### Pygame Init ####
pygame.init()
pygame.mixer.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
# os.environ["SDL_VIDEO_WINDOW_POS"] = "1000,500"

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "default_config.json")
CONFIG_PATH = alternate_path("config.json", DEFAULT_CONFIG_PATH)
CONFIG_DATA = read_json(CONFIG_PATH)

win_obj = Window(CONFIG_DATA.get("window_data"))
alpha_surface = pygame.Surface(
    (win_obj.screen_width, win_obj.screen_height), pygame.SRCALPHA
)
