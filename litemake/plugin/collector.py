from .validator import PluginValidator
from .manager import litemakePluginManager

import typing

T = typing.TypeVar("T")


class litemakePluginCollector:
    def __init__(self):
        self._plugins = list()

    def collect(self, cls: T) -> T:
        PluginValidator.validate(cls)
        self._plugins.append(cls)
        return cls

    def initialize(self) -> litemakePluginManager:
        instances = [plug() for plug in self._plugins]
        return litemakePluginManager(*instances)
