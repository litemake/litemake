import typing

import subprocess
from os import path, makedirs

from .exceptions import litemakeCompilationError
from .make import MakeFolder, MakeFile
from .printer import litemakePrinter as Printer


class litemakeCompiler:

    def __init__(self,
                 src: str,
                 dest: str,
                 compiler: str,
                 flags: typing.List[str],
                 objext: str,
                 ) -> None:
        self.src = src
        self.dest = dest
        self.compiler = compiler
        self.flags = flags
        self.objext = objext

    def _compile(self, *args: typing.List[str]) -> None:
        """ Recives a list of strings that represents a command arguments.
        This method will execute the command, and if the return code from the
        command is not 0, will also print a custom error. """

        cmd = [self.compiler] + self.flags + list(args)
        Printer.command(cmd)

        # Execute the command
        # TODO: keep compiling object files even if one of them fails because
        #       of a compilation error.

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise litemakeCompilationError(
                subprocess=self.compiler,
                error_msg=result.stderr,
            )

    def compile_obj(self, filepath: str) -> None:

        src_dir = path.dirname(filepath)
        rel_dir = path.relpath(src_dir, start=self.src)
        dest_dir = path.join(self.dest, rel_dir)

        makedirs(dest_dir, exist_ok=True)

        filename = path.basename(filepath)
        name, ext = path.splitext(filename)

        dest = path.join(dest_dir, name + self.objext)

        # TODO: To support less popular compilers, add the template command
        #       to the configuration setup file, instead of hardcoding '-c'
        #       and '-o' options.
        self._compile('-c', filepath, '-o', dest)
