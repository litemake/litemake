import typing

import subprocess
from os import path, makedirs, listdir

from .exceptions import litemakeCompilationError
from .printer import litemakePrinter as Printer


class litemakeCompiler:

    def __init__(self,
                 src: str,
                 dest: str,
                 compiler: str,
                 flags: typing.List[str],
                 objext: str,
                 srcext: str,
                 ) -> None:
        self.src = src
        self.dest = dest
        self.compiler = compiler
        self.flags = flags
        self.objext = objext
        self.srcext = srcext

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

    def _dest_filepath(self, filepath) -> str:

        src_dir = path.dirname(filepath)
        rel_dir = path.relpath(src_dir, start=self.src)
        dest_dir = path.join(self.dest, rel_dir)

        filename = path.basename(filepath)
        name, _ = path.splitext(filename)

        return path.join(dest_dir, name + self.objext)

    def compile_obj(self, filepath: str) -> None:

        dest = self._dest_filepath(filepath)
        makedirs(path.dirname(dest), exist_ok=True)

        # TODO: To support less popular compilers, add the template command
        #       to the configuration setup file, instead of hardcoding '-c'
        #       and '-o' options.
        self._compile('-c', filepath, '-o', dest)

    def compile_file(self, filepath: str) -> None:

        if not any(filepath.endswith(ext) for ext in self.srcext):
            # This is not a source file -> nothing to compile! -> exit
            return

        dest = self._dest_filepath(filepath)

        if not path.exists(dest):
            # If object file isn't compiled yet -> we should compile it.
            # TODO: in this case, the '_dest_filepath' function we be called
            #       twice (first time here, and second time in the 'compile_obj'
            #       function). It is possible to cache the result using the
            #       'cache' decorator, or pass the path as a parameter.
            self.compile_obj(filepath)

        if path.getmtime(filepath) > path.getmtime(dest):
            # If the source file is newer then the compiled one, we need
            # to recompile.
            self.compile_obj(filepath)

    def compile_folder(self, src: str) -> None:
        assert path.isdir(src), f"expected directory {src!r}"

        for name in listdir(src):
            cur = path.join(src, name)

            if path.isfile(cur):
                self.compile_file(cur)

            elif path.isdir(cur):
                self.compile_folder(cur)
