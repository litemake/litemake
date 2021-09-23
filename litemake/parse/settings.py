import os

from .file import FileParser
from .templates import Template
from .endpoints import (
    FolderPathTemplate,
    CompilerTemplate,
)

import typing
if typing.TYPE_CHECKING:
    from litemake.compile.compilers.base import AbstractCompiler


class SettingsParser(FileParser):

    TEMPLATE = Template(
        home=FolderPathTemplate(must_exist=True, default='/'),
        output=FolderPathTemplate(default='.litemake/'),
        compiler=CompilerTemplate(default='g++'),
    )

    @property
    def home(self,) -> str:
        """ The home directory in which litemake will run relative to.
        The current working directory by default. """
        data = self._data['home']
        return os.getcwd() if data == '/' else data

    @property
    def output(self,) -> str:
        """ The directory in which litemake will store all compiled objects,
        archives, source files of dependencies and all other files that are
        managed by litemake. """

        path = self._data['output']
        if os.path.isabs(path):
            return path
        else:
            return os.path.join(self.home, path)

    @property
    def compiler(self,) -> 'AbstractCompiler':
        """ A compiler instance that is used to compile different files
        in litemake. """
        return self._data['compiler']
