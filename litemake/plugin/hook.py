from abc import ABC, abstractmethod


class Hook(ABC):
    def __init__(self, *funcs):
        self._registered = funcs

    def __call__(self, *args, **kwargs):
        """When treating a hook instance as a function and trying to "call it"
        using the 'hook()' syntax, all registered hook triggers will be
        executed."""

        return self._run(*args, **kwargs)

    @abstractmethod
    def _run(self, *args, **kwargs):
        """A method that uses the list of registered functions and calls
        them. The use of the returned values etc is defined in this abstract
        method."""


class VoidHook(Hook):
    """A basic hook that doesn't return a value. When calling the run function,
    it just calls the registered functions in the order they have been registered,
    one by one."""

    def _run(self, *args, **kwargs):
        for func in self._registered:
            func(*args, **kwargs)


class GatherHook(Hook):
    """Returns a generator that yields return values from the hooks, for
    each registered hook function."""

    def _run(self, *args, **kwargs):
        return (func(*args, **kwargs) for func in self._registered)


class UpdateHook(Hook):
    """The run function recives a single value. The value is passed as an
    argument to the first hook function, and it gets updated with the return
    value from the hook. The second hook function gets called with the return
    value from the first hook, etc. The returned value from the run function
    is the returned value from the last hook function."""

    def _run(self, val):
        for func in self._registered:
            val = func(val)
        return val
