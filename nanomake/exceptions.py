import typing
from .printer import NanomakePrinter as Printer


class NanomakeError(Exception):

    def __init__(self, *msg: str):
        self.msg = msg

    def print(self,) -> None:
        Printer.error('\n'.join(self.msg))


class NanomakeConfigError(NanomakeError):
    """ Raised when there is an error in the nanomake setup configuration
    file. """

    def __init__(self, filename: str, fieldpath: typing.List[str], msg: str):
        super().__init__(
            f'*configuration error in {filename!r}:*',
            f'Under field {fieldpath!r}: {msg}',
        )


class NanomakeParsingError(NanomakeError):
    """ Raised when the configuration file doesn't follow the TOML syntax
    specification and it can't be parsed correctly. """

    def __init__(self, filename: str, line: int, col: int, msg: str):
        super().__init__(
            f'*parsing error in {filename}:*',
            f'On line {line}, column {col} - {msg}',
        )


class NanomakeSetupFileNotFoundError(NanomakeError):
    """ Raised if the default (`setup.nanomake.toml`) setup configuration
    file isn't present or if the custom file (specified with the -f/--flags
    arguments) isn't found. """

    def __init__(self, filename: str):
        super().__init__(f'*setup file {filename!r} not found*')
