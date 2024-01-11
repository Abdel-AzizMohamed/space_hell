"""Define a collision module"""
###### Python Packages ######
import pygame
from pygame.mouse import get_pos as mouse_pos

###### My Packages ######

#### Type Hinting ####


def mouse_collision(rect: pygame.Rect) -> bool:
    """
    Check if the given rect collision with mouse cursor

    Arguments:
        rect: rect to check collision with mouse cursor
    """
    if rect.collidepoint(mouse_pos()):
        return True
    return False


def object_collision(first_object: pygame.Rect, other_object: pygame.Rect) -> bool:
    """
    Check if the given rect collision another rect

    Arguments:
        first_object: first object to check collision
        other_object: other object to check collision with first
    """
    return first_object.colliderect(other_object)
