import os
import typing

from .base import AbstractCompiler


class LlvmCompiler(AbstractCompiler):

    def create_obj(self, src: str, dest: str, includes: typing.List[str]) -> None:
        includes = [f'-I{i}' for i in includes]
        self._exec_cmd(self.name, '-c', src, '-o', dest, *includes)

    def create_archive(self, dest: str, objs: typing.List[str]) -> None:
        self._exec_cmd('llvm-ar', '-crs', dest, *objs)

    def create_executable(self, dest: str, archives: typing.List[str]) -> None:
        self._exec_cmd(self.name, '-o', dest, *archives)


class ClangCompiler(LlvmCompiler):
    name = 'clang'
    required_clis = {'clang', 'llvm-ar'}


class ClangplusplusCompiler(LlvmCompiler):
    name = 'clang++'
    required_clis = {'clang++', 'llvm-ar'}
