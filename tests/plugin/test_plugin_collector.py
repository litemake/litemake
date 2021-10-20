import pytest

from litemake.plugin.collector import litemakePluginCollector
from litemake.exceptions import (
    litemakePluginTemplateInitError,
    litemakePluginInvalidHooks,
)


@pytest.fixture
def plugins():
    return litemakePluginCollector()


def test_collect_single_plugin(plugins):
    @plugins.collect
    class MyPlugin:
        name = "my-testing-plugin"
        description = "This is a simple plugin."

        def before_compiling_node(self):
            raise NotImplementedError

        def after_compiling_node(self):
            raise self._private_method_that_should_work()

        def _private_method_isnt_a_hook(self):
            raise NotImplementedError


def test_collect_no_name_plugin(plugins):
    with pytest.raises(litemakePluginTemplateInitError) as err:

        @plugins.collect
        class MyPlugin:
            def before_compiling_node(self):
                raise NotImplementedError

    assert err.value.raw_msg == "Missing required field"
    assert err.value.fieldpath == ["name"]


def test_collect_invalid_plugin_hooks(plugins):
    with pytest.raises(litemakePluginInvalidHooks) as err:

        @plugins.collect
        class MyPlugin:
            name = "my-plugin"

            def not_a_hook(self):
                raise NotImplementedError

    assert err.value.raw_msg == "Invalid hook: 'not_a_hook'"
    assert err.value.hook_names == {"not_a_hook"}
