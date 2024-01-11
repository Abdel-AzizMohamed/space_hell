"""Contains all transition functions movement"""
###### Python Packages ######
from __future__ import annotations
from typing import TYPE_CHECKING

###### My Packages ######
from pyengine import win_obj
from pyengine.utils.import_handler import check_import

#### Type Hinting ####
if TYPE_CHECKING:
    from pyengine.libs.transition.transition import Transition


def liner_transition(transition: Transition):
    """Move the element with a liner speed"""
    if transition.start_x is not None and transition.end_x is not None:
        offset = round(
            (abs(transition.start_x - transition.end_x) / transition.duration)
            * win_obj.delta_time
        )
        transition.element.rect.x += offset
        if transition.element.rect.x >= transition.end_x:
            transition.transition_state = False
            transition.delay.start_timer()
            for data in transition.after_functions:
                check_import(data.get("import"))(transition.element, *data.get("args"))

    elif transition.start_y is not None and transition.end_y is not None:
        offset = round(
            (abs(transition.start_y - transition.end_y) / transition.duration)
            * win_obj.delta_time
        )
        transition.element.rect.y += offset
        if transition.element.rect.y >= transition.end_y:
            transition.transition_state = False
            transition.delay.start_timer()
            for data in transition.after_functions:
                check_import(data.get("import"))(transition.element, *data.get("args"))
