from litemake.__main__ import parser, make
import litemake.exceptions

from inspect import cleandoc
import os.path


class VirtualProject:
    """ An objects that represents a virtual testing folder. This folder can be
    accessed by the 'project' fixture, and it is unique for each new test. """

    def __init__(self, name: str, basepath: str):
        self.name = name
        self.basepath = basepath

    def add_file(self, path: str, content: str) -> str:
        assert not os.path.isabs(path), "relative path is required"
        path = os.path.join(self.basepath, path)

        # Create folders (recursively) on path to file
        dirpath = os.path.dirname(path)
        os.makedirs(dirpath, exist_ok=True)

        # Write content to file
        with open(path, 'w', encoding='utf8') as file:
            file.write(cleandoc(content))

        # return path to new created file
        return path

    def add_dir(self, path: str) -> str:
        assert not os.path.isabs(path), "relative path is required"
        dirpath = os.path.join(self.basepath, path)
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    def add_setup(self, content: str, path: str = None) -> str:
        path = path or litemake.constants.DEFAULT_SETUP_FILENAME
        return self.add_file(path, content)

    def make(self, *args):
        # By default, the virtual project class adds the '-d' argument
        # to run litemake inside the virtual project directory.
        args = ('-d', self.basepath) + args
        return make(parser.parse_args(args))
