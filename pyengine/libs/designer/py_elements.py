"""Contains all the basic ui elements"""
# pylint: disable=R0903
# pylint: disable=R0902
###### Python Packages ######
###### My Packages ######
from pyengine.libs.designer.py_base import PyBase
from pyengine.libs.designer.py_attributes import Rectangle, Text
from pyengine.libs.eventer.eventer import Eventer

#### Type Hinting ####


class PyRect(PyBase, Rectangle, Text):
    """Define a basic rect shape"""

    def __init__(self, attributes: dict) -> None:
        """
        Init a new Rect object

        Attributes:
            attributes: contains all the rect element data
        """
        PyBase.__init__(self, attributes.get("base_data"))
        Rectangle.__init__(self, attributes.get("rect_data"))
        Text.__init__(self, attributes.get("text_data"), self.rect)

        obj_data = attributes.get("obj_data")

        self.color = obj_data.get("color")
        self.opacity = obj_data.get("opacity")


class PyCircle(PyBase, Rectangle, Text):
    """Define a basic circle shape"""

    def __init__(self, attributes: dict) -> None:
        """
        Init a new circle element object

        Attributes:
            attributes: contains all the circle data
        """
        PyBase.__init__(self, attributes.get("base_data"))
        Rectangle.__init__(self, attributes.get("rect_data"))
        Text.__init__(self, attributes.get("text_data"), self.rect)

        obj_data = attributes.get("obj_data")

        self.radius = obj_data.get("radius")
        self.rect.size = (self.radius * 2, self.radius * 2)

        self.color = obj_data.get("color")
        self.opacity = obj_data.get("opacity")


class PyButton(PyBase, Rectangle, Text):
    """Define a basic button object"""

    def __init__(self, attributes: dict) -> None:
        """
        Init a new button element object

        Attributes:
            attributes: contains all the button data
        """
        PyBase.__init__(self, attributes.get("base_data"))
        Rectangle.__init__(self, attributes.get("rect_data"))
        Text.__init__(self, attributes.get("text_data"), self.rect)

        obj_data = attributes.get("obj_data")

        self.active = obj_data.get("active")
        self.disabled = obj_data.get("disabled")

        self.active_color = self.base_color = obj_data.get("base_color")
        self.hover_color = obj_data.get("hover_color")
        self.select_color = obj_data.get("select_color")
        self.disabled_color = obj_data.get("disabled_color")

        self.opacity = obj_data.get("opacity")

        Eventer.add_object_event(
            self,
            {
                "button_hover": {
                    "function_path": "pyengine.libs.eventer.ui_events:ButtonEvents.button_hover",
                    "event_type": "mousein",
                    "args": [],
                }
            },
        )
        Eventer.add_object_event(
            self,
            {
                "button_unhover": {
                    "function_path": "pyengine.libs.eventer.ui_events:ButtonEvents.button_hover",
                    "event_type": "mouseout",
                    "args": [False],
                }
            },
        )
        Eventer.add_object_event(
            self,
            {
                "button_select": {
                    "function_path": "pyengine.libs.eventer.ui_events:ButtonEvents.button_select",
                    "event_type": "leftclick",
                    "args": [],
                }
            },
        )
