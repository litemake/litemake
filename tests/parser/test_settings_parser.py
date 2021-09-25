import os
from litemake.parse import SettingsParser


import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


def test_default_settings(project: 'VirtualProject'):
    # All settings should be provided by default, and using the settings
    # file shouldn't be mandetory.

    path = project.add_settings_file('')  # empty settings file
    info = SettingsParser(path)
    assert info.home == os.getcwd()
    assert info.output == os.path.join(project.basepath, '.litemake/')
    assert info.compiler.name == 'g++'


def test_absolute_paths(project: 'VirtualProject'):
    src = project.add_dir('src/')
    out = project.add_dir('.litemake_cache/')

    path = project.add_settings_file(f'''
        home='{src}'
        output='{out}'
    ''')

    info = SettingsParser(path)
    assert info.home == src
    assert info.output == out


def test_relative_paths(project: 'VirtualProject'):
    src = project.add_dir('src/')
    out = project.add_dir('.litemake_cache/')

    path = project.add_settings_file('''
        home="src/"
        output=".litemake_cache/"
    ''')

    info = SettingsParser(path)
    assert info.home == src
    assert info.output == out
