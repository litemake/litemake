import pytest
from litemake.parse import PackageParser
from litemake.package import PackageInfo
from litemake.exceptions import litemakeConfigError

import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


def test_basic_package_info(project: 'VirtualProject'):
    path = project.add_setup('''
        name="testing"
    ''')

    info = PackageParser(path)
    assert info.name == 'testing'
    assert info.version == (0, 0, 0)
    assert info.author is None
    assert info.description is None
    assert info.version_label is None
    assert info.identifier == 'testing-v0.0.0'


def test_package_custom_version(project: 'VirtualProject'):
    path = project.add_setup('''
        name="testing"
        
        [version]
        major=1
        minor=2
        patch=3
        label="dev"
    ''')

    info = PackageParser(path)
    assert info.version == (1, 2, 3)
    assert info.version_label == 'dev'
    assert info.identifier == 'testing-v1.2.3-dev'


@pytest.mark.parametrize('name', (
    'שלוםעולם',
    'Hello world',
    'ThisNameIsWayyyyyTooooooooLonggggg',
    'InvalidChar!',
    'Two__RepeatingChars',
    'Yes_',
    'Hello..There',
))
def test_package_invalid_names(name, project: 'VirtualProject'):
    path = project.add_setup(f'''
        name="{name}"
    ''')

    with pytest.raises(litemakeConfigError):
        PackageParser(path)
