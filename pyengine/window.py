"""
Contains game window configuration & reconfiguration methods
"""
# pylint: disable=E1101
# pylint: disable=R0903
# pylint: disable=W0511
###### Python Packages ######
import time
import pygame

###### My Packages ######

#### Type Hinting ####


class Resolution:
    """Defines helper class that contains resolution configuration"""

    def __init__(self, size: list, grid_precision_level: int) -> None:
        """
        Init a new resolution object

        Arguments:
            size: list contains window size [width, height]
            grid_precision_level: the level of precision in grid system
        """
        self.screen_width = 1
        self.screen_height = 1
        self.width_ratio = 1.0
        self.height_ratio = 1.0
        self.x_ceil = 1
        self.y_ceil = 1

        self.set_window_size(size)
        self.set_ratio()
        self.set_grid_ceils(grid_precision_level)

    def set_window_size(self, size: list) -> None:
        """
        Sets the game window size according to size parameter

        if the size parameter is <= 0 the size will = monitor size

        Arguments:
            size: list contains window size [width, height]
        """
        screen_info = pygame.display.Info()
        monitor_width = screen_info.current_w
        monitor_height = screen_info.current_h

        if size[0] <= 0 or size[1] <= 0:
            self.screen_width = monitor_width
            self.screen_height = monitor_height
        else:
            self.screen_width = size[0]
            self.screen_height = size[1]

    def set_ratio(self) -> None:
        """
        Set the window ration according to 1920x1080 and the current screen size
        to use it with images

        ! this is a fixed ration so a screen size with different aspect than 16:9 will not work
        """
        # TODO: try to fix the above problem to make the ratio calc handle different screen ratios
        self.width_ratio = self.screen_width / 1920
        self.height_ratio = self.screen_height / 1080

    def set_grid_ceils(self, grid_precision_level: int) -> None:
        """
        Sets the grid lines according to precision level

        Arguments:
            grid_precision_level: the level of precision in grid system

        ! for now the grid system only works with 16:9 monitors
        """
        # TODO: try to fix the above problem to make the grid works with different aspect ratio
        self.x_ceil = grid_precision_level * 9
        self.y_ceil = grid_precision_level * 16


class FrameRate:
    """Defines helper class that contains framerate configuration"""

    # TODO: add a way to change game fps during the run time

    def __init__(self, fps: int) -> None:
        """
        Init a new clock object

        Arguments:
            fps: game framerate
        """
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.delta_time = 1.0
        self.previous_time = time.time()

    def set_delta(self) -> None:
        """
        Sets the game delta-time in each game cycle
        """
        self.delta_time = time.time() - self.previous_time
        self.previous_time = time.time()


class Window(Resolution, FrameRate):
    """Main window class that contains all the configuration"""

    # TODO: add option to window data that sets the game to full screen

    def __init__(self, window_data: dict) -> None:
        """
        Init a new window object

        Arguments:
            window_data: dict contains window data {window_size, grid_precision_level, ...}
        """

        window_size = window_data.get("window_size")
        grid_precision_level = window_data.get("grid_precision_level")
        fps = window_data.get("fps")
        window_title = window_data.get("window_title")

        Resolution.__init__(self, window_size, grid_precision_level)
        FrameRate.__init__(self, fps)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(window_title)
