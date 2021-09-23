import os
from tests.utils import change_cwd
from litemake.parse import SettingsParser


import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


def test_default_settings(project: 'VirtualProject'):
    # All settings should be provided by default, and using the settings
    # file shouldn't be mandetory.

    path = project.add_setup('')  # empty settings file

    with change_cwd(project.basepath):
        info = SettingsParser(path)
        assert info.home == project.basepath
        assert info.output == os.path.join(project.basepath, '.litemake/')
        assert info.compiler.name == 'g++'
