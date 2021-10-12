from litemake.plugin.hook import VoidHook, GatherHook, UpdateHook


def test_void_hook():
    hook, run = VoidHook()
    out = list()

    @hook
    def add(a, b):
        out.append(a + b)

    @hook
    def sub(a, b):
        out.append(a - b)

    rv = run(1, 2)
    assert rv is None
    assert out == [3, -1]


def test_gather_hook():
    hook, run = GatherHook()

    @hook
    def first():
        return 1

    @hook
    def second():
        return 2

    hook(lambda: 3)

    assert list(run()) == [1, 2, 3]


def test_update_hook():
    hook, run = UpdateHook()

    @hook
    def hello(s):
        return s + "Hello"

    @hook
    def world(s):
        return s + ", world!"

    assert run(str()) == "Hello, world!"
    assert run("Hello, ") == "Hello, Hello, world!"
