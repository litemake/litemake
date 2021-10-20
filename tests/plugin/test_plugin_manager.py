import pytest

from litemake.plugin.manager import litemakePluginManager


@pytest.fixture
def log():
    return list()


def test_two_plugins_same_call(log):
    class FirstPlugin:
        def call(self, msg: str):
            print(f"FirstPlugin: {msg}")
            log.append(f"FirstPlugin: {msg}")

    class SecondPlugin:
        def call(self, msg: str):
            print(f"SecondPlugin: {msg}")
            log.append(f"SecondPlugin: {msg}")

    manager = litemakePluginManager(FirstPlugin(), SecondPlugin())

    # Generate all values from generator by spilling them into a tuple
    tuple(manager.call("hello"))
    tuple(manager.call("goodbye"))

    assert log == [
        "FirstPlugin: hello",
        "SecondPlugin: hello",
        "FirstPlugin: goodbye",
        "SecondPlugin: goodbye",
    ]


def test_missing_hooks_in_some_plugins(log):
    class FirstPlugin:
        def hello(self, name):
            msg = f"hello, {name}!"
            log.append(msg)
            return msg

    class SecondPlugin:
        def goodbye(self, name):
            msg = f"goodbye, {name} ):"
            log.append(msg)
            return msg

    manager = litemakePluginManager(FirstPlugin(), SecondPlugin())

    assert tuple(manager.hello("litemake")) == ("hello, litemake!",)
    assert tuple(manager.goodbye("litemake")) == ("goodbye, litemake ):",)
    assert tuple(manager.missing()) == tuple()

    assert log == ["hello, litemake!", "goodbye, litemake ):"]
