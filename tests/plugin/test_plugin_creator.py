from litemake.plugin.creator import PluginCreator

import pytest

from types import FunctionType


def test_basic_plugin_creation():
    def register(plugin):

        with pytest.raises(NotImplementedError):
            plugin.hooks.notimplemented.func()

        assert isinstance(plugin.hooks.nothing.func, FunctionType)
        assert plugin.hooks.notprovided.func is None
        assert set(plugin.hooks) == {"nothing", "notimplemented"}

    with PluginCreator(register) as plugin:

        @plugin.hooks.nothing
        def nothing_hook():
            pass

        @plugin.hooks.notimplemented
        def not_implemented_hook():
            raise NotImplementedError


def test_empty_plugin():
    def register(plugin):
        assert set(plugin.hooks) == set()

    with PluginCreator(register) as _:
        pass  # don't do a thing with the plugin!
