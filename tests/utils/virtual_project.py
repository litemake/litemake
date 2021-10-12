import os
import typing
from inspect import cleandoc

import tests.utils

from litemake.__main__ import make
from litemake.constants import (
    PACKAGE_CONFIG_FILENAME,
    TARGETS_CONFIG_FILENAME,
    SETTINGS_FILENAME,
)


class VirtualProject:
    """An objects that represents a virtual testing folder. This folder can be
    accessed by the 'project' fixture, and it is unique for each new test."""

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
        with open(path, "w", encoding="utf8") as file:
            file.write(cleandoc(content))

        # return path to new created file
        return path

    def add_dir(self, path: str) -> str:
        assert not os.path.isabs(path), "relative path is required"
        dirpath = os.path.join(self.basepath, path)
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    def add_targets_file(self, content: str, path: str = None) -> str:
        path = path or TARGETS_CONFIG_FILENAME
        return self.add_file(path, content)

    def add_package_file(self, content: str, path: str = None) -> str:
        path = path or PACKAGE_CONFIG_FILENAME
        return self.add_file(path, content)

    def add_settings_file(self, content: str, path: str = None) -> str:
        path = path or SETTINGS_FILENAME
        return self.add_file(path, content)

    def join(self, *paths) -> str:
        return os.path.join(self.basepath, *paths)

    def run(self, *targets: typing) -> None:
        with tests.utils.change_cwd(self.basepath):
            make(*targets)
