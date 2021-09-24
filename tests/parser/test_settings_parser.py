import os
from litemake.parse import SettingsParser


import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


def test_default_settings(project: 'VirtualProject'):
    # All settings should be provided by default, and using the settings
    # file shouldn't be mandetory.

    path = project.add_setup('')  # empty settings file
    info = SettingsParser(path)
    assert info.home == os.getcwd()
    assert info.output == os.path.join(os.getcwd(), '.litemake/')
    assert info.compiler.name == 'g++'
