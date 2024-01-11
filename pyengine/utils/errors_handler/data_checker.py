"""Define a execption handling moudle"""
import os
from importlib import import_module
import pygame
from pyengine.utils.json_handler import read_json
from pyengine.utils.errors_handler.custom_exception import InvalidDataTypeError


def validate_color(color: str) -> bool:
    """
    Checks if the given color is vaild

    Arguments:
        color: color value to validate
    """
    try:
        pygame.Color(color)
        return True
    except ValueError:
        return False


def validate_path(
    input_path: str, valid_file: bool = False, valid_dir: bool = False
) -> bool:
    """Check if the given file/dir exists"""
    if valid_file and os.path.isfile(input_path):
        return True
    elif valid_dir and os.path.isdir(input_path):
        return True
    return False


def validate_data(
    file_name: str,
    data: any,
    data_name: str,
    data_type: str,
    valid_color: bool = False,
    vaild_file: bool = False,
    vaild_dir: bool = False,
    valid_range: int = None,
    valid_data: list = None,
) -> None:
    """Validate the given data"""
    if data is None:
        raise KeyError(f"{data_name} not found, in {file_name} file")

    if not isinstance(data, data_type):
        raise InvalidDataTypeError(data_name, data_type.__name__, type(data).__name__)

    if valid_color and not validate_color(data):
        raise ValueError(f"Incorrect color value {data}, for {data_name}")

    if vaild_dir or vaild_file and not validate_path(data, vaild_file, vaild_dir):
        raise FileNotFoundError(f"No such a file {data}")

    if valid_range and data < valid_range:
        raise ValueError(f"{data_name} should be >= {valid_range}, but got {data}")

    if valid_data and data not in valid_data:
        raise ValueError(
            f"Incorrect data value for {data_name}, Got {data} Expected {valid_data}"
        )


def config_check(file: str) -> None:
    """
    Check if the given config file has the right values/types
    and if a key dosen't exists

    Arguments:
        file: config file path
    """
    file_data = read_json(file)

    window = file_data.get("window")
    fonts = file_data.get("fonts")
    devtools = file_data.get("devtools")
    events = file_data.get("events")

    validate_data(file, window, "window", dict)
    validate_data(file, fonts, "fonts", dict)
    validate_data(file, devtools, "devtools", dict)
    validate_data(file, events, "events", dict)

    window_size = window.get("size")
    grid_div = window.get("grid_div")
    fps = window.get("fps")
    title = window.get("title")

    validate_data(file, window_size, "window_size", list)
    validate_data(file, window_size[0], "window width", int, valid_range=0)
    validate_data(file, window_size[1], "window height", int, valid_range=0)

    validate_data(file, grid_div, "grid_div", int, valid_range=1)
    validate_data(file, fps, "fps", int, valid_range=1)
    validate_data(file, title, "title", str)

    current_fonts = []

    for name, font in fonts.items():
        current_fonts.append(name)

        font_path = font.get("font_path")
        size = font.get("size")

        validate_data(file, font_path, "font_path", str, vaild_file=True)
        validate_data(file, size, "size", int, valid_range=1)

    aligment = [
        "top",
        "topleft",
        "topright",
        "center",
        "midleft",
        "midright",
        "bottom",
        "bottomeleft",
        "bottomright",
    ]

    grid_color = devtools.get("grid_color")
    fps_font = devtools.get("fps_font")
    fps_antialias = devtools.get("fps_antialias")
    fps_color = devtools.get("fps_color")
    fps_align = devtools.get("fps_align")
    object_rect_color = devtools.get("object_rect_color")
    object_rect_size = devtools.get("object_rect_size")

    validate_data(file, grid_color, "grid_color", str, valid_color=True)

    validate_data(file, fps_font, "fps_font", str, valid_data=current_fonts)
    validate_data(file, fps_antialias, "fps_antialias", bool)
    validate_data(file, fps_color, "fps_color", str, valid_color=True)
    validate_data(file, fps_align, "fps_align", str, valid_data=aligment)

    validate_data(file, object_rect_color, "object_rect_color", str, valid_color=True)
    validate_data(file, object_rect_size, "object_rect_size", int, valid_range=1)


def ui_check(file: str, config_file: str) -> None:
    """
    Check if the given ui file has the right values/types
    and if a key dosen't exists

    Arguments:
        file: ui file path
        config_file: config file path
    """
    file_data = read_json(file)
    config_data = read_json(config_file)

    for element in file_data.values():
        base = element.get("base")
        rect = element.get("rect")
        events = element.get("events")
        text_obj = element.get("text_obj")

        validate_data(file, base, "base", dict)
        validate_data(file, rect, "rect", dict)
        validate_data(file, text_obj, "text_obj", dict)

        name = base.get("name")
        group = base.get("group")
        element_type = base.get("class")

        validate_data(file, name, "name", str)
        validate_data(file, group, "group", str)
        validate_data(file, element_type, "class", str)

        x_pos = rect.get("x_pos")
        y_pos = rect.get("y_pos")
        x_size = rect.get("x_size")
        y_size = rect.get("y_size")
        radius = rect.get("radius")

        validate_data(file, x_pos, "x_pos", int)
        validate_data(file, y_pos, "y_pos", int)

        if element_type == "PyCircle":
            validate_data(file, radius, "radius", float)
        else:
            validate_data(file, x_size, "x_size", int)
            validate_data(file, y_size, "y_size", int)

        event_types = ["leftclick", "rightclick", "middleclick"]

        for function_path, event in events.items():
            moudle_path, function_name = function_path.split(":")

            try:
                function = getattr(import_module(moudle_path), function_name)
            except Exception as e:
                raise e
            if function is None:
                raise AttributeError(
                    f"module {moudle_path} has no function {function_name}"
                )
            event_type = event.get("event")
            event_args = event.get("args")

            validate_data(file, event_type, "event_type", str, valid_data=event_types)
            validate_data(file, event_args, "event_args", list)

        current_fonts = []
        for font_name in config_data.get("fonts").keys():
            current_fonts.append(font_name)

        font = text_obj.get("font")
        text = text_obj.get("text")
        antialias = text_obj.get("antialias")
        color = text_obj.get("color")
        align = text_obj.get("align")

        aligment = [
            "top",
            "topleft",
            "topright",
            "center",
            "midleft",
            "midright",
            "bottom",
            "bottomeleft",
            "bottomright",
        ]

        validate_data(file, font, "font", str, valid_data=current_fonts)
        validate_data(file, text, "text", str)
        validate_data(file, antialias, "antialias", bool)
        validate_data(file, color, "color", str, valid_color=True)
        validate_data(file, align, "align", str, valid_data=aligment)

        if element_type == "PyCircle" or element_type == "PyRect":
            element_color = element.get("color")
            validate_data(file, element_color, "element_color", str, valid_color=True)
        else:
            button = element.get("button")
            active = button.get("active")
            disabled = button.get("disabled")
            base_color = button.get("base_color")
            hover_color = button.get("hover_color")
            select_color = button.get("select_color")
            disabled_color = button.get("disabled_color")

            validate_data(file, button, "button", dict)
            validate_data(file, active, "active", bool)
            validate_data(file, disabled, "disabled", bool)
            validate_data(file, base_color, "base_color", str, valid_color=True)
            validate_data(file, hover_color, "hover_color", str, valid_color=True)
            validate_data(file, select_color, "select_color", str, valid_color=True)
            validate_data(file, disabled_color, "disabled_color", str, valid_color=True)
