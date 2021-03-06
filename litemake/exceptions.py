import typing
from .printer import litemakePrinter as Printer


T = typing.TypeVar("T")


def stringify_fieldpath(path: list) -> str:
    return ".".join(str(p) for p in path)


class litemakeError(Exception):
    def __init__(self, *msg: str, raw_msg: str = None):
        super().__init__(msg)
        self.msg = msg
        self.raw_msg = raw_msg

    def print(self) -> None:
        Printer.error("\n".join(self.msg))


class litemakeTemplateError(litemakeError):
    """Raised when there is an error in the litemake setup configuration
    file."""

    def __init__(self, fieldpath: typing.List[str], msg: str):
        self.fieldpath = fieldpath

        super().__init__(
            "*template error:*",
            f"Under field {stringify_fieldpath(fieldpath)!r} - {msg}",
            raw_msg=msg,
        )


class litemakeConfigError(litemakeError):
    """Raised when there is an error in the litemake setup configuration
    file."""

    def __init__(self, filename: str, fieldpath: typing.List[str], msg: str):
        self.filename = filename
        self.fieldpath = fieldpath

        super().__init__(
            f"*configuration error in {filename!r}:*",
            f"Under field {stringify_fieldpath(fieldpath)!r} - {msg}",
            raw_msg=msg,
        )

    @classmethod
    def from_template_error(
        cls: T,
        filename: str,
        template: litemakeTemplateError,
    ) -> T:
        return cls(filename, template.fieldpath, template.raw_msg)


class litemakeParsingError(litemakeError):
    """Raised when the configuration file doesn't follow the TOML syntax
    specification and it can't be parsed correctly."""

    def __init__(self, filename: str, line: int, col: int, msg: str):
        super().__init__(
            f"*parsing error in {filename}:*",
            f"On line {line}, column {col} - {msg}",
            raw_msg=msg,
        )


class litemakeFileNotFoundError(litemakeError):
    """Raised if the default (`package.litemake.toml`) setup configuration
    file isn't present or if the custom file (specified with the -f/--flags
    arguments) isn't found."""

    def __init__(self, filename: str):
        super().__init__(f"*file {filename!r} not found*")


class litemakeCompilationError(litemakeError):
    """Raised by the 'compiler' object if when calling the compiler (gcc, g++,
    clang), it returned a non-zero code."""

    def __init__(self, subprocess: str, msg: str):
        super().__init__(
            f"*error while calling {subprocess!r}:*",
            msg,
        )


class litemakeUnknownTargetsError(litemakeError):
    """Raised by '__main__.py' if the user want to execute a target that is not
    specified in the configuration file."""

    def __init__(self, targets: typing.Set[str]):
        self.targets = targets

        title = "targets" if len(targets) > 1 else "target"
        targets_str = ", ".join(repr(t_) for t_ in targets)

        super().__init__(f"*unknown {title}:* {targets_str}")


class litemakePluginInitError(litemakeError):
    """Raised by the plugin collector when it stumbles upon a plugin that is
    not configured correctly and can't be initialized."""

    def __init__(self, name: str, msg: str, raw_msg: str = None) -> None:
        self.name = name
        super().__init__(
            f"*error while initializing plugin class {name!r}:*",
            msg,
            raw_msg=msg if raw_msg is None else raw_msg,
        )


class litemakePluginTemplateInitError(litemakePluginInitError):
    def __init__(self, name, fieldpath: typing.List[str], msg: str) -> None:
        self.fieldpath = fieldpath
        super().__init__(
            name,
            msg=f"Under field {stringify_fieldpath(fieldpath)!r} - {msg}",
            raw_msg=msg,
        )

    @classmethod
    def from_template_error(
        cls: T,
        name: str,
        template: litemakeTemplateError,
    ) -> T:
        return cls(name, template.fieldpath, template.raw_msg)


class litemakePluginInvalidHooks(litemakePluginInitError):
    def __init__(self, name: str, hooks: typing.Set[str]) -> None:
        self.hook_names = hooks

        hook_s = "hook" if len(hooks) < 2 else "hooks"
        super().__init__(
            name=name,
            msg=f"Invalid {hook_s}: {', '.join(repr(n) for n in hooks)}",
        )
