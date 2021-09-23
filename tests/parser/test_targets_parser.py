from litemake.parse import TargetsParser

import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


def test_target_names(project: 'VirtualProject'):
    path = project.add_setup('''
        [build]
        sources=["src/**/*.c"]

        [test]
        sources=["src/**/*.c", "tests/**/*.c"]
    ''')

    info = TargetsParser(path)
    assert info.targets == ['build', 'test']
    assert info.default_target == 'build'
