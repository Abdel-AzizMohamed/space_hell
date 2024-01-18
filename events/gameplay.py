"""Contains main menu events"""
# pylint: disable=E1101
# pylint: disable=R0913
###### Python Packages ######
import random
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
        offside_bullets = []

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

            check = Bullet.check_bullet(bullet)

            if check:
                offside_bullets.append(check)

        for bullet in offside_bullets:
            Bullet.bullets.remove(bullet)

    @staticmethod
    def check_bullet(bullet):
        """
        Check if any bullets collide with the target or reach the end of the screen

        Arguments:
            bullet: bullet to check if it's collided
        """
        if (
            bullet.element.rect.x <= 0
            or bullet.element.rect.left >= win_obj.screen_width
        ):
            Designer.remove_element(bullet.element.name)
            return bullet
        if (
            bullet.element.rect.y <= 0
            or bullet.element.rect.bottom >= win_obj.screen_height
        ):
            Designer.remove_element(bullet.element.name)
            return bullet

        return None


class Monster:
    """Define a Monster"""

    win_timer = None
    monster_attributes = read_json("dynamic_ui_data/gameplay.json").get("monster")
    monster_data = PyEngine.save_data.get("monsters").get("data").get("main_stage")
    current_monster_group = 0
    monsters = []

    def __init__(self, monster_type, monster_data, element_attributes):
        """Init a new monster object"""
        element_attributes["base_data"]["name"] = secrets.token_hex(8)

        if monster_data.get("x_pos") == "random":
            element_attributes["rect_data"]["x_pos"] = random.randint(0, 31)
        if monster_data.get("y_pos") == "random":
            element_attributes["rect_data"]["y_pos"] = random.randint(0, 17)
        if monster_data.get("delay") == "random":
            element_attributes["transition_data"]["delay"] = random.randint(1, 5)

        Designer.create_element(element_attributes)
        self.element = Designer.get_element(
            element_attributes.get("base_data").get("name")
        )

        Monster.monsters.append(self)

    @staticmethod
    def spawn_monsters():
        """Spawns monsters if the current monsters group are all dead"""
        if not Monster.monsters and Designer.exclude_groups.get("gameplay"):
            if len(Monster.monster_data) == Monster.current_monster_group:
                Monster.display_win()
                return

            current_monsters = Monster.monster_data[Monster.current_monster_group]
            Monster.current_monster_group += 1

            for monster_type, monster_group in current_monsters.items():
                for _ in range(monster_group.get("count")):
                    Monster(monster_type, monster_group, Monster.monster_attributes)

    @staticmethod
    def check_monster_state():
        """Check if the monster hp goes blow 0 or he reach the end of screen"""
        dead_monsters = []
        for monster in Monster.monsters:
            mon_width, mon_height = monster.element.rect.size
            mon_x = monster.element.rect.x
            mon_left = monster.element.rect.left
            mon_bottom = monster.element.rect.bottom

            if mon_x <= 0 - mon_width or mon_left >= win_obj.screen_width + mon_width:
                Designer.remove_element(monster.element.name)
                dead_monsters.append(monster)
            if mon_bottom >= win_obj.screen_height + mon_height:
                Designer.remove_element(monster.element.name)
                dead_monsters.append(monster)

        for dead in dead_monsters:
            Monster.monsters.remove(dead)

    @staticmethod
    def display_win():
        """Display win menu"""
        if Monster.win_timer is None:
            Designer.toggle_exclude("win_menu")
            Monster.win_timer = Timer(3500)
            Monster.win_timer.start_timer()
        elif Monster.win_timer.check_timer():
            Monster.win_timer = None
            Monster.return_to_menu()

    @staticmethod
    def return_to_menu():
        """Win the game"""
        Player.shoot_state(False)
        Designer.toggle_exclude("win_menu")
        Designer.toggle_exclude("main_menu")
        Designer.toggle_exclude("gameplay")
        Monster.current_monster_group = 0


class Player:
    """Define player"""

    bullet_data = read_json("dynamic_ui_data/gameplay.json").get("bullet")
    player = None
    current_x = 0
    current_y = 0
    is_shooting = False
    firerate = None

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

        if (
            Player.player.rect.centerx <= mouse_pos()[0] + 2
            and Player.player.rect.centerx >= mouse_pos()[0] - 2
        ):
            Player.player.rect.centerx = mouse_pos()[0]
        else:
            Player.current_x += x_speed
            Player.player.rect.centerx = Player.current_x
        if (
            Player.player.rect.centery <= mouse_pos()[1] + 2
            and Player.player.rect.centery >= mouse_pos()[1] - 2
        ):
            Player.player.rect.centery = mouse_pos()[1]
        else:
            Player.current_y += y_speed
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
            bullet_count = (
                PyEngine.save_data.get("main").get("data").get("bullet_upgrade")
            )
            if bullet_count == 1:
                Bullet(Player.player, "enemy", 500, 180, Player.bullet_data)
            if bullet_count == 2:
                Bullet(Player.player, "enemy", 500, 185, Player.bullet_data)
                Bullet(Player.player, "enemy", 500, 175, Player.bullet_data)
            if bullet_count >= 3:
                Bullet(Player.player, "enemy", 500, 185, Player.bullet_data)
                Bullet(Player.player, "enemy", 500, 180, Player.bullet_data)
                Bullet(Player.player, "enemy", 500, 175, Player.bullet_data)
            if bullet_count >= 4:
                Bullet(Player.player, "enemy", 500, 195, Player.bullet_data)
            if bullet_count >= 5:
                Bullet(Player.player, "enemy", 500, 165, Player.bullet_data)
            if bullet_count >= 6:
                Bullet(Player.player, "enemy", 500, 183, Player.bullet_data)
                Bullet(Player.player, "enemy", 500, 178, Player.bullet_data)

            Player.firerate.start_timer()
