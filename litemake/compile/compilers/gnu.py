import os
import typing

from .base import AbstractCompiler


class GnuCompiler(AbstractCompiler):
    def create_obj(self, src: str, dest: str, includes: typing.List[str]) -> None:
        includes = [f"-I{i}" for i in includes]
        self._exec_cmd(self.name, "-c", src, "-o", dest, *includes)

    def create_archive(self, dest: str, objs: typing.List[str]) -> None:
        self._exec_cmd("ar", "-crs", dest, *objs)

    def create_executable(self, dest: str, archives: typing.List[str]) -> None:
        self._exec_cmd(self.name, "-o", dest, *archives)


class GccCompiler(GnuCompiler):
    name = "gcc"
    required_clis = {"gcc", "ar"}


class GplusplusCompiler(GnuCompiler):
    name = "g++"
    required_clis = {"g++", "ar"}
