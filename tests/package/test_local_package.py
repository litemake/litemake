import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject

from litemake.package import LocalPackage


def test_basic_local_package_properties(project: 'VirtualProject'):
    project.add_setup('''
        [metadata]
        name="testing"

        [target.build]
        sources=["*.c"]
    ''')

    package = LocalPackage(basedir=project.basepath)
    assert package.name == 'testing'
    assert package.version == (0, 0, 0)
    assert package.author is None
    assert package.description is None
    assert package.version_label is None
    assert package.identifier == 'testing-v0.0.0'


def test_local_package_custom_version(project: 'VirtualProject'):
    project.add_setup('''
        [metadata]
        name="testing"

        [metadata.version]
        major=1
        minor=2
        patch=3
        label="dev"

        [target.build]
        sources=["*.cpp"]
    ''')

    package = LocalPackage(basedir=project.basepath)
    assert package.version == (1, 2, 3)
    assert package.version_label == 'dev'
    assert package.identifier == 'testing-v1.2.3-dev'
