"""Define game events handler"""
#### Python Packages ####
import pygame

# pylint: disable=E1101
#### My Packages ####
from pyengine.utils.collision_handler import mouse_collision
from pyengine.utils.import_handler import check_import


class Eventer:
    """Define main event class"""

    elements_events = {}
    global_events = []
    exclude_groups = {}

    @staticmethod
    def add_object_event(element: object, events_data: dict) -> None:
        """
        Add event to given element

        Arguments:
            element: element the preform the event
            event_data: dict contains event_data {event, args}
        """
        if events_data is None:
            return

        if not Eventer.elements_events.get(element.group):
            Eventer.elements_events[element.group] = []

        for event_data in events_data.values():
            module_function = check_import(event_data.get("function_path"))

            Eventer.elements_events[element.group].append(
                (module_function, event_data, element)
            )

    @staticmethod
    def load_global_events(events: dict, element_grabber: object) -> list:
        """
        Load global events from config file

        Arguments:
            event_data: dict contains event_data {event, args}
        """
        non_events = []

        for event in events.values():
            module_function = check_import(event.get("function_path"))

            if event.get("event_type") == "none":
                non_events.append((module_function, event))
            elif event.get("event_type") == "rectin":
                event["args"][0] = element_grabber(event["args"][0])
                event["args"][1] = element_grabber(event["args"][1])
                non_events.append((module_function, event))
            else:
                Eventer.global_events.append((module_function, event))

        return non_events

    @staticmethod
    def trigger_events(event: pygame.event) -> None:
        """
        Trigger all global/elements events

        Arguments:
            event: event object from pygame to check for events
        """
        elements = [
            element
            for (name, group) in Eventer.elements_events.items()
            for element in group
            if Eventer.exclude_groups.get(name)
        ]

        for element in elements:
            function = element[0]
            event_type = element[1].get("event_type")

            args = element[1].get("args").copy()
            args.insert(0, element[2])
            rect = element[2].rect

            if not mouse_collision(rect) and event_type == "mouseout":
                function(*args)
            if mouse_collision(rect) and event_type == "mousein":
                function(*args)
            if Eventer.check_mouse_event(event, event_type) and mouse_collision(rect):
                function(*args)
            if Eventer.check_keyboard_event(event, event_type):
                function(*args)

        for global_event in Eventer.global_events:
            function = global_event[0]
            event_type = global_event[1].get("event_type")
            args = global_event[1].get("args").copy()

            if Eventer.check_mouse_event(event, event_type):
                function(*args)
            if Eventer.check_keyboard_event(event, event_type):
                function(*args)

    @staticmethod
    def check_mouse_event(event: pygame.event, event_type: str) -> bool:
        """
        Check for mouse event

        Arguments:
            event: event object from pygame to check for events
            event_type: event type (leftclick, rightclick)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event_type == "click":
                return True
            if event.button == 1 and event_type == "leftclick":
                return True
            if event.button == 2 and event_type == "middleclick":
                return True
            if event.button == 3 and event_type == "rightclick":
                return True
        return False

    @staticmethod
    def check_keyboard_event(event: pygame.event, event_type: str) -> bool:
        """
        Check for keyboard event

        Arguments:
            event: event object from pygame to check for events
            event_type: event type (leftclick, rightclick)
        """
        if event_type.find(":") == -1:
            return False

        key_action, key = event_type.split(":")

        if event.type == pygame.KEYDOWN and key_action == "down":
            if event.key == getattr(pygame, key):
                return True
        if event.type == pygame.KEYUP and key_action == "up":
            if event.key == getattr(pygame, key):
                return True

        return False
