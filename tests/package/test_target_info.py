import pytest
from litemake.package import TargetInfo
from litemake.exceptions import litemakeTemplateError


def test_empty_target():
    # Each target requires at least one source glob.
    with pytest.raises(litemakeTemplateError):
        TargetInfo('TargetName', data=dict(), fieldpath=list())


def test_basic_target():
    TargetInfo('test', data={'sources': ['*.c']}, fieldpath=list())
