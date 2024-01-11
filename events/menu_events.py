"""Contains main menu events"""
# pylint: disable=E1101
###### Python Packages ######
import sys
import pygame

###### My Packages ######

#### Type Hinting ####


def exit_game(_):
    """Exit the game :)"""
    pygame.quit()
    sys.exit()
