import typing

import subprocess
from os import path, makedirs, listdir

from litemake.exceptions import litemakeCompilationError
from litemake.printer import litemakePrinter as Printer


class litemakeCompiler:

    # static counter
    compiled = 0

    def __init__(self,
                 src: str,
                 dest: str,
                 compiler: str,
                 flags: typing.List[str],
                 objsuffix: str,
                 ) -> None:
        self.src = src
        self.dest = dest
        self.compiler = compiler
        self.flags = flags
        self.objsuffix = objsuffix

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

    def src_to_obj_path(self, filepath) -> str:

        src_dir = path.dirname(filepath)
        rel_dir = path.relpath(src_dir, start=self.src)
        dest_dir = path.join(self.dest, rel_dir)

        filename = path.basename(filepath)
        return path.join(dest_dir, filename + self.objsuffix)

    def compile_obj(self, src: str, dest: str) -> None:
        makedirs(path.dirname(dest), exist_ok=True)

        # TODO: To support less popular compilers, add the template command
        #       to the configuration setup file, instead of hardcoding '-c'
        #       and '-o' options.
        self._compile('-c', src, '-o', dest)
        litemakeCompiler.compiled += 1

    def compile_file(self, filepath: str) -> bool:
        """ Recives a path to a source file, and checks if it really needs to
        be compiled. If it does indeed, the file is compiled and the function
        returns `True`. If the file isn't compiled, the returned value is
        `False`. """

        dest = self.src_to_obj_path(filepath)

        if not path.exists(dest) or path.getmtime(filepath) > path.getmtime(dest):
            # Case 1: If object file isn't compiled yet -> we should compile it.
            # Case 2: If the source file is newer then the compiled one, we need
            #         to recompile.

            self.compile_obj(filepath, dest)
            return True
        return False
