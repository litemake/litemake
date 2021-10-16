from litemake.plugin.hook import Hook


def test_no_funcs_hook():
    hook = Hook()
    value = list(hook())
    assert value == list()


def test_lambdas_hook():
    hook = Hook(
        lambda: 1,
        lambda: 2,
        lambda: "hi!",
    )

    values = tuple(hook())
    assert values == (1, 2, "hi!")


def test_param_hooks():
    def hello(name: str) -> str:
        return f"hello {name}!"

    def goodbye(name: str) -> str:
        return f"goodbye {name}..."

    hook = Hook(hello, goodbye)
    values = tuple(hook("litemake"))
    assert values == ("hello litemake!", "goodbye litemake...")


def test_hooks_params_not_by_ref():
    def pop_first(values: list):
        values.pop(0)
        return values

    def pop_last(values: list):
        values.pop(-1)
        return values

    hook = Hook(pop_first, pop_last)

    values = [1, 2, 3]
    returned = tuple(hook(values))

    assert returned[0] == [2, 3]
    assert returned[1] == [1, 2]
    assert values == [1, 2, 3]
