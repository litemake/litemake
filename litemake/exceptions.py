import typing
from .printer import litemakePrinter as Printer


class litemakeError(Exception):

    def __init__(self, *msg: str):
        self.msg = msg

    def print(self,) -> None:
        Printer.error('\n'.join(self.msg))


class litemakeConfigError(litemakeError):
    """ Raised when there is an error in the litemake setup configuration
    file. """

    def __init__(self, filename: str, fieldpath: typing.List[str], msg: str):
        super().__init__(
            f'*configuration error in {filename!r}:*',
            f'Under field {".".join(fieldpath)!r} - {msg}',
        )


class litemakeParsingError(litemakeError):
    """ Raised when the configuration file doesn't follow the TOML syntax
    specification and it can't be parsed correctly. """

    def __init__(self, filename: str, line: int, col: int, msg: str):
        super().__init__(
            f'*parsing error in {filename}:*',
            f'On line {line}, column {col} - {msg}',
        )


class litemakeSetupFileNotFoundError(litemakeError):
    """ Raised if the default (`setup.litemake.toml`) setup configuration
    file isn't present or if the custom file (specified with the -f/--flags
    arguments) isn't found. """

    def __init__(self, filename: str):
        super().__init__(f'*setup file {filename!r} not found*')


class litemakeCompilationError(litemakeError):
    """ Raised by the 'compiler' object if when calling the compiler (gcc, g++,
    clang), it returned a non-zero code. """

    def __init__(self, subprocess: str, error_msg: str):
        super().__init__(
            f'*error while calling {subprocess!r}:*',
            error_msg,
        )
