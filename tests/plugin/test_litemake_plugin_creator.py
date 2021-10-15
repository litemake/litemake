import pytest
from litemake.plugin.creator import litemakePluginCreator
from litemake.exceptions import (
    litemakePluginInitError,
    litemakePluginInvalidHooksError,
)


def test_valid_litemake_plugin_creation():
    def register(plugin: litemakePluginCreator):
        assert plugin.name == "plugin123"
        assert plugin.description == "a simple plugin that does nothing!"

        with pytest.raises(NotImplementedError):
            plugin.hooks.setup.func()

    with litemakePluginCreator(register) as plugin:
        plugin.name = "plugin123"
        plugin.description = "a simple plugin that does nothing!"

        @plugin.hooks.setup
        def setup():
            raise NotImplementedError


def test_no_plugin_info_provided():
    def register(*_, **__):
        raise NotImplementedError

    with pytest.raises(litemakePluginInitError) as err:
        with litemakePluginCreator(register) as plugin:

            @plugin.hooks.setup
            def setup():
                raise NotImplementedError

    assert err.value.fieldpath == ["name"]
    assert err.value.raw_msg == "Missing required field"


def test_very_long_plugin_name():
    def register(*_, **__):
        raise NotImplementedError

    with pytest.raises(litemakePluginInitError) as err:
        with litemakePluginCreator(register) as plugin:
            plugin.name = "a-very-long-plugin-name-that-is-not-allowed"

    assert err.value.raw_msg == "Max length allowed is 30 (not 43)"
    assert err.value.fieldpath == ["name"]


def test_invalid_plugin_hooks():
    def register(*_, **__):
        raise NotImplementedError

    with pytest.raises(litemakePluginInvalidHooksError) as err:
        with litemakePluginCreator(register) as plugin:
            plugin.name = "test"

            @plugin.hooks.setup
            def valid_hook():
                print("hello!")

            @plugin.hooks.invalid
            def invalid_hook():
                print("oh no!")

    assert err.value.name == "test"
    assert err.value.hooks == {"invalid"}
    assert err.value.raw_msg == "Provided invalid hook: 'invalid'"
