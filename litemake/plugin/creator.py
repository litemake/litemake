from collections import defaultdict

import typing

T = typing.TypeVar("T", bound="PluginCreator")


class PluginCreator:
    """A wrapper of the creation process of a third-party litemake plugin.
    Instances of this class shouldn't be created directly, and you should
    use the 'create_plugin' function. For more information, read the third-party
    plugins API documentation."""

    def __init__(self: T, register: typing.Callable[[T], None]):
        self._register = register
        self._hooks = HooksCollection()

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, *_) -> None:
        self._register(self)

    @property
    def hooks(self) -> "HooksCollection":
        return self._hooks


class HooksCollection:
    """A wrapper of a dictionary of functions. Each function as a name, and
    can be accessed using the __getattr__ method (or the self.<name> syntax).
    By accessing (calling) the __getattr__ method, a new FuncWrapper instance
    is created implicitly."""

    def __init__(self) -> None:
        self.__hooks = defaultdict(FuncWrapper)

    def __getattr__(self, name: str):
        return self.__hooks[name]

    def __repr__(self):
        return f"<HooksCollection {dict(self.__hooks)!r}>"  # pragma: no cover

    def __iter__(self):
        return iter(
            # hook names that have assigned functions to them
            name
            for name in self.__hooks
            if self.__hooks[name].func is not None
        )


class FuncWrapper:
    """A wrapper for a basic function. Calling the __call__ method on an
    instance of this objects is designed to behave like a decorator: It the
    call method recives a single argument, and expects it to be a function.
    Calling the __call__ method will save the decoratoed function under the
    'func' property."""

    def __init__(self):
        self.__func = None

    def __call__(self, func) -> None:
        self.__func = func

    @property
    def func(self) -> typing.Callable:
        return self.__func

    def __repr__(self) -> str:
        return f"<FuncWrapper of {self.__func!r}>"  # pragma: no cover
