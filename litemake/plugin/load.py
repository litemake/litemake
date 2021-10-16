import pkg_resources

from .collector import litemakePluginCollector
from litemake.constants import PLUGINS_ENTRY_POINT

import typing

if typing.TYPE_CHECKING:
    from .manager import litemakePluginManager


def load_plugins() -> "litemakePluginManager":
    """A function that collects all avaliable plugins on this machine using the
    litemake entry point, validates that the plugins are configured correctly,
    and returns a 'litemakePluginManager' instance that contains and wraps all
    plugins. If something goes wrong, raises a PluginInitError."""

    collector = litemakePluginCollector()
    for entry in pkg_resources.iter_entry_points(PLUGINS_ENTRY_POINT):
        collector.collect(entry.load())

    return collector.initialize()
