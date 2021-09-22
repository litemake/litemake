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
