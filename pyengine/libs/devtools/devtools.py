"""Define start point for Devtools Package"""
# pylint: disable=R0903
###### Python Packages ######
###### My Packages ######
from pyengine.libs.devtools.debug_tools import Debugger


class DevTools:
    """Define main developer tools class"""

    tools_config = {"grid": {}, "fps": {}, "object_rect": {}}

    show_grid = True
    show_fps = True
    show_object_rect = True

    @staticmethod
    def display_tools() -> None:
        """Display developer tools if active"""
        grid_data = DevTools.tools_config.get("grid")
        fps_data = DevTools.tools_config.get("fps")
        object_rect_data = DevTools.tools_config.get("object_rect")

        if DevTools.show_grid:
            Debugger.display_grid(grid_data)
        if DevTools.show_fps:
            Debugger.display_fps(fps_data)
        if DevTools.show_object_rect:
            Debugger.display_object_rect(object_rect_data)

    @staticmethod
    def toggle_tool(tool: str) -> None:
        """
        Toggle Debug tool/tools

        Arguments:
            tool: tool name if the value is 'all' then all tools will be toggled
        """
        if tool == "all":
            DevTools.show_grid = not DevTools.show_grid
            DevTools.show_fps = not DevTools.show_fps
            DevTools.show_object_rect = not DevTools.show_object_rect
        elif getattr(DevTools, tool):
            setattr(DevTools, tool, False)
        else:
            setattr(DevTools, tool, True)

    @staticmethod
    def load_devtools(config: dict):
        """
        Load devtools config

        Arguments:
            config: dict contains devtools config
        """
        DevTools.tools_config["grid"]["grid_color"] = config.get("grid_color")

        DevTools.tools_config["fps"]["fps_font"] = config.get("fps_font")
        DevTools.tools_config["fps"]["fps_antialias"] = config.get("fps_antialias")
        DevTools.tools_config["fps"]["fps_color"] = config.get("fps_color")
        DevTools.tools_config["fps"]["fps_align"] = config.get("fps_align")

        DevTools.tools_config["object_rect"]["object_rect_color"] = config.get(
            "object_rect_color"
        )
        DevTools.tools_config["object_rect"]["object_rect_size"] = config.get(
            "object_rect_size"
        )
