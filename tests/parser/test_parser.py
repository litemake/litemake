import os

import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject

from litemake.parse import SetupConfigParser


def test_default_setup(project: 'VirtualProject'):
    """ Tests that a minimal setup file, with a lot of default configurations,
    is parser as expected, and all defaults are loaded currently. """

    setup = project.add_setup('''
        [litemake.meta]
        name="testing"
        standard="c++17"
        [target.default]
    ''')

    parser = SetupConfigParser(setup)

    assert parser.filepath == setup
    assert parser.homepath == os.getcwd()
    assert parser.package_name == 'testing'
    assert parser.package_description == ''
    assert parser.package_author == ''
    assert parser.package_version == (0, 0, 0, '')
    assert parser.target_names == {'default'}
