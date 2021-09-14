import pytest
from .conftest import VirtualProject

from litemake import exceptions


def matching_msg(expected: str, got: str) -> bool:
    expected, got = expected.lower(), got.lower()
    return got in expected


def test_setup_file_not_found_error(project: VirtualProject):
    """ Creates a new empty project, and tried to run litemake in it.
    Litemake is expected to raise an error: a setup file isn't found! """

    with pytest.raises(exceptions.litemakeSetupFileNotFoundError):
        project.make()


def test_minimal_setup_file(project: VirtualProject):
    """ Creates a minimal project setup file in an empty project directory,
    and tests that litemake is able to run. """

    project.add_setup(
        '''
        [litemake.meta]
        name="testing"
        standard="c++17"

        [target.build]
        sources=["src/**/*.cpp"]
        '''
    )

    project.make()


def test_missing_name(project: VirtualProject):
    """ Tests if an appropriate error message is provided when the setup file
    is missing the 'litemake.meta.name' field. """

    project.add_setup(
        '''
        [litemake.meta]
        standard="c++17"

        [target.build]
        sources=["src/**/*.cpp"]
        '''
    )

    with pytest.raises(exceptions.litemakeConfigError) as err:
        project.make()

    assert err.value.fieldpath == ['litemake', 'meta', 'name']
    assert matching_msg('missing required field', err.value.raw_msg)
