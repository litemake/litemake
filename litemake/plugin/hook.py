import typing
from copy import deepcopy


class Hook:
    """A class that groups the execution of a collection of functions, and
    executes them together, when requested. Functions to be executed are passed
    to the __init__ method of this class, and executing those functions can be
    done using the __call__ method of the Hook class."""

    def __init__(self, *funcs: typing.List[typing.Callable]):
        self._funcs = funcs

    def __call__(self, *args, **kwargs):
        for func in self._funcs:
            yield func(*deepcopy(args), **deepcopy(kwargs))
