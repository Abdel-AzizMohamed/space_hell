"""Contains main menu events"""
# pylint: disable=E1101
###### Python Packages ######
import sys
import pygame

###### My Packages ######
from pyengine.libs.designer.designer import Designer
from pyengine.libs.transition.transition import Transition

#### Type Hinting ####
from pyengine.libs.designer.py_elements import PyRect


def exit_game(_):
    """Exit the game :)"""
    pygame.quit()
    sys.exit()


def background_repeat(background: PyRect):
    """Move the background to the top of the screen"""
    if Transition.elements.get(background.group).get(background.name).start_y != -768:
        Transition.elements.get(background.group).get(background.name).start_y = -768
        Transition.elements.get(background.group).get(background.name).duration *= 2


def toggle_shop(_):
    """toggle shop menu"""
    Designer.toggle_exclude("shop_menu")
