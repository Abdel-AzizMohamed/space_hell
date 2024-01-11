"""Contains all the images elements"""
# pylint: disable=R0903
###### Python Packages ######
###### My Packages ######
from pyengine.libs.designer.py_base import PyBase, PyImageBase
from pyengine.libs.designer.py_attributes import Rectangle, Text

#### Type Hinting ####


class PyImage(PyBase, PyImageBase, Rectangle, Text):
    """Define a basic image"""

    def __init__(self, attributes: dict) -> None:
        """
        Init a new image object

        Attributes:
            attributes: contains all the image element data
        """
        PyBase.__init__(self, attributes.get("base_data"))
        Rectangle.__init__(self, attributes.get("rect_data"))
        Text.__init__(self, attributes.get("text_data"), self.rect)
        PyImageBase.__init__(self, attributes.get("image_data"))

        self.rect.size = self.image.get_rect().size
        self.opacity = attributes.get("obj_data").get("opacity")
