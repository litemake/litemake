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

    def add_file(self, path: str, content: str) -> None:
        assert not os.path.isabs(path), "A relative path isn't allowed here"
        path = os.path.join(self.basepath, path)

        with open(path, 'w', encoding='utf8') as file:
            file.write(cleandoc(content))

    def add_setup(self, content: str, path: str = None):
        path = path or litemake.constants.DEFAULT_SETUP_FILENAME
        self.add_file(path, content)

    def make(self, *args):
        # By default, the virtual project class adds the '-d' argument
        # to run litemake inside the virtual project directory.
        args = ('-d', self.basepath) + args
        return make(parser.parse_args(args))
