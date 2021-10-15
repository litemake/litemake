import pytest

from litemake.plugin.base import litemakePlugin, PluginValidator
from litemake.exceptions import litemakePluginInitError


def test_empty_plugin():
    class MyPlugin(litemakePlugin):
        pass

    with pytest.raises(litemakePluginInitError) as err:
        PluginValidator.validate(MyPlugin)

    assert err.value.name == "MyPlugin"
    assert err.value.fieldpath == ["name"]
    assert err.value.raw_msg == "Missing required field"


def test_no_hooks_plugin():
    class MyPlugin(litemakePlugin):
        name = "my-plugin"
        description = "A plugin created for testing only!"

    PluginValidator.validate(MyPlugin)  # doesn't raise an error


def test_invalid_hook():
    class MyPlugin(litemakePlugin):
        name = "my-plugin"

        def hello_there(self) -> None:
            raise NotImplementedError

    with pytest.raises(litemakePluginInitError) as err:
        PluginValidator.validate(MyPlugin)

    assert err.value.hook_names == {"hello_there"}
    assert err.value.name == "MyPlugin"
    assert err.value.raw_msg == "Invalid hook: 'hello_there'"


def test_valid_plugin():
    class MyPlugin(litemakePlugin):
        name = "my-plugin"
        description = "this is my description!"

    PluginValidator.validate(MyPlugin)


def test_all_hooks_plugin():
    class MyPlugin(litemakePlugin):
        name = "my-plugin"

        # fmt: off
        def before_node_collection(self): pass
        def after_collecting_node(self): pass
        def after_node_collection(self): pass
        def before_node_compilation(self): pass
        def before_compiling_node(self): pass
        def after_compiling_node(self): pass
        def after_node_compilation(self): pass
        # fmt: on

    PluginValidator.validate(MyPlugin)
