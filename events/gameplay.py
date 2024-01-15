"""Contains main menu events"""
# pylint: disable=E1101
###### Python Packages ######
import math
from pygame.mouse import get_pos as mouse_pos

###### My Packages ######
from pyengine.engine import PyEngine
from pyengine.libs.designer.designer import Designer
from pyengine import win_obj

#### Type Hinting ####


def calc_angle(object_1: tuple, object_2: tuple):
    """Calc the angle between 2 objects"""
    dx = object_1[0] - object_2[0]
    dy = object_1[1] - object_2[1]

    angle = math.atan2(dy, dx)
    x_angel = math.cos(angle)
    y_angel = math.sin(angle)

    return (x_angel, y_angel)


class Player:
    """Define player"""

    player = None
    current_x = 0
    current_y = 0

    @staticmethod
    def load_player(_, player_name: str) -> None:
        """Init a new player object"""
        PyEngine.save_data["main"]["data"]["hp"] = (
            PyEngine.save_data["main"]["data"]["hp_upgrade"] * 5
        )
        Player.player = Designer.get_element(player_name)
        Player.current_x = Player.player.rect.x
        Player.current_y = Player.player.rect.y

    @staticmethod
    def player_movement() -> None:
        """Move the player"""
        if not Designer.exclude_groups.get("gameplay"):
            return

        speed = PyEngine.save_data.get("main").get("data").get("speed_upgrade")

        x_angle, y_angle = calc_angle(mouse_pos(), Player.player.rect.center)
        x_speed = (speed * 50 + 150) * win_obj.delta_time * x_angle
        y_speed = (speed * 50 + 150) * win_obj.delta_time * y_angle

        Player.current_x += x_speed
        Player.current_y += y_speed

        Player.player.rect.centerx = Player.current_x
        Player.player.rect.centery = Player.current_y

    @staticmethod
    def display_hp() -> None:
        """Display player hp"""
        player_hp = PyEngine.save_data.get("main").get("data").get("hp")
        max_hp = PyEngine.save_data.get("main").get("data").get("hp_upgrade") * 5
        Designer.get_element("player_hp").update_text(text=f"HP: {player_hp}/{max_hp}")

    @staticmethod
    def display_points() -> None:
        """Display player hp"""
        player_points = PyEngine.save_data.get("main").get("data").get("points")
        Designer.get_element("player_points").update_text(
            text=f"Points: {player_points}"
        )
