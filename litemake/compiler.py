import typing

import subprocess
from os import path, makedirs

from .exceptions import litemakeCompilationError
from .make import MakeFolder, MakeFile
from .printer import litemakePrinter as Printer


class litemakeCompiler:

    def __init__(self, src: str, dest: str,
                 compiler: str, flags: typing.List[str]) -> None:
        self.src = src
        self.dest = dest
        self.compiler = compiler
        self.flags = flags

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
