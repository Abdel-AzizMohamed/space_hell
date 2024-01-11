"""
Contains main functions to work with time in pygame
"""
# pylint: disable=E1101
###### Python Packages ######
from typing import Union
import pygame

###### My Packages ######

#### Type Hinting ####


class Timer:
    """Timer class that works as a basic timer"""

    def __init__(self, duration: int) -> None:
        """
        Init a new timer object

        Arguments:
            duration: timer duration in milliseconds
        """
        self._start_time = 0
        self._current_time = 0
        self._timer_active = False
        self._duration = duration

    def start_timer(self) -> None:
        """Start the timer"""
        self._current_time = pygame.time.get_ticks()
        self._start_time = self._duration + self._current_time
        self._timer_active = True

    def check_timer(self) -> Union[bool, None]:
        """Checks if the timer is done"""
        if not self._timer_active:
            return None
        if self._start_time - self._current_time < 0:
            self._timer_active = False
            return True

        self._current_time = pygame.time.get_ticks()
        return False

    def get_passed_time(self) -> int:
        """Returns remaining time"""
        return self._start_time - self._current_time
