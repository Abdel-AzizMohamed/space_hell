"""Define import handler module"""
###### Python Packages ######
from typing import Callable
from importlib import import_module

###### My Packages ######

#### Type Hinting ####


def check_import(import_path: str) -> Callable[..., None]:
    """
    Checks if the given import is a function or a method

    Arguments:
        import_path: given function/method path in format

    Returns:
        the imported function/method
    """

    if import_path.split(":")[-1].find(".") != -1:
        return import_method(import_path)
    return import_function(import_path)


def import_function(function_path: str) -> Callable[..., None]:
    """
    Import a given function from a string

    Arguments:
        function_path: given function path in format (path.to.module:function_name)

    Returns:
        the imported function
    """
    module_path, function_path = function_path.split(":")
    module = import_module(module_path)
    module_function = getattr(module, function_path)

    return module_function


def import_method(method_path: str) -> Callable[..., None]:
    """
    Import a given method from a string

    Arguments:
        method_path: given method path in format (path.to.module:class_name.method_name)

    Returns:
        the imported method
    """
    module_path, method_path = method_path.split(":")
    class_name, method_name = method_path.split(".")

    module = import_module(module_path)
    module_class = getattr(module, class_name)
    module_method = getattr(module_class, method_name)

    return module_method
