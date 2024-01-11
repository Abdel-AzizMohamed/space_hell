"""Define a debugging tools module"""
###### Python Packages ######
import pygame

###### My Packages ######
from pyengine import win_obj
from pyengine.libs.designer.py_attributes import Text
from pyengine.libs.designer.designer import Designer

from pyengine.utils.alignment_handler import align_offset


class Debugger:
    """Define debugging tools"""

    @staticmethod
    def display_grid(grid_data: dict) -> None:
        """Display game gird according to x_ceil, y_ceil in window object"""
        grid_color = grid_data.get("grid_color")

        for row in range(win_obj.x_ceil):
            offset = row * (win_obj.screen_height / win_obj.x_ceil)
            pygame.draw.aaline(
                win_obj.screen,
                grid_color,
                (0, offset),
                (win_obj.screen_width, offset),
            )

        for column in range(win_obj.y_ceil):
            offset = column * (win_obj.screen_width / win_obj.y_ceil)
            pygame.draw.aaline(
                win_obj.screen,
                grid_color,
                (offset, 0),
                (offset, win_obj.screen_height),
            )

    @staticmethod
    def display_fps(fps_data: dict) -> None:
        """Display game current fps"""
        fps_font = fps_data.get("fps_font")
        fps_antialias = fps_data.get("fps_antialias")
        fps_color = fps_data.get("fps_color")
        fps_align = fps_data.get("fps_align")

        fps_text = str(round(win_obj.clock.get_fps()))
        render_font = Text.fonts[fps_font].render(fps_text, fps_antialias, fps_color)

        x_offset = 50 if fps_align in ("topleft", "midleft", "bottomleft") else -50
        y_offset = -50 if fps_align in ("topleft", "midleft", "bottomleft") else 50

        x_pos, y_pos = align_offset(
            render_font.get_rect().size,
            (win_obj.screen_width, win_obj.screen_height),
            fps_align,
        )

        win_obj.screen.blit(render_font, (x_pos + x_offset, y_pos + y_offset))

    @staticmethod
    def display_object_rect(object_rect_data: dict) -> None:
        """Display all game objects rect"""
        object_rect_color = object_rect_data.get("object_rect_color")
        object_rect_size = object_rect_data.get("object_rect_size")

        elements = [
            item for group in Designer.game_elements.values() for item in group.values()
        ]

        for element in elements:
            pygame.draw.rect(
                win_obj.screen,
                object_rect_color,
                element.rect,
                object_rect_size,
            )
