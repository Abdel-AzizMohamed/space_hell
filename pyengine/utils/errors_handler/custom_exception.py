"""Define custom exceptions moudle"""


class InvalidDataTypeError(ValueError):
    """Define invalid data type in config/ui files"""

    def __init__(self, key: str, expected_type: str, actual_type: str) -> None:
        self.key = key
        self.expected_type = expected_type
        self.actual_type = actual_type
        message = f"Invalid data type for key '{key}'. Expected {expected_type}, but got {actual_type}."

        super().__init__(message)
