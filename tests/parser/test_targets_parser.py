from litemake.parse import TargetsParser

import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


def test_target_names(project: 'VirtualProject'):
    path = project.add_setup('''
        [build]
        library=true
        sources=["src/**/*.c"]
        include=["include/"]

        [test]
        sources=["src/**/*.c", "tests/**/*.c"]
    ''')

    info = TargetsParser(path)
    assert info.targets == ['build', 'test']
    assert info.default_target == 'build'

    build = info.target('build')
    assert build.library
    assert build.name == 'build'
    assert build.sources == ['src/**/*.c']
    assert build.include == ['include/']

    test = info.target('test')
    assert test.name == 'test'
    assert not test.library
    assert test.sources == ['src/**/*.c', 'tests/**/*.c']
    assert test.include == []
