"""Contains main menu events"""
# pylint: disable=E1101
###### Python Packages ######
import secrets
import math
from pygame.mouse import get_pos as mouse_pos

###### My Packages ######
from pyengine.engine import PyEngine
from pyengine.libs.designer.designer import Designer
from pyengine import win_obj
from pyengine.utils.json_handler import read_json
from pyengine.utils.timer import Timer

#### Type Hinting ####


def calc_angle(object_1: tuple, object_2: tuple):
    """Calc the angle between 2 objects"""
    dx = object_1[0] - object_2[0]
    dy = object_1[1] - object_2[1]

    angle = math.atan2(dy, dx)
    x_angel = math.cos(angle)
    y_angel = math.sin(angle)

    return (x_angel, y_angel)


class Bullet:
    """Define a bullet"""

    bullets = []

    def __init__(self, source, target, speed, angel, element_attributes):
        """Init a new bullet object"""
        self.target = target
        self.speed = speed
        self.angel = angel

        element_attributes["base_data"]["name"] = secrets.token_hex(8)
        Designer.create_element(element_attributes)
        self.element = Designer.get_element(
            element_attributes.get("base_data").get("name")
        )
        self.element.rect.center = source.rect.center

        self.current_x = self.element.rect.centerx
        self.current_y = self.element.rect.centery

        Bullet.bullets.append(self)

    @staticmethod
    def move_bullets():
        """Move all bullets"""
        for bullet in Bullet.bullets:
            bullet.current_x += (
                bullet.speed
                * win_obj.delta_time
                * -math.sin(math.radians(bullet.angel))
            )
            bullet.current_y += (
                bullet.speed * win_obj.delta_time * math.cos(math.radians(bullet.angel))
            )

            bullet.element.rect.x = bullet.current_x
            bullet.element.rect.y = bullet.current_y


class Player:
    """Define player"""

    bullet_data = read_json("dynamic_ui_data/gameplay.json").get("bullet")
    player = None
    current_x = 0
    current_y = 0
    is_shooting = False
    firerate = None
    angel = 0

    @staticmethod
    def load_player(_, player_name: str) -> None:
        """Init a new player object"""
        PyEngine.save_data["main"]["data"]["hp"] = (
            PyEngine.save_data["main"]["data"]["hp_upgrade"] * 5
        )
        Player.player = Designer.get_element(player_name)
        Player.current_x = Player.player.rect.x
        Player.current_y = Player.player.rect.y
        Player.firerate = Timer(
            800 / PyEngine.save_data.get("main").get("data").get("firerate_upgrade")
        )

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

    @staticmethod
    def shoot_state(state):
        """Switch shooting state"""
        if Designer.exclude_groups.get("gameplay"):
            Player.is_shooting = state
            Player.firerate.start_timer()

    @staticmethod
    def shoot_bullets():
        """Shot bullets"""
        if Player.is_shooting and Player.firerate.check_timer():
            Bullet(Player.player, "enemy", 100, Player.angel, Player.bullet_data)
            Player.firerate.start_timer()
            Player.angel += 1
