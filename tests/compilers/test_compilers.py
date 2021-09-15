import os
import typing
import subprocess
from shutil import which
from abc import ABC, abstractmethod

import pytest
from tests.utils import VirtualProject

from litemake.compile.compilers import (
    AbstractCompiler,
    Compiler,
    ClangCompiler,
    ClangplusplusCompiler,
    GccCompiler,
    GplusplusCompiler,
)


class _TestCompiler(ABC):

    @property
    @classmethod
    @abstractmethod
    def COMPILER(cls) -> AbstractCompiler:
        """ Returns an instance to the compiler that is currently being
        tested. This property should be overwritten using inheritance. """

    @staticmethod
    def _execute_binary(*cmd) -> typing.Tuple[int, str]:
        """ Executes the given binary file and returns the return code as an
        interger and the captured stdout stream, as a string. """

        result = subprocess.run(*cmd, capture_output=True, text=True)
        return result.returncode, result.stdout

    def test_c_hello_world(self, project: VirtualProject):
        """ A simple test that creates a file named 'main.c', and tries to
        compile it into an object file, then into an archive, and then into
        an executable using the supported compileres by litemake. """

        obj_src = project.add_file('main.c', '''
            #include <stdio.h>

            int main() {
                printf("Hello from litemake!\\n");
                return 0;
            };

        ''')

        obj_dest = os.path.join(project.basepath, 'main.o')
        self.COMPILER.create_obj(obj_src, obj_dest)

        arc_dest = os.path.join(project.basepath, 'main.a')
        self.COMPILER.create_archive(arc_dest, [obj_dest])

        out_dest = os.path.join(project.basepath, 'main.out')
        self.COMPILER.create_executable(out_dest, [obj_dest])

        code, out = self._execute_binary(out_dest)
        assert code == 0, "Compiled program crashed unexpectedly"
        assert out == 'Hello from litemake!\n', "Unexpected output from compiled program"


def required_clis_exists(compiler: AbstractCompiler) -> bool:
    """ Returns `True` only if the given compiler can and compile on the
    current machine. """
    clis = compiler.required_clis
    return all(which(cli) is not None for cli in clis)


def skip_if_missing_clis(compiler: AbstractCompiler):
    """ A simple decorator that uses the 'pytest.mark.skipif' decorator only
    if the given compiler can't run on this machine because there are required
    command line exectutable tools that aren't avaliable. """

    def decorator(func):
        dec = pytest.mark.skipif(
            not required_clis_exists(ClangplusplusCompiler),
            reason="Missing required CLIs",
        )
        return dec(func)
    return decorator


@skip_if_missing_clis(GccCompiler)
class TestGccCompiler(_TestCompiler):
    COMPILER = Compiler('gcc')


@skip_if_missing_clis(GplusplusCompiler)
class TestGplusplusCompiler(_TestCompiler):
    COMPILER = Compiler('g++')


@skip_if_missing_clis(ClangCompiler)
class TestClangCompiler(_TestCompiler):
    COMPILER = Compiler('clang')


@skip_if_missing_clis(ClangplusplusCompiler)
class TestClangplusplusCompiler(_TestCompiler):
    COMPILER = Compiler('clang++')
