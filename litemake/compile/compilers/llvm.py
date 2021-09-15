import os
import typing

from .base import AbstractCompiler


class LlvmCompiler(AbstractCompiler):

    def create_obj(self, src: str, dest: str) -> None:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        self._exec_cmd(self.name, '-c', src, '-o', dest)

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
