"""Define a path handling moudle"""
import os


def alternate_path(main, alt=""):
    """
    Check if the main path is valid or alt path if valid else throw an error

    Arguments:
        main: Main path to check if it's exists
        alt: Alternate path if the given path doesn't exists
    """
    if os.path.exists(main):
        return main
    if os.path.exists(alt):
        return alt
    raise FileNotFoundError(f"No such file/directory for: {main}&{alt}")


def walk_search(dir_path: str, exe_filter: str = "") -> list:
    """
    returns list for all files path that are in the given directory and its sub directories

    Arguments:
        dir_path: directory path to preform walk search
        exe_filter: wanted files extension (without dot '.')
    """
    search_result = []

    for root_path, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root_path, file)
            _, file_exe = os.path.splitext(file)

            if exe_filter and file_exe != exe_filter:
                continue

            search_result.append(file_path)

    return search_result
