import pytest
from litemake.package import TargetInfo
from litemake.exceptions import litemakeTemplateError


def test_empty_target():
    """ Test the case when no data is provided. An error should be raised. """

    # Each target requires at least one source glob.
    with pytest.raises(litemakeTemplateError):
        TargetInfo('TargetName', data=dict(), fieldpath=list())


def test_basic_target():
    """ Test the simplest case of the target, when only a single source is
    provided. """

    info = TargetInfo('test', data={'sources': ['*.c']}, fieldpath=list())

    assert info.name == 'test'
    assert info.sources == ['*.c']
    assert not info.is_library
    assert info.include == list()


def test_full_target():
    """ Test input and expected output of when all properties of target are
    provided in the constructor. """

    info = TargetInfo('test', fieldpath=list(), data={
        'library': True,
        'sources': ['*.c', 'src/**/*.c'],
        'include': ['include/'],
    })

    assert info.name == 'test'
    assert info.is_library
    assert info.sources == ['*.c', 'src/**/*.c']
    assert info.include == ['include/']
