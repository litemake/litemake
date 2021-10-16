from litemake.plugin.hook import VoidHook, GatherHook, UpdateHook


def test_void_hook():
    out = list()

    def add(a, b):
        out.append(a + b)

    def sub(a, b):
        out.append(a - b)

    hook = VoidHook(add, sub)

    rv = hook(1, 2)
    assert rv is None
    assert out == [3, -1]


def test_gather_hook():
    def first():
        return 1

    def second():
        return 2

    hook = GatherHook(first, second, lambda: 3)
    assert list(hook()) == [1, 2, 3]


def test_update_hook():
    def hello(s):
        return s + "Hello"

    def world(s):
        return s + ", world!"

    hook = UpdateHook(hello, world)
    assert hook(str()) == "Hello, world!"
    assert hook("Hello, ") == "Hello, Hello, world!"
