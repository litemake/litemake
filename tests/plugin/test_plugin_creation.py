import pytest

from litemake.plugin.base import litemakePlugin, PluginValidator
from litemake.exceptions import litemakePluginInitError


def test_empty_plugin():
    class MyPlugin(litemakePlugin):
        pass

    with pytest.raises(litemakePluginInitError) as err:
        PluginValidator.validate(MyPlugin)

    assert err.value.fieldpath == ["name"]
    assert err.value.raw_msg == "Missing required field"


def test_no_hooks_plugin():
    class MyPlugin(litemakePlugin):
        name = "my-plugin"
        description = "A plugin created for testing only!"

    PluginValidator.validate(MyPlugin)  # doesn't raise an error
