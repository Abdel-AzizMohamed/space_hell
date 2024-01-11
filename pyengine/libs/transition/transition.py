"""Main transition module"""
# pylint: disable=R0902
###### Python Packages ######
###### My Packages ######
from pyengine.libs.transition.transition_functions import liner_transition
from pyengine.utils.timer import Timer
from pyengine.utils.import_handler import check_import

#### Type Hinting ####


class Transition:
    """Define a transition effect"""

    elements = {}
    exclude_groups = {}
    transition_functions = {"liner": liner_transition}

    def __init__(self, element, attributes: dict) -> None:
        """
        Init a new transition object

        Attributes:
            attributes: contains all the transition data
        """
        self.element = element

        self.duration = attributes.get("duration")
        self.delay = Timer(attributes.get("delay") * 1000)
        self.delay.start_timer()
        self.repeat = attributes.get("repeat")
        self.transition_state = True
        self.transition_function = attributes.get("transition_function")

        self.after_functions = attributes.get("after_functions")
        self.during_functions = attributes.get("during_functions")
        self.before_functions = attributes.get("before_functions")

        self.start_x = attributes.get("start_x")
        self.element.rect.x = (
            self.start_x if self.start_x is not None else self.element.rect.x
        )
        self.start_y = attributes.get("start_y")
        self.element.rect.y = (
            self.start_y if self.start_y is not None else self.element.rect.y
        )

        self.end_x = attributes.get("end_x")
        self.end_y = attributes.get("end_y")

        if self.duration >= 1:
            Transition.elements[element.group].append(self)

        for data in self.before_functions:
            check_import(data.get("import"))(self.element, *data.get("args"))

    @staticmethod
    def trigger_transition() -> None:
        """Trigger all the transition"""
        elements = [
            element
            for (name, group) in Transition.elements.items()
            for element in group
            if Transition.exclude_groups.get(name)
        ]

        for element in elements:
            timer_check = element.delay.check_timer()
            if not timer_check and timer_check is not None:
                continue
            if element.transition_state:
                Transition.transition_functions.get(element.transition_function)(
                    element
                )
                for data in element.during_functions:
                    check_import(data.get("import"))(element.element, *data.get("args"))
            else:
                element.reset_transition()

    def reset_transition(self) -> None:
        """Reset the given transition after a delay and if it still repeated"""
        if self.repeat == 1:
            return

        for data in self.before_functions:
            check_import(data.get("import"))(self.element, *data.get("args"))

        self.repeat = self.repeat - 1 if self.repeat != -1 else self.repeat

        self.transition_state = True
        self.element.rect.x = (
            self.start_x if self.start_x is not None else self.element.rect.x
        )
        self.element.rect.y = (
            self.start_y if self.start_y is not None else self.element.rect.y
        )
