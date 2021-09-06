''' make.py - nanomake - Alon Krymgand Osovsky (2021)

    In this file, we contain the implementation of tools similar to the GNU
    Make tool. Using this, we can detect files that have been changed since
    the last 'nanomake' call, and recompile only them.
'''

import typing
from os import path, listdir
from abc import ABC, abstractmethod


class Make(ABC):

    def __init__(self, input: str, output: str):
        self.input = input
        self.output = output


class MakeFile(Make):

    def __init__(self, input: str, output: str):
        super().__init__(input, output)
        assert path.isfile(input)

    def needs_update(self,) -> bool:
        """ Returns `True` only if the output file is more up to date then
        the output file. If the output file doesn't exist, returns `True`.
        If `True`, the input files needs to be updated and recompiled! """

        if not path.exists(self.input):
            return True

        return path.getmtime(self.input) > path.getmtime(self.output)


class MakeFolder(Make):

    def __init__(self, input: str, output: str) -> None:
        super().__init__(input, output)
        assert path.isdir(input)
        self.children = set(self._get_children())

    def _get_children(self,):

        for cur_in in listdir(self.input):
            cur_out = path.join(self.output, path.basename(cur_in))

            if cur_in.is_dir():
                yield MakeFolder(cur_in, cur_out)

            elif cur_in.is_file():
                yield MakeFile(cur_in, cur_out)

    def needs_update(self,):
        """ A generator that yields `MakeFile` instances that are located
        in under this `MakeFolder` instance (recursive). The yielded files
        need to be updated. """

        for child in self.children:
            if isinstance(child, MakeFile):
                if child.needs_update():
                    yield child

            elif isinstance(child, MakeFolder):
                yield from child.needs_update()
