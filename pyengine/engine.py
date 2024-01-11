"""Project start point"""
# pylint: disable=E1101
# pylint: disable=W0511
# pylint: disable=R0914
###### Python Packages ######
import os
import sys
import pygame

###### My Packages ######
from pyengine import win_obj, CONFIG_PATH
from pyengine.libs.mixer import Sound, Music

from pyengine.libs.eventer.eventer import Eventer

from pyengine.libs.designer.designer import Designer
from pyengine.libs.designer.py_base import PyImageBase
from pyengine.libs.designer.py_attributes import Text

from pyengine.libs.devtools.devtools import DevTools

from pyengine.libs.transition.transition import Transition

from pyengine.utils.json_handler import read_json, write_json
from pyengine.utils.collision_handler import object_collision
from pyengine.utils.path_handler import walk_search

# from pyengine.utils.errors_handler.data_checker import config_check, ui_check
#### Type Hinting ####


class PyEngine:
    """Main class that works as a connector for all packages"""

    none_events = []
    save_data = {}
    auto_save = None

    @staticmethod
    def run(debug: bool = False):
        """
        Run the app

        Arguments:
            debug: Display debugging tools
        """
        PyEngine.load_data()
        PyEngine.mainloop(debug)

    @staticmethod
    def mainloop(debug: bool) -> None:
        """
        game mainloop

        Arguments:
            debug: Display debugging tools
        """
        while True:
            win_obj.set_delta()
            PyEngine.check_events(debug)

            for global_event in PyEngine.none_events:
                function = global_event[0]
                event_type = global_event[1].get("event")
                args = global_event[1].get("args").copy()

                if event_type == "rectin":
                    rect_1 = args.pop(0).rect
                    rect_2 = args.pop(0).rect
                    if object_collision(rect_1, rect_2):
                        function(*args)
                else:
                    function(*args)

            Transition.trigger_transition()

            Designer.draw_groups()
            if debug:
                DevTools.display_tools()

            pygame.display.update()
            win_obj.clock.tick(win_obj.fps)

    @staticmethod
    def check_events(debug: bool) -> None:
        """
        Check all game events

        Arguments:
            debug: Trigger debugging events if true
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and debug:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == PyEngine.auto_save:
                for data in PyEngine.save_data.values():
                    write_json(data.get("path"), data.get("data"))

            Eventer.trigger_events(event)

    @staticmethod
    def load_data() -> None:
        """Loads game data"""
        # TODO: Fix the data check and add it here before loading the data
        # config_check(CONFIG_PATH)

        # for file in walk_search("UiData"):
        #     ui_check(file, CONFIG_PATH)

        game_config = read_json(CONFIG_PATH)

        fonts_data = game_config.get("fonts_data")
        devtools_data = game_config.get("devtools_data")
        events_data = game_config.get("events_data")
        sounds_data = game_config.get("sounds_data")
        music_data = game_config.get("music_data")
        groups_data = game_config.get("groups_data")
        default_data = game_config.get("default_data")
        path_data = game_config.get("path_data")

        Text.load_fonts(fonts_data)
        DevTools.load_devtools(devtools_data)
        Sound.load_sounds(sounds_data)

        Music.load_music(music_data)
        if default_data.get("default_music"):
            Music.play_music(default_data.get("default_music"))

        for save_file_path in walk_search(path_data.get("save_data_path")):
            save_file_name = os.path.splitext(os.path.basename(save_file_path))[0]
            save_file_data = read_json(save_file_path)
            PyEngine.save_data[save_file_name] = {
                "data": save_file_data,
                "path": save_file_path,
            }

        images = {}
        for image_path in walk_search(path_data.get("sprites_path")):
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            images[image_name] = image_path
        PyImageBase.load_images(images)

        for ui_file in walk_search(path_data.get("ui_data_path")):
            Designer.create_from_file(ui_file)

        for group, value in groups_data.items():
            Designer.exclude_groups[group] = value
            Eventer.exclude_groups[group] = value

        PyEngine.none_events = Eventer.load_global_events(
            events_data, Designer.get_element
        )

        if default_data.get("default_auto_save"):
            PyEngine.auto_save = pygame.USEREVENT + 1
            pygame.time.set_timer(
                PyEngine.auto_save, default_data.get("default_auto_save")
            )

    @staticmethod
    def update_data(file_name: str, data_name: str, new_data: any) -> None:
        """
        Update data from a save file

        Arguments:
            file_name: save file name (without extension)
            data_name: the name of the data that will be updated
            new_data: the new data the will be replaced with the current data
        """
        PyEngine.save_data[file_name]["data"][data_name] = new_data

    @staticmethod
    def get_data(file_name: str, data_name: str) -> any:
        """
        Update data from a save file

        Arguments:
            file_name: save file name (without extension)
            data_name: the name of the data
        """
        return PyEngine.save_data.get(file_name).get("data").get(data_name)
