"""Contains elements attributes"""
# pylint: disable=R0903
# pylint: disable=R0902
# pylint: disable=R0913
###### Python Packages ######
import pygame

###### My Packages ######
from pyengine import win_obj

from pyengine.utils.alignment_handler import align_offset

#### Type Hinting ####


class Rectangle:
    """Define a pygame Rectangle"""

    def __init__(self, rect_data: dict) -> None:
        """
        Init new pygame rect object

        Arguments:
            rect_data: dict contains rect data {x_pos, y_pos, x_size, y_size}
        """
        self.rect = Rectangle.create_rect(rect_data)

    @staticmethod
    def create_rect(rect_data: dict) -> pygame.Rect:
        """
        Creates a new pygame rect object from dict

        Arguments:
            rect_data: dict contains rect data {x_pos, y_pos, x_size, y_size}
        """

        anchor_point = rect_data.get("anchor_point")

        x_pos = rect_data.get("x_pos")
        y_pos = rect_data.get("y_pos")
        x_offset = rect_data.get("x_offset")
        y_offset = rect_data.get("y_offset")

        x_size = rect_data.get("x_size")
        y_size = rect_data.get("y_size")
        x_padding = rect_data.get("x_padding")
        y_padding = rect_data.get("y_padding")

        x_pos = round(x_pos * (win_obj.screen_width / win_obj.y_ceil)) + x_offset
        y_pos = round(y_pos * (win_obj.screen_height / win_obj.x_ceil)) + y_offset

        if x_size is None or y_size is None:
            x_size = y_size = 0
        else:
            x_size = round(x_size * (win_obj.screen_width / win_obj.y_ceil)) + x_padding
            y_size = (
                round(y_size * (win_obj.screen_height / win_obj.x_ceil)) + y_padding
            )

        rect = pygame.Rect((0, 0), (x_size, y_size))
        setattr(rect, anchor_point, (x_pos, y_pos))

        return rect


class Text:
    """Define a pygame Text"""

    fonts = {}

    def __init__(self, text_data: dict, obj_rect: pygame.Rect) -> None:
        """
        Init new pygame text object

        Arguments:
            text_data: dict contains text data {font, text, antialias, color, align}
            obj_rect: the given element rect
        """
        self._font_size = None
        self._rect_size = obj_rect.size

        self.align_x = 0
        self.align_y = 0
        self.font_render = None

        self._text_data = self.set_text(text_data)
        self.set_align(self._text_data.get("align"))

    def set_text(self, text_data: dict) -> dict:
        """
        creates a new pygame text object

        Arguments:
            text_data: dict contains text data {font, text, antialias, color, align}

        Returns:
            dict contains all the text_data {font, text, color, ...}
        """
        data = {}

        data["font"] = self.fonts.get(text_data.get("font"))
        data["text"] = text_data.get("text")
        data["antialias"] = text_data.get("antialias")
        data["color"] = text_data.get("color")
        data["align"] = text_data.get("align")

        self.font_render = data.get("font").render(
            data.get("text"), data.get("antialias"), data.get("color")
        )
        self._font_size = self.font_render.get_rect().size

        return data

    def update_text(
        self,
        font: str = None,
        text: str = None,
        antialias: bool = None,
        color: str = None,
        align: str = None,
    ) -> None:
        """
        Update font properties

        Arguments:
            font: font name
            text: font text
            antialias: font antialias
            color: font color
            align: alignment direction
        """
        self._text_data["font"] = (
            self._text_data["font"] if font is None else self.fonts.get(font)
        )
        self._text_data["text"] = self._text_data["text"] if text is None else text
        self._text_data["antialias"] = (
            self._text_data["antialias"] if antialias is None else antialias
        )
        self._text_data["color"] = self._text_data["color"] if color is None else color
        self._text_data["align"] = self._text_data["align"] if align is None else align

        self.font_render = self._text_data.get("font").render(
            self._text_data.get("text"),
            self._text_data.get("color"),
            self._text_data.get("antialias"),
        )
        self._font_size = self.font_render.get_rect().size

        self.set_align(self._text_data.get("align"))

    def set_align(self, align: str) -> None:
        """
        Calculate the text alignment offset

        Arguments:
            align: text alignment (left, right, ...)
        """
        self._text_data["align"] = align

        self.align_x, self.align_y = align_offset(
            self._font_size, self._rect_size, align
        )

    @staticmethod
    def load_fonts(fonts: dict) -> None:
        """
        Load all fonts from config file

        Arguments:
            fonts: dict contains fonts {font_path, font_size}
        """

        for name, font in fonts.items():
            font_path = font.get("font_path")
            font_size = font.get("font_size")

            py_font = pygame.font.Font(font_path, font_size)
            Text.fonts[name] = py_font
