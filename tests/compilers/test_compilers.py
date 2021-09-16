import os

import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject

from .base import _TestCompiler, skip_if_missing_clis

from litemake.compile.compilers import (
    Compiler,
    ClangCompiler,
    ClangplusplusCompiler,
    GccCompiler,
    GplusplusCompiler,
)


class _TestCompilerC(_TestCompiler):

    def test_c_hello_world(self, project: 'VirtualProject'):
        """ A simple test that creates a file named 'main.c', and tries to
        compile it into an object file, then into an archive, and then into
        an executable using the supported compileres by litemake. """

        src = project.add_file('main.c', '''
            #include <stdio.h>

            int main() {
                printf("Hello from litemake!\\n");
                return 0;
            };

        ''')

        obj_dest = os.path.join(project.basepath, 'main.o')
        self.COMPILER.create_obj(src, obj_dest)

        arc_dest = os.path.join(project.basepath, 'main.a')
        self.COMPILER.create_archive(arc_dest, [obj_dest])

        out_dest = os.path.join(project.basepath, 'main.out')
        self.COMPILER.create_executable(out_dest, [obj_dest])

        out = self._execute_binary(out_dest)
        assert out == 'Hello from litemake!\n'


class _TestCompilerCPP(_TestCompilerC):

    def test_cpp_hello_world(self, project: 'VirtualProject'):
        src = project.add_file('main.cpp', '''
            #include <iostream>
            
            int main() {
                std::cout << "Hello from litemake!" << std::endl;
            }

        ''')

        obj_dest = os.path.join(project.basepath, 'main.o')
        self.COMPILER.create_obj(src, obj_dest)

        arc_dest = os.path.join(project.basepath, 'main.a')
        self.COMPILER.create_archive(arc_dest, [obj_dest])

        out_dest = os.path.join(project.basepath, 'main.out')
        self.COMPILER.create_executable(out_dest, [obj_dest])

        out = self._execute_binary(out_dest)
        assert out == 'Hello from litemake!\n'


@skip_if_missing_clis(GccCompiler)
class TestGccCompiler(_TestCompilerC):
    COMPILER = Compiler('gcc')


@skip_if_missing_clis(GplusplusCompiler)
class TestGplusplusCompiler(_TestCompilerCPP):
    COMPILER = Compiler('g++')


@skip_if_missing_clis(ClangCompiler)
class TestClangCompiler(_TestCompilerC):
    COMPILER = Compiler('clang')


@skip_if_missing_clis(ClangplusplusCompiler)
class TestClangplusplusCompiler(_TestCompilerCPP):
    COMPILER = Compiler('clang++')
