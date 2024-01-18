"""Contains main menu events"""
# pylint: disable=E1101
# pylint: disable=W0212
###### Python Packages ######
import sys
import pygame

###### My Packages ######
from pyengine.engine import PyEngine
from pyengine.libs.designer.designer import Designer
from pyengine.libs.transition.transition import Transition

#### Type Hinting ####
from pyengine.libs.designer.py_elements import PyRect


def exit_game(_) -> None:
    """Exit the game :)"""
    pygame.quit()
    sys.exit()


def background_repeat(background: PyRect) -> None:
    """Move the background to the top of the screen"""
    if Transition.elements.get(background.group).get(background.name).start_y != -768:
        Transition.elements.get(background.group).get(background.name).start_y = -768
        Transition.elements.get(background.group).get(background.name).duration *= 2


def toggle_shop(_):
    """toggle shop menu"""
    Designer.toggle_exclude("shop_menu")


def start_game(_):
    """start the game"""
    Designer.toggle_exclude("main_menu")
    Designer.toggle_exclude("gameplay")
    Designer.exclude_groups["shop_menu"] = 0


def calc_price(base: int, level: int) -> int:
    """
    Calculate the upgrade price

    Arguments:
        base: the base price
        level: the level of the upgrade
    """
    return round(base * 1.5**level)


def refresh_upgrades(_):
    """Refresh all upgrades buttons"""
    buttons = [
        ["hp_upgrade", 30],
        ["damage_upgrade", 50],
        ["speed_upgrade", 20],
        ["firerate_upgrade", 40],
        ["bullet_upgrade", 70],
    ]
    upgrades_data = PyEngine.save_data.get("main").get("data")

    for upgrade in buttons:
        upgrade_name = upgrade[0]
        upgrade_base = upgrade[1]

        upgrade_button = Designer.get_element(upgrade_name)
        upgrade_level = upgrades_data.get(upgrade_name)
        upgrade_price = calc_price(upgrade_base, upgrade_level)

        upgrade_text = upgrade_button._text_data.get("text").split(" ")
        upgrade_text[-1] = "$" + str(upgrade_price)
        upgrade_text[-2] = str(upgrade_level)

        upgrade_button.update_text(text=" ".join(upgrade_text))


def buy_upgrade(_, upgrade_name: str) -> None:
    """
    Checks if you can buy an upgrade
    and update the upgrade in the save file & upgrade button

    Arguments:
        upgrade_name: upgrade name from the save file
    """
    upgrades_base = {
        "hp_upgrade": 30,
        "damage_upgrade": 50,
        "speed_upgrade": 20,
        "firerate_upgrade": 40,
        "bullet_upgrade": 70,
    }
    points = PyEngine.save_data.get("main").get("data").get("points")
    upgrade_data = PyEngine.save_data.get("main").get("data")

    price = calc_price(upgrades_base.get(upgrade_name), upgrade_data.get(upgrade_name))

    if points >= price:
        PyEngine.save_data.get("main").get("data")["points"] -= price
        upgrade_data[upgrade_name] += 1

    refresh_upgrades("")
