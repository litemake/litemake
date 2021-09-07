import typing
from .printer import litemakePrinter as Printer


def stringify_fieldpath(path: list) -> str:
    return '.'.join(str(p) for p in path)


class litemakeError(Exception):

    def __init__(self, *msg: str):
        self.msg = msg

    def print(self,) -> None:
        Printer.error('\n'.join(self.msg))


class litemakeWarning(Exception):
    def __init__(self, *msg: str):
        self.msg = msg

    def print(self,) -> None:
        Printer.warning('\n'.join(self.msg))


class litemakeTemplateError(litemakeError):
    """ Raised when there is an error in the litemake setup configuration
    file. """

    def __init__(self, fieldpath: typing.List[str], error: str):
        self.fieldpath = fieldpath
        self.error = error

        super().__init__(
            '*template error:*',
            f'Under field {stringify_fieldpath(fieldpath)!r} - {error}',
        )

    def to_config_error(self, filename: str) -> 'litemakeConfigError':
        return litemakeConfigError(filename, self.fieldpath, self.error)


class litemakeConfigError(litemakeError):
    """ Raised when there is an error in the litemake setup configuration
    file. """

    def __init__(self, filename: str, fieldpath: typing.List[str], msg: str):
        super().__init__(
            f'*configuration error in {filename!r}:*',
            f'Under field {stringify_fieldpath(fieldpath)!r} - {msg}',
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


class litemakeUnknownTargetsError(litemakeError):
    """ Raised by '__main__.py' if the user want to execute a target that is not
    specified in the configuration file. """

    def __init__(self, targets: typing.Set[str]):
        title = 'targets' if len(targets) > 1 else 'target'
        targets_str = ', '.join(repr(t_) for t_ in targets)
        super().__init__(f'*unknown {title}:* {targets_str}')


class litemakeNoSourcesWarning(litemakeWarning):
    """ Raised by the compiler when there are zero files that match the
    requested source files pattern. """
