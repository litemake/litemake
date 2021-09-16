import os

from tests.utils import change_cwd

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

        main_o = os.path.join(project.basepath, 'main.o')
        main_a = os.path.join(project.basepath, 'main.a')
        main_out = os.path.join(project.basepath, 'main.out')

        self.COMPILER.create_obj(src, main_o, list())
        self.COMPILER.create_archive(main_a, [main_o])
        self.COMPILER.create_executable(main_out, [main_a])

        out = self._execute_binary(main_out)
        assert out == 'Hello from litemake!\n'

    def test_c_with_includes(self, project: 'VirtualProject'):
        project.add_file('main.c', '''
            #include <stdio.h>
            #include <mymath/math.h>

            int main() {
                printf("2 + 2 = %d\\n", add(2,2));
                printf("2 ^ 4 = %d\\n", pow(2, 4));
            }
        ''')

        project.add_file('include/mymath/math.h', '''
            int add(int, int);
            int pow(int, int);
        ''')

        project.add_file('math.c', '''
            #include <mymath/math.h>
            
            int add(int a, int b) { return a + b; };
            int pow(int a, int b) {
                if (b <= 0) { return 1; }
                return a * pow(a, b-1);
            };
        ''')

        with change_cwd(project.basepath):
            self.COMPILER.create_obj('main.c', 'main.o', ['include/'])
            self.COMPILER.create_obj('math.c', 'math.o', ['include/'])
            self.COMPILER.create_archive('main.a', ['main.o', 'math.o'])
            self.COMPILER.create_executable('main.out', ['main.a'])
            out = self._execute_binary('./main.out')

        assert out == '2 + 2 = 4\n2 ^ 4 = 16\n'


class _TestCompilerCPP(_TestCompilerC):

    def test_cpp_hello_world(self, project: 'VirtualProject'):
        src = project.add_file('main.cpp', '''
            #include <iostream>
            
            int main() {
                std::cout << "Hello from litemake!" << std::endl;
            }

        ''')

        obj_dest = os.path.join(project.basepath, 'main.o')
        self.COMPILER.create_obj(src, obj_dest, list())

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
