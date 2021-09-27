import os

from .file import FileParser
from .templates import Template
from .endpoints import (
    FolderPathTemplate,
    CompilerTemplate,
)

import typing
if typing.TYPE_CHECKING:
    from litemake.compile.compilers.base import AbstractCompiler  # pragma: no cover


class SettingsParser(FileParser):

    TEMPLATE = Template(
        home=FolderPathTemplate(default=''),
        output=FolderPathTemplate(default='.litemake/'),
        compiler=CompilerTemplate(default='g++'),
    )

    @property
    def home(self,) -> str:
        """ The home directory in which litemake will run relative to.
        The current working directory by default. """
        path = self._data['home']

        if not path:
            return os.getcwd()

        if os.path.isabs(path):
            return path

        else:
            folder = os.path.dirname(self.filepath)
            return os.path.join(folder, path)

    @property
    def output(self,) -> str:
        """ The directory in which litemake will store all compiled objects,
        archives, source files of dependencies and all other files that are
        managed by litemake. """

        path = self._data['output']
        if os.path.isabs(path):
            return path
        else:
            folder = os.path.dirname(self.filepath)
            return os.path.join(folder, path)

    @property
    def compiler(self,) -> 'AbstractCompiler':
        """ A compiler instance that is used to compile different files
        in litemake. """
        return self._data['compiler']
