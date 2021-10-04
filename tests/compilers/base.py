import subprocess
from shutil import which
from abc import ABC, abstractmethod

import pytest

import typing
if typing.TYPE_CHECKING:
    from litemake.compile.compilers import AbstractCompiler  # pragma: no cover


class _TestCompiler(ABC):

    @property
    @classmethod
    @abstractmethod
    def COMPILER(cls) -> 'AbstractCompiler':
        """ Returns an instance to the compiler that is currently being
        tested. This property should be overwritten using inheritance. """

    @staticmethod
    def _execute_binary(*cmd) -> str:
        """ Executes the given binary file. Asserts that the return code is
        zero, and returns the captured stdout stream, as a string. """

        result = subprocess.run(
            *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0, "Return code of compiled program isn't 0"
        return result.stdout


def required_clis_exists(compiler: 'AbstractCompiler') -> bool:
    """ Returns `True` only if the given compiler can and compile on the
    current machine. """
    clis = compiler.required_clis
    return all(which(cli) is not None for cli in clis)


def skip_if_missing_clis(compiler: 'AbstractCompiler'):
    """ A simple decorator that uses the 'pytest.mark.skipif' decorator only
    if the given compiler can't run on this machine because there are required
    command line exectutable tools that aren't avaliable. """

    def decorator(func):
        dec = pytest.mark.skipif(
            not required_clis_exists(compiler),
            reason="Missing required CLIs",
        )
        return dec(func)
    return decorator
