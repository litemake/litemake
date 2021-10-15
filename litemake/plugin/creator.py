import inspect

from litemake.constants import NAME_CHARS, SPECIAL_CHARS
from litemake.parse.templates import Template
from litemake.parse.endpoints import StringTemplate
from litemake.exceptions import (
    litemakeTemplateError,
    litemakePluginInitError,
    litemakePluginInvalidHooksError,
)

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
        self.__hooks = dict()

    def __getattr__(self, name: str):
        if name not in self.__hooks:
            self.__hooks[name] = FuncWrapper()
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


class litemakePluginCreator(PluginCreator):
    """A plugin creator that has the ability to store additional information
    about the plugin (his name, description, etc). Also validates that the
    provided hook functions are valid, and raises a litemakePluginInitError if
    something goes wrong while initializing a plugin."""

    PROPERTIES_TEMPLATE = Template(
        name=StringTemplate(
            min_len=3,
            max_len=30,
            allowed_chars=NAME_CHARS,
            no_repeating=SPECIAL_CHARS,
            no_on_edges=SPECIAL_CHARS,
        ),
        description=StringTemplate(max_len=200, default=str()),
    )

    # A list of valid hook names, under the 'self.hooks' property.
    # Will throw an error when trying to set other unknown hooks!
    VALID_HOOK_NAMES = {
        # general
        "setup",
        "teardown",
        # node collection
        "before_node_collection",
        "after_collecting_node",
        "after_node_collection",
        # node compilation
        "before_node_compilation",
        "before_compiling_node",
        "after_compiling_node",
        "after_node_compilation",
    }

    def __init__(self: T, register: typing.Callable[[T], None]):
        super().__init__(register)
        self._info = dict()

    # - - - Property getters and setters - - - #

    def __setattr__(self, name: str, value) -> None:
        if name.startswith("_"):
            return super().__setattr__(name, value)
        else:
            self._info[name] = value

    def __getattr__(self, name: str):
        if name.startswith("_"):
            return super().__getattr__(name)
        else:
            return self._info[name]

    # - - - validators - - - #

    def _validate_info(self) -> None:
        try:
            self.PROPERTIES_TEMPLATE.validate(self._info, fieldpath=list())

        except litemakeTemplateError as err:
            # Raise the template error as a custom plugin initialization error.
            caller = inspect.stack()[1]
            module = inspect.getmodule(caller[0])
            filename = module.__file__
            raise litemakePluginInitError.from_template_error(filename, err) from None

    def _validate_hooks(self) -> None:
        unknown = set(self._hooks) - self.VALID_HOOK_NAMES
        if unknown:
            raise litemakePluginInvalidHooksError(self.name, unknown)

    def __exit__(self, *_) -> None:
        """When exiting the 'with' scope, the data will be validated an errors
        will be raised if the given data is invalid. Finally, if the data IS
        valid, the register function will be called and this instance will be
        passed as the only argument."""

        self._validate_info()
        self._validate_hooks()
        self._register(self)
