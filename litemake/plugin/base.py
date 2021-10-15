import typing

if typing.TYPE_CHECKING:
    from litemake.parse.templates import BaseTemplate

import inspect
from abc import ABC

from litemake.constants import NAME_CHARS, SPECIAL_CHARS
from litemake.parse.templates import Template
from litemake.parse.endpoints import StringTemplate
from litemake.exceptions import (
    litemakeTemplateError,
    litemakePluginInvalidHooks,
    litemakePluginTemplateInitError,
)


class litemakePlugin(ABC):

    _plugins: typing.List["litemakePlugin"] = list()

    def __init_subclass__(cls) -> None:
        litemakePlugin._plugins.append(cls)


class PluginValidator:

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

    VALID_HOOK_NAMES = {
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

    @classmethod
    def _validate_from_template(
        cls,
        plugin: "litemakePlugin",
        template: "BaseTemplate",
        data,
    ) -> None:
        try:
            template.validate(data, fieldpath=list())
        except litemakeTemplateError as err:
            raise litemakePluginTemplateInitError.from_template_error(
                name=plugin.__name__,
                template=err,
            ) from None

    @classmethod
    def validate(cls, plugin: typing.Type[litemakePlugin]) -> None:
        """Checks if the given plugin class is configured correctly, and raises
        an error if something is missing or configured incorrectly."""

        # validate plugin properties
        cls._validate_from_template(
            plugin=plugin,
            template=cls.PROPERTIES_TEMPLATE,
            data=cls._get_cls_properties(plugin),
        )

        cls._validate_hooks(plugin)

    @classmethod
    def _validate_hooks(cls, plugin: typing.Type[litemakePlugin]) -> None:

        hooks = cls._get_cls_methods(plugin)

        unknown = set(hooks) - cls.VALID_HOOK_NAMES
        if unknown:
            raise litemakePluginInvalidHooks(
                name=plugin.__name__,
                hooks=unknown,
            )

    @staticmethod
    def _get_cls_properties(cls) -> typing.Dict[str, typing.Any]:
        """Recives a class type, and returns a dictionary of (name, value) pairs
        that represent all public properties of the class."""

        return {
            name: value
            for name, value in inspect.getmembers(cls)
            if not name.startswith("_") and not inspect.isfunction(value)
        }

    @staticmethod
    def _get_cls_methods(cls) -> typing.Dict[str, typing.Callable]:
        """Recives a class type, and returns a dictionary of (name, value) pairs
        that represent all public properties of the class."""

        return {
            name: value
            for name, value in inspect.getmembers(cls)
            if not name.startswith("_") and inspect.isfunction(value)
        }
